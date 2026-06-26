# OpenClaw Skill: corporate-ppt-generator

## Install (local path)

```bash
# Put this folder under your OpenClaw skills directory, e.g.
# ~/.openclaw/workspace/skills/corporate-ppt-generator
```

## Test

```bash
openclaw chat
```

Try:
- "Generate a PPT in DaoCloud style using corporate-ppt-generator."
- "Use corporate-ppt-generator to render PPT from block_xml while preserving template style."

## Dependencies

- python-pptx

```bash
python3 -m pip install -r requirements.txt
```

## Local Commands

```bash
cd PPT_Builder_Skill
make demo
make extract-catalog
make package-openclaw
```

## XML Strategy

- Runtime is XML-only.
- Preferred: `render_strategy=template_first`.
- Optional: HTML blocks are allowed as fallback and converted into template content slides.
- Goal: keep template style (background/icon/font/layout) while letting models provide structured blocks.
- `make demo` uses `assets/demo_blocks.xml` and now covers toc + matrix + pie/bar/line + table + slogan.
