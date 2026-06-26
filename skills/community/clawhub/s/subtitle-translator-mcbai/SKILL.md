---
name: subtitle-translator-mcbai
description: Translate SRT subtitle files into any target language using AI. Processes subtitles in batches to handle large files efficiently, preserves exact SRT format and timing, and outputs a new translated SRT file. Use this skill when the user wants to translate subtitles, translate an SRT file, dịch phụ đề, dịch file srt, translate movie subtitles, or asks to convert subtitles to another language. Triggers on phrases like "dịch phụ đề", "translate subtitles", "dịch file srt", "translate srt", "dịch sang tiếng Việt", or when user uploads/pastes an SRT file and asks for translation.
---

# 🌐 Subtitle Translator - MCB AI

Dịch file SRT sang bất kỳ ngôn ngữ nào. Xử lý theo lô (batch), giữ nguyên format và timing SRT, xuất file SRT mới.

## Cài đặt

```bash
npx clawhub@latest install subtitle-translator-mcbai
```

## Cách dùng

```
Dịch file phụ đề này sang tiếng Việt: [đường dẫn file .srt]
Translate this subtitle to English: [path/to/file.srt]
```

Hoặc paste nội dung SRT trực tiếp vào chat và yêu cầu dịch.

## Tùy chọn

| Tham số | Mặc định | Mô tả |
|---------|---------|-------|
| Ngôn ngữ đích | Vietnamese | Bất kỳ ngôn ngữ nào |
| Batch size | 50 dòng | Số dòng mỗi lần gọi AI |
| Output | Cùng thư mục + `_vi` | Tên file output |

## Workflow

1. **Parse** file SRT (tự detect encoding: UTF-8, GBK, Shift-JIS, v.v.)
2. **Chia batch** — mỗi batch 50 dòng, dịch song song
3. **Build** — ghép lại thành file SRT chuẩn với timecode gốc
4. **Xuất** file `[tên gốc]_[lang].srt`

## Lưu ý
- Giữ nguyên toàn bộ timecode gốc
- HTML tags (`<i>`, `<b>`) được giữ nguyên, chỉ dịch text bên trong
- File lớn (>500 dòng): báo ước tính thời gian trước khi chạy
