/**
 * 文章主题：色板(colors) + 背景(section/p) + 可选版式
 * 与 layouts 搭配时用 getResolvedTheme(themeId, layoutId) 得到最终样式
 */

import { getLayout, resolveLayout } from './layouts.js'

export const themes = [
  {
    id: 'coral-warm',
    name: '珊瑚暖意',
    desc: '暖色块标题，圆角引用',
    colors: { accent: '#FA8B73', accentLight: '#f0d8d0', text: '#333', textSecondary: '#555', quoteBg: '#FFF8F6', tableBorder: '#f0d8d0', tableThBg: '#FA8B73' },
    section: "margin:0;padding:12px 10px;font-family:Optima,'Microsoft YaHei',PingFang SC,serif;font-size:16px;color:#333;line-height:1.8;word-break:break-word",
    p: "margin:0;padding:8px 0;color:#333;font-size:16px;line-height:1.8",
    h1: "margin:28px 0 14px;padding:0;display:flex;justify-content:center;border-top:2px solid #FA8B73;border-bottom:none",
    h1Content: "font-size:22px;color:#fff;background:#FA8B73;padding:4px 12px 6px;border-radius:0 0 12px 12px;font-weight:normal",
    h2: "margin:24px 0 12px;padding:0;display:flex;justify-content:flex-start",
    h2Content: "font-size:20px;color:#fff;background:#FA8B73;padding:6px 14px;font-weight:bold",
    h3: "margin:22px 0 10px;padding:0",
    h3Content: "font-size:18px;color:#333;font-weight:bold",
    blockquote: "margin:18px 0;padding:14px 18px;background:#FFF8F6;border-left:4px solid #FA8B73;color:#555;border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:#C45C3E",
    u: "text-decoration:underline;text-underline-offset:3px;color:#FA8B73",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #f0d8d0;border-radius:8px;overflow:hidden",
      th: "padding:10px 12px;background:#FA8B73;color:#fff;font-weight:bold;text-align:left;border:1px solid #e8c4b8",
      td: "padding:10px 12px;border:1px solid #f0d8d0;background:#fff",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px;box-shadow:0 4px 16px rgba(250,139,115,0.2)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px;border:3px solid #FA8B73",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#b85c44;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '✨', border: '#FA8B73', bg: '#FFF8F6', color: '#b85c44' },
      NOTE: { emoji: '📎', border: '#e8c4b8', bg: '#fef5f2', color: '#555' },
      IMPORTANT: { emoji: '🔶', border: '#C45C3E', bg: '#FFF8F6', color: '#8b3a28' },
      WARNING: { emoji: '⚠️', border: '#e6a336', bg: '#fffbeb', color: '#92400e' },
      CAUTION: { emoji: '🛑', border: '#c53030', bg: '#fef2f2', color: '#991b1b' },
    },
  },
  {
    id: 'ink-seri',
    name: '墨色书香',
    desc: '传统衬线，下划线强调',
    colors: { accent: '#2c2c2c', accentLight: '#5c5c5c', text: '#2c2c2c', textSecondary: '#444', quoteBg: '#f6f6f6', tableBorder: '#ddd', tableThBg: '#2c2c2c' },
    section: "margin:0;padding:12px 10px;font-family:'Noto Serif SC',SimSun,serif;font-size:16px;color:#2c2c2c;line-height:1.9;word-break:break-word",
    p: "margin:0;padding:8px 0;color:#2c2c2c;font-size:16px;line-height:1.9",
    h1: "margin:28px 0 14px;padding-bottom:10px;border-bottom:3px solid #2c2c2c;line-height:1.4",
    h1Content: "font-size:24px;color:#2c2c2c;font-weight:bold",
    h2: "margin:24px 0 12px;padding-bottom:8px;border-bottom:2px solid #2c2c2c",
    h2Content: "font-size:20px;color:#2c2c2c;font-weight:bold",
    h3: "margin:22px 0 10px;padding-left:12px;border-left:4px solid #2c2c2c",
    h3Content: "font-size:18px;color:#2c2c2c;font-weight:bold",
    blockquote: "margin:18px 0;padding:14px 18px;background:#f6f6f6;border-left:4px solid #5c5c5c;color:#444;font-style:italic",
    strong: "font-weight:bold;color:#1a1a1a",
    u: "text-decoration:underline;text-underline-offset:2px;color:#2c2c2c",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #ddd",
      th: "padding:10px 12px;background:#2c2c2c;color:#fff;font-weight:bold;text-align:left;border:1px solid #2c2c2c",
      td: "padding:10px 12px;border:1px solid #ddd;background:#fff",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:6px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:6px;box-shadow:0 2px 12px rgba(0,0,0,0.12)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border:2px solid #2c2c2c",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:13px;color:#5c5c5c;text-align:center;font-style:italic;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '📖', border: '#2c2c2c', bg: '#f6f6f6', color: '#444' },
      NOTE: { emoji: '🖋️', border: '#5c5c5c', bg: '#ebebeb', color: '#2c2c2c' },
      IMPORTANT: { emoji: '▪️', border: '#1a1a1a', bg: '#e0e0e0', color: '#1a1a1a' },
      WARNING: { emoji: '⚠️', border: '#8b7355', bg: '#f5f0e8', color: '#5c4a32' },
      CAUTION: { emoji: '✖️', border: '#8b0000', bg: '#f5e5e5', color: '#991b1b' },
    },
  },
  {
    id: 'teal-fresh',
    name: '青绿清新',
    desc: '左边线点缀，清爽留白',
    colors: { accent: '#0d9488', accentLight: '#5eead4', text: '#2d5a4a', textSecondary: '#115e59', quoteBg: '#f0fdfa', tableBorder: '#99f6e4', tableThBg: '#0d9488' },
    section: "margin:0;padding:12px 10px;font-family:Optima,'Microsoft YaHei',PingFang SC,sans-serif;font-size:16px;color:#2d5a4a;line-height:1.85;word-break:break-word",
    p: "margin:0;padding:8px 0;color:#2d5a4a;font-size:16px;line-height:1.85",
    h1: "margin:28px 0 14px;padding-left:16px;border-left:5px solid #0d9488;line-height:1.4",
    h1Content: "font-size:22px;color:#0d9488;font-weight:bold",
    h2: "margin:24px 0 12px;padding-left:14px;border-left:4px solid #0d9488",
    h2Content: "font-size:20px;color:#0d9488;font-weight:bold",
    h3: "margin:22px 0 10px;padding-left:12px;border-left:3px solid #5eead4",
    h3Content: "font-size:18px;color:#2d5a4a;font-weight:bold",
    blockquote: "margin:18px 0;padding:14px 18px;background:#f0fdfa;border-left:4px solid #0d9488;color:#115e59;border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:#0f766e",
    u: "text-decoration:underline;text-underline-offset:3px;color:#0d9488",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #99f6e4;border-radius:8px;overflow:hidden",
      th: "padding:10px 12px;background:#0d9488;color:#fff;font-weight:bold;text-align:left;border:1px solid #0d9488",
      td: "padding:10px 12px;border:1px solid #99f6e4;background:#f0fdfa",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:16px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:16px;box-shadow:0 4px 20px rgba(13,148,136,0.15)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:16px;border:3px solid #0d9488",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#0d9488;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '🌿', border: '#0d9488', bg: '#f0fdfa', color: '#115e59' },
      NOTE: { emoji: '💧', border: '#5eead4', bg: '#ccfbf1', color: '#0f766e' },
      IMPORTANT: { emoji: '📗', border: '#047857', bg: '#d1fae5', color: '#064e3b' },
      WARNING: { emoji: '🍃', border: '#e6a336', bg: '#fef3c7', color: '#92400e' },
      CAUTION: { emoji: '🔺', border: '#dc2626', bg: '#fee2e2', color: '#991b1b' },
    },
  },
  {
    id: 'purple-elegant',
    name: '紫调雅致',
    desc: '渐变标题，柔和边框',
    colors: { accent: '#7c3aed', accentLight: '#c4b5fd', text: '#4c1d95', textSecondary: '#5b21b6', quoteBg: '#f5f3ff', tableBorder: '#c4b5fd', tableThBg: '#7c3aed' },
    section: "margin:0;padding:12px 10px;font-family:Optima,'Microsoft YaHei',PingFang SC,serif;font-size:16px;color:#4c1d95;line-height:1.8;word-break:break-word",
    p: "margin:0;padding:8px 0;color:#4c1d95;font-size:16px;line-height:1.8",
    h1: "margin:28px 0 14px;padding:10px 16px;background:linear-gradient(90deg,#7c3aed,#a78bfa);border-radius:0 12px 12px 0;line-height:1.4",
    h1Content: "font-size:22px;color:#fff;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.2)",
    h2: "margin:24px 0 12px;padding:8px 14px;background:linear-gradient(90deg,#7c3aed,#a78bfa);border-radius:0 10px 10px 0",
    h2Content: "font-size:20px;color:#fff;font-weight:bold",
    h3: "margin:22px 0 10px;padding:6px 12px;border:1px solid #c4b5fd;border-radius:8px;background:#f5f3ff",
    h3Content: "font-size:18px;color:#5b21b6;font-weight:bold",
    blockquote: "margin:18px 0;padding:14px 18px;background:#f5f3ff;border-left:4px solid #7c3aed;color:#5b21b6;border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:#5b21b6",
    u: "text-decoration:underline;text-underline-offset:3px;color:#7c3aed",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #c4b5fd;border-radius:10px;overflow:hidden",
      th: "padding:10px 12px;background:linear-gradient(90deg,#7c3aed,#8b5cf6);color:#fff;font-weight:bold;text-align:left;border:1px solid #a78bfa",
      td: "padding:10px 12px;border:1px solid #c4b5fd;background:#faf5ff",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:14px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:14px;box-shadow:0 4px 20px rgba(124,58,237,0.25)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:14px;border:3px solid #7c3aed",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#6d28d9;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '💜', border: '#7c3aed', bg: '#f5f3ff', color: '#5b21b6' },
      NOTE: { emoji: '📌', border: '#c4b5fd', bg: '#ede9fe', color: '#6d28d9' },
      IMPORTANT: { emoji: '🔮', border: '#8b5cf6', bg: '#e9d5ff', color: '#4c1d95' },
      WARNING: { emoji: '⚠️', border: '#a78bfa', bg: '#faf5ff', color: '#92400e' },
      CAUTION: { emoji: '🛑', border: '#dc2626', bg: '#fef2f2', color: '#991b1b' },
    },
  },
  {
    id: 'minimal-bw',
    name: '极简黑白',
    desc: '无装饰，纯排版',
    colors: { accent: '#171717', accentLight: '#a3a3a3', text: '#171717', textSecondary: '#525252', quoteBg: '#fafafa', tableBorder: '#e5e5e5', tableThBg: '#171717' },
    section: "margin:0;padding:12px 10px;font-family:'PingFang SC',-apple-system,sans-serif;font-size:16px;color:#171717;line-height:1.9;word-break:break-word",
    p: "margin:0;padding:8px 0;color:#171717;font-size:16px;line-height:1.9",
    h1: "margin:32px 0 16px;padding:0;line-height:1.4",
    h1Content: "font-size:26px;color:#171717;font-weight:700;letter-spacing:-0.02em",
    h2: "margin:28px 0 14px;padding:0",
    h2Content: "font-size:20px;color:#171717;font-weight:600",
    h3: "margin:24px 0 12px;padding:0",
    h3Content: "font-size:17px;color:#171717;font-weight:600",
    blockquote: "margin:20px 0;padding:16px 20px;background:#fafafa;color:#525252;border-left:3px solid #a3a3a3",
    strong: "font-weight:700;color:#171717",
    u: "text-decoration:underline;text-underline-offset:2px;color:#171717",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #e5e5e5",
      th: "padding:12px 14px;background:#171717;color:#fff;font-weight:600;text-align:left;border:1px solid #171717",
      td: "padding:12px 14px;border:1px solid #e5e5e5;background:#fff",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:16px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:16px auto;margin-left:auto;margin-right:auto;border-radius:8px",
      shadow: "max-width:100%;height:auto;display:block;margin:16px auto;margin-left:auto;margin-right:auto;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08)",
      border: "max-width:100%;height:auto;display:block;margin:16px auto;margin-left:auto;margin-right:auto;border:2px solid #e5e5e5;border-radius:8px",
    },
    imageCaption: "display:block;margin:-6px 0 16px;font-size:13px;color:#737373;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '○', border: '#a3a3a3', bg: '#fafafa', color: '#525252' },
      NOTE: { emoji: '◎', border: '#737373', bg: '#f5f5f5', color: '#171717' },
      IMPORTANT: { emoji: '●', border: '#171717', bg: '#e5e5e5', color: '#171717' },
      WARNING: { emoji: '⚠', border: '#737373', bg: '#fafafa', color: '#525252' },
      CAUTION: { emoji: '✕', border: '#404040', bg: '#f5f5f5', color: '#991b1b' },
    },
  },
  {
    id: 'amber-paper',
    name: '琥珀暖纸',
    desc: '暖黄纸感背景，复古标题',
    colors: { accent: '#c9a227', accentLight: '#e8dcb8', text: '#5c4a32', textSecondary: '#5c4a32', quoteBg: 'rgba(201,162,39,0.12)', tableBorder: '#e8dcb8', tableThBg: '#c9a227' },
    section: "margin:0;padding:16px 14px;font-family:'Noto Serif SC',Georgia,serif;font-size:16px;color:#5c4a32;line-height:1.85;word-break:break-word;background:linear-gradient(180deg,#fef9f0 0%,#fdf5e6 100%);border-radius:12px;border:1px solid #f0e6d0",
    p: "margin:0;padding:8px 0;color:#5c4a32;font-size:16px;line-height:1.85",
    h1: "margin:26px 0 12px;padding:0;display:flex;justify-content:center;line-height:1.4",
    h1Content: "font-size:22px;color:#fff;background:linear-gradient(90deg,#c9a227,#d4af37);padding:6px 16px;border-radius:0 0 10px 10px;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.15)",
    h2: "margin:22px 0 10px;padding:0;border-bottom:2px solid #d4af37",
    h2Content: "font-size:19px;color:#8b6914;font-weight:bold",
    h3: "margin:20px 0 8px;padding-left:12px;border-left:4px solid #c9a227",
    h3Content: "font-size:17px;color:#6b5344;font-weight:bold",
    blockquote: "margin:16px 0;padding:14px 18px;background:rgba(201,162,39,0.12);border-left:4px solid #c9a227;color:#5c4a32;border-radius:0 8px 8px 0;font-style:italic",
    strong: "font-weight:bold;color:#8b6914",
    u: "text-decoration:underline;text-underline-offset:3px;color:#c9a227",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #e8dcb8;border-radius:8px;overflow:hidden;background:#fffef9",
      th: "padding:10px 12px;background:linear-gradient(90deg,#c9a227,#d4af37);color:#fff;font-weight:bold;text-align:left;border:1px solid #d4af37",
      td: "padding:10px 12px;border:1px solid #e8dcb8;background:#fffef9",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px;border:1px solid #f0e6d0",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px;box-shadow:0 4px 16px rgba(201,162,39,0.2)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px;border:3px solid #c9a227",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#8b6914;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '📜', border: '#c9a227', bg: 'rgba(201,162,39,0.12)', color: '#5c4a32' },
      NOTE: { emoji: '📎', border: '#d4af37', bg: '#fef9e7', color: '#6b5344' },
      IMPORTANT: { emoji: '🔶', border: '#8b6914', bg: 'rgba(201,162,39,0.2)', color: '#5c4a32' },
      WARNING: { emoji: '⚠️', border: '#b8860b', bg: '#fffbeb', color: '#92400e' },
      CAUTION: { emoji: '🛑', border: '#c53030', bg: '#fef2f2', color: '#991b1b' },
    },
  },
  {
    id: 'mist-blue',
    name: '雾蓝静读',
    desc: '淡蓝灰背景，安静阅读',
    colors: { accent: '#64748b', accentLight: '#94a3b8', text: '#334155', textSecondary: '#475569', quoteBg: 'rgba(148,163,184,0.15)', tableBorder: '#cbd5e1', tableThBg: '#475569' },
    section: "margin:0;padding:16px 14px;font-family:Optima,'Microsoft YaHei',PingFang SC,serif;font-size:16px;color:#334155;line-height:1.85;word-break:break-word;background:linear-gradient(180deg,#f0f4f8 0%,#e2e8f0 100%);border-radius:12px;border:1px solid #cbd5e1",
    p: "margin:0;padding:8px 0;color:#334155;font-size:16px;line-height:1.85",
    h1: "margin:26px 0 12px;padding:0;line-height:1.4",
    h1Content: "font-size:22px;color:#fff;background:linear-gradient(90deg,#475569,#64748b);padding:6px 14px;border-radius:0 10px 10px 0;font-weight:bold",
    h2: "margin:22px 0 10px;padding:8px 12px;background:rgba(71,85,105,0.12);border-left:4px solid #64748b;border-radius:0 6px 6px 0",
    h2Content: "font-size:19px;color:#475569;font-weight:bold",
    h3: "margin:20px 0 8px;padding-left:12px;border-left:3px solid #94a3b8",
    h3Content: "font-size:17px;color:#475569;font-weight:bold",
    blockquote: "margin:16px 0;padding:14px 18px;background:rgba(148,163,184,0.15);border-left:4px solid #64748b;color:#475569;border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:#1e293b",
    u: "text-decoration:underline;text-underline-offset:3px;color:#475569",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #cbd5e1;border-radius:8px;overflow:hidden;background:#fff",
      th: "padding:10px 12px;background:linear-gradient(90deg,#475569,#64748b);color:#fff;font-weight:bold;text-align:left;border:1px solid #64748b",
      td: "padding:10px 12px;border:1px solid #e2e8f0;background:#fff",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px;box-shadow:0 4px 16px rgba(71,85,105,0.15)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px;border:2px solid #94a3b8",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#64748b;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '🌫️', border: '#64748b', bg: 'rgba(148,163,184,0.15)', color: '#475569' },
      NOTE: { emoji: '📋', border: '#94a3b8', bg: '#f1f5f9', color: '#334155' },
      IMPORTANT: { emoji: '🔵', border: '#475569', bg: 'rgba(71,85,105,0.12)', color: '#1e293b' },
      WARNING: { emoji: '⚠️', border: '#f59e0b', bg: '#fffbeb', color: '#92400e' },
      CAUTION: { emoji: '🔴', border: '#ef4444', bg: '#fef2f2', color: '#991b1b' },
    },
  },
  {
    id: 'sakura-soft',
    name: '樱粉轻语',
    desc: '浅粉背景，温柔标题',
    colors: { accent: '#ec4899', accentLight: '#f9a8d4', text: '#4a3f47', textSecondary: '#831843', quoteBg: 'rgba(251,207,232,0.5)', tableBorder: '#fbcfe8', tableThBg: '#db2777' },
    section: "margin:0;padding:16px 14px;font-family:Optima,'Microsoft YaHei',PingFang SC,serif;font-size:16px;color:#4a3f47;line-height:1.85;word-break:break-word;background:linear-gradient(180deg,#fff5f7 0%,#fce7ef 100%);border-radius:12px;border:1px solid #fbcfe8",
    p: "margin:0;padding:8px 0;color:#4a3f47;font-size:16px;line-height:1.85",
    h1: "margin:26px 0 12px;padding:0;display:flex;justify-content:center;line-height:1.4",
    h1Content: "font-size:22px;color:#fff;background:linear-gradient(90deg,#db2777,#ec4899);padding:6px 16px;border-radius:0 0 12px 12px;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.1)",
    h2: "margin:22px 0 10px;padding:6px 12px;background:rgba(236,72,153,0.12);border-radius:0 10px 10px 0",
    h2Content: "font-size:19px;color:#be185d;font-weight:bold",
    h3: "margin:20px 0 8px;padding-left:12px;border-left:4px solid #f9a8d4",
    h3Content: "font-size:17px;color:#831843;font-weight:bold",
    blockquote: "margin:16px 0;padding:14px 18px;background:rgba(251,207,232,0.5);border-left:4px solid #ec4899;color:#831843;border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:#9d174d",
    u: "text-decoration:underline;text-underline-offset:3px;color:#db2777",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #fbcfe8;border-radius:10px;overflow:hidden;background:#fff",
      th: "padding:10px 12px;background:linear-gradient(90deg,#db2777,#ec4899);color:#fff;font-weight:bold;text-align:left;border:1px solid #ec4899",
      td: "padding:10px 12px;border:1px solid #fce7ef;background:#fff",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:14px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:14px;box-shadow:0 4px 20px rgba(219,39,119,0.2)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:14px;border:3px solid #ec4899",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#be185d;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '🌸', border: '#ec4899', bg: 'rgba(251,207,232,0.5)', color: '#831843' },
      NOTE: { emoji: '💗', border: '#f9a8d4', bg: '#fce7ef', color: '#9d174d' },
      IMPORTANT: { emoji: '🎀', border: '#db2777', bg: '#fbcfe8', color: '#831843' },
      WARNING: { emoji: '⚠️', border: '#f59e0b', bg: '#fffbeb', color: '#92400e' },
      CAUTION: { emoji: '🔴', border: '#ef4444', bg: '#fef2f2', color: '#991b1b' },
    },
  },
  {
    id: 'dark-calm',
    name: '深色护眼',
    desc: '深色背景，护眼阅读',
    colors: { accent: '#38bdf8', accentLight: '#475569', text: '#cbd5e1', textSecondary: '#94a3b8', quoteBg: 'rgba(56,189,248,0.12)', tableBorder: '#475569', tableThBg: '#334155' },
    section: "margin:0;padding:16px 14px;font-family:'PingFang SC',-apple-system,sans-serif;font-size:16px;color:#e2e8f0;line-height:1.85;word-break:break-word;background:linear-gradient(180deg,#1e293b 0%,#0f172a 100%);border-radius:12px;border:1px solid #334155",
    p: "margin:0;padding:8px 0;color:#cbd5e1;font-size:16px;line-height:1.85",
    h1: "margin:26px 0 12px;padding:0;line-height:1.4",
    h1Content: "font-size:22px;color:#0f172a;background:linear-gradient(90deg,#38bdf8,#7dd3fc);padding:6px 14px;border-radius:0 10px 10px 0;font-weight:bold",
    h2: "margin:22px 0 10px;padding:0;border-bottom:2px solid #475569",
    h2Content: "font-size:19px;color:#7dd3fc;font-weight:bold",
    h3: "margin:20px 0 8px;padding-left:12px;border-left:4px solid #38bdf8",
    h3Content: "font-size:17px;color:#94a3b8;font-weight:bold",
    blockquote: "margin:16px 0;padding:14px 18px;background:rgba(56,189,248,0.12);border-left:4px solid #38bdf8;color:#94a3b8;border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:#e2e8f0",
    u: "text-decoration:underline;text-underline-offset:3px;color:#38bdf8",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #475569;border-radius:8px;overflow:hidden;background:#1e293b",
      th: "padding:10px 12px;background:#334155;color:#f1f5f9;font-weight:bold;text-align:left;border:1px solid #475569",
      td: "padding:10px 12px;border:1px solid #334155;background:#1e293b;color:#cbd5e1",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px;box-shadow:0 4px 20px rgba(0,0,0,0.4)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px;border:2px solid #475569",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#94a3b8;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '💎', border: '#38bdf8', bg: 'rgba(56,189,248,0.15)', color: '#7dd3fc' },
      NOTE: { emoji: '📋', border: '#7dd3fc', bg: 'rgba(125,211,252,0.1)', color: '#94a3b8' },
      IMPORTANT: { emoji: '🔵', border: '#0ea5e9', bg: 'rgba(14,165,233,0.2)', color: '#c4b5fd' },
      WARNING: { emoji: '⚠️', border: '#fbbf24', bg: 'rgba(251,191,36,0.15)', color: '#fde68a' },
      CAUTION: { emoji: '🔴', border: '#f87171', bg: 'rgba(248,113,113,0.15)', color: '#fca5a5' },
    },
  },
  {
    id: 'autumn-gold',
    name: '金秋暖阳',
    desc: '秋色背景，暖阳标题',
    colors: { accent: '#ea580c', accentLight: '#fcd34d', text: '#422006', textSecondary: '#78350f', quoteBg: 'rgba(251,191,36,0.4)', tableBorder: '#fcd34d', tableThBg: '#ea580c' },
    section: "margin:0;padding:16px 14px;font-family:'Noto Serif SC',Georgia,serif;font-size:16px;color:#422006;line-height:1.85;word-break:break-word;background:linear-gradient(180deg,#fef3c7 0%,#fde68a 100%);border-radius:12px;border:1px solid #fcd34d",
    p: "margin:0;padding:8px 0;color:#422006;font-size:16px;line-height:1.85",
    h1: "margin:26px 0 12px;padding:0;display:flex;justify-content:center;line-height:1.4",
    h1Content: "font-size:22px;color:#fff;background:linear-gradient(90deg,#ea580c,#f97316);padding:6px 16px;border-radius:0 0 12px 12px;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.2)",
    h2: "margin:22px 0 10px;padding:6px 12px;background:rgba(234,88,12,0.2);border-radius:0 8px 8px 0",
    h2Content: "font-size:19px;color:#c2410c;font-weight:bold",
    h3: "margin:20px 0 8px;padding-left:12px;border-left:4px solid #ea580c",
    h3Content: "font-size:17px;color:#9a3412;font-weight:bold",
    blockquote: "margin:16px 0;padding:14px 18px;background:rgba(251,191,36,0.4);border-left:4px solid #ea580c;color:#78350f;border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:#c2410c",
    u: "text-decoration:underline;text-underline-offset:3px;color:#ea580c",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #fcd34d;border-radius:8px;overflow:hidden;background:#fffbeb",
      th: "padding:10px 12px;background:linear-gradient(90deg,#ea580c,#f97316);color:#fff;font-weight:bold;text-align:left;border:1px solid #ea580c",
      td: "padding:10px 12px;border:1px solid #fde68a;background:#fffbeb",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px;box-shadow:0 4px 16px rgba(234,88,12,0.25)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px;border:3px solid #ea580c",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#c2410c;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '🍂', border: '#ea580c', bg: 'rgba(251,191,36,0.4)', color: '#78350f' },
      NOTE: { emoji: '🌾', border: '#fcd34d', bg: '#fef3c7', color: '#422006' },
      IMPORTANT: { emoji: '🔶', border: '#c2410c', bg: '#fde68a', color: '#9a3412' },
      WARNING: { emoji: '⚠️', border: '#f59e0b', bg: '#fffbeb', color: '#92400e' },
      CAUTION: { emoji: '🛑', border: '#dc2626', bg: '#fef2f2', color: '#991b1b' },
    },
  },
  {
    id: 'yanqi-lake',
    name: '雁栖湖',
    desc: 'mdnice 风格，蓝线下划线',
    colors: { accent: '#2584B5', accentLight: '#9FCDD0', text: '#000', textSecondary: '#333', quoteBg: 'transparent', tableBorder: '#2584B5', tableThBg: '#2584B5' },
    section: "margin:0;padding:10px;font-family:Optima,'Microsoft YaHei',PingFang SC,serif;font-size:16px;color:#000;line-height:1.5em;word-break:break-word",
    p: "margin:0;padding:8px 0;color:#000;font-size:16px;line-height:1.8em",
    h1: "margin:30px 0 15px;padding:0 0 0 0;border-bottom:1px solid #2584B5;line-height:1.5em",
    h1Content: "font-size:20px;color:#2584B5;font-weight:bold",
    h2: "margin:30px 0 15px;padding:0",
    h2Content: "font-size:18px;color:#2584B5;font-weight:bold;border-bottom:4px solid #2584B5;padding-bottom:2px;display:inline-block",
    h3: "margin:30px 0 15px;padding:0 0 2px 10px;border-left:4px solid #2584B5",
    h3Content: "font-size:16px;color:#2584B5;font-weight:bold;border-bottom:2px solid #2584B5;display:inline-block;padding:2px 10px 2px 0",
    blockquote: "margin:20px 0;padding:10px 20px;border:1px dashed #2584B5;border-bottom-style:solid;color:#000;background:transparent",
    strong: "font-weight:bold;color:#2584B5",
    u: "text-decoration:underline;text-underline-offset:2px;color:#2584B5",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #2584B5",
      th: "padding:10px 12px;background:#2584B5;color:#fff;font-weight:bold;text-align:left;border:1px solid #2584B5",
      td: "padding:10px 12px;border:1px solid #9FCDD0;background:#fff",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:10px auto;margin-left:auto;margin-right:auto;border:3px solid rgba(0,0,0,0.2)",
      rounded: "max-width:100%;height:auto;display:block;margin:10px auto;margin-left:auto;margin-right:auto;border-radius:6px;border:3px solid rgba(0,0,0,0.2)",
      shadow: "max-width:100%;height:auto;display:block;margin:10px auto;margin-left:auto;margin-right:auto;border-radius:6px;box-shadow:0 2px 12px rgba(37,132,181,0.2);border:3px solid rgba(0,0,0,0.15)",
      border: "max-width:100%;height:auto;display:block;margin:10px auto;margin-left:auto;margin-right:auto;border:3px solid #2584B5",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#2584B5;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '🌊', border: '#2584B5', bg: 'rgba(159,205,208,0.2)', color: '#333' },
      NOTE: { emoji: '📎', border: '#9FCDD0', bg: 'rgba(37,132,181,0.08)', color: '#000' },
      IMPORTANT: { emoji: '🔵', border: '#1a6b94', bg: 'rgba(37,132,181,0.15)', color: '#333' },
      WARNING: { emoji: '⚠️', border: '#e6a336', bg: '#fffbeb', color: '#92400e' },
      CAUTION: { emoji: '🔴', border: '#c53030', bg: '#fef2f2', color: '#991b1b' },
    },
  },
  {
    id: 'yanqi-coral',
    name: '橙心',
    desc: 'H2 色块标签、暖色引用',
    colors: { accent: '#EF7060', accentLight: '#efebe9', text: '#000', textSecondary: '#333', quoteBg: '#fff9f9', tableBorder: '#EF7060', tableThBg: '#EF7060' },
    section: "margin:0;padding:10px;font-family:Optima,'Microsoft YaHei',PingFang SC,serif;font-size:16px;color:#000;line-height:1.5em;word-break:break-word",
    p: "margin:0;padding:8px 0;color:#000;font-size:16px;line-height:1.8em",
    h1: "margin:30px 0 15px;padding:0;display:block;line-height:1.5em",
    h1Content: "font-size:24px;color:#000;font-weight:bold;display:block",
    h2: "margin:30px 0 15px;padding:0;border-bottom:2px solid #EF7060;line-height:1.1em",
    h2Content: "font-size:22px;color:#fff;background:#EF7060;padding:3px 10px 1px;border-radius:3px 3px 0 0;font-weight:bold;display:inline-block;margin-right:5px",
    h3: "margin:30px 0 15px;padding:0;display:block",
    h3Content: "font-size:20px;color:#000;font-weight:bold;display:block",
    blockquote: "margin:20px 0;padding:10px 20px 10px 10px;border-left:3px solid #EF7060;background:#fff9f9;color:#000",
    strong: "font-weight:bold;color:#000",
    u: "text-decoration:underline;text-underline-offset:2px;color:#EF7060",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #EF7060",
      th: "padding:10px 12px;background:#EF7060;color:#fff;font-weight:bold;text-align:left;border:1px solid #EF7060",
      td: "padding:10px 12px;border:1px solid #efebe9;background:#fff",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:10px auto;margin-left:auto;margin-right:auto;border:3px solid rgba(0,0,0,0.2)",
      rounded: "max-width:100%;height:auto;display:block;margin:10px auto;margin-left:auto;margin-right:auto;border-radius:6px;border:3px solid rgba(0,0,0,0.2)",
      shadow: "max-width:100%;height:auto;display:block;margin:10px auto;margin-left:auto;margin-right:auto;border-radius:6px;box-shadow:0 2px 12px rgba(239,112,96,0.2);border:3px solid rgba(0,0,0,0.15)",
      border: "max-width:100%;height:auto;display:block;margin:10px auto;margin-left:auto;margin-right:auto;border:3px solid #EF7060",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#EF7060;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '🧡', border: '#EF7060', bg: '#fff9f9', color: '#333' },
      NOTE: { emoji: '📌', border: '#efebe9', bg: '#fff5f5', color: '#333' },
      IMPORTANT: { emoji: '🔶', border: '#d64538', bg: '#fff0ee', color: '#991b1b' },
      WARNING: { emoji: '⚠️', border: '#e6a336', bg: '#fffbeb', color: '#92400e' },
      CAUTION: { emoji: '🛑', border: '#c53030', bg: '#fef2f2', color: '#991b1b' },
    },
  },
  {
    id: 'cyanosis',
    name: '绀青 (Cyanosis)',
    desc: '深青蓝，沉稳科技感',
    colors: { accent: '#0d7377', accentLight: '#14a3a8', text: '#1a1a2e', textSecondary: '#16213e', quoteBg: '#e8f6f6', tableBorder: '#14a3a8', tableThBg: '#0d7377' },
    section: "margin:0;padding:12px 10px;font-family:Optima,'Microsoft YaHei',PingFang SC,serif;font-size:16px;color:#1a1a2e;line-height:1.8;word-break:break-word;background-color:#f8fffe;background-image:linear-gradient(rgba(13,115,119,0.06) 1px,transparent 1px),linear-gradient(90deg,rgba(13,115,119,0.06) 1px,transparent 1px);background-size:20px 20px",
    p: "margin:0;padding:8px 0;color:#1a1a2e;font-size:16px;line-height:1.8",
    h1: "margin:28px 0 14px;padding:0;border-bottom:3px solid #0d7377;line-height:1.4",
    h1Content: "font-size:22px;color:#0d7377;font-weight:bold",
    h2: "margin:24px 0 12px;padding-left:12px;border-left:4px solid #0d7377",
    h2Content: "font-size:20px;color:#0d7377;font-weight:bold",
    h3: "margin:22px 0 10px;padding-left:10px;border-left:3px solid #14a3a8",
    h3Content: "font-size:18px;color:#16213e;font-weight:bold",
    blockquote: "margin:18px 0;padding:14px 18px;background:#e8f6f6;border-left:4px solid #0d7377;color:#16213e;border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:#0d7377",
    u: "text-decoration:underline;text-underline-offset:3px;color:#0d7377",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #14a3a8;border-radius:8px;overflow:hidden",
      th: "padding:10px 12px;background:#0d7377;color:#fff;font-weight:bold;text-align:left;border:1px solid #0d7377",
      td: "padding:10px 12px;border:1px solid #14a3a8;background:#fff",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px;box-shadow:0 4px 16px rgba(13,115,119,0.2)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px;border:3px solid #0d7377",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#0d7377;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '🔷', border: '#0d7377', bg: '#e8f6f6', color: '#16213e' },
      NOTE: { emoji: '📋', border: '#14a3a8', bg: '#d4f1f1', color: '#1a1a2e' },
      IMPORTANT: { emoji: '▪️', border: '#0a5c5f', bg: '#b8e8e8', color: '#0d7377' },
      WARNING: { emoji: '⚠️', border: '#e6a336', bg: '#fef3c7', color: '#92400e' },
      CAUTION: { emoji: '🔺', border: '#dc2626', bg: '#fee2e2', color: '#991b1b' },
    },
  },
  {
    id: 'smartblue',
    name: '智慧蓝 (Smartblue)',
    desc: '明亮蓝，清爽活力',
    colors: { accent: '#1890ff', accentLight: '#69b1ff', text: '#262626', textSecondary: '#595959', quoteBg: '#e6f7ff', tableBorder: '#91d5ff', tableThBg: '#1890ff' },
    section: "margin:0;padding:12px 10px;font-family:'PingFang SC',-apple-system,sans-serif;font-size:16px;color:#262626;line-height:1.8;word-break:break-word;background-color:#fafcff;background-image:linear-gradient(rgba(24,144,255,0.06) 1px,transparent 1px),linear-gradient(90deg,rgba(24,144,255,0.06) 1px,transparent 1px);background-size:20px 20px",
    p: "margin:0;padding:8px 0;color:#262626;font-size:16px;line-height:1.8",
    h1: "margin:28px 0 14px;padding:8px 14px;background:linear-gradient(90deg,#1890ff,#40a9ff);border-radius:0 10px 10px 0;line-height:1.4",
    h1Content: "font-size:22px;color:#fff;font-weight:bold",
    h2: "margin:24px 0 12px;padding:6px 12px;background:#e6f7ff;border-left:4px solid #1890ff;border-radius:0 6px 6px 0",
    h2Content: "font-size:20px;color:#1890ff;font-weight:bold",
    h3: "margin:22px 0 10px;padding-left:12px;border-left:3px solid #69b1ff",
    h3Content: "font-size:18px;color:#262626;font-weight:bold",
    blockquote: "margin:18px 0;padding:14px 18px;background:#e6f7ff;border-left:4px solid #1890ff;color:#595959;border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:#096dd9",
    u: "text-decoration:underline;text-underline-offset:3px;color:#1890ff",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #91d5ff;border-radius:8px;overflow:hidden",
      th: "padding:10px 12px;background:linear-gradient(90deg,#1890ff,#40a9ff);color:#fff;font-weight:bold;text-align:left;border:1px solid #1890ff",
      td: "padding:10px 12px;border:1px solid #bae7ff;background:#fff",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px;box-shadow:0 4px 16px rgba(24,144,255,0.25)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px;border:3px solid #1890ff",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#1890ff;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '💡', border: '#1890ff', bg: '#e6f7ff', color: '#595959' },
      NOTE: { emoji: '📎', border: '#69b1ff', bg: '#bae7ff', color: '#262626' },
      IMPORTANT: { emoji: '🔵', border: '#096dd9', bg: '#91d5ff', color: '#262626' },
      WARNING: { emoji: '⚠️', border: '#faad14', bg: '#fffbe6', color: '#92400e' },
      CAUTION: { emoji: '🔴', border: '#ff4d4f', bg: '#fff1f0', color: '#991b1b' },
    },
  },
  {
    id: 'channing-cyan',
    name: '禅宁青 (Channing-cyan)',
    desc: '青绿清新，柔和阅读',
    colors: { accent: '#00bcd4', accentLight: '#80deea', text: '#37474f', textSecondary: '#546e7a', quoteBg: '#e0f7fa', tableBorder: '#80deea', tableThBg: '#00bcd4' },
    section: "margin:0;padding:12px 10px;font-family:Optima,'Microsoft YaHei',PingFang SC,serif;font-size:16px;color:#37474f;line-height:1.85;word-break:break-word;background-color:#f7feff;background-image:linear-gradient(rgba(0,188,212,0.06) 1px,transparent 1px),linear-gradient(90deg,rgba(0,188,212,0.06) 1px,transparent 1px);background-size:20px 20px",
    p: "margin:0;padding:8px 0;color:#37474f;font-size:16px;line-height:1.85",
    h1: "margin:28px 0 14px;padding:0;display:flex;justify-content:center;line-height:1.4",
    h1Content: "font-size:22px;color:#fff;background:linear-gradient(90deg,#00bcd4,#26c6da);padding:6px 16px;border-radius:20px;font-weight:bold",
    h2: "margin:24px 0 12px;padding:6px 14px;background:linear-gradient(90deg,rgba(0,188,212,0.15),transparent);border-left:4px solid #00bcd4;border-radius:0 8px 8px 0",
    h2Content: "font-size:20px;color:#00838f;font-weight:bold",
    h3: "margin:22px 0 10px;padding-left:12px;border-left:3px solid #80deea",
    h3Content: "font-size:18px;color:#37474f;font-weight:bold",
    blockquote: "margin:18px 0;padding:14px 18px;background:#e0f7fa;border-left:4px solid #00bcd4;color:#546e7a;border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:#00838f",
    u: "text-decoration:underline;text-underline-offset:3px;color:#00bcd4",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #80deea;border-radius:8px;overflow:hidden",
      th: "padding:10px 12px;background:linear-gradient(90deg,#00bcd4,#26c6da);color:#fff;font-weight:bold;text-align:left;border:1px solid #00bcd4",
      td: "padding:10px 12px;border:1px solid #b2ebf2;background:#fff",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:14px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:14px;box-shadow:0 4px 20px rgba(0,188,212,0.2)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:14px;border:3px solid #00bcd4",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#00838f;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '🌊', border: '#00bcd4', bg: '#e0f7fa', color: '#546e7a' },
      NOTE: { emoji: '💧', border: '#80deea', bg: '#b2ebf2', color: '#37474f' },
      IMPORTANT: { emoji: '📗', border: '#0097a7', bg: '#b2dfdb', color: '#00838f' },
      WARNING: { emoji: '⚠️', border: '#ffa726', bg: '#fff3e0', color: '#92400e' },
      CAUTION: { emoji: '🔴', border: '#ef5350', bg: '#ffebee', color: '#991b1b' },
    },
  },
  {
    id: 'fancy',
    name: '花哨 (Fancy)',
    desc: '多彩装饰，活泼风格',
    colors: { accent: '#9c27b0', accentLight: '#ce93d8', text: '#4a148c', textSecondary: '#6a1b9a', quoteBg: '#f3e5f5', tableBorder: '#ce93d8', tableThBg: '#9c27b0' },
    section: "margin:0;padding:12px 10px;font-family:Optima,'Microsoft YaHei',PingFang SC,serif;font-size:16px;color:#4a148c;line-height:1.8;word-break:break-word;background-color:#fefaff;background-image:linear-gradient(rgba(156,39,176,0.06) 1px,transparent 1px),linear-gradient(90deg,rgba(156,39,176,0.06) 1px,transparent 1px);background-size:20px 20px",
    p: "margin:0;padding:8px 0;color:#4a148c;font-size:16px;line-height:1.8",
    h1: "margin:28px 0 14px;padding:10px 16px;background:linear-gradient(135deg,#9c27b0,#e91e63);border-radius:12px;line-height:1.4;box-shadow:0 4px 12px rgba(156,39,176,0.3)",
    h1Content: "font-size:22px;color:#fff;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.2)",
    h2: "margin:24px 0 12px;padding:8px 14px;background:linear-gradient(90deg,#ce93d8,transparent);border-radius:0 10px 10px 0",
    h2Content: "font-size:20px;color:#6a1b9a;font-weight:bold",
    h3: "margin:22px 0 10px;padding:6px 12px;border:2px dashed #ce93d8;border-radius:8px;background:#f3e5f5",
    h3Content: "font-size:18px;color:#7b1fa2;font-weight:bold",
    blockquote: "margin:18px 0;padding:14px 18px;background:linear-gradient(90deg,#f3e5f5,transparent);border-left:4px solid #9c27b0;color:#6a1b9a;border-radius:0 12px 12px 0",
    strong: "font-weight:bold;color:#7b1fa2",
    u: "text-decoration:underline;text-underline-offset:3px;color:#9c27b0",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:2px solid #ce93d8;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(156,39,176,0.1)",
      th: "padding:10px 12px;background:linear-gradient(90deg,#9c27b0,#ba68c8);color:#fff;font-weight:bold;text-align:left;border:1px solid #9c27b0",
      td: "padding:10px 12px;border:1px solid #e1bee7;background:#faf5ff",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:16px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:16px;box-shadow:0 6px 20px rgba(156,39,176,0.25)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:16px;border:3px solid #9c27b0",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#7b1fa2;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '🎀', border: '#9c27b0', bg: '#f3e5f5', color: '#6a1b9a' },
      NOTE: { emoji: '💜', border: '#ce93d8', bg: '#e1bee7', color: '#4a148c' },
      IMPORTANT: { emoji: '🔮', border: '#7b1fa2', bg: '#ce93d8', color: '#4a148c' },
      WARNING: { emoji: '⚠️', border: '#ff9800', bg: '#fff3e0', color: '#92400e' },
      CAUTION: { emoji: '🛑', border: '#e91e63', bg: '#fce4ec', color: '#991b1b' },
    },
  },
  {
    id: 'jade-green',
    name: '碧玉',
    desc: '翡翠绿，温润雅致',
    colors: { accent: '#059669', accentLight: '#6ee7b7', text: '#064e3b', textSecondary: '#047857', quoteBg: '#ecfdf5', tableBorder: '#a7f3d0', tableThBg: '#059669' },
    section: "margin:0;padding:12px 10px;font-family:'Noto Serif SC',Georgia,serif;font-size:16px;color:#064e3b;line-height:1.85;word-break:break-word;background:linear-gradient(180deg,#f0fdf4 0%,#dcfce7 100%);border-radius:12px;border:1px solid #a7f3d0",
    p: "margin:0;padding:8px 0;color:#064e3b;font-size:16px;line-height:1.85",
    h1: "margin:28px 0 14px;padding:0;display:flex;justify-content:center;line-height:1.4",
    h1Content: "font-size:22px;color:#fff;background:linear-gradient(90deg,#059669,#10b981);padding:6px 16px;border-radius:0 0 12px 12px;font-weight:bold",
    h2: "margin:24px 0 12px;padding:6px 14px;border-left:4px solid #059669;background:rgba(5,150,105,0.08);border-radius:0 8px 8px 0",
    h2Content: "font-size:20px;color:#047857;font-weight:bold",
    h3: "margin:22px 0 10px;padding-left:12px;border-left:3px solid #6ee7b7",
    h3Content: "font-size:18px;color:#064e3b;font-weight:bold",
    blockquote: "margin:18px 0;padding:14px 18px;background:#ecfdf5;border-left:4px solid #059669;color:#047857;border-radius:0 8px 8px 0;font-style:italic",
    strong: "font-weight:bold;color:#047857",
    u: "text-decoration:underline;text-underline-offset:3px;color:#059669",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #a7f3d0;border-radius:8px;overflow:hidden;background:#fff",
      th: "padding:10px 12px;background:linear-gradient(90deg,#059669,#10b981);color:#fff;font-weight:bold;text-align:left;border:1px solid #059669",
      td: "padding:10px 12px;border:1px solid #a7f3d0;background:#f0fdf4",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px;box-shadow:0 4px 16px rgba(5,150,105,0.2)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:12px;border:3px solid #059669",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#047857;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '🌿', border: '#059669', bg: '#ecfdf5', color: '#047857' },
      NOTE: { emoji: '💚', border: '#6ee7b7', bg: '#d1fae5', color: '#064e3b' },
      IMPORTANT: { emoji: '📗', border: '#047857', bg: '#a7f3d0', color: '#064e3b' },
      WARNING: { emoji: '⚠️', border: '#e6a336', bg: '#fef3c7', color: '#92400e' },
      CAUTION: { emoji: '🔺', border: '#dc2626', bg: '#fee2e2', color: '#991b1b' },
    },
  },
  {
    id: 'ink-bamboo',
    name: '墨竹',
    desc: '墨绿竹韵，古风雅致',
    colors: { accent: '#15803d', accentLight: '#86efac', text: '#14532d', textSecondary: '#166534', quoteBg: '#f0fdf4', tableBorder: '#bbf7d0', tableThBg: '#15803d' },
    section: "margin:0;padding:12px 10px;font-family:'Noto Serif SC','KaiTi',serif;font-size:16px;color:#14532d;line-height:1.9;word-break:break-word;background:#fffbeb;border-radius:8px;border:1px solid #fef3c7",
    p: "margin:0;padding:8px 0;color:#14532d;font-size:16px;line-height:1.9",
    h1: "margin:28px 0 14px;padding:0;border-bottom:2px solid #15803d;line-height:1.4",
    h1Content: "font-size:22px;color:#15803d;font-weight:bold",
    h2: "margin:24px 0 12px;padding-left:12px;border-left:4px solid #15803d",
    h2Content: "font-size:20px;color:#15803d;font-weight:bold",
    h3: "margin:22px 0 10px;padding-left:10px;border-left:3px solid #86efac",
    h3Content: "font-size:18px;color:#14532d;font-weight:bold",
    blockquote: "margin:18px 0;padding:14px 18px;background:#f0fdf4;border-left:4px solid #15803d;color:#166534;font-style:italic;border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:#15803d",
    u: "text-decoration:underline;text-underline-offset:3px;color:#15803d",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #bbf7d0;border-radius:8px;overflow:hidden;background:#fff",
      th: "padding:10px 12px;background:#15803d;color:#fff;font-weight:bold;text-align:left;border:1px solid #15803d",
      td: "padding:10px 12px;border:1px solid #bbf7d0;background:#fffbeb",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:8px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:8px;box-shadow:0 2px 12px rgba(21,128,61,0.15)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border:2px solid #15803d;border-radius:8px",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#166534;text-align:center;line-height:1.5;font-style:italic",
    alertBoxes: {
      TIP: { emoji: '🎋', border: '#15803d', bg: '#f0fdf4', color: '#166534' },
      NOTE: { emoji: '📜', border: '#86efac', bg: '#dcfce7', color: '#14532d' },
      IMPORTANT: { emoji: '▪️', border: '#166534', bg: '#bbf7d0', color: '#14532d' },
      WARNING: { emoji: '⚠️', border: '#ca8a04', bg: '#fef9c3', color: '#92400e' },
      CAUTION: { emoji: '🔴', border: '#dc2626', bg: '#fee2e2', color: '#991b1b' },
    },
  },
  {
    id: 'cream-apricot',
    name: '奶油杏',
    desc: '暖杏奶白，温柔舒适',
    colors: { accent: '#ea580c', accentLight: '#fdba74', text: '#431407', textSecondary: '#9a3412', quoteBg: '#fff7ed', tableBorder: '#fed7aa', tableThBg: '#ea580c' },
    section: "margin:0;padding:16px 14px;font-family:Optima,'Microsoft YaHei',PingFang SC,serif;font-size:16px;color:#431407;line-height:1.85;word-break:break-word;background:linear-gradient(180deg,#fffbf5 0%,#fff7ed 100%);border-radius:12px;border:1px solid #ffedd5",
    p: "margin:0;padding:8px 0;color:#431407;font-size:16px;line-height:1.85",
    h1: "margin:26px 0 12px;padding:0;display:flex;justify-content:center;line-height:1.4",
    h1Content: "font-size:22px;color:#fff;background:linear-gradient(90deg,#ea580c,#f97316);padding:8px 18px;border-radius:20px;font-weight:bold;box-shadow:0 2px 8px rgba(234,88,12,0.2)",
    h2: "margin:22px 0 10px;padding:8px 14px;background:rgba(251,146,60,0.2);border-radius:0 12px 12px 0",
    h2Content: "font-size:19px;color:#c2410c;font-weight:bold",
    h3: "margin:20px 0 8px;padding-left:12px;border-left:4px solid #fdba74",
    h3Content: "font-size:17px;color:#9a3412;font-weight:bold",
    blockquote: "margin:16px 0;padding:14px 18px;background:#fff7ed;border-left:4px solid #ea580c;color:#9a3412;border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:#c2410c",
    u: "text-decoration:underline;text-underline-offset:3px;color:#ea580c",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #fed7aa;border-radius:10px;overflow:hidden;background:#fff",
      th: "padding:10px 12px;background:linear-gradient(90deg,#ea580c,#f97316);color:#fff;font-weight:bold;text-align:left;border:1px solid #ea580c",
      td: "padding:10px 12px;border:1px solid #ffedd5;background:#fffbf5",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:16px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:16px;box-shadow:0 4px 20px rgba(234,88,12,0.15)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:16px;border:3px solid #fdba74",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#9a3412;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '🍑', border: '#ea580c', bg: '#fff7ed', color: '#9a3412' },
      NOTE: { emoji: '📎', border: '#fdba74', bg: '#ffedd5', color: '#431407' },
      IMPORTANT: { emoji: '🔶', border: '#c2410c', bg: '#fed7aa', color: '#9a3412' },
      WARNING: { emoji: '⚠️', border: '#f59e0b', bg: '#fffbeb', color: '#92400e' },
      CAUTION: { emoji: '🛑', border: '#dc2626', bg: '#fef2f2', color: '#991b1b' },
    },
  },
  {
    id: 'starry-blue',
    name: '星空蓝',
    desc: '深邃蓝紫，沉稳专业',
    colors: { accent: '#2563eb', accentLight: '#93c5fd', text: '#1e3a8a', textSecondary: '#1e40af', quoteBg: '#eff6ff', tableBorder: '#bfdbfe', tableThBg: '#2563eb' },
    section: "margin:0;padding:16px 14px;font-family:'PingFang SC',-apple-system,sans-serif;font-size:16px;color:#1e3a8a;line-height:1.85;word-break:break-word;background:linear-gradient(180deg,#f8fafc 0%,#eff6ff 100%);border-radius:12px;border:1px solid #dbeafe",
    p: "margin:0;padding:8px 0;color:#1e3a8a;font-size:16px;line-height:1.85",
    h1: "margin:26px 0 12px;padding:0;line-height:1.4",
    h1Content: "font-size:22px;color:#fff;background:linear-gradient(135deg,#2563eb,#4f46e5);padding:8px 16px;border-radius:0 12px 12px 0;font-weight:bold;box-shadow:0 4px 12px rgba(37,99,235,0.25)",
    h2: "margin:22px 0 10px;padding:6px 12px;background:rgba(37,99,235,0.1);border-left:4px solid #2563eb;border-radius:0 8px 8px 0",
    h2Content: "font-size:19px;color:#1d4ed8;font-weight:bold",
    h3: "margin:20px 0 8px;padding-left:12px;border-left:3px solid #93c5fd",
    h3Content: "font-size:17px;color:#1e40af;font-weight:bold",
    blockquote: "margin:16px 0;padding:14px 18px;background:#eff6ff;border-left:4px solid #2563eb;color:#1e40af;border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:#1d4ed8",
    u: "text-decoration:underline;text-underline-offset:3px;color:#2563eb",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #bfdbfe;border-radius:8px;overflow:hidden;background:#fff",
      th: "padding:10px 12px;background:linear-gradient(90deg,#2563eb,#3b82f6);color:#fff;font-weight:bold;text-align:left;border:1px solid #2563eb",
      td: "padding:10px 12px;border:1px solid #dbeafe;background:#f8fafc",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px;box-shadow:0 4px 16px rgba(37,99,235,0.2)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px;border:2px solid #93c5fd",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#1e40af;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '⭐', border: '#2563eb', bg: '#eff6ff', color: '#1e40af' },
      NOTE: { emoji: '📌', border: '#93c5fd', bg: '#dbeafe', color: '#1e3a8a' },
      IMPORTANT: { emoji: '🔵', border: '#1d4ed8', bg: '#bfdbfe', color: '#1e3a8a' },
      WARNING: { emoji: '⚠️', border: '#f59e0b', bg: '#fffbeb', color: '#92400e' },
      CAUTION: { emoji: '🔴', border: '#ef4444', bg: '#fef2f2', color: '#991b1b' },
    },
  },
  {
    id: 'condensed-night-purple',
    name: '凝夜紫 (Condensed-night-purple)',
    desc: '深色紫调，夜间阅读',
    colors: { accent: '#a78bfa', accentLight: '#7c3aed', text: '#e9d5ff', textSecondary: '#c4b5fd', quoteBg: 'rgba(167,139,250,0.15)', tableBorder: '#6d28d9', tableThBg: '#5b21b6' },
    section: "margin:0;padding:16px 14px;font-family:'PingFang SC',-apple-system,sans-serif;font-size:16px;color:#e9d5ff;line-height:1.85;word-break:break-word;background-color:#1e1b4b;background-image:linear-gradient(rgba(167,139,250,0.08) 1px,transparent 1px),linear-gradient(90deg,rgba(167,139,250,0.08) 1px,transparent 1px),linear-gradient(180deg,#1e1b4b 0%,#0f0a1e 100%);background-size:20px 20px,20px 20px,100% 100%;border-radius:12px;border:1px solid #312e81",
    p: "margin:0;padding:8px 0;color:#e9d5ff;font-size:16px;line-height:1.85",
    h1: "margin:26px 0 12px;padding:0;line-height:1.4",
    h1Content: "font-size:22px;color:#1e1b4b;background:linear-gradient(90deg,#a78bfa,#c4b5fd);padding:6px 14px;border-radius:0 10px 10px 0;font-weight:bold",
    h2: "margin:22px 0 10px;padding:0;border-bottom:2px solid #6d28d9",
    h2Content: "font-size:19px;color:#c4b5fd;font-weight:bold",
    h3: "margin:20px 0 8px;padding-left:12px;border-left:4px solid #a78bfa",
    h3Content: "font-size:17px;color:#c4b5fd;font-weight:bold",
    blockquote: "margin:16px 0;padding:14px 18px;background:rgba(167,139,250,0.15);border-left:4px solid #a78bfa;color:#c4b5fd;border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:#e9d5ff",
    u: "text-decoration:underline;text-underline-offset:3px;color:#a78bfa",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid #6d28d9;border-radius:8px;overflow:hidden;background:#1e1b4b",
      th: "padding:10px 12px;background:#5b21b6;color:#e9d5ff;font-weight:bold;text-align:left;border:1px solid #6d28d9",
      td: "padding:10px 12px;border:1px solid #4c1d95;background:#1e1b4b;color:#c4b5fd",
    },
    image: {
      default: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto",
      rounded: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px",
      shadow: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px;box-shadow:0 4px 20px rgba(0,0,0,0.4)",
      border: "max-width:100%;height:auto;display:block;margin:14px auto;margin-left:auto;margin-right:auto;border-radius:10px;border:2px solid #6d28d9",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:#c4b5fd;text-align:center;line-height:1.5",
    alertBoxes: {
      TIP: { emoji: '🌙', border: '#a78bfa', bg: 'rgba(167,139,250,0.15)', color: '#c4b5fd' },
      NOTE: { emoji: '📋', border: '#c4b5fd', bg: 'rgba(196,181,253,0.12)', color: '#e9d5ff' },
      IMPORTANT: { emoji: '🔮', border: '#8b5cf6', bg: 'rgba(139,92,246,0.2)', color: '#e9d5ff' },
      WARNING: { emoji: '⚠️', border: '#fbbf24', bg: 'rgba(251,191,36,0.15)', color: '#fde68a' },
      CAUTION: { emoji: '🔴', border: '#f87171', bg: 'rgba(248,113,113,0.15)', color: '#fca5a5' },
    },
  },
]

export const imageStyleOptions = [
  { id: 'default', name: '默认' },
  { id: 'rounded', name: '圆角' },
  { id: 'shadow', name: '阴影' },
  { id: 'border', name: '描边' },
]

export { layoutSets } from './layouts.js'
export { getLayout } from './layouts.js'

export function getTheme(id) {
  return themes.find((t) => t.id === id) || themes[0]
}

/** 主题 + 版式 合并后的最终样式，用于渲染与导出 */
export function getResolvedTheme(themeId, layoutId) {
  const theme = getTheme(themeId)
  if (!layoutId || layoutId === 'default') return theme
  // 橙心主题使用自身色块样式，不随「极简」版式覆盖，避免与黑白极简混淆
  if (themeId === 'yanqi-coral' && layoutId === 'minimal') return theme
  const layout = getLayout(layoutId)
  if (!layout || !theme.colors) return theme
  const resolved = resolveLayout(layout, theme.colors)
  return { ...theme, ...resolved }
}

export function getImageStyle(themeOrThemeId, imageStyleId, layoutId) {
  const t = typeof themeOrThemeId === 'string'
    ? getResolvedTheme(themeOrThemeId, layoutId)
    : themeOrThemeId
  const key = imageStyleOptions.some((o) => o.id === imageStyleId) ? imageStyleId : 'default'
  return t.image?.[key] || t.image?.default || ''
}

/** 短代码：根据主题返回对应 HTML（支持 layoutId） */
export function getShortcodeHtml(themeId, key, layoutId) {
  const t = getResolvedTheme(themeId, layoutId)
  const map = {
    '关注引导': `<p style="${t.p};text-align:center;color:#888;font-size:14px">欢迎点击上方蓝字关注我们～</p>`,
    '分割线-细': `<hr style="border:none;height:1px;background:#e5e5e5;margin:24px 0">`,
    '分割线-粗': `<hr style="border:none;height:3px;background:#999;margin:28px 0;border-radius:2px">`,
  }
  return map[key] || ''
}

export const shortcodeKeys = ['关注引导', '分割线-细', '分割线-粗']

/** 默认警告框配置（emoji + 配色），主题可通过 alertBoxes 覆盖 */
export const DEFAULT_ALERT_BOXES = {
  TIP: { emoji: '💡', border: '#10b981', bg: '#ecfdf5', color: '#065f46' },
  NOTE: { emoji: '📌', border: '#3b82f6', bg: '#eff6ff', color: '#1e40af' },
  IMPORTANT: { emoji: '⭐', border: '#8b5cf6', bg: '#f5f3ff', color: '#5b21b6' },
  WARNING: { emoji: '⚠️', border: '#f59e0b', bg: '#fffbeb', color: '#92400e' },
  CAUTION: { emoji: '🔴', border: '#ef4444', bg: '#fef2f2', color: '#991b1b' },
}

function buildAlertBoxStyle(border, bg, color) {
  return `margin:16px 0;padding:12px 16px;border-radius:8px;border-left:4px solid ${border};background:${bg};color:${color};`
}

/**
 * 根据主题与版式返回警告框配置（emoji + 内联样式），支持主题级 alertBoxes 覆盖
 * @param {string} themeId
 * @param {string} layoutId
 * @param {string} kind - TIP | NOTE | IMPORTANT | WARNING | CAUTION
 * @returns {{ emoji: string, style: string }}
 */
export function getAlertBoxConfig(themeId, layoutId, kind) {
  const T = getResolvedTheme(themeId, layoutId)
  const key = (kind || '').toUpperCase()
  const overrides = T.alertBoxes && T.alertBoxes[key]
  const base = overrides || DEFAULT_ALERT_BOXES[key] || DEFAULT_ALERT_BOXES.NOTE
  const style = base.style != null
    ? base.style
    : buildAlertBoxStyle(base.border || '#3b82f6', base.bg || '#eff6ff', base.color || '#1e40af')
  return { emoji: base.emoji != null ? base.emoji : '📌', style }
}

function hexToRgb(hex) {
  if (!hex || typeof hex !== 'string') return '124,58,237'
  const h = hex.replace(/^#/, '')
  if (h.length === 3) {
    const r = parseInt(h[0] + h[0], 16)
    const g = parseInt(h[1] + h[1], 16)
    const b = parseInt(h[2] + h[2], 16)
    return `${r},${g},${b}`
  }
  if (h.length === 6) {
    const r = parseInt(h.slice(0, 2), 16)
    const g = parseInt(h.slice(2, 4), 16)
    const b = parseInt(h.slice(4, 6), 16)
    return `${r},${g},${b}`
  }
  return '124,58,237'
}

/**
 * 图床样式：根据主题 accent/accentLight 生成 gallery、track、titleBar 内联样式
 * 主题可通过 theme.gallery 覆盖 { galleryStyle, trackStyle, titleBarStyle }
 */
export function getGalleryStyles(themeId, layoutId) {
  const T = getResolvedTheme(themeId, layoutId)
  if (T.gallery && T.gallery.galleryStyle) {
    return T.gallery
  }
  const accent = T.colors?.accent || '#7c3aed'
  const accentLight = T.colors?.accentLight || '#c4b5fd'
  const rgb = hexToRgb(accent)
  const galleryStyle = `margin: 1.5em 0 2em; padding: 18px; background: radial-gradient(80.23% 80.23% at 50% 88.37%, rgba(${rgb}, 0.08) 0%, rgba(${rgb}, 0.02) 100%); border: 2px solid rgba(${rgb}, 0.4); border-radius: 12px; box-shadow: 0 8px 32px rgba(${rgb}, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1); position: relative; box-sizing: border-box; width: 100%;`
  const trackStyle = `border-radius: 8px; box-shadow: 0 4px 20px rgba(${rgb}, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.1); border: 1px solid rgba(${rgb}, 0.25); padding: 8px; margin-bottom: 15px; box-sizing: border-box;`
  const titleBarStyle = `text-align: center; font-size: 12px; color: #fff; margin: 15px 0 0; padding: 12px 18px; background: linear-gradient(90deg, ${accent}, ${accentLight}); border-radius: 8px; font-weight: 600; box-shadow: 0 0 20px rgba(${rgb}, 0.35); text-shadow: 0 1px 2px rgba(0,0,0,0.2); box-sizing: border-box;`
  return { galleryStyle, trackStyle, titleBarStyle }
}
