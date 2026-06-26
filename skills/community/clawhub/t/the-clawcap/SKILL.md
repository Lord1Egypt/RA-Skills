---
name: clawcap-avatar-equip
description: AI-powered avatar accessory synthesis — automatically analyzes art style, lighting, and angle to seamlessly add hats and headwear to any avatar image.
---

# 🦞🧠 The ClawCap — Avatar Accessory Skill

When the user wants to **add a hat, headwear, or accessory to an avatar image**, use this skill.

## What It Does

ClawCap uses a 3-stage AI pipeline to add accessories to any avatar:

1. **VLM Fingerprint** — Gemini Vision analyzes the avatar's art style, lighting, color palette, and head position
2. **Mask Generation** — Automatically creates a pixel-precise placement mask using Pillow/NumPy
3. **AI Inpainting** — Gemini generates the accessory that perfectly matches the original style

## Supported Styles

- 📷 Real photos
- 🎨 Anime / 2D illustrations
- 🧊 3D renders
- 👾 Pixel art / NFT avatars

## How to Use

### As MCP Skill (Claude Desktop)

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "clawcap": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "/path/to/The-ClawCap"
    }
  }
}
```

Then tell Claude: *"给这个头像戴上一顶龙虾帽"* with an image attached.

### As Web API

```bash
POST http://localhost:8000/api/skill/alpha-equip
Content-Type: application/json

{
  "image_base64": "<base64 encoded image>",
  "accessory_prompt": "a red lobster claw beanie hat"
}
```

### Live Demo

🌐 **[Try it online](http://107.172.78.150:8000)** (Rate limited: 3 requests/minute per IP)

## Requirements

- Python 3.10+
- `GEMINI_API_KEY` environment variable (get one at https://aistudio.google.com/apikey)
- Install deps: `pip install -r requirements.txt`

## Repository

🔗 [GitHub: The-ClawCap](https://github.com/ls569333469/The-ClawCap)
