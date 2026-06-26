---
name: sats4ai
description: >
  Bitcoin-powered AI tools marketplace via MCP. Generate images (Flux, Seedream, Recraft),
  text (Kimi K2.5, DeepSeek, GPT-OSS), video (Kling V3), music, speech, 3D models,
  vision analysis, file conversion, and SMS — all paid per use with Bitcoin Lightning.
  No API key, no signup, no credit card. Use when you need AI generation tools and want
  to pay with Lightning micropayments. Works with any Lightning wallet.
homepage: https://sats4ai.com/openclaw
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins: []
---

# Sats4AI — Bitcoin-Powered AI Tools

Sats4AI is an MCP server that gives you access to 10+ AI tools, paid per use with Bitcoin Lightning. No API key, no signup — the Lightning payment is the only authentication.

## Setup

Add the Sats4AI MCP server to your `openclaw.json`:

```json
{
  "mcpServers": {
    "sats4ai": {
      "url": "https://sats4ai.com/api/mcp"
    }
  }
}
```

That's it. You now have access to all tools below.

## You Need a Lightning Wallet

To pay invoices, add a wallet MCP server alongside Sats4AI. The easiest options:

**Option A: Lightning Wallet MCP** (recommended)
```bash
npm install -g lightning-wallet-mcp
lw register --name "my-agent"   # save the API key
lw deposit 10000                # fund with any wallet
```

**Option B: Alby MCP Server**
```json
{
  "mcpServers": {
    "sats4ai": {
      "url": "https://sats4ai.com/api/mcp"
    },
    "wallet": {
      "command": "npx",
      "args": ["-y", "@getalby/mcp"],
      "env": {
        "NWC_CONNECTION_STRING": "nostr+walletconnect://YOUR_CONNECTION_STRING"
      }
    }
  }
}
```

Get your NWC connection string from [Alby Hub](https://getalby.com/ai).

## Available Tools

After connecting, you can call these tools:

### Payment Flow
1. **create_payment** — Get a Lightning invoice for any service. Specify the tool and model.
2. **Pay the invoice** — Using your wallet (Lightning Wallet MCP, Alby, or any Lightning wallet).
3. **Call the tool** — Pass the `paymentId` to execute the service.

### AI Tools

| Tool | What it does | Cost (Sats) |
|------|-------------|-------------|
| **generate_image** | Text to image (Flux, Seedream, Recraft) | 100-200 |
| **generate_text** | Chat with Kimi K2.5, DeepSeek, GPT-OSS | 5-15+ |
| **generate_video** | Text/image to video (Kling V3) | 2,500 |
| **generate_music** | AI-composed songs with vocals (MiniMax) | 200 |
| **generate_speech** | Text to speech (MiniMax voices) | 300 |
| **transcribe_speech** | Audio to text (Whisper) | 10 |
| **generate_3d_model** | Image to 3D model (Hunyuan 3D) | 350 |
| **analyze_image** | Vision / image analysis (Qwen-VL) | 21 |
| **convert_file** | Convert between 200+ file formats | 50 |
| **send_sms** | Send SMS to any country | varies |

### Example: Generate an Image

```
1. Call create_payment with tool: "image", model: "Best"
2. Pay the returned Lightning invoice (e.g., lw pay <invoice>)
3. Call generate_image with paymentId, prompt: "a sunset over mountains", model: "Best"
4. Receive base64 image data
```

### Example: Generate Text with Kimi K2.5

```
1. Call create_payment with tool: "text-generation", model: "Best"
2. Pay the Lightning invoice (~15 Sats minimum)
3. Call generate_text with paymentId and your messages
4. Receive the text response
```

Kimi K2.5 rivals Claude 4.6 and GPT-5.2 in coding, math, and reasoning — at ~$0.006 per request.

## L402 Alternative

You can also use Sats4AI via L402 endpoints with `lnget`:

```bash
lnget --max-cost 500 POST https://sats4ai.com/api/l402/image \
  -d '{"input":{"prompt":"a sunset over mountains"},"model":"Best"}'
```

No MCP needed — `lnget` auto-pays the Lightning invoice on 402 responses.

## Privacy

- No signup, no account, no email
- No API key — payment is the credential
- No KYC or identity verification
- No prompts or outputs logged

## Links

- Website: https://sats4ai.com
- OpenClaw guide: https://sats4ai.com/openclaw
- MCP docs: https://sats4ai.com/mcp
- L402 docs: https://sats4ai.com/l402
- Service discovery: https://sats4ai.com/.well-known/l402-services
