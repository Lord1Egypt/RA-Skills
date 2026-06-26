# Slide Editor

A browser-based visual editor for HTML presentations. Self-contained, offline-capable, and designed for both AI agent control and direct user manipulation.

## Features

- **Select, Move, Resize** - Click to select, drag to move, 8-point resize handles
- **Text Editing** - Double-click to edit text inline
- **Add Elements** - Add text boxes and images via toolbar or API
- **Image Cropping** - Non-destructive crop using CSS clip-path
- **Slide Navigation** - Thumbnail strip with drag-to-reorder
- **History** - Full undo/redo support (Ctrl+Z / Ctrl+Shift+Z)
- **Theme Support** - Light, dark, and auto (system) themes
- **Clean Export** - Export HTML without editor artifacts

## Quick Start

### Build

```bash
cd ~/projects/slide-editor
bun install
bun run build
```

Output: `dist/editor.bundle.js` (~55KB minified)

## Usage

### Method 1: CLI Injection (Recommended)

From any directory, inject the editor into your HTML file:

```bash
# Full workflow: inject + enable + open (recommended)
~/projects/slide-editor/inject.ts presentation.html --inline --enable --open

# Inline mode (single file, portable)
~/projects/slide-editor/inject.ts presentation.html --inline --enable

# Link mode (separate bundle file)
~/projects/slide-editor/inject.ts presentation.html --link --enable

# Remove editor from HTML
~/projects/slide-editor/inject.ts presentation.html --remove
```

Options:
- `--inline` - Embed bundle directly in HTML (single file, shareable)
- `--link` - Reference external `editor.bundle.js` file
- `--enable` - Add auto-enable check
- `--open` - Open in browser after injection (editor auto-enabled)
- `--remove` - Remove editor from HTML
- `-o <file>` - Output to different file

### Method 2: Manual Copy

```bash
# Copy bundle to your HTML's directory
cp ~/projects/slide-editor/dist/editor.bundle.js /path/to/your/project/

# Add to your HTML before </body>
```

```html
<script src="editor.bundle.js"></script>
<script>
  // Enable via console or URL parameter
  if (new URLSearchParams(location.search).get('edit') === '1') {
    window.__openclawEditor.enable();
  }
</script>
```

### Method 3: AI Agent Integration

When generating HTML with an AI agent, include the bundle inline:

```javascript
// Read the bundle
const bundle = require('fs').readFileSync(
  require.resolve('slide-editor/dist/editor.bundle.js'),
  'utf-8'
);

// Inject into generated HTML
const html = generatedHtml.replace('</body>', `
<script>${bundle}</script>
<script>
if (new URLSearchParams(location.search).get('edit') === '1') {
  window.__openclawEditor.enable();
}
</script>
</body>`);
```

### Enable Editor

After injection, enable the editor by:

1. **URL**: Add `?edit=1` to the page URL
2. **Console**: Run `window.__openclawEditor.enable()`
3. **PostMessage**: `window.postMessage({ type: 'OPENCLAW_EDITOR_ENABLE' }, '*')`

Note: When using `--open` flag, the editor auto-enables without needing URL parameters.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl/Cmd + Z` | Undo |
| `Ctrl/Cmd + Shift + Z` | Redo |
| `Ctrl/Cmd + S` | Save (download) |
| `Delete` / `Backspace` | Delete selected |
| `Escape` | Deselect all |
| `P` | Toggle properties panel |
| `T` | Toggle theme (light/dark/auto) |
| `Shift + Click` | Multi-select |

## Development

```bash
# Watch mode
bun run dev

# Type check
bun run typecheck
```

## Project Structure

```
src/
├── index.ts           # Main entry, EditorAPI implementation
├── types.ts           # TypeScript type definitions
├── styles.ts          # CSS styles (injected when enabled)
├── core/
│   ├── SelectionManager.ts   # Selection state management
│   ├── DragManager.ts        # Pointer drag handling
│   ├── ResizeManager.ts      # 8-point resize handles
│   ├── TextEditor.ts         # Contenteditable wrapper
│   └── HistoryManager.ts     # Undo/redo stack
├── components/
│   ├── Toolbar.ts            # Top toolbar
│   ├── PropertiesPanel.ts    # Right sidebar properties
│   └── SlideNavigator.ts     # Bottom slide strip
└── serialization/
    └── Exporter.ts           # HTML export & image cropping
```

## API

Full API documentation in [SKILL.md](./SKILL.md).

### Quick Reference

```javascript
// Enable/disable
window.__openclawEditor.enable();
window.__openclawEditor.disable();

// Add elements
window.__openclawEditor.addText({ content: 'Title', fontSize: '48px' });
window.__openclawEditor.addImage({ src: 'image.png' });

// Modify elements
window.__openclawEditor.moveElement(id, x, y);
window.__openclawEditor.resizeElement(id, width, height);
window.__openclawEditor.setStyle(id, { color: 'red' });

// Export
const html = window.__openclawEditor.export();
```

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13.1+
- Edge 80+

Requires Pointer Events API.

## License

MIT
