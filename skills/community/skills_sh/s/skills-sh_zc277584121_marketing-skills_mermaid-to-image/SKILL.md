---
name: mermaid-to-image
description: Convert Mermaid code blocks in Markdown files to PNG images using the mermaid.ink API.
---

# Skill: Mermaid to Image

Convert ` ```mermaid ` code blocks in Markdown (or other text) files into PNG images, and replace the code blocks with image references. Useful for platforms that don't render Mermaid natively (GitHub Pages/Jekyll, Dev.to, etc.).

---

## When to Use

- The user asks to convert Mermaid diagrams in a file to images
- The user wants to render specific Mermaid code blocks as PNG
- A publishing workflow requires static images instead of Mermaid code blocks

---

## Workflow

### Step 1: Identify target files

The user may specify:
- A single file: `convert mermaid blocks in docs/architecture.md`
- Multiple files: `convert mermaid in all files under docs/`
- A specific code block: `convert the second mermaid block in README.md`

Scan the target file(s) for ` ```mermaid ` code blocks. Report how many blocks were found and in which files before proceeding.

### Step 2: Determine the image output directory

Check the project structure to find where images are typically stored:

```bash
# Look for common image directories
ls -d images/ img/ assets/ assets/images/ static/images/ docs/images/ 2>/dev/null
```

**If a clear image directory exists** (e.g., `images/`, `assets/images/`), use it. Create a subdirectory by topic if appropriate (e.g., `images/<topic>/`).

**If no image directory is obvious or multiple candidates exist**, ask the user:

```
Where should I save the rendered Mermaid images?

1. images/ (create new)
2. assets/images/
3. docs/figures/
4. Custom — enter a path
```

### Step 3: Render each diagram to PNG

Use the [mermaid.ink](https://mermaid.ink) API to render diagrams. Run this Python snippet for each block:

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

#### Naming convention

Use descriptive filenames based on the diagram content, not generic names:

- GOOD: `architecture-overview.png`, `data-flow.png`, `heartbeat-sequence.png`
- BAD: `mermaid-1.png`, `diagram.png`, `image1.png`

### Step 4: Replace code blocks with image references

Replace each ` ```mermaid ... ``` ` block with a Markdown image reference using a **relative path** from the file to the image:

```markdown
![Architecture overview](images/topic/architecture-overview.png)
```

If the project uses absolute URLs (e.g., GitHub Pages), use those instead:

```markdown
![Architecture overview](https://example.github.io/images/topic/architecture-overview.png)
```

Choose the link style that matches the project's existing image references. If unsure, use relative paths.

### Step 5: Report results

After processing, summarize:
- How many diagrams were converted
- Where the images were saved
- Which files were modified

---

## Edge Cases

- **Large diagrams**: mermaid.ink may time out on very complex diagrams. If a render fails, report the error and suggest the user simplify the diagram or try an alternative renderer.
- **Multiple blocks in one file**: process all blocks in order, give each a unique descriptive filename.
- **Already-rendered blocks**: if a mermaid block already has a corresponding image (commented out or adjacent), skip it or ask the user.
- **Non-Markdown files**: the same approach works for any text file containing mermaid code blocks (e.g., `.rst`, `.txt`).
