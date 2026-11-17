# Token Usage Diagnostics — vn-translate

> Recipe để trả lời câu hỏi "tại sao token tiêu thụ cao mà chỉ dịch được bấy nhiêu?"
> Đã áp dụng thành công 08/2026 cho dự án Tỷ muội (144 parts).

## 1. Ước lượng token "hữu ích" từ file (không cần dashboard)

```python
def est_tokens(text: str) -> int:
    cjk = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    other = len(text) - cjk
    return cjk + other // 4   # CJK ≈1 token/ký tự, tiếng Việt ≈4 ký tự/token
```

Kết quả đo được (project Tỷ muội, 08/2026):
- 12 part (064–075): input raw ~42.4K + output dịch ~36.1K = **~78.5K token hữu ích**
- 1 part ≈ 3.5K input + 3.0K output ≈ 6.5K token hữu ích
- Toàn bộ 144 part nếu dịch hết: ~1.2M token hữu ích (cả 2 dự án)

## 2. So sánh với con số dashboard → hệ số chênh lệch

| Giai đoạn | Token tiêu thụ | Số part | Token/part | Hệ số vs hữu ích |
|-----------|---------------|---------|-----------|------------------|
| Có subagent nền (1–63) | 104,989,783 | 63 | **~1.67M** | ~250x |
| Dịch trực tiếp batch 2 (64–75) | 2,520,948 | 12 | **~0.21M** | ~32x |

→ Chênh ~8x GIỮA 2 GIAI ĐOẠN là do subagent nền (spawn + chết giữa chừng + retry),
KHÔNG phải do batch size (batch 2 chỉ giảm ~1.6x số lượt đọc).

## 3. Chẩn đoán subagent nền đã chạy (bằng chứng cứng từ file)

### a) Nhịp robot trong mtime
```python
import datetime
outs = sorted([f for f in (proj/"out").glob("part_*.md") if f.stat().st_size > 0],
              key=lambda f: int(f.stem.split("_")[1]))
for f in outs:
    print(f.stem, datetime.datetime.fromtimestamp(f.stat().st_mtime).strftime("%H:%M:%S"))
```
- Dấu hiệu subagent nền: **mtime cách đều ~1 phút/part** (01:14 → 02:01, part_035–063) —
  nhịp robot không phải nhịp agent chính (agent chính ghi từng part cách nhau 30–90s
  nhưng không đều, và thường đi theo cặp batch).
- Ngoài ra: một đợt file cùng mtime 01:12:33 (nhiều part bị touch/ghi hàng loạt).

### b) File 0 byte từ pipe stdin
- Process nền ghi out qua `python -c "...sys.stdin.buffer.read()..."` nhận 0 byte stdin
  → tạo `out/part_x.md` rỗng, thông báo `WROTE 0 0`.
- Đã xảy ra: part_038 (0 byte, đã xóa); process `proc_2e094507224b` kết thúc `WROTE 0 0`.
- Xử lý: xóa file rỗng ngay; trước khi merge: `find out -name '*.md' -size 0 -delete`.

## 4. Trình tự trả lời user

1. Đối chiếu: token hữu ích (mục 1) vs con số dashboard → hệ số (mục 2).
2. Giải thích: ~90% là input lặp lại (system prompt + skill + lịch sử hội thoại tích lũy
   mỗi lượt tool), không phải nội dung dịch.
3. Nếu có nghi ngờ subagent nền: xem mtime (3a) + file 0 byte (3b).
4. Đề xuất giảm chi phí: dịch tuần tự 1–2 part/lượt bởi agent chính, không spawn subagent,
   không đọc sample, verify chỉ bằng đếm số đoạn.
