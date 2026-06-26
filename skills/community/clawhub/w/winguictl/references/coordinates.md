# Coordinate Systems

Understanding winguictl coordinate systems.

## Coordinate Types

| Label | Description | Origin |
|-------|-------------|--------|
| `relative_rect` | Window-relative coordinates | Window top-left corner |
| `absolute_rect` | Screen-absolute coordinates | Screen top-left corner |

## Commands by Coordinate Type

### Window-Relative (`relative_rect`)

- `snapshot hwnd`
- `snapshot uia`
- `snapshot ocr`
- `find text`
- `find uia`
- `find ocr`
- `find image`

### Screen-Absolute (`absolute_rect`)

- `window list`

### Action Command Output

Action commands use nested objects instead of `relative_rect`/`absolute_rect`:

```json
{
  "relative": {"x": 100, "y": 200},
  "absolute": {"x": 500, "y": 300}
}
```

- `relative`: Included when using `--relative-x/y` or `--element-id`
- `absolute`: Included when using `--absolute-x/y` or `--element-id`

## Using Coordinates

Window-relative coordinates from `snapshot`/`find` can be used directly with `action click`:

```powershell
# Find button
find --window-id 12345 ocr "Submit"
# Output: - "Submit" [relative_rect=(100,200 80x30)]

# Click button center
action --window-id 12345 click --relative-x 140 --relative-y 215
```

**No coordinate conversion needed**.
