---
name: vn-translate
description: Dịch truyện từ ngôn ngữ nguồn sang tiếng Việt. Chuyển đổi định dạng đầu vào, cắt file thành các phần nhỏ ~12kb, dịch tuần tự từng phần, tổng hợp tên nhân vật và xưng hô nhất quán, ghép các phần đã dịch thành file hoàn chỉnh.
version: 1.0.1
author: KaibaZax
---


# vn-translate — Dịch Truyện Sang Tiếng Việt


## Tổng quan

Quy trình dịch truyện gồm 4 bước:
1. **Chuẩn bị:** Chuyển đổi file đầu vào thành `.md` nếu cần (dùng `scripts/convert_to_md.py`)
2. **Cắt file:** Chia file truyện thành nhiều phần nhỏ ~12kb (dùng `scripts/split_file.py`)
3. **Dịch:** Dịch từng phần, đồng thời tổng hợp tên nhân vật và xưng hô
4. **Ghép:** Nối các phần đã dịch thành một file hoàn chỉnh (dùng `scripts/merge_parts.py`)


## Cấu trúc thư mục

```
<project-dir>/
├── raw/              # File gốc đã cắt nhỏ: part_001.md, part_002.md, ...
├── out/              # File đã dịch: part_001.md, part_002.md, ...
├── TenRieng.md       # Bảng tổng hợp tên riêng (nhân vật, địa danh, thuật ngữ)
├── XungHo.md         # MA TRẬN xưng hô (người nói × người nghe)
├── full.md           # File đã ghép hoàn chỉnh sau khi dịch
└── (file gốc)
```


## Bước 1: Chuẩn bị

Chạy:
```bash
python scripts/convert_to_md.py <file_goc>
```

Script tự động nhận diện `.txt`, `.epub`, `.docx`, `.html`, `.pdf` và xuất ra `.md`.


## Bước 2: Cắt file ~12kb

Chạy:
```bash
python scripts/split_file.py <file.md> raw/
```

Tạo các file `raw/part_xxx.md`, mỗi file ~12KB, chỉ cắt tại ký tự xuống dòng `\n`.


## Bước 3: Dịch từng phần + Tổng hợp tên/xưng hô

### Quy trình dịch:

1. **Khởi tạo:** Tạo `TenRieng.md` và `XungHo.md` với format chuẩn (xem bên dưới).
2. **Dịch tuần tự:** Dịch từng file `raw/part_x.md` → `out/part_x.md`. Mỗi part dịch xong, kiểm tra chéo với bảng tên và xưng hô.
3. **Tổng hợp:** Trong quá trình dịch part đầu tiên, lập danh sách **tất cả tên riêng** và **cách xưng hô**. Ghi nhận ngay vào `TenRieng.md` và `XungHo.md`. Các part sau phải tuân thủ tuyệt đối.

### Format `TenRieng.md`:

Bảng 1 chiều: tên gốc → tên dịch + ghi chú. Bao gồm **mọi tên riêng**: nhân vật, địa danh, tổ chức, vật phẩm đặc biệt, thuật ngữ riêng.

```markdown
# Tên Riêng

| Tên gốc | Tên dịch | Ghi chú |
|---------|----------|---------|
| Alice   | Alice    | Nữ chính, 16 tuổi |
| Bob     | Bob      | Bạn thân của Alice |
| Wonderland | Xứ sở thần tiên | Địa danh chính |
```

### Format `XungHo.md`:

**Ma trận 2 chiều:** hàng = người nói, cột = người nghe.
Ô giao nhau ghi `Xưng\Hô` (cách nhau bởi dấu gạch chéo).

```markdown
# Bảng Xưng Hô

Ma trận: [Người nói] × [Người nghe], ô = `Xưng\Hô`

| Người nói \ Người nghe | An | Mẹ kế |
|------------------------|------|---------|
| An | - | Con / Dì |
| Mẹ kế | Mẹ / Con | - |

| Người nói \ Người nghe | Chị A | Em B |
|------------------------|-------|------|
| Chị A | - | Chị / Em |
| Em B | Em / Chị | - |
```

**Nguyên tắc dịch xưng hô:**
- Xác định mối quan hệ giữa các nhân vật (gia đình, bạn bè, kẻ thù, xa lạ, cấp trên/dưới).
- Dùng ma trận để đảm bảo nhất quán: nếu A gọi B là "chị" thì B gọi A là "em".
- Cập nhật ma trận ngay khi có nhân vật mới xuất hiện.
- Các đại từ phổ biến cần có mapping rõ: I/you/he/she/they → xưng hô cụ thể theo từng cặp nhân vật.


## Bước 4: Ghép các phần đã dịch

Chạy:
```bash
python scripts/merge_parts.py out/ full.md
```


## Quy trình thực hiện đầy đủ

```bash
# 1. Chuẩn bị
python scripts/convert_to_md.py truyen.epub

# 2. Cắt file
python scripts/split_file.py truyen.md raw/

# 3. Dịch (thủ công từng part, cập nhật TenRieng.md + XungHo.md)

# 4. Ghép
python scripts/merge_parts.py out/ full.md
```


## Pitfalls & Lưu ý

- **Luôn cắt tại `\n`** — không cắt giữa chừng một câu/đoạn.
- **~12KB** là mục tiêu, có thể dao động do phải cắt tại xuống dòng.
- **Tên riêng:** Quyết định và ghi vào `TenRieng.md` ngay từ lần đầu xuất hiện. Tuyệt đối không đổi giữa chừng.
- **Xưng hô ma trận:** kiểm tra tính đối xứng (A→B và B→A phải khớp logic). Nếu thêm nhân vật mới giữa chừng, cập nhật ma trận ngay.
- File `.md` có thể chứa BOM — script xử lý UTF-8 chuẩn.
