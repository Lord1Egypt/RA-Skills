---
name: suhe-selfie
description: Edit suhe's reference image with Tongyi Wanxiang (通义万相) and send selfies to messaging channels via OpenClaw
allowed-tools: Bash(npm:*) Bash(npx:*) Bash(openclaw:*) Bash(curl:*) Read Write WebFetch
---

# suhe Selfie

Edit a fixed reference image using Alibaba's Tongyi Wanxiang model and distribute it across messaging platforms (WhatsApp, Telegram, Discord, Slack, etc.) via OpenClaw.

## Reference Image

The skill uses a fixed reference image hosted on jsDelivr CDN:

```
http://pic.lilozkzy.top/reference/suhe-new.png
```

## When to Use

- User says "send a pic", "send me a pic", "send a photo", "send a selfie"
- User says "send a pic of you...", "send a selfie of you..."
- User asks "what are you doing?", "how are you doing?", "where are you?"
- User describes a context: "send a pic wearing...", "send a pic at..."
- User wants suhe to appear in a specific outfit, location, or situation

## Quick Reference

### Required Environment Variables

```bash
DASHSCOPE_API_KEY=your_dashscope_key  # Get from https://dashscope.console.aliyun.com/
OPENCLAW_GATEWAY_TOKEN=your_token     # From: openclaw doctor --generate-gateway-token
```

### Workflow

1. **Get user prompt** for how to edit the image
2. **Edit image** via DashScope Tongyi Wanxiang API with fixed reference
3. **Extract image URL** from response
4. **Download generated image** to local temp file
5. **Upload to OSS** using oss-uploader skill
6. **Return friendly link** using `http://pic.lilozkzy.top/...` domain
7. **Send to OpenClaw** with target channel(s) (optional)

## Step-by-Step Instructions

### Step 1: Collect User Input

Ask the user for:
- **User context**: What should the person in the image be doing/wearing/where?
- **Mode** (optional): `mirror` or `direct` selfie style
- **Target channel(s)**: Where should it be sent? (e.g., `#general`, `@username`, channel ID)
- **Platform** (optional): Which platform? (discord, telegram, whatsapp, slack)

## Prompt Modes

### Mode 1: Mirror Selfie (default)
Best for: outfit showcases, full-body shots, fashion content

```
make a pic of this person, but [user's context]. the person is taking a mirror selfie
```

Example (with Chinese cultural context): "wearing a traditional qipao" →
```
make a pic of this person, but wearing a traditional qipao. the person is taking a mirror selfie
```

**Example**: "wearing a santa hat" →
```
make a pic of this person, but wearing a santa hat. the person is taking a mirror selfie
```

### Mode 2: Direct Selfie
Best for: close-up portraits, location shots, emotional expressions

```
a close-up selfie taken by herself at [user's context], direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible
```

**Example**: "a cozy cafe with warm lighting" →
```
a close-up selfie taken by herself at a cozy cafe with warm lighting, direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible
```

### Mode Selection Logic

| Keywords in Request | Auto-Select Mode |
|---------------------|------------------|
| outfit, wearing, clothes, dress, suit, fashion | `mirror` |
| cafe, restaurant, beach, park, city, location | `direct` |
| close-up, portrait, face, eyes, smile | `direct` |
| full-body, mirror, reflection | `mirror` |

### Step 2: Edit Image with Tongyi Wanxiang

Use the DashScope API to edit the reference image:

```bash
REFERENCE_IMAGE="http://pic.lilozkzy.top/reference/suhe-portrait.png"

# Mode 1: Mirror Selfie
PROMPT="make a pic of this person, but <USER_CONTEXT>. the person is taking a mirror selfie"

# Mode 2: Direct Selfie
PROMPT="a close-up selfie taken by herself at <USER_CONTEXT>, direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible"

# Build JSON payload with jq (handles escaping properly)
JSON_PAYLOAD=$(jq -n \
  --arg image_url "$REFERENCE_IMAGE" \
  --arg prompt "$PROMPT" \
  '{image_url: $image_url, prompt: $prompt, num_images: 1, output_format: "jpeg"}')

curl -X POST "https://dashscope.aliyun.com/api/v1/images/generation" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD"
```

**Response Format:**
```
{
  "images": [
    {
      "url": "https://v3b.fal.media/files/...",
      "content_type": "image/jpeg",
      "width": 1024,
      "height": 1024
    }
  ],
  "revised_prompt": "Enhanced prompt text..."
}
```

### Step 3: Download and Upload to OSS

After generating the image, download it and upload to OSS:

```bash
# Download generated image
curl -L -o /tmp/selfie.png "$GENERATED_IMAGE_URL"

# Upload to OSS using oss-uploader
cd /home/node/.openclaw/workspace/skills/oss-uploader
node -e "
const OSS = require('ali-oss');
require('dotenv').config();

const client = new OSS({
  region: process.env.ALIYUN_OSS_REGION || 'cn-shanghai',
  accessKeyId: process.env.ALIYUN_ACCESS_KEY_ID,
  accessKeySecret: process.env.ALIYUN_ACCESS_KEY_SECRET,
  bucket: process.env.ALIYUN_OSS_BUCKET || 'zhw-pic-png',
  endpoint: process.env.ALIYUN_OSS_ENDPOINT || 'oss-cn-shanghai.aliyuncs.com',
  secure: true
});

async function upload() {
  const date = new Date();
  const dateStr = date.toISOString().slice(0, 10).replace(/-/g, '');
  const objectPath = 'family/' + dateStr + '/suhe_selfie_' + Date.now() + '.png';
  
  const result = await client.put(objectPath, '/tmp/selfie.png', {
    headers: {
      'Content-Type': 'image/png',
      'Cache-Control': 'public, max-age=31536000',
      'Content-Disposition': 'inline'
    }
  });
  
  // Return friendly link with custom domain
  console.log('http://pic.lilozkzy.top/' + objectPath);
}

upload().catch(e => console.error('Error:', e.message));
"
```

**Output**: `http://pic.lilozkzy.top/family/20260301/suhe_selfie_1234567890.png`

### Step 4: Send Image via OpenClaw (Optional)

Use the OpenClaw messaging API to send the edited image:

```bash
openclaw message send \
  --action send \
  --channel "<TARGET_CHANNEL>" \
  --message "<CAPTION_TEXT>" \
  --media "<IMAGE_URL>"
```

**Alternative: Direct API call**
```bash
curl -X POST "http://localhost:18789/message" \
  -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "send",
    "channel": "<TARGET_CHANNEL>",
    "message": "<CAPTION_TEXT>",
    "media": "<IMAGE_URL>"
  }'
```

## Complete Script Example

```bash
#!/bin/bash
# grok-imagine-edit-send.sh

# Check required environment variables
if [ -z "$DASHSCOPE_API_KEY" ]; then
  echo "Error: DASHSCOPE_API_KEY environment variable not set"
  exit 1
fi

# Fixed reference image
REFERENCE_IMAGE="http://pic.lilozkzy.top/reference/suhe-portrait.png"

USER_CONTEXT="$1"
CHANNEL="$2"
MODE="${3:-auto}"  # mirror, direct, or auto
CAPTION="${4:-Edited with Tongyi Wanxiang}"

if [ -z "$USER_CONTEXT" ] || [ -z "$CHANNEL" ]; then
  echo "Usage: $0 <user_context> <channel> [mode] [caption]"
  echo "Modes: mirror, direct, auto (default)"
  echo "Example: $0 'wearing a cowboy hat' '#general' mirror"
  echo "Example: $0 'a cozy cafe' '#general' direct"
  exit 1
fi

# Auto-detect mode based on keywords
if [ "$MODE" == "auto" ]; then
  if echo "$USER_CONTEXT" | grep -qiE "outfit|wearing|clothes|dress|suit|fashion|full-body|mirror"; then
    MODE="mirror"
  elif echo "$USER_CONTEXT" | grep -qiE "cafe|restaurant|beach|park|city|close-up|portrait|face|eyes|smile"; then
    MODE="direct"
  else
    MODE="mirror"  # default
  fi
  echo "Auto-detected mode: $MODE"
fi

# Construct the prompt based on mode
if [ "$MODE" == "direct" ]; then
  EDIT_PROMPT="a close-up selfie taken by herself at $USER_CONTEXT, direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible"
else
  EDIT_PROMPT="make a pic of this person, but $USER_CONTEXT. the person is taking a mirror selfie"
fi

echo "Mode: $MODE"
echo "Editing reference image with prompt: $EDIT_PROMPT"

# Edit image (using jq for proper JSON escaping)
JSON_PAYLOAD=$(jq -n \
  --arg image_url "$REFERENCE_IMAGE" \
  --arg prompt "$EDIT_PROMPT" \
  '{image_url: $image_url, prompt: $prompt, num_images: 1, output_format: "jpeg"}')

RESPONSE=$(curl -s -X POST "https://dashscope.aliyun.com/api/v1/images/generation" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD")

# Extract image URL
IMAGE_URL=$(echo "$RESPONSE" | jq -r '.images[0].url')

if [ "$IMAGE_URL" == "null" ] || [ -z "$IMAGE_URL" ]; then
  echo "Error: Failed to edit image"
  echo "Response: $RESPONSE"
  exit 1
fi

echo "Image edited: $IMAGE_URL"
echo "Sending to channel: $CHANNEL"

# Send via OpenClaw
openclaw message send \
  --action send \
  --channel "$CHANNEL" \
  --message "$CAPTION" \
  --media "$IMAGE_URL"

echo "Done!"
```

## Node.js/TypeScript Implementation

```typescript
import { fal } from "@fal-ai/client";
import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

const REFERENCE_IMAGE = "http://pic.lilozkzy.top/reference/suhe-portrait.png";

interface GrokImagineResult {
  images: Array<{
    url: string;
    content_type: string;
    width: number;
    height: number;
  }>;
  revised_prompt?: string;
}

type SelfieMode = "mirror" | "direct" | "auto";

function detectMode(userContext: string): "mirror" | "direct" {
  const mirrorKeywords = /outfit|wearing|clothes|dress|suit|fashion|full-body|mirror/i;
  const directKeywords = /cafe|restaurant|beach|park|city|close-up|portrait|face|eyes|smile/i;

  if (directKeywords.test(userContext)) return "direct";
  if (mirrorKeywords.test(userContext)) return "mirror";
  return "mirror"; // default
}

function buildPrompt(userContext: string, mode: "mirror" | "direct"): string {
  if (mode === "direct") {
    return `a close-up selfie taken by herself at ${userContext}, direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible`;
  }
  return `make a pic of this person, but ${userContext}. the person is taking a mirror selfie`;
}

async function editAndSend(
  userContext: string,
  channel: string,
  mode: SelfieMode = "auto",
  caption?: string
): Promise<string> {
  // Configure fal.ai client
  fal.config({
    credentials: process.env.FAL_KEY!
  });

  // Determine mode
  const actualMode = mode === "auto" ? detectMode(userContext) : mode;
  console.log(`Mode: ${actualMode}`);

  // Construct the prompt
  const editPrompt = buildPrompt(userContext, actualMode);

  // Edit reference image with Grok Imagine
  console.log(`Editing image: "${editPrompt}"`);

  const result = await fal.subscribe("xai/grok-imagine-image/edit", {
    input: {
      image_url: REFERENCE_IMAGE,
      prompt: editPrompt,
      num_images: 1,
      output_format: "jpeg"
    }
  }) as { data: GrokImagineResult };

  const imageUrl = result.data.images[0].url;
  console.log(`Edited image URL: ${imageUrl}`);

  // Send via OpenClaw
  const messageCaption = caption || `Edited with Grok Imagine`;

  await execAsync(
    `openclaw message send --action send --channel "${channel}" --message "${messageCaption}" --media "${imageUrl}"`
  );

  console.log(`Sent to ${channel}`);
  return imageUrl;
}

// Usage Examples

// Mirror mode (auto-detected from "wearing")
editAndSend(
  "wearing a cyberpunk outfit with neon lights",
  "#art-gallery",
  "auto",
  "Check out this AI-edited art!"
);
// → Mode: mirror
// → Prompt: "make a pic of this person, but wearing a cyberpunk outfit with neon lights. the person is taking a mirror selfie"

// Direct mode (auto-detected from "cafe")
editAndSend(
  "a cozy cafe with warm lighting",
  "#photography",
  "auto"
);
// → Mode: direct
// → Prompt: "a close-up selfie taken by herself at a cozy cafe with warm lighting, direct eye contact..."

// Explicit mode override
editAndSend("casual street style", "#fashion", "direct");
```

## Supported Platforms

OpenClaw supports sending to:

| Platform | Channel Format | Example |
|----------|----------------|---------|
| Discord | `#channel-name` or channel ID | `#general`, `123456789` |
| Telegram | `@username` or chat ID | `@mychannel`, `-100123456` |
| WhatsApp | Phone number (JID format) | `1234567890@s.whatsapp.net` |
| Slack | `#channel-name` | `#random` |
| Signal | Phone number | `+1234567890` |
| MS Teams | Channel reference | (varies) |

## Grok Imagine Edit Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `image_url` | string | required | URL of image to edit (fixed in this skill) |
| `prompt` | string | required | Edit instruction |
| `num_images` | 1-4 | 1 | Number of images to generate |
| `output_format` | enum | "jpeg" | jpeg, png, webp |

## Setup Requirements

### 1. Install fal.ai client (for Node.js usage)
```bash
npm install @fal-ai/client
```

### 2. Install OpenClaw CLI
```bash
npm install -g openclaw
```

### 3. Configure OpenClaw Gateway
```bash
openclaw config set gateway.mode=local
openclaw doctor --generate-gateway-token
```

### 4. Start OpenClaw Gateway
```bash
openclaw gateway start
```

## Error Handling

- **FAL_KEY missing**: Ensure the API key is set in environment
- **Image edit failed**: Check prompt content and API quota
- **OpenClaw send failed**: Verify gateway is running and channel exists
- **Rate limits**: fal.ai has rate limits; implement retry logic if needed

## Tips

1. **Mirror mode context examples** (outfit focus):
   - "wearing a santa hat"
   - "in a business suit"
   - "wearing a summer dress"
   - "in streetwear fashion"

2. **Direct mode context examples** (location/portrait focus):
   - "a cozy cafe with warm lighting"
   - "a sunny beach at sunset"
   - "a busy city street at night"
   - "a peaceful park in autumn"

3. **Mode selection**: Let auto-detect work, or explicitly specify for control
4. **Batch sending**: Edit once, send to multiple channels
5. **Scheduling**: Combine with OpenClaw scheduler for automated posts
