---
name: xiaohongshu-publisher
description: Publish notes (posts) to Xiaohongshu (小红书) via the Creator Platform using browser automation (CDP). Use when user asks to post/publish/发布 content on Xiaohongshu/小红书, create notes with images, or manage their Xiaohongshu account.
---

# Xiaohongshu Publisher

Automate publishing notes to Xiaohongshu (小红书) via the Creator Platform (creator.xiaohongshu.com) using browser CDP.

## Prerequisites

- Browser with CDP access (Chromium with `--remote-debugging-port`)
- User must be **already logged in** to Xiaohongshu (manual QR scan login required — automation is blocked by anti-bot detection)
- Chinese font installed (e.g., `DroidSansFallbackFull.ttf`) for cover image generation

## Workflow

### 1. Verify Login Status

```
browser open → https://creator.xiaohongshu.com
browser snapshot → check if logged in (look for user avatar/name)
```

If not logged in, ask user to scan QR code manually. Phone number login is blocked by anti-automation detection.

### 2. Navigate to Publish Page

```
browser open → https://creator.xiaohongshu.com/publish/publish
```

Wait for the editor to load. Look for the upload area and editor elements.

### 3. Upload Cover Image

Upload image via CDP `DOM.setFileInputFiles`:

```javascript
// Find the file input element
const fileInput = document.querySelector('input[type="file"]');
// Use CDP to set file
DOM.setFileInputFiles({ files: ['/path/to/image.jpg'], objectId: ... })
```

**⚠️ Cover Image Text Rendering**: On systems without full CJK fonts, Chinese text in generated images may show as squares (□). Solutions:
- Use `DroidSansFallbackFull.ttf` for Chinese characters
- Use a mixed font approach: CJK font for Chinese + DejaVu/system font for ASCII
- Always verify the image before uploading

### 4. Input Title

Use CDP `Input.insertText` for reliable Chinese text input (avoids encoding issues):

```javascript
// Click title input field first
// Then use CDP:
Input.insertText({ text: "你的标题" })
```

**Title limit**: 20 characters max.

### 5. Input Body Content

Target the ProseMirror editor:

```javascript
// Selector: .tiptap.ProseMirror (contenteditable div)
// Click to focus, then use Input.insertText
```

Supports basic formatting. For hashtags, type `#话题` and select from dropdown.

### 6. Publish

Click the publish button. Use coordinate-based click (`Input.dispatchMouseEvent`) if selector-based click fails:

```javascript
Input.dispatchMouseEvent({ type: 'mousePressed', x: X, y: Y, button: 'left', clickCount: 1 })
Input.dispatchMouseEvent({ type: 'mouseReleased', x: X, y: Y, button: 'left', clickCount: 1 })
```

### 7. Verify Publication

After publishing, check for:
- Success: redirect to content management page
- Failure: `error_code=300031` means content was taken down (usually image issues)

## Key Technical Details

- **Tab switching**: `.creator-tab:not(.active)` CSS selector for switching between image/video modes
- **Anti-automation**: Xiaohongshu has aggressive bot detection. Avoid rapid automated actions. Add delays between steps.
- **Content moderation**: Posts may be auto-reviewed and taken down. Check content management page for status.
- **Image requirements**: Recommended ratio 3:4, minimum 960x1280px for best display

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Login blocked | Use QR code scan (manual), not phone number |
| Chinese text shows □ in images | Use DroidSansFallbackFull.ttf font |
| Post taken down (300031) | Check cover image for rendering issues |
| Title input garbled | Use `Input.insertText` CDP method |
| Publish button unresponsive | Use coordinate-based mouse events |
| Cannot delete posts via API | Use web UI manually; API returns 404 |

## Reference: User Profile Access

To fetch user profile info:
```
browser open → https://www.xiaohongshu.com/user/profile/{userId}
browser snapshot → extract follower count, note count, etc.
```
