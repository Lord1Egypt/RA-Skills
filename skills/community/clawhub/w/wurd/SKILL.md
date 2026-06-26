---
description: "Compile markdown documents with plugin tags into editorial-quality HTML pages using Wurd. USE FOR: creating documents, adding plugins, configuring layout, writing custom plugins, debugging compilation issues. DO NOT USE FOR: general markdown questions unrelated to this tool."
---

# Wurd Skill

You are working with **Wurd** ([github.com/vreff/Wurd](https://github.com/vreff/Wurd)), a document compiler that turns markdown files with `[plugin:name]...[/plugin]` tags into self-contained editorial HTML pages.

## How to Compile

```bash
# From the project root:
npx tsx src/cli.ts <path-to-markdown> [--no-cache] [--pdf] [--plugins <dir>]

# Or if installed globally:
wurd <path-to-markdown>
```

Output goes to `dist/<parent-dir-name>/index.html`.

## Document Format

Documents are markdown files. Optional YAML frontmatter between `---` controls layout and theme.

### Frontmatter (all optional)

```yaml
---
columns: 2              # 1, 2, 3, or 'auto'
columnWidth: 500         # target px per column
dropCap: true            # decorative first letter
accentColor: '#7c6ee6'   # drop cap and accent color
h1MaxFontSize: 120       # max px for h1 headline fitting
headingUnderline: 'subtitle'  # comma-separated element IDs to underline
pointerEventsNone: 'title'    # comma-separated element IDs for pointer passthrough
---
```

Key layout properties: `gutter`, `narrowGutter`, `narrowBreakpoint`, `maxContentWidth`, `columnGap`, `paragraphSpacing`, `sectionGap`, `bodyFontSize`, `bodyLineHeight`.

Heading properties: `h1MaxFontSize`, `h2MaxFontSize`, `h3MaxFontSize`, `h1MaxHeight`, `h2MaxHeight`, `h3MaxHeight`, `headingMinFontSize`, `headingLineHeightRatio`, spacing (`h1SpacingAbove`, `h2SpacingAbove`, `h3SpacingAbove`, `headingSpacingBelow`, `subheadingSpacingBelow`).

Color properties: `bgColor`, `textColor`, `headingColor`, `pullQuoteColor`, `pullQuoteBorderColor`, `headingUnderlineColor`.

### Plugin Tag Syntax

**Inline** (within a paragraph):
```
Some text [plugin:math]x^2[/plugin] more text.
```

**Block** (on its own lines):
```
[plugin:math]
\[E = mc^2\]
[/plugin]
```

**With config** (key: value lines, used by plugins like binary-stream):
```
[plugin:binary-stream]
rows: 12
position: absolute
top: 80px
left: var(--content-left)
right: var(--content-right)
[/plugin]
```

### Element IDs

Tag headings with `{#id}` for use in frontmatter features:
```markdown
# Title {#title}
## Subtitle {#subtitle}
```

### Blocks

Group content with `[block]...[/block]`:
```markdown
[block]
Paragraph and plugin stay together.

[plugin:math]\[x^2\][/plugin]
[/block]
```

## Built-in Plugins

### Deterministic (no LLM needed)

- **math**: KaTeX rendering. Inline `[plugin:math]x^2[/plugin]` or block with `\[...\]` delimiters.
- **accordion**: FAQ sections. Format: `Title | Body text` per line.
- **cite**: Citations. Format: `Author, "Title", Year, URL`. Auto-generates references section.
- **binary-stream**: Decorative binary digit grid with mouse-hover glow effect. Config keys: `rows`, `cols`, `fontSize`, `lineHeight`, `opacity`, `glowRadius`, `dimColor`, `litColor`. All other keys become inline CSS styles.

### LLM-powered (require LLM_API_KEY)

- **graph**: Describe a chart in natural language. Generates SVG via LLM.
- **table**: Describe table contents in natural language. Generates HTML via LLM.

## LLM Setup

Create `.env` in the project root:
```env
LLM_API_KEY=sk-...
LLM_BASE_URL=https://api.anthropic.com/v1
LLM_MODEL=claude-opus-4-6
```

Without this, deterministic plugins still work. LLM responses are cached in `.cache/llm/` — use `--no-cache` to regenerate.

## Creating Custom Plugins

Plugins live in `plugins/<name>/index.ts` (or flat `plugins/<name>.ts`). External plugins via `--plugins <dir>`.

### Deterministic Plugin Template

```typescript
import type { DeterministicPlugin } from '../../src/plugins.js'

const myPlugin: DeterministicPlugin = {
  name: 'my-plugin',
  mode: 'deterministic',
  render(content: string, id: string): string {
    return `<div id="${id}">${content}</div>`
  },
  layoutHints: {           // optional
    spanKey: 'my-plugin',
    defaultSpan: 'column', // or 'all'
    marginTop: 16,
    marginBottom: 20,
  },
  assets: {                // optional
    css: `.my-class { color: white; }`,
    headElements: [],
    runtimeModule: join(__dirname, 'runtime.ts'),
  },
}
export default myPlugin
```

### LLM Plugin Template

```typescript
import type { LLMPlugin } from '../../src/plugins.js'

const myPlugin: LLMPlugin = {
  name: 'my-plugin',
  mode: 'llm',
  systemPrompt: 'You generate HTML.',
  guidelines: 'Dark theme, modern aesthetic.',
  extractContent(response: string): string {
    const match = response.match(/```html\s*\n([\s\S]*?)```/)
    return match ? match[1] : response
  },
}
export default myPlugin
```

### Runtime Modules

If a plugin needs browser-side JavaScript, set `assets.runtimeModule` to a TS file that exports `init()`. It gets bundled into the page via esbuild and called after fonts load.

## Key Files

- `src/cli.ts` — CLI entry point, orchestrates compilation
- `src/parser.ts` — Markdown parsing, plugin tag extraction, `{#id}` support
- `src/plugins.ts` — Plugin loading, execution, layout hint wrapping
- `src/template.ts` — HTML page template with all base CSS
- `src/llm.ts` — LLM client with file-based caching
- `src/runtime/layout.ts` — Pretext-powered editorial layout engine (runs in browser)
- `src/runtime/main.ts` — Browser runtime entry point

## Common Tasks

**Add a new document:** Create `examples/my-doc/text.md`, then `npx tsx src/cli.ts examples/my-doc/text.md`.

**Add a new plugin:** Create `plugins/my-plugin/index.ts` with a default export implementing `DeterministicPlugin` or `LLMPlugin`.

**Change layout:** Edit the YAML frontmatter at the top of the markdown file.

**Clear LLM cache:** Delete `.cache/llm/` or use `--no-cache` flag.

**Use external plugins:** `npx tsx src/cli.ts text.md --plugins /path/to/plugins`
