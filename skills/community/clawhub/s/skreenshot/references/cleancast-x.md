# CleanShot X Workflows

CleanShot X is a premium screenshot tool for macOS with advanced features.

## Key Features

- **Custom save location** (not Desktop clutter)
- **Built-in OCR** (Cmd+Shift+O)
- **Auto-upload to cloud** (optional, generates shareable links)
- **Scrolling screenshots** (full webpage capture)
- **Screen recording** (GIF/MP4)
- **Annotation tools** (arrows, boxes, blur, text)

## Configuration

### Set Custom Save Location
1. CleanShot X Preferences → Save To → Custom Folder
2. Recommended: `~/Pictures/Screenshots`

### Auto-OCR
Enable auto-OCR on capture to make screenshots searchable immediately.

### Cloud Upload
- Uploads to cleancast.cloud (or custom S3)
- Generates short shareable URLs
- Optional: auto-copy URL to clipboard

## Workflow Integration

**Capture → Organize:**
1. Capture with CleanShot (saves to custom folder)
2. Run `scripts/archive_old_screenshots.py` weekly
3. OCR index updated automatically

**Capture → Share:**
1. Capture → auto-upload enabled
2. URL copied to clipboard
3. Paste in chat/docs

**Search:**
1. Use CleanShot OCR library (stored in metadata)
2. Or run `scripts/ocr_search.py` on folder

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Area capture | Cmd+Shift+A |
| Window capture | Cmd+Shift+W |
| Full screen | Cmd+Shift+F |
| OCR selection | Cmd+Shift+O |
| Last capture | Cmd+Shift+L |
