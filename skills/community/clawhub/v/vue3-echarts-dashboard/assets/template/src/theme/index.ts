import * as echarts from 'echarts'

// 大屏主题配置。生成脚手架时可用 --theme 切换，也可在此自行扩展。
export interface DashboardTheme {
  name: string
  primary: string // 主色（标题装饰、数字、强调线）
  primary2: string // 辅色（渐变末端）
  text: string // 正文/坐标轴文字
  axis: string // 轴线颜色
  split: string // 分割线颜色
  accent: string // 点缀色（饼图/图例备用）
}

export const themes: Record<string, DashboardTheme> = {
  'tech-blue': {
    name: 'tech-blue',
    primary: '#00eaff',
    primary2: '#1890ff',
    text: '#cfe9ff',
    axis: '#1c3a5c',
    split: 'rgba(28, 58, 92, 0.4)',
    accent: '#13c2c2',
  },
  'tech-green': {
    name: 'tech-green',
    primary: '#00ffa3',
    primary2: '#36cfc9',
    text: '#d6fff0',
    axis: '#15402f',
    split: 'rgba(21, 64, 47, 0.4)',
    accent: '#52c41a',
  },
  'tech-purple': {
    name: 'tech-purple',
    primary: '#b37feb',
    primary2: '#9254de',
    text: '#efe6ff',
    axis: '#3a2a5c',
    split: 'rgba(58, 42, 92, 0.4)',
    accent: '#ff85c0',
  },
}

// 默认主题：生成脚本可通过 --theme 改写此常量
export const DEFAULT_THEME = 'tech-blue'

function palette(t: DashboardTheme): string[] {
  return [t.primary, t.primary2, t.accent, '#2fc25b', '#facc14', '#ff7a45', '#9254de']
}

let active: DashboardTheme = themes[DEFAULT_THEME]

export function getTheme(): DashboardTheme {
  return active
}

// 应用主题：写入 CSS 变量（组件样式用 var(--c-*)）+ 注册 ECharts 暗色主题
export function applyTheme(name: string): void {
  if (themes[name]) active = themes[name]
  const t = active
  const root = document.documentElement
  root.style.setProperty('--c-primary', t.primary)
  root.style.setProperty('--c-primary2', t.primary2)
  root.style.setProperty('--c-text', t.text)
  root.style.setProperty('--c-accent', t.accent)
  root.style.setProperty('--c-axis', t.axis)

  echarts.registerTheme('dashboard', {
    color: palette(t),
    backgroundColor: 'transparent',
    textStyle: {
      color: t.text,
      fontFamily: 'PingFang SC, Microsoft YaHei, sans-serif',
    },
    title: { textStyle: { color: t.text } },
    legend: { textStyle: { color: t.text } },
    categoryAxis: {
      axisLine: { lineStyle: { color: t.axis } },
      axisTick: { lineStyle: { color: t.axis } },
      axisLabel: { color: t.text },
      splitLine: { lineStyle: { color: t.split } },
    },
    valueAxis: {
      axisLine: { lineStyle: { color: t.axis } },
      axisTick: { lineStyle: { color: t.axis } },
      axisLabel: { color: t.text },
      splitLine: { lineStyle: { color: t.split } },
    },
    tooltip: {
      backgroundColor: 'rgba(3, 18, 38, 0.92)',
      borderColor: t.axis,
      textStyle: { color: t.text },
    },
  })
}

// 模块加载即注册默认主题（保证图表在任何组件渲染前都能拿到 'dashboard' 主题）
applyTheme(DEFAULT_THEME)

// 十六进制颜色转 rgba，供 ECharts 渐变等需要带透明度的场景使用
export function hexToRgba(hex: string, alpha: number): string {
  const h = hex.replace('#', '')
  const full = h.length === 3 ? h.split('').map((c) => c + c).join('') : h
  const r = parseInt(full.slice(0, 2), 16)
  const g = parseInt(full.slice(2, 4), 16)
  const b = parseInt(full.slice(4, 6), 16)
  return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

export default echarts
