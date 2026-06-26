/**
 * 字体缩放系统
 * 基于视频实际渲染高度自动缩放字体
 * 基准：1080×1920（竖屏 9:16）
 */

import { useVideoConfig } from "remotion";

export const BASE_HEIGHT = 1920;
export const BASE_WIDTH = 1080;

/**
 * 基准字号（竖屏 1080×1920 设计）
 */
export const BASE_FONT_SIZES = {
  hero: 180,
  h1: 120,
  h2: 96,
  body: 90,
  caption: 60,
  subtitle: 45,
  tiny: 30,
} as const;

export const COLORS = {
  primary: "#00d4ff",
  background: "#0a0e17",
  card: "#111827",
  text: "#ffffff",
  muted: "#888888",
  faint: "#444444",
  accent: "#ffd93d",
  error: "#ff4d4d",
  success: "#00ff88",
} as const;

/**
 * 获取当前视频的缩放因子（基于高度）
 * 在组件顶层调用一次，所有字号复用
 */
export function useFontScale(): number {
  const { height } = useVideoConfig();
  return height / BASE_HEIGHT;
}

/**
 * 获取指定 key 的基准字号（自动按当前视频高度缩放）
 * 用法：fontSize={getFontSize("body")}
 */
export function getFontSize(key: keyof typeof BASE_FONT_SIZES): number {
  const { height } = useVideoConfig();
  return Math.round(BASE_FONT_SIZES[key] * (height / BASE_HEIGHT));
}

/**
 * 缩放任意字号
 * 用法：fontSize={scale(72)}
 * 必须在 React 组件内调用（依赖 useVideoConfig）
 */
export function scale(designSize: number): number {
  const { height } = useVideoConfig();
  return Math.round(designSize * (height / BASE_HEIGHT));
}

/** @deprecated 用 scale() 代替 */
export const scaleFontSize = scale;

export function getLineHeight(key: keyof typeof BASE_FONT_SIZES): number {
  const { height } = useVideoConfig();
  const ratios = { hero: 1.2, h1: 1.25, h2: 1.3, body: 1.6, caption: 1.5, subtitle: 1.4, tiny: 1.3 };
  return Math.round(BASE_FONT_SIZES[key] * (height / BASE_HEIGHT) * (ratios[key] ?? 1.5));
}
