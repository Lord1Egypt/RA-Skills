---
name: vietnam-education
description: >
  Skill soạn giáo án, đề thi, phiếu học tập theo chuẩn Chương trình GDPT 2018
  (Thông tư 32/2018/TT-BGDĐT) và Công văn 7991/BGDĐT-GDTrH (cấu trúc đề kiểm tra
  định kỳ THCS-THPT mới nhất). Có hệ thống VERIFY ĐÁP ÁN 3 LỚP: web search verify
  kiến thức SGK (tất cả môn), SymPy kiểm tra tính toán chính xác (Toán/Lý/Hóa),
  Matplotlib vẽ hình (hình học, đồ thị, biểu đồ). Có script tạo file .docx đề thi
  chuẩn format CV 7991 (chạy 1 lệnh). Phủ tất cả cấp học: Tiểu học, THCS, THPT.
  Sử dụng khi người dùng nhắc đến: giáo án, kế hoạch bài dạy, đề thi, đề kiểm tra,
  phiếu học tập, CTGDPT 2018, Thông tư 32, CV 7991, ma trận đề, soạn bài,
  kiểm tra đánh giá, đúng sai, trắc nghiệm, trả lời ngắn, tự luận.
version: 3.0.0
metadata:
  openclaw:
    author: Pham Triet
    community: OpenClaw Việt Nam
    community_link: https://zalo.me/g/lajsqc334jqc5fezevvo
    emoji: "🎓"
    requires:
      bins:
        - python3
        - node
    tags:
      - education
      - vietnamese
      - lesson-plan
      - exam
      - CV-7991
      - CTGDPT-2018
      - verify-answer
      - teacher
---

# Vietnam Education v3 — Soạn giáo án, đề thi, phiếu học tập

> **Author:** Pham Triet
> **Cộng đồng:** [OpenClaw Việt Nam](https://zalo.me/g/lajsqc334jqc5fezevvo)
> **Chuẩn:** CTGDPT 2018 (TT 32/2018) + Công văn 7991/BGDĐT-GDTrH (17/12/2024)

## Cấu trúc thư mục

```
vietnam-education/
├── SKILL.md                     ← File này
├── scripts/
│   ├── create-exam.js           ← Script tạo .docx đề thi chuẩn CV 7991
│   ├── verify-answer.py         ← SymPy verify đáp án (Toán/Lý/Hóa)
│   └── draw-figure.py           ← Matplotlib vẽ hình (tất cả môn)
└── references/
    ├── ctgdpt-2018.md           ← Khung chương trình GDPT 2018
    └── templates.md             ← Mẫu ma trận CV 7991 + giáo án + phiếu HT
```

## Cài đặt (1 lần)

```bash
npm install -g docx                                        # Tạo file .docx
pip install sympy matplotlib numpy --break-system-packages # Verify + vẽ hình
```

---

## NGUYÊN TẮC SỐ 1: ĐẢM BẢO TRI THỨC ĐÚNG

> **KHÔNG BAO GIỜ soạn đề/đáp án/giáo án dựa trên "kiến thức nhớ" của AI.**
> LUÔN verify bằng 3 lớp trước khi xuất cho giáo viên.

### Hệ thống verify 3 lớp

| Lớp | Công cụ | Bắt buộc cho | Mục đích |
|:---:|---------|:-------------|----------|
| 1 | **Web search** | TẤT CẢ các môn | Lấy nội dung SGK chính xác, verify đáp án |
| 2 | **SymPy** (`verify-answer.py`) | Toán, Lý, Hóa, KHTN | Tính toán lại đáp án — chính xác tuyệt đối |
| 3 | **Matplotlib** (`draw-figure.py`) | Môn cần hình | Vẽ hình học, đồ thị, biểu đồ → chèn đề |

### Lớp 1: Web search (BẮT BUỘC tất cả môn)

```
# Tìm nội dung bài học ĐÚNG bộ sách
web_search: "[KNTT/CTST/Cánh Diều] [môn] lớp [số] bài [tên bài]"
web_search: "sách [tên sách] [môn] lớp [số] yêu cầu cần đạt"

# Verify đáp án
web_search: "[nội dung câu hỏi] site:loigiaihay.com OR site:sachgiaibaitap.com"
web_search: "[sự kiện/công thức/tác phẩm] SGK [môn] lớp [số]"

# Kiểm tra CV 7991 cập nhật
web_search: "CV 7991 [môn] [năm học] hướng dẫn Sở GDĐT"
```

**Quy tắc:** Kiến thức KHÁC nhau giữa 3 bộ sách → PHẢI search đúng bộ sách GV yêu cầu.

### Lớp 2: SymPy verify (Toán, Lý, Hóa)

```bash
python scripts/verify-answer.py --equation "2*x+5=11" --var x       # Giải PT
python scripts/verify-answer.py --quadratic 1 -5 6                   # PT bậc 2
python scripts/verify-answer.py --calc "sqrt(3**2 + 4**2)"           # Tính biểu thức
python scripts/verify-answer.py --geometry triangle --params '{"base":6,"h":4}'
python scripts/verify-answer.py --chem "H2+O2->H2O"                  # Cân bằng PTHH
```

**Quy tắc:** Nếu SymPy cho kết quả KHÁC đáp án → SỬA ĐÁP ÁN theo SymPy.

### Lớp 3: Matplotlib vẽ hình

```bash
python scripts/draw-figure.py --type triangle --params '{"A":[0,0],"B":[6,0],"C":[3,4]}' -o h.png
python scripts/draw-figure.py --type rectangle --params '{"A":[0,0],"B":[6,0],"C":[6,4],"D":[0,4]}' -o h.png
python scripts/draw-figure.py --type circle --params '{"center":[0,0],"radius":3}' -o h.png
python scripts/draw-figure.py --type graph --expr "x**2-4*x+3" --range="-1,5" -o h.png
python scripts/draw-figure.py --type coordinate --params '{"points":{"A":[1,2],"B":[4,3]}}' -o h.png
python scripts/draw-figure.py --type bar --params '{"labels":["A","B"],"values":[80,95]}' -o h.png
python scripts/draw-figure.py --type pie --params '{"labels":["NN","CN","DV"],"values":[30,35,35]}' -o h.png
python scripts/draw-figure.py --type line --params '{"labels":["2020","2021","2022"],"datasets":[{"values":[85,90,78],"name":"A"}]}' -o h.png
```

---

## SOẠN ĐỀ KIỂM TRA (CV 7991)

### Cấu trúc đề chuẩn CV 7991 (ban hành 17/12/2024)

**→ Đọc `references/templates.md` để xem ma trận + mẫu đề chi tiết**

```
TỔNG: 10 điểm

PHẦN I: TRẮC NGHIỆM KHÁCH QUAN (7,0 điểm)
  A. Nhiều lựa chọn ──── khoảng 3,0đ (12 câu × 0,25đ)
  B. Đúng - Sai ────────── khoảng 2,0đ (2 câu × 4 ý × 0,25đ)
  C. Trả lời ngắn ──────── khoảng 2,0đ (4 câu × 0,5đ)
     ⚠️ Môn không có dạng C → chuyển hết cho B (B = 4,0đ)

PHẦN II: TỰ LUẬN (3,0 điểm)
  2-3 câu, thang điểm chi tiết

Tỷ lệ theo khối: Lớp 10-11 = 70/30 | Lớp 12 = 80/20
Mức nhận thức:    40% NB + 30% TH + 30% VD (gộp VD cao)
```

**MÔN KHÔNG ÁP DỤNG CV 7991:**
- **Ngữ văn**: tự luận 100% (theo CV 3175/BGDĐT-GDTrH)
- GD thể chất, Nghệ thuật, HĐTN, Nội dung GD địa phương: nhận xét

**THCS:** Tùy Sở GD&ĐT → web search hướng dẫn của Sở trước khi soạn.

### GV cung cấp → Agent tạo đề

```
GV nói: "Soạn đề giữa kỳ Toán 10, sách Kết nối tri thức, Chương 1-2"

Agent:
  ① Web search nội dung Chương 1-2 sách KNTT Toán 10
  ② Soạn câu hỏi + đáp án dựa trên nội dung đã search
  ③ verify-answer.py → SymPy kiểm tra TỪNG đáp án Toán
  ④ draw-figure.py → vẽ hình (nếu có hình học/đồ thị)
  ⑤ Sửa CONFIG + dữ liệu trong create-exam.js
  ⑥ node create-exam.js → xuất .docx chuẩn format
  ⑦ validate.py kiểm tra file Word
  ⑧ Giao GV + cảnh báo "vui lòng kiểm tra lại đáp án"
```

### Tạo file .docx bằng create-exam.js

Script `scripts/create-exam.js` tạo file .docx hoàn chỉnh, chuẩn format CV 7991.

**Cách dùng:**

1. Copy `create-exam.js` ra thư mục làm việc
2. Sửa phần `CONFIG` (tên trường, môn, lớp, thời gian)
3. Sửa phần `DỮ LIỆU ĐỀ THI`:
   - `multipleChoice` — 12 câu TN nhiều lựa chọn
   - `trueFalse` — 2 câu Đúng-Sai (mỗi câu 4 ý)
   - `shortAnswer` — 4 câu Trả lời ngắn
   - `essay` — 3 câu Tự luận
4. Chạy: `node create-exam.js`
5. Validate: `python /mnt/skills/public/docx/scripts/office/validate.py [file].docx`

**File .docx xuất ra bao gồm:**
- Header 2 cột: Trường (trái) — Đề KT (phải)
- Font Times New Roman 13pt, lề A4 chuẩn VN
- 4 PA (A/B/C/D) trên 2 dòng
- Bảng Đúng-Sai có ô □ Đúng □ Sai cho 4 ý
- Trả lời ngắn có dòng "Đáp án: ..."
- Tự luận có khoảng trống
- Trang đáp án riêng (bảng ĐA + thang điểm TL chi tiết)

### Verify theo từng môn

| Môn | Lớp 1: Web search | Lớp 2: SymPy | Lớp 3: Matplotlib |
|-----|:--:|:--:|:--:|
| Toán | ✅ Nội dung SGK | ✅ Giải PT, tính toán | ✅ Hình học, đồ thị |
| Vật lý | ✅ Công thức, định luật | ✅ F=ma, U=IR... | ✅ Sơ đồ lực |
| Hóa học | ✅ PTHH, tính chất | ✅ Cân bằng, mol | Biểu đồ nếu cần |
| Ngữ văn | ✅ Tác phẩm, tác giả | ❌ | ❌ |
| Tiếng Anh | ✅ Từ vựng, ngữ pháp | ❌ | ❌ |
| Lịch sử | ✅ Sự kiện, năm, nhân vật | ❌ | Timeline nếu cần |
| Địa lý | ✅ Số liệu SGK | ❌ | ✅ Biểu đồ cột/tròn |
| Sinh/KHTN | ✅ Kiến thức SGK | SymPy nếu tính toán | Biểu đồ nếu cần |
| GDCD | ✅ SGK + luật liên quan | ❌ | ❌ |

---

## SOẠN KẾ HOẠCH BÀI DẠY (GIÁO ÁN)

**→ Đọc `references/templates.md` phần "Kế hoạch bài dạy"**

### GV cung cấp

```
1. Môn + Lớp + Bộ sách
2. Bài/Chủ đề cụ thể
3. Số tiết
```

### Agent thực hiện

```
① Web search yêu cầu cần đạt + nội dung bài trong SGK
② Xác định mục tiêu (năng lực đặc thù + chung + phẩm chất)
③ Thiết kế 4 hoạt động:
   HĐ1: Khởi động — tạo hứng thú, kết nối
   HĐ2: Hình thành kiến thức mới — HS tìm hiểu, khám phá
   HĐ3: Luyện tập — củng cố qua bài tập
   HĐ4: Vận dụng — áp dụng thực tế
④ Mỗi HĐ có: a) Mục tiêu  b) Nội dung  c) Sản phẩm  d) Tổ chức thực hiện
⑤ Tạo file .docx (dùng skill docx)
```

### Cấu trúc giáo án chuẩn

```
KẾ HOẠCH BÀI DẠY
Môn: ... — Lớp: ... — Bộ sách: ...
Bài: ... — Số tiết: ...

I. MỤC TIÊU
  1. Năng lực
     a) Năng lực đặc thù: [của môn]
     b) Năng lực chung: tự chủ tự học / giao tiếp hợp tác / GQVĐ sáng tạo
  2. Phẩm chất: yêu nước / nhân ái / chăm chỉ / trung thực / trách nhiệm

II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

III. TIẾN TRÌNH DẠY HỌC
  HĐ 1: KHỞI ĐỘNG (... phút)
  HĐ 2: HÌNH THÀNH KIẾN THỨC MỚI (... phút)
  HĐ 3: LUYỆN TẬP (... phút)
  HĐ 4: VẬN DỤNG (... phút)

IV. HỒ SƠ DẠY HỌC (phiếu HT, rubric...)
```

**Lưu ý:** Mục tiêu dùng ĐỘNG TỪ hành động (nêu, giải thích, áp dụng, phân tích...).
Hoạt động lấy HS làm trung tâm. Có phân hóa cho HS giỏi/yếu.

---

## SOẠN PHIẾU HỌC TẬP

**→ Đọc `references/templates.md` phần "Phiếu học tập"**

### Các loại phiếu

| Loại | Dùng khi | Đặc điểm |
|------|---------|----------|
| **Cá nhân** | HS tự hoàn thành | Có câu hỏi + chỗ trống + tự đánh giá |
| **Nhóm** | Hoạt động nhóm | Phân công TV + bảng đánh giá nhóm |
| **Dự án** | Dự án dài hạn | Mục tiêu + sản phẩm + tiến độ + rubric |

### Agent thực hiện

```
① Web search nội dung bài học
② Xác định loại phiếu phù hợp
③ Soạn nội dung phiếu (câu hỏi, bảng, sơ đồ cần điền)
④ Tạo file .docx (dùng skill docx)
```

---

## THAM KHẢO NHANH

### 5 phẩm chất + 3 năng lực chung (CTGDPT 2018)

**→ Đọc `references/ctgdpt-2018.md` để xem chi tiết**

| 5 phẩm chất | 3 năng lực chung |
|-------------|-----------------|
| Yêu nước | Tự chủ và tự học |
| Nhân ái | Giao tiếp và hợp tác |
| Chăm chỉ | Giải quyết vấn đề và sáng tạo |
| Trung thực | |
| Trách nhiệm | |

### 3 bộ sách giáo khoa

| Bộ sách | NXB | Viết tắt |
|---------|-----|---------|
| Kết nối tri thức với cuộc sống | NXB Giáo dục VN | KNTT |
| Chân trời sáng tạo | NXB Giáo dục VN | CTST |
| Cánh Diều | NXB ĐH Sư phạm | CD |

### Động từ theo mức nhận thức (Bloom)

| Mức (~%) | Động từ |
|----------|---------|
| Nhận biết (40%) | nêu, liệt kê, nhận ra, chỉ ra, mô tả, xác định, kể tên |
| Thông hiểu (30%) | giải thích, phân biệt, so sánh, tóm tắt, diễn giải |
| Vận dụng (30%) | áp dụng, giải quyết, tính toán, phân tích, đánh giá, sáng tạo |
