# url2md

**url2md** is an agent **Skill** which converts web pages to clean, readable **Markdown** using a small Python script. Handy for documentation, archiving articles, batch exports, or any workflow where you want HTML turned into `.md` without pulling in third-party packages. **Git repository:** [url2md](https://github.com/rwonly/url2md). Contributions are welcome—open an issue or pull request for bug reports, ideas, or improvements. 

## Requirements

- **Python 3** (uses only the standard library: `urllib`, `html.parser`)

## Quick start

**Single URL** (prints Markdown to stdout):

```bash
python3 scripts/url2md.py https://example.com/article
```

**Save to a file:**

```bash
python3 scripts/url2md.py https://example.com/article -o article.md
```

**Batch conversion** — put one URL per line in a text file, then write each page into a directory:

```bash
python3 scripts/url2md.py -f urls.txt -d ./markdown_files/
```

## Features

- **No dependencies** beyond the Python standard library
- **Reader-style scope** — removes script/style/noscript/template, then prefers `<article>` or `<main>` (otherwise the full `<body>`) so Markdown resembles “main article” extraction
- **Title extraction** — prefers Open Graph / Twitter card title when present, else `<title>`; optional leading `#` heading
- **YAML Frontmatter** — extracts structured metadata (title, author, published, description, category, source URL) from `<meta>` tags and Schema.org JSON-LD for knowledge-base workflows
- **Template system** — customize output format with variables like `{{title}}`, `{{content}}`, `{{author}}`, `{{published}}`, `{{date}}`, etc.
- **Link resolution** — relative URLs are turned into absolute ones
- **Basic formatting** — headings, paragraphs, lists, links, images, fenced code with optional language, GFM-style tables, bold/italic
- **Noise removal** — skips nav, aside, footer, forms, and similar chrome within the chosen fragment

## CLI reference


| Option            | Description                                                    |
| ----------------- | -------------------------------------------------------------- |
| `url`             | Single URL to convert                                          |
| `-o`, `--output`  | Output file (default: stdout)                                  |
| `-f`, `--file`    | File containing URLs (one per line)                            |
| `-d`, `--dir`     | Output directory for batch mode                                |
| `--no-title`      | Do not add the page title as H1                                |
| `--full-page`     | Use full `<body>` instead of preferring `<article>` / `<main>` |
| `--timeout`       | Request timeout in seconds (default: 30)                       |
| `--frontmatter`   | Add YAML frontmatter with extracted metadata                   |
| `-t`, `--template`| Path to a template file for customizing output                 |
| `--filename-template` | Batch mode filename pattern (e.g. `{{date}}-{{title}}.md`) |
| `--download-images` | Download remote images to a local folder (relative to the output file, e.g. `../assets`) |
| `-v`, `--version` | Show version                                                   |


**More examples:**

```bash
python3 scripts/url2md.py https://docs.python.org/3
python3 scripts/url2md.py https://docs.python.org/3 -o python-docs.md
python3 scripts/url2md.py -f urls.txt -d ./output/ --timeout 60
python3 scripts/url2md.py https://example.com --no-title
python3 scripts/url2md.py https://example.com/deep-page --full-page -o full.md

# YAML frontmatter output (great for Obsidian / PKM workflows)
python3 scripts/url2md.py https://example.com/article --frontmatter -o article.md

# Custom template
python3 scripts/url2md.py https://example.com/article -t article.tpl -o article.md

# Batch with smart filenames
python3 scripts/url2md.py -f urls.txt -d ./output/ --filename-template "{{date}}-{{title}}.md"
python3 scripts/url2md.py -f urls.txt -d ./output/ --filename-template "{{index}}-{{title}}.md"

# Download images locally (relative to the output Markdown file)
python3 scripts/url2md.py https://example.com/article -o article.md --download-images assets
python3 scripts/url2md.py -f urls.txt -d ./output/ --download-images assets
```

### Template example

Create `article.tpl`:

```markdown
---
title: "{{title}}"
author: {{author}}
published: {{published}}
source: "{{source}}"
clipped: {{date}}
---

# {{title}}

> {{description}}

{{content}}

---
Original: [{{source}}]({{url}})
```

Available variables: `{{title}}`, `{{content}}`, `{{url}}`, `{{source}}`, `{{author}}`, `{{published}}`, `{{description}}`, `{{category}}`, `{{site_name}}`, `{{date}}`, `{{datetime}}`.

**Filename template variables** (batch mode only): `{{title}}`, `{{date}}`, `{{datetime}}`, `{{author}}`, `{{published}}`, `{{site_name}}`, `{{url}}`, `{{index}}`.

## When to use it

- Turn documentation pages into Markdown for local reference
- Archive articles as plain text files
- Batch a list of URLs into separate files
- Build a knowledge base with structured metadata (frontmatter / templates)
- Prefer a script when interactive browser or fetch tools are not the right fit

## Limitations

- Only **static HTML** is converted; **JavaScript is not executed**
- Complex layouts (multi-column, heavy CSS) may not map cleanly to Markdown
- **Login or paywalled** pages need your own auth or cookies; the script does not log you in
- **Rate limits** or blocking by the remote site still apply to repeated requests

## License

[MIT-0](LICENSE) (MIT No Attribution).