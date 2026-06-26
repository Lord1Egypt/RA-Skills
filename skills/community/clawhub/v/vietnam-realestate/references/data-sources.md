# Nguồn dữ liệu BĐS Việt Nam — Hướng dẫn tra cứu chi tiết

Tài liệu hướng dẫn cách web search hiệu quả cho từng loại dữ liệu BĐS.

---

## 1. Giá thị trường (giá rao bán / cho thuê)

### Nguồn chính

| Nguồn | URL | Loại dữ liệu | Độ tin cậy |
|-------|-----|--------------|-----------|
| Batdongsan.com.vn | batdongsan.com.vn | Rao bán/thuê lớn nhất VN | ★★★★★ |
| Chợ Tốt Nhà | nha.chotot.com | Rao bán/thuê phổ biến | ★★★★ |
| Homedy | homedy.com | Rao bán, đánh giá dự án | ★★★★ |
| CafeF BĐS | cafef.vn/bat-dong-san | Tin tức thị trường | ★★★★ |
| CafeLand | cafeland.vn | Tin tức, phân tích | ★★★★ |

### Cách search hiệu quả

**Giá đất nền:**
```
web_search: "giá đất [phường/xã] [quận/huyện] [tỉnh/thành] m2 2026"
web_search: "site:batdongsan.com.vn bán đất [quận] [thành phố]"
```

**Giá chung cư:**
```
web_search: "giá chung cư [tên dự án] m2 mới nhất"
web_search: "chung cư [quận/khu vực] giá dưới [số] tỷ"
```

**Giá cho thuê:**
```
web_search: "giá thuê [loại BĐS] [khu vực] tháng"
```

### Xử lý dữ liệu

- Lấy ít nhất 5–10 tin rao để tính khoảng giá
- Loại bỏ giá quá cao/thấp bất thường (outliers)
- Giá rao thường cao hơn giá giao dịch thực 5–15%
- Phân biệt: mặt tiền, hẻm xe hơi, hẻm xe máy, hẻm nhỏ

---

## 2. Bảng giá đất Nhà nước

### Nguồn chính

| Nguồn | Cách truy cập |
|-------|--------------|
| UBND tỉnh/thành | [tỉnh].gov.vn |
| Thư viện pháp luật | thuvienphapluat.vn |
| Sở TN&MT | sotainguyen.[tỉnh].gov.vn |

### Cách search

```
web_search: "quyết định bảng giá đất [tỉnh/thành] [năm] UBND"
web_search: "bảng giá đất [quận/huyện] [tỉnh/thành] [năm]"
web_search: "site:thuvienphapluat.vn bảng giá đất [tỉnh/thành]"
```

### Cấu trúc bảng giá đất

Phân theo: Loại đất → Vị trí (VT1–VT4) → Khu vực/đường → Đoạn đường

**Lưu ý:** Luật Đất đai 2024 yêu cầu bảng giá hàng năm, tiệm cận giá thị trường.

---

## 3. Báo cáo thị trường

| Tổ chức | Tần suất | Cách search |
|---------|----------|-------------|
| CBRE Vietnam | Hàng quý | "CBRE Vietnam market report [quý] [năm]" |
| Savills Vietnam | Hàng quý | "Savills Vietnam property report [quý] [năm]" |
| JLL Vietnam | Hàng quý | "JLL Vietnam real estate [quý] [năm]" |
| DKRA Vietnam | Hàng tháng | "DKRA báo cáo thị trường [tháng] [năm]" |
| VARS | Hàng quý | "VARS báo cáo bất động sản [quý] [năm]" |
| Bộ Xây dựng | Hàng quý | "Bộ Xây dựng báo cáo thị trường BĐS [năm]" |

---

## 4. Quy hoạch

| Nguồn | URL | Ghi chú |
|-------|-----|---------|
| Cổng quy hoạch quốc gia | quyhoach.gov.vn | Bản đồ quy hoạch |
| UBND tỉnh/thành | [tỉnh].gov.vn | Quy hoạch chi tiết |
| Sở QH-KT | soquyhoach.[tỉnh].gov.vn | Chi tiết khu vực |

### Cách search

```
web_search: "quy hoạch [quận/huyện] [tỉnh/thành] [năm]"
web_search: "bản đồ quy hoạch [khu vực] mới nhất"
web_search: "quy hoạch đường [tên dự án hạ tầng]"
```

---

## 5. Tips tra cứu nâng cao

### Kết hợp nhiều nguồn — Ví dụ tra cứu TP Thủ Đức

```
web_search: "giá đất TP Thủ Đức 2026 m2"                    # Giá chung
web_search: "site:batdongsan.com.vn đất Thủ Đức giá"         # Rao bán
web_search: "bảng giá đất TP Thủ Đức UBND TP.HCM mới nhất"  # Nhà nước
web_search: "quy hoạch TP Thủ Đức metro"                     # Hạ tầng
web_search: "CBRE Thủ Đức bất động sản"                      # Phân tích
```

### Tránh dữ liệu sai

- **Kiểm tra ngày**: Bài cũ hơn 6 tháng có thể outdated
- **So sánh nguồn**: 1 nguồn chênh lớn → cần xác minh thêm
- **Phân biệt đơn vị**: triệu/m² vs tỷ/lô vs tỷ/căn
- **Rao bán ≠ giao dịch**: Giá rao thường cao hơn thực tế 5–15%
