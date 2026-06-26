---
name: site-cloner
description: Clone any live website into a self-contained, dependency-free HTML file with all content, styles, fonts, and images extracted and preserved. Use when asked to clone, copy, replicate, or mirror a website; or when the user says "clone this site", "copy this site", "make me a copy of this URL", or "recreate this website". Handles React/Vue/Angular SPAs by extracting from the JS bundle. Optionally deploys to a VPS via nginx and pushes to a private GitHub repo.
---

# Site Cloner

Clones any live website into a clean, standalone HTML file with all assets.

## Workflow

### 1. Fetch the page
```powershell
$html = (Invoke-WebRequest -Uri "<URL>" -UseBasicParsing).Content
```

Check `<script src="...">` and `<link rel="stylesheet" href="...">` tags.

### 2. Detect site type
- **Static HTML**: Extract content directly from `$html`
- **React/Vue/Angular SPA**: The `<body>` has only `<div id="root">` — extract from the JS bundle instead (see references/spa-extraction.md)

### 3. Extract content from JS bundle (SPA)

Download the JS bundle, then mine for:
- **UI copy**: `[regex]::Matches($js, '"([A-Z][^"]{10,400})"')` — filter for strings with spaces, no code keywords
- **Image paths**: `[regex]::Matches($js, '"(/[^"]+\.(jpg|jpeg|png|webp|svg|avif))"')`
- **Nav links**: search for `href:"#` patterns
- **Theme/colors**: download the CSS bundle, extract `--[a-z-]+:` custom properties
- **Fonts**: look for `family=` in the CSS `@import` URL

### 4. Download all images
```powershell
$images = @("image1.png", "image2.jpg")  # from step 3
$dir = "C:\Users\MJ\.openclaw\workspace\<site-name>-clone\images"
New-Item -ItemType Directory -Force -Path $dir | Out-Null
foreach ($img in $images) {
    Invoke-WebRequest -Uri "<BASE_URL>/images/$img" -OutFile "$dir\$img" -UseBasicParsing -TimeoutSec 25
}
```

### 5. Build the HTML file

Use `write` tool to create `index.html`. Follow the template in references/html-template.md.

**Rules:**
- Single file, zero npm/build dependencies
- Inline all CSS in `<style>` tags using extracted custom properties
- Load fonts via Google Fonts `<link>` tag
- Reference images as `/images/filename.ext`
- Add scroll animations via IntersectionObserver
- Add navbar scroll behavior, carousel logic, form toast — all vanilla JS

### 6. Deploy to VPS (if requested)

```powershell
# Upload files
ssh -i C:\Users\MJ\.ssh\vps_key root@187.124.92.226 "mkdir -p /var/www/<name> && chmod 755 /var/www/<name>"
scp -i C:\Users\MJ\.ssh\vps_key index.html root@187.124.92.226:/var/www/<name>/
scp -i C:\Users\MJ\.ssh\vps_key -r images root@187.124.92.226:/var/www/<name>/
ssh -i C:\Users\MJ\.ssh\vps_key root@187.124.92.226 "chmod 755 /var/www/<name>/images"

# Write nginx config locally, scp it (never write via heredoc — variable escaping breaks)
$config = "server { listen <PORT>; server_name _; root /var/www/<name>; index index.html; location / { try_files `$uri `$uri/ =404; } }"
# Write full multiline config to file first, then scp
$config | Out-File ".\nginx-<name>.conf" -Encoding ASCII -NoNewline
scp -i C:\Users\MJ\.ssh\vps_key ".\nginx-<name>.conf" root@187.124.92.226:/etc/nginx/sites-available/<name>
ssh -i C:\Users\MJ\.ssh\vps_key root@187.124.92.226 "ln -sf /etc/nginx/sites-available/<name> /etc/nginx/sites-enabled/<name> && nginx -t && systemctl reload nginx"
```

**Port allocation** (MJW VPS — 187.124.92.226):
- 8080 → arnicapatch
- 8081 → taylored-touch
- 8082 → twisted-roots
- 8083+ → next available

**Critical nginx gotcha:** Always write the config to a local file and `scp` it. Never use heredoc or `printf` over SSH — `$uri` gets mangled.

### 7. Push to GitHub (if requested)

```powershell
cd "<clone-dir>"
git init
git add index.html images/
git commit -m "Initial clone of <URL>"
gh repo create <name>-clone --private --source=. --remote=origin --push
```

If repo already exists: `git remote set-url origin git@github.com:michelle447/<name>-clone.git && git push`

## Output

Always report:
- ✅ Local path
- ✅ GitHub URL (if pushed)
- ✅ VPS URL (if deployed)
- Image count downloaded
