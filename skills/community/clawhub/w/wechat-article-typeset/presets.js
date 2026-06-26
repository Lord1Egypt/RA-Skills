/**
 * 主题混搭预设：主题(themeId) + 版式(layoutId) 组合，可直接用 --preset <名称> 或 WEWORK_PRESET=<名称>。
 * 任意主题与任意版式均可自由组合；此处仅列出常用混搭，便于快速选用。
 */
export const PRESETS = {
  // 暖色系
  '暖色色块': { themeId: 'coral-warm', layoutId: 'block' },
  '暖色下划线': { themeId: 'coral-warm', layoutId: 'underline' },
  '暖色左边线': { themeId: 'coral-warm', layoutId: 'leftline' },
  '暖色极简': { themeId: 'coral-warm', layoutId: 'minimal' },
  '琥珀色块': { themeId: 'amber-paper', layoutId: 'block' },
  '金秋渐变': { themeId: 'autumn-gold', layoutId: 'gradient' },
  '奶油杏色块': { themeId: 'cream-apricot', layoutId: 'block' },

  // 冷色 / 商务
  '墨色下划线': { themeId: 'ink-seri', layoutId: 'underline' },
  '墨色极简': { themeId: 'ink-seri', layoutId: 'minimal' },
  '青绿左边线': { themeId: 'teal-fresh', layoutId: 'leftline' },
  '青绿色块': { themeId: 'teal-fresh', layoutId: 'block' },
  '紫调渐变': { themeId: 'purple-elegant', layoutId: 'gradient' },
  '紫调色块': { themeId: 'purple-elegant', layoutId: 'block' },
  '雾蓝卡片': { themeId: 'mist-blue', layoutId: 'card' },
  '智慧蓝左边线': { themeId: 'smartblue', layoutId: 'leftline' },
  '星空蓝渐变': { themeId: 'starry-blue', layoutId: 'gradient' },
  '禅宁青色块': { themeId: 'channing-cyan', layoutId: 'block' },
  '绀青下划线': { themeId: 'cyanosis', layoutId: 'underline' },
  '凝夜紫卡片': { themeId: 'condensed-night-purple', layoutId: 'card' },

  // 黑白 / 极简
  '极简黑白': { themeId: 'minimal-bw', layoutId: 'minimal' },
  '极简色块': { themeId: 'minimal-bw', layoutId: 'block' },
  '墨色书香': { themeId: 'ink-seri', layoutId: 'default' },

  // 特色
  '雁栖湖': { themeId: 'yanqi-lake', layoutId: 'yanqi' },
  '橙心': { themeId: 'yanqi-coral', layoutId: 'yanqi-coral' },
  '樱粉色块': { themeId: 'sakura-soft', layoutId: 'block' },
  '碧玉左边线': { themeId: 'jade-green', layoutId: 'leftline' },
  '墨竹下划线': { themeId: 'ink-bamboo', layoutId: 'underline' },
  '深色护眼': { themeId: 'dark-calm', layoutId: 'card' },
  '花哨渐变': { themeId: 'fancy', layoutId: 'gradient' },
}

/** 解析预设名称（支持中文或英文 key，不区分大小写） */
export function resolvePreset(name) {
  if (!name || typeof name !== 'string') return null
  const key = name.trim()
  if (PRESETS[key]) return PRESETS[key]
  const lower = key.toLowerCase()
  for (const [k, v] of Object.entries(PRESETS)) {
    if (k.toLowerCase() === lower) return v
  }
  return null
}

/** 列出所有预设（用于 --list-presets） */
export function listPresets() {
  return Object.entries(PRESETS).map(([name, { themeId, layoutId }]) => ({
    name,
    themeId,
    layoutId,
  }))
}
