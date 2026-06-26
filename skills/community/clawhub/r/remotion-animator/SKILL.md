---
name: remotion-animator
description: "Create animated videos programmatically using Remotion. Triggered only when the user explicitly asks to (1) make, edit, render, or build an animated video or motion graphics, (2) animate text, numbers, progress bars, or components, (3) render a composition to MP4/ProRes/WebM, (4) programmatically generate video content via an agent, (5) scaffold a video project and render it, or (6) convert an existing project into an animated explainer, intro, or social clip. Does not trigger on general discussion, search, or information requests about video tools.

**Permission boundaries:** This skill scaffolds Node.js projects in the agent workspace and runs Node/npm/Remotion shell commands. The agent only creates files within the specified project directory. No networking, no external file access outside the workspace, no sudo.

**Proactivity rules:** The agent may offer to create a video once (per request) when user content clearly matches a template type. The agent must ask before scaffolding. Declined offers are never repeated for the same content.

**Cron/recurring automation:** Not enabled by default. If the user requests recurring renders, the agent must confirm: schedule, output directory, file retention policy, and a disable method before creating any cron job. No unattended background rendering without explicit consent."
---

# Remotion Animator

Your agent builds animated videos with components. No After Effects needed — write code, preview in browser, render to MP4.

## Showcase

Your agent scaffolds, builds, and renders videos on demand. Templates for intros, explainers, data visualizations, and dialogue videos. A library of animation components your agent composes and customizes for each task.

📹 [Watch the showcase video](https://github.com/PratyushChauhan/PratyushChauhan/releases/download/remotion-showcase-v1/remotion-showcase-agent.mp4)

## Quick Start

### 1. Scaffold a project

```bash
python /path/to/skill/scripts/new-project.py my-video
```

### 2. Install dependencies

```bash
cd my-video && npm install
```

### 3. Preview in studio

```bash
npm run dev
# Open http://localhost:3000
```

### 4. Render to video

```bash
npm run render
# Or use the render helper:
python /path/to/skill/scripts/render.py --output out/video.mp4 --quality high
```

## Templates

Scaffold with a pre-built template instead of the starter:

```bash
python scripts/new-project.py my-intro --template intro
python scripts/new-project.py my-stats --template data-kinetic
python scripts/new-project.py my-tutorial --template explainer
python scripts/new-project.py my-podcast --template conversation
```

| Template | Use Case | Duration |
|----------|----------|----------|
| **starter** | Blank canvas with animation primitives | 6s |
| **intro** | Logo + title + tagline reveal | 5s |
| **data-kinetic** | Animated metrics, count-ups, progress bars | 8s |
| **explainer** | Step-by-step feature walkthrough | 10s |
| **conversation** | Multi-speaker dialogue with colored bubbles | Variable |

Set dimensions for vertical video:
```bash
python scripts/new-project.py my-reel --template intro --width 1080 --height 1920
```

## Animation Components

Import from `./components` in any project scaffolded from this skill:

```tsx
import { FadeIn, SlideIn, ScaleIn, Typewriter, CountUp, ProgressBar } from "./components";
```

| Component | Effect |
|-----------|--------|
| `<FadeIn>` | Opacity tween |
| `<SlideIn>` | Directional slide with opacity |
| `<ScaleIn>` | Scale up with easing overshoot |
| `<Typewriter>` | Character-by-character text reveal |
| `<CountUp>` | Number counter animation |
| `<ProgressBar>` | Animated progress bar |
| `<DriftingGrid>` | Drifting CSS grid background |
| `<FloatingOrb>` | Ambient floating orb |
| `<PulseRing>` | Expanding attention ring |
| `<StaggerChildren>` | Staggered child animations |

**Usage example:**

```tsx
export const MyVideo: React.FC = () => {
  return (
    <div style={{ width: "100%", height: "100%", background: "#0a0a0f" }}>
      <FadeIn start={0} duration={20}>
        <h1 style={{ fontSize: 72, color: "#fff" }}>Hello World</h1>
      </FadeIn>
      <SlideIn start={25} direction="up">
        <p style={{ fontSize: 28, color: "#a0a0b0" }}>Animated with code</p>
      </SlideIn>
    </div>
  );
};
```

## Customizing Templates

### Change colors
Edit gradient backgrounds or component color props:
```tsx
background: "linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%)"
```

### Change timing
All animations are frame-based. At 30fps:
- 30 frames = 1 second
- 15 frames = 0.5 seconds

### Add audio
Place audio in `public/audio.mp3`, then:
```tsx
import { Audio, staticFile } from "remotion";
<Audio src={staticFile("audio.mp3")} />
```

### Load data from JSON
```tsx
const data = require("../data/content.json");
```

## Render Options

```bash
# High quality, smaller file
python scripts/render.py --quality high --codec h264

# ProRes for editing
python scripts/render.py --codec prores --quality ultra

# Vertical video
python scripts/render.py --output out/reel.mp4
# (Set composition width/height in Root.tsx)
```

## Resources

- **references/proactivity.md** — When and how to suggest animation proactively
- **references/component-api.md** — Full component API reference
- **references/animation-patterns.md** — Timing, easing, stagger, loops, audio sync
- **assets/boilerplate/** — Base Remotion project with component library
- **assets/templates/** — Pre-built compositions (intro, data-kinetic, explainer, conversation)
- **scripts/new-project.py** — Project scaffolding tool
- **scripts/render.py** — Render helper with quality presets

## Proactivity

This skill enables one-time proactive video creation. The agent may offer once when content clearly matches a specific template type. The agent must obtain explicit verbal confirmation before scaffolding any project.

**User-facing warning when recurring is mentioned:** Cron-based jobs are persistent automation that continue running on schedule until explicitly removed. They consume compute resources and generate output files repeatedly. Always explain this before the user consents.

### Offer triggers (one-time only)

The agent may suggest a video one time when these specific content patterns are unambiguous:

| Signal | Template to suggest | Pitch |
|--------|---------------------|-------|
| User shares a transcript or interview | `conversation` | "Want me to turn this into a conversation video?" |
| User shares stats, metrics, or KPIs | `data-kinetic` | "These numbers would hit harder as an animated clip." |
| User announces a product/feature | `intro` + custom | "Want a quick intro video for the announcement?" |
| User writes a step-by-step guide | `explainer` | "I can animate this into a shareable explainer." |
| User asks for a social media clip | `intro` (vertical) | "Want this as a short-form video?" |

### Pitch rules

- **Ask, don't assume**: "Want me to animate this?" not "I'm making a video."
- **Suggest a template**: Reference the specific template by name.
- **One offer per content**: If the user declines or ignores, do not re-offer.
- **Recurring prohibited without explicit four-part confirmation**: The agent must not create any cron job unless the user explicitly confirms (a) exact schedule, (b) output directory, (c) file retention policy, (d) how to disable. If any part is missing, the agent stops.

## Dependencies

- Node.js + npm
- `@remotion/cli` (included in boilerplate package.json)
