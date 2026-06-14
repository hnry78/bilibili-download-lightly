# 🎬 Bilibili Downloader

一键下载 Bilibili 视频，自动选择最高画质，支持登录 Cookie。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

---

## ✨ 功能

- 🚀 输入链接一键下载
- 🔍 自动检测并选择最高可用画质（480P / 720P / 1080P+）
- 🍪 Cookie 登录支持（下载高清/大会员视频）
- 📋 查看视频所有可用画质格式
- 🔗 自动纠正畸形 B 站链接
- ⚡ 基于 [you-get](https://github.com/soimort/you-get)，稳定可靠

## 📦 安装

### 前置要求

- **Python** 3.10+
- **ffmpeg**（推荐）：用于合并音视频流。下载后放入项目 `ffmpeg/` 目录，或添加到系统 PATH。

### 步骤

```bash
# 1. 克隆仓库
git clone https://github.com/hnry78/bilibili-light-downloader.git
cd bilibili-light-downloader

# 2. 创建虚拟环境（推荐）
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS / Linux:
# source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

> 💡 也可以全局安装 `pip install you-get`，脚本会自动在系统 PATH 中找到它。

## 🚀 使用

```bash
# 查看视频可用画质
python download.py -i "https://www.bilibili.com/video/BV1XX411R7Ff/"

# 下载最高画质（未登录默认 480P）
python download.py "https://www.bilibili.com/video/BV1XX411R7Ff/"

# 使用 Cookie 登录后下载（支持 720P / 1080P）
python download.py --cookies cookies.txt "https://www.bilibili.com/video/BV1XX411R7Ff/"

# 指定画质下载
python download.py --format dash-flv720 "https://www.bilibili.com/video/BV1XX411R7Ff/"

# 自定义下载目录
python download.py -o ./my_videos "https://www.bilibili.com/video/BV1XX411R7Ff/"
```

## 🍪 获取 Cookie

下载高清视频（720P 以上）需要 B 站登录状态。获取 Cookie 文件的方法：

1. 在浏览器中登录 [bilibili.com](https://www.bilibili.com)
2. 安装 Cookie 导出扩展（如 [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)）
3. 在 B 站页面点击扩展 → 导出为 **Netscape 格式**
4. 将导出的文件重命名为 `cookies.txt` 放在项目根目录

> ⚠️ **安全提醒**：Cookie 等于你的登录凭证，**切勿**提交到 Git 仓库，也**不要**分享给他人。本项目已将 `cookies.txt` 加入 `.gitignore`。

## ⚙️ 高级选项

| 参数 | 简写 | 说明 |
|------|------|------|
| `--cookies FILE` | `-c` | Cookie 文件路径（Netscape 格式） |
| `--format FMT` | `-f` | 指定画质格式 ID（如 `dash-flv720`） |
| `--info` | `-i` | 仅列出可用画质，不下载 |
| `--output DIR` | `-o` | 下载目录（默认: `./downloads/`） |

### 常见画质格式

| 格式 ID | 说明 |
|---------|------|
| `dash-flv480-HEVC` | 480P 清晰（默认） |
| `dash-flv720` | 720P 高清 |
| `dash-flv1080` | 1080P 全高清 |
| `dash-av1-4k` | 4K 超清（需大会员） |

## ❓ 常见问题

**Q: 下载的文件只有画面没有声音？**
A: 需要安装 ffmpeg 来合并音视频流。放入 `ffmpeg/` 目录或添加到系统 PATH。

**Q: 下载 720P 提示需要登录？**
A: B 站对高清视频有登录限制。请导出 Cookie 后使用 `--cookies cookies.txt`。

**Q: Windows 下 emoji 显示乱码？**
A: 脚本已自动适配 UTF-8 输出。如果终端仍显示异常，请运行 `chcp 65001` 切换为 UTF-8 编码。

## 📄 许可证

[MIT](LICENSE) © 2026

## 🙏 致谢

- [you-get](https://github.com/soimort/you-get) — 优秀的下载引擎
