---
name: vietnam-realestate
description: >
  Skill tra cứu và phân tích bất động sản Việt Nam toàn diện. Bao gồm: tra cứu giá đất/m²
  theo khu vực, bảng giá đất Nhà nước (khung giá UBND tỉnh/thành), phân tích xu hướng
  thị trường, tư vấn pháp lý BĐS (sổ đỏ, sổ hồng, quy hoạch, pháp lý dự án). Nguồn dữ liệu
  từ batdongsan.com.vn, các sàn giao dịch, bảng giá đất UBND, báo cáo thị trường CBRE/Savills/JLL,
  quy hoạch đất đai. Phục vụ tất cả đối tượng: nhà đầu tư, môi giới, người mua nhà lần đầu.
  Sử dụng skill này khi người dùng hỏi về giá đất, giá nhà, giá m², bất động sản, BĐS,
  quy hoạch, sổ đỏ, sổ hồng, khung giá đất, bảng giá đất, thị trường nhà đất, đầu tư BĐS,
  mua bán nhà đất, cho thuê, chung cư, đất nền, biệt thự, hoặc bất kỳ câu hỏi nào liên quan
  đến bất động sản Việt Nam.
version: 1.0.0
metadata:
  openclaw:
    author: Pham Triet
    community: OpenClaw Việt Nam
    community_link: https://zalo.me/g/lajsqc334jqc5fezevvo
    emoji: "🏠"
    tags:
      - realestate
      - vietnamese
      - property
      - land-price
      - market-analysis
---

# Vietnam Real Estate Research & Analysis

> **Author:** Pham Triet
> **Cộng đồng:** [OpenClaw Việt Nam](https://zalo.me/g/lajsqc334jqc5fezevvo)

Skill tra cứu, phân tích và tư vấn bất động sản Việt Nam toàn diện.
Dữ liệu real-time qua web search từ các nguồn chính thống.

## Mục lục

1. [Xác định nhu cầu người dùng](#1-xác-định-nhu-cầu-người-dùng)
2. [Tra cứu giá đất/m² theo khu vực](#2-tra-cứu-giá-đấtm²-theo-khu-vực)
3. [Bảng giá đất Nhà nước (khung giá)](#3-bảng-giá-đất-nhà-nước-khung-giá)
4. [Phân tích xu hướng thị trường](#4-phân-tích-xu-hướng-thị-trường)
5. [Tư vấn pháp lý BĐS](#5-tư-vấn-pháp-lý-bđs)
6. [Xuất báo cáo](#6-xuất-báo-cáo)

---

## Nguyên tắc hoạt động

**SKILL NÀY HOẠT ĐỘNG HOÀN TOÀN DỰA TRÊN WEB SEARCH.**

Dữ liệu BĐS thay đổi liên tục — KHÔNG BAO GIỜ dùng kiến thức cũ để trả lời
về giá cả, xu hướng, hay quy hoạch. Luôn search trước khi trả lời.

**Nguồn dữ liệu chính thống (đọc `references/data-sources.md` để biết chi tiết):**

| Loại dữ liệu | Nguồn chính | Cách tra cứu |
|--------------|-------------|--------------|
| Giá thị trường | batdongsan.com.vn, chotot.com, homedy.com | web_search + web_fetch |
| Bảng giá đất Nhà nước | UBND tỉnh/thành, thuvienphapluat.vn | web_search |
| Xu hướng thị trường | CBRE, Savills, JLL, cafeland.vn | web_search |
| Quy hoạch | quyhoach.gov.vn, UBND tỉnh/thành | web_search |
| Pháp lý | thuvienphapluat.vn, Luật Đất đai 2024 | web_search |

---

## 1. Xác định nhu cầu người dùng

Khi nhận yêu cầu, xác định người dùng thuộc nhóm nào để điều chỉnh cách trả lời:

| Nhóm | Nhu cầu chính | Tone trả lời |
|------|--------------|--------------|
| Nhà đầu tư | ROI, biên lợi nhuận, xu hướng tăng giá, quy hoạch tương lai | Phân tích sâu, có số liệu, so sánh |
| Môi giới | Giá thị trường chính xác, pháp lý, thông tin dự án | Nhanh, cụ thể, có nguồn dẫn |
| Người mua nhà lần đầu | Giá phù hợp túi tiền, thủ tục, vay ngân hàng | Dễ hiểu, hướng dẫn từng bước |

**Thông tin cần thu thập:**
- **Khu vực**: Tỉnh/thành, quận/huyện, phường/xã, đường/khu vực cụ thể
- **Loại BĐS**: Đất nền, nhà phố, chung cư, biệt thự, đất nông nghiệp, thương mại
- **Mục đích**: Mua ở, đầu tư, cho thuê, xây dựng
- **Ngân sách** (nếu mua): Khoảng giá chấp nhận được

---

## 2. Tra cứu giá đất/m² theo khu vực

### Quy trình tra cứu

**Bước 1: Search giá thị trường hiện tại**

```
web_search: "giá đất [quận/huyện] [tỉnh/thành] 2025 2026 m2"
web_search: "giá nhà đất [đường/khu vực] [quận] mới nhất"
web_search: "giá chung cư [tên dự án/khu vực] m2"
web_search: "site:batdongsan.com.vn [khu vực] giá"
```

**Bước 2: Fetch dữ liệu từ các sàn giao dịch**

```
web_fetch: "https://batdongsan.com.vn/ban-dat-[khu-vuc]"
web_search: "site:chotot.com bất động sản [khu vực] giá"
web_search: "site:homedy.com [khu vực] giá m2"
```

**Bước 3: So sánh và tổng hợp**

Khi trình bày kết quả, luôn bao gồm:
- **Khoảng giá**: Giá thấp nhất – cao nhất – trung bình
- **Đơn vị**: triệu/m² (đất nền, nhà phố) hoặc triệu/căn (chung cư)
- **So sánh**: So với quý trước, năm trước (nếu có dữ liệu)
- **Nguồn**: Ghi rõ dữ liệu lấy từ đâu
- **Thời điểm**: Dữ liệu cập nhật đến tháng/năm nào

### Lưu ý quan trọng

- Giá rao bán ≠ giá giao dịch thực tế (thường chênh 5–15%)
- Giá đất mặt tiền ≠ giá đất trong hẻm (chênh 30–60%)
- Cùng quận nhưng khác phường có thể chênh 20–50%
- Luôn ghi rõ **"giá rao bán tham khảo"**, không khẳng định đây là giá chính xác

---

## 3. Bảng giá đất Nhà nước (khung giá)

### Khung giá đất là gì?

Bảng giá đất do UBND tỉnh/thành ban hành, dùng để:
- Tính thuế chuyển nhượng BĐS
- Tính tiền sử dụng đất khi cấp sổ đỏ
- Bồi thường giải phóng mặt bằng
- Tính tiền thuê đất

**Lưu ý:** Giá đất Nhà nước thường THẤP HƠN giá thị trường 30–70%.
Từ Luật Đất đai 2024, bảng giá đất phải tiệm cận giá thị trường hơn.

### Quy trình tra cứu

```
web_search: "bảng giá đất [tỉnh/thành] 2025 2026"
web_search: "quyết định bảng giá đất UBND [tỉnh/thành] mới nhất"
web_search: "khung giá đất [quận/huyện] [tỉnh/thành] site:thuvienphapluat.vn"
web_search: "bảng giá đất [đường cụ thể] [quận] [tỉnh/thành]"
```

### Trình bày kết quả

Khi trả lời về bảng giá đất Nhà nước, bao gồm:
- **Số quyết định**: QĐ số .../QĐ-UBND ngày ...
- **Thời hạn áp dụng**: Từ ngày ... đến ngày ...
- **Giá theo vị trí**: Vị trí 1 (mặt tiền), Vị trí 2 (hẻm lớn), Vị trí 3 (hẻm nhỏ)...
- **So sánh**: Giá Nhà nước vs giá thị trường
- **Lưu ý**: Giải thích ý nghĩa thực tế (thuế, phí...)

---

## 4. Phân tích xu hướng thị trường

### Quy trình phân tích

**Bước 1: Thu thập báo cáo mới nhất**

```
web_search: "báo cáo thị trường bất động sản Việt Nam [quý/năm] CBRE"
web_search: "Savills Vietnam property market report [năm]"
web_search: "JLL Vietnam real estate outlook [năm]"
web_search: "thị trường bất động sản [tỉnh/thành] [quý] [năm] xu hướng"
web_search: "cafeland.vn thị trường bất động sản [khu vực]"
```

**Bước 2: Phân tích các chỉ số**

| Chỉ số | Ý nghĩa | Nguồn |
|--------|---------|-------|
| Nguồn cung mới | Số dự án/căn hộ mới ra thị trường | CBRE, Savills |
| Tỷ lệ hấp thụ | % bán được / tổng nguồn cung | Báo cáo quý |
| Giá bán trung bình | Đồng/m², so sánh theo quý/năm | Các sàn GD |
| Tỷ suất cho thuê | Thu nhập cho thuê / giá mua | Savills, JLL |
| Lãi suất vay mua nhà | Ảnh hưởng trực tiếp đến cầu | Ngân hàng |

**Bước 3: Đưa ra nhận định**

Khi phân tích xu hướng, bao gồm:
- **Xu hướng giá**: Tăng/giảm/đi ngang, tốc độ thay đổi (%)
- **Phân khúc nổi bật**: Phân khúc nào đang hot, phân khúc nào trầm lắng
- **Yếu tố tác động**: Quy hoạch hạ tầng, chính sách, lãi suất, nguồn cung
- **Khu vực tiềm năng**: Khu vực nào đang được hưởng lợi từ hạ tầng
- **Rủi ro**: Pháp lý, bong bóng, thanh khoản

**QUAN TRỌNG:** Luôn nhắc người dùng:
> "Phân tích này mang tính tham khảo dựa trên dữ liệu thu thập được.
> Quyết định đầu tư cần được cân nhắc kỹ với tư vấn chuyên gia."

---

## 5. Tư vấn pháp lý BĐS

**→ Đọc file `references/legal-framework.md`** để biết khung pháp lý BĐS Việt Nam.

### 5.1. Kiểm tra pháp lý BĐS

Khi người dùng hỏi về pháp lý, tra cứu:

```
web_search: "kiểm tra pháp lý bất động sản [loại BĐS] [vấn đề cụ thể]"
web_search: "thủ tục cấp sổ đỏ [loại đất] [tỉnh/thành] mới nhất"
web_search: "Luật Đất đai 2024 [vấn đề cụ thể]"
web_search: "quy hoạch [khu vực] site:quyhoach.gov.vn"
```

### 5.2. Các vấn đề pháp lý thường gặp

| Vấn đề | Cần kiểm tra | Nguồn |
|--------|-------------|-------|
| Sổ đỏ/Sổ hồng | Tình trạng pháp lý, quyền sử dụng đất | UBND, Văn phòng đăng ký đất đai |
| Quy hoạch | Đất có nằm trong quy hoạch không | quyhoach.gov.vn, UBND |
| Tranh chấp | Lịch sử tranh chấp, thế chấp | Tòa án, ngân hàng |
| Giấy phép xây dựng | Điều kiện xây dựng, mật độ | Sở Xây dựng |
| Chuyển nhượng | Thuế, phí, thủ tục | Thuế, Công chứng |

### 5.3. Thuế và phí BĐS

Khi được hỏi về chi phí giao dịch:

```
web_search: "thuế chuyển nhượng bất động sản 2025 2026 Việt Nam"
web_search: "phí công chứng mua bán nhà đất mới nhất"
web_search: "lệ phí trước bạ nhà đất [tỉnh/thành]"
```

Các loại thuế/phí thường gặp (luôn web search để xác minh mức hiện hành):
- Thuế thu nhập cá nhân: thường 2% giá chuyển nhượng
- Lệ phí trước bạ: thường 0.5% giá trị
- Phí công chứng: theo biểu phí quy định
- Phí đăng bộ sang tên

---

## 6. Xuất báo cáo

Khi người dùng yêu cầu báo cáo chi tiết, tạo file .docx theo skill `vietnamese-contract`
(nếu có) hoặc tạo artifact markdown với cấu trúc:

```
1. Tổng quan khu vực
2. Giá thị trường hiện tại (bảng giá chi tiết)
3. Bảng giá đất Nhà nước (nếu liên quan)
4. Xu hướng thị trường (biểu đồ nếu có)
5. Phân tích pháp lý
6. Đánh giá và khuyến nghị
7. Nguồn dữ liệu tham khảo
```

---

## Lưu ý đạo đức nghề nghiệp

- **Không khẳng định giá chính xác** — luôn nói "giá tham khảo", "khoảng giá"
- **Không khuyên mua/bán cụ thể** — chỉ phân tích, đưa thông tin
- **Luôn nhắc tham khảo chuyên gia** — luật sư, môi giới có giấy phép
- **Ghi rõ nguồn dữ liệu** — và thời điểm cập nhật
- **Cảnh báo rủi ro** — đặc biệt với đất chưa có sổ, dự án chưa đủ pháp lý

---

## Tham khảo nhanh: Cấu trúc thư mục skill

```
vietnam-realestate/
├── SKILL.md                          ← File này
├── scripts/
│   └── price-calculator.py           ← Tính toán thuế, phí, ROI
└── references/
    ├── data-sources.md               ← Chi tiết nguồn dữ liệu & cách search
    └── legal-framework.md            ← Khung pháp lý BĐS Việt Nam
```
