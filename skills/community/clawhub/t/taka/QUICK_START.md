# Taka CLI - Quick Start Guide

## Install

```bash
npm install -g taka-cli
```

## Authenticate

```bash
taka login
```

Enter your email, then the verification code sent to your inbox.

## Generate Your First Image

```bash
taka generate-image --prompt "a cozy coffee shop with warm lighting"
```

## Create an Instagram Post

```bash
# Create + auto-generate image in one command
taka create-creative --name "Morning Coffee" --type instagram --prompt "latte art in a ceramic cup"
```

## Create a Promotional Flyer

```bash
# 1. Create the project
taka create-creative --name "Grand Opening" --type flyer

# 2. Build the structure (use the ID from step 1)
taka build-flyer \
  --creative-id <id> \
  --template-id opening \
  --headline "Grand Opening" \
  --subtitle "Join us this Saturday"

# 3. Generate a hero image
taka generate-flyer-image --prompt "festive storefront" --creative-id <id>
```

## Generate a Video

```bash
taka generate-video --prompt "waves crashing on a beach" --duration 7 --aspect-ratio 9:16
```

## Build an Email

```bash
taka build-email \
  --creative-id <id> \
  --subject "Welcome!" \
  --preheader "Great things ahead" \
  --global-style '{"backgroundColor":"#ffffff","contentWidth":600,"fontFamily":"Arial","fontColor":"#333"}' \
  --sections '[{"type":"hero","content":{"title":"Welcome!"}},{"type":"text","content":{"body":"Thanks for joining."}}]' \
  --footer '{"businessName":"My Business","showUnsubscribe":true,"showViewInBrowser":true}'
```

## View Your Creatives

```bash
taka list-creatives
taka get-creative --id <id>
```

## Get Help

```bash
taka --help
```

## Next Steps

- Read [SKILL.md](./SKILL.md) for full command reference
- See [examples/](./examples/) for ready-to-use scripts
