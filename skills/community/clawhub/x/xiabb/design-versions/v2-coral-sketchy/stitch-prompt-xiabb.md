# Design Brief: 虾BB (XiaBB) — Unified Design System

## The Product

虾BB is a free, open-source macOS voice-to-text tool for developers. Hold the Globe key, speak in mixed Chinese + English, text appears at your cursor with perfect punctuation. 280KB, pure Swift, zero dependencies.

**The name is the brand:** 虾BB = 瞎BB = "talking nonsense" in Chinese internet slang. The joke: the best ideas sound crazy when you say them out loud. A voice-to-text tool named after talking nonsense.

**Target users:** Developers doing "Vibe Coding" — building software by talking to AI tools (Claude Code, Cursor, etc.) in a mix of Chinese and English.

## The Mascot

A lobster holding a microphone. We call it "BB" (虾哥). The lobster-mic silhouette is the existing logo (attached as SVG).

The mascot should feel like an indie developer's inside joke — someone you'd put on a laptop sticker. Not corporate, not childish. Mischievous, expressive, the kind of character who talks too much but is always right.

## What We Need Designed

Three surfaces that currently look like they were designed by three different people:

1. **Website** (xiabb.lol) — Landing page. Dark theme. Single HTML file for GitHub Pages.
2. **Onboarding wizard** — 6-step setup flow inside a native macOS window (600×500px, WKWebView). Currently light theme with blue accents that don't match the website at all.
3. **HUD overlay** — Small floating translucent panel (~300px wide) that appears during recording. Shows live text, audio bars, lobster icon.

These need to feel like one product.

## Design References We Love

Study these sites for how they integrate mascots:

- **deno.com** — Dinosaur in a cozy coding scene as the hero. Lo-fi warm illustration style. The mascot IS the atmosphere. We love how the scene tells the product story visually.
- **go.dev** — Gopher appears in 3-4 different action poses across sections (climbing ladder, flying plane, pilot bust). Same character, different contexts. Shows a mascot can repeat without feeling childish.
- **bun.sh** — Cute mascot + dark mode + dead serious benchmarks. The contrast between kawaii and hardcore is powerful. Also: mascot appears in unexpected small places.
- **astro.build** — Houston astronaut woven into error states, CLI, and community touchpoints. Subtle but omnipresent.

For overall polish: **linear.app**, **raycast.com**, **warp.dev**

For Chinese mascot branding: **闲鱼** (reclaimed 咸鱼 = "deadbeat" as brand, same pattern as our 瞎BB), **知乎 刘看山** (lo-fi indie illustration style), **哔哩哔哩 2233娘** (character with personality lore)

## What's Fixed (Hard Constraints)

- Website must be a single HTML file (no frameworks, no build step)
- Onboarding is HTML embedded in a Swift string (rendered in WKWebView inside a 600×500 NSWindow)
- HUD is native NSView (colors specified as RGB floats)
- Must support Chinese (primary) + English (secondary) with a language toggle
- Website must be responsive
- Existing logo silhouette (lobster-with-mic SVG) should be the basis for the character design
- MIT open source, free product — should feel indie/premium, not enterprise SaaS
- Chinese text is primary, English secondary

## What's Open (Design Questions for You)

### Color & Theme
- The website is dark. The onboarding is light. The HUD is dark translucent. **How should the accent color unify these?** Currently the website uses red (#ef4444) and the onboarding uses blue (#3b82f6) — they feel disconnected. What's the right unified palette?
- Should the onboarding stay light or go dark to match the website? Or is there a warm middle ground?
- Red is the obvious lobster color, but is it the right primary? Or should red be reserved for the mascot while the UI uses a different accent? What secondary/tertiary colors complement a lobster character?
- Should we lean warm (lobster reds, oranges, golds) or contrast warm mascot against cool UI (like Bun's warm bun on cool dark)?

### Illustration Style
- What illustration style best fits "indie dev tool with a meme mascot"? Lo-fi anime (like Deno)? Flat geometric (like Go's gopher)? Something else entirely?
- How detailed should the hero scene be vs. the section cameos?
- Should the mascot have a consistent outline weight, or vary between detailed (hero) and simplified (icons)?

### Mascot Treatment
- We want the mascot throughout the page — **hero scene** (like Deno's dino-at-desk) + **section poses** (like Go's gopher) + **Easter eggs** (like Bun). But how many appearances is too many before it gets annoying?
- What poses/expressions would work best for each section?
- Should the mascot appear in the onboarding wizard too? If so, how — full illustrations or just the logo mark?
- For the HUD (tiny floating panel), how much mascot presence makes sense at ~300px wide?

### Typography
- What font pairing says "playful but trustworthy developer tool"? Needs to handle both Chinese and English well. The current site uses Helvetica Neue which is... fine but forgettable.
- How should the headline hierarchy work for mixed CN+EN content?

### Layout & Composition
- The 瞎BB pun/story is our strongest brand asset. Where should it live — hero subtitle? Its own section? How prominent?
- How should the comparison table work visually? (We're free vs competitors at $8-29/month — this is a key selling point)
- The "How it works" flow is dead simple (3 steps: hold Globe → speak → text appears). What's the most impactful way to visualize this?

## Page Content (for the website)

### Navbar
- Logo + 虾BB
- Links: Features, Compare, Install
- GitHub star count + Download CTA

### Hero
- Product name + the 瞎BB brand story
- Tagline: 按住 Globe 键，说话，文字出现。
- Sub: 专为 Vibe Coding 打造的语音输入法
- CTA: Download for macOS + View on GitHub
- The hero scene illustration with the lobster

### Features (6)
1. 永久免费 — Gemini free tier, 250 transcriptions/day
2. 中英混搭 — Bilingual Chinese + English, perfect punctuation
3. 实时预览 — Streaming text preview as you speak
4. 280KB 极简 — Pure Swift, zero dependencies
5. 开源 MIT — Full source on GitHub
6. LLM 引擎 — Gemini understands meaning, not just sound

### How It Works
1. Press and hold Globe key → 2. Speak → 3. Text appears at cursor

### Comparison Table
| | 虾BB | SuperWhisper | Typeless | Wispr Flow | MacWhisper |
|---|---|---|---|---|---|
| Price | Free | $8.49/mo | $12/mo | $15/mo | $29 one-time |
| Engine | Gemini LLM | Whisper | Whisper | Whisper | Whisper |
| Size | 280KB | ~100MB | ~200MB | ~150MB | ~1GB |
| Streaming | Yes | No | Yes | Yes | No |
| Open source | Yes (MIT) | No | No | No | No |
| Chinese+English | Native | Basic | Basic | Basic | Basic |

### Install
```bash
# Download
curl -L -o /tmp/XiaBB.dmg "https://github.com/dyz2102/xiabb/releases/..."
# Verify + install
open /tmp/XiaBB.dmg
```

### Footer
- GitHub · MIT License · xiabb.lol
- Something with personality — not a generic footer

## Mascot Poses Needed

At minimum, for the website and product UI:
1. **Hero scene** — Lobster in a late-night coding environment with mic
2. **Listening** — Active, mic up, sound waves
3. **Winning** — Confident, for comparison section
4. **Teaching/pointing** — For install section
5. **Waving** — Friendly, for CTA/footer
6. **Celebrating** — Success state, "BB!" — for the HUD after transcription
7. **Thinking** — Processing state — for the HUD during transcription
8. **Confused** — Error state — for when something goes wrong

But I'm open to your suggestions on what poses would work best.

## Deliverables

1. **Unified color system** — Tokens that work across dark website, light/warm onboarding, translucent HUD
2. **Typography system** — For mixed CN+EN content
3. **Mascot character sheet** — Based on the logo silhouette, with poses
4. **Hero illustration** — The signature scene
5. **Website design** — Full landing page layout with mascot integrated
6. **Onboarding design** — 6 screens at 600×500px (Welcome, API Key, Mic, Accessibility, Try It, Dictionary)
7. **HUD design** — Recording, processing, and success states
8. **Component library** — Buttons, cards, inputs, badges, step dots
