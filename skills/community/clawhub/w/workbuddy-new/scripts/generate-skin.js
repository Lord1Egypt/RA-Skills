#!/usr/bin/env node
/**
 * WorkBuddy Dream Skin — 皮肤生成器（零外部依赖）
 *
 * 把一句话描述自动映射成一套 WorkBuddy 皮肤 CSS：
 *   - 关键词匹配内置调色板（粉紫/黑金/海蓝/初音/赛博/森林/日落/莫兰迪/星空/糖果/极简…）
 *   - 自动识别描述里的十六进制主色（如 #39c5bb）作为强调色
 *   - 自动识别「明/亮/light」「暗/夜/dark」切换深/浅色
 *   - 生成一段覆盖 --vscode-* 变量 + 装饰光晕背景的 CSS
 *
 * 用法：
 *   node generate-skin.js --desc "赛博朋克霓虹" --name cyberpunk
 *   node generate-skin.js --desc "来个明亮清新的薄荷绿" --name mint
 *   node generate-skin.js --desc "主色用 #ff5500" --name orange
 *   node generate-skin.js --desc "星空宇宙" --name galaxy --bg "file:///C:/Users/me/space.jpg"
 *   node generate-skin.js --list
 *
 * 输出：默认写入 ../skins/<name>.css，可用 --out 指定；同时打印所用调色板摘要。
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync } = require('child_process');
const { extractPalette } = require('./lib/png-palette');

// ---------- 调色板（关键词 → 配色） ----------
const PALETTES = {
  sakura:    { label: '粉紫梦幻', keywords: ['粉', '紫', '梦幻', '樱', 'sakura', 'purple', 'pink', 'dream', '少女', '可爱', '甜'], mode: 'light', accent: '#ec5a9e', glow1: '#ffb7e0', glow2: '#c7b2ff', g1: '18% 22%', g2: '82% 78%', grad: ['#ffe3f1', '#ead6ff'] },
  blackgold: { label: '黑金奢华', keywords: ['黑金', '金', '奢华', '土豪', 'blackgold', 'gold', 'luxury', 'golden'], mode: 'dark', accent: '#d4af37', glow1: '#ffd97a', glow2: '#8a6d1f', g1: '25% 18%', g2: '75% 85%', grad: ['#1a160c', '#0e0c06'] },
  ocean:     { label: '海蓝清新', keywords: ['海', '蓝', '海洋', '清新', '水', 'ocean', 'blue', 'sea', 'aqua', '薄荷', '清'], mode: 'dark', accent: '#36cfd1', glow1: '#7fe9e6', glow2: '#2b8fff', g1: '28% 20%', g2: '72% 82%', grad: ['#0a1f2b', '#06212e'] },
  miku:      { label: '初音未来', keywords: ['初音', 'miku', '葱', '葱绿'], mode: 'dark', accent: '#39c5bb', glow1: '#7ff5ec', glow2: '#00e5ff', g1: '22% 24%', g2: '78% 76%', grad: ['#06231f', '#04181f'] },
  cyber:     { label: '赛博朋克', keywords: ['赛博', 'cyber', '朋克', '霓虹', 'neon', '故障', 'glitch'], mode: 'dark', accent: '#ff2bd6', glow1: '#ff2bd6', glow2: '#21e6ff', g1: '20% 25%', g2: '80% 75%', grad: ['#0d0221', '#15002e'] },
  forest:    { label: '森林自然', keywords: ['森林', '绿', '自然', 'forest', 'green', '草木', '植物'], mode: 'dark', accent: '#52c41a', glow1: '#a6e887', glow2: '#1f8f4d', g1: '25% 22%', g2: '75% 80%', grad: ['#0c1f10', '#06140a'] },
  sunset:    { label: '日落晚霞', keywords: ['日落', '晚霞', '橙', '夕阳', 'sunset', 'orange', '黄昏'], mode: 'dark', accent: '#ff8a3d', glow1: '#ffc08a', glow2: '#ff5e62', g1: '22% 26%', g2: '78% 74%', grad: ['#2a1407', '#1f0a1e'] },
  morandi:   { label: '莫兰迪高级灰', keywords: ['莫兰迪', '高级灰', 'morandi', '冷淡', '性冷淡', '高级'], mode: 'light', accent: '#a3927e', glow1: '#d8cdbf', glow2: '#b9a8c9', g1: '20% 24%', g2: '80% 76%', grad: ['#efe9e1', '#e3dcd2'] },
  galaxy:    { label: '星空宇宙', keywords: ['星空', '宇宙', '银河', 'galaxy', 'star', '星辰', '星河', '紫蓝'], mode: 'dark', accent: '#8a7cff', glow1: '#b9aaff', glow2: '#5ec8ff', g1: '24% 22%', g2: '76% 80%', grad: ['#0a0a1f', '#120a2a'] },
  candy:     { label: '糖果马卡龙', keywords: ['糖果', 'candy', '马卡龙', 'macaron', '彩色'], mode: 'light', accent: '#ff9ec4', glow1: '#ffd1e8', glow2: '#bce0ff', g1: '20% 22%', g2: '80% 78%', grad: ['#fff0f7', '#e8f3ff'] },
  mono:      { label: '暗黑极简', keywords: ['暗黑', '极简', '极客', 'mono', 'hacker', '黑客', '极黑', '黑客风'], mode: 'dark', accent: '#e0e0e0', glow1: '#3a3a3a', glow2: '#1a1a1a', g1: '50% 0%', g2: '50% 100%', grad: ['#0a0a0a', '#000000'] },
  emerald:   { label: '翡翠绿', keywords: ['翡翠', '翠', 'emerald'], mode: 'dark', accent: '#10b981', glow1: '#6ee7b7', glow2: '#059669', g1: '25% 22%', g2: '75% 80%', grad: ['#05201a', '#03120d'] },
};

// ---------- 经典场景主题（预生成原创同人场景图 + 双角色，命中场景词时复制） ----------
const CLASSIC_THEMES = {
  dahua: {
    file: 'dahua-classic.css', label: '大话西游经典界面',
    regex: /大话西游|至尊宝|紫霞|月光宝盒|盘丝洞|七彩祥云/,
    hero: 'dahua_scene.png', user: 'zhi_zun_bao.png', ai: 'zi_xia.png',
  },
  cyber: {
    file: 'cyberpunk-classic.css', label: '赛博朋克经典界面',
    regex: /赛博朋克.*(城市|都市|夜景|大楼|界面|经典)|霓虹都市|未来都市|cyberpunk city|赛博都市|赛博.*夜景/,
    hero: 'cyber_scene.png', user: 'cyber_runner.png', ai: 'cyber_net.png',
  },
  spirited: {
    file: 'spirited-away-classic.css', label: '千与千寻经典界面',
    regex: /千与千寻|油屋|汤屋|神隐|无脸男|白龙|千寻/,
    hero: 'spirited_scene.png', user: 'spirited_girl.png', ai: 'spirited_mask.png',
  },
  kungfu: {
    file: 'kungfu-soccer-classic.css', label: '功夫女足经典界面',
    regex: /功夫女足|功夫足球|女足|少林女足|kung fu soccer/,
    hero: 'kungfu_soccer_scene.png', user: 'kungfu_soccer_girl.png', ai: 'kungfu_soccer_girl.png',
  },
};

// ---------- 颜色工具 ----------
function hexToRgb(hex) {
  hex = hex.replace('#', '');
  if (hex.length === 3) hex = hex.split('').map((c) => c + c).join('');
  const n = parseInt(hex, 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}
function rgbToHex(r, g, b) {
  const h = (v) => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0');
  return '#' + h(r) + h(g) + h(b);
}
function mix(a, b, t) {
  const ca = hexToRgb(a), cb = hexToRgb(b);
  return rgbToHex(ca[0] + (cb[0] - ca[0]) * t, ca[1] + (cb[1] - ca[1]) * t, ca[2] + (cb[2] - ca[2]) * t);
}
const lighten = (hex, t) => mix(hex, '#ffffff', t);
const darken = (hex, t) => mix(hex, '#000000', t);
function rgba(hex, a) {
  const [r, g, b] = hexToRgb(hex);
  return `rgba(${r}, ${g}, ${b}, ${a})`;
}

// ---------- 参数解析 ----------
function parseArgs(argv) {
  const a = { desc: '', name: '', bg: '', mode: '', out: '', accent: '', ref: '', list: false, text: '', textPos: '', textColor: '', textSize: '' };
  for (let i = 2; i < argv.length; i++) {
    const x = argv[i];
    if (x === '--desc') a.desc = argv[++i] || '';
    else if (x === '--name') a.name = argv[++i] || '';
    else if (x === '--bg') a.bg = argv[++i] || '';
    else if (x === '--mode') a.mode = argv[++i] || '';
    else if (x === '--accent') a.accent = argv[++i] || '';
    else if (x === '--ref') a.ref = argv[++i] || '';
    else if (x === '--out') a.out = argv[++i] || '';
    else if (x === '--text') a.text = argv[++i] || '';
    else if (x === '--text-pos') a.textPos = argv[++i] || '';
    else if (x === '--text-color') a.textColor = argv[++i] || '';
    else if (x === '--text-size') a.textSize = argv[++i] || '';
    else if (x === '--list') a.list = true;
    else if (x === '--help' || x === '-h') { printHelp(); process.exit(0); }
  }
  return a;
}
function printHelp() {
  console.log('用法: node generate-skin.js --desc "描述" --name <id> [--bg "file:///..."] [--mode dark|light] [--ref 图片] [--accent #hex]');
  console.log('      [--text "自定义文字"] [--text-pos bottom-right|bottom-left|top-right|top-left|center|watermark]');
  console.log('      [--text-color "rgba(...)" 或 #hex] [--text-size 数字px] [--out 路径]');
}

// ---------- 解析描述 → 调色板 ----------
function resolvePalette(desc, forcedMode, accentArg) {
  const d = (desc || '').toLowerCase();
  // 1) 关键词匹配
  let hit = null;
  for (const key of Object.keys(PALETTES)) {
    if (PALETTES[key].keywords.some((k) => d.includes(k.toLowerCase()))) { hit = key; break; }
  }
  // 2) 显式主色（描述里的 #hex）
  const hexMatch = d.match(/#([0-9a-f]{6}|[0-9a-f]{3})/);
  let accent = hit ? PALETTES[hit].accent : (hexMatch ? '#' + hexMatch[1] : null);
  // 2.5) --accent 参数优先级最高
  if (accentArg && /^#?[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$/.test(accentArg.trim())) {
    let h = accentArg.trim().replace('#', '');
    if (h.length === 3) h = h.split('').map((c) => c + c).join('');
    accent = '#' + h;
  }
  // 3) 模式
  let mode = hit ? PALETTES[hit].mode : 'dark';
  if (/明|亮|light|浅/.test(d)) mode = 'light';
  else if (/暗|夜|dark|深/.test(d)) mode = 'dark';
  if (forcedMode === 'light' || forcedMode === 'dark') mode = forcedMode;
  // 4) 兜底
  if (!hit) hit = mode === 'light' ? 'candy' : 'galaxy';
  const p = Object.assign({}, PALETTES[hit]);
  p.mode = mode;
  if (accent) p.accent = accent;
  return { key: hit, p, label: PALETTES[hit].label };
}

// ---------- 自定义文字（皮肤签名 / 标语） ----------
// 把用户文字转成一段固定在界面上的 CSS（伪元素，不挡操作）
function textToCss(text) {
  if (!text || !text.content) return '';
  const content = String(text.content)
    .replace(/\\/g, '\\\\')
    .replace(/'/g, "\\'")
    .replace(/"/g, '\\"')
    .replace(/\r?\n/g, ' ');
  const pos = (text.pos || 'bottom-right').toLowerCase();
  let place;
  if (pos === 'top-left') place = 'top: 16px; left: 20px;';
  else if (pos === 'top-right') place = 'top: 16px; right: 20px;';
  else if (pos === 'bottom-left') place = 'bottom: 16px; left: 20px;';
  else if (pos === 'center') place = 'top: 50%; left: 50%; transform: translate(-50%, -50%);';
  else if (pos === 'watermark') place = 'top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-28deg);';
  else place = 'bottom: 18px; right: 24px;'; // bottom-right 默认
  const color = text.color || 'rgba(255, 255, 255, 0.6)';
  const size = text.size || 22;
  return `
/* —— 皮肤签名 / 自定义文字（不挡操作，固定浮层）—— */
body::after {
  content: '${content}';
  position: fixed;
  ${place}
  z-index: 99999;
  pointer-events: none;
  font-family: "PingFang SC", "Microsoft YaHei", "Source Han Sans SC", "Noto Sans CJK SC", sans-serif;
  font-size: ${size}px;
  font-weight: 600;
  letter-spacing: 1px;
  color: ${color};
  text-shadow: 0 2px 14px rgba(0, 0, 0, 0.5);
  opacity: 0.9;
  white-space: nowrap;
}
`;
}
// 从命令行参数构造 textToCss 所需的对象（无 --text 时返回 null）
function buildTextArg(args) {
  if (!args.text) return null;
  let size = parseInt(args.textSize, 10);
  if (isNaN(size) || size <= 0) size = 22;
  return { content: args.text, pos: args.textPos || 'bottom-right', color: args.textColor || '', size };
}

// ---------- 生成 CSS ----------
function buildCss(p, bgImage, text) {
  const A = p.accent;
  const Ah = lighten(A, 0.12);
  const Ad = darken(A, 0.20);
  const dark = p.mode === 'dark';
  const Af = dark ? mix('#f0f0f5', A, 0.08) : darken(A, 0.55);
  const editorBg = dark ? rgba(mix('#0d0f15', A, 0.10), 0.86) : rgba(mix('#ffffff', A, 0.03), 0.62);
  const panelBg = dark ? rgba(mix('#0d0f15', A, 0.07), 0.80) : rgba(mix('#ffffff', A, 0.04), 0.55);
  const sideBg = dark ? rgba(mix('#0d0f15', A, 0.06), 0.78) : rgba(mix('#ffffff', A, 0.05), 0.52);
  const actBg = dark ? rgba(mix('#0d0f15', A, 0.05), 0.75) : rgba(mix('#ffffff', A, 0.06), 0.50);
  const titleBg = dark ? rgba(mix('#0d0f15', A, 0.07), 0.80) : rgba(mix('#ffffff', A, 0.07), 0.58);
  const tabActive = dark ? rgba(mix('#0d0f15', A, 0.12), 0.92) : rgba(mix('#ffffff', A, 0.05), 0.70);
  const tabInactive = dark ? rgba(mix('#0d0f15', A, 0.05), 0.70) : rgba(mix('#ffffff', A, 0.05), 0.40);
  const widgetBg = dark ? rgba(mix('#0d0f15', A, 0.10), 0.92) : rgba(mix('#ffffff', A, 0.04), 0.92);
  const inputBg = dark ? rgba(mix('#0d0f15', A, 0.08), 0.85) : rgba(mix('#ffffff', A, 0.05), 0.80);
  const border = rgba(A, dark ? 0.35 : 0.30);
  const borderSoft = rgba(A, dark ? 0.22 : 0.25);
  const borderStrong = rgba(A, 0.60);
  const selBg = rgba(A, 0.22);
  const hoverBg = rgba(A, 0.12);
  const statusBg = rgba(A, 0.85);
  const mutedFg = rgba(Af, 0.7);

  const glowLayer1 = `radial-gradient(circle at ${p.g1}, ${rgba(p.glow1, 0.55)}, transparent 45%)`;
  const glowLayer2 = `radial-gradient(circle at ${p.g2}, ${rgba(p.glow2, 0.55)}, transparent 45%)`;
  const gradLayer = `linear-gradient(135deg, ${p.grad[0]} 0%, ${p.grad[1]} 100%)`;
  const bgImageLayer = bgImage && bgImage !== 'none' ? `url("${bgImage}") center / cover no-repeat` : '';
  const bgList = [glowLayer1, glowLayer2, gradLayer];
  if (bgImageLayer) bgList.unshift(bgImageLayer);
  const bgValue = bgList.join(',\n    ');

  return `/* ============================================================
 * WorkBuddy Dream Skin · ${p.label}（由 generate-skin.js 自动生成）
 * ${dark ? '深色' : '浅色'} / 主色 ${A}
 * 仅覆盖 --vscode-* 变量 + 一层装饰背景，不动任何官方文件
 * ============================================================ */

:root {
  /* —— 编辑器 / 主区 —— */
  --vscode-editor-background: ${editorBg} !important;
  --vscode-editor-foreground: ${Af} !important;
  --vscode-editorWidget-background: ${widgetBg} !important;
  --vscode-editorWidget-border: ${border} !important;

  /* —— 侧边栏 —— */
  --vscode-sideBar-background: ${sideBg} !important;
  --vscode-sideBar-foreground: ${Af} !important;
  --vscode-sideBarSectionHeader-background: ${rgba(A, dark ? 0.10 : 0.18)} !important;
  --vscode-sideBarTitle-foreground: ${A} !important;

  /* —— 活动栏 —— */
  --vscode-activityBar-background: ${actBg} !important;
  --vscode-activityBar-foreground: ${A} !important;
  --vscode-activityBar-inactiveForeground: ${rgba(A, 0.50)} !important;
  --vscode-activityBarBadge-background: ${A} !important;
  --vscode-activityBarBadge-foreground: #ffffff !important;

  /* —— 标题栏 —— */
  --vscode-titleBar-activeBackground: ${titleBg} !important;
  --vscode-titleBar-activeForeground: ${Af} !important;
  --vscode-titleBar-inactiveBackground: ${rgba(A, dark ? 0.04 : 0.20)} !important;
  --vscode-titleBar-inactiveForeground: ${mutedFg} !important;

  /* —— 状态栏 —— */
  --vscode-statusBar-background: ${statusBg} !important;
  --vscode-statusBar-foreground: #ffffff !important;
  --vscode-statusBar-noFolderForeground: #ffffff !important;

  /* —— 标签页 —— */
  --vscode-tab-activeBackground: ${tabActive} !important;
  --vscode-tab-inactiveBackground: ${tabInactive} !important;
  --vscode-tab-activeForeground: ${A} !important;
  --vscode-tab-inactiveForeground: ${mutedFg} !important;
  --vscode-tab-unfocusedActiveForeground: ${rgba(Af, 0.85)} !important;
  --vscode-tab-border: ${border} !important;
  --vscode-editorGroupHeader-tabsBackground: ${rgba(A, dark ? 0.05 : 0.18)} !important;
  --vscode-editorGroupHeader-tabsBorder: ${borderSoft} !important;

  /* —— 面板 —— */
  --vscode-panel-background: ${panelBg} !important;
  --vscode-panel-border: ${borderSoft} !important;
  --vscode-panelTitle-activeForeground: ${A} !important;
  --vscode-panelTitle-inactiveForeground: ${mutedFg} !important;

  /* —— 输入 / 下拉 —— */
  --vscode-input-background: ${inputBg} !important;
  --vscode-input-foreground: ${Af} !important;
  --vscode-input-border: ${border} !important;
  --vscode-input-placeholderForeground: ${mutedFg} !important;
  --vscode-inputOption-activeBackground: ${rgba(A, 0.20)} !important;
  --vscode-inputOption-activeBorder: ${rgba(A, 0.55)} !important;
  --vscode-dropdown-background: ${widgetBg} !important;
  --vscode-dropdown-foreground: ${Af} !important;
  --vscode-dropdown-border: ${border} !important;

  /* —— 按钮 —— */
  --vscode-button-background: ${A} !important;
  --vscode-button-hoverBackground: ${Ah} !important;
  --vscode-button-foreground: #ffffff !important;
  --vscode-button-secondaryBackground: ${rgba(A, dark ? 0.15 : 0.30)} !important;
  --vscode-button-secondaryForeground: ${A} !important;
  --vscode-button-secondaryHoverBackground: ${rgba(A, dark ? 0.25 : 0.45)} !important;

  /* —— 列表 —— */
  --vscode-list-activeSelectionBackground: ${selBg} !important;
  --vscode-list-activeSelectionForeground: ${dark ? lighten(A, 0.55) : darken(A, 0.40)} !important;
  --vscode-list-inactiveSelectionBackground: ${rgba(A, 0.16)} !important;
  --vscode-list-inactiveSelectionForeground: ${dark ? lighten(A, 0.55) : darken(A, 0.40)} !important;
  --vscode-list-hoverBackground: ${hoverBg} !important;
  --vscode-list-hoverForeground: ${Af} !important;
  --vscode-list-focusBackground: ${rgba(A, 0.16)} !important;
  --vscode-list-focusForeground: ${Af} !important;
  --vscode-list-highlightForeground: ${A} !important;
  --vscode-list-focusOutline: ${rgba(A, 0.55)} !important;

  /* —— 强调 / 焦点 —— */
  --vscode-focusBorder: ${rgba(A, 0.60)} !important;
  --vscode-contrastBorder: ${borderSoft} !important;
  --vscode-widget-shadow: ${rgba(A, 0.25)} !important;

  /* —— 链接 / 文本 —— */
  --vscode-textLink-foreground: ${A} !important;
  --vscode-textLink-activeForeground: ${Ad} !important;
  --vscode-textPreformat-foreground: ${A} !important;
  --vscode-textSeparator-foreground: ${rgba(A, 0.40)} !important;
  --vscode-descriptionForeground: ${mutedFg} !important;
  --vscode-icon-foreground: ${A} !important;

  /* —— 徽标 —— */
  --vscode-badge-background: ${A} !important;
  --vscode-badge-foreground: #ffffff !important;

  /* —— 滚动条 —— */
  --vscode-scrollbarSlider-background: ${rgba(A, 0.35)} !important;
  --vscode-scrollbarSlider-hoverBackground: ${rgba(A, 0.55)} !important;
  --vscode-scrollbarSlider-activeBackground: ${rgba(A, 0.70)} !important;

  /* —— 菜单 / 浮层 —— */
  --vscode-menu-background: ${widgetBg} !important;
  --vscode-menu-foreground: ${Af} !important;
  --vscode-menu-selectionBackground: ${A} !important;
  --vscode-menu-selectionForeground: #ffffff !important;
  --vscode-menu-separatorBackground: ${borderSoft} !important;
  --vscode-toolbar-hoverBackground: ${hoverBg} !important;

  /* —— 杂项 —— */
  --vscode-quickInput-background: ${widgetBg} !important;
  --vscode-quickInput-foreground: ${Af} !important;
  --vscode-notifications-background: ${widgetBg} !important;
  --vscode-notifications-foreground: ${Af} !important;
  --vscode-breadcrumb-background: ${rgba(A, dark ? 0.03 : 0.18)} !important;
  --vscode-breadcrumb-foreground: ${mutedFg} !important;
}

/* —— 装饰背景：柔光渐变 + 缓慢呼吸的光晕 —— */
body::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: -9999;
  pointer-events: none;
  background:
    ${bgValue};
  background-size: 200% 200%, 200% 200%, 100% 100%;
  animation: wb-skin-drift 18s ease-in-out infinite alternate;
}

@keyframes wb-skin-drift {
  0%   { background-position: 0% 0%, 100% 100%, 0 0; }
  100% { background-position: 30% 20%, 70% 80%, 0 0; }
}

@media (prefers-reduced-motion: reduce) {
  body::before { animation: none; }
}

/* —— 应用级设计变量（按钮 / 品牌色 / 描边 / 徽标） —— */
:root {
  --accent-9: ${A} !important;
  --accent-10: ${Ah} !important;
  --accent-11: ${Ad} !important;
  --accent-contrast: #ffffff !important;
  --accent-surface: ${rgba(A, 0.12)} !important;
  --accent-track: ${rgba(A, 0.25)} !important;
  --background: ${editorBg} !important;
  --color-background: ${editorBg} !important;
  --color-badge: ${A} !important;
  --color-border-outline: ${border} !important;
  --color-border-outline-variant: ${borderSoft} !important;
  --color-brand-active: ${Ad} !important;
  --color-brand-hover: ${Ah} !important;
  --border-color: ${border} !important;
  --border-active: ${borderStrong} !important;
  --border-hover: ${rgba(A, 0.45)} !important;
}
` + textToCss(text && !text.color ? Object.assign({}, text, { color: rgba(A, 0.85) }) : text);
}

// ---------- 经典场景皮肤：复制预置 css 并改写开发机路径为本机 ----------
function emitClassic(args, t) {
  const src = path.resolve(__dirname, '..', 'skins', t.file);
  const out = args.out || path.resolve(__dirname, '..', 'skins', `${args.name}.css`);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  // 复制时把开发机绝对路径改成本机 skill 目录，保证发出去在别人机器也能用
  const SKILL_DIR = path.resolve(__dirname, '..').replace(/\\/g, '/');
  const PREFIX = 'file:///C:/Users/qingc/.workbuddy/skills/workbuddy-dream-skin';
  let css = fs.readFileSync(src, 'utf8');
  css = css.split(PREFIX).join('file:///' + SKILL_DIR);
  const tArg = buildTextArg(args);
  if (tArg) css += textToCss(tArg);
  fs.writeFileSync(out, css, 'utf8');
  console.log(`✔ 已生成${t.label}皮肤 → ${out}`);
  console.log(`  背景场景: ${t.hero}，毛玻璃面板，双角色头像: ${t.user} / ${t.ai}` + (tArg ? `，自定义文字: ${tArg.content}` : ''));
  console.log(`  生成预览：make-preview.js --skin "${out}" --hero assets/${t.hero} --avatar-user assets/${t.user} --avatar-ai assets/${t.ai}`);
}

// ---------- 主流程 ----------
function main() {
  const args = parseArgs(process.argv);
  if (args.list) { printPalettes(); return; }
  if (!args.desc) { console.error('缺少 --desc 描述。用 --list 查看调色板，或用 --help。'); process.exit(2); }
  if (!args.name) { console.error('缺少 --name（皮肤文件名 id，仅字母数字）。'); process.exit(2); }

  const d = (args.desc || '').toLowerCase();

  // 把参考图转成取色可用的 PNG：png 直接返回（ok=true）；jpg/jpeg 尝试用 ImageMagick 的 convert 转临时 png，
  // 若本机无 convert（如 Windows 自带 convert 被误用）则降级 ok=false（仅作背景、不取色）。
  function refToPaletteSource(ref) {
    const ext = path.extname(ref).toLowerCase();
    if (ext === '.png') return { src: ref, tmp: false, ok: true };
    if (ext === '.jpg' || ext === '.jpeg') {
      const tmp = path.join(os.tmpdir(), 'dream-skin-ref-' + Date.now() + '.png');
      try { execFileSync('convert', [ref, tmp], { stdio: 'ignore' }); return { src: tmp, tmp: true, ok: true }; }
      catch (_) { return { src: null, tmp: false, ok: false }; }
    }
    return { src: null, tmp: false, ok: false, unsupported: ext };
  }

  // 参考图驱动：用户给了一张图，要「以这张图为准」生成皮肤界面
  if (args.ref) {
    const refInfo = refToPaletteSource(args.ref);
    let pal = null, palMsg = '';
    if (refInfo.ok) {
      try { pal = extractPalette(refInfo.src); }
      catch (e) { palMsg = '（取色失败，改用默认配色）'; }
      if (refInfo.tmp) { try { fs.unlinkSync(refInfo.src); } catch (_) {} }
    } else if (refInfo.unsupported) {
      console.error('参考图仅支持 PNG/JPG，当前为 ' + refInfo.unsupported);
      process.exit(1);
    } else {
      palMsg = '（本机无 ImageMagick，jpg 仅作背景、未取主色，可用 --accent 指定主色）';
    }
    const A = args.accent || (pal ? pal.accent : '#7aa2ff');
    const dark = args.mode === 'dark' || (args.mode !== 'light' && (!pal || pal.mode === 'dark'));
    const dCol = pal ? pal.dominant : (dark ? '#0a0c12' : '#e8e8e8');
    const p = pal ? {
      label: '参考图配色',
      mode: dark ? 'dark' : 'light',
      accent: A,
      glow1: lighten(A, 0.30),
      glow2: mix(dCol, A, 0.5),
      grad: dark ? [darken(dCol, 0.45), '#05060a'] : [dCol, '#ffffff'],
      g1: '30% 25%', g2: '70% 75%',
    } : {
      label: '参考图背景（默认配色）',
      mode: dark ? 'dark' : 'light',
      accent: A,
      glow1: lighten(A, 0.30),
      glow2: darken(A, 0.20),
      grad: dark ? ['#0a0c12', '#05060a'] : ['#e8e8e8', '#ffffff'],
      g1: '30% 25%', g2: '70% 75%',
    };
    const refAbs = path.resolve(args.ref);
    const bgImage = 'file:///' + refAbs.replace(/\\/g, '/');
    const css = buildCss(p, bgImage, buildTextArg(args));
    const out = args.out || path.resolve(__dirname, '..', 'skins', `${args.name}.css`);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, css, 'utf8');
    console.log(`✔ 已按参考图生成皮肤 → ${out}`);
    console.log(`  主色(accent): ${A}  模式: ${p.mode}` + (pal ? `  主背景色: ${dCol}` : ''));
    console.log(`  参考图已作为背景嵌入：${bgImage}` + (palMsg ? '\n  ' + palMsg : ''));
    if (pal) console.log('  调色板前 ' + pal.colors.length + ' 主色：' + pal.colors.map((c) => c.hex).join(' '));
    console.log('  生成预览：make-preview.js --skin "' + out + '" --hero "' + refAbs + '"');
    return;
  }

  // 经典场景皮肤：命中场景词时，复制预置的 *-classic.css（含原创同人场景图）
  for (const key of Object.keys(CLASSIC_THEMES)) {
    const t = CLASSIC_THEMES[key];
    if (t.regex.test(d)) { emitClassic(args, t); return; }
  }

  const { key, p, label } = resolvePalette(args.desc, args.mode, args.accent);
  const bgImage = args.bg
    ? (/^file:\/\//.test(args.bg) ? args.bg : 'file:///' + path.resolve(args.bg).replace(/\\/g, '/'))
    : undefined;
  const css = buildCss(p, bgImage, buildTextArg(args));

  const out = args.out || path.resolve(__dirname, '..', 'skins', `${args.name}.css`);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, css, 'utf8');

  console.log(`✔ 已生成皮肤 [${label}] → ${out}`);
  console.log(`  模式: ${p.mode === 'dark' ? '深色' : '浅色'}  主色: ${p.accent}` + (args.bg ? `  背景图: ${args.bg}` : ''));
  console.log(`  调色板匹配: ${key}`);
}

function printPalettes() {
  console.log('可用调色板（关键词触发）：');
  Object.keys(PALETTES).forEach((k) => {
    console.log(`  ${k.padEnd(10)} ${PALETTES[k].label}  [${PALETTES[k].mode}]  关键词: ${PALETTES[k].keywords.slice(0, 4).join('/')}…`);
  });
}

main();
