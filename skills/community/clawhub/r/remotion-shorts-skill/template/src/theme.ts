import type { FontName, Theme } from "./types";

export const WIDTH = 1080;
export const HEIGHT = 1920;

/**
 * Area that no app button, caption or progress bar covers on TikTok, Reels
 * and Shorts: the strictest edge of the three (top and right from YouTube
 * Shorts, bottom and left from Meta's Reels guidance). Text never leaves it.
 */
export const SAFE = { top: 288, bottom: 672, left: 96, right: 192 };
export const SAFE_W = WIDTH - SAFE.left - SAFE.right;
export const SAFE_H = HEIGHT - SAFE.top - SAFE.bottom;
/** Centred text uses the right margin on both sides, so it sits on the true centre line of the frame. */
export const CENTER_W = WIDTH - 2 * SAFE.right;
/** Left-aligned text starts this far inside the safe box (room for the emphasis punch). */
export const LEFT_INSET = 24;
export const LEFT_W = SAFE_W - LEFT_INSET;

export const THEMES: Record<string, Theme> = {
  ink: { bg: "#0E0E10", fg: "#F5F5F2", accent: "#FFD23F", accentText: "#0E0E10", font: "Anton", uppercase: true },
  paper: { bg: "#F3EEE4", fg: "#151515", accent: "#E63946", accentText: "#FFFFFF", font: "Poppins", uppercase: false },
  volt: { bg: "#111418", fg: "#FFFFFF", accent: "#C8FF2E", accentText: "#111418", font: "Anton", uppercase: true },
  ocean: { bg: "#0A2540", fg: "#FFFFFF", accent: "#3DD6F5", accentText: "#0A2540", font: "Poppins", uppercase: false },
  clean: { bg: "#FFFFFF", fg: "#111111", accent: "#2F5BFF", accentText: "#FFFFFF", font: "Inter", uppercase: false },
};

export const FONTS: Record<FontName, { family: string; file: string; weight: string; lineHeight: number }> = {
  Anton: { family: "Anton", file: "fonts/Anton-Regular.ttf", weight: "400", lineHeight: 1.08 },
  Poppins: { family: "Poppins", file: "fonts/Poppins-ExtraBold.ttf", weight: "800", lineHeight: 1.12 },
  Inter: { family: "Inter", file: "fonts/Inter.ttf", weight: "800", lineHeight: 1.12 },
};

/** Second font for small lines (labels, author, footer). */
export const SMALL = { family: "Poppins", file: "fonts/Poppins-Bold.ttf", weight: "700", lineHeight: 1.2 };

export const resolveTheme = (theme: string | Partial<Theme> | undefined, font?: FontName): Theme => {
  let base = THEMES.ink;
  let custom: Partial<Theme> = {};
  if (typeof theme === "string") {
    if (!THEMES[theme]) throw new Error(`Unknown theme "${theme}". Use one of: ${Object.keys(THEMES).join(", ")}, or an object.`);
    base = THEMES[theme];
  } else if (theme) {
    custom = theme;
  }
  const merged = { ...base, ...custom };
  if (font) merged.font = font;
  if (!FONTS[merged.font]) throw new Error(`Unknown font "${merged.font}". Use Anton, Poppins or Inter.`);
  return merged;
};
