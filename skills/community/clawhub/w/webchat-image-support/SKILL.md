# webchat-image-support

Universal image understanding enhancement for OpenClaw. This skill enables image understanding across all channels (WebChat, Discord, Slack, etc.) and works with any model that supports image input.

## What It Does

When users send images through any channel, this skill ensures the agent can understand and analyze them:

- **Automatic Detection**: Detects when an inbound message contains images
- **Universal Support**: Works with Claude, MiniMax, OpenAI, Gemini, or any vision-enabled model
- **Fallback Processing**: If model doesn't support images, uses OpenClaw's built-in media understanding pipeline
- **Multi-Image Support**: Handles multiple images in a single message

## Requirements

1. **Gateway with image support** (OpenClaw 2026.3.29+)
2. **At least one vision-capable model** configured in `models.json`:
   - Claude (with vision)
   - MiniMax-VL-01
   - Gemini Pro Vision
   - GPT-4 Vision

## Usage

No explicit commands needed. Just send images:

```
User: [sends a screenshot of error]
Agent: "我看到了错误信息：Unable to load script..."

User: [sends a photo]
Agent: "这张图片显示了一个卡通猪头..."
```

## Configuration

### Model Selection

For best results, use a vision-capable model. In `~/.openclaw/agents/main/agent/models.json`:

```json
{
  "providers": {
    "minimax": {
      "models": [
        {
          "id": "MiniMax-VL-01",
          "input": ["text", "image"]
        }
      ]
    }
  }
}
```

### Default Behavior

| Model Support | Behavior |
|---------------|----------|
| Model supports images | Direct image input to model |
| Model no images | Use media understanding pipeline |

## Troubleshooting

**Q: Agent doesn't see images**
A: Make sure your model supports image input (check `input` field in models.json)

**Q: Images sent but no response**
A: Check gateway logs for media processing errors

**Q: Works in CLI but not WebChat**
A: This skill requires OpenClaw 2026.3.29+ with the MediaPath fix

## Related

- Gateway fix: [GitHub #57064](https://github.com/openclaw/openclaw/issues/57064)
- OpenClaw docs: https://openclaw.dev
