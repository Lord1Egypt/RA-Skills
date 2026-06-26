---
name: smart-speak
description: Chuyển đổi văn bản đa ngôn ngữ (Việt - Hoa - Anh) thành giọng nói chuẩn xác. Tự động xử lý Pinyin và ghép nối âm thanh chất lượng cao. Yêu cầu cài đặt edge-tts và ffmpeg.
---

# Smart-Speak: Trợ lý Giọng nói Đa ngôn ngữ

Skill này giúp em tạo ra các file âm thanh bài giảng hoặc thông báo chất lượng cao, kết hợp mượt mà giữa tiếng Việt, tiếng Hoa (bao gồm cả Pinyin) và tiếng Anh.

## Yêu cầu hệ thống

Để skill này hoạt động hoàn hảo, máy của anh cần được trang bị các công cụ sau:

1.  **Python 3**: Nền tảng để chạy script xử lý.
2.  **edge-tts**: Thư viện cung cấp giọng đọc AI cực kỳ tự nhiên của Microsoft Edge.
3.  **ffmpeg**: Bộ công cụ mạnh mẽ để ghép nối các đoạn âm thanh.

### Lệnh cài đặt nhanh (cho Linux/Ubuntu)

Anh chạy các dòng lệnh sau trong terminal để chuẩn bị nhé:

```bash
# Cài đặt ffmpeg
sudo apt update && sudo apt install -y ffmpeg

# Cài đặt edge-tts
python3 -m pip install edge-tts
```

## Tính năng nổi bật

1.  **Xử lý Pinyin thông minh:** Tự động nhận diện và chuyển đổi Pinyin sang Hán tự trước khi đọc để đảm bảo thanh điệu chuẩn xác 100%.
2.  **Phân đoạn ngôn ngữ:** Tự động chia nhỏ văn bản thành các khối ngôn ngữ riêng biệt để áp dụng đúng giọng đọc bản ngữ.
3.  **Giọng đọc ưu tiên:**
    *   🇻🇳 Tiếng Việt: `vi-VN-HoaiMyNeural` (Dịu dàng, truyền cảm)
    *   🇨🇳 Tiếng Hoa: `zh-CN-XiaoxiaoNeural` (Chuẩn giọng Bắc Kinh)
    *   🇺🇸 Tiếng Anh: `en-US-AvaNeural` (Tự nhiên, hiện đại)

## Quy trình thực hiện

1.  **Phân tích:** Tách câu thành các đoạn dựa trên ngôn ngữ.
2.  **Chuyển đổi:** Chuyển các đoạn Pinyin sang Hán tự (ví dụ: "Nǐ hǎo" -> "你好").
3.  **Tổng hợp:** Gọi `smart_speak.py` để tạo từng đoạn âm thanh nhỏ và dùng `ffmpeg` ghép lại thành một file `.mp3` duy nhất.

## Lệnh thực thi mẫu

```bash
python3 skills/public/smart-speak/scripts/smart_speak.py \
  --segments-json '[
    {"text": "Chào anh Vũ,", "voice": "vi-VN-HoaiMyNeural"},
    {"text": "你好吗？", "voice": "zh-CN-XiaoxiaoNeural"},
    {"text": "How are you today?", "voice": "en-US-AvaNeural"}
  ]' \
  --output "/home/jackie_chen_phong/.openclaw/workspace/bai_hoc.mp3"
```

## Lưu ý quan trọng
- **Đường dẫn tuyệt đối:** Luôn cung cấp đường dẫn đầy đủ cho file đầu ra (`--output`).
- **Xử lý Emoji:** Skill sẽ tự động lược bỏ emoji để tránh máy đọc tên emoji làm gián đoạn bài học.
- **Dấu câu:** Mỗi đoạn văn nên kết thúc bằng dấu câu phù hợp để tạo quãng nghỉ tự nhiên.
