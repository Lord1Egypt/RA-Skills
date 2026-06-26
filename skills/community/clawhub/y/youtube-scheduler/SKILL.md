---
name: youtube-scheduler
description: Phân tích lịch đăng video của kênh YouTube để tìm "khung giờ vàng" — thời điểm đăng có nhiều view và engagement nhất. Dùng khi user yêu cầu "Tìm giờ vàng đăng video @Channel", "Best time to post for @Channel", "Kênh này hay đăng lúc mấy giờ", hoặc muốn tối ưu lịch đăng nội dung.
---

# ⏰ YouTube Scheduler Analyzer

Phân tích lịch đăng của kênh → tìm ngày và giờ có hiệu suất cao nhất.

## Cài đặt

### Cách 1 — Tải skill thẳng từ GitHub (khuyến nghị)

```powershell
# Windows
$skillDir = "$env:USERPROFILE\.agents\skills\youtube-scheduler"
New-Item -ItemType Directory -Force "$skillDir\scripts" | Out-Null
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/mcbaivn/openclaw-skills-mcbai/main/skills/youtube/youtube-scheduler/SKILL.md" -OutFile "$skillDir\SKILL.md"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/mcbaivn/openclaw-skills-mcbai/main/skills/youtube/youtube-scheduler/scripts/analyze_schedule.py" -OutFile "$skillDir\scripts\analyze_schedule.py"
```

```bash
# macOS / Linux
mkdir -p ~/.agents/skills/youtube-scheduler/scripts
curl -o ~/.agents/skills/youtube-scheduler/SKILL.md \
  https://raw.githubusercontent.com/mcbaivn/openclaw-skills-mcbai/main/skills/youtube/youtube-scheduler/SKILL.md
curl -o ~/.agents/skills/youtube-scheduler/scripts/analyze_schedule.py \
  https://raw.githubusercontent.com/mcbaivn/openclaw-skills-mcbai/main/skills/youtube/youtube-scheduler/scripts/analyze_schedule.py
```

### Cách 2 — Clone toàn bộ repo

```powershell
# Windows
git clone https://github.com/mcbaivn/openclaw-skills-mcbai.git
Copy-Item -Recurse openclaw-skills-mcbai\skills\youtube\youtube-scheduler $env:USERPROFILE\.agents\skills\
```

```bash
# macOS / Linux
git clone https://github.com/mcbaivn/openclaw-skills-mcbai.git
cp -r openclaw-skills-mcbai/skills/youtube/youtube-scheduler ~/.agents/skills/
```

## Sử dụng

```
python scripts/analyze_schedule.py <channel_url> [--limit N] [--tz Asia/Ho_Chi_Minh]
```

**Ví dụ:**
- `Tìm giờ vàng @MrBeast` → `python scripts/analyze_schedule.py https://youtube.com/@MrBeast --limit 50`
- Đổi timezone → thêm `--tz Asia/Ho_Chi_Minh` (mặc định UTC)

## Output

```
Youtube_Schedule/
└── [Channel]_schedule_DD_MM_YYYY.txt
```

**Báo cáo gồm:**
- 📅 Ngày trong tuần tốt nhất (sắp xếp theo avg views)
- ⏰ Khung giờ vàng (0-23h, theo avg views)
- 🗺️ Heatmap Ngày × Giờ (ASCII)
- 🏆 Top 5 video views cao nhất với ngày/giờ đăng
- 💡 Khuyến nghị lịch đăng tối ưu

## Lưu ý
- Phân tích dựa trên `--limit` video gần nhất (khuyến nghị 30-100 video).
- Mặc định timezone UTC, dùng `--tz` để chuyển sang giờ địa phương.
- Kết quả là ước tính thống kê từ dữ liệu lịch sử, không phải đảm bảo tuyệt đối.
