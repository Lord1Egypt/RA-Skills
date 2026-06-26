# Hướng dẫn quét CCCD tự động điền hợp đồng

Quét ảnh CCCD/CMND để tự động trích xuất thông tin và điền vào hợp đồng.

**Kiến trúc 2 lớp: EasyOCR (offline) + AI model (bất kỳ) = chính xác cao nhất.**

---

## Tại sao 2 lớp?

| | Lớp 1: EasyOCR | Lớp 2: AI verify |
|---|---|---|
| **Vai trò** | Quét ảnh → raw text | Sửa lỗi → JSON sạch |
| **Offline** | Có | Tùy model |
| **Phụ thuộc AI** | Không | Có (bất kỳ model) |
| **Chính xác** | ~75-85% | ~95-99% sau khi AI sửa |
| **Khi nào chạy** | Luôn luôn | Khi có AI model |

Nếu OpenClaw đang chạy model nào (Claude, GPT, Llama, Gemini...) → AI sửa lỗi OCR.
Nếu không có AI → vẫn dùng được kết quả lớp 1 (người dùng tự kiểm tra).

---

## Cài đặt

```bash
pip install easyocr opencv-python --break-system-packages
```

Lần đầu chạy sẽ tự tải model tiếng Việt (~100MB).

---

## Quy trình đầy đủ

### Bước 1: EasyOCR quét ảnh (offline)

```bash
# Mặt trước
python scripts/cccd-ocr.py cccd-truoc.jpg --json

# Mặt trước + mặt sau
python scripts/cccd-ocr.py cccd-truoc.jpg --back cccd-sau.jpg --json

# Có GPU (nhanh hơn 5-10x)
python scripts/cccd-ocr.py cccd.jpg --json --gpu
```

Kết quả raw JSON (có thể có lỗi OCR):
```json
{
  "so_cccd": "089200010297",
  "ho_ten": "PHAM MINH TRÍET",
  "ngay_sinh": "21/02/2000",
  "noi_thuong_tru": "39/10A Trung Hung, My Thoi, Long Xuyen, An Giang",
  "ngay_cap": "25/02/2025",
  "noi_cap": "Cuc truong Cuc Canh sat quan ly hanh chinh ve trat tu xa hoi"
}
```

Lưu ý: raw text có thể **thiếu dấu tiếng Việt** hoặc **sai chính tả** — đây là hạn chế OCR.

### Bước 2: AI model verify và cải thiện

Agent (bất kỳ model nào đang chạy trên OpenClaw) nhận raw JSON và xử lý:

**Prompt mẫu cho AI:**

```
Đây là kết quả OCR quét từ ảnh CCCD Việt Nam. Kết quả có thể thiếu dấu
tiếng Việt hoặc có lỗi chính tả.

{paste_raw_json}

Hãy:
1. Thêm dấu tiếng Việt đúng (VD: "Pham" → "Phạm", "Triet" → "Triết")
2. Sửa lỗi chính tả nếu có
3. Kiểm tra số CCCD đủ 12 chữ số
4. Kiểm tra ngày tháng hợp lệ (DD/MM/YYYY)
5. Họ tên viết hoa đúng
6. Địa chỉ đầy đủ, đúng format

Trả về JSON đã sửa, cùng format. Trường nào không chắc thì ghi [CẦN XÁC NHẬN].
```

Kết quả sau AI verify:
```json
{
  "so_cccd": "089200010297",
  "ho_ten": "PHẠM MINH TRIẾT",
  "ngay_sinh": "21/02/2000",
  "noi_thuong_tru": "39/10A Trung Hưng, Mỹ Thới, Long Xuyên, An Giang",
  "ngay_cap": "25/02/2025",
  "noi_cap": "Cục trưởng Cục Cảnh sát quản lý hành chính về trật tự xã hội"
}
```

**AI đã sửa:**
- "TRÍET" → "TRIẾT" (sửa dấu)
- "Trung Hung" → "Trung Hưng" (thêm dấu)
- "My Thoi" → "Mỹ Thới" (thêm dấu)
- "Cuc truong..." → "Cục trưởng..." (thêm dấu đầy đủ)

### Bước 3: Hiển thị → xác nhận → hỏi thêm

```
Tôi đã quét CCCD và xử lý kết quả:

  Số CCCD: 089200010297
  Họ tên: PHẠM MINH TRIẾT
  Ngày sinh: 21/02/2000
  Địa chỉ: 39/10A Trung Hưng, Mỹ Thới, Long Xuyên, An Giang
  Ngày cấp: 25/02/2025
  Nơi cấp: Cục trưởng Cục Cảnh sát QLHC về TTXH

  Thông tin chính xác không?
  Cho tôi thêm: SĐT, Email, STK ngân hàng + tên NH
```

### Bước 4: Điền vào hợp đồng

Agent lấy JSON đã verify + thông tin bổ sung → điền vào hợp đồng → tạo .docx.

---

## Xử lý nhiều CCCD (Bên A + Bên B)

```
Upload CCCD Bên A → EasyOCR → AI verify → xác nhận → lưu
Upload CCCD Bên B → EasyOCR → AI verify → xác nhận → lưu
Hỏi thêm SĐT, email, STK cho mỗi bên
→ Điền cả 2 bên vào hợp đồng → tạo .docx
```

---

## Mapping CCCD → Hợp đồng

| Trường OCR | Trường hợp đồng |
|-----------|-----------------|
| ho_ten | Ông/Bà: [tên] |
| ngay_sinh | Ngày sinh: [ngày] |
| so_cccd | CCCD số: [số] |
| ngay_cap | Ngày cấp: [ngày] |
| noi_cap | Nơi cấp: [nơi] |
| noi_thuong_tru | Địa chỉ thường trú: [địa chỉ] |

**Phải hỏi thêm (CCCD không có):** SĐT, Email, STK ngân hàng + tên NH

---

## Bảo mật

- **Lớp 1 (EasyOCR)**: Chạy OFFLINE — ảnh CCCD không gửi ra internet
- **Lớp 2 (AI verify)**: Chỉ gửi TEXT (không phải ảnh) cho AI model
- KHÔNG lưu ảnh CCCD sau khi trích xuất
- Xóa file tạm sau khi tạo xong hợp đồng
- Nhắc người dùng về bảo mật thông tin cá nhân

---

## Tips quét chính xác hơn

1. Ảnh rõ nét, đủ sáng, không bị mờ
2. Đặt CCCD thẳng, không nghiêng quá 10°
3. Tránh ánh sáng phản chiếu trên mặt nhựa
4. Chụp full frame, không cắt mất chữ
5. Nền tương phản (đặt trên giấy trắng)
