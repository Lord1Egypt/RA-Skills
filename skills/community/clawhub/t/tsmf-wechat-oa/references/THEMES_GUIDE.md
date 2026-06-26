# 🎨 WeChat Official Account Theme Guide

## Quick Usage

```bash
# View all 20 themes
python3 scripts/push_draft.py --list-themes

# Use specific theme
python3 scripts/push_draft.py --file article.md --theme macaron_lavender
```

---

## Classic Themes (8)

### 1️⃣ Minimal Business (minimal_business)
**Best for:** Business analysis, career tips, management insights
**Features:** Professional black-white-gray, bottom border H1, left blue line H2
**Colors:** Primary #1a1a2e, Accent #0984e3

---

### 2️⃣ Warm Artistic (warm_artistic)
**Best for:** Lifestyle, emotions, book reviews
**Features:** Warm beige/gold tones, centered title, decorative borders
**Colors:** Primary #8b6914, Background #fdf8f0

---

### 3️⃣ Tech Modern (tech_modern)
**Best for:** Technical tutorials, programming, digital reviews
**Features:** Dark background, glowing title, VS Code-style code blocks
**Colors:** Background #0d1117, Accent #58a6ff

---

### 4️⃣ Fresh Lively (fresh_lively)
**Best for:** Food, travel, lifestyle content
**Features:** Colorful palette, centered coral H1, large rounded corners
**Colors:** Primary #ff6b6b, Accent #4ecdc4

---

### 5️⃣ Magazine Premium (magazine_premium)
**Best for:** Fashion, art, deep reading
**Features:** Elegant typography, generous whitespace, magazine-quality design
**Colors:** Primary #1a1a1a, Accent #c0a080

---

### 6️⃣ Academic Professional (academic_professional)
**Best for:** Academic papers, research reports, scholarly analysis
**Features:** Rigorous academic style, navy borders, italic quotes
**Colors:** Primary #1a365d, Accent #4299e1

---

### 7️⃣ Retro Classic (retro_classic)
**Best for:** History, traditional culture, memoirs
**Features:** Nostalgic vintage feel, sepia tones, decorative gold borders
**Colors:** Primary #5c3d2e, Accent #c9a86c

---

### 8️⃣ Dark Minimal (dark_minimal)
**Best for:** Gaming, anime, nighttime reading, tech
**Features:** Dark theme with glowing accents, optimized for low-light
**Colors:** Background #1a202c, Accent #63b3ed

---

## Macaron Themes (12) - Soft Pastel Colors

### 🌸 Macaron Pink (macaron_pink)
**Best for:** Female audience, romance, emotion, lifestyle
**Features:** Sweet pink gradients, soft rounded corners, warm and gentle
**Colors:** Background #fef6f9, Accent #d4859a

---

### 🌊 Macaron Blue (macaron_blue)
**Best for:** Travel, nature, relaxation, calming content
**Features:** Serene blue gradients, clean and refreshing
**Colors:** Background #f0f9ff, Accent #4299e1

---

### 🌿 Macaron Mint (macaron_mint)
**Best for:** Health, eco-friendly, natural, wellness
**Features:** Fresh mint gradients, natural and clean
**Colors:** Background #f0fdfa, Accent #14b8a6

---

### 💜 Macaron Lavender (macaron_lavender)
**Best for:** Romance, art, dreamy content, French style
**Features:** Elegant purple gradients, romantic and refined
**Colors:** Background #faf5ff, Accent #a78bfa

---

### 🍑 Macaron Peach (macaron_peach)
**Best for:** Food, desserts, afternoon tea, warm content
**Features:** Warm peach gradients, cozy and sweet
**Colors:** Background #fff7ed, Accent #f97316

---

### 🍋 Macaron Lemon (macaron_lemon)
**Best for:** Energy, motivation, positive vibes, sunny topics
**Features:** Bright yellow gradients, vibrant and uplifting
**Colors:** Background #fefce8, Accent #eab308

---

### 🪸 Macaron Coral (macaron_coral)
**Best for:** Passion, summer, beach, energetic content
**Features:** Warm coral gradients, passionate and bold
**Colors:** Background #fff5f5, Accent #f87171

---

### 🌱 Macaron Sage (macaron_sage)
**Best for:** Nature, outdoor, forest, eco lifestyle
**Features:** Natural green gradients, fresh and organic
**Colors:** Background #f0fdf4, Accent #4ade80

---

### 💐 Macaron Lilac (macaron_lilac)
**Best for:** Elegant, refined, sophisticated content
**Features:** Sophisticated purple gradients, refined and classy
**Colors:** Background #fdf4ff, Accent #d946ef

---

### 🥛 Macaron Cream (macaron_cream)
**Best for:** Cozy, home, healing, daily life
**Features:** Warm cream gradients, comfortable and cozy
**Colors:** Background #fffbeb, Accent #d4a574

---

### ☁️ Macaron Sky (macaron_sky)
**Best for:** Travel, freedom, dreams, inspirational
**Features:** Light blue gradients, fresh and airy
**Colors:** Background #f0f9ff, Accent #38bdf8

---

### 🌹 Macaron Rose (macaron_rose)
**Best for:** Love, romance, elegant lifestyle
**Features:** Romantic pink gradients, exquisite and lovely
**Colors:** Background #fdf2f8, Accent #ec4899

---

## Theme Selection Guide

| Article Type | Recommended Theme |
|--------------|-------------------|
| AI/Tech Tutorial | tech_modern |
| Career/Business Analysis | minimal_business |
| Lifestyle/Emotions/Books | warm_artistic, macaron_lavender |
| Food/Travel/Lifestyle | fresh_lively, macaron_peach |
| Fashion/Art/Deep Reading | magazine_premium, macaron_rose |
| Academic Papers/Research | academic_professional |
| History/Tradition/Memoirs | retro_classic |
| Gaming/Anime/Night Reading | dark_minimal |
| Female/Romance/Emotion | macaron_pink, macaron_rose |
| Health/Eco/Wellness | macaron_mint, macaron_sage |
| Energy/Motivation/Positive | macaron_lemon, macaron_coral |
| Travel/Freedom/Dreams | macaron_blue, macaron_sky |
| Cozy/Home/Healing | macaron_cream |
| Elegant/Refined/Sophisticated | macaron_lilac |

## Smart Theme Recommendation

```
"AI Development Trends" → tech_modern (confidence: 60%)
"Coffee Culture and Life" → warm_artistic (confidence: 75%)
"Business Strategy Analysis" → minimal_business (confidence: 80%)
"Romantic Love Story" → macaron_pink (confidence: 85%)
"Healthy Living Guide" → macaron_mint (confidence: 75%)
"Travel Diary" → macaron_blue (confidence: 70%)
```

## Technical Implementation

Theme system uses CSS-in-Python architecture with background color blocks.
Edit `scripts/markdown_to_wechat_html.py` to customize.

---

**MIT License • Open Source**
