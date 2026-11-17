/**
 * 大屏主题配置：修改此文件即可全局换肤（背景/面板/强调色/图表色板）。
 * 原理：main.ts 将字段注入 CSS 变量，theme.css 消费；图表 option 直接读本文件。
 */
export interface ThemeConfig {
  /** 页面整体背景（深色渐变三段色） */
  background: { start: string; mid: string; end: string }
  /** 页面底色（缩放留白区域） */
  pageBg: string
  /** 面板（半透明背景 + 边框色） */
  panel: { bg: string; border: string }
  /** 强调色（标题线 / KPI 数字 / 主图线条） */
  accent: string
  /** 文字 */
  text: { primary: string; secondary: string }
  /** 图表色板（ECharts series 取色，饼图按序取用） */
  chartPalette: string[]
  /** 脚注文字 */
  footer: string
}

/** 默认主题：深蓝科技风 */
export const theme: ThemeConfig = {
  background: { start: '#071527', mid: '#0d2440', end: '#0a1a33' },
  pageBg: '#030c18',
  panel: { bg: 'rgba(16, 44, 82, 0.35)', border: '#1e3a5f' },
  accent: '#14c9c9',
  text: { primary: '#e8f4ff', secondary: '#7fb3d9' },
  chartPalette: ['#14c9c9', '#3370ff', '#ff9f43', '#34c77b'],
  footer: '#5b84a8',
}

/** hex 色转带透明度 rgba（图表渐变/分割线使用） */
export function alpha(hex: string, a: number): string {
  const h = hex.replace('#', '')
  const full = h.length === 3 ? h.split('').map((c) => c + c).join('') : h
  const n = parseInt(full, 16)
  const r = (n >> 16) & 255
  const g = (n >> 8) & 255
  const b = n & 255
  return `rgba(${r},${g},${b},${a})`
}
