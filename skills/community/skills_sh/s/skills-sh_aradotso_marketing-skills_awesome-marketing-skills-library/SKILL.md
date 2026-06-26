---
name: awesome-marketing-skills-library
description: AI agent skill library for generating premium marketing materials with aesthetic-first design using Sacred Drift principles
triggers:
  - "create a premium brochure using awesome marketing skills"
  - "generate a luxury marketing brochure with sacred drift aesthetic"
  - "use the brochure generator skill for this marketing campaign"
  - "design a high-fidelity marketing material with vibe design principles"
  - "make a WCAG compliant brochure for this product launch"
  - "build a premium PDF brochure with mathematical typography"
  - "create marketing collateral using the awesome marketing skills library"
  - "generate a mobile-optimized marketing brochure with research automation"
---

# Awesome Marketing Skills Library

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

A universal, high-fidelity library of AI Agent skills for generating premium marketing materials. This library follows the "Vibe Designing" philosophy using Sacred Drift aesthetics, mathematical precision, and contextual intelligence to create pixel-perfect marketing collateral.

## What It Does

Awesome Marketing Skills provides reusable skill modules that AI coding agents can execute to:

- Generate premium multi-page marketing brochures (PDF) with 1:1 aspect ratio
- Apply Sacred Drift design archetype (Cormorant Garamond + Jost typography)
- Ensure WCAG AAA compliance programmatically
- Automate research using Tavily and Firecrawl MCP servers
- Export high-resolution PDFs via Puppeteer automation
- Create contextually accurate marketing copy with local cultural awareness

## Installation

Clone into your project's `.agents/skills/` directory:

```bash
mkdir -p .agents/skills
cd .agents/skills
git clone https://github.com/plushyta/Awesome-Marketing-Skills.git awesome-marketing-skills
```

## MCP Server Requirements

The skills require these Model Context Protocol servers:

```json
{
  "mcpServers": {
    "tavily": {
      "command": "uvx",
      "args": ["mcp-server-tavily"],
      "env": { "TAVILY_API_KEY": "<YOUR_TAVILY_API_KEY>" }
    },
    "firecrawl": {
      "command": "uvx",
      "args": ["firecrawl-mcp"],
      "env": { "FIRECRAWL_API_KEY": "<YOUR_FIRECRAWL_API_KEY>" }
    },
    "stock-images": {
      "command": "uvx",
      "args": ["stock-images-mcp"],
      "env": { "PEXELS_API_KEY": "<YOUR_PEXELS_API_KEY>" }
    }
  }
}
```

Add this to your `mcp_config.json` or IDE-specific MCP configuration file.

## Active Skills

### Brochure Generator

Located at: `.agents/skills/awesome-marketing-skills/.agents/skills/brochure-generator/`

The flagship skill for creating premium marketing brochures.

**Triggering the Skill:**

Simply describe what you want in natural language:

```
"Create a premium 5-page brochure for a luxury yoga retreat in Rishikesh using the Sacred Drift theme"
```

```
"Design a high-end PDF brochure for my tech conference with WCAG AAA compliance"
```

**Key Features:**
- Sacred Drift typography (Cormorant Garamond + Jost)
- Automated research via MCP servers
- WCAG AAA contrast checking
- Mobile-optimized layouts (1:1 aspect)
- Puppeteer PDF export

## Code Examples

### Basic HTML Structure (Sacred Drift Pattern)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --font-serif: 'Cormorant Garamond', serif;
            --font-sans: 'Jost', sans-serif;
            --color-primary: #2C1810;
            --color-accent: #D4A574;
            --color-bg: #FAF8F3;
        }
        
        body {
            font-family: var(--font-sans);
            background: var(--color-bg);
            color: var(--color-primary);
            line-height: 1.75;
            margin: 0;
            padding: 0;
        }
        
        h1, h2, h3 {
            font-family: var(--font-serif);
            font-weight: 300;
            letter-spacing: 0.02em;
        }
        
        .page {
            width: 1080px;
            height: 1080px;
            position: relative;
            overflow: hidden;
            page-break-after: always;
        }
    </style>
</head>
<body>
    <div class="page">
        <h1>Sacred Drift Brochure</h1>
    </div>
</body>
</html>
```

### WCAG Contrast Checker (JavaScript)

```javascript
// Programmatic contrast ratio validation
function getContrastRatio(color1, color2) {
    const getLuminance = (color) => {
        const rgb = color.match(/\d+/g).map(Number);
        const [r, g, b] = rgb.map(val => {
            val = val / 255;
            return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
        });
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    };
    
    const lum1 = getLuminance(color1);
    const lum2 = getLuminance(color2);
    const brightest = Math.max(lum1, lum2);
    const darkest = Math.min(lum1, lum2);
    
    return (brightest + 0.05) / (darkest + 0.05);
}

// Check WCAG AAA compliance (7:1 for normal text)
const ratio = getContrastRatio('rgb(44, 24, 16)', 'rgb(250, 248, 243)');
if (ratio >= 7) {
    console.log('✓ WCAG AAA Compliant');
} else {
    console.log('✗ Contrast ratio insufficient:', ratio);
}
```

### Puppeteer PDF Export

```javascript
const puppeteer = require('puppeteer');

async function exportBrochureToPDF(htmlPath, outputPath) {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setViewport({ width: 1080, height: 1080 });
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });
    
    await page.pdf({
        path: outputPath,
        format: 'A4',
        printBackground: true,
        preferCSSPageSize: true,
        margin: { top: 0, right: 0, bottom: 0, left: 0 }
    });
    
    await browser.close();
    console.log(`✓ PDF exported to ${outputPath}`);
}

// Usage
exportBrochureToPDF(
    './brochure.html',
    './output/Premium_Brochure.pdf'
);
```

### MCP Server Integration Pattern

```javascript
// Using Tavily for research (via MCP)
async function researchLocation(location) {
    // MCP server handles API calls automatically
    const query = `cultural significance and attractions of ${location}`;
    
    // Agent will route through configured Tavily MCP
    const results = await tavily.search({
        query: query,
        search_depth: 'advanced',
        max_results: 5
    });
    
    return results;
}

// Using Stock Images MCP for contextual imagery
async function fetchContextualImage(theme, orientation = 'landscape') {
    const results = await stockImages.search({
        query: theme,
        orientation: orientation,
        size: 'large',
        per_page: 3
    });
    
    return results[0].src.large2x;
}
```

## Configuration

### IDE-Specific Setup

**Claude Code / Cursor / Windsurf:**

The agent automatically discovers skills in `.agents/skills/`. No additional configuration needed.

**GitHub Copilot:**

Add to `.github/copilot-instructions.md`:

```markdown
## Custom Skills

Check `.agents/skills/awesome-marketing-skills/` for marketing design skills.
Use Sacred Drift aesthetic principles for all brochure generation tasks.
```

**Codex CLI:**

```bash
codex run .agents/skills/awesome-marketing-skills/.agents/skills/brochure-generator
```

## Common Patterns

### Sacred Drift Color Palette

```css
:root {
    /* Primary Palette */
    --sacred-drift-charcoal: #2C1810;
    --sacred-drift-cream: #FAF8F3;
    --sacred-drift-gold: #D4A574;
    --sacred-drift-sage: #9CAA9C;
    
    /* Overlay Gradients */
    --overlay-dark: linear-gradient(135deg, rgba(44,24,16,0.85), rgba(44,24,16,0.65));
    --overlay-light: linear-gradient(135deg, rgba(250,248,243,0.95), rgba(250,248,243,0.85));
}
```

### Vertical Rhythm System

```css
/* Mathematical line-height system */
.rhythm-small { line-height: 1.5; }    /* 24px base */
.rhythm-medium { line-height: 1.75; }  /* 28px base */
.rhythm-large { line-height: 2.0; }    /* 32px base */

/* Spacing scale (based on 8px grid) */
.spacing-xs { margin-bottom: 8px; }
.spacing-sm { margin-bottom: 16px; }
.spacing-md { margin-bottom: 24px; }
.spacing-lg { margin-bottom: 40px; }
.spacing-xl { margin-bottom: 64px; }
```

## Troubleshooting

### MCP Servers Not Found

**Error:** `MCP server 'tavily' not configured`

**Solution:**
```bash
# Install MCP servers
uvx mcp-server-tavily
uvx firecrawl-mcp
uvx stock-images-mcp

# Verify API keys are set
echo $TAVILY_API_KEY
echo $FIRECRAWL_API_KEY
echo $PEXELS_API_KEY
```

### PDF Export Issues

**Error:** `Failed to launch browser`

**Solution:**
```bash
# Install Chromium dependencies
sudo apt-get install -y chromium-browser

# Or use system Chrome
const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome',
    headless: true
});
```

### Font Loading Failures

**Error:** `Google Fonts not loading in PDF`

**Solution:**
```javascript
// Add delay for font loading
await page.goto(htmlPath, { waitUntil: 'networkidle0' });
await page.evaluateHandle('document.fonts.ready');
await page.waitForTimeout(1000); // Extra safety buffer
```

### WCAG Compliance Failures

**Error:** `Contrast ratio below 7:1`

**Solution:**
```javascript
// Darken text or lighten background
const improveContrast = (textColor, bgColor) => {
    let ratio = getContrastRatio(textColor, bgColor);
    
    // Darken text incrementally
    while (ratio < 7) {
        textColor = darkenColor(textColor, 0.05);
        ratio = getContrastRatio(textColor, bgColor);
    }
    
    return textColor;
};
```

## Directory Structure

```
.agents/skills/awesome-marketing-skills/
├── .agents/skills/
│   └── brochure-generator/
│       ├── SKILL.md              # Skill instructions
│       ├── templates/            # HTML/CSS templates
│       └── examples/             # Example outputs
├── image.png                     # Banner
├── README.md                     # Main documentation
└── LICENSE
```

## Contributing New Skills

To add a new skill to this library:

1. Create a new directory in `.agents/skills/`
2. Add a `SKILL.md` with frontmatter (name, description, triggers)
3. Include example code and templates
4. Update main README.md with skill entry
5. Follow Sacred Drift design principles

## Example Workflow

```javascript
// Complete brochure generation workflow
async function generatePremiumBrochure(config) {
    const { title, theme, location, pages } = config;
    
    // Step 1: Research
    const research = await researchLocation(location);
    
    // Step 2: Fetch imagery
    const heroImage = await fetchContextualImage(theme);
    
    // Step 3: Generate HTML
    const html = generateBrochureHTML({
        title,
        research,
        heroImage,
        pages,
        typography: 'sacred-drift',
        palette: 'warm-earth'
    });
    
    // Step 4: Validate WCAG
    const isCompliant = validateWCAG(html);
    if (!isCompliant) throw new Error('Contrast compliance failed');
    
    // Step 5: Export PDF
    await exportBrochureToPDF(html, `./output/${title}.pdf`);
    
    return { success: true, path: `./output/${title}.pdf` };
}

// Usage
await generatePremiumBrochure({
    title: 'Yog Yatra Retreat',
    theme: 'spiritual wellness yoga',
    location: 'Rishikesh, India',
    pages: 5
});
```
