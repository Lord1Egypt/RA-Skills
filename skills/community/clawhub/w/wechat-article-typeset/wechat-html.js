#!/usr/bin/env node
/**
 * 从 Markdown 生成公众号排版用 HTML（支持主题混搭：预设 / 主题+版式 自由组合）。
 * 用法：node wechat-html.js [选项] [input.md]  或  echo "markdown..." | node wechat-html.js [选项]
 * 选项：--preset|-p <名称>  --theme|-t <id>  --layout|-l <id>  --image-style|-i <id>  --code-theme|-c <id>
 *       --list-presets|-L  --list-themes  --list-layouts
 * 环境变量：WEWORK_PRESET, WEWORK_THEME_ID, WEWORK_LAYOUT_ID, WEWORK_IMAGE_STYLE_ID, WEWORK_CODE_THEME_ID
 */

import { getFullHtml } from './lib/utils/markdown.js'
import { resolveOptions } from './opts.js'

async function readStdin() {
  const chunks = []
  for await (const chunk of process.stdin) chunks.push(chunk)
  return Buffer.concat(chunks).toString('utf8')
}

async function main() {
  const opts = resolveOptions()
  if (opts.exit) return

  let content
  const fileArg = opts.positional[0]
  if (fileArg) {
    const fs = await import('fs')
    const path = await import('path')
    const fullPath = path.isAbsolute(fileArg) ? fileArg : path.join(process.cwd(), fileArg)
    content = fs.readFileSync(fullPath, 'utf8')
  } else {
    content = await readStdin()
  }
  if (!content || !content.trim()) {
    process.stderr.write('wechat-html: 无输入内容（请从 stdin 或传入文件路径）\n')
    process.exit(1)
  }

  const html = getFullHtml(content, opts.themeId, opts.imageStyleId, opts.layoutId, null, opts.codeThemeId)
  process.stdout.write(html)
}

main().catch((err) => {
  process.stderr.write('wechat-html: ' + (err.message || err) + '\n')
  process.exit(1)
})
