# Window Commands

Control window state and position.

## Commands

| Subcommand | Description | Parameters | Example |
|------------|-------------|------------|---------|
| `list` | List all visible windows | None | `window list` |
| `focus` | Bring window to foreground | `--window-id` | `window --window-id 12345 focus` |
| `minimize` | Minimize window | `--window-id` | `window --window-id 12345 minimize` |
| `maximize` | Maximize window | `--window-id` | `window --window-id 12345 maximize` |
| `restore` | Restore window to normal | `--window-id` | `window --window-id 12345 restore` |
| `close` | Close window | `--window-id` | `window --window-id 12345 close` |
| `move` | Move window position | `--window-id`, `--x`, `--y` | `window --window-id 12345 move --x 100 --y 200` |
| `resize` | Resize window | `--window-id`, `--width`, `--height` | `window --window-id 12345 resize --width 800 --height 600` |

## Output Format

**Window List** returns content with boundary markers:
```
--- WINGUICTL_CONTENT nonce=<nonce> ---
- "Window Title" [window_id="123456" absolute_rect=(0,0 1920x1080) pid="1234" process="notepad.exe" state="maximized" foreground="true"]
  - "Child Window" [window_id="123457" absolute_rect=(10,10 200x100)]
--- END_WINGUICTL_CONTENT nonce=<nonce> ---
```

**Key Fields**:
- `window_id`: Window handle (required for all operations except `list`)
- `absolute_rect`: Screen-absolute coordinates (not window-relative)
- `state`: "minimized", "maximized", or "normal"
- `foreground`: "true" if window is in foreground

## Notes

- `absolute_rect` uses screen coordinates (different from `snapshot`/`find` which use window-relative `relative_rect`)
- Child windows are indented under parent windows in list output
- `close` sends WM_CLOSE message
