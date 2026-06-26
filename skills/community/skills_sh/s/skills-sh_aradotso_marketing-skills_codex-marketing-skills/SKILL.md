---
name: codex-marketing-skills
description: Use and customize Codex Marketing Skills—YouTube research, Readwise integration, diagram generation, video production, and social publishing workflows for AI agents.
triggers:
  - "help me set up a marketing skill from the codex repo"
  - "analyze YouTube videos for content ideas"
  - "create a diagram with Excalidraw"
  - "search my Readwise highlights for research"
  - "generate a video with Remotion"
  - "schedule a post to Buffer"
  - "research this brand deal opportunity"
  - "pull YouTube transcripts and analyze hooks"
---

# Codex Marketing Skills

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

A curated collection of shareable marketing and creator workflow skills for AI coding agents. Includes YouTube research, Readwise search/export, visual diagram generation, motion graphics/video production, social media publishing, and brand deal research automation.

## What It Does

Codex Marketing Skills provides ready-to-use skill modules that enable AI agents to:

- **YouTube Researcher**: Search channels, pull transcripts, analyze hooks and creator styles
- **Readwise CLI Control**: Query Reader saves and Readwise highlights for content research
- **Excalidraw Diagrams**: Generate editable visual diagrams and flowcharts
- **Paper MCP Integration**: Edit Paper boards and create polished decks
- **Remotion/HyperFrames**: Build motion graphics, launch videos, captions, and rendered assets
- **Gen Media**: Search fal.ai models and generate/edit images and video
- **Brand Deal Researcher**: Scan sponsorship emails, dedupe opportunities, research brands
- **Buffer Publisher**: Draft and schedule social media posts across channels

Each skill is designed to be drop-in compatible with Codex, Claude Code, Cursor, and similar AI agents.

## Installation

### Clone the Repository

```bash
git clone https://github.com/rbrown101010/codex-marketing-skills.git
cd codex-marketing-skills
```

### Install a Skill

Copy the desired skill folder into your agent's skills directory:

```bash
# For Codex
mkdir -p "$HOME/.codex/skills"
cp -R skills/youtube-researcher "$HOME/.codex/skills/"

# For Claude Code (adjust path as needed)
cp -R skills/youtube-researcher "$HOME/.claude/skills/"
```

### Configure Secrets

Each skill requires specific API keys or authentication. Set environment variables or use your system's secret manager:

```bash
# YouTube Researcher
export SUPADATA_API_KEY="your_key_here"
export SERPAPI_KEY="your_key_here"

# Buffer Publisher
export BUFFER_API_KEY="your_key_here"

# Gen Media
export FAL_KEY="your_key_here"
```

**Never commit secrets to the repo.** Reference `docs/requirements.md` in the project for the full setup checklist.

## Skill Overview

### 1. YouTube Researcher

**Location**: `skills/youtube-researcher`

**Requirements**: `SUPADATA_API_KEY`, `SERPAPI_KEY`

**What it does**: Search YouTube channels, extract transcripts, analyze video hooks, and ground AI responses in creator style.

**Key workflow**:

```python
import os
import requests

SUPADATA_API_KEY = os.getenv("SUPADATA_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def search_youtube_channel(channel_id, query):
    """Search a specific YouTube channel for videos matching query."""
    url = f"https://serpapi.com/search"
    params = {
        "engine": "youtube",
        "search_query": f"{query} site:youtube.com/c/{channel_id}",
        "api_key": SERPAPI_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

def get_transcript(video_id):
    """Fetch transcript for a YouTube video."""
    url = f"https://api.supadata.ai/v1/youtube/transcript/{video_id}"
    headers = {"Authorization": f"Bearer {SUPADATA_API_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Example: analyze a creator's hook style
results = search_youtube_channel("veritasium", "physics")
for video in results.get("video_results", [])[:3]:
    transcript = get_transcript(video["id"])
    first_30_sec = [t for t in transcript if t["start"] < 30]
    print(f"Hook for {video['title']}:")
    print(" ".join([t["text"] for t in first_30_sec]))
```

### 2. Readwise CLI Control

**Location**: `skills/readwise-cli-control`

**Requirements**: Readwise CLI installed and authenticated

**What it does**: Search and export highlights from Readwise and Reader for content research.

**Key commands**:

```bash
# Search highlights
readwise search "marketing frameworks"

# Export highlights from a specific book
readwise export --book "Building a Second Brain" --format markdown

# List recent Reader saves
readwise reader list --limit 20
```

**Python integration**:

```python
import subprocess
import json

def search_readwise(query):
    """Search Readwise highlights."""
    result = subprocess.run(
        ["readwise", "search", query, "--format", "json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

# Example: find all highlights about "storytelling"
highlights = search_readwise("storytelling")
for h in highlights[:5]:
    print(f"{h['text']} — {h['title']}")
```

### 3. Excalidraw Diagrams

**Location**: `skills/excalidraw-diagrams`

**Requirements**: `excalidraw-cli` installed

**What it does**: Generate editable Excalidraw diagrams from code or natural language.

**Key commands**:

```bash
# Generate diagram from JSON definition
excalidraw-cli create diagram.json --output funnel.excalidraw

# Export to PNG
excalidraw-cli export funnel.excalidraw --format png --output funnel.png
```

**Python workflow**:

```python
import json
import subprocess

def create_excalidraw_diagram(elements, output_path):
    """Create an Excalidraw diagram from element definitions."""
    diagram_def = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements
    }
    
    with open("temp_diagram.json", "w") as f:
        json.dump(diagram_def, f)
    
    subprocess.run([
        "excalidraw-cli", "create", "temp_diagram.json",
        "--output", output_path
    ])

# Example: create a simple funnel
elements = [
    {"type": "rectangle", "x": 100, "y": 50, "width": 200, "height": 60, "text": "Awareness"},
    {"type": "rectangle", "x": 100, "y": 150, "width": 180, "height": 60, "text": "Interest"},
    {"type": "rectangle", "x": 100, "y": 250, "width": 160, "height": 60, "text": "Purchase"}
]
create_excalidraw_diagram(elements, "marketing_funnel.excalidraw")
```

### 4. Paper MCP

**Location**: `skills/paper-mcp`, `skills/paper-deck-style`

**Requirements**: Paper desktop app, local MCP server running

**What it does**: Programmatically edit Paper boards and create presentation decks.

**Key operations** (via MCP protocol):

```python
import requests

MCP_SERVER = "http://localhost:8080"

def create_paper_card(board_id, title, content):
    """Create a new card on a Paper board."""
    response = requests.post(
        f"{MCP_SERVER}/boards/{board_id}/cards",
        json={"title": title, "content": content}
    )
    return response.json()

def get_board_cards(board_id):
    """Retrieve all cards from a board."""
    response = requests.get(f"{MCP_SERVER}/boards/{board_id}/cards")
    return response.json()

# Example: create a campaign planning board
board_id = "campaign-q4-2026"
create_paper_card(board_id, "Audience", "Target: SaaS founders, 30-45, technical background")
create_paper_card(board_id, "Channels", "LinkedIn, YouTube, email newsletter")
```

### 5. Remotion and HyperFrames

**Location**: `plugin-workflows/remotion`, `plugin-workflows/hyperframes`

**Requirements**: Node.js, Remotion CLI, HyperFrames plugin

**What it does**: Create programmatic motion graphics, launch videos, and caption overlays.

**Key commands**:

```bash
# Render a Remotion composition
npx remotion render src/index.ts LaunchVideo output.mp4

# Preview in browser
npx remotion preview src/index.ts
```

**React/Remotion example**:

```javascript
// src/LaunchVideo.jsx
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

export const LaunchVideo = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });
  
  return (
    <div style={{ flex: 1, justifyContent: 'center', alignItems: 'center', opacity }}>
      <h1 style={{ fontSize: 100 }}>New Product Launch</h1>
    </div>
  );
};
```

**HyperFrames GSAP animation**:

```javascript
// plugin-workflows/hyperframes-gsap/animate.js
import gsap from 'gsap';

export function animateCTA(element) {
  gsap.timeline()
    .from(element, { scale: 0.8, opacity: 0, duration: 0.5 })
    .to(element, { scale: 1.05, duration: 0.3, yoyo: true, repeat: 1 });
}
```

### 6. Gen Media

**Location**: `skills/genmedia`

**Requirements**: `genmedia` CLI, `FAL_KEY` environment variable

**What it does**: Search and run fal.ai models for image/video generation.

**Key commands**:

```bash
# List available models
genmedia list

# Generate an image
genmedia run fal-ai/flux/schnell --prompt "product shot of a coffee mug on a desk" --output mug.png

# Generate a video
genmedia run fal-ai/ltx-video --prompt "camera pan over a modern office" --duration 5 --output office.mp4
```

**Python wrapper**:

```python
import os
import subprocess

FAL_KEY = os.getenv("FAL_KEY")

def generate_image(prompt, model="fal-ai/flux/schnell", output="output.png"):
    """Generate an image using fal.ai models."""
    subprocess.run([
        "genmedia", "run", model,
        "--prompt", prompt,
        "--output", output,
        "--api-key", FAL_KEY
    ])
    return output

# Example: create a thumbnail image
thumbnail = generate_image(
    "bold text 'Marketing Automation' over abstract tech background",
    output="thumbnail.png"
)
print(f"Thumbnail saved to {thumbnail}")
```

### 7. Brand Deal Researcher

**Location**: `skills/brand-deal-researcher`

**Requirements**: Gmail API access, Calendar plugin (optional)

**What it does**: Scan incoming sponsorship emails, deduplicate opportunities, research brands, and produce structured summaries.

**Workflow**:

```python
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def fetch_brand_deal_emails():
    """Fetch unread emails with 'sponsorship' or 'partnership' in subject."""
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.readonly'])
    service = build('gmail', 'v1', credentials=creds)
    
    query = "is:unread (subject:sponsorship OR subject:partnership OR subject:collaboration)"
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    
    deals = []
    for msg in messages:
        full_msg = service.users().messages().get(userId='me', id=msg['id']).execute()
        subject = next(h['value'] for h in full_msg['payload']['headers'] if h['name'] == 'Subject')
        snippet = full_msg['snippet']
        deals.append({"subject": subject, "snippet": snippet, "id": msg['id']})
    
    return deals

# Example: print all new brand deal opportunities
deals = fetch_brand_deal_emails()
for deal in deals:
    print(f"New opportunity: {deal['subject']}")
    print(f"Preview: {deal['snippet']}\n")
```

### 8. Buffer Publisher

**Location**: `skills/buffer-publisher`

**Requirements**: `BUFFER_API_KEY`

**What it does**: Inspect Buffer account state, create drafts, queue posts, and schedule content.

**Key API calls**:

```python
import os
import requests

BUFFER_API_KEY = os.getenv("BUFFER_API_KEY")
BASE_URL = "https://api.bufferapp.com/1"

def get_profiles():
    """List all connected social profiles."""
    response = requests.get(
        f"{BASE_URL}/profiles.json",
        params={"access_token": BUFFER_API_KEY}
    )
    return response.json()

def create_post(profile_id, text, scheduled_at=None):
    """Create a new Buffer post (queued or scheduled)."""
    data = {
        "profile_ids[]": profile_id,
        "text": text,
        "access_token": BUFFER_API_KEY
    }
    if scheduled_at:
        data["scheduled_at"] = scheduled_at
        endpoint = f"{BASE_URL}/updates/create.json"
    else:
        endpoint = f"{BASE_URL}/updates/create.json"
    
    response = requests.post(endpoint, data=data)
    return response.json()

# Example: schedule a LinkedIn post
profiles = get_profiles()
linkedin_profile = next(p for p in profiles if p["service"] == "linkedin")

post = create_post(
    linkedin_profile["id"],
    "Excited to share our new marketing automation toolkit! 🚀",
    scheduled_at="2026-05-25T10:00:00Z"
)
print(f"Post scheduled: {post['id']}")
```

## Common Patterns

### Chaining Skills

Combine multiple skills for end-to-end workflows:

```python
# 1. Research content ideas from Readwise
highlights = search_readwise("content marketing")

# 2. Analyze competitor YouTube videos
competitor_videos = search_youtube_channel("competitor", "content strategy")

# 3. Generate a diagram visualizing the strategy
create_excalidraw_diagram(strategy_elements, "strategy.excalidraw")

# 4. Create social posts for Buffer
for idea in content_ideas:
    create_post(linkedin_profile["id"], idea["text"])
```

### Error Handling

Always check for missing credentials and API errors:

```python
import os
import sys

def ensure_env_var(name):
    value = os.getenv(name)
    if not value:
        print(f"Error: {name} environment variable not set.", file=sys.stderr)
        sys.exit(1)
    return value

BUFFER_API_KEY = ensure_env_var("BUFFER_API_KEY")
```

### Rate Limiting

Respect API rate limits by adding delays:

```python
import time

for video in video_list:
    transcript = get_transcript(video["id"])
    process_transcript(transcript)
    time.sleep(1)  # Avoid hitting rate limits
```

## Troubleshooting

### "API key not found"

Ensure environment variables are set before running:

```bash
echo $BUFFER_API_KEY  # Should print your key
export BUFFER_API_KEY="your_key_here"
```

### "Skill not loaded by agent"

Verify the skill folder is in the correct location:

```bash
ls "$HOME/.codex/skills/youtube-researcher"
# Should show SKILL.md and related files
```

### "Permission denied" for CLI tools

Install CLI tools globally or ensure they're in your PATH:

```bash
which excalidraw-cli
npm install -g excalidraw-cli
```

### MCP Server Not Responding

Check that the Paper desktop app is running and the MCP server is started:

```bash
curl http://localhost:8080/health
# Should return {"status": "ok"}
```

### Readwise CLI Authentication

If Readwise commands fail, re-authenticate:

```bash
readwise logout
readwise login
```

## Further Documentation

- Full setup checklist: `docs/requirements.md`
- Individual skill READMEs in each `skills/` subfolder
- Plugin workflow instructions in `plugin-workflows/`

## Contributing

This is a private team repo. To add a new skill:

1. Create a folder in `skills/` with a clear name
2. Include a README with requirements and examples
3. Add an entry to the main repo table
4. **Never commit secrets or API keys**

---

**License**: No license specified (private repo)

**Repository**: https://github.com/rbrown101010/codex-marketing-skills
