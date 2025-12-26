# Snapchat Metadata Fixer 📅

Fix the metadata on your downloaded Snapchat memories so your photo library shows the correct dates!

<p align="center">
  <a href="https://buymeacoffee.com/ethanshoforost">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="150">
  </a>
</p>

---

## 🎯 What Does This Do?

When you download Snapchat memories, the files are named with the correct date (like `2024-03-15_14-30-45.jpg`), but the **metadata** shows today's date (when you downloaded them). This messes up your photo library sorting!

**This tool fixes that** by reading the date from the filename and writing it to the file's metadata.

### ✨ Features

- 📸 **Photos** - Writes proper EXIF metadata (`DateTimeOriginal`, etc.)
- 🎥 **Videos** - Updates file timestamps (or full metadata with FFmpeg)
- 🔄 **Batch Processing** - Fixes entire folders at once
- 📊 **Progress Tracking** - Shows live progress and stats
- ✅ **Safe** - Modifies files in place (make backups first!)

---

## 📥 Download

### Windows
Download: [`Snapchat_Metadata_Fixer.pyw`](https://github.com/ethanshoforost/snapchat-metadata-fixer/releases/latest)

### macOS
Download: [`Snapchat_Metadata_Fixer.py`](https://github.com/ethanshoforost/snapchat-metadata-fixer/releases/latest)

---

## 🚀 Quick Start

### Windows:
1. **Install Python 3.11.9:** [Download here](https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe)
   - ⚠️ **CHECK "Add Python to PATH"**
2. Download `Snapchat_Metadata_Fixer.pyw`
3. Double-click to run
4. Select your memories folder
5. Click "Fix Metadata"
6. Done! ✨

### Mac:
1. **Install Python 3.11.9:** [Download here](https://www.python.org/ftp/python/3.11.9/python-3.11.9-macos11.pkg)
2. Download `Snapchat_Metadata_Fixer.py`
3. Double-click to run (or `python3 Snapchat_Metadata_Fixer.py`)
4. Select your memories folder
5. Click "Fix Metadata"
6. Done! ✨

**First run:** The tool will automatically install required libraries (`piexif`, `Pillow`).

---

## 🎥 Video Metadata (Optional)

For **full video metadata support**, install FFmpeg:

### Windows:
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

### Mac:
```bash
brew install ffmpeg
```

**Note:** The tool works without FFmpeg - it just updates file timestamps instead of internal metadata for videos.

---

## 🔐 Privacy & Security

- ✅ **Everything Local** - Runs entirely on your computer
- ✅ **No Data Collection** - Zero analytics or tracking
- ✅ **No Internet** - Doesn't need network access
- ✅ **Open Source** - Review the code yourself

---

## 🛠️ How It Works

1. **Scans folder** - Finds files matching pattern: `YYYY-MM-DD_HH-MM-SS.*`
2. **Parses date** - Reads date from filename
3. **Writes metadata:**
   - **Photos (.jpg, .jpeg):** EXIF data (`DateTimeOriginal`, `DateTime`, `DateTimeDigitized`)
   - **Videos (.mp4, .mov):** File timestamps (or full metadata with FFmpeg)
4. **Updates file times** - Sets modification time to match

---

## 📋 Use Cases

### If You Used Old Memory Manager (v1.0.x)
Downloaded memories before metadata fixing was added? Run this tool to fix your existing files!

### If You Use Memory Manager v1.1.0+
New downloads already have correct metadata! But you can still use this tool if you want full video metadata support (with FFmpeg).

---

## ⚠️ Important Notes

- **Make backups** - This tool modifies your original files
- **Test first** - Try on a few files before processing everything
- **File pattern required** - Only works on files named `YYYY-MM-DD_HH-MM-SS.*`

---

## 🐛 Troubleshooting

### "No files found"
- Make sure files are named like: `2024-03-15_14-30-45.jpg`
- Check you selected the correct folder

### "Python not found"
- Install Python 3.11.9 and check "Add to PATH"

### Libraries won't install
```bash
# Windows
python -m pip install piexif Pillow

# Mac
pip3 install piexif Pillow
```

### Videos not getting full metadata
- Install FFmpeg (optional)
- Without FFmpeg, only file timestamps are updated (still works for most apps!)

---

## 🤝 Contributing

Found a bug? Have a feature request? Open an issue or submit a pull request!

---

## ⚖️ Legal

This software is provided under the MIT License. By using this software, you agree to the terms of the [LICENSE](LICENSE) and acknowledge that the creator is not liable for any damages or issues that may arise from its use.

**Key Points:**
- Software is provided "AS IS" without warranty of any kind
- Use at your own risk - make backups before using
- Creator is not liable for any damages or data loss
- This tool modifies your files directly

---

## ⚠️ Disclaimer

This tool is **not affiliated with, endorsed by, or connected to Snapchat Inc.**

Use at your own risk. Make sure you have backups of your files before using this tool.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Ethan Shoforost

---

## ☕ Support

If this tool helped you organize your memories, consider buying me a coffee!

<a href="https://buymeacoffee.com/ethanshoforost">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="150">
</a>

Your support helps maintain and improve this project! 🙏

---

## 📧 Contact

Created by **Ethan Shoforost**

- GitHub: [@ethanshoforost](https://github.com/ethanshoforost)
- Support: [Buy Me a Coffee](https://buymeacoffee.com/ethanshoforost)

---

<p align="center">
  <strong>Happy Memory Organizing! 📸✨</strong>
</p>
