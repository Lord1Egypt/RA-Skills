---
name: md-to-feishu
description: Convert local Markdown files to Feishu (Lark) documents with automatic image uploading. Uses the feishu-docx CLI tool.
---

# Markdown to Feishu Document

Convert a local Markdown file into a Feishu document, with automatic image upload.

## User Input

The user only needs to provide a **Markdown file path**. Title is optional — if not provided, extract it automatically (see below).

## Step 1: Determine the Document Title

1. Read the Markdown file and look for the first `# heading` — use that as the title.
2. If no `# heading` exists, scan the content and generate a concise, descriptive title based on the topic.
3. If the user explicitly provides a title, use that instead.

## Step 2: Check the Runtime Environment

Try each option in order. Use the **first one that works**.

### Option A: uvx (preferred)

```bash
which uvx
```

If `uvx` is available, the run command is:

```bash
uvx feishu-docx create "<TITLE>" -f <MARKDOWN_FILE_PATH>
```

If `uvx` runs with Python < 3.11, add `--python 3.11`:

```bash
uvx --python 3.11 feishu-docx create "<TITLE>" -f <MARKDOWN_FILE_PATH>
```

### Option B: feishu-docx already installed

```bash
which feishu-docx
```

If found, check Python version:

```bash
python3 --version
```

If Python >= 3.11, the run command is:

```bash
feishu-docx create "<TITLE>" -f <MARKDOWN_FILE_PATH>
```

### Option C: Nothing available — install guidance

If neither `uvx` nor `feishu-docx` is found, tell the user:

> `feishu-docx` requires Python >= 3.11. Install with one of:
>
> ```bash
> # Recommended: install uv, then run directly without global install
> curl -LsSf https://astral.sh/uv/install.sh | sh
> uvx feishu-docx create "Title" -f file.md
>
> # Or: install globally with pip (Python >= 3.11 required)
> pip install feishu-docx
> ```
>
> Feishu credentials must be configured first:
> ```bash
> feishu-docx config set --app-id <APP_ID> --app-secret <APP_SECRET>
> ```

Then stop and wait for the user to set up the environment.

## Step 3: Pre-process Mermaid Blocks

The `feishu-docx` tool cannot handle Mermaid code blocks. Before uploading, check if the Markdown contains any ` ```mermaid ` blocks and convert them to images first.

### 3a: Scan for Mermaid blocks

Read the Markdown file and check if it contains any ` ```mermaid ` fenced code blocks. If **none are found, skip to Step 4**.

### 3b: Create a temporary copy

Copy the original Markdown file to a temp file in the same directory (so relative image paths still work):

```
<original-name>.feishu-tmp.md
```

For example: `blog_post.md` → `blog_post.feishu-tmp.md`

All subsequent modifications happen on this temp copy. The original file is never modified.

### 3c: Render Mermaid diagrams to PNG

For each ` ```mermaid ... ``` ` block in the temp file, render it to a PNG image using the mermaid.ink API:

```python
import base64, urllib.request

def render_mermaid(code: str, output_path: str):
    """Render a Mermaid diagram to PNG via mermaid.ink API."""
    encoded = base64.urlsafe_b64encode(code.encode()).decode()
    url = f"https://mermaid.ink/img/{encoded}?bgColor=white"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=30)
    with open(output_path, "wb") as f:
        f.write(resp.read())
```

**Important:** The `User-Agent` header is required — mermaid.ink returns 403 without it.

Save rendered images to the same directory as the Markdown file, using descriptive filenames based on diagram content:

- GOOD: `mermaid-architecture-overview.png`, `mermaid-data-flow.png`
- BAD: `mermaid-1.png`, `diagram.png`

### 3d: Replace Mermaid blocks with image references

In the temp copy, replace each ` ```mermaid ... ``` ` block with a Markdown image reference:

```markdown
![Architecture overview](mermaid-architecture-overview.png)
```

Use relative paths from the temp file to the rendered images.

### 3e: Use the temp file for upload

From this point, the **temp file** becomes the `<MARKDOWN_FILE_PATH>` used in Step 4.

## Step 4: Run the Command

- **Run from the directory where the Markdown file lives** (or where its relative image paths resolve correctly), so that local image references work.
- The tool will:
  - Convert Markdown blocks to Feishu format
  - Automatically upload local images referenced in the Markdown
  - Wait ~10s for block consistency before uploading images

## Step 5: Clean Up

If a temp file was created in Step 3:
- Delete the temp Markdown file (`*.feishu-tmp.md`)
- Delete all rendered Mermaid PNG files created in Step 3c (they were only needed for the upload)

## Step 6: Report Result

Show the user:
- Number of blocks converted and images uploaded
- The created document ID
- Success or failure status

If it fails with authentication errors, remind the user to configure credentials:
```bash
feishu-docx config set --app-id <APP_ID> --app-secret <APP_SECRET>
```
