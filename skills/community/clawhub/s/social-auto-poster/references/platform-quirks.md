# Platform Quirks & Gotchas

Real-world issues discovered through production use. Read this when a platform behaves unexpectedly.

## LinkedIn

### Shadow DOM Upload
The "Upload from computer" input lives inside `div.theme--light`'s shadow root. Standard selectors and `browser upload selector=...` won't reach it. ARM + Playwright native click is the only reliable path.

```javascript
// For debugging only — do NOT use this to upload; use ARM instead
const div = document.querySelector('div.theme--light');
const input = div.shadowRoot.querySelector('input[type=file]');
```

### Leftover Images from Previous Sessions
If LinkedIn detects an in-progress draft, the Editor dialog may show "2 of 2" or "1 of 2". Always check the counter before clicking Next. Use the Delete button to remove extras until "1 of 1" remains.

### Post Button Stays Grey
The text editor is inside shadow DOM. `type selector` targeting a CSS class won't reach it. Use `type ref` with the ref from snapshot (accessibility tree ref, e.g., `e7`). Verify via:
```javascript
document.querySelector('div.theme--light').shadowRoot.querySelector('[contenteditable]').innerText.length
```

---

## X / Twitter

### Two Posts Instead of One (Image + Text Separate)
This happens when `evaluate element.click()` is used to open the file picker. JS clicks do not trigger ARM. Result: image attaches via one mechanism, text types into a different compose state — they post as two separate tweets.

**Fix:** Always get the "Add photos or video" ref from snapshot and use `browser act kind=click ref=eXX`.

### Ref Expires After Image Attaches
After ARM fires and the image appears, the DOM re-renders. Refs from the pre-image snapshot are no longer valid. Always take a new snapshot after `blob=1` is confirmed to get fresh refs for the textbox.

### 280 Character Limit
X counts URLs as 23 characters regardless of actual length. Count raw text length before typing. If `tweetButton.disabled === true` after typing, check:
```javascript
document.querySelector('[data-testid="tweetTextarea_0"]').innerText.length
```

---

## Facebook

### Three Textboxes Before Image, One After
Before image upload, Facebook renders 3+ `[role=textbox][contenteditable=true]` elements. After the image loads, only 1 remains (the compose textbox). Always query AFTER `blob=1`.

### ARM vs Direct Upload
- ARM (no selector) works when triggered before clicking "Ảnh/video"
- `browser upload selector=input[type="file"]` can work as fallback if the input becomes visible after dialog opens

### Notification Panel Opens Instead of Compose Dialog
If clicking "Bạn đang nghĩ gì?" triggers the notification panel, the JS selector matched the wrong element. Use: `[...document.querySelectorAll('[role="button"]')].find(b => b.textContent.includes('đang nghĩ gì'))` to target the correct one.

### Compose Dialog Not at Index 0
Facebook renders multiple `[role=dialog]` elements simultaneously (notifications, compose, etc.). Always find the compose dialog by text content: `dialogs.find(d => d.innerText.includes('Tạo bài viết'))`.

---

## WordPress

### Yoast OG Image Shows Avatar Instead of Post Image
WordPress REST API sets the featured image but Yoast SEO has separate OG image fields. If you skip the Yoast PATCH step, Facebook/LinkedIn shares will show the author avatar instead of the post image.

Always patch after publishing:
```bash
curl -X POST "$WP_URL/wp-json/wp/v2/posts/POST_ID" \
  -u "$WP_USER:$WP_APP_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{"meta":{"_yoast_wpseo_opengraph-image":"IMAGE_URL","_yoast_wpseo_opengraph-image-id":MEDIA_ID}}'
```

### Heredoc Breaks UTF-8
Building JSON with `cat << EOF` in bash mangles Vietnamese characters. Always use Python `json.dump(..., ensure_ascii=False)` and write to a temp file, then POST with `--data-binary @file.json`.

---

## Substack

### Text Disappears if Typed Before Image
Substack's ProseMirror editor resets when an image is inserted. Text typed before inserting the image gets wiped. Always: image first → wait → text second.

### Wrong URL Format
`substack.com/new` does not work for most publications. Use the publication subdomain:
`[publication].substack.com/publish/post/new`

### Long Text Timeout
ProseMirror can be slow with large text blocks. Use `timeoutMs=60000` when typing long posts.
