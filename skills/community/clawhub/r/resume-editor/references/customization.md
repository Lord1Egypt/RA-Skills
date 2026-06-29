# Customization

## Tuning an Existing Theme

If the user likes one of the built-in themes but wants adjustments, scaffold a reusable custom theme:

```bash
python3 scripts/create_theme.py my-theme --base modern
```

This creates:

- `user-themes/my-theme/template.html`
- `user-themes/my-theme/style.css`

Then:

1. Edit `style.css` for colors, spacing, fonts, borders, print layout, and emphasis.
2. Edit `template.html` only if the outer HTML wrapper needs to change.
3. Export with the custom theme:
   ```bash
   python3 scripts/export_resume.py --theme my-theme --format html resume.json output.html
   ```

For one-off experimentation, you can also pass a direct path to a custom theme directory:

```bash
python3 scripts/export_resume.py --theme /absolute/path/to/my-theme --format pdf resume.json output.pdf
```

## Creating a Theme From Scratch

Create a directory with:

- `style.css` (required)
- `template.html` (optional; falls back to the default HTML wrapper when omitted)

Recommended location:

- `user-themes/<theme-name>/`

Example:

```text
user-themes/editorial/
├── style.css
└── template.html
```

Use it with:

```bash
python3 scripts/export_resume.py --theme editorial --format html resume.json output.html
```

### Enabling the portrait photo

`personal.photo` is hidden by default in every built-in theme. To display it in a custom theme, add a `.resume-photo` rule to your `style.css`:

```css
.resume-photo {
    display: block;
    width: 96px;
    height: 96px;
    object-fit: cover;
    border-radius: 50%;   /* or 4px for a square headshot */
    margin: 0 auto 12px;
}
```

Only include a photo when the target market expects one — many regions (US, UK, Canada, Australia, much of the EU) penalize or reject photo resumes for anti-discrimination reasons.

## Restyling the Edit Toolbar

The editable HTML (`--editable`) ships with its own self-contained edit-mode UI. Custom themes should generally leave it alone, but you can restyle it from your theme's CSS via these classes/IDs:

- `#resume-edit-btn` — the floating pencil button (top-right corner).
- `#resume-edit-toolbar` — the top toolbar shown while editing.
- `#resume-edit-toolbar .toolbar-btn-format` — the B / I / U / color buttons.
- `#resume-edit-toolbar .toolbar-btn-save` — the Save button (writes to disk via the local sync server).
- `#resume-edit-toolbar .toolbar-btn-copy` — the Copy JSON button (fallback).
- `#resume-edit-toolbar .toolbar-btn-cancel` — the Done button.
- `#resume-color-popover` — the color swatch/hex dropdown.
- `#resume-edit-toast` — transient confirmation toast.

The toolbar UI is hidden during `@media print`, so it never appears in PDF output.

## Modifying Resume Data Structure

To add custom fields:

1. Update the JSON schema in your resume data file
2. Add HTML generation logic in `scripts/generate_html.py` for the new section
3. Add CSS styles for the custom section in your theme's CSS file

## Adding New Languages

1. Register the language code in `scripts/resume_utils.py`
2. Add translations to `LOCALIZED_TEXT` in `scripts/resume_utils.py`
3. Test:
   ```bash
   python3 scripts/export_resume.py --theme modern --lang your-lang --format html resume.json output.html
   ```

## Exporting to Other Formats

- **Markdown**: `pandoc resume.html -o resume.md`
- **Word**: `pandoc resume.html -o resume.docx`
- **Plain Text**: `html2text resume.html > resume.txt`
