/**
 * 版式：只定义标题、引用、表格等「造型」，用占位符引用主题色板
 * 占位符：{{accent}} {{accentLight}} {{text}} {{textSecondary}} {{quoteBg}} {{tableBorder}} {{tableThBg}}
 * 与任意主题搭配后由 getResolvedTheme 替换为实际颜色
 */

export const layoutSets = [
  {
    id: 'block',
    name: '色块',
    desc: '标题色块、圆角引用，适用多数主题',
    h1: "margin:28px 0 14px;padding:0;display:flex;justify-content:center;border-top:2px solid {{accent}};border-bottom:none",
    h1Content: "font-size:22px;color:#fff;background:{{accent}};padding:4px 12px 6px;border-radius:0 0 12px 12px;font-weight:normal",
    h2: "margin:24px 0 12px;padding:0;display:flex;justify-content:flex-start",
    h2Content: "font-size:20px;color:#fff;background:{{accent}};padding:6px 14px;font-weight:bold",
    h3: "margin:22px 0 10px;padding:0",
    h3Content: "font-size:18px;color:{{text}};font-weight:bold",
    blockquote: "margin:18px 0;padding:14px 18px;background:{{quoteBg}};border-left:4px solid {{accent}};color:{{textSecondary}};border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:{{accent}}",
    u: "text-decoration:underline;text-underline-offset:3px;color:{{accent}}",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid {{tableBorder}};border-radius:8px;overflow:hidden",
      th: "padding:10px 12px;background:{{tableThBg}};color:#fff;font-weight:bold;text-align:left;border:1px solid {{tableBorder}}",
      td: "padding:10px 12px;border:1px solid {{tableBorder}};background:inherit",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:{{accent}};text-align:center;line-height:1.5",
  },
  {
    id: 'underline',
    name: '下划线',
    desc: '标题下划线、简洁引用，适合正式文章',
    h1: "margin:28px 0 14px;padding-bottom:10px;border-bottom:3px solid {{accent}};line-height:1.4",
    h1Content: "font-size:24px;color:{{text}};font-weight:bold",
    h2: "margin:24px 0 12px;padding-bottom:8px;border-bottom:2px solid {{accent}}",
    h2Content: "font-size:20px;color:{{text}};font-weight:bold",
    h3: "margin:22px 0 10px;padding-bottom:6px;border-bottom:1px solid {{accentLight}}",
    h3Content: "font-size:18px;color:{{text}};font-weight:bold",
    blockquote: "margin:18px 0;padding:14px 18px;background:{{quoteBg}};border-left:4px solid {{accentLight}};color:{{textSecondary}};font-style:italic",
    strong: "font-weight:bold;color:{{text}}",
    u: "text-decoration:underline;text-underline-offset:2px;color:{{accent}}",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid {{tableBorder}}",
      th: "padding:10px 12px;background:{{tableThBg}};color:#fff;font-weight:bold;text-align:left;border:1px solid {{tableBorder}}",
      td: "padding:10px 12px;border:1px solid {{tableBorder}};background:inherit",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:13px;color:{{textSecondary}};text-align:center;font-style:italic;line-height:1.5",
  },
  {
    id: 'leftline',
    name: '左边线',
    desc: '标题左边线、留白清爽，适合长文阅读',
    h1: "margin:28px 0 14px;padding-left:16px;border-left:5px solid {{accent}};line-height:1.4",
    h1Content: "font-size:22px;color:{{accent}};font-weight:bold",
    h2: "margin:24px 0 12px;padding-left:14px;border-left:4px solid {{accent}}",
    h2Content: "font-size:20px;color:{{accent}};font-weight:bold",
    h3: "margin:22px 0 10px;padding-left:12px;border-left:3px solid {{accentLight}}",
    h3Content: "font-size:18px;color:{{text}};font-weight:bold",
    blockquote: "margin:18px 0;padding:14px 18px;background:{{quoteBg}};border-left:4px solid {{accent}};color:{{textSecondary}};border-radius:0 8px 8px 0",
    strong: "font-weight:bold;color:{{accent}}",
    u: "text-decoration:underline;text-underline-offset:3px;color:{{accent}}",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid {{tableBorder}};border-radius:8px;overflow:hidden",
      th: "padding:10px 12px;background:{{tableThBg}};color:#fff;font-weight:bold;text-align:left;border:1px solid {{tableBorder}}",
      td: "padding:10px 12px;border:1px solid {{tableBorder}};background:inherit",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:{{accent}};text-align:center;line-height:1.5",
  },
  {
    id: 'minimal',
    name: '极简',
    desc: '无装饰、纯排版，专注内容',
    h1: "margin:32px 0 16px;padding:0;line-height:1.4",
    h1Content: "font-size:26px;color:{{text}};font-weight:700;letter-spacing:-0.02em",
    h2: "margin:28px 0 14px;padding:0",
    h2Content: "font-size:20px;color:{{text}};font-weight:600",
    h3: "margin:24px 0 12px;padding:0",
    h3Content: "font-size:17px;color:{{text}};font-weight:600",
    blockquote: "margin:20px 0;padding:16px 20px;background:{{quoteBg}};color:{{textSecondary}};border-left:3px solid {{accentLight}}",
    strong: "font-weight:700;color:{{text}}",
    u: "text-decoration:underline;text-underline-offset:2px;color:{{text}}",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid {{tableBorder}}",
      th: "padding:12px 14px;background:{{tableThBg}};color:#fff;font-weight:600;text-align:left;border:1px solid {{tableBorder}}",
      td: "padding:12px 14px;border:1px solid {{tableBorder}};background:inherit",
    },
    imageCaption: "display:block;margin:-6px 0 16px;font-size:13px;color:{{textSecondary}};text-align:center;line-height:1.5",
  },
  {
    id: 'yanqi',
    name: '雁栖湖',
    desc: 'mdnice 风格，蓝线下划线',
    h1: "margin:30px 0 15px;padding:0;border-bottom:1px solid {{accent}};line-height:1.5em",
    h1Content: "font-size:20px;color:{{accent}};font-weight:bold",
    h2: "margin:30px 0 15px;padding:0",
    h2Content: "font-size:18px;color:{{accent}};font-weight:bold;border-bottom:4px solid {{accent}};padding-bottom:2px;display:inline-block",
    h3: "margin:30px 0 15px;padding:0 0 2px 10px;border-left:4px solid {{accent}}",
    h3Content: "font-size:16px;color:{{accent}};font-weight:bold;border-bottom:2px solid {{accent}};display:inline-block;padding:2px 10px 2px 0",
    blockquote: "margin:20px 0;padding:10px 20px;border:1px dashed {{accent}};border-bottom-style:solid;color:{{text}};background:{{quoteBg}}",
    strong: "font-weight:bold;color:{{accent}}",
    u: "text-decoration:underline;text-underline-offset:2px;color:{{accent}}",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid {{tableBorder}}",
      th: "padding:10px 12px;background:{{tableThBg}};color:#fff;font-weight:bold;text-align:left;border:1px solid {{tableBorder}}",
      td: "padding:10px 12px;border:1px solid {{accentLight}};background:inherit",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:{{accent}};text-align:center;line-height:1.5",
  },
  {
    id: 'gradient',
    name: '渐变',
    desc: '渐变标题、圆角卡片',
    h1: "margin:28px 0 14px;padding:0;line-height:1.4",
    h1Content: "font-size:22px;color:#fff;background:linear-gradient(90deg,{{accent}},{{accentLight}});padding:8px 16px;border-radius:0 12px 12px 0;font-weight:bold;box-shadow:0 2px 8px rgba(0,0,0,0.1)",
    h2: "margin:24px 0 12px;padding:6px 14px;background:linear-gradient(90deg,{{accentLight}},transparent);border-left:4px solid {{accent}};border-radius:0 8px 8px 0",
    h2Content: "font-size:20px;color:{{text}};font-weight:bold",
    h3: "margin:22px 0 10px;padding-left:12px;border-left:3px solid {{accentLight}}",
    h3Content: "font-size:18px;color:{{text}};font-weight:bold",
    blockquote: "margin:18px 0;padding:14px 18px;background:{{quoteBg}};border-left:4px solid {{accent}};color:{{textSecondary}};border-radius:0 12px 12px 0;box-shadow:0 1px 4px rgba(0,0,0,0.04)",
    strong: "font-weight:bold;color:{{accent}}",
    u: "text-decoration:underline;text-underline-offset:3px;color:{{accent}}",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid {{tableBorder}};border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.06)",
      th: "padding:10px 12px;background:linear-gradient(90deg,{{accent}},{{accentLight}});color:#fff;font-weight:bold;text-align:left;border:1px solid {{tableBorder}}",
      td: "padding:10px 12px;border:1px solid {{tableBorder}};background:inherit",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:{{accent}};text-align:center;line-height:1.5",
  },
  {
    id: 'card',
    name: '卡片',
    desc: '引用/表格带阴影、层次分明',
    h1: "margin:28px 0 14px;padding:0;line-height:1.4",
    h1Content: "font-size:22px;color:{{text}};font-weight:bold;padding:12px 16px;background:{{quoteBg}};border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.06);border-left:4px solid {{accent}}",
    h2: "margin:24px 0 12px;padding:0",
    h2Content: "font-size:20px;color:{{text}};font-weight:bold;padding:8px 14px;background:{{quoteBg}};border-radius:0 10px 10px 0;border-left:4px solid {{accent}};box-shadow:0 1px 4px rgba(0,0,0,0.04)",
    h3: "margin:22px 0 10px;padding-left:12px;border-left:4px solid {{accentLight}}",
    h3Content: "font-size:18px;color:{{text}};font-weight:bold",
    blockquote: "margin:18px 0;padding:16px 20px;background:{{quoteBg}};border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.06);border:none;border-left:4px solid {{accent}};color:{{textSecondary}}",
    strong: "font-weight:bold;color:{{accent}}",
    u: "text-decoration:underline;text-underline-offset:3px;color:{{accent}}",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid {{tableBorder}};border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.06)",
      th: "padding:10px 12px;background:{{tableThBg}};color:#fff;font-weight:bold;text-align:left;border:1px solid {{tableBorder}}",
      td: "padding:10px 12px;border:1px solid {{tableBorder}};background:inherit",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:{{accent}};text-align:center;line-height:1.5",
  },
  {
    id: 'center',
    name: '居中',
    desc: '标题居中、对称排版',
    h1: "margin:28px 0 14px;padding:0;display:flex;justify-content:center;line-height:1.4",
    h1Content: "font-size:24px;color:{{accent}};font-weight:bold;text-align:center",
    h2: "margin:24px 0 12px;padding:0;display:flex;justify-content:center",
    h2Content: "font-size:20px;color:{{text}};font-weight:bold;text-align:center;border-bottom:2px solid {{accent}};padding-bottom:6px",
    h3: "margin:22px 0 10px;padding:0;text-align:center",
    h3Content: "font-size:18px;color:{{text}};font-weight:bold;text-align:center",
    blockquote: "margin:18px 0;padding:14px 20px;background:{{quoteBg}};border-radius:12px;color:{{textSecondary}};text-align:center;border:1px solid {{tableBorder}}",
    strong: "font-weight:bold;color:{{accent}}",
    u: "text-decoration:underline;text-underline-offset:3px;color:{{accent}}",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid {{tableBorder}};border-radius:8px;overflow:hidden",
      th: "padding:10px 12px;background:{{tableThBg}};color:#fff;font-weight:bold;text-align:center;border:1px solid {{tableBorder}}",
      td: "padding:10px 12px;border:1px solid {{tableBorder}};background:inherit;text-align:center",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:{{accent}};text-align:center;line-height:1.5",
  },
  {
    id: 'yanqi-coral',
    name: '橙心',
    desc: 'H2 色块标签、暖色引用',
    h1: "margin:30px 0 15px;padding:0;display:block;line-height:1.5em",
    h1Content: "font-size:24px;color:{{text}};font-weight:bold;display:block",
    h2: "margin:30px 0 15px;padding:0;border-bottom:2px solid {{accent}};line-height:1.1em",
    h2Content: "font-size:22px;color:#fff;background:{{accent}};padding:3px 10px 1px;border-radius:3px 3px 0 0;font-weight:bold;display:inline-block;margin-right:5px",
    h3: "margin:30px 0 15px;padding:0;display:block",
    h3Content: "font-size:20px;color:{{text}};font-weight:bold;display:block",
    blockquote: "margin:20px 0;padding:10px 20px 10px 10px;border-left:3px solid {{accent}};background:{{quoteBg}};color:{{text}}",
    strong: "font-weight:bold;color:{{accent}}",
    u: "text-decoration:underline;text-underline-offset:2px;color:{{accent}}",
    table: {
      wrap: "margin:16px 0;width:100%;border-collapse:collapse;border:1px solid {{tableBorder}}",
      th: "padding:10px 12px;background:{{tableThBg}};color:#fff;font-weight:bold;text-align:left;border:1px solid {{tableBorder}}",
      td: "padding:10px 12px;border:1px solid {{accentLight}};background:inherit",
    },
    imageCaption: "display:block;margin:-6px 0 14px;font-size:14px;color:{{accent}};text-align:center;line-height:1.5",
  },
]

function replaceVars(str, colors) {
  if (typeof str !== 'string') return str
  let s = str
  for (const [key, value] of Object.entries(colors)) {
    s = s.replace(new RegExp(`\\{\\{${key}\\}\\}`, 'g'), value || '')
  }
  return s
}

export function resolveLayout(layoutObj, colors) {
  if (!layoutObj || !colors) return layoutObj
  const out = {}
  for (const [key, value] of Object.entries(layoutObj)) {
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      out[key] = resolveLayout(value, colors)
    } else {
      out[key] = replaceVars(value, colors)
    }
  }
  return out
}

export function getLayout(id) {
  return layoutSets.find((l) => l.id === id) || null
}
