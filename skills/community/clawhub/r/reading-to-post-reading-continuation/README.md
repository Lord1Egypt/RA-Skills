# Reading to Post-Reading Continuation Writing

A skill for turning any English reading passage into an interactive post-reading continuation writing (读后续写) exercise — a single-file HTML webpage.

## What This Skill Does

- Takes a reading passage
- Extracts characters, emotions, events, timeline, plot structure
- Generates an 8-section interactive webpage
- Outputs a single self-contained HTML file with no external dependencies

## The 8 Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Home | Title, subtitle, friendship proverb, "Start the Journey" CTA |
| 2 | Original Text | Passage with character/emotion/event highlights + click-to-annotate |
| 3 | Basic Information | Cards + timeline + 5 open-ended discussion questions with answers |
| 4 | Character Analysis | Two word-bank sections with adjective chips |
| 5 | Story Mountain | SVG mountain with 5 foldable step cards |
| 6 | Continuation Planning | Two panels with 3 plan items each + draft textareas |
| 7 | Writing Sample | Language Bank + Basic Version + Advanced Version |
| 8 | Practice | 7 cloze questions with click-to-check |

## Usage

Just open the HTML file in any browser — no server or internet required.

## Publishing to ClawHub

```bash
# 1. Install the CLI
npm i -g clawhub

# 2. Sign in
clawhub login

# 3. Verify
clawhub whoami

# 4. Dry run first
clawhub skill publish ./reading-to-post-reading-continuation --slug reading-to-post-reading-continuation --name "Reading to Post-Reading Continuation Writing" --categories education,writing --topics "reading,writing,english-teaching" --dry-run

# 5. Publish
clawhub skill publish ./reading-to-post-reading-continuation --slug reading-to-post-reading-continuation --name "Reading to Post-Reading Continuation Writing" --categories education,writing --topics "reading,writing,english-teaching"
```

## Design System

- **Navy**: `#1B2A4A` — headers, buttons, section titles
- **Accent blue**: `#4A90D9` — buttons, highlights
- **Accent light**: `#E8F1FB` — hover states
- **Accent soft**: `#D6E6F5` — advanced structure highlight
- **Page bg**: `#F7F9FC` — background
- **Card bg**: `#FFFFFF` — cards
- **Text primary**: `#2D3748` — body
- **Border**: `#E2E8F0` — card borders

### Visual fatigue rules

- Max 3 accent colors
- Generous whitespace
- Body text: `0.98rem`, `line-height: 1.65`
- Section title: `2rem`, `font-weight: 800`, navy
- All annotation text bilingual (English + Chinese)
