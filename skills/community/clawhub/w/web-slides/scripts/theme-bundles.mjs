export const THEMES = {
  "cyber-grid": {
    scenes: ["ai-product-launch", "cloud-platform", "industry-keynote"],
    layouts: ["cover", "section-break", "insight", "metrics", "chart-focus", "closing"],
    tone: "future-tech",
    engine: "reveal",
    density: ["medium"],
    mobileScore: 3,
  },
  "executive-dark": {
    scenes: ["board-review", "strategy-review", "annual-summary"],
    layouts: ["cover", "agenda", "insight", "comparison", "metrics", "closing"],
    tone: "premium-formal",
    engine: "reveal",
    density: ["medium", "heavy"],
    mobileScore: 3,
  },
  "executive-light": {
    scenes: ["consulting-proposal", "client-update", "project-report"],
    layouts: ["cover", "agenda", "two-column", "insight", "chart-focus", "closing"],
    tone: "clean-business",
    engine: "reveal",
    density: ["medium", "heavy"],
    mobileScore: 5,
  },
  "glass-future": {
    scenes: ["aigc-solution", "innovation-lab", "concept-showcase"],
    layouts: ["cover", "section-break", "two-column", "quote", "insight", "closing"],
    tone: "soft-futuristic",
    engine: "reveal",
    density: ["light", "medium"],
    mobileScore: 3,
  },
  "data-intelligence": {
    scenes: ["bi-report", "growth-review", "operations-analysis"],
    layouts: ["cover", "agenda", "metrics", "chart-focus", "timeline", "closing"],
    tone: "data-driven",
    engine: "reveal",
    density: ["medium", "heavy"],
    mobileScore: 5,
  },
  "startup-pitch": {
    scenes: ["investor-pitch", "fundraising", "startup-story"],
    layouts: ["cover", "insight", "two-column", "metrics", "timeline", "closing"],
    tone: "aggressive-growth",
    engine: "reveal",
    density: ["light", "medium"],
    mobileScore: 4,
  },
  "product-launch": {
    scenes: ["new-product-launch", "feature-release", "roadmap-launch"],
    layouts: ["cover", "section-break", "insight", "timeline", "quote", "closing"],
    tone: "stage-product",
    engine: "reveal",
    density: ["light", "medium"],
    mobileScore: 3,
  },
  "dev-summit": {
    scenes: ["tech-talk", "architecture-sharing", "developer-conference"],
    layouts: ["cover", "agenda", "insight", "two-column", "chart-focus", "closing"],
    tone: "engineering-trust",
    engine: "reveal",
    density: ["medium", "heavy"],
    mobileScore: 4,
  },
  "luxury-black-gold": {
    scenes: ["premium-brand-launch", "vip-presentation", "executive-event"],
    layouts: ["cover", "quote", "insight", "metrics", "closing"],
    tone: "luxury-ceremony",
    engine: "reveal",
    density: ["light"],
    mobileScore: 2,
  },
  "editorial-serif": {
    scenes: ["whitepaper", "research-report", "education-deck"],
    layouts: ["cover", "agenda", "insight", "two-column", "quote", "closing"],
    tone: "editorial-knowledge",
    engine: "reveal",
    density: ["medium", "heavy"],
    mobileScore: 3,
  },
  "neo-minimal": {
    scenes: ["design-proposal", "brand-refresh", "minimal-briefing"],
    layouts: ["cover", "insight", "comparison", "two-column", "closing"],
    tone: "minimal-premium",
    engine: "reveal",
    density: ["light", "medium"],
    mobileScore: 5,
  },
  "creative-motion": {
    scenes: ["campaign-proposal", "creative-pitch", "event-showcase"],
    layouts: ["cover", "section-break", "quote", "timeline", "insight", "closing"],
    tone: "energetic-creative",
    engine: "reveal",
    density: ["light", "medium"],
    mobileScore: 2,
  },
};

export const SCENE_ALIASES = {
  "ai-launch": "ai-product-launch",
  "product-launch": "new-product-launch",
  "pitch": "investor-pitch",
  "board": "board-review",
  "report": "project-report",
  "tech-share": "tech-talk",
};

export const DEFAULT_DECK_LENGTH = {
  light: 8,
  medium: 10,
  heavy: 14,
};

export function normalizeScene(scene = "") {
  return SCENE_ALIASES[scene] ?? scene;
}

export function listThemes() {
  return Object.keys(THEMES).sort();
}

export function getTheme(name) {
  return THEMES[name] ?? null;
}

export function findThemeByScene(scene) {
  const normalized = normalizeScene(scene);
  for (const [name, theme] of Object.entries(THEMES)) {
    if (theme.scenes.includes(normalized)) {
      return { name, ...theme };
    }
  }
  return null;
}

export function scoreTheme({ scene, density = "medium", mobile = false, themeName }) {
  const theme = getTheme(themeName);
  if (!theme) return -1;

  let score = 0;
  const normalized = normalizeScene(scene);

  if (normalized && theme.scenes.includes(normalized)) score += 5;
  if (theme.density.includes(density)) score += 2;
  if (mobile) score += theme.mobileScore;

  return score;
}

export function recommendTheme({ scene, density = "medium", mobile = false }) {
  const candidates = listThemes()
    .map((themeName) => ({
      themeName,
      score: scoreTheme({ scene, density, mobile, themeName }),
      ...getTheme(themeName),
    }))
    .sort((a, b) => b.score - a.score);

  return candidates[0] ?? null;
}
