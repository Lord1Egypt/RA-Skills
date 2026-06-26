---
name: video-generator
description: Automated video generation pipeline with OpenAI TTS, Whisper, and Remotion - from text script to professional short videos
tags: [video-generation, remotion, openai, tts, whisper, automation, ai-video, short-video, text-to-video]
---

# 🎬 Video Generator Skill

Automated video generation system that transforms text scripts into professional short videos with AI-powered voiceover, precise timing, and stunning cyber-wireframe visuals.

## 📦 Installation

### Step 1: Install the Skill

```bash
clawhub install video-generator
```

### Step 2: Clone & Setup the Project

**Option A: From GitHub (Recommended)**

```bash
# Clone to standard location
git clone https://github.com/ZhenRobotics/openclaw-video.git ~/openclaw-video
cd ~/openclaw-video

# Install dependencies
npm install

# Set API key
export OPENAI_API_KEY="sk-your-key-here"
```

**Option B: Via npm (Coming Soon)**

```bash
npm install -g openclaw-video
```

### Step 3: Verify Installation

```bash
cd ~/openclaw-video
./agents/video-cli.sh help
```

---

## 🚀 Usage

### When to Use This Skill

**AUTO-TRIGGER** when user's message contains:

- Keywords: `video`, `generate video`, `create video`, `make video`, `生成视频`, `做视频`
- Provides text that looks like a video script (multiple sentences describing a story/concept)
- Asks about video generation, TTS, or Remotion
- Wants to convert text to video format

**TRIGGER EXAMPLES** (always use this skill for these):
- "AI makes development easier. GPT writes code, Whisper transcribes audio, Remotion generates videos." ← This is a VIDEO SCRIPT
- "Generate a video: [any script]"
- "Make a video about AI tools"
- "Create a short video with this content..."

**DO NOT USE** when:
- Only video playback or format conversion (use video-frames skill)
- Video editing or clipping (use other tools)

---

## 🎯 Core Features

Complete video generation pipeline:

- 🎤 **TTS Generation** - OpenAI TTS API with multiple voice options
- ⏱️ **Timestamp Extraction** - OpenAI Whisper API for precise segmentation
- 🎬 **Scene Orchestration** - Intelligent detection of 6 scene types
- 🎨 **Video Rendering** - Remotion with cyber-wireframe aesthetics
- 🤖 **Agent Interface** - Natural language interaction

---

## 💻 Agent Usage Guide

### Important Notes

**CRITICAL**: Use the existing project directory. Do NOT create new projects or run `npx remotion`.

Project location:
- Standard install: `~/openclaw-video/`
- Or detect: Ask user for project location on first use

### Primary Command: Generate Video

When user requests video generation, execute:

```bash
# Method 1: Convenience script (Recommended)
~/openclaw-video/generate-for-openclaw.sh "user's script content"

# Method 2: CLI
cd ~/openclaw-video && ./agents/video-cli.sh generate "script content"

# Method 3: Full Agent (for complex requests)
cd ~/openclaw-video && pnpm exec tsx agents/video-agent.ts "generate video: script content"
```

**Example**:

User says: "Generate video: AI makes development easier"

Execute:
```bash
~/openclaw-video/generate-for-openclaw.sh "AI makes development easier"
```

### Other Operations

**Optimize script**:
```bash
cd ~/openclaw-video && ./agents/video-cli.sh optimize "script content"
```

**Get help**:
```bash
cd ~/openclaw-video && ./agents/video-cli.sh help
```

### Output Location

Generated video saved at: `~/openclaw-video/out/generated.mp4`

---

## ⚙️ Configuration Options

### Voice Selection
- `alloy` - Neutral
- `echo` - Clear
- `nova` - Warm (Recommended)
- `shimmer` - Soft

### Speed
- Range: 0.25 - 4.0
- Recommended: 1.15 (fast-paced short videos)
- Default: 1.0

### Video Style
- Fast-paced short video (default)
- Tutorial/explanation
- Product marketing
- Storytelling

---

## 📊 Video Specifications

- **Resolution**: 1080 x 1920 (Portrait, optimized for TikTok/YouTube Shorts)
- **Frame Rate**: 30 fps
- **Format**: MP4 (H.264 + AAC)
- **Style**: Cyber-wireframe with neon colors
- **Duration**: Auto-calculated based on script length

---

## 🎨 Scene Types

System automatically detects and generates 6 scene types:

| Type | Effect | Trigger Condition |
|------|--------|-------------------|
| **title** | Glitch effect + spring scale | First segment |
| **emphasis** | Pop-up zoom | Contains percentages, numbers |
| **pain** | Shake + red warning | Contains problems, pain points |
| **content** | Smooth fade-in | Regular content |
| **circle** | Rotating ring highlight | Listed points |
| **end** | Slide-up fade-out | Last segment |

---

## 💰 Cost Estimation

Per 15-second video: **~$0.003** (less than 1 cent):

- OpenAI TTS: ~$0.001
- OpenAI Whisper: ~$0.0015
- Remotion rendering: Free (local)

---

## 📝 Usage Examples

### Example 1: Quick Generation

User: "Generate a video: Three AI tools boost productivity. GPT writes code, Whisper transcribes audio, Remotion creates videos."

Agent executes:
```bash
~/openclaw-video/generate-for-openclaw.sh "Three AI tools boost productivity. GPT writes code, Whisper transcribes audio, Remotion creates videos."
```

Output: `~/openclaw-video/out/generated.mp4`

### Example 2: With Configuration

User: "Use warm voice and faster speed"

Agent:
1. Confirm script content
2. Execute with parameters:
```bash
cd ~/openclaw-video && ./agents/video-cli.sh generate "script content" --voice nova --speed 1.3
```

### Example 3: Script Optimization

User: "Is this script good for a video: AI changes the world"

Agent:
```bash
cd ~/openclaw-video && ./agents/video-cli.sh optimize "AI changes the world"
```

Agent receives analysis and informs user.

---

## 🔧 Troubleshooting

### Issue 1: Project Not Found

**Error**: `bash: ~/openclaw-video/generate-for-openclaw.sh: No such file or directory`

**Solution**:
```bash
# Check if project exists
ls ~/openclaw-video

# If not, install the project
git clone https://github.com/ZhenRobotics/openclaw-video.git ~/openclaw-video
cd ~/openclaw-video && npm install
```

### Issue 2: API Key Error

**Error**: `model_not_found` or TTS access denied

**Solution**:
- Use a paid OpenAI account (minimum $5 balance)
- Verify API key has TTS + Whisper access
- Set environment variable: `export OPENAI_API_KEY="sk-..."`

### Issue 3: Missing Dependencies

**Error**: `command not found: pnpm` or `tsx`

**Solution**:
```bash
cd ~/openclaw-video
npm install
```

---

## 📚 Full Documentation

- **GitHub**: https://github.com/ZhenRobotics/openclaw-video
- **Quick Start**: `~/openclaw-video/QUICKSTART.md`
- **Agent Guide**: `~/openclaw-video/docs/AGENT.md`
- **FAQ**: `~/openclaw-video/docs/FAQ.md`
- **Full README**: `~/openclaw-video/README.md`

---

## 🌟 Features

- ✅ Fully automated video generation pipeline
- ✅ Supports Chinese and English scripts
- ✅ Low cost (< $0.01 per video)
- ✅ Local rendering, no cloud services required
- ✅ Cyberpunk visual style
- ✅ Customizable configurations
- ✅ Agent-friendly interface

---

## ⚠️ Important Notes

1. **Environment Variable**: Valid `OPENAI_API_KEY` required
2. **Project Installation**: Must clone and install project before use
3. **Network Required**: TTS and Whisper APIs need internet connection
4. **Path Assumption**: Default project location is `~/openclaw-video/`, adjust if different

---

## 🎯 Agent Behavior Guidelines

When using this skill, agents should:

**DO**:
- ✅ Check if project is installed on first use
- ✅ Use existing project, don't create new Remotion projects
- ✅ Provide clear feedback (progress, estimated time)
- ✅ Handle errors gracefully with solutions
- ✅ Show output location after generation

**DON'T**:
- ❌ Run `npx remotion` to create new projects
- ❌ Assume project is installed without checking
- ❌ Ignore error messages
- ❌ Use hardcoded absolute paths (except `~` paths)

---

## 📊 Tech Stack

- **Remotion**: React-based video generation framework
- **OpenAI TTS**: Text-to-speech API
- **OpenAI Whisper**: Speech recognition API
- **TypeScript**: Type-safe development
- **React**: UI component framework
- **Node.js**: Runtime environment

---

## 🆕 Version History

### v1.0.1 (2026-03-03)
- ✨ Optimized installation guide with universal paths
- 📝 Improved documentation structure
- 🛠️ Added troubleshooting guide
- 🤖 Added agent behavior guidelines
- 🌍 Full English version

### v1.0.0 (2026-03-03)
- ✨ Initial release
- 🎤 TTS voice generation
- ⏱️ Whisper timestamp extraction
- 🎬 Intelligent scene orchestration
- 🎨 Cyber-wireframe visual style
- 🤖 Agent CLI interface

---

**Project Status**: ✅ Production Ready

**License**: MIT

**Author**: @ZhenStaff

**Support**: https://github.com/ZhenRobotics/openclaw-video/issues

**ClawHub**: https://clawhub.ai/ZhenStaff/video-generator
