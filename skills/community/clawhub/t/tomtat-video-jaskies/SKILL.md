---
name: tomtat-video
description: Tóm tắt nội dung video YouTube từ đường link cung cấp. Hỗ trợ trích xuất transcript tự động và phân tích ý chính chuyên sâu. Yêu cầu máy chủ có cài đặt yt-dlp và ffmpeg.
---

# Tóm tắt Video YouTube

Skill này giúp em lấy transcript (phụ đề) từ video YouTube và tóm tắt lại nội dung một cách logic và súc tích nhất.

## Yêu cầu hệ thống

Để skill này hoạt động ổn định, máy của anh cần được cài đặt hai công cụ quan trọng sau:

1.  **yt-dlp**: Công cụ mạnh mẽ để tải thông tin và phụ đề từ YouTube.
2.  **ffmpeg**: Bộ công cụ xử lý đa phương tiện.

### Lệnh cài đặt nhanh (cho Linux/Ubuntu)

Anh chạy dòng lệnh sau trong terminal nhé:

```bash
# Cài đặt ffmpeg
sudo apt update && sudo apt install -y ffmpeg

# Cài đặt yt-dlp bản mới nhất qua pip3
python3 -m pip install -U yt-dlp
```

## Quy trình thực hiện

1. **Lấy dữ liệu:** Sử dụng script `scripts/get_transcript.sh` để trích xuất transcript từ URL video.
2. **Xử lý nội dung:** Đọc nội dung transcript (định dạng VTT) và lọc bỏ các mốc thời gian để lấy văn bản thuần túy.
3. **Tóm tắt:** Sử dụng mô hình AI hiện tại để tóm tắt văn bản đó theo các ý chính, cấu trúc logic và dễ hiểu.

## Lệnh thực thi lấy transcript

```bash
bash skills/public/tomtat-video/scripts/get_transcript.sh "<URL_VIDEO>"
```

## Lưu ý
- Skill ưu tiên lấy phụ đề tiếng Việt, nếu không có sẽ lấy tiếng Anh.
- Đối với các video quá dài, em sẽ thực hiện tóm tắt theo từng phần để đảm bảo không mất thông tin quan trọng.
- Luôn trình bày bản tóm tắt một cách chuyên nghiệp và hoạt bát theo phong cách của Thanh Tình.
