# X Expert - Smart X Publisher

A ClawHub Skill for OpenClaw/NanoClaw

## Features

This is a smart X (Twitter) publishing assistant that helps you create, plan, and publish tweets through a **conversational workflow**.

### Core Features

- ✅ Conversational publishing flow (9 steps)
- ✅ Information collection (Exa / MiniMax / Brave Search)
- ✅ Smart tweet generation (multiple styles)
- ✅ Image generation (DALL-E / MiniMax / Nano Banana / Leonardo.ai)
- ✅ Scheduled publishing
- ✅ Pre-publish review

## Installation

### Option 1: ClawHub CLI

```bash
npx clawhub@latest install x-expert
```

### Option 2: Manual Install

```bash
git clone https://github.com/shiyusimon/x-publisher-skill.git ~/.openclaw/skills/x-publisher
cd ~/.openclaw/skills/x-publisher
npm install
```

## Configuration

### Required Environment Variables

```bash
# X API (Required)
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
```

### Optional Environment Variables

```bash
# Search services (optional, choose one or more)
EXA_API_KEY=your_exa_key
MINIMAX_API_KEY=your_minimax_key
BRAVE_API_KEY=your_brave_key

# Image generation (optional, choose one or more)
OPENAI_API_KEY=your_openai_key       # DALL-E
MINIMAX_API_KEY=your_minimax_key    # MiniMax Image
NANO_BANANA_API_KEY=your_nano_key   # Nano Banana
LEONARDO_API_KEY=your_leonardo_key # Leonardo.ai
```

## Usage

Type `/x-expert` to start the conversational publishing flow.

### Workflow

1. **Confirm Needs** - Do you need to collect information first?
2. **Collect Information** - Search for relevant topics
3. **Confirm Content** - Do you need help writing tweets?
4. **Determine Style** - Choose tweet style and reference examples
5. **Publishing Settings** - Schedule/review settings
6. **Confirm Images** - Do you need images?
7. **Image Style** - Choose image style and service
8. **Generate Images** - Call AI to generate images
9. **Final Confirm** - Preview and publish

## Scripts

| Script | Function |
|--------|----------|
| `post-tweet.js` | Post a single tweet |
| `post-thread.js` | Post a tweet thread |
| `post-media.js` | Post tweet with media |
| `collect-info.js` | Search information |
| `generate-tweet.js` | Generate tweet content |
| `generate-image.js` | Generate images |
| `delete-tweet.js` | Delete a tweet |

## License

MIT
