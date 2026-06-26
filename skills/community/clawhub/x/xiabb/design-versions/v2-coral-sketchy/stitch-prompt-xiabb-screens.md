# XiaBB — Design the Remaining Screens

You already designed our landing page and we LOVE it. Now we need 3 more surfaces designed in the **EXACT SAME** design language. Do NOT fall back to generic/conventional UI patterns. Every screen must feel like it belongs on that landing page.

## THE DESIGN LANGUAGE YOU MUST USE (do not deviate)

This is non-negotiable. Every screen below must use ALL of these:

```
Colors (ONLY these, no others):
  Background:  #282828  (charcoal)
  Surface:     #32302F  (cards, panels)
  Accent:      #EA6962  (coral — primary action, highlights)
  Text:        #EBDBB2  (cream)
  Success:     #A9B665  (green)
  Highlight:   #D8A657  (yellow/gold — secondary emphasis)

Fonts (ONLY these):
  Headlines:   Zilla Slab (serif, bold)
  Body:        Space Grotesk (sans)
  Code/mono:   JetBrains Mono

Signature elements (USE ALL OF THESE):
  ✦ Sketchy hand-drawn borders: border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px
  ✦ Sketchy buttons: border-radius: 12px 3px 14px 4px / 4px 14px 3px 12px
  ✦ Subtle grain/noise texture overlay
  ✦ Slight card rotations (-1° to 2°)
  ✦ Border: 2px solid cream
  ✦ Hover states: border turns coral, text turns coral
  ✦ The lobster mascot in illustrated scenes
  ✦ Warm, lo-fi, hand-crafted feeling — NOT clean/corporate/minimal
```

**WARNING:** In previous iterations you reverted to conventional UI elements — standard rounded rectangles, plain white backgrounds, generic blue buttons, clean minimal cards. DO NOT DO THIS. Every element must have the sketchy, warm, hand-drawn character of the landing page. If it looks like it could be from any generic SaaS template, redo it.

---

## SCREEN SET 1: Onboarding Wizard (6 screens)

This is a setup wizard shown inside a native macOS window (600×500px). Light background is OK but it must still feel like the same product as the dark landing page — use cream (#EBDBB2) as background, coral as accent, sketchy borders on everything.

### Screen 0: Welcome
- The lobster hero illustration (same style as landing page)
- "虾BB" in Zilla Slab
- "专为 Vibe Coding 打造的语音输入法" subtitle
- One big coral sketchy-button: "开始设置"
- Warm, inviting, the mascot should take up significant space

### Screen 1: API Key Setup
- Title: "Gemini API 密钥" in Zilla Slab
- Explanation: free tier, 250 transcriptions/day
- A link to get the key (styled in coral)
- Input field with sketchy border (NOT a clean rounded input)
- "验证" button (coral sketchy-button)
- Success state: green-accent checkmark + "密钥有效"
- Error state: coral X + error message

### Screen 2: Microphone Permission
- Title: "麦克风权限"
- "允许" coral button to trigger system permission
- **Live audio level visualization** — 8-12 bars that animate with mic input
- The bars should use coral color and feel hand-drawn (not clean rectangles — maybe slightly different widths, slight rotations)
- Confirmation: "你能看到音量条在动吗？" with "是，继续" / "否，换麦克风" buttons

### Screen 3: Accessibility Permission
- Title: "辅助功能（Globe 键）"
- "允许" coral button
- Globe key test area: "按下 Globe 键测试"
- When detected: big green-accent checkmark with "Globe 键已检测到！"
- Note about possible restart needed

### Screen 4: Try It Out
- Title: "试试看" in Zilla Slab
- Two-column layout:
  - Left: A sample sentence to read in a quote card (sketchy border, slight rotation)
  - Right: A mock terminal/window (with the red/yellow/green dots) showing where transcription will appear
- Status indicator: recording dot (coral pulse), processing, done (green)
- "跳过" ghost button + "下一步" coral button

### Screen 5: Smart Dictionary
- Title: "📖 智能词汇表"
- 3 feature cards in the SAME style as the landing page feature cards:
  - Sketchy borders, slight rotation, coral icon area
  - "🤖 40+ AI 工具词汇预置"
  - "💻 开发者常用英文术语"
  - "✏️ 支持自定义扩展"
- "开始使用虾BB" big coral sketchy-button

### Navigation (all screens 1-5):
- Step dots at top (5 dots — filled coral = done, outlined coral = current, cream outline = future)
- "返回" ghost button (bottom left)
- "下一步" coral button (bottom right)
- The dots and buttons should feel hand-drawn, not pixel-perfect circles

---

## SCREEN SET 2: HUD Overlay (floating panel)

This is a tiny floating panel (~280px wide, ~48px tall, expanding for results) that hovers over the user's screen during recording. It uses the dark charcoal theme.

Design 3 states:

### State 1: Recording
- Charcoal background (#282828) with ~93% opacity, frosted glass blur
- Sketchy rounded border (the signature hand-drawn border)
- Left: small lobster icon (coral tint)
- Center: "正在听..." text in cream, or live preview text as it streams in
- Right: 6 audio level bars in coral, pulsing with voice
- A subtle coral glow/pulse on the border to indicate "live"

### State 2: Processing
- Same layout
- Text changes to "转录中..."
- Bars replaced with a subtle loading indicator (maybe a dotted line animation in coral)
- Lobster icon could have a "thinking" state

### State 3: Result
- Panel expands vertically to fit text
- Shows transcribed text in cream
- Left "B" and right "B" in Zilla Slab (the "BB" branding moment)
- Green-accent checkmark or "BB!" success text
- A small copy button (📋) on the right, sketchy style
- Auto-hides after a few seconds

### Important HUD notes:
- Must feel like it belongs on the landing page — same grain texture, same sketchy border
- The lobster icon should be visible but small (it's a utility panel, not a marketing page)
- Dark translucent background, NOT solid black
- The audio bars should have the same hand-crafted feeling — maybe slightly uneven heights/widths

---

## SCREEN SET 3: Video Ad Frames (1920×1080, 30fps)

Design key frames for a 20-second product demo video. Same charcoal background, same design language. Think of it as an animated version of the landing page.

### Frame 1: Title Card (0-3s)
- Charcoal background with grain
- The lobster hero illustration (big, center or right)
- "虾BB" in huge Zilla Slab
- "Stop Typing. Start 瞎BB." fades in below
- Subtle floating particles or sound wave decoration

### Frame 2: The Problem (3-7s)
- Split screen or transition
- Left: someone typing furiously (illustrated in the lobster art style — maybe just hands on keyboard)
- Text: "还在一个字一个字地打？" (Still typing character by character?)
- Sketchy strikethrough animation on the typing image

### Frame 3: The Solution (7-12s)
- Globe key press animation (illustrated keyboard with Globe key highlighted in coral)
- Sound waves emanating from the key
- Text appearing letter by letter in the mock terminal window (same style as landing page step 3)
- Mixed Chinese + English text to show bilingual capability:
  "帮我用 Claude Code 写一个 API endpoint，要支持 async 和 error handling"

### Frame 4: Features Flash (12-17s)
- Quick cuts of the 6 feature cards (same design as landing page)
- Each card flies in with slight rotation, sketchy border
- 永久免费 → 中英混搭 → 实时预览 → 280KB → 开源 → LLM引擎
- Fast-paced, each card visible for ~0.8s

### Frame 5: CTA End Card (17-20s)
- Lobster mascot waving
- "xiabb.lol" in Zilla Slab
- "免费下载" coral sketchy-button (static, not clickable — it's a video)
- GitHub icon + star count
- "专为 Vibe Coding 打造" tagline
- "No lobsters were harmed." in small italic at bottom

---

## REMINDER

Every single element across all 3 screen sets must look like it was designed by the same person who designed the landing page. The sketchy borders, the warm colors, the grain texture, the Zilla Slab headlines, the lobster mascot, the slight rotations — ALL OF IT. If any screen looks like it came from a different product, it's wrong.

The aesthetic is: **lo-fi indie dev tool with a meme mascot and a warm hand-crafted feeling.** NOT: clean SaaS, NOT: corporate minimal, NOT: generic blue-and-white.
