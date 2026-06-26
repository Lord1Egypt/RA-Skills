---
name: fb-repost
description: >
  Skill để lấy nội dung từ link bài viết Facebook, viết lại bài theo phong cách phù hợp, 
  tạo ảnh minh họa bằng Gemini, rồi đăng lên Facebook Page qua Graph API. 
  KÍCH HOẠT khi user đưa link Facebook và muốn repost, đăng lại, viết lại bài, 
  hay nói "lấy bài này đăng lên page". Dùng skill này BẤT CỨ KHI NÀO có link FB + yêu cầu đăng bài.
---

# FB Repost Skill

Workflow: **Scrape → Rewrite → Image → Post**

## Yêu cầu credentials (lần đầu)

Nếu chưa có, hỏi user cung cấp:

1. **APIFY_TOKEN** — https://console.apify.com/account/integrations
2. **GEMINI_API_KEY** — https://aistudio.google.com/app/apikey  
3. **FB_PAGE_ID** — ID Facebook Page
4. **FB_PAGE_ACCESS_TOKEN** — Page Access Token (permission `pages_manage_posts`)

> Gợi ý user lưu vào OpenClaw secrets/env vars để không nhập lại.

---

## Workflow chi tiết

### Bước 1: Scrape bài viết Facebook

Chạy script scrape:
```bash
python3 scripts/scrape_fb.py "<FB_POST_URL>" "<APIFY_TOKEN>"
```

Script trả về JSON với các trường:
- `text` — nội dung bài viết
- `images` — array URL ảnh
- `video` — URL video (nếu có)
- `likesCount`, `commentsCount` — engagement stats
- `pageName` — tên page gốc

Nếu lỗi → thử actor thay thế `apify~facebook-scraper`

### Bước 2: Phân tích & Viết lại bài

Phân tích bài gốc:
- **Thể loại**: tin tức, cảm xúc, kiến thức, hài hước, viral...
- **Tone**: nghiêm túc, vui vẻ, cảm động...
- **Độ dài**: ngắn/vừa/dài

**Nguyên tắc viết lại:**
- KHÔNG copy nguyên văn — paraphrase hoàn toàn
- Giữ thông tin cốt lõi (số liệu, tên, sự kiện)
- Thêm hook mạnh ở đầu
- Kết bằng CTA hoặc câu hỏi tương tác
- Dùng emoji vừa phải
- Độ dài: 150-400 chữ (tối ưu Facebook)

**Template theo thể loại:**

| Thể loại | Cấu trúc |
|----------|----------|
| Tin tức | [Hook sự kiện] → [Nội dung] → [Bình luận] → "Bạn nghĩ sao?" |
| Kiến thức | [Hook "Bạn có biết"] → [Danh sách] → [Takeaway] → "Bạn đã thử chưa?" |
| Cảm xúc | [Hook câu chuyện] → [Viết lại] → [Bài học] → "Tag ngưỉi chia sẻ!" |
| Hài hước | [Hook hài] → [Nội dung] → "Đúng không? Share ngay!" |

### Bước 3: Tạo ảnh với Gemini

Soạn image prompt từ nội dung đã rewrite:
```
[Mô tả visual chính], [style: realistic/illustrative/infographic], 
[màu sắc/mood phù hợp], no text overlay, high quality, 16:9 ratio
```

Chạy script tạo ảnh:
```bash
python3 scripts/generate_image.py "<IMAGE_PROMPT>" "<GEMINI_API_KEY>" /tmp/fb_image.png
```

### Bước 4: Đăng lên Facebook Page

**Upload ảnh trước (nếu có):**
```bash
python3 scripts/post_fb.py upload-photo "<PAGE_ID>" "<PAGE_TOKEN>" /tmp/fb_image.png
```
→ Trả về `photo_id`

**Đăng bài:**
```bash
python3 scripts/post_fb.py post "<PAGE_ID>" "<PAGE_TOKEN>" "<MESSAGE>" "<PHOTO_ID>"
```

---

## Checklist trước khi đăng

- [ ] Hiển thị bài viết đã rewrite cho user xem
- [ ] Hiển thị ảnh đã tạo (hoặc mô tả)
- [ ] Hỏi: "Bạn muốn đăng luôn hay chỉnh sửa gì không?"
- [ ] Chỉ đăng khi user xác nhận ✅

---

## Xử lý lỗi

| Lỗi | Nguyên nhân | Xử lý |
|-----|------------|-------|
| Apify rỗng | Link private/xóa | Báo user, xin paste nội dung thủ công |
| Gemini 429 | Rate limit | Retry sau 10s |
| FB 200 | Token hết hạn | Hướng dẫn refresh Page Access Token |
| FB 368 | Vi phạm policy | Rewrite nhẹ hơn, bỏ từ nhạy cảm |

---

## Flow tóm tắt

```
User đưa link FB
    ↓
[Apify] Scrape nội dung
    ↓
[Claude] Phân tích → Viết lại
    ↓
[Gemini] Tạo ảnh
    ↓
[Claude] Preview → Xin xác nhận
    ↓
[FB Graph API] Upload → Đăng
    ↓
Trả về link bài đã đăng ✅
```

## References

- API docs chi tiết: [references/api_docs.md](references/api_docs.md)
