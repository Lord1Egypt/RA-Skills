# ARM Upload Guide

ARM (Automatic Request Manager) is OpenClaw's browser file upload interceptor. It queues a file to be attached the next time the browser opens a native file picker dialog.

## How ARM Works

1. Call `browser upload paths=[...]` — this ARMS the interceptor (queues the file)
2. The browser waits for a native `<input type="file">` to be triggered
3. When a file picker opens (via any Playwright-native click), ARM intercepts it and injects the queued file
4. The file appears as if the user selected it manually

## Critical Rules

### ARM fires on Playwright native click only
- `browser act kind=click ref=eXX` → ✅ triggers ARM
- `evaluate element.click()` → ❌ does NOT trigger ARM (JS click bypasses browser events)
- This is why X/Twitter must use `click ref` from snapshot for the "Add photos" button

### ARM is one-shot
- Each `browser upload` call arms exactly one intercept
- If the file picker closes without selecting, ARM stays armed but may not re-fire correctly
- Re-ARM by calling `browser upload` again before retrying the click

### ARM has no selector requirement for queuing
- `browser upload paths=["/path/to/file.png"]` — correct, no selector needed when arming
- `browser upload selector="input[type=file]" paths=[...]` — direct upload, bypasses ARM, only works on visible inputs

## Platform-Specific Notes

### LinkedIn
- Shadow DOM wraps the upload input — ARM is the only reliable method
- Click the Photo link (ref from snapshot) after arming

### X/Twitter
- Must snapshot first to get ref for "Add photos or video"
- Click ref (not evaluate) to trigger ARM

### Facebook
- ARM before clicking "Ảnh/video" button
- If blob=0 after 6s: arm again + click again
- `browser upload selector=input[type="file"]` also works as fallback if input becomes visible

### Substack
- ARM before clicking the Image toolbar button
- Image inserts directly into ProseMirror body
