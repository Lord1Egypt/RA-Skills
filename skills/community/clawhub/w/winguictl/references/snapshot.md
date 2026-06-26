# Snapshot Commands

Capture window structure snapshots (HWND/UIA/OCR).

## Commands

| Subcommand | Description | Key Output Fields | Performance Options |
|------------|-------------|-------------------|---------------------|
| `hwnd` | Win32 HWND tree | `hwnd`, `class`, `control_type`, `visible`, `text`, `control_id`, `relative_rect` | `--max-depth` |
| `uia` | UIA element tree | `control_type`, `class`, `automation_id`, `runtime_id`, `supported_actions`, `relative_rect` | `--max-depth`, `--skip-actions`, `--skip-state` |
| `ocr` | OCR text regions | `text`, `relative_rect`, `confidence` | None |

## Usage

```powershell
# HWND tree
snapshot --window-id <id> hwnd

# UIA tree (with performance options for Qt apps)
snapshot --window-id <id> uia --skip-actions --skip-state

# UIA tree with depth limit
snapshot --window-id <id> --max-depth 3 uia

# OCR text
snapshot --window-id <id> ocr
```

## Output Format

All snapshots use boundary markers with window-relative coordinates:
```
--- WINGUICTL_CONTENT nonce=<nonce> ---
- "Window Title" [control_type="Window" class="Notepad" hwnd="123456" relative_rect=(0,0 800x600)]
  - "Text Content" [control_type="Edit" class="Edit" hwnd="123457" relative_rect=(8,31 784x561)]
--- END_WINGUICTL_CONTENT nonce=<nonce> ---
```

## Element IDs for Interaction

**UIA elements** provide identifiers for `uia-control` commands:
- `automation_id`: String identifier (may have duplicates in Qt apps)
- `runtime_id`: Hyphen-separated numeric ID (guaranteed unique, **preferred**)

```powershell
# Use runtime_id (preferred)
uia-control --window-id <id> --element-id "42-3155764" click

# Use automation_id
uia-control --window-id <id> --element-id "SubmitButton" click
```

## Performance Optimization

For **Qt applications** (Kate, Qt Creator), UIA traversal is slow. Use these flags:

| Flag | Effect | When to Use |
|------|--------|-------------|
| `--skip-actions` | Skip collecting supported actions | When action info not needed |
| `--skip-state` | Skip collecting element state | When state info not needed |
| `--max-depth` | Limit tree depth | For large windows |

**Note**: When `--skip-actions` is used, `--action` filter in `find uia` is ignored.

## OCR Warning

OCR captures all visible text, which may include sensitive information. Close sensitive windows before running OCR commands.

## Dependencies

- `hwnd`/`uia`: `pywinauto`
- `ocr`: `wx-ocr` (optional)
