# VibeSKU CLI Command Reference

## Table of Contents

- [auth](#auth)
- [init](#init)
- [config](#config)
- [templates](#templates)
- [generate](#generate)
- [refine](#refine)
- [status](#status)
- [jobs](#jobs)
- [export](#export)
- [batch](#batch)
- [credits](#credits)

---

## auth

Manage authentication.

### auth login

Sign in via browser-based device authorization flow.

```bash
vibesku auth login                # Open browser and sign in
vibesku auth login --no-browser   # Print URL instead of opening browser
```

Tokens stored at `~/.vibesku/config.json` (mode 0600), last 90 days with automatic refresh. Non-interactive environments imply `--no-browser`.

### auth logout

Sign out and clear stored credentials.

```bash
vibesku auth logout
```

### auth status

Show current auth status (method, user info, token expiry).

```bash
vibesku auth status
```

### auth refresh

Manually refresh CLI token.

```bash
vibesku auth refresh
```

---

## init

Initialize CLI with an API key. Verifies the key against the server.

```bash
vibesku init vsk_abc123def456
vibesku init vsk_abc123def456 --base-url http://localhost:3005
```

---

## config

Manage CLI configuration.

```bash
vibesku config set-key vsk_your_key   # Set API key
vibesku config set-url http://localhost:3005  # Set custom API URL
vibesku config show                   # Show current configuration
vibesku config reset                  # Reset to defaults
```

Config stored at `~/.vibesku/config.json`.

---

## templates

List and inspect available templates.

### templates (list)

```bash
vibesku templates          # Table format
vibesku templates --json   # JSON format
```

Shows template ID, name, version, output type, and options count.

### templates info

Show detailed template spec: asset requirements, brief fields, options with defaults/allowed values, example CLI command.

```bash
vibesku templates info ecom-hero          # Human-readable
vibesku templates info kv-image-set --json # JSON
vibesku templates info exploded-view       # Exploded infographic template
```

Output includes:
- Name, description, version, output type
- Analysis support indicator
- Asset requirements (min/max for product images and logo)
- Brief fields (name, type, required)
- Options (name, type, required, default, enum values with descriptions)
- Example `vibesku generate` command

---

## generate

Generate content from a template. Handles asset upload automatically.

```bash
# Basic
vibesku generate -t ecom-hero -n "Product Name"

# With images and logo
vibesku generate -t ecom-hero \
  -n "Wireless Headphones" \
  -d "Premium noise-cancelling headphones" \
  -b "AudioTech" \
  -i photo1.jpg photo2.jpg \
  -l logo.png

# With template options
vibesku generate -t kv-image-set \
  -n "Smart Watch" \
  -i watch.png \
  -o '{"style":"tech-future","aspectRatio":"3:4"}'

# Exploded technical infographic
vibesku generate -t exploded-view \
  -n "Ceramic Aroma Diffuser" \
  -i diffuser.jpg \
  -o '{"style":"premium-technical","layerDensity":"balanced","backgroundMode":"product-matched-scene","labelPlacement":"balanced-callout","aspectRatio":"3:4"}'

# Text listing
vibesku generate -t listing \
  -n "Organic Green Tea" \
  -d "Hand-picked premium tea leaves" \
  -o '{"templateName":"AMAZON_LISTING","language":"English"}'
```

| Flag | Description |
|------|-------------|
| `-t, --template <id>` | Template ID (required) |
| `-n, --product-name <name>` | Product name |
| `-d, --product-details <text>` | Product description |
| `-b, --brand <name>` | Brand name |
| `-i, --images <paths...>` | Product image files (auto-uploaded) |
| `-l, --logo <path>` | Logo file (auto-uploaded) |
| `-o, --options <json>` | Template-specific options as JSON |
| `--json` | Output as JSON |

On success, displays remaining credit balance.

---

## refine

Refine an existing output with new instructions. Consumes credits. Requires a **full output UUID** — use `vibesku status <job-id> --json` to get complete IDs (the table view truncates them).

```bash
vibesku refine beb47f34-fdf8-49c4-9b9f-96bd367ed145 -p "make the background brighter"
vibesku refine beb47f34-fdf8-49c4-9b9f-96bd367ed145 -p "change to landscape" --aspect-ratio 16:9 --image-size 4K
vibesku refine beb47f34-fdf8-49c4-9b9f-96bd367ed145 -p "remove watermark" --yes    # Skip confirmation
vibesku refine beb47f34-fdf8-49c4-9b9f-96bd367ed145 -p "increase contrast" --json
```

| Flag | Description |
|------|-------------|
| `-p, --prompt <text>` | Edit instruction (required) |
| `--aspect-ratio <ratio>` | Override aspect ratio (e.g. `16:9`, `3:2`) |
| `--image-size <size>` | Image size: `1K`, `2K`, or `4K` |
| `-y, --yes` | Skip credit confirmation prompt |
| `--json` | Output as JSON |

On success, displays run ID, job ID, and remaining credits.

---

## status

Check job status, active runs, and detailed output list.

```bash
vibesku status abc123-def456              # One-time check
vibesku status abc123-def456 --watch      # Poll every 5s until complete
vibesku status abc123-def456 --json       # JSON format
```

Output table shows each output's ID, type, size, aspect ratio, creation time, and parent lineage (for refined outputs):

```
Outputs:
ID                                      Type    Size    Ratio   Created             Parent
──────────────────────────────────────────────────────────────────────────────────────────────────
beb47f34-fdf8-49c4-9b9f-96bd367ed145    IMAGE   2K      3:2     2024-02-12 10:30    —
c1a2b3d4-e5f6-7890-abcd-ef1234567890    IMAGE   2K      3:2     2024-02-12 10:35    beb47f34… (refined)
d4e5f6a7-b8c9-0123-4567-890abcdef123    TEXT    —       —       2024-02-12 10:32    —
```

---

## jobs

List jobs with pagination.

```bash
vibesku jobs                              # Default: page 1, 20 items
vibesku jobs -p 2 -s 50                   # Page 2, 50 items
vibesku jobs -t ecom-hero                 # Filter by template
vibesku jobs --json                       # JSON format
```

---

## export

Download job outputs (images and text).

```bash
vibesku export abc123-def456                           # Current directory
vibesku export abc123-def456 -o ./my-outputs           # Custom directory
vibesku export abc123-def456 --output-id specific-id   # Specific output
vibesku export abc123-def456 --json                    # Metadata only
```

Files saved as `{output-id}.{png|jpg|webp}` for images, `{output-id}.txt` for text.

---

## batch

Run batch generation from a JSON file.

```bash
vibesku batch jobs.json            # Submit all jobs
vibesku batch jobs.json --dry-run  # Validate file only
vibesku batch jobs.json --json     # Results as JSON
```

### Batch file format

```json
[
  {
    "templateId": "ecom-hero",
    "brief": {
      "productName": "Wireless Headphones",
      "productDetails": "Premium noise-cancelling",
      "brandName": "AudioTech"
    },
    "assetIds": {
      "productImages": ["asset-id-1", "asset-id-2"],
      "logo": "asset-id-3"
    },
    "options": {
      "style": "premium",
      "aspectRatio": "1:1"
    }
  }
]
```

`assetIds` reference pre-uploaded asset IDs. Use `vibesku generate -i` for automatic upload, or upload first via the API.

---

## credits

Manage credits and balance. Running `vibesku credits` with no subcommand defaults to `show`.

### credits show

```bash
vibesku credits              # Human-readable (default)
vibesku credits show         # Explicit
vibesku credits show --json  # JSON
```

Displays low-balance warning when total credits < 10.

### credits buy

Purchase credits or subscribe. Interactive TTY shows numbered menu; non-interactive uses flags.

```bash
vibesku credits buy                                          # Interactive menu
vibesku credits buy --tier starter-pack --mode one_time      # Non-interactive
vibesku credits buy --tier pro --mode subscription --cycle yearly
vibesku credits buy --no-browser                             # Print URL only
```

| Flag | Description |
|------|-------------|
| `--tier <id>` | Tier/product ID |
| `--mode <mode>` | `subscription` or `one_time` |
| `--cycle <cycle>` | `monthly` or `yearly` (subscriptions only) |
| `--no-browser` | Print checkout URL |
| `--json` | JSON output |

### credits redeem

Redeem a credit code.

```bash
vibesku credits redeem VSK-ABCD-EFGH-JK
vibesku credits redeem VSK-ABCD-EFGH-JK --json
```
