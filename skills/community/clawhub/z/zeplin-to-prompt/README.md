# zeplintopromptskill

Export a Zeplin screen into a local, prompt-ready package with previewable HTML and copyable JSON for AI-driven UI implementation.

## Install

Install dependencies before the first run:

```bash
npm install
```

If dependencies are missing, the script may fail with `ERR_MODULE_NOT_FOUND`.

## Export a Single Screen

```bash
ZEPLIN_TOKEN='your-token' node export_screen.mjs 'https://app.zeplin.io/project/<projectId>/screen/<screenId>' --no-open --quiet
```

Use a fixed output directory for repeated testing:

```bash
ZEPLIN_TOKEN='your-token' node export_screen.mjs 'https://app.zeplin.io/project/<projectId>/screen/<screenId>' --workdir ./build/test-attributedstring --no-open --quiet
```

Optional flags:

- `--workdir <DIR>`: set the export directory
- `--no-open`: do not auto-open Finder or the generated HTML
- `--quiet`: reduce logs
- `--verbose`: print detailed logs
- `--platform <key>`: load color and font mapping context; text style parsing still works without it

## Output

The export directory usually contains:

- `raw.json`: the original Zeplin response
- `layers_tree.json`: the minified structured layer tree
- `layers_tree.html`: visual preview and copy entry point
- `assets/`: downloaded local assets

When a Zeplin text layer includes multiple `textStyles` entries with `range` metadata, copied JSON includes multi-run text information. A run may contain some of these fields:

- `text`
- `color`
- `colorHex`
- `colorName`
- `fontSize`
- `fontWeight`
- `fontFamily`
- `fontName`

## Verify

1. Run the export command
2. Open the generated `layers_tree.html`
3. Right-click the target text layer and copy its JSON
4. Check whether the result contains multi-run text information

If it does not, check these first:

- You are opening the latest exported `layers_tree.html`
- The corresponding text layer in `raw.json` really contains multiple `textStyles[].range` entries
