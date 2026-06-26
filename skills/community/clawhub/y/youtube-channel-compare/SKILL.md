---
name: youtube-channel-compare
description: So sánh 2-5 kênh YouTube theo views, engagement rate, trending score và tần suất đăng bài. Dùng khi user hỏi "So sánh @KênhA vs @KênhB", "Kênh nào mạnh hơn trong niche X", hoặc cần dữ liệu phân tích cạnh tranh.
---

# 📊 YouTube Channel Compare

So sánh hiệu suất của nhiều kênh YouTube và tạo báo cáo benchmark.

## Cài đặt

### Cách 1 — Tải skill thẳng từ GitHub (khuyến nghị)

```powershell
# Windows
$skillDir = "$env:USERPROFILE\.agents\skills\youtube-channel-compare"
New-Item -ItemType Directory -Force "$skillDir\scripts" | Out-Null
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/mcbaivn/openclaw-skills-mcbai/main/skills/youtube/youtube-channel-compare/SKILL.md" -OutFile "$skillDir\SKILL.md"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/mcbaivn/openclaw-skills-mcbai/main/skills/youtube/youtube-channel-compare/scripts/compare_channels.py" -OutFile "$skillDir\scripts\compare_channels.py"
```

```bash
# macOS / Linux
mkdir -p ~/.agents/skills/youtube-channel-compare/scripts
curl -o ~/.agents/skills/youtube-channel-compare/SKILL.md \
  https://raw.githubusercontent.com/mcbaivn/openclaw-skills-mcbai/main/skills/youtube/youtube-channel-compare/SKILL.md
curl -o ~/.agents/skills/youtube-channel-compare/scripts/compare_channels.py \
  https://raw.githubusercontent.com/mcbaivn/openclaw-skills-mcbai/main/skills/youtube/youtube-channel-compare/scripts/compare_channels.py
```

### Cách 2 — Clone toàn bộ repo

```powershell
# Windows
git clone https://github.com/mcbaivn/openclaw-skills-mcbai.git
Copy-Item -Recurse openclaw-skills-mcbai\skills\youtube\youtube-channel-compare $env:USERPROFILE\.agents\skills\
```

```bash
# macOS / Linux
git clone https://github.com/mcbaivn/openclaw-skills-mcbai.git
cp -r openclaw-skills-mcbai/skills/youtube/youtube-channel-compare ~/.agents/skills/
```

## Sử dụng

```
python scripts/compare_channels.py <url1> <url2> [url3...] [--limit N]
```

**Ví dụ:**
- `So sánh @MrBeast vs @PewDiePie` → `python scripts/compare_channels.py https://youtube.com/@MrBeast https://youtube.com/@PewDiePie --limit 20`

## Output

```
Youtube_Compare/
└── compare_[Kênh1]_vs_[Kênh2]_DD_MM_YYYY.txt
```

**Báo cáo gồm:**

| Chỉ số | Kênh A | Kênh B |
|--------|--------|--------|
| Avg Views | ... | ... |
| Avg Likes | ... | ... |
| Avg Comments | ... | ... |
| Trending Score | ... | ... |
| Tần suất đăng | ... | ... |
| Engagement Rate | ... | ... |

**Trending Score**: `(Views × 0.6) + (Likes × 0.3) + (Comments × 0.1)` chuẩn hóa 1-100

## Lưu ý
- Mặc định lấy 20 video gần nhất mỗi kênh (dùng `--limit` để thay đổi).
- Kênh không có stats công khai sẽ hiển thị N/A.
