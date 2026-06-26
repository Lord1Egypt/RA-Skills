---
name: youtube-subtitle-extractor
description: Tải phụ đề (SRT/VTT/TXT) từ video YouTube bằng yt-dlp. Hỗ trợ auto-generated và manual subtitles, đa ngôn ngữ. Dùng khi user yêu cầu "Tải phụ đề video X", "Get subtitles from [URL]", "Extract SRT from @Channel", hoặc cần file phụ đề để phân tích nội dung.
---

# 📥 YouTube Subtitle Extractor

Tải phụ đề từ video hoặc kênh YouTube, xuất ra file `.srt` sạch.

## Cài đặt

### Cách 1 — Tải skill thẳng từ GitHub (khuyến nghị)

```powershell
# Windows
$skillDir = "$env:USERPROFILE\.agents\skills\youtube-subtitle-extractor"
New-Item -ItemType Directory -Force "$skillDir\scripts" | Out-Null
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/mcbaivn/openclaw-skills-mcbai/main/skills/youtube/youtube-subtitle-extractor/SKILL.md" -OutFile "$skillDir\SKILL.md"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/mcbaivn/openclaw-skills-mcbai/main/skills/youtube/youtube-subtitle-extractor/scripts/extract_subtitles.py" -OutFile "$skillDir\scripts\extract_subtitles.py"
```

```bash
# macOS / Linux
mkdir -p ~/.agents/skills/youtube-subtitle-extractor/scripts
curl -o ~/.agents/skills/youtube-subtitle-extractor/SKILL.md \
  https://raw.githubusercontent.com/mcbaivn/openclaw-skills-mcbai/main/skills/youtube/youtube-subtitle-extractor/SKILL.md
curl -o ~/.agents/skills/youtube-subtitle-extractor/scripts/extract_subtitles.py \
  https://raw.githubusercontent.com/mcbaivn/openclaw-skills-mcbai/main/skills/youtube/youtube-subtitle-extractor/scripts/extract_subtitles.py
```

### Cách 2 — Clone toàn bộ repo

```powershell
# Windows
git clone https://github.com/mcbaivn/openclaw-skills-mcbai.git
Copy-Item -Recurse openclaw-skills-mcbai\skills\youtube\youtube-subtitle-extractor $env:USERPROFILE\.agents\skills\
```

```bash
# macOS / Linux
git clone https://github.com/mcbaivn/openclaw-skills-mcbai.git
cp -r openclaw-skills-mcbai/skills/youtube/youtube-subtitle-extractor ~/.agents/skills/
```

## Sử dụng

```
python scripts/extract_subtitles.py <video_or_channel_url> [--lang vi,en] [--format srt] [--auto]
```

**Ví dụ:**
- `Tải phụ đề từ https://youtu.be/xxxx` → `python scripts/extract_subtitles.py https://youtu.be/xxxx`
- `Tải phụ đề tiếng Việt` → thêm `--lang vi`
- Chỉ lấy auto-generated → thêm `--auto`

## Output

```
Youtube_Subtitles/
└── [Video_Title]/
    ├── [title].vi.srt
    ├── [title].en.srt
    └── [title]_plain.txt    (plain text không có timestamp)
```

## Lưu ý
- Ưu tiên manual subtitles trước, fallback sang auto-generated nếu không có.
- File `_plain.txt` dùng để đưa vào `youtube-content-analyzer`.
- Nếu URL là kênh, tải phụ đề tất cả video trong kênh (giới hạn với `--limit N`).
