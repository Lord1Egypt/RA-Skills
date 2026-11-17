# Worked Example: "Yêu tinh, đừng hòng loạn ta hiếu tâm"

Novel translated in Jun 2026. Chinese web novel, ~12.5 MB, 762 chapters, 1032 parts.

## Thư mục dự án

```
<project-dir>/
├── raw/                    # 1032 parts (12KB each)
├── out/                    # Translated parts
├── TenRieng.md             # Character/term name table
├── XungHo.md               # Address matrix
├── full.md                 # Merged output (after all parts done)
└── *.txt / *.md            # Source files
```

## TenRieng.md khởi tạo (Part 0001)

| Tên gốc | Tên dịch | Ghi chú |
|---------|----------|---------|
| 楚无疾 | Sở Vô Tật | Nam chính, 17-18 tuổi, xuyên không |
| 白素锦 | Bạch Tố Cẩm | Mẹ nuôi, đại yêu |
| 寡妇掌柜 | Quả phụ chưởng quầy | Chủ tiệm thuốc, yêu tinh |
| 恭文帝 | Cung Văn Đế | Hoàng đế Ly Hỏa (đã băng) |
| 离火国 | Ly Hỏa Quốc | Nước trong truyện |
| 离火王室 | Ly Hỏa Vương Thất | Vương thất Ly Hỏa |
| 京城 | Kinh Thành | Kinh đô Ly Hỏa |
| 黑玉回魂丹 | Hắc Ngọc Hồi Hồn Đan | Đan dược hồi hồn |
| 安神汤 | An Thần Thang | Thang an thần |

## XungHo.md khởi tạo

| Người nói \ Người nghe | Sở Vô Tật | Bạch Tố Cẩm | Quả phụ chưởng quầy |
|------------------------|-----------|-------------|---------------------|
| Sở Vô Tật | - | Con / Mẹ | Em / Chị (掌柜姐姐) |
| Bạch Tố Cẩm | Mẹ / Vô Tật | - | ? |
| Quả phụ chưởng quầy | Chị/Em (好弟弟) | ? | - |

## Workflow ghi nhớ

1. **Đọc part gốc** → xác định nhân vật mới, tên riêng, cách xưng hô
2. **Cập nhật `TenRieng.md`** và `XungHo.md` ngay lập tức
3. **Dịch** bằng `execute_code` + Python (KHÔNG dùng cat heredoc)
4. **Ghi** vào `out/part_xxxx.md` bằng `Path.write_text()`
5. **Lặp lại** cho part tiếp theo

## Lưu ý dịch thuật

- Giữ nguyên tên nhân vật chính (Sở Vô Tật, Bạch Tố Cẩm)
- Dịch tên địa danh (离火 → Ly Hỏa)
- Giữ nguyên tên đan dược/thuật ngữ (黑玉回魂丹 → Hắc Ngọc Hồi Hồn Đan)
- Dịch xưng hô theo quan hệ: 掌柜姐姐 → chưởng quầy tỷ tỷ, 好弟弟 → em trai, 干娘 → mẹ nuôi
- Dịch thoại giữ nguyên dấu ngoặc kép, văn phong tự nhiên tiếng Việt
- Giữ cấu trúc chương gốc (Chương 1 → Chương 1)
