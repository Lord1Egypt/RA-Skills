---
name: reading-to-post-reading-continuation
description: >
  Step-by-step skill: convert any English reading passage into an interactive post-reading continuation writing (读后续写) webpage exercise. Covers reading analysis, 8-section structure, navy/white/single-accent design system, and HTML/JS/HTML output with no external dependencies.
  Output: a single self-contained HTML file (reading_continuation_webpage.html) with 8 interactive sections.
category: education
---

# Reading to Post-Reading Continuation Writing Skill

Turn any English reading passage into an interactive, classroom-ready post-reading continuation writing exercise. The output is a single self-contained HTML file — no internet or server required.

## Trigger

- You are a high school English teacher (reading/writing lesson)
- You have a reading passage and want to turn it into a "读后续写" (post-reading continuation writing) task
- You want an interactive, classroom-ready webpage (not a static document)
- You want the design to be "like a product homepage" — minimal, navy blue (#1B2A4A) + white + single accent (#4A90D9)
- You want to share the lesson template with other teachers

## Communication Style

- **Be concise and direct.** State the action and the result in 1–3 sentences.
- **One-line is enough.** A one-line answer for a one-line question.
- **Skip the apology.** Do not say "I'm sorry" or "Please let me know." Just report what happened.
- **When GitHub push fails** with `Recv failure: Connection was reset`, report the failure plainly, then suggest: wait and retry, use GitHub web upload, or switch network.

## Input

Provide the reading passage text (English). Include:
- The full passage (or the relevant excerpt)
- Any title, author, or source info

## Output

A single self-contained HTML file (e.g., `reading_continuation_webpage.html`) that:
1. Opens in any browser — no internet or server required
2. Contains **8 interactive sections** in order:
   - **Home**: title, subtitle, friendship proverb, CTA "Start the Journey"
   - **Original Text**: full passage with character/emotion/event highlights + click-to-annotate tooltips
   - **Basic Information**: Characters / Setting / Key Events cards + timeline + 5 open-ended discussion questions + "Show Answers ▼" collapse
   - **Character Analysis**: 2 word-bank card sections (each protagonist) with 8–9 adjective chips + reflection prompt
   - **Story Mountain**: white card with an SVG mountain (polygon path + snow cap at peak); 5 foldable step cards with "Show Plot Detail" buttons; step labels on a slope row
   - **Continuation Planning**: 2 panel sections (Paragraph 1 / Paragraph 2), each with 3 foldable plan items; textarea for draft
   - **Writing Sample**: Language Bank table (12 common phrases) + Basic Version + Advanced Version (advanced sentences highlighted in blue bold)
   - **Practice**: 7 cloze questions drawn from the sample essays, click-to-check
3. Uses the navy/white/single-blue accent design system (product-homepage aesthetic)
4. No external dependencies — works offline in any browser

## Design System (standing rules)

### Colors

| Token | Hex | Usage |
|---|---|---|
| Navy | `#1B2A4A` | Headers, buttons, active nav, section titles |
| Accent blue | `#4A90D9` | Buttons, highlights, section labels, fold indicators |
| Accent light | `#E8F1FB` | Button hover, chip highlight, form fields |
| Accent soft | `#D6E6F5` | Advanced structure highlight background |
| Page bg | `#F7F9FC` | Page background |
| Card bg | `#FFFFFF` | Cards, panels |
| Text primary | `#2D3748` | Body text |
| Text secondary | `#718096` | Labels, hints, descriptions |
| Text faint | `#A0AEC0` | Placeholder, faint guide text |
| Border | `#E2E8F0` | Card borders, separators |

### Visual fatigue rules (always)

- Keep the design minimal — no more than **3 accent colors**
- Avoid decorative clutter; use generous whitespace
- Cards use thin borders (`1px solid #E2E8F0`) and subtle shadow
- Body text: `0.98rem`, `line-height: 1.65`
- Section title: `2rem`, `font-weight: 800`, navy
- Section label: inline badge `0.78rem`, white text on accent bg, `border-radius: 20px`
- All annotation text must be **bilingual (English + Chinese)** — students are Chinese high school students

## Procedure (in order)

### Step 1 — Read the passage

- Extract: characters, emotions, events, timeline, plot structure
- Identify the two protagonists and their relationship arc

### Step 2 — Generate title and subtitle

- Use the passage title or a generated title (e.g., "Friendship on the Rocks")
- Subtitle: "From Reader to Writer — 读后续写"

### Step 3 — Build the 8 sections in order

See "The 8 Sections" section below for detailed templates of each section.

### Step 4 — Write the HTML/CSS/JS

- Single self-contained file (no external CSS/JS/CDN)
- Use the design system above
- Include interactivity: highlight clicks, foldable panels, cloze checks, scroll progress, breathing pulse on the "Start" button

### Step 5 — Test in browser

- Open the file and verify:
  - All 8 sections render correctly
  - Interactive features work (highlight tooltips, foldable panels, cloze checks)
  - Responsive at 1280×720 and 768×1024
  - No external dependencies

### Step 6 — Save

- Output as `reading_continuation_webpage.html`

## The 8 Sections (Detailed)

### Section 1 — Home / Intro

- Title: "Friendship on the Rocks" (from passage or generated)
- Subtitle: "From Reader to Writer — 读后续写"
- Friendship proverb (bilingual): e.g., Sir Walter Scott quote or a Chinese English proverb
- CTA button: "🚀 Start the Journey" (remove Chinese text from the button)
- Minimal: just title, subtitle, proverb card, and the button

### Section 2 — Original Text

- Display the full passage with highlights
- Highlight words/phrases connecting to:
  - **Characters**: people, roles, relationships
  - **Emotions**: feeling words, emotional states, inner thoughts
  - **Events**: actions, plot points, time markers
- Legend: 人物 (characters) / 情绪 (emotions) / 事件 (events)
- Click a highlight → tooltip annotation with bilingual explanation
- Pitfall: Do not highlight every word — only the 15–25 most meaningful items

### Section 3 — Basic Information

- **Cards**: Characters | Setting | Key Events (grid layout)
- **Timeline**: Before / During / After the incident
- **5 open-ended questions** (no single-answer), e.g.:
  - "Why does Amy say 'How stupid I was'? What does this reveal about her change in understanding?"
  - "What does 'hardly out of each other's sight' tell us about their relationship?"
  - "What is Amy's real problem? Is it only the lie, or is it something about her friendship?"
- **Show Answers ▼** button that reveals bilingual answer explanations

### Section 4 — Character Analysis

- Two word-bank sections (main character + counterpart)
- 8–9 adjective chips per section (click to select, visual feedback)
- Reflection: "Combine 2 adjectives for each character to write a short description"
- Pitfall: Do not let students just pick random adjectives — require them to justify with evidence from the text

### Section 5 — Story Mountain

- **White card** with **SVG mountain** (single polygon path + snow cap at peak)
- **Slope label row**: "1 · Beginning" → "2 · Rising Action" → "3 · Climax" → "4 · Falling Action" → "≠ Resolution"
- **5 foldable step cards** with "Show Plot Detail" buttons:
  1. Beginning: eight-year friendship; "hardly out of each other's sight"
  2. Rising Action: Saturday plan: see a film; friend posts "cold"; Amy comforts her
  3. Climax: classmate reveals the "cold" was a complete lie
  4. Falling Action: Amy avoids her friend at school; refuses messages; stress mounting
  5. Resolution (Open): your continuation starts here
- Each step has a "Show Plot Detail" button (click to expand)
- Pitfall: Do not use CSS gradients for the mountain — use an SVG polygon path so the mountain shape is clearly visible. A gradient triangle is not easily recognizable as a mountain.

### Section 6 — Continuation Planning

- **Two panels**: Paragraph 1 (Amy's reaction) | Paragraph 2 (Reconciliation)
- Each panel: 3 foldable plan items (feelings → realization → attempt to reach the friend)
- Textareas for drafting two paragraphs (minimum 80 words, past tense)
- Pitfall: Students often write continuation without a clear paragraph breakdown — the planner panel prevents this

### Section 7 — Writing Sample

- **Language Bank table**: 12 common phrases with example sentences
- **Basic Version**: simpler sentence structures
- **Advanced Version**: 3–4 advanced sentence structures, highlighted in blue bold with subtle background
- Hint button on each sample to label which sentences are advanced

### Section 8 — Practice (Cloze)

- **7 fill-in-the-blank questions** drawn from the sample essays
- Each question: 4 options, click-to-check with immediate feedback (correct/wrong)
- Reflection prompt at the end
- Pitfall: Do not make cloze questions too easy or too hard — use phrases from the actual sample that students should have learned

## GitHub Push

After creating the webpage file:

```bash
git add reading_continuation_webpage.html SKILL.md README.md
git commit -m "Add post-reading continuation writing webpage builder skill"
git push -u origin main
```

## Publish to ClawHub

### Prerequisites

1. Install the ClawHub CLI globally:
   ```bash
   npm i -g clawhub
   # or
   pnpm add -g clawhub
   ```

2. Sign in (opens GitHub OAuth flow):
   ```bash
   clawhub login
   ```

3. Verify your login:
   ```bash
   clawhub whoami
   ```

### Publish a skill folder

A skill is a folder containing `SKILL.md` plus any supporting files:

```bash
clawhub skill publish ./my-skill --slug my-skill --name "My Skill" --changelog "Initial release"
```

| Flag | Description |
|---|---|
| `--slug <slug>` | Published skill URL name (lowercase, hyphens) |
| `--name <name>` | Display name shown on the catalog |
| `--changelog <text>` | One-line changelog for this release |
| `--version <version>` | Semver version (default: `1.0.0` for new skills) |
| `--dry-run` | Preview the publish plan without uploading |
| `--categories <cat1,cat2>` | Category slugs from the catalog (e.g., `development,education`) |
| `--topics <t1,t2>` | Free-form topic tags (show as `#t1` on the catalog) |
| `--owner <handle>` | Publish to an org owned listing (omit for your own) |

### Example: publishing this skill

```bash
# 1. Create the skill folder
mkdir -p reading-to-post-reading-continuation
cd reading-to-post-reading-continuation

# 2. Write SKILL.md (frontmatter + content)
# 3. Write README.md (optional, for human browsing)

# 4. Dry run to preview
clawhub skill publish . --slug reading-to-post-reading-continuation \
  --name "Reading to Post-Reading Continuation Writing" \
  --categories education,writing --topics "reading,writing,english-teaching"

# 5. Publish for real
clawhub skill publish . --slug reading-to-post-reading-continuation \
  --name "Reading to Post-Reading Continuation Writing" \
  --categories education,writing --topics "reading,writing,english-teaching"
```

### After publishing

- The skill appears on `clawhub.ai` with a page: `https://clawhub.ai/skills/<slug>`
- Share the URL with colleagues. They can install with:
  ```bash
  openclaw skills install @<owner>/reading-to-post-reading-continuation
  ```

## Pitfalls and How to Avoid Them

| Pitfall | Why | Rule |
|---|---|---|
| CSS gradient used for the mountain | A CSS triangle is not easily recognizable as a mountain shape | Use an SVG polygon path with a snow cap at the peak |
| Too many accent colors | Causes visual fatigue, defeats the "product homepage" minimal aesthetic | Limit to 3 accent colors: navy, accent blue, accent light |
| Too many highlighted words | Over-highlighted text loses meaning and overwhelms students | Highlight only 15–25 most meaningful words |
| Bright colors | Causes visual fatigue in a classroom setting | Keep the palette low-saturation; use navy as the dominant color |
| Chinese text on buttons | Confuses the "product homepage" clean aesthetic | Use English for buttons, Chinese for annotations and explanations |
| Dead JS references | Script references elements that no longer exist in the HTML | After any HTML edit, grep for all `onclick`/`id` references and match them |
| Only one version of the sample | Students at different levels need different support | Provide both a Basic Version and an Advanced Version |
