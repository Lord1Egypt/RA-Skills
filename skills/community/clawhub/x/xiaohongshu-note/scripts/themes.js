// 小红书图文 · 风格主题库（每次渲染随机选一套，也可用 --theme 指定）
// 用法：
//   node render.js                 → 随机一套风格
//   node render.js <themeName>     → 用指定风格（如 node render.js matcha）
//   node render.js list            → 列出所有风格

const THEMES = {
  // 奶油系（默认）
  cream: {
    label: '奶油系',
    bg: '#FFFDF8', pageBg: '#f0e9df',
    ink: '#3D3A35', cocoa: '#6B5B4B', caramel: '#C68B59',
    oat: '#E9DFC9', matcha: '#A8B99A', peach: '#F2C49B',
    muted: '#A79C8C', line: '#EFE7D8', cover1: '#FFFDF8', cover2: '#F7EEDC',
    dot: '✦', emoji: true
  },

  // 抹茶清新
  matcha: {
    label: '抹茶清新',
    bg: '#F6FAF2', pageBg: '#e8f0e4',
    ink: '#2F3B30', cocoa: '#4A5A4C', caramel: '#7A9B6E',
    oat: '#E4EED9', matcha: '#8FB98A', peach: '#D7E8C9',
    muted: '#8FA08C', line: '#DEEBD6', cover1: '#F6FAF2', cover2: '#EAF2E3',
    dot: '✦', emoji: true
  },

  // 蜜桃少女
  peach: {
    label: '蜜桃少女',
    bg: '#FFF7F3', pageBg: '#fbeae2',
    ink: '#4A3530', cocoa: '#7A5A52', caramel: '#E89B7A',
    oat: '#FBE3D3', matcha: '#F2B8A0', peach: '#FFD8C4',
    muted: '#B79A8E', line: '#F9E2D6', cover1: '#FFF7F3', cover2: '#FDE9DE',
    dot: '✦', emoji: true
  },

  // 极简黑白
  mono: {
    label: '极简黑白',
    bg: '#FFFFFF', pageBg: '#ececec',
    ink: '#1A1A1A', cocoa: '#333333', caramel: '#555555',
    oat: '#F0F0F0', matcha: '#C9C9C9', peach: '#E5E5E5',
    muted: '#999999', line: '#E0E0E0', cover1: '#FFFFFF', cover2: '#F5F5F5',
    dot: '·', emoji: false
  },

  // 焦糖暖棕
  caramel: {
    label: '焦糖暖棕',
    bg: '#FBF3E6', pageBg: '#f0e3cf',
    ink: '#3E3228', cocoa: '#6B5540', caramel: '#B5793C',
    oat: '#EFDDBE', matcha: '#C9A87C', peach: '#E8C79A',
    muted: '#A08B6E', line: '#EBDDC4', cover1: '#FBF3E6', cover2: '#F3E6CF',
    dot: '✦', emoji: true
  },

  // 雾霾蓝
  mistyblue: {
    label: '雾霾蓝',
    bg: '#F2F7FA', pageBg: '#e3edf2',
    ink: '#2E3A42', cocoa: '#4A5B66', caramel: '#6E8CA0',
    oat: '#DDEAF1', matcha: '#9DB8C8', peach: '#C9DDE8',
    muted: '#8A9AA6', line: '#D9E6ED', cover1: '#F2F7FA', cover2: '#E6EFF5',
    dot: '✦', emoji: true
  },

  // 紫调梦幻
  lilac: {
    label: '紫调梦幻',
    bg: '#FBF6FC', pageBg: '#f0e7f3',
    ink: '#3D3342', cocoa: '#5E4F66', caramel: '#9B7FA8',
    oat: '#EBDCF0', matcha: '#C4A8D0', peach: '#E3D0EA',
    muted: '#A08AA8', line: '#EDE0F1', cover1: '#FBF6FC', cover2: '#F3EAF6',
    dot: '✦', emoji: true
  },
};

const THEME_KEYS = Object.keys(THEMES);

function pickTheme(requested) {
  if (!requested) {
    const k = THEME_KEYS[Math.floor(Math.random() * THEME_KEYS.length)];
    return { name: k, ...THEMES[k] };
  }
  if (requested === 'list') return null;
  if (THEMES[requested]) return { name: requested, ...THEMES[requested] };
  console.error('未知主题:', requested, '可用:', THEME_KEYS.join(', '));
  process.exit(1);
}

module.exports = { THEMES, THEME_KEYS, pickTheme };
