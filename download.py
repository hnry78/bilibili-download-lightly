#!/usr/bin/env python3
"""
Bilibili 视频下载器
用法：
    python download.py "https://www.bilibili.com/video/BV1NXJE6EEeJ/"
    python download.py --cookies cookies.txt "https://www.bilibili.com/video/BV1NXJE6EEeJ/"
"""

import argparse
import io
import os
import re
import subprocess
import sys

# Windows 终端 GBK 编码适配（支持 emoji 输出）
if sys.stdout.encoding and sys.stdout.encoding.upper() != "UTF-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.upper() != "UTF-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
VENV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")


def resolve_youget():
    """找到 venv 中的 you-get"""
    candidates = [
        os.path.join(VENV_DIR, "Scripts", "you-get.exe"),
        os.path.join(VENV_DIR, "bin", "you-get"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    # 回退到系统 PATH
    return "you-get"


def resolve_ffmpeg():
    """找到可用的 ffmpeg，优先检查系统 PATH，再检查项目目录"""
    # 1. 优先查系统 PATH（用户自己安装的 ffmpeg）
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return None  # None 表示用系统 PATH
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    # 2. 回退到项目中的 ffmpeg
    ffmpeg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg")
    candidates = [
        os.path.join(ffmpeg_dir, "ffmpeg.exe"),
        os.path.join(ffmpeg_dir, "bin", "ffmpeg.exe"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return os.path.dirname(path)
    return None


def clean_url(raw_url: str) -> str:
    """清理 B站视频链接中的常见错误（重复 BV 号等）"""
    url = raw_url.strip().strip('"').strip("'")
    # 修复重复 BV 号: .../video/BVxxx/BVxxx/... → .../video/BVxxx/...
    url = re.sub(r'(/video/BV[a-zA-Z0-9]+)/BV[a-zA-Z0-9]+', r'\1', url)
    return url


def download_video(url: str, cookies: str | None = None, quality: str = "dash-flv480-HEVC", output_dir: str = DOWNLOAD_DIR):
    os.makedirs(output_dir, exist_ok=True)

    you_get = resolve_youget()
    cmd = [you_get]

    if cookies:
        cookies_path = os.path.abspath(cookies)
        if not os.path.isfile(cookies_path):
            print(f"❌ Cookie 文件不存在: {cookies_path}")
            sys.exit(1)
        cmd.extend(["--cookies", cookies_path])

    cmd.extend(["--format", quality])
    cmd.extend(["-o", output_dir])
    cmd.append(url)

    env = os.environ.copy()
    ffmpeg_dir = resolve_ffmpeg()
    if ffmpeg_dir:
        env["PATH"] = ffmpeg_dir + os.pathsep + env["PATH"]

    print(f"🎬 开始下载: {url}")
    print(f"📁 保存到: {output_dir}")
    if cookies:
        print(f"🍪 使用 Cookie: {cookies}")
    print(f"⚙️  画质: {quality}")
    print("-" * 50)

    result = subprocess.run(cmd, env=env)
    if result.returncode == 0:
        print("-" * 50)
        print("✅ 下载完成！")
    else:
        print("-" * 50)
        print("❌ 下载失败，请检查网络或参数。")
        sys.exit(result.returncode)


def list_formats(url: str, cookies: str | None = None):
    """列出视频可用的清晰度格式"""
    you_get = resolve_youget()
    cmd = [you_get, "-i"]

    if cookies:
        cookies_path = os.path.abspath(cookies)
        if not os.path.isfile(cookies_path):
            print(f"❌ Cookie 文件不存在: {cookies_path}")
            sys.exit(1)
        cmd.extend(["--cookies", cookies_path])

    cmd.append(url)

    env = os.environ.copy()
    ffmpeg_dir = resolve_ffmpeg()
    if ffmpeg_dir:
        env["PATH"] = ffmpeg_dir + os.pathsep + env["PATH"]

    subprocess.run(cmd, env=env)


def get_highest_quality(url: str, cookies: str | None = None) -> str | None:
    """自动检测视频可用的最高画质，返回格式 ID"""

    you_get = resolve_youget()
    cmd = [you_get, "-i"]

    if cookies:
        cookies_path = os.path.abspath(cookies)
        if not os.path.isfile(cookies_path):
            print(f"❌ Cookie 文件不存在: {cookies_path}")
            sys.exit(1)
        cmd.extend(["--cookies", cookies_path])

    cmd.append(url)

    env = os.environ.copy()
    ffmpeg_dir = resolve_ffmpeg()
    if ffmpeg_dir:
        env["PATH"] = ffmpeg_dir + os.pathsep + env["PATH"]

    result = subprocess.run(cmd, env=env, capture_output=True)
    # 用二进制捕获，手动 UTF-8 解码（避免 Windows GBK 编码错误）
    raw = result.stderr or result.stdout or b""
    output = raw.decode("utf-8", errors="replace")

    # 剥离 ANSI 转义码（颜色标记）
    output = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', output)

    # 解析多行格式：
    #   - format:        dash-flv480-HEVC
    #     container:     mp4
    #     quality:       清晰 480P hvc1...
    #     size:          106.0 MiB
    formats = []
    lines = output.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        fmt_match = re.search(r'-\s*format:\s*(\S+)', line)
        if fmt_match:
            fmt_id = fmt_match.group(1).strip()
            # 往后找 quality 行（通常隔 2 行）
            for j in range(i + 1, min(i + 5, len(lines))):
                qual_match = re.search(r'quality:\s*(.*)', lines[j])
                if qual_match:
                    desc = qual_match.group(1)
                    res_match = re.search(r'(\d{3,4})\s*[Pp]', desc)
                    if res_match:
                        res = int(res_match.group(1))
                        # 编码优先级：AV1 > HEVC > AVC
                        codec = 0
                        if "av1" in fmt_id.lower():
                            codec = 2
                        elif "hevc" in fmt_id.lower():
                            codec = 1
                        formats.append((res, codec, fmt_id))
                    break
        i += 1

    if not formats:
        return None

    # 按分辨率降序，同分辨率按编码质量降序
    formats.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return formats[0][2]


def main():
    parser = argparse.ArgumentParser(
        description="Bilibili 视频下载器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 查看可用画质
  python download.py -i "https://www.bilibili.com/video/BV1NXJE6EEeJ/"

  # 下载最高画质（未登录默认 480P）
  python download.py "https://www.bilibili.com/video/BV1NXJE6EEeJ/"

  # 使用 Cookie 下载高清（720P/1080P 需要登录）
  python download.py --cookies cookies.txt "https://www.bilibili.com/video/BV1NXJE6EEeJ/"

  # 指定画质下载
  python download.py --format dash-flv720 "https://www.bilibili.com/video/BV1NXJE6EEeJ/"
        """,
    )
    parser.add_argument("url", help="Bilibili 视频链接")
    parser.add_argument("--cookies", "-c", help="Netscape 格式的 Cookie 文件路径")
    parser.add_argument("--format", "-f", default=None,
                        help="画质格式（不指定则自动选择最高画质）")
    parser.add_argument("--info", "-i", action="store_true",
                        help="列出视频可用的画质格式（不下载）")
    parser.add_argument("--output", "-o", default=DOWNLOAD_DIR,
                        help=f"下载目录（默认: {DOWNLOAD_DIR}）")

    args = parser.parse_args()

    # 清理 URL 中的常见错误
    original_url = args.url
    args.url = clean_url(args.url)
    if original_url != args.url:
        print(f"🔗 已自动修正链接: {args.url}")

    if args.info:
        list_formats(args.url, args.cookies)
    else:
        fmt = args.format
        if fmt is None:
            print("🔍 正在自动检测可用画质...")
            fmt = get_highest_quality(args.url, args.cookies)
            if fmt:
                print(f"✅ 已选择最高画质: {fmt}")
            else:
                fmt = "dash-flv480-HEVC"  # fallback
                print(f"⚠️  未能检测画质，使用默认: {fmt}")
        download_video(args.url, args.cookies, fmt, args.output)


if __name__ == "__main__":
    main()
