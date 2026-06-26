---
name: "social-auto-poster"
description: "Automate posting content with images to LinkedIn, X/Twitter, Facebook, WordPress, and Substack via browser automation. Use when: (1) posting a new article or social update to one or more platforms, (2) cross-platform publishing with platform-specific images, (3) verifying a post was published successfully. Includes image creation via overlay script, ARM upload pattern, and per-platform browser workflows. NOT for: reading feeds, DMs, analytics, or scheduling (use cron instead)."
license: MIT
metadata:
  version: 1.1.0
  author: quocmodoro
  category: marketing
---

# Social Auto Poster

Cross-platform publishing skill for LinkedIn, X/Twitter, Facebook, WordPress, and Substack. Covers one-time setup, image creation, ARM upload, text entry, and post verification for each platform.

---

## Prerequisites — One-Time Setup

Complete these steps once before using this skill for the first time.

### 1. Browser Login (LinkedIn, X, Facebook, Substack)

These four platforms use browser session authentication. You must log in manually once and keep the browser session alive.

```
browser start
navigate linkedin.com → log in if prompted
navigate x.com → log in if prompted
navigate facebook.com → log in if prompted
navigate [publication].substack.com → log in if prompted
browser stop
```

**Important rules:**
- Never run `pkill -f "Google Chrome"` or kill the browser process manually — this destroys all saved sessions and forces you to log in again
- Only use `browser stop` / `browser start` via OpenClaw to restart the browser safely
- Sessions persist in the browser profile directory and survive restarts as long as you use `browser stop`

### 2. WordPress Credentials

WordPress uses REST API with Application Password — no browser needed.

Create a credentials file at `~/.openclaw/.wp-[yoursite].env`:

```bash
WP_URL=https://yoursite.com
WP_USER=your_username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

To generate an Application Password:
1. Go to WordPress Admin → Users → Profile
2. Scroll to "Application Passwords"
3. Enter a name (e.g., "OpenClaw") → click Add New
4. Copy the generated password into the `.env` file

### 3. Image Overlay Script

This skill uses a shell script to generate quote images from your photo library. Locate or install it at:

```
~/workspace/linkedin-assets/create-overlay-image.sh
```

Verify it works:
```bash
bash ~/workspace/linkedin-assets/create-overlay-image.sh "Test quote" /tmp/test-output.png
ls -lh /tmp/test-output.png
```

Expected output: a PNG file with your quote overlaid on a background photo.

### 4. Upload Directory

Ensure the uploads directory exists:

```bash
mkdir -p /tmp/openclaw/uploads
```

Note: `/tmp/` is cleared on system reboot. Recreate images if needed after restart.

---

## Workflow Overview

For each post, follow this sequence:

```
Step 1: Create images (bash script) — before opening any browser
Step 2: Post to LinkedIn
Step 3: Post to X/Twitter (include LinkedIn link)
Step 4: Post to Facebook
Step 5: Post to WordPress (API, no browser)
Step 6: Post to Substack (browser)
Step 7: Verify all platforms
```

Always create both images first. Opening and closing the browser repeatedly wastes time and risks losing sessions.

---

## Step 1 — Create Images

Run both image commands before opening the browser:

```bash
# English image — used for LinkedIn and X
bash ~/workspace/linkedin-assets/create-overlay-image.sh \
  "Your English quote here" \
  /tmp/openclaw/uploads/[topic]-en.png

# Local language image — used for Facebook, WordPress, Substack
bash ~/workspace/linkedin-assets/create-overlay-image.sh \
  "Your local language quote here" \
  /tmp/openclaw/uploads/[topic]-vi.png
```

Verify both files exist and are non-empty before continuing:
```bash
ls -lh /tmp/openclaw/uploads/[topic]-en.png /tmp/openclaw/uploads/[topic]-vi.png
```

---

## Step 2 — LinkedIn

**Key constraint:** Upload dialog lives inside a Shadow DOM (`div.theme--light`). ARM + Playwright native click is required. Never use `evaluate input.click()`.

```
browser start → navigate linkedin.com/feed/ → wait for "Photo" text to appear

ARM upload:
  browser upload paths=["/tmp/openclaw/uploads/[topic]-en.png"]
  (no selector — ARM queues the file for the next file picker that opens)

snapshot → get ref for Photo button (an <A> link to /preload/sharebox/?detourType=IMAGE)
click ref [Photo] → wait for Editor dialog to open

  CHECK: if dialog shows "N of M" (e.g. "1 of 2") → leftover from previous session
  → click Delete button until counter shows "1 of 1"

click Next → wait for "Create post modal" to appear
snapshot → get ref for textbox labeled "Text editor for creating content"
click ref [textbox] → type ref [full post text including hashtags]
snapshot → verify Post button is active (not disabled)
click ref [Post] → wait 8s

Verify:
  navigate linkedin.com/in/[username]/recent-activity/all/
  evaluate: document.querySelectorAll('[data-urn]')[0].innerText → should contain your text

browser close tab → browser stop
```

---

## Step 3 — X / Twitter

**Key constraint:** ARM interceptor only fires on Playwright native click (`click ref`). Never use `evaluate btn.click()` to trigger the file picker — it breaks ARM and causes the image and text to post as two separate tweets.

**280-character limit:** Count characters before typing. If over, shorten the text first.

```
browser start → navigate x.com/compose/post → wait 3s

ARM upload:
  browser upload paths=["/tmp/openclaw/uploads/[topic]-en.png"]

snapshot depth=6 → get ref for "Add photos or video" button
  (depth=6 needed to expose buttons nested inside <navigation>)

click ref [Add photos or video] ← Playwright native click, NOT evaluate
wait 5s → evaluate: document.querySelectorAll('img[src*="blob:"]').length
  → must equal 1 before continuing

snapshot → get ref for textbox "Post text" (refs change after image attaches — always re-snapshot)
click ref [textbox] → type ref [text, max 280 characters]

evaluate: verify before posting
  document.querySelector('[data-testid="tweetButton"]').disabled === false
  document.querySelector('[data-testid="tweetTextarea_0"]').innerText.length ≤ 280

evaluate: document.querySelector('[data-testid="tweetButton"]').click()
wait 10s → evaluate: location.href → should be "https://x.com/home"

browser close tab → browser stop
```

**Tip:** Include the LinkedIn post URL in the X text to drive cross-platform traffic.

---

## Step 4 — Facebook

**Key constraint:** After the image uploads, Facebook switches to a new screen and the textbox count drops from 3 to 1. Always re-query the textbox AFTER `blob=1` is confirmed — typing before that goes into the wrong element.

```
browser start → navigate facebook.com → wait 5s

evaluate: click "What's on your mind?" / "Bạn đang nghĩ gì?" button
  [...document.querySelectorAll('[role="button"]')]
    .find(b => b.textContent.includes('đang nghĩ gì') || b.textContent.includes("on your mind"))
    .click()

wait 2s → verify "Create post" / "Tạo bài viết" dialog is open

ARM upload:
  browser upload paths=["/tmp/openclaw/uploads/[topic]-vi.png"]

evaluate: inside "Tạo bài viết" dialog, click the photo button:
  dialog.querySelector('[aria-label="Ảnh/video"]').click()
  (or "[aria-label='Photo/video']" for English UI)

wait 6s → evaluate: document.querySelectorAll('img[src*="blob:"]').length
  IF blob=0: ARM again + click photo button again (max 2 retries)

Once blob=1:
  evaluate: re-query textbox — after image loads there is exactly 1:
    document.querySelector('[role="dialog"] [role="textbox"][contenteditable="true"]')
  evaluate: tb.click(); tb.focus()
  browser act type selector='[role="dialog"] [role="textbox"][contenteditable="true"]'
    text=[full post text including hashtags]

evaluate: verify blob=1 AND textbox.innerText.length > 0

evaluate: click "Next" / "Tiếp" button
wait 5s
evaluate: click "Post" / "Đăng" button
wait 8s

evaluate: verify compose dialog is gone:
  !document.querySelectorAll('[role="dialog"]').some(d => d.innerText.includes('Tạo bài viết'))

browser close tab → browser stop
```

---

## Step 5 — WordPress (REST API)

No browser needed. Load credentials first:

```bash
source ~/.openclaw/.wp-[yoursite].env
```

**5a. Upload featured image:**
```bash
MEDIA=$(curl -s -X POST "$WP_URL/wp-json/wp/v2/media" \
  -u "$WP_USER:$WP_APP_PASSWORD" \
  -H "Content-Disposition: attachment; filename=post-image.png" \
  -H "Content-Type: image/png" \
  --data-binary @/tmp/openclaw/uploads/[topic]-vi.png)

MEDIA_ID=$(echo $MEDIA | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
IMAGE_URL=$(echo $MEDIA | python3 -c "import sys,json; print(json.load(sys.stdin)['source_url'])")
```

**5b. Build post JSON** (always use Python — never heredoc, heredoc breaks UTF-8):
```bash
python3 -c "
import json
post = {
  'title': 'Your Post Title',
  'content': '<p>Full HTML content here.</p>',
  'status': 'publish',
  'categories': [8],
  'featured_media': $MEDIA_ID
}
with open('/tmp/wp-post.json', 'w') as f:
    json.dump(post, f, ensure_ascii=False)
"
```

**5c. Publish:**
```bash
POST=$(curl -s -X POST "$WP_URL/wp-json/wp/v2/posts" \
  -u "$WP_USER:$WP_APP_PASSWORD" \
  -H "Content-Type: application/json" \
  --data-binary @/tmp/wp-post.json)

POST_ID=$(echo $POST | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
POST_URL=$(echo $POST | python3 -c "import sys,json; print(json.load(sys.stdin)['link'])")
echo "Published: $POST_URL"
```

**5d. Patch Yoast SEO OG image** (required — skipping this causes avatar.jpg to show when the post is shared):
```bash
curl -s -X POST "$WP_URL/wp-json/wp/v2/posts/$POST_ID" \
  -u "$WP_USER:$WP_APP_PASSWORD" \
  -H "Content-Type: application/json" \
  -d "{\"meta\":{\"_yoast_wpseo_opengraph-image\":\"$IMAGE_URL\",\"_yoast_wpseo_opengraph-image-id\":$MEDIA_ID}}"
```

**5e. Verify OG image:**
```bash
curl -s "$WP_URL/wp-json/wp/v2/posts/$POST_ID?_fields=yoast_head_json" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['yoast_head_json']['og_image'][0]['url'])"
# Should print the post image URL, not avatar.jpg
```

**Default category IDs** (adjust per site): 8=Business, 6=Marketing, 14=Skills, 10=Lifestyle, 5=Other

---

## Step 6 — Substack

**Key constraint:** Insert the image into the body FIRST, then type text. Opposite of Facebook. Text typed before image insertion gets wiped when ProseMirror re-renders.

```
browser start
navigate [publication].substack.com/publish/post/new → wait 5s
  (NOT substack.com/new — must use the publication subdomain URL)

snapshot → type Title → type Subtitle (if needed)

ARM upload:
  browser upload paths=["/tmp/openclaw/uploads/[topic]-vi.png"]

snapshot → get ref for Image button in ProseMirror toolbar
click ref [Image] → wait for file picker → ARM intercepts → image inserts into body
wait 5s → verify image blob appears in editor content

snapshot → get ref for .ProseMirror-focused editor area
type ref [full post content] (timeoutMs=60000 for long posts)

click Continue → wait 5s
snapshot → click "Send to everyone now" / "Publish now"
wait 8s → verify publish confirmation appears

browser tabs → get targetId → browser close targetId → browser stop
```

**Verify:** Navigate to `[publication].substack.com` — latest post should appear at the top.

---

## Step 7 — Verification Checklist

After posting to all platforms:

| Platform | Verify by |
|----------|-----------|
| LinkedIn | recent-activity page — post text visible + image attached |
| X | x.com/home feed — tweet with image visible |
| Facebook | Profile or Page feed — post with image and full text visible |
| WordPress | Visit post URL — featured image correct, OG image not avatar |
| Substack | Publication homepage — post appears at top |

---

## Error Reference

| Symptom | Cause | Fix |
|---------|-------|-----|
| X: two posts (1 image-only, 1 text-only) | Used `evaluate btn.click()` for Add photos | Must use `click ref` from snapshot |
| X: Post button stays disabled | Text over 280 chars | Check `tweetTextarea_0.innerText.length`, trim and retype |
| FB: image uploaded but no text in post | Typed before blob=1 | Re-query textbox after blob=1 confirmed |
| FB: blob=0 after 6s | ARM missed the file input | ARM again + click Ảnh/video again (max 2 retries) |
| LinkedIn: "N of M" in Editor | Leftover image from previous session | Delete extras until "1 of 1" |
| LinkedIn: Post button stays grey | Text not in shadow DOM editor | Use `type ref` not `type selector` |
| WP: avatar shows on social share | Yoast OG image not patched | Run Step 5d and verify Step 5e |
| Substack: text missing after publish | Text typed before image insertion | Always insert image first, then type |
| Substack: page not found | Wrong URL format | Use `[pub].substack.com/publish/post/new` not `substack.com/new` |
| All platforms: session lost after restart | Browser was killed manually | Never `pkill Chrome`; always use `browser stop` |

---

## Platform Summary

| Platform | Image variant | Auth method | Tool |
|----------|--------------|-------------|------|
| LinkedIn | EN | Browser session | `browser` + ARM |
| X/Twitter | EN | Browser session | `browser` + ARM (native click only) |
| Facebook | Local/VI | Browser session | `browser` + ARM + re-query textbox |
| WordPress | Local/VI | App password in `.env` | `curl` REST API |
| Substack | Local/VI | Browser session | `browser` + ARM (image before text) |
