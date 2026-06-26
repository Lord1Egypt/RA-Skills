---
name: thancuu
description: Hệ thống phân tích tính cách Thần Cửu độc lập (phát minh bởi Anh Vũ). Hỗ trợ tính toán 8 chỉ số cốt lõi và phân tích tương quan mối quan hệ. Yêu cầu bộ tài liệu hướng dẫn trong thư mục references.
---

# Thần Cửu: Hệ thống Phân tích Nhân sinh chuyên sâu

Skill này là một hệ thống phân tích tính cách độc lập, khác biệt hoàn toàn với Thần số học truyền thống. Nó được thiết kế để giúp anh Vũ thấu hiểu bản thân và các mối quan hệ xung quanh dựa trên logic và các quy tắc đặc thù.

## Yêu cầu hệ thống

Để skill này hoạt động chính xác, nó cần truy cập vào bộ tri thức nền tảng nằm trong thư mục `references/` của skill. Bộ tri thức này bao gồm:

1.  **Bảng quy đổi chữ cái sang số:** Định nghĩa riêng cho hệ thống Thần Cửu.
2.  **Công thức tính toán:** Cách rút gọn các con số về một chữ số duy nhất (từ 1 đến 9).
3.  **Ý nghĩa của 9 con số:** Được biên soạn riêng cho từng phạm trù.

## Các tính năng chính

### 1. Phân tích cá nhân (8 Chỉ số)
Tính toán và luận giải chi tiết dựa trên Họ tên và Ngày sinh (theo CCCD):
- **Số Đường Đời:** Sứ mệnh và con đường phát triển.
- **Số Vận Mệnh:** Năng lực bẩm sinh.
- **Số Nội Tâm:** Khát khao thầm kín.
- **Số Nhân Cách:** Hình ảnh phản chiếu trong mắt người khác.
- **Số Thái Độ:** Cách phản ứng trước các tình huống cuộc sống.
- **Số Ngày Sinh:** Năng khiếu đặc biệt.
- **Số Tên Gọi:** Sức mạnh của định danh.
- **Số Cảm Xúc:** Cách xử lý rung động nội tâm.

### 2. Phân tích Tương quan (Relationship)
So sánh bộ chỉ số của hai người để tìm ra:
- Điểm tương đồng và sự bù trừ.
- Các mức độ quan hệ: Hợp tự nhiên, Trung lập, hoặc Đối đầu.
- Lời khuyên để phát triển mối quan hệ bền vững.

## Hướng dẫn sử dụng

### Phân tích cho một người
Anh chỉ cần gửi thông tin:
> "Phân tích Thần Cửu cho [Họ và tên], ngày sinh [Ngày/Tháng/Năm]"

### Phân tích tương quan
Anh gửi thông tin của cả hai người:
> "Phân tích tương quan Thần Cửu giữa [Người A - Ngày sinh] và [Người B - Ngày sinh]"

## Lưu ý quan trọng
- **Độ chính xác:** Luôn sử dụng đúng tên và ngày sinh trên giấy tờ tùy thân.
- **Nguyên tắc cốt lõi:** Tuyệt đối không áp dụng các khái niệm số Master (11, 22, 33) của Thần số học truyền thống vào đây. Hệ thống này chỉ vận hành trên 9 con số cơ bản.
- **Lưu trữ:** Mọi kết quả phân tích sẽ được lưu vào thư mục tri thức `knowledge/ThanCuu/` để anh có thể tra cứu lại bất cứ lúc nào.
