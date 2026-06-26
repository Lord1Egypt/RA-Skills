---
name: taka
description: Taka creative tools CLI — generate AI images, videos, emails, and flyers for small businesses from the command line
homepage: https://taka.ai
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":[],"env":["TAKA_SERVER_URL"]}}}
---

## Install Taka CLI

```bash
npm install -g taka-cli
```

npm release: https://www.npmjs.com/package/taka-cli

---

| Property | Value |
|----------|-------|
| **name** | taka |
| **description** | AI-powered creative tools CLI for generating images, videos, emails, and flyers |
| **allowed-tools** | Bash(taka:*) |

---

## Core Workflow

The fundamental pattern for using Taka CLI:

1. **Authenticate** - Log in with your Taka account (email + OTP)
2. **Create** - Start a new creative project (Instagram post, email, flyer, etc.)
3. **Generate** - Use AI to generate images, videos, or build content
4. **Refine** - Update content fields, rename, or regenerate
5. **Review** - List and inspect your creatives

```bash
# 1. Authenticate
taka login

# 2. Create a project
taka create-creative --name "Summer Sale" --type instagram

# 3. Generate an image
taka generate-image --prompt "vibrant summer sale banner with tropical colors"

# 4. Refine
taka update-content --creative-id <id> --fields '{"caption": "Summer sale starts now!"}'

# 5. Review
taka list-creatives
taka get-creative --id <id>
```

---

## Authentication

Taka uses email OTP (one-time password) authentication. Tokens are saved locally and auto-refresh silently.

```bash
# Log in (interactive — prompts for email, then verification code)
taka login

# Check who you're logged in as
taka whoami

# Log out (removes saved credentials)
taka logout
```

**Environment Variables:**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TAKA_SERVER_URL` | No | `https://api.taka.ai/v1` | Custom API endpoint (for staging/dev) |

Credentials are saved to `~/.config/taka/config.json` with restricted permissions (owner-only read/write).

---

## Commands

### Creative Management

**Create a new creative project**
```bash
taka create-creative --name "My Post" --type instagram
taka create-creative --name "My Post" --type instagram --prompt "sunset over ocean"
```

Types: `instagram`, `email`, `logo`, `blog`, `flyer`

When `--prompt` is provided for instagram, logo, or flyer types, an image is automatically generated after creation.

**List all creatives**
```bash
taka list-creatives
```

**Get a specific creative**
```bash
taka get-creative --id <creative-id>
```

**Delete a creative**
```bash
taka delete-creative --id <creative-id>
```

**Rename a creative**
```bash
taka rename-creative --creative-id <id> --name "New Name"
```
Name is limited to 40 characters.

**List generated images for a creative**
```bash
taka list-images --creative-id <id>
```

---

### Image Generation

**Generate an image from a text prompt**
```bash
taka generate-image --prompt "a sunset over the ocean"
```

Uses Google Gemini AI to generate images.

**Options:**
- `--prompt <text>` (required) - Text description of the image
- `--aspect-ratio <ratio>` - One of: `1:1`, `3:4`, `4:3`, `9:16`, `16:9`
- `--reference-attachment-ids <ids...>` - Attachment IDs for reference images (image-to-image)
- `--reference-mode <mode>` - `inspire` (loose inspiration) or `edit` (modify in-place)
- `--creative-id <id>` - Associate the image with a creative project

**Examples:**
```bash
# Square image
taka generate-image --prompt "coffee shop logo" --aspect-ratio 1:1

# Portrait image for Instagram story
taka generate-image --prompt "motivational quote background" --aspect-ratio 9:16

# Associate with a creative
taka generate-image --prompt "product photo" --creative-id abc123
```

---

### Video Generation

**Generate a video from a text prompt**
```bash
taka generate-video --prompt "waves crashing on a beach at sunset"
```

Uses Fal AI to generate videos.

**Options:**
- `--prompt <text>` (required) - Text description of the video
- `--duration <seconds>` - `5`, `7`, or `10` (default: `7`)
- `--aspect-ratio <ratio>` - `16:9`, `9:16`, or `1:1`
- `--source-image-attachment-id <id>` - Animate an existing image (image-to-video)
- `--creative-id <id>` - Associate with a creative project

**Examples:**
```bash
# Short video for Instagram Reels
taka generate-video --prompt "coffee being poured" --duration 5 --aspect-ratio 9:16

# Longer landscape video
taka generate-video --prompt "timelapse of city skyline" --duration 10 --aspect-ratio 16:9
```

---

### Flyer Creation

**Generate a hero image for a flyer**
```bash
taka generate-flyer-image --prompt "grand opening celebration" --creative-id <id>
```
Always generates in 3:4 (portrait) aspect ratio.

**Build a flyer structure**
```bash
taka build-flyer \
  --creative-id <id> \
  --template-id promo \
  --headline "50% Off Everything" \
  --subtitle "This weekend only" \
  --tagline "Shop Now"
```

Template IDs: `promo`, `event`, `opening`, `seasonal`, `minimal`, `photo-heavy`

---

### Email Creation

**Generate an image for an email section**
```bash
taka generate-email-image \
  --section-id hero \
  --prompt "holiday email banner" \
  --creative-id <id>
```

**Options:**
- `--section-id <id>` (required) - Section ID within the email
- `--prompt <text>` (required) - Image description
- `--aspect-ratio <ratio>` - `16:9`, `4:3`, or `1:1`
- `--cell-index <n>` - Column cell index (0-based, for multi-column sections)
- `--creative-id <id>` - Associate with a creative

**Build a complete email**
```bash
taka build-email \
  --creative-id <id> \
  --subject "Welcome to Our Newsletter" \
  --preheader "Great things are coming" \
  --global-style '{"backgroundColor":"#f4f4f5","contentWidth":600,"fontFamily":"Arial","fontColor":"#333333"}' \
  --sections '[{"type":"hero","content":{"title":"Welcome!","subtitle":"We are glad you are here"}},{"type":"text","content":{"body":"Lorem ipsum..."}}]' \
  --footer '{"businessName":"My Business","showUnsubscribe":true,"showViewInBrowser":true}'
```

---

### Brand Kit

**Get brand images**
```bash
taka get-brand-images
taka get-brand-images --tags signature products
```

Available tags: `signature`, `products`, `lifestyle`, `people`

---

### Content Updates

**Update any fields on a creative**
```bash
taka update-content --creative-id <id> --fields '{"caption":"New caption","hashtags":["summer","sale"]}'
```

The `--fields` parameter accepts any valid JSON object with fields specific to the creative type.

---

## Common Workflows

### Create Instagram Post with AI Image
```bash
# Create and auto-generate in one step
taka create-creative --name "Summer Vibes" --type instagram --prompt "tropical beach sunset"
```

### Create a Complete Email Campaign
```bash
# 1. Create the project
RESULT=$(taka create-creative --name "Welcome Email" --type email)
ID=$(echo $RESULT | jq -r '.creative.id')

# 2. Build the email structure
taka build-email \
  --creative-id $ID \
  --subject "Welcome!" \
  --preheader "We are excited to have you" \
  --global-style '{"backgroundColor":"#ffffff","contentWidth":600,"fontFamily":"Arial","fontColor":"#333"}' \
  --sections '[{"type":"hero","content":{"title":"Welcome!"}},{"type":"text","content":{"body":"Thanks for joining us."}}]' \
  --footer '{"businessName":"My Biz","showUnsubscribe":true,"showViewInBrowser":true}'

# 3. Generate a hero image
taka generate-email-image --section-id hero-0 --prompt "welcoming banner" --creative-id $ID
```

### Create a Promotional Flyer
```bash
# 1. Create project
RESULT=$(taka create-creative --name "Grand Opening" --type flyer)
ID=$(echo $RESULT | jq -r '.creative.id')

# 2. Build structure
taka build-flyer --creative-id $ID --template-id opening --headline "Grand Opening" --subtitle "Join us this Saturday"

# 3. Generate hero image
taka generate-flyer-image --prompt "festive grand opening storefront" --creative-id $ID
```

---

## Output Format

All commands output JSON for easy parsing:

```bash
# Parse output with jq
CREATIVE_ID=$(taka create-creative --name "Test" --type instagram | jq -r '.creative.id')
IMAGE_URL=$(taka generate-image --prompt "test" | jq -r '.imageUrl')
```

---

## Error Handling

| Error | Solution |
|-------|----------|
| `Not authenticated. Run taka login first.` | Run `taka login` |
| `Session expired. Run taka login to re-authenticate.` | Run `taka login` (refresh token also expired) |
| `Not enough credits` | Purchase more credits or upgrade plan |
| `A video is already being generated` | Wait for current video generation to complete |
| `Creative not found` | Verify creative ID with `taka list-creatives` |

---

## Quick Reference

```bash
# Auth
taka login                                          # Log in
taka whoami                                         # Check auth status
taka logout                                         # Log out

# Creatives
taka create-creative --name "X" --type instagram    # Create
taka list-creatives                                 # List all
taka get-creative --id <id>                         # Get one
taka delete-creative --id <id>                      # Delete
taka rename-creative --creative-id <id> --name "Y"  # Rename
taka list-images --creative-id <id>                 # List images

# Generate
taka generate-image --prompt "..."                  # Image (Gemini)
taka generate-video --prompt "..."                  # Video (Fal)
taka generate-flyer-image --prompt "..."            # Flyer hero image
taka generate-email-image --section-id X --prompt "..."  # Email image

# Build
taka build-email --creative-id <id> --subject "..." --preheader "..." --global-style '{}' --sections '[]' --footer '{}'
taka build-flyer --creative-id <id> --template-id promo --headline "..." --subtitle "..."

# Content
taka update-content --creative-id <id> --fields '{}'
taka get-brand-images --tags products lifestyle

# Help
taka --help
```
