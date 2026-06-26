# Getting Started with Mistral OCR

This guide walks you through obtaining a Mistral API key and setting it up for use with this skill.

## Step 1: Create a Mistral Account

1. Go to [console.mistral.ai](https://console.mistral.ai/)
2. Click **Sign Up** (or **Sign In** if you have an account)
3. You can sign up with:
   - Email and password
   - Google account
   - GitHub account

## Step 2: Add Billing (Required for API Access)

Mistral requires a payment method to use the API:

1. Go to **Billing** in the left sidebar
2. Click **Add Payment Method**
3. Enter your credit card details
4. Add credits to your account (minimum ~$5)

> **Note:** Check current pricing at [mistral.ai/pricing](https://mistral.ai/pricing/)

## Step 3: Create an API Key

1. Go to **API Keys** in the left sidebar
2. Click **Create new key**
3. Give it a descriptive name (e.g., "OCR Skill")
4. Copy the key immediately - it won't be shown again!

Your key looks like: `aBc123XyZ...` (about 32 characters)

## Step 4: Configure Your API Key

### Option A: Tell the Agent Directly (Recommended)

**Works with any AI agent** (Claude Code, skills.sh, etc.):

```
Use this Mistral key: your-api-key-here
```

Or include it in your request:
```
Convert this PDF to markdown. My Mistral API key is: your-api-key-here
```

This is the **simplest and most universal** method.

### Option B: Claude Code Settings

Add to `~/.claude/settings.json`:

```json
{
  "env": {
    "MISTRAL_API_KEY": "your-api-key-here"
  }
}
```

Then restart Claude Code.

### Option C: Environment Variable

**Linux/macOS:**
```bash
export MISTRAL_API_KEY="your-api-key-here"
```

**Windows:**
```powershell
$env:MISTRAL_API_KEY = "your-api-key-here"
```

## Step 5: Verify It Works

Test your key with curl (works on all platforms via Git Bash on Windows):

```bash
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "mistral-ocr-latest", "document": {"type": "document_url", "document_url": "https://www.w3.org/WAI/WCAG21/Techniques/pdf/img/table-word.jpg"}}' \
  | head -100
```

If successful, you'll see extracted markdown from the test image.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Unauthorized" error | Check your API key is correct and has credits |
| "No credits" error | Add billing/credits in Mistral console |
| Key not recognized | Ensure no extra spaces, quotes are correct |
| Rate limited | Wait a minute and try again |

## Pricing Overview

As of 2025, Mistral OCR pricing:

| Service | Cost |
|---------|------|
| OCR (per 1,000 pages) | ~$2.00 |
| Batch API discount | 50% off |

> **Tip:** Check [mistral.ai/pricing](https://mistral.ai/pricing/) for current rates.

## Next Steps

Once your key is configured:

1. Try extracting text from an image
2. Convert a PDF to Markdown
3. See [guide.md](guide.md) for complete examples
