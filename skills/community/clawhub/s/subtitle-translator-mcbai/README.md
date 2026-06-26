# subtitle-translator — Dịch file SRT phụ đề sang bất kỳ ngôn ngữ nào

> Skill OpenClaw dịch file SRT phụ đề phim/video sang bất kỳ ngôn ngữ nào. Xử lý theo lô thông minh, giữ nguyên timecode và format SRT, xuất file SRT mới sẵn sàng dùng.

---

## Skill này dùng để làm gì?

Bạn có file phụ đề tiếng Anh muốn xem bằng tiếng Việt? Hay ngược lại? Skill này giúp bạn:
- Dịch toàn bộ file SRT sang ngôn ngữ bạn chọn
- Giữ nguyên 100% timecode — không bao giờ lệch phụ đề
- Xử lý theo lô để không bị giới hạn độ dài
- Dùng AI dịch tự nhiên kiểu điện ảnh, không dịch máy cứng nhắc
- Xuất file SRT mới ngay lập tức

---

## Tính năng

| Tính năng | Chi tiết |
|-----------|---------|
| 🌐 Đa ngôn ngữ | Dịch sang bất kỳ ngôn ngữ nào (Vietnamese, English, Japanese, Korean...) |
| ⏱️ Giữ nguyên timecode | 100% timing được bảo toàn |
| 📦 Batch processing | Xử lý theo lô, không giới hạn độ dài file |
| 🎬 Cinematic translation | Prompt được tối ưu cho ngôn ngữ điện ảnh tự nhiên |
| 🔄 Retry tự động | Tự retry nếu AI trả về JSON lỗi |
| 💾 Output SRT | Xuất file SRT chuẩn, đặt tên theo ngôn ngữ đích |

---

## Cài đặt

### Yêu cầu
- Python 3.8+
- OpenClaw đã cài đặt

```powershell
# Windows
Copy-Item -Recurse subtitle-translator $env:USERPROFILE\.agents\skills\

# macOS / Linux
cp -r subtitle-translator ~/.agents/skills/
```

---

## Cách dùng

### Đơn giản nhất
```
Dịch file này sang tiếng Việt: C:\Downloads\movie.srt
```

### Chỉ định đầy đủ
```
Dịch file phụ đề sang tiếng Nhật, batch 30 dòng: /path/to/subtitle.srt
```

### Paste nội dung SRT trực tiếp
```
Dịch phụ đề này sang tiếng Hàn:
1
00:00:01,000 --> 00:00:03,000
Hello world

2
00:00:04,000 --> 00:00:06,000
How are you?
```

---

## Ngôn ngữ đích phổ biến

`Vietnamese` · `English` · `Japanese` · `Korean` · `Chinese Simplified` · `Chinese Traditional` · `French` · `Spanish` · `German` · `Thai` · `Indonesian`

---

## Output

File SRT được lưu cùng thư mục file gốc, thêm suffix ngôn ngữ:
```
movie.srt          → movie_vi.srt  (Vietnamese)
movie.srt          → movie_ja.srt  (Japanese)
movie.srt          → movie_en.srt  (English)
```

---

## Cấu trúc files

```
subtitle-translator/
├── README.md              ← Bạn đang đọc
├── SKILL.md               ← Điều khiển agent
└── scripts/
    ├── parse-srt.py       ← Parse SRT → JSON array
    └── build-srt.py       ← JSON array → SRT file mới
```

---

<p align="center">
  <a href="https://www.mcbai.vn">MCB AI</a> &nbsp;·&nbsp;
  <a href="https://www.youtube.com/@mcbaivn">YouTube</a> &nbsp;·&nbsp;
  <a href="https://openclaw.mcbai.vn">OpenClaw Cheatsheet</a> &nbsp;·&nbsp;
  <a href="https://openclaw.mcbai.vn/openclaw101">Khoá học OpenClaw 101</a> &nbsp;·&nbsp;
  <a href="https://www.facebook.com/groups/openclawxvn">Cộng đồng Facebook</a> &nbsp;·&nbsp;
  <a href="https://zalo.me/g/mmqkhi259">MCB AI Academy (Zalo)</a>
</p>
