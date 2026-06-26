# Uploaded Scratch Files

Use this reference only when the user provides or uploads a Scratch project
file and you need to inspect it.

## Supported files
- `.sb3`
- `.sprite3`
- raw Scratch `project.json`
- raw Scratch `sprite.json`

## Handling
- Use the uploaded file path directly when one is available in the workspace or
  thread context.
- If you need to inspect the project structure, run:

```bash
python3 <SKILL_DIR>/scripts/extract.py "<FILE>"
```

- For `.sb3`, `.sprite3`, `project.json`, or `sprite.json` inputs, this writes one combined JSON file at
  `/tmp/scratchcode/<file md5>/blocks.json`.
- Wait for extraction to finish, then use the printed file path as the source
  of truth.
- After extraction, do not go back to the original `.sb3` or `.sprite3` file
  unless you need to rerun the extractor.
- Combine the extracted content with the user's question, if there is one.
- Reason about the project in `scratch-json`, following the format in
  `SKILL.md`.
- `scripts/render_ascii.py` expects `scratch-json`, not raw Scratch
  `project.json` / `sprite.json`.
- Use `scripts/render_ascii.py` only if you want to show the Scratch code back
  to the user in a more visual block layout.
