/**
 * 字体缩放系统
 * 基于视频实际渲染高度自动缩放字体
 * 基准：1080×1920（竖屏 9:16）
 */

import { useCurrentDimension } from "./hooks/useCurrentDimension";

/**
 * 基准设计分辨率
 * 竖屏（视频号）：1080 × 1920
 * 横屏（B站/油管）：1920 × 1080
 */
export const BASE_HEIGHT = 1920;
export const BASE_WIDTH = 1080;

/**
 * 基准字号（基于 BASE_HEIGHT = 1920 设计）
 * 所有组件统一引用这些值，系统自动缩放
 */
export const BASE_FONT_SIZES = {
  // 金句/超标题 — 全屏焦点
  hero: 144,

  // 一级标题
  h1: 96,

  // 二级标题
  h2: 72,

  // 正文（竖屏最小 54px，横屏最小 32px）
  body: 72,

  // 说明文字
  caption: 48,

  // 底部字幕
  subtitle: 36,

  // 极小说明（水印/时间戳）
  tiny: 24,
} as const;

/**
 * 颜色系统
 */
export const COLORS = {
  // 主色：科技蓝
  primary: "#00d4ff",
  // 深色背景
  background: "#0a0e17",
  // 卡片背景
  card: "#111827",
  // 主文字
  text: "#ffffff",
  // 次要文字
  muted: "#888888",
  // 极淡文字
  faint: "#444444",
  // 强调色
  accent: "#ffd93d",
  // 错误色
  error: "#ff4d4d",
  // 成功色
  success: "#00ff88",
} as const;

/**
 * 获取当前字号（带自动缩放）
 * 用法：fontSize={getFontSize("body")}
 */
export function getFontSize(
  key: keyof typeof BASE_FONT_SIZES,
  actualHeight: number = BASE_HEIGHT
): number {
  const scale = actualHeight / BASE_HEIGHT;
  return Math.round(BASE_FONT_SIZES[key] * scale);
}

/**
 * 获取当前字号（按宽度等比例缩放，防止横屏时字体过大）
 */
export function getFontSizeByWidth(
  key: keyof typeof BASE_FONT_SIZES,
  actualWidth: number = BASE_WIDTH,
  actualHeight: number = BASE_HEIGHT
): number {
  // 取宽高比例的较小者，确保不变形
  const scale = Math.min(actualWidth / BASE_WIDTH, actualHeight / BASE_HEIGHT);
  return Math.round(BASE_FONT_SIZES[key] * scale);
}

/**
 * 计算行高
 */
export function getLineHeight(
  key: keyof typeof BASE_FONT_SIZES,
  actualHeight: number = BASE_HEIGHT
): number {
  const fontSize = getFontSize(key, actualHeight);
  const lineHeightRatios = {
    hero: 1.2,
    h1: 1.25,
    h2: 1.3,
    body: 1.6,
    caption: 1.5,
    subtitle: 1.4,
    tiny: 1.3,
  };
  return Math.round(fontSize * (lineHeightRatios[key] ?? 1.5));
}
