# TOC Link Generation Rule

For each `##` heading with text `[heading]`, slug = heading lowercased with spaces/non-ASCII replaced by hyphens:

    <a href="#section-[slug]" data-section="[heading]">[heading]</a>

For `###` heading, same but add `class="toc-h3"`:

    <a href="#section-[slug]" data-section="[heading]" class="toc-h3">[heading]</a>

Add `id="section-[slug]"` to the corresponding `<section>` or `<h3>` elements.

# Theme Override Injection

If `theme_overrides` is set in frontmatter, append CSS variable overrides after the theme CSS block:

    :root {
      [--primary: value if primary_color set]
      [--font-sans: value if font_family set]
    }
    [if logo set: .report-wrapper::before { content: ''; display: block; background: url([logo]) no-repeat left center; background-size: contain; height: 48px; margin-bottom: 1.5rem; }]

# Custom Template Mode

If `template:` is set in frontmatter:
1. Read the template file
2. Replace these placeholders:
   - `{{report.body}}` → all rendered section content HTML
   - `{{report.title}}` → title value
   - `{{report.author}}` → author value
   - `{{report.date}}` → date value
   - `{{report.abstract}}` → abstract value
   - `{{report.theme_css}}` → selected theme CSS + shared component CSS (assembled per Theme CSS rules above)
   - `{{report.summary_json}}` → the complete `<script type="application/json" id="report-summary">...</script>` block (including the script tags)
3. If `logo` is set in `theme_overrides`, prepend `<img src="[logo]" alt="Company logo" class="report-logo" style="height:48px;margin-bottom:1.5rem;display:block">` at the start of `{{report.body}}` content.
4. Output the result as the HTML file

**Example template:** `templates/_custom-template.example.html` — a documented starting point showing all available placeholders. Users can copy and customize it for their own branding. The leading underscore signals that this file is not loaded automatically.