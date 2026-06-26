---
name: ppt-generator
description: "Generate PowerPoint (.pptx) files from Markdown input. Use when user requests a PPT to be created or exported."
---

# PPT Generator Skill

Automatically generate PowerPoint presentations from structured Markdown.

## When to Use

✅ **USE this skill when:**

- "Create a PPT for me"
- "Export this as a PowerPoint"
- "Generate a .pptx file"
- User provides content and expects a downloadable PPT

## Implementation

This skill uses a Python script (`generate_ppt.py`) that leverages the `python-pptx` library to parse Markdown and create slides.

### Markdown Format

The input Markdown should use `---` to separate slides.

```
# Slide 1 Title

- Bullet point 1
- Bullet point 2

---

## Slide 2 Title

This is a paragraph.
```

## Commands

The skill will call:

```bash
python generate_ppt.py --input <input_md_file> --output <output_pptx_file>
```

## Dependencies

- `python-pptx` (must be installed in the environment)
- Python 3.7+

## Notes

- This is a custom skill and must be installed manually.
- The `generate_ppt.py` script must be in the same directory.