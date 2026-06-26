# Embedding & Integration Reference

Three ways to deploy Trugen agents into your application.

## Option A: iFrame Embed (Simplest)

Zero setup — no WebRTC or media pipelines required:

```html
<iframe
  src="https://app.trugen.ai/embed/{agent_id}?username=USER_NAME&id=USER_ID&context=CONTEXT"
  width="100%"
  height="600"
  frameborder="0"
  allow="camera; microphone; autoplay">
</iframe>
```

**Why use iFrame:**
- Zero WebRTC configuration
- Works in any HTML/CMS environment
- Camera, microphone, speech, vision out of the box
- Production-ready across all browsers

## Option B: Widget Embed

A floating chat-widget button that opens the agent interface.

> **⚠️ Security Note**: The examples below follow the official Trugen docs pattern. In production, consider injecting the `apiKey` value server-side rather than hardcoding it in client-facing HTML, as it will be visible to anyone inspecting the page.

**1. Configure the widget before the script tag:**
```html
<script>
  window.TrugenWidget = {
    agentName: "Your agent name",
    agentId: "your-agent-id",
    apiKey: "x-api-key",
    heading: "Main heading of widget",
    subHeading: "Sub heading of widget",
    logoUrl: "https://yourdomain.com/logo.svg",
    displayAvatarUrl: "https://yourdomain.com/avatar.png"
  };
</script>
<script src="https://dist.trugen.ai/trugen-chat.js"></script>
```

**Complete Widget Example:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Widget Integration</title>
</head>
<body>
  <script>
    window.TrugenWidget = {
      agentName: 'Lisa',
      agentId: "your-agent-id",
      apiKey: "x-api-key",
      heading: "Lisa AI Sales Agent",
      subHeading: "Your AI sales assistant",
      logoUrl: "https://trugen.ai/_next/static/media/trugen-logo2.d572f903.svg",
      displayAvatarUrl: "https://trugen.ai/_next/static/media/trugen-logo2.d572f903.svg"
    };
  </script>
  <script src="https://dist.trugen.ai/trugen-chat.js"></script>
</body>
</html>
```

## Option C: LiveKit Integration (Advanced)

For custom LiveKit-based voice/video agents, add Trugen avatars to your existing LiveKit pipeline.

**Install the plugin:**
```bash
pip install "livekit-agents[trugen]~=1.3"
# or with UV:
uv add "livekit-agents[trugen]~=1.3"
```

**Setup:**
1. Generate an API key from the [Developer Platform](https://app.trugen.ai)
2. Set `TRUGEN_API_KEY` in your `.env` file
3. (Optional) Set `TRUGEN_AVATAR_ID` for the avatar to use

**Integration code:**
```python
from livekit.plugins import trugen
import os

async def entrypoint(ctx: JobContext):
    session = AgentSession(
        # Your existing LiveKit agent configuration
    )

    # Add Trugen avatar
    avatar_id = os.getenv("TRUGEN_AVATAR_ID") or "45e3f732"
    trugen_avatar = trugen.AvatarSession(avatar_id=avatar_id)
    await trugen_avatar.start(session, room=ctx.room)

    await session.start(
        # Start agent session as usual
    )

    # Gracefully shutdown:
    # Use ctx.room.disconnect() to close the room connection
    # or ctx.shutdown() to end the JobContext.
    # TruGen Avatar session stops automatically when room disconnects.
```

## LiveKit-Ready Avatar IDs

| Avatar | ID |
|--------|----|
| Kevin | `182b03e8` |
| Jessica | `21ef04ad` |
| Cathy | `17de03e4` |
| Sofia | `1928040f` |
| Lucy | `c5b563de` |
| Kiara | `178303d3` |
| Jason | `05a001fc` |
| Sameer | `be5b2ce0` |
| Jennifer | `0de70332` |
| Mike | `03ae0187` |
| Johnny | `1fa504ff` |
| Priya | `7d881c1b` |
| Chloe | `178803d6` |
| Lisa | `1a640442` |
| Aman | `0f160301` |
| Allie | `057501e8` |
| Misha | `05b401f3` |
| Alex | `13550375` |
| Amir | `48d778c9` |
| Akbar | `18c4043e` |
