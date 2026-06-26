import { getResolvedTheme, getImageStyle, getShortcodeHtml, shortcodeKeys, getAlertBoxConfig, getGalleryStyles } from '../themes/index.js'
import { highlight as syntaxHighlight } from './syntaxHighlight.js'
import { getCodeTheme } from './codeThemes.js'

function escapeHtml(str) {
  if (!str) return ''
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

/** 在转义后允许 <u></u> 以真实标签渲染（带主题样式） */
function allowU(escapedStr, theme) {
  if (!escapedStr) return ''
  return escapedStr
    .replace(/&lt;u&gt;/gi, `<u style="${theme.u}">`)
    .replace(/&lt;\/u&gt;/gi, '</u>')
}

/**
 * 简单表格解析：| a | b | 换行 | c | d |
 */
function parseTable(lines, startIdx) {
  const rows = []
  let i = startIdx
  while (i < lines.length) {
    const line = lines[i]
    if (!/^\|.+\|$/.test(line.trim())) break
    const cells = line
      .split('|')
      .map((c) => c.trim())
      .filter((_, idx, arr) => idx > 0 && idx < arr.length - 1)
    if (cells.length) rows.push(cells)
    i++
  }
  return { rows, nextIdx: i }
}

export function parseMarkdown(text, themeId, imageStyleId, forExport = true, layoutId = 'default', _imageResolver, codeThemeId = 'vscode-dark') {
  const T = getResolvedTheme(themeId, layoutId)
  const imgStyle = getImageStyle(themeId, imageStyleId, layoutId)
  const lines = text.split('\n')
  const refs = {}
  const abbrevs = {}
  const footnoteDefs = {}
  const footnoteOrder = []
  const skipLineIdx = new Set()
  for (let idx = 0; idx < lines.length; idx++) {
    const ln = lines[idx]
    const refM = ln.match(/^\s*\[([^\]]+)\]:\s*(\S+)(?:\s+["']([^"']*)["'])?\s*$/)
    if (refM) {
      const id = refM[1].toLowerCase().replace(/\s+/g, ' ')
      refs[id] = { url: refM[2].replace(/^<|>$/g, ''), title: refM[3] || '' }
    }
    const abbrM = ln.match(/^\s*\*\[([^\]]+)\]:\s*(.+)\s*$/)
    if (abbrM) abbrevs[abbrM[1]] = abbrM[2].trim()
    const fnM = ln.match(/^\s*\[\^([^\]]+)\]:\s*(.*)\s*$/)
    if (fnM) {
      const id = fnM[1]
      if (!footnoteDefs[id]) {
        let content = fnM[2]
        let j = idx + 1
        skipLineIdx.add(idx)
        while (j < lines.length && /^    /.test(lines[j])) {
          content += '\n' + lines[j].replace(/^    /, '')
          skipLineIdx.add(j)
          j++
        }
        footnoteDefs[id] = content
        footnoteOrder.push(id)
      }
    }
  }
  let html = ''
  let inBlockquote = false
  let inList = false
  let listType = ''
  let listNestDepth = 0
  let inDefList = false

  function peekNextNonBlank(fromIdx) {
    for (let k = fromIdx + 1; k < lines.length; k++) {
      if (lines[k].trim() !== '') return lines[k]
    }
    return null
  }

  function closeList() {
    const listTag = listType === 'ol' ? 'ol' : 'ul'
    while (listNestDepth > 0) { html += `</${listTag}></li>`; listNestDepth-- }
    if (inList) {
      html += listType === 'ul' ? '</ul>' : '</ol>'
      inList = false
    }
  }

  /** 列表项加粗：由 <strong>标签</strong>：说明 改为 <strong><span leaf="">标签<span textstyle="" style="font-weight: normal">说明</span></span></strong> */
  function wrapListItemStrong(html) {
    const m = html.match(/^<strong style="([^"]*)">([\s\S]*?)<\/strong>([\s\S]*)$/)
    if (!m) return html
    return `<strong style="${m[1]}"><span leaf="">${m[2]}<span textstyle="" style="font-weight: normal">${m[3]}</span></span></strong>`
  }

  function renderTaskOrListItem(raw) {
    const taskMatch = raw.match(/^(\[[ xX]\])\s+(.*)$/)
    if (taskMatch) {
      const checked = /x|X/.test(taskMatch[1])
      const text = taskMatch[2]
      const box = checked ? '☑' : '☐'
      const inner = processInline(allowU(escapeHtml(text), T))
      return `<span style="margin-right:6px;color:${checked ? '#52c41a' : '#bfbfbf'}" role="img" aria-label="${checked ? '已完成' : '未完成'}">${box}</span>${wrapListItemStrong(inner)}`
    }
    return wrapListItemStrong(processInline(allowU(escapeHtml(raw), T)))
  }

  function applyAbbrevs(str) {
    let s = str
    const keys = Object.keys(abbrevs).sort((a, b) => b.length - a.length)
    for (const k of keys) {
      const re = new RegExp(`(?<![a-zA-Z0-9])${k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![a-zA-Z0-9])`, 'g')
      s = s.replace(re, (m) => `<abbr title="${escapeHtml(abbrevs[k])}">${m}</abbr>`)
    }
    return s
  }

  function resolveImgSrc(src) {
    const raw = src.trim().split('|')[0].trim()
    return raw
  }

  const fnNumMap = {}
  const fnRefCount = {}
  footnoteOrder.forEach((id, idx) => { fnNumMap[id] = idx + 1; fnRefCount[id] = 0 })

  function processInline(str, opts = {}) {
    let result = str
      .replace(/\*\*(.+?)\*\*/g, (_, x) => `<strong style="${T.strong}">${escapeHtml(x)}</strong>`)
      .replace(/__(.+?)__/g, (_, x) => `<strong style="${T.strong}">${escapeHtml(x)}</strong>`)
      .replace(/\*(.+?)\*/g, (_, x) => `<em>${escapeHtml(x)}</em>`)
      .replace(/_(.+?)_/g, (_, x) => `<em>${escapeHtml(x)}</em>`)
      .replace(/~~(.+?)~~/g, (_, x) => `<s>${escapeHtml(x)}</s>`)
      .replace(/\+\+(.+?)\+\+/g, (_, x) => `<ins>${escapeHtml(x)}</ins>`)
      .replace(/==(.+?)==/g, (_, x) => `<mark>${escapeHtml(x)}</mark>`)
      .replace(/\^(.+?)\^/g, (_, x) => `<sup>${escapeHtml(x)}</sup>`)
      .replace(/~(.+?)~/g, (_, x) => `<sub>${escapeHtml(x)}</sub>`)
      .replace(/`(.+?)`/g, (_, x) => `<code style="background:#f5f5f5;padding:2px 6px;border-radius:4px;font-size:14px">${escapeHtml(x)}</code>`)
      .replace(/\[\^([^\]]+)\]/g, (_, id) => {
        const num = fnNumMap[id]
        if (!num) return _
        const cnt = (fnRefCount[id] = (fnRefCount[id] || 0) + 1)
        const refId = cnt === 1 ? `fnref${num}` : `fnref${num}:${cnt - 1}`
        return `<sup class="footnote-ref"><a href="#fn${num}" id="${refId}" style="font-size:12px;color:#1890ff;text-decoration:none">[${num}]</a></sup>`
      })
      .replace(/!\[([^\]]*)\]\[([^\]]*)\]/g, (_, alt, id) => {
        const key = (id || alt || '').toLowerCase().replace(/\s+/g, ' ')
        const r = refs[key]
        if (!r) return _
        const u = escapeHtml(resolveImgSrc(r.url))
        const a = escapeHtml(alt || '')
        const titleAttr = r.title ? ` title="${escapeHtml(r.title)}"` : ''
        const caption = (a && T.imageCaption) ? `<span style="${T.imageCaption}">${a}</span>` : ''
        return `<img src="${u}" alt="${a}"${titleAttr} style="${imgStyle}">${caption}`
      })
      .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_, alt, srcPart) => {
        const parts = srcPart.trim().split(/\s+/)
        const src = (parts[0] || '').trim()
        const title = parts[1] ? parts[1].replace(/^["']|["']$/g, '') : ''
        const u = escapeHtml(resolveImgSrc(src))
        const a = escapeHtml(alt || '')
        const titleAttr = title ? ` title="${escapeHtml(title)}"` : ''
        const caption = (a && T.imageCaption) ? `<span style="${T.imageCaption}">${a}</span>` : ''
        return `<img src="${u}" alt="${a}"${titleAttr} style="${imgStyle}">${caption}`
      })
      .replace(/\[([^\]]*)\]\[([^\]]*)\]/g, (_, text, id) => {
        const key = (id || text || '').toLowerCase().replace(/\s+/g, ' ')
        const r = refs[key]
        if (!r) return _
        const url = escapeHtml(r.url)
        const t = escapeHtml(text || r.url)
        const titleAttr = r.title ? ` title="${escapeHtml(r.title)}"` : ''
        return `<a href="${url}"${titleAttr} style="color:#1890ff;text-decoration:underline" target="_blank" rel="noopener">${t}</a>`
      })
      .replace(/\[([^\]]*)\]\(([^)]+)\)/g, (_, text, hrefPart) => {
        const parts = hrefPart.trim().split(/\s+/)
        const href = (parts[0] || '').trim()
        const title = parts[1] ? parts[1].replace(/^["']|["']$/g, '') : ''
        const url = escapeHtml(href)
        const t = escapeHtml(text || url)
        const titleAttr = title ? ` title="${escapeHtml(title)}"` : ''
        return `<a href="${url}"${titleAttr} style="color:#1890ff;text-decoration:underline" target="_blank" rel="noopener">${t}</a>`
      })
    return applyAbbrevs(result)
  }

  for (let i = 0; i < lines.length; i++) {
    let line = lines[i]

    if (skipLineIdx.has(i) || /^\s*\[([^\]]+)\]:\s*\S+/.test(line) || /^\s*\*\[([^\]]+)\]:\s*/.test(line)) continue

    const shortcodeMatch = line.match(/^\[([^\]]+)\]$/)
    if (shortcodeMatch && shortcodeKeys.includes(shortcodeMatch[1])) {
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      closeList()
      html += getShortcodeHtml(themeId, shortcodeMatch[1], layoutId)
      continue
    }

    if (line === '---' || line === '***' || /^___+$/.test(line.trim())) {
      if (inBlockquote) {
        html += '</blockquote>'
        inBlockquote = false
      }
      closeList()
      html += '<hr style="border:none;height:1px;background:#e5e5e5;margin:24px 0">'
      continue
    }

    const galleryOpen = line.trim().match(/^:::\s*gallery\s*(?:\[([^\]]*)\])?\s*$/)
    if (galleryOpen) {
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      closeList()
      const title = (galleryOpen[1] || '').trim()
      const galleryLines = []
      let j = i + 1
      while (j < lines.length && lines[j].trim() !== ':::') {
        galleryLines.push(lines[j])
        j++
      }
      const items = []
      for (const ln of galleryLines) {
        const m = ln.trim().match(/^!\[([^\]]*)\]\(([^)]+)\)\s*$/)
        if (m) {
          const url = (m[2] || '').trim().split(/\s+/)[0].trim().split('|')[0]
          items.push({ alt: m[1] || '', url })
        }
      }
      const n = Math.max(1, items.length)
      const pct = (100 / n).toFixed(4)
      const widthPct = n * 100
      const galleryStyles = getGalleryStyles(themeId, layoutId)
      const scrollStyle = 'display: inline-block; width: 100%; vertical-align: top; overflow-x: auto; scroll-snap-type: x mandatory; overflow-y: hidden; padding-right: 3px; padding-left: 3px; box-sizing: border-box;'
      const flexStyle = `width: ${widthPct}%; min-width: 100%; box-sizing: border-box; display: flex; justify-content: flex-start; align-items: center; max-width: ${widthPct}% !important;`
      const slideStyle = `display: inline-block; width: ${pct}%; vertical-align: middle; box-sizing: border-box; scroll-snap-align: start;`
      const galleryImgStyle = 'height: auto !important; visibility: visible !important; width: 100% !important;'
      const slidesHtml = items.length ? items.map((it) => {
        const u = escapeHtml(resolveImgSrc(it.url))
        const a = escapeHtml(it.alt || '')
        return `<section style="${slideStyle}"><section style="box-sizing: border-box;"><section style="display: inline-block; width: 100%; vertical-align: top; padding-right: 3px; padding-left: 3px; box-sizing: border-box;"><section style="box-sizing: border-box;"><section style="text-align: center; margin-left: 8px; margin-right: 8px;"><img src="${u}" alt="${a}" style="${galleryImgStyle}">${(a && T.imageCaption) ? `<span style="${T.imageCaption}">${a}</span>` : ''}</section></section></section></section></section>`
      }).join('') : `<section style="${slideStyle}"><section style="text-align: center; color: #999; padding: 24px;">暂无图片</section></section>`
      const titleText = escapeHtml(title) || '滑动图床'
      html += `<section class="gallery" style="${galleryStyles.galleryStyle}"><section style="margin: 0; padding: 0; box-sizing: border-box;"><section style="${galleryStyles.trackStyle}"><section style="margin: 0; padding: 0; box-sizing: border-box;"><section style="${scrollStyle}"><section style="${flexStyle}">${slidesHtml}</section></section></section></section><section style="${galleryStyles.titleBarStyle}"><p style="margin: 0; text-align: center; box-sizing: border-box;"><span style="font-size: 12px; color: inherit;">${titleText}</span></p></section></section></section>`
      i = j
      continue
    }

    const containerOpen = line.trim().match(/^:::\s*(\w+)\s*$/)
    if (containerOpen) {
      const name = containerOpen[1]
      const containerLines = []
      let j = i + 1
      while (j < lines.length && lines[j].trim() !== ':::') {
        containerLines.push(lines[j])
        j++
      }
      const inner = containerLines.map((ln) => {
        const p = allowU(escapeHtml(ln), T)
        return `<p style="margin:8px 0">${processInline(p)}</p>`
      }).join('')
      html += `<div class="${name}" style="padding:16px;margin:16px 0;border-radius:8px;border:1px solid #ffc107;background:#fffbf0">${inner}</div>`
      i = j
      continue
    }

    const codeBlockOpen = line.trim().startsWith('```')
    if (codeBlockOpen) {
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      closeList()
      const langMatch = line.trim().match(/^```(\w*)/)
      const lang = (langMatch && langMatch[1]) ? langMatch[1] : ''
      const codeLines = []
      let j = i + 1
      while (j < lines.length && lines[j].trim() !== '```') {
        codeLines.push(lines[j])
        j++
      }
      const codeContent = codeLines.join('\n')
      const ct = getCodeTheme(codeThemeId)
      const codeBlockStyle = T.codeBlock || `margin:16px 0;padding:14px 18px;background:${ct.block.bg};border-radius:8px;overflow:auto;font-family:Consolas,Monaco,monospace;font-size:14px;line-height:1.5;border:1px solid ${ct.block.border};white-space:pre-wrap;word-break:break-word;color:${ct.colors.default}`
      const langLabel = lang ? `<div style="font-size:12px;color:${ct.block.labelColor};margin-bottom:8px;font-family:Consolas,monospace">${escapeHtml(lang)}</div>` : ''
      const highlighted = syntaxHighlight(codeContent, lang, codeThemeId)
      const dataLang = lang ? ` data-lang="${escapeHtml(lang)}"` : ''
      html += `<pre style="${codeBlockStyle}"${dataLang}>${langLabel}<code style="background:transparent;padding:0;font-size:inherit">${highlighted}</code></pre>`
      i = j
      continue
    }

    if (line.startsWith('# ')) {
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      closeList()
      const content = processInline(allowU(escapeHtml(line.slice(2)), T))
      html += `<h1 style="${T.h1}"><span style="${T.h1Content}">${content}</span></h1>`
      continue
    }
    if (line.startsWith('## ')) {
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      closeList()
      const content = processInline(allowU(escapeHtml(line.slice(3)), T))
      html += `<h2 style="${T.h2}"><span style="${T.h2Content}">${content}</span></h2>`
      continue
    }
    if (line.startsWith('### ')) {
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      closeList()
      const content = processInline(allowU(escapeHtml(line.slice(4)), T))
      html += `<h3 style="${T.h3}"><span style="${T.h3Content}">${content}</span></h3>`
      continue
    }
    if (line.startsWith('#### ')) {
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      closeList()
      const content = processInline(allowU(escapeHtml(line.slice(5)), T))
      html += `<h4 style="${T.h3};font-size:16px">${content}</h4>`
      continue
    }
    if (line.startsWith('##### ')) {
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      closeList()
      const content = processInline(allowU(escapeHtml(line.slice(6)), T))
      html += `<h5 style="${T.h3};font-size:15px">${content}</h5>`
      continue
    }
    if (line.startsWith('###### ')) {
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      closeList()
      const content = processInline(allowU(escapeHtml(line.slice(7)), T))
      html += `<h6 style="${T.h3};font-size:14px">${content}</h6>`
      continue
    }

    if (/^\|.+\|$/.test(line.trim()) && line.includes('|')) {
      const { rows, nextIdx } = parseTable(lines, i)
      i = nextIdx - 1
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      closeList()
      if (rows.length >= 1) {
        const sepIdx = rows.findIndex((r) => r.every((c) => /^[-:]+$/.test(c)))
        const headerRow = sepIdx >= 0 ? rows[0] : null
        const bodyRows = sepIdx >= 0 ? rows.slice(sepIdx + 1).filter((r) => !r.every((c) => /^[-:]+$/.test(c))) : rows
        html += `<table style="${T.table.wrap}">`
        if (headerRow && headerRow.length) {
          html += '<thead><tr>'
          headerRow.forEach((cell) => {
            html += `<th style="${T.table.th}">${processInline(allowU(escapeHtml(cell), T))}</th>`
          })
          html += '</tr></thead>'
        }
        html += '<tbody>'
        bodyRows.forEach((row) => {
          html += '<tr>'
          row.forEach((cell) => {
            html += `<td style="${T.table.td}">${processInline(allowU(escapeHtml(cell), T))}</td>`
          })
          html += '</tr>'
        })
        html += '</tbody></table>'
      }
      continue
    }

    if (/^(    |\t)/.test(line) && line.trim() !== '') {
      const trimmed = line.replace(/^(    |\t)/, '')
      if (/^[-*+]\s/.test(trimmed) || /^\d+\.\s/.test(trimmed)) {
      } else {
        if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
        closeList()
        const codeLines = []
        let j = i
        while (j < lines.length && /^(    |\t)/.test(lines[j])) {
          const t = lines[j].replace(/^(    |\t)/, '')
          if (/^[-*+]\s/.test(t) || /^\d+\.\s/.test(t)) break
          codeLines.push(t)
          j++
        }
        const codeContent = codeLines.join('\n')
        const ct = getCodeTheme(codeThemeId)
        const codeBlockStyle = T.codeBlock || `margin:16px 0;padding:14px 18px;background:${ct.block.bg};border-radius:8px;overflow:auto;font-family:Consolas,Monaco,monospace;font-size:14px;line-height:1.5;border:1px solid ${ct.block.border};white-space:pre-wrap;word-break:break-word;color:${ct.colors.default}`
        const highlighted = syntaxHighlight(codeContent, '', codeThemeId)
        html += `<pre style="${codeBlockStyle}" data-lang=""><code style="background:transparent;padding:0;font-size:inherit">${highlighted}</code></pre>`
        i = j - 1
        continue
      }
    }
    // GitHub 风格警告框: > [!TIP] / > [!NOTE] / > [!IMPORTANT] / > [!WARNING] / > [!CAUTION]（主题适配 emoji + 配色）
    const alertMatch = line.match(/^>\s*\[\!(TIP|NOTE|IMPORTANT|WARNING|CAUTION)\]\s*$/i)
    if (alertMatch) {
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      closeList()
      const kind = alertMatch[1].toUpperCase()
      const labels = { TIP: '建议', NOTE: '提醒', IMPORTANT: '重要', WARNING: '警告', CAUTION: '注意' }
      const label = labels[kind] || kind
      const alertCfg = getAlertBoxConfig(themeId, layoutId, kind)
      const bodyLines = []
      let j = i + 1
      while (j < lines.length && /^>\s?/.test(lines[j])) {
        bodyLines.push(lines[j].replace(/^>\s?/, ''))
        j++
      }
      i = j - 1
      const body = bodyLines.filter((ln) => ln.trim() !== '').map((ln) => processInline(allowU(escapeHtml(ln), T))).join('<br>')
      const bodyHtml = body ? `<p style="margin:0;padding:4px 0 0 0;line-height:1.6">${body}</p>` : ''
      // 1×1 table 渲染：粘贴到公众号可保留边框/背景，且不算引用、利于原创声明
      html += `<table style="width:100%;border-collapse:collapse;border:none"><tr><td style="${alertCfg.style}"><span style="margin-right:6px" role="img" aria-hidden="true">${alertCfg.emoji}</span><strong style="font-weight:600">${escapeHtml(label)}</strong>${bodyHtml}</td></tr></table>`
      continue
    }

    const blockquoteMatch = line.match(/^(>+)\s?(.*)$/)
    if (blockquoteMatch) {
      const level = blockquoteMatch[1].length
      const inner = blockquoteMatch[2] || ''
      if (!inBlockquote) {
        html += `<blockquote style="${T.blockquote}">`
        inBlockquote = true
      }
      const q = level > 1 ? '<blockquote style="margin:8px 0;padding-left:12px;border-left:3px solid rgba(0,0,0,0.1)">'.repeat(level - 1) : ''
      const qClose = level > 1 ? '</blockquote>'.repeat(level - 1) : ''
      html += q + processInline(allowU(escapeHtml(inner), T)) + qClose + '<br>'
      continue
    }
    if (inBlockquote) {
      html += '</blockquote>'
      inBlockquote = false
    }

    const ulMatch = line.match(/^(\s*)[-*+]\s+(.*)$/)
    if (ulMatch) {
      const indentStr = ulMatch[1] || ''
      const indentLen = indentStr.replace(/\t/g, '  ').length
      const level = Math.floor(indentLen / 2)
      const content = ulMatch[2]
      if (!inList || listType !== 'ul') {
        if (inList) {
          while (listNestDepth > 0) { html += `</${listType === 'ol' ? 'ol' : 'ul'}></li>`; listNestDepth-- }
          html += listType === 'ol' ? '</ol>' : '</ul>'
        }
        html += '<ul style="padding-left:24px;margin:16px 0">'
        inList = true
        listType = 'ul'
      }
      while (listNestDepth > level) { html += '</ul></li>'; listNestDepth-- }
      for (let d = listNestDepth; d < level; d++) {
        html += '<ul style="padding-left:24px;margin:8px 0">'
        listNestDepth++
      }
      html += '<li style="margin:8px 0;">' + renderTaskOrListItem(content) + '</li>'
      continue
    }
    const olMatch = line.match(/^(\s*)(\d+)\.\s+(.*)$/)
    if (olMatch) {
      const indentStr = olMatch[1] || ''
      const indentLen = indentStr.replace(/\t/g, '  ').length
      const level = Math.floor(indentLen / 2)
      const num = parseInt(olMatch[2], 10)
      const rest = olMatch[3]
      if (!inList || listType !== 'ol') {
        if (inList) {
          while (listNestDepth > 0) { html += `</${listType === 'ol' ? 'ol' : 'ul'}></li>`; listNestDepth-- }
          html += listType === 'ul' ? '</ul>' : '</ol>'
        }
        const startAttr = (num !== 1) ? ` start="${num}"` : ''
        html += `<ol style="padding-left:24px;margin:16px 0"${startAttr}>`
        inList = true
        listType = 'ol'
      }
      while (listNestDepth > level) { html += '</ol></li>'; listNestDepth-- }
      for (let d = listNestDepth; d < level; d++) {
        html += '<ol style="padding-left:24px;margin:8px 0">'
        listNestDepth++
      }
      html += '<li style="margin:8px 0;">' + wrapListItemStrong(processInline(allowU(escapeHtml(rest), T))) + '</li>'
      continue
    }
    closeList()

    const defListColon = line.match(/^:\s+(.*)$/)
    if (defListColon) {
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      closeList()
      if (!inDefList) { html += '<dl style="margin:16px 0">'; inDefList = true }
      let defContent = defListColon[1]
      let j = i + 1
      while (j < lines.length && /^[ \t]+\S/.test(lines[j]) && !/^[ \t]*:/.test(lines[j]) && !/^[ \t]{4,}/.test(lines[j])) {
        defContent += ' ' + lines[j].trim()
        j++
      }
      const ddParts = []
      while (j < lines.length) {
        const ln2 = lines[j]
        if (/^[ \t]{4,}/.test(ln2)) {
          const codeLines = []
          while (j < lines.length && /^[ \t]{4,}/.test(lines[j])) {
            codeLines.push(lines[j].replace(/^[ \t]{4,}/, ''))
            j++
          }
          ddParts.push(`<pre style="margin:8px 0;padding:12px;background:#f5f5f5;border-radius:4px;overflow:auto"><code>${escapeHtml(codeLines.join('\n'))}</code></pre>`)
          continue
        }
        if (/^[ \t]+\S/.test(ln2) && !/^[ \t]*:/.test(ln2)) {
          ddParts.push(`<p style="margin:4px 0">${processInline(allowU(escapeHtml(ln2.trim()), T))}</p>`)
          j++
          continue
        }
        break
      }
      html += `<dd style="margin:4px 0 16px 24px"><p style="margin:4px 0">${processInline(allowU(escapeHtml(defContent), T))}</p>${ddParts.join('')}</dd>`
      i = j - 1
      continue
    }

    const defListCompact = line.match(/^[ \t]{2,}~[ \t]+(.*)$/)
    if (defListCompact) {
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      closeList()
      if (!inDefList) { html += '<dl style="margin:16px 0">'; inDefList = true }
      html += `<dd style="margin:4px 0 8px 24px">${processInline(allowU(escapeHtml(defListCompact[1]), T))}</dd>`
      continue
    }

    const nextIsDef = i + 1 < lines.length && /^[ \t]*:/.test(lines[i + 1])
    const defListTerm = nextIsDef && line.trim() !== '' && !line.match(/^[#>\-\*\+]/) && !line.match(/^\s*\d+\./) && !line.match(/^\s*\|/)
    if (defListTerm) {
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      closeList()
      if (!inDefList) { html += '<dl style="margin:16px 0">'; inDefList = true }
      html += `<dt style="font-weight:600;margin:8px 0">${processInline(allowU(escapeHtml(line), T))}</dt>`
      continue
    }

    if (inDefList) {
      html += '</dl>'
      inDefList = false
    }

    const imgMatch = line.match(/^!\[([^\]]*)\]\(([^)]+)\)\s*$/)
    if (imgMatch) {
      const rawUrl = imgMatch[2].trim().split(/\s+/)[0].trim().split('|')[0]
      const u = escapeHtml(resolveImgSrc(rawUrl))
      const a = escapeHtml(imgMatch[1] || '')
      const caption = (a && T.imageCaption) ? `<span style="${T.imageCaption}">${a}</span>` : ''
      html += `<p style="${T.p}"><img src="${u}" alt="${a}" style="${imgStyle}">${caption}</p>`
      continue
    }

    if (line.trim() !== '') {
      html += `<p style="${T.p}">${processInline(allowU(escapeHtml(line), T))}</p>`
    }
  }

  if (inBlockquote) html += '</blockquote>'
  closeList()
  if (inDefList) html += '</dl>'

  if (footnoteOrder.length) {
    html += '<hr class="footnotes-sep" style="border:none;border-top:1px solid #e5e5e5;margin:24px 0">'
    html += '<section class="footnotes" style="font-size:14px;color:#666">'
    html += '<ol class="footnotes-list" style="padding-left:24px">'
    footnoteOrder.forEach((id, idx) => {
      const num = idx + 1
      const raw = footnoteDefs[id]
      const paras = raw.split(/\n\n+/)
      const cnt = fnRefCount[id] || 1
      const backrefs = []
      for (let r = 0; r < cnt; r++) {
        const refId = r === 0 ? `fnref${num}` : `fnref${num}:${r}`
        backrefs.push(`<a href="#${refId}" class="footnote-backref" style="font-size:12px;color:#1890ff;text-decoration:none">↩︎</a>`)
      }
      const backref = backrefs.join(' ')
      const body = paras.map((p, pi) => {
        const content = processInline(allowU(escapeHtml(p), T))
        return `<p style="margin:4px 0">${content}${pi === paras.length - 1 ? ' ' + backref : ''}</p>`
      }).join('')
      html += `<li id="fn${num}" class="footnote-item" style="margin:8px 0">${body}</li>`
    })
    html += '</ol></section>'
  }

  return html
}

/** 预览与生成文章内容头部：本文由稿定助手排版 */
const ARTICLE_HEADER_HTML = '<p style="margin-bottom: 0px;"><span leaf="" data-pm-slice="1 1 [&quot;para&quot;,{&quot;tagName&quot;:&quot;section&quot;,&quot;attributes&quot;:{&quot;data-tool&quot;:&quot;公众号排版&quot;,&quot;style&quot;:&quot;margin:0; padding:16px 14px; font-family:Optima,\'Microsoft YaHei\',PingFang SC,serif; font-size:16px; color:#4a3f47; line-height:1.85; word-break:break-word; background:linear-gradient(180deg,#fff5f7 0%,#fce7ef 100%); border-radius:12px; border:1px solid #fbcfe8;&quot;,&quot;data-pm-slice&quot;:&quot;0 0 []&quot;},&quot;namespaceURI&quot;:&quot;http://www.w3.org/1999/xhtml&quot;},&quot;para&quot;,{&quot;tagName&quot;:&quot;p&quot;,&quot;attributes&quot;:{&quot;style&quot;:&quot;text-align: left;&quot;},&quot;namespaceURI&quot;:&quot;http://www.w3.org/1999/xhtml&quot;}]"><span textstyle="" style="font-size: 16px; color: rgb(136, 136, 136)">本文由</span><a class="weapp_text_link js_weapp_entry" style="color: rgb(136, 136, 136);" data-unique-id="mmfmm9jw-cwxdhm" data-miniprogram-type="text" data-miniprogram-appid="wxe6248c9d07f819cb" data-miniprogram-path="pages/drafts/drafts" data-miniprogram-nickname="稿定助手" data-miniprogram-servicetype="0" data-miniprogram-applink=""><span textstyle="" style="font-size: 16px; color: rgb(136, 136, 136)">稿定助手</span></a><span textstyle="" style="font-size: 16px; color: rgb(136, 136, 136)">排版，</span><a class="weapp_text_link js_weapp_entry" style="letter-spacing: 0.578px; color: rgb(136, 136, 136);" data-unique-id="mmfmm9jw-cwxdhm" data-miniprogram-type="text" data-miniprogram-appid="wxe6248c9d07f819cb" data-miniprogram-path="pages/drafts/drafts" data-miniprogram-nickname="稿定助手" data-miniprogram-servicetype="0" data-miniprogram-applink=""><span textstyle="" style="font-size: 16px; color: rgb(136, 136, 136)">稿定助手</span></a><span textstyle="" style="font-size: 16px; color: rgb(136, 136, 136)">，手机也能轻松排版！</span></span></p>'

export function getFullHtml(content, themeId, imageStyleId, layoutId = 'default', _imageResolver, codeThemeId = 'vscode-dark') {
  const theme = getResolvedTheme(themeId, layoutId)
  const body = parseMarkdown(content, themeId, imageStyleId, true, layoutId, null, codeThemeId)
  return `<section data-tool="公众号排版" style="${theme.section}">\n${ARTICLE_HEADER_HTML}\n${body}\n</section>`
}
