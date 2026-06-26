/**
 * 字体缩放系统
 * 基准：1080×1920（竖屏 9:16）
 */

import { useVideoConfig } from "remotion";

export const BASE_HEIGHT = 1920;
export const BASE_WIDTH = 1080;

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
 * 缩放因子（供组件顶层调用）
 * 用法：const scale = useFontScale() // 在组件顶层
 *       fontSize={Math.round(72 * scale)}
 */
export function useFontScale(): number {
  const { height } = useVideoConfig();
  return height / BASE_HEIGHT;
}

/**
 * 纯函数：计算指定字号的实际像素值
 * 注意：此函数不含 hook 调用，scale 必须由调用者传入
 * 用法：fontSize={fs("body")}  （需配合 useFontScale hook）
 *
 * 示例（正确用法）：
 *   const s = useFontScale();      // 组件顶层
 *   <div style={{ fontSize: fs(72) * s }}>
 *
 * @param designSize - 设计时字号（基于 1080×1920）
 * @param scale - 可选，手动传入缩放因子（未传则返回设计字号）
 */
export function fs(designSize: number, scale?: number): number {
  if (scale === undefined) return designSize;
  return Math.round(designSize * scale);
}

/** @deprecated 用 useFontScale() + fs() 代替 */
export const scaleFontSize = fs;
