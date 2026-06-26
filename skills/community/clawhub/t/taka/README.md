# Taka CLI

**AI-powered creative tools CLI for small businesses** — Generate images, videos, emails, and flyers from the command line.

Taka CLI provides a command-line interface to the Taka creative platform, enabling developers and AI agents to generate AI-powered marketing content: Instagram posts, promotional emails, flyers, logos, blog posts, and videos.

---

## Installation

```bash
npm install -g taka-cli
```

---

## Setup

**Authenticate with your Taka account:**

```bash
taka login
```

This uses email + OTP verification (no passwords). Credentials are saved locally and auto-refresh.

**Optional:** Custom API endpoint for staging/dev:

```bash
export TAKA_SERVER_URL=https://staging.api.taka.ai/v1
```

---

## Commands

### Authentication

| Command | Description |
|---------|-------------|
| `taka login` | Authenticate via email OTP |
| `taka logout` | Remove saved credentials |
| `taka whoami` | Show current authentication status |

### Creative Management

| Command | Description |
|---------|-------------|
| `taka create-creative --name "My Post" --type instagram` | Create a new creative project |
| `taka create-creative --name "My Post" --type instagram --prompt "..."` | Create and auto-generate an image |
| `taka list-creatives` | List all your creatives |
| `taka get-creative --id <id>` | View a specific creative |
| `taka delete-creative --id <id>` | Delete a creative |
| `taka rename-creative --creative-id <id> --name "New Name"` | Rename a creative |
| `taka list-images --creative-id <id>` | List generated images for a creative |

### Content Generation

| Command | Description |
|---------|-------------|
| `taka generate-image --prompt "..."` | Generate an image (Google Gemini) |
| `taka generate-video --prompt "..."` | Generate a video (Fal AI) |
| `taka generate-flyer-image --prompt "..."` | Generate a hero image for a flyer |
| `taka generate-email-image --section-id "..." --prompt "..."` | Generate an image for an email section |

### Content Building

| Command | Description |
|---------|-------------|
| `taka build-email --creative-id <id> --subject "..." ...` | Build complete email structure |
| `taka build-flyer --creative-id <id> --template-id promo ...` | Build flyer structure |
| `taka update-content --creative-id <id> --fields '{...}'` | Update creative content fields |
| `taka get-brand-images` | Get brand kit images |

---

## Quick Start

```bash
# 1. Install
npm install -g taka-cli

# 2. Authenticate
taka login

# 3. Create an Instagram post with AI-generated image
taka create-creative --name "Summer Sale" --type instagram --prompt "vibrant summer sale banner"

# 4. Generate a video
taka generate-video --prompt "waves crashing on beach" --aspect-ratio 9:16

# 5. List your creatives
taka list-creatives
```

---

## Features for AI Agents

- All output is JSON for easy parsing
- Auto-refreshing authentication (no manual token management)
- Supports all creative types: instagram, email, flyer, logo, blog
- Image generation with reference images and aspect ratio control
- Video generation with duration and aspect ratio options
- Full email and flyer building with templates

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TAKA_SERVER_URL` | No | `https://api.taka.ai/v1` | Custom API endpoint |

---

## Documentation

- **[SKILL.md](./SKILL.md)** — Complete skill reference with all commands, options, and workflows
- **[HOW_TO_RUN.md](./HOW_TO_RUN.md)** — Installation and setup guide
- **[examples/](./examples/)** — Ready-to-use example scripts

---

## Links

- **Website:** [taka.ai](https://taka.ai)
