#!/usr/bin/env python3
"""
FFmpeg 自动下载器
当系统中未找到 ffmpeg 时，自动下载 Windows 官方构建版本到项目 ffmpeg/ 目录。
"""

import os
import sys
import urllib.request
import zipfile
import shutil
import tempfile
import subprocess

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
FFMPEG_DIR = os.path.join(PROJECT_DIR, "ffmpeg")
FFMPEG_EXE = os.path.join(FFMPEG_DIR, "ffmpeg.exe")

# Windows ffmpeg 官方构建（ffmpeg.org 推荐的 gyan.dev 构建）
FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"


def is_ffmpeg_on_path() -> bool:
    """检查 ffmpeg 是否在系统 PATH 中可用。"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def find_ffmpeg_in_project() -> str | None:
    """在项目目录中查找 ffmpeg.exe。"""
    candidates = [
        FFMPEG_EXE,
        os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return os.path.dirname(path)
    return None


def _download_with_progress(url: str, dest: str):
    """带进度条的下载。"""
    last_percent = -1

    def report(block_num, block_size, total_size):
        nonlocal last_percent
        if total_size > 0:
            percent = int(block_num * block_size * 100 / total_size)
            if percent != last_percent:
                last_percent = percent
                downloaded_mb = block_num * block_size / 1024 / 1024
                total_mb = total_size / 1024 / 1024
                sys.stdout.write(
                    f"\r⏬ 下载中... {percent}% "
                    f"({downloaded_mb:.1f}MB / {total_mb:.1f}MB)"
                )
                sys.stdout.flush()

    print("⏬ 正在下载 ffmpeg（约 50MB）...")
    urllib.request.urlretrieve(url, dest, report)
    print("\n✅ 下载完成")


def download_ffmpeg() -> str | None:
    """
    下载 ffmpeg 并解压到项目目录。
    返回 ffmpeg.exe 所在目录，失败返回 None。
    """
    os.makedirs(FFMPEG_DIR, exist_ok=True)

    zip_path = os.path.join(tempfile.gettempdir(), "ffmpeg-release-essentials.zip")

    try:
        # 1. 下载
        _download_with_progress(FFMPEG_URL, zip_path)

        # 2. 解压
        print("📦 正在解压...")
        with zipfile.ZipFile(zip_path, "r") as zf:
            exe_members = [m for m in zf.namelist() if m.endswith("ffmpeg.exe")]
            if not exe_members:
                print("❌ 压缩包中未找到 ffmpeg.exe")
                return None

            extract_dir = os.path.join(tempfile.gettempdir(), "ffmpeg_extract")
            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir)

            zf.extractall(extract_dir)

            # 3. 找到 ffmpeg.exe 并复制到项目目录
            for root, _, files in os.walk(extract_dir):
                if "ffmpeg.exe" in files:
                    src = os.path.join(root, "ffmpeg.exe")
                    shutil.copy2(src, FFMPEG_EXE)
                    print(f"✅ ffmpeg 已安装到: {FFMPEG_EXE}")

                    # 清理临时文件
                    shutil.rmtree(extract_dir, ignore_errors=True)
                    try:
                        os.remove(zip_path)
                    except OSError:
                        pass

                    return FFMPEG_DIR

        print("❌ 未能找到 ffmpeg.exe")
        return None

    except Exception as e:
        print(f"❌ 下载 ffmpeg 失败: {e}")
        for p in [zip_path]:
            try:
                if os.path.exists(p):
                    os.remove(p)
            except OSError:
                pass
        return None


def ensure_ffmpeg() -> str | None:
    """
    确保 ffmpeg 可用。
    检查顺序：系统 PATH → 项目目录 → 自动下载。
    返回需要添加到 PATH 的目录，如果在系统 PATH 中找到则返回 None。
    """
    # 1. 优先使用系统 PATH 中的 ffmpeg
    if is_ffmpeg_on_path():
        return None

    # 2. 检查项目目录
    ffmpeg_dir = find_ffmpeg_in_project()
    if ffmpeg_dir:
        return ffmpeg_dir

    # 3. 自动下载
    print("🔍 未找到 ffmpeg，正在自动下载...")
    return download_ffmpeg()


if __name__ == "__main__":
    """单独运行此脚本也可手动下载 ffmpeg"""
    result = ensure_ffmpeg()
    if result is None:
        print("✅ ffmpeg 已在系统 PATH 中可用")
    elif result:
        print(f"✅ ffmpeg 已就绪: {result}")
    else:
        print("❌ ffmpeg 安装失败，请手动下载")
        sys.exit(1)
