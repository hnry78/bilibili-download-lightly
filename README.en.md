# 🎬 Bilibili Light Downloader

A lightweight Bilibili video downloader — no more struggling with the mobile app's cache or the desktop client. Automatically selects the highest available quality, with Cookie login support.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

---

## ✨ Features

- 🚀 Download videos by pasting a link
- 🔍 Auto-detect and select the highest available quality (480P / 720P / 1080P+)
- 🍪 Cookie login support (for high-quality / membership videos)
- 📋 List all available video formats and qualities
- 🔗 Auto-fix malformed Bilibili URLs
- ⚡ Powered by [you-get](https://github.com/soimort/you-get), stable and reliable

## 📦 Installation

### Prerequisites

- **Python** 3.10+
- **ffmpeg** (recommended): for merging audio and video streams. Download and place it in the `ffmpeg/` directory, or add it to your system PATH.

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/hnry78/bilibili-light-downloader.git
cd bilibili-light-downloader

# 2. Create a virtual environment (recommended)
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS / Linux:
# source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

> 💡 You can also install globally with `pip install you-get`, and the script will find it on your system PATH automatically.

## 🚀 Usage

```bash
# List available qualities for a video
python download.py -i "https://www.bilibili.com/video/BV1XX411R7Ff/"

# Download at the highest quality (480P default without login)
python download.py "https://www.bilibili.com/video/BV1XX411R7Ff/"

# Download with Cookie login (supports 720P / 1080P)
python download.py --cookies cookies.txt "https://www.bilibili.com/video/BV1XX411R7Ff/"

# Specify a particular quality
python download.py --format dash-flv720 "https://www.bilibili.com/video/BV1XX411R7Ff/"

# Custom download directory
python download.py -o ./my_videos "https://www.bilibili.com/video/BV1XX411R7Ff/"
```

## 🍪 Getting Cookies

Downloading HD videos (720P+) requires a Bilibili login. To get your cookies:

1. Log in to [bilibili.com](https://www.bilibili.com) in your browser
2. Install a cookie export extension (e.g. [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc))
3. On the Bilibili page, click the extension → export in **Netscape format**
4. Rename the exported file to `cookies.txt` and place it in the project root

> ⚠️ **Security Notice**: Cookies are your login credentials. **Never** commit them to Git or share them with anyone. This project already includes `cookies.txt` in `.gitignore`.

## ⚙️ Advanced Options

| Argument | Short | Description |
|----------|-------|-------------|
| `--cookies FILE` | `-c` | Path to Netscape-format cookie file |
| `--format FMT` | `-f` | Specify quality format ID (e.g. `dash-flv720`) |
| `--info` | `-i` | List available qualities only (no download) |
| `--output DIR` | `-o` | Download directory (default: `./downloads/`) |

### Common Quality Formats

| Format ID | Description |
|-----------|-------------|
| `dash-flv480-HEVC` | 480P (default) |
| `dash-flv720` | 720P HD |
| `dash-flv1080` | 1080P Full HD |
| `dash-av1-4k` | 4K Ultra HD (membership required) |

## ❓ FAQ

**Q: The downloaded file has video but no audio?**
A: You need ffmpeg to merge audio and video streams. Place it in the `ffmpeg/` directory or add it to your system PATH.

**Q: Downloading 720P says I need to log in?**
A: Bilibili restricts HD video access to logged-in users. Export cookies and use `--cookies cookies.txt`.

**Q: Emoji display is broken on Windows?**
A: The script auto-configures UTF-8 output. If your terminal still shows garbled text, run `chcp 65001` to switch to UTF-8 encoding.

## 📄 License

[MIT](LICENSE) © 2026

## 🙏 Credits

- [you-get](https://github.com/soimort/you-get) — the excellent download engine
