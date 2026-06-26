# Changelog

## [2.0.1] - 2026-06-13

### Fixed
- **YAML frontmatter added**: Added `---` frontmatter block with `name` and `description` to SKILL.md
  - This makes OpenClaw's skill loader detect the skill properly
  - Previously the skill was silently discarded because the loader requires both fields from frontmatter

## [2.0.0] - 2026-05-14

### Added
- **Quality parameter for `/capture`**: Optional quality override (1-100)
  - Body: `{"quality": 60}` for faster/smaller captures
  - Defaults to 90 if not specified
  - Response includes `quality` field: `{"ok": true, "path": "...", "quality": 60}`

### Changed
- **Updated docs**: README and SKILL.md now document quality feature
- **Gitignore**: Added `.gitignore` to exclude `screenshot.jpg`

## [1.5.0] - 2026-04-12

### Added
- **Cursor movement endpoint**: `POST /move` - Move mouse cursor without clicking
  - Body: `{"x": 500, "y": 300}`
  - Useful for hovering before clicking or UI traversal

## [1.4.0] - 2026-04-12

### Changed
- **Single screenshot file**: Saves to `screenshot.jpg` in skill folder, overwritten each capture
  - No more numbered frame files
  - Simpler to consume from other tools
- **Simplified capture response**: Removed `frame` counter and `screen` dimensions from `/capture` endpoint
  - Response is now simply: `{"ok": true, "path": "..."}`
- **Removed endpoint**: `GET /frames` - no longer needed with single screenshot
- **License**: MIT-0 (ClawHub requires all skills to be MIT-0)

### API Changes
**Before:**
```bash
POST /capture  # Returns {"path": ".../frames/frame_000001.jpg", "frame": 1, "screen": {...}}
GET /frames    # List all frames
```

**After:**
```bash
POST /capture  # Returns {"path": ".../screenshot.jpg"}
# GET /frames removed
```

## [1.3.0] - 2026-04-11

### Changed
- **Native Windows support**: No longer requires WSL
  - Screenshots saved to user's `Pictures/WinControl/` folder
  - Added `start.bat` for easy native Windows startup
  - WSL still supported as legacy mode
- **Auto-cleanup**: All screenshots deleted when server stops (Ctrl+C)
  - Tracks created files and cleans up on SIGINT, SIGTERM, or normal exit
  - Uses `atexit` and signal handlers for reliable cleanup
- **Better error handling**:
  - Input validation for coordinates, buttons, and key arrays
  - Proper HTTP status codes (400, 404, 413, 500)
  - Graceful fallbacks for screen detection and file operations
  - Request body size limit (10MB)
- **New endpoint**: `GET /frames` - List all captured frames

### Added
- `start.bat` - Native Windows start script
- Frame persistence tracking - remembers highest frame number across restarts

### Removed
- Hardcoded WSL paths - now uses `%USERPROFILE%\Pictures\WinControl`
- Manual cleanup required - now automatic

## [1.2.0] - 2026-04-11

### Changed
- **Unified keyboard API**: Merged `/type`, `/key`, and `/combo` into single `/enter` endpoint
  - Accepts a list of keys that can be text, special keys, or modifier combinations
  - Automatically detects intent: text strings are typed, modifiers trigger combos

### API Changes
**Before:**
```bash
POST /type  -d '{"text": "Hello"}'
POST /key   -d '{"key": "Enter"}'
POST /combo -d '{"keys": ["Ctrl", "C"]}'
```

**After:**
```bash
POST /enter -d '{"keys": ["Hello"]}'           # Type text
POST /enter -d '{"keys": ["Enter"]}'           # Press key
POST /enter -d '{"keys": ["Ctrl", "C"]}'       # Key combo
POST /enter -d '{"keys": ["Hello", "Enter"]}'  # Mixed sequence
```

### Removed
- `POST /type` endpoint (replaced by `/enter`)
- `POST /key` endpoint (replaced by `/enter`)
- `POST /combo` endpoint (replaced by `/enter`)

## [1.1.0] - 2026-04-09

### Changed
- **Simplified API**: Removed `/screen` and `/frames` endpoints
- **Enhanced `/capture`**: Now returns screen dimensions directly in the response
  - Added `screen: {width, height}` field to capture response
- **On-demand capture only**: No background thread, captures only when POSTed

### API Changes
**Before:**
```bash
GET /screen    # Get dimensions
curl -X POST /capture  # Returns {path, frame}
```

**After:**
```bash
curl -X POST /capture  # Returns {path, frame, screen}
```

### Removed
- `GET /screen` endpoint (functionality merged into `/capture`)
- `GET /frames` endpoint (no longer needed with on-demand capture)

## [1.0.0] - 2026-04-09

### Initial Release
- AI remote control for Windows desktop
- On-demand screenshot capture via `POST /capture`
- Mouse control: click, drag, scroll
- Keyboard control: type, key press, combinations
- WSL integration: saves frames to `/tmp/wincontrol/`
- HTTP API on port 8767
