---
name: velora-chat
description: |
  Chat with AI companions on Velora (velora.cloudm8.net). Use for: (1) Testing Velora app functionality, 
  (2) Interacting with AI companions, (3) Generating companion images, (4) Quality assurance testing of the platform.
  Requires Playwright and Chromium for browser automation.
---

# Velora Chat Skill

Automated testing and interaction with Velora AI companions (velora.cloudm8.net).

## Prerequisites

Before using this skill, ensure:

1. **Node.js installed** (v18+)
2. **Playwright installed**: 
   ```bash
   npm install playwright
   npx playwright install chromium
   ```
3. **Valid Velora account credentials**

## Credentials Setup

### Required Environment Variables

Create a `.env` file or set these variables:

```bash
# Velora Account (REQUIRED)
VELORA_EMAIL=your-email@domain.com
VELORA_PASSWORD=your-password
```

### Required Credentials

Create a `.env` file or set these environment variables:

```bash
VELORA_EMAIL=your-email@domain.com
VELORA_PASSWORD=your-password
```

⚠️ **Note**: You must provide your own Velora account credentials. The skill does not include default credentials for security reasons.

## Quick Start

### Option 1: Using the Script (CLI)

```bash
# Basic chat
node scripts/velora-chat.js "email@domain.com" "password" "Lilith" "Hey, how are you?"

# With image generation request
node scripts/velora-chat.js "email@domain.com" "password" "Rin" "Send me your best photo!"
```

**Usage:**
```bash
node scripts/velora-chat.js <email> <password> <companion> <message>
```

### Option 2: Direct in OpenClaw

The skill provides instructions for browser automation directly in conversations. Simply request:

- "Chat with [Companion Name]"
- "Test [Companion Name]'s image generation"
- "Generate [Companion Name]'s image"

## Companion List

Available companions (28 total):

| Name | Type | 
|------|------|
| Rin | Tsundere |
| Lilith | Vampire/Succubus |
| Freya | Cozy warmth |
| Yuki | Snow princess |
| Miko | Sacred sin |
| Amara | Radiant temptress |
| Aoi | Sporty & flirty |
| And 21 more... |

See [references/companions.md](references/companions.md) for full list.

## API Reference

### Login Flow

```javascript
const { chromium } = require('playwright');

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

await page.goto('https://velora.cloudm8.net/login');
await page.fill('input[type="email"]', process.env.VELORA_EMAIL);
await page.fill('input[type="password"]', process.env.VELORA_PASSWORD);
await page.click('button:has-text("Sign In")');
await page.waitForURL('**/chat**', { timeout: 20000 });
```

### Start Chat

```javascript
// New chat
await page.click('text=Neuer Chat');
await page.click('text=Lilith'); // Companion name
await page.waitForTimeout(5000);
```

### Send Message

```javascript
const input = await page.locator('input[type="text"], textarea').first();
await input.fill('Your message');
await input.press('Enter');
await page.waitForTimeout(15000); // Wait for AI response
```

### Get Generated Images

```javascript
const images = await page.evaluate(() => {
  const imgs = document.querySelectorAll('img');
  return Array.from(imgs).map(img => img.src);
});
// Download: curl -s -o image.jpg "IMAGE_URL"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Login fails | Verify credentials, check account exists |
| Images not loading | Wait 15-20 seconds for generation |
| Chat won't start | Ensure proper navigation to /chat URL |
| Playwright not found | Run `npm install playwright` |

## Security Notes

- ⚠️ Never commit credentials to version control
- Use environment variables, not hardcoded values
- Test accounts recommended for automation

## Testing Checklist

- [ ] Login flow works
- [ ] Companion list loads (28+ companions)
- [ ] Chat initiates properly
- [ ] Messages send successfully
- [ ] AI responses received
- [ ] Images generate correctly (512x768 / 1024x1024)
- [ ] Wallet/Gallery features (optional)