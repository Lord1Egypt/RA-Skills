/**
 * SeedFlip MCP — Search Engine
 *
 * Scores seeds against a natural language query.
 * Handles brand references ("Stripe"), vibes ("dark minimal"),
 * and style descriptors ("brutalist", "warm editorial").
 */

// DesignSeed type — matches the seed objects in seeds-data.json
interface DesignSeed {
  name: string;
  fakeUrl: string;
  vibe: string;
  tags: string[];
  headingFont: string;
  bodyFont: string;
  headingWeight: number;
  letterSpacing: string;
  bg: string;
  surface: string;
  surfaceHover: string;
  border: string;
  text: string;
  textMuted: string;
  accent: string;
  accentSoft: string;
  radius: string;
  radiusSm: string;
  radiusXl: string;
  shadow: string;
  shadowSm: string;
  shadowStyle: string;
  gradient: string;
  aiPromptTypography: string;
  aiPromptColors: string;
  aiPromptShape: string;
  aiPromptDepth: string;
  aiPromptRules: string;
  collection?: string;
}

export type { DesignSeed };

// ── Brand reference map ──────────────────────────────────────────
// Maps common queries to the brand names that appear in aiPromptRules.
// An agent saying "make it look like Stripe" triggers a search for "Stripe"
// in the seed's AI prompts.

const BRAND_ALIASES: Record<string, string[]> = {
  stripe: ['stripe', 'fintech'],
  vercel: ['vercel'],
  linear: ['linear purple', 'linear\'s'],
  github: ['github'],
  notion: ['notion'],
  supabase: ['supabase'],
  spotify: ['spotify'],
  framer: ['framer'],
  resend: ['resend'],
  superhuman: ['superhuman'],
  raycast: ['raycast'],
  arc: ['arc browser'],
  railway: ['railway'],
  tailwind: ['tailwind css', 'tailwind'],
  atlassian: ['atlassian', 'jira', 'confluence'],
  phantom: ['phantom wallet'],
};

// Some brand names collide with CSS terms (e.g. "linear" in "linear-gradient").
// For these, we use phrase-level matching instead of single-word boundaries.
// The aliases above are already configured to avoid false positives.

// ── Style synonyms ───────────────────────────────────────────────
// Maps natural language to tag values that exist on seeds.

const STYLE_SYNONYMS: Record<string, string[]> = {
  minimal: ['minimal', 'clean', 'precise'],
  minimalist: ['minimal', 'clean', 'precise'],
  clean: ['clean', 'minimal'],
  bold: ['bold', 'brutalist'],
  brutalist: ['brutalist', 'bold'],
  warm: ['warm', 'elegant'],
  elegant: ['elegant', 'warm'],
  editorial: ['editorial'],
  neon: ['neon', 'cyberpunk', 'vibrant'],
  cyberpunk: ['cyberpunk', 'neon'],
  retro: ['retro', 'vintage', 'nostalgic'],
  playful: ['playful', 'vibrant', 'rounded'],
  professional: ['professional', 'spacious', 'clean'],
  luxury: ['luxury', 'elegant', 'premium'],
  premium: ['premium', 'elegant', 'luxury'],
  developer: ['developer', 'precise', 'mono'],
  dev: ['developer', 'precise', 'mono'],
  modern: ['modern', 'clean', 'cool'],
  geometric: ['geometric', 'bold'],
  organic: ['organic', 'natural', 'warm'],
  nature: ['organic', 'natural', 'warm'],
  industrial: ['industrial', 'bold'],
};

// ── Luminance helper ─────────────────────────────────────────────

function isDark(bg: string): boolean {
  const hex = bg.replace('#', '');
  const r = parseInt(hex.substring(0, 2), 16);
  const g = parseInt(hex.substring(2, 4), 16);
  const b = parseInt(hex.substring(4, 6), 16);
  return (0.299 * r + 0.587 * g + 0.114 * b) / 255 < 0.5;
}

// ── Tokenizer ────────────────────────────────────────────────────

function tokenize(query: string): string[] {
  return query
    .toLowerCase()
    .replace(/[^a-z0-9\s#]/g, ' ')
    .split(/\s+/)
    .filter(Boolean);
}

// ── Scorer ───────────────────────────────────────────────────────

export interface ScoredSeed {
  seed: DesignSeed;
  score: number;
  matchReasons: string[];
}

export function searchSeeds(seeds: DesignSeed[], query: string): ScoredSeed[] {
  const tokens = tokenize(query);
  if (tokens.length === 0) {
    // No query — return a random seed
    const idx = Math.floor(Math.random() * seeds.length);
    return [{ seed: seeds[idx], score: 1, matchReasons: ['random'] }];
  }

  // Detect dark/light preference from query
  const wantsDark = tokens.includes('dark');
  const wantsLight = tokens.includes('light');

  const scored: ScoredSeed[] = seeds.map((seed) => {
    let score = 0;
    const reasons: string[] = [];
    const allPrompts = [
      seed.aiPromptRules,
      seed.aiPromptColors,
      seed.aiPromptTypography,
      seed.aiPromptShape,
      seed.aiPromptDepth,
    ]
      .filter(Boolean)
      .join(' ')
      .toLowerCase();
    const seedIsDark = isDark(seed.bg);

    // 1. Exact name match (highest signal — agent asked for a specific seed)
    const nameLower = seed.name.toLowerCase();
    for (const token of tokens) {
      if (nameLower === token || nameLower.includes(token)) {
        score += 25;
        reasons.push(`name: "${seed.name}"`);
      }
    }

    // 2. Brand reference in AI prompts (word boundary match)
    for (const token of tokens) {
      const brandAliases = BRAND_ALIASES[token];
      if (brandAliases) {
        for (const alias of brandAliases) {
          // Use word boundary regex to avoid "stripes" matching "stripe"
          const pattern = new RegExp(`\\b${alias.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i');
          if (pattern.test(allPrompts)) {
            score += 20;
            reasons.push(`brand: "${token}"`);
            break;
          }
        }
      }
    }

    // 3. Tag matches
    const seedTags = seed.tags.map((t) => t.toLowerCase());
    for (const token of tokens) {
      if (seedTags.includes(token)) {
        score += 10;
        reasons.push(`tag: "${token}"`);
      }
      // Also check style synonyms
      const synonyms = STYLE_SYNONYMS[token];
      if (synonyms) {
        for (const syn of synonyms) {
          if (seedTags.includes(syn)) {
            score += 6;
            reasons.push(`style: "${token}" → "${syn}"`);
            break;
          }
        }
      }
    }

    // 4. Dark/light preference
    if (wantsDark && seedIsDark) {
      score += 8;
      reasons.push('dark mode');
    } else if (wantsLight && !seedIsDark) {
      score += 8;
      reasons.push('light mode');
    } else if (wantsDark && !seedIsDark) {
      score -= 15; // Strong penalty for wrong mode
    } else if (wantsLight && seedIsDark) {
      score -= 15;
    }

    // 5. Vibe text match
    const vibeLower = seed.vibe.toLowerCase();
    for (const token of tokens) {
      if (vibeLower.includes(token)) {
        score += 5;
        reasons.push(`vibe: "${seed.vibe}"`);
      }
    }

    // 6. Font match
    const fontsLower = `${seed.headingFont} ${seed.bodyFont}`.toLowerCase();
    for (const token of tokens) {
      if (fontsLower.includes(token)) {
        score += 5;
        reasons.push(`font: "${token}"`);
      }
    }

    // 7. General keyword in AI prompts (weak signal but catches everything)
    for (const token of tokens) {
      if (
        token.length >= 4 &&
        !BRAND_ALIASES[token] &&
        !STYLE_SYNONYMS[token] &&
        token !== 'dark' &&
        token !== 'light' &&
        allPrompts.includes(token)
      ) {
        score += 3;
        reasons.push(`keyword: "${token}"`);
      }
    }

    return { seed, score, matchReasons: [...new Set(reasons)] };
  });

  return scored.filter((s) => s.score > 0).sort((a, b) => b.score - a.score);
}
