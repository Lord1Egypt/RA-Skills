# 🎬 Remotion Server Skill for OpenClaw

Render videos headlessly on any Linux server using [Remotion](https://remotion.dev). No Mac or GUI required.

## What it does

- **Headless rendering** - generate MP4, WebM, GIF, or PNG sequences from code
- **Chat demo template** - Telegram-style phone mockup with animated messages
- **Title card template** - animated intro/title cards
- **Any Linux server** - works on VPS, Pi, CI, wherever Chrome headless runs

## Quick start

### Install the skill

```bash
git clone https://github.com/mvanhorn/clawdbot-skill-remotion-server.git ~/.openclaw/skills/remotion-server
```

### One-time setup

Install browser dependencies (Ubuntu/Debian):

```bash
bash scripts/setup.sh
```

### Create and render a project

```bash
bash scripts/create.sh my-video
cd my-video
npx remotion render MyComp out/video.mp4
```

### Example chat usage

- "Make a video showing a chat about our new feature"
- "Create a promo video for the product launch"
- "Render a title card that says 'Welcome to OpenClaw'"

## Templates

**Chat Demo** - phone mockup with animated chat bubbles:
```bash
bash scripts/create.sh my-promo --template chat
# Edit src/messages.json with your conversation
```

**Title Card** - simple animated intro:
```bash
bash scripts/create.sh my-intro --template title
```

## Output formats

- MP4 (h264) - default
- WebM (vp8/vp9) - `--codec=vp8`
- GIF - `--codec=gif`
- PNG sequence

## How it works

Wraps Remotion's CLI renderer with project scaffolding and templates. The setup script installs Chrome headless dependencies (libnss3, libatk, libgbm, etc.) so rendering works on headless Linux. All templates use fake demo data only.

## License

MIT
