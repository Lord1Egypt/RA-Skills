/**
 * SeedFlip MCP — Export Generators
 *
 * Produces ready-to-use config files directly from DesignSeed data.
 * All colors are already hex — no conversion needed.
 */

import type { DesignSeed } from './search.js';

// ── Helpers ──────────────────────────────────────────────────────

function fontFamily(name: string): string {
  const mono =
    name.toLowerCase().includes('mono') ||
    ['JetBrains Mono', 'Fira Code', 'IBM Plex Mono', 'Iosevka'].includes(name);
  const serif = [
    'Playfair Display', 'DM Serif Display', 'Fraunces', 'Lora',
    'Merriweather', 'Source Serif 4', 'Crimson Text', 'EB Garamond',
    'Cormorant Garamond', 'Libre Baskerville', 'Bespoke Serif',
    'Bonny', 'Boska', 'Erode', 'Gambetta', 'Neco', 'Recia',
    'Rowan', 'Sentient', 'Zodiak', 'Bitter', 'Spectral',
    'Instrument Serif', 'Noto Serif Display',
  ].includes(name);
  const fallback = mono ? 'monospace' : serif ? 'serif' : 'sans-serif';
  return `'${name}', ${fallback}`;
}

function googleFontsUrl(seed: DesignSeed): string {
  const fonts = new Set([seed.headingFont, seed.bodyFont]);
  const families = [...fonts].map((f) => {
    const weights =
      f === seed.headingFont ? `wght@${seed.headingWeight}` : 'wght@400;500';
    return `family=${f.replace(/ /g, '+')}:${weights}`;
  });
  return `https://fonts.googleapis.com/css2?${families.join('&')}&display=swap`;
}

function hexToHSLString(hex: string): string {
  const c = hex.replace('#', '');
  const r = parseInt(c.slice(0, 2), 16) / 255;
  const g = parseInt(c.slice(2, 4), 16) / 255;
  const b = parseInt(c.slice(4, 6), 16) / 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const l = (max + min) / 2;
  if (max === min) return `0 0% ${Math.round(l * 100)}%`;
  const d = max - min;
  const s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
  let h = 0;
  if (max === r) h = ((g - b) / d + (g < b ? 6 : 0)) / 6;
  else if (max === g) h = ((b - r) / d + 2) / 6;
  else h = ((r - g) / d + 4) / 6;
  return `${(h * 360).toFixed(1)} ${(s * 100).toFixed(1)}% ${(l * 100).toFixed(1)}%`;
}

function hexLuminance(hex: string): number {
  const c = hex.replace('#', '');
  const r = parseInt(c.substring(0, 2), 16);
  const g = parseInt(c.substring(2, 4), 16);
  const b = parseInt(c.substring(4, 6), 16);
  return (0.299 * r + 0.587 * g + 0.114 * b) / 255;
}

// ── Token summary (default format) ──────────────────────────────

export function formatTokens(seed: DesignSeed): string {
  const isDark = hexLuminance(seed.bg) < 0.5;
  return `## SeedFlip — ${seed.name}

**${seed.vibe}**
Mode: ${isDark ? 'Dark' : 'Light'} | Tags: ${seed.tags.join(', ')}

### Fonts
- Heading: ${seed.headingFont} (weight: ${seed.headingWeight}, spacing: ${seed.letterSpacing})
- Body: ${seed.bodyFont}
- CSS: font-family: ${fontFamily(seed.headingFont)}
- Import: ${googleFontsUrl(seed)}

### Colors
| Token | Value |
|-------|-------|
| Background | ${seed.bg} |
| Surface | ${seed.surface} |
| Surface Hover | ${seed.surfaceHover} |
| Border | ${seed.border} |
| Text | ${seed.text} |
| Text Muted | ${seed.textMuted} |
| Accent | ${seed.accent} |
| Accent Soft | ${seed.accentSoft} |

### Shape
- Border Radius: ${seed.radius} (sm: ${seed.radiusSm}, xl: ${seed.radiusXl})
- Shadow: ${seed.shadow}
- Shadow Style: ${seed.shadowStyle}
- Gradient: ${seed.gradient}

### Design Brief
${seed.aiPromptRules}

#### Typography Notes
${seed.aiPromptTypography}

#### Color Notes
${seed.aiPromptColors}

#### Shape Notes
${seed.aiPromptShape}

#### Depth Notes
${seed.aiPromptDepth}`;
}

// ── Tailwind config ─────────────────────────────────────────────

export function formatTailwind(seed: DesignSeed): string {
  const headingFallback = fontFamily(seed.headingFont).split(', ')[1];
  const bodyFallback = fontFamily(seed.bodyFont).split(', ')[1];

  return `// SeedFlip — ${seed.name}
// ${seed.vibe}
// https://seedflip.com

import type { Config } from "tailwindcss";

export default {
  theme: {
    extend: {
      colors: {
        background: "${seed.bg}",
        surface: "${seed.surface}",
        "surface-hover": "${seed.surfaceHover}",
        border: "${seed.border}",
        foreground: "${seed.text}",
        muted: "${seed.textMuted}",
        accent: "${seed.accent}",
        "accent-soft": "${seed.accentSoft}",
      },
      borderRadius: {
        DEFAULT: "${seed.radius}",
        sm: "${seed.radiusSm}",
        xl: "${seed.radiusXl}",
      },
      fontFamily: {
        heading: ["${seed.headingFont}", "${headingFallback}"],
        body: ["${seed.bodyFont}", "${bodyFallback}"],
      },
      boxShadow: {
        DEFAULT: "${seed.shadow}",
        sm: "${seed.shadowSm}",
      },
    },
  },
} satisfies Config;

/*
  Font import — add to your layout or globals.css:
  @import url('${googleFontsUrl(seed)}');

  Design brief:
  ${seed.aiPromptRules}
*/`;
}

// ── CSS custom properties ───────────────────────────────────────

export function formatCSS(seed: DesignSeed): string {
  return `/* SeedFlip — ${seed.name} */
/* ${seed.vibe} */
@import url('${googleFontsUrl(seed)}');

:root {
  /* Colors */
  --sf-bg: ${seed.bg};
  --sf-surface: ${seed.surface};
  --sf-surface-hover: ${seed.surfaceHover};
  --sf-border: ${seed.border};
  --sf-text: ${seed.text};
  --sf-text-muted: ${seed.textMuted};
  --sf-accent: ${seed.accent};
  --sf-accent-soft: ${seed.accentSoft};

  /* Typography */
  --sf-font-heading: ${fontFamily(seed.headingFont)};
  --sf-font-body: ${fontFamily(seed.bodyFont)};
  --sf-heading-weight: ${seed.headingWeight};
  --sf-letter-spacing: ${seed.letterSpacing};

  /* Shape */
  --sf-radius: ${seed.radius};
  --sf-radius-sm: ${seed.radiusSm};
  --sf-radius-xl: ${seed.radiusXl};

  /* Depth */
  --sf-shadow: ${seed.shadow};
  --sf-shadow-sm: ${seed.shadowSm};
  --sf-gradient: ${seed.gradient};
}

/*
  Design brief:
  ${seed.aiPromptRules}
*/`;
}

// ── OpenClaw dashboard theme ────────────────────────────────────

export function formatOpenClaw(seed: DesignSeed): string {
  const isDark = hexLuminance(seed.bg) < 0.5;
  const headingFF = fontFamily(seed.headingFont);
  const bodyFF = fontFamily(seed.bodyFont);

  // Derive shadow scale from seed's shadow tokens
  const shadowSm = seed.shadowSm;
  const shadowMd = seed.shadow;
  // Scale up for lg/xl
  const shadowLg = shadowMd.replace(/(\d+)px/g, (_, n) => `${Math.round(Number(n) * 1.5)}px`);
  const shadowXl = shadowMd.replace(/(\d+)px/g, (_, n) => `${Math.round(Number(n) * 2.5)}px`);

  // Derive radius scale
  const rSm = seed.radiusSm;
  const rMd = seed.radius;
  const rLg = seed.radiusXl;
  const rXl = `${Math.round(parseFloat(seed.radiusXl) * 1.5)}px`;

  const cssBlock = `:root {
  /* SeedFlip — ${seed.name} */
  /* ${seed.vibe} */

  /* Colors */
  --bg: ${seed.bg};
  --card: ${seed.surface};
  --bg-elevated: ${seed.surfaceHover};
  --accent: ${seed.accent};
  --primary: ${seed.accent};
  --text: ${seed.text};
  --text-secondary: ${seed.textMuted};
  --muted: ${seed.textMuted};
  --border: ${seed.border};

  /* Typography */
  --font-body: ${bodyFF};
  --font-heading: ${headingFF};
  --mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Shape */
  --radius-sm: ${rSm};
  --radius-md: ${rMd};
  --radius-lg: ${rLg};
  --radius-xl: ${rXl};

  /* Depth */
  --shadow-sm: ${shadowSm};
  --shadow-md: ${shadowMd};
  --shadow-lg: ${shadowLg};
  --shadow-xl: ${shadowXl};
}`;

  const themeJson = JSON.stringify(
    {
      name: seed.name,
      vibe: seed.vibe,
      mode: isDark ? 'dark' : 'light',
      bg: seed.bg,
      card: seed.surface,
      'bg-elevated': seed.surfaceHover,
      accent: seed.accent,
      primary: seed.accent,
      text: seed.text,
      'text-secondary': seed.textMuted,
      muted: seed.textMuted,
      border: seed.border,
      'font-body': bodyFF,
      'font-heading': headingFF,
      'radius-sm': rSm,
      'radius-md': rMd,
      'radius-lg': rLg,
      'radius-xl': rXl,
      'shadow-sm': shadowSm,
      'shadow-md': shadowMd,
      'shadow-lg': shadowLg,
      'shadow-xl': shadowXl,
    },
    null,
    2
  );

  return `## SeedFlip — ${seed.name} (OpenClaw Theme)

**${seed.vibe}**
Mode: ${isDark ? 'Dark' : 'Light'} | Tags: ${seed.tags.join(', ')}

### CSS Variables — paste into your OpenClaw dashboard

\`\`\`css
@import url('${googleFontsUrl(seed)}');

${cssBlock}
\`\`\`

### themes.json entry

\`\`\`json
${themeJson}
\`\`\`

### Quick inject (browser console)

\`\`\`js
// Paste this into your browser console to preview the theme instantly
const s = document.documentElement.style;
s.setProperty('--bg', '${seed.bg}');
s.setProperty('--card', '${seed.surface}');
s.setProperty('--bg-elevated', '${seed.surfaceHover}');
s.setProperty('--accent', '${seed.accent}');
s.setProperty('--primary', '${seed.accent}');
s.setProperty('--text', '${seed.text}');
s.setProperty('--text-secondary', '${seed.textMuted}');
s.setProperty('--muted', '${seed.textMuted}');
s.setProperty('--border', '${seed.border}');
s.setProperty('--font-body', "${bodyFF}");
s.setProperty('--font-heading', "${headingFF}");
s.setProperty('--radius-sm', '${rSm}');
s.setProperty('--radius-md', '${rMd}');
s.setProperty('--radius-lg', '${rLg}');
s.setProperty('--radius-xl', '${rXl}');
s.setProperty('--shadow-sm', '${shadowSm}');
s.setProperty('--shadow-md', '${shadowMd}');
document.body.style.background = '${seed.bg}';
document.body.style.color = '${seed.text}';
\`\`\`

### Design Brief
${seed.aiPromptRules}`;
}

// ── shadcn/ui theme ─────────────────────────────────────────────

export function formatShadcn(seed: DesignSeed): string {
  const bg = hexToHSLString(seed.bg);
  const surface = hexToHSLString(seed.surface);
  const text = hexToHSLString(seed.text);
  const textMuted = hexToHSLString(seed.textMuted);
  const accent = hexToHSLString(seed.accent);
  const border = hexToHSLString(seed.border);
  const primaryFg = hexLuminance(seed.accent) > 0.5 ? '0 0% 9%' : '0 0% 98%';
  const accentFg = hexLuminance(seed.surface) > 0.5 ? '0 0% 9%' : '0 0% 98%';
  const radiusRem =
    (parseFloat(seed.radius) / 16).toFixed(3).replace(/0+$/, '').replace(/\.$/, '') + 'rem';

  return `/* SeedFlip — ${seed.name} — shadcn/ui theme */
/* ${seed.vibe} */
@import url('${googleFontsUrl(seed)}');

@layer base {
  :root {
    --background: ${bg};
    --foreground: ${text};
    --card: ${surface};
    --card-foreground: ${text};
    --popover: ${surface};
    --popover-foreground: ${text};
    --primary: ${accent};
    --primary-foreground: ${primaryFg};
    --secondary: ${surface};
    --secondary-foreground: ${textMuted};
    --muted: ${surface};
    --muted-foreground: ${textMuted};
    --accent: ${surface};
    --accent-foreground: ${accentFg};
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: ${border};
    --input: ${border};
    --ring: ${accent};
    --radius: ${radiusRem};
    --font-heading: '${seed.headingFont}', sans-serif;
    --font-body: '${seed.bodyFont}', sans-serif;
  }
}

/*
  Design brief:
  ${seed.aiPromptRules}
*/`;
}
