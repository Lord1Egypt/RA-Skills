#!/usr/bin/env node
/**
 * 生成 HTML 并 POST 到 edit.shiker.tech/api/copy，输出复制页 URL（支持主题混搭）。
 * 用法：node wechat-copy.js [选项] <input.md>
 * 选项：--preset|-p <名称>  --theme|-t <id>  --layout|-l <id>  --image-style|-i <id>  --code-theme|-c <id>
 *       --list-presets|-L  --list-themes  --list-layouts
 * 环境变量：WEWORK_PRESET, WEWORK_THEME_ID, WEWORK_LAYOUT_ID, WEWORK_IMAGE_STYLE_ID, WEWORK_CODE_THEME_ID
 */

import { getFullHtml } from './lib/utils/markdown.js'
import { resolveOptions } from './opts.js'
import { readFileSync, writeFileSync } from 'fs'
import { dirname, isAbsolute, join, resolve as resolvePath } from 'path'

const opts = resolveOptions()
if (opts.exit) process.exit(0)

const fileArg = opts.positional[0]
if (!fileArg) {
  console.error('用法: node wechat-copy.js [--preset 预设名|--theme id --layout id] <input.md>')
  console.error('  例: node wechat-copy.js --preset 墨色下划线 article.md')
  process.exit(1)
}
const mdPath = isAbsolute(fileArg) ? fileArg : resolvePath(process.cwd(), fileArg)
const content = readFileSync(mdPath, 'utf8')
const outDir = dirname(mdPath)

const html = getFullHtml(content, opts.themeId, opts.imageStyleId, opts.layoutId, null, opts.codeThemeId)

const res = await fetch('https://edit.shiker.tech/api/copy', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ html }),
})

const data = await res.json()
if (data.success && data.data?.url) {
  const url = data.data.url
  console.log(url)
  // 必交产物：将预设主题 HTML 与预览链接写入 md 同目录，避免 AI 转述或漏数字
  try {
    const htmlFile = join(outDir, 'article.preset.html')
    writeFileSync(htmlFile, html + '\n', 'utf8')
  } catch {}
  try {
    const urlFile = join(outDir, 'wechat-preview-url.txt')
    writeFileSync(urlFile, url + '\n', 'utf8')
  } catch {}
} else {
  console.error('请求失败:', data.message || res.status)
  process.exit(1)
}
