---
name: resume-export
description: Export resume JSON to styled HTML or PDF with theme and language options
arguments:
  - name: input
    description: Path to resume JSON file
    required: true
  - name: format
    description: "Output format: html or pdf (default: html)"
    required: false
  - name: theme
    description: "Theme: modern, classic, minimal, creative (default: modern)"
    required: false
  - name: lang
    description: "Language: en, zh, ja, fr, de, es (default: en)"
    required: false
  - name: output
    description: "Output file path (default: resume_output.html)"
    required: false
  - name: editable
    description: "Add inline editing capabilities to the HTML output"
    required: false
---

Export a resume JSON file to a styled HTML or PDF document.

## Steps

1. Validate that the `$input` file exists and is valid JSON with a `personal` field
2. Determine the output path:
   - Use `$output` if provided
   - Otherwise use `resume_output.html` (or `.pdf` if format is pdf)
3. Run the unified export script:
   ```bash
   python3 "$SKILL_DIR/scripts/export_resume.py" --format "$format" --theme "$theme" --lang "$lang" $([[ "$editable" == "true" ]] && echo "--editable") "$input" "$output_path"
   ```
4. If the user is still iterating on content, prefer `editable=true` with HTML first, review the returned JSON, then run a final non-editable export.
5. Report the generated file path to the user

## Notes

- `$SKILL_DIR` resolves to the directory containing this skill's SKILL.md
- Built-in themes: modern, classic, minimal, creative
- Custom themes: any folder under `user-themes/<name>/`, or a direct path to a custom theme directory
- Available languages: en, zh, ja, fr, de, es
- PDF export renders a clean intermediary HTML before creating the final PDF
- PDF export requires pdfkit or playwright installed
