/**
 * 轻量级代码语法高亮（纯 JS 无依赖，输出 inline 样式）
 * 支持: javascript, typescript, python, json, html, css, bash, java, sql, xml, go, php
 * themeId: 使用 codeThemes 中的主题，与文章主题独立
 */
import { getCodeTheme } from './codeThemes.js'

function escapeHtml(str) {
  if (!str) return ''
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

function span(style, text) {
  return `<span style="color:${style}">${text}</span>`
}

function highlightJS(code, C) {
  const parts = []
  const len = code.length
  const tokens = []
  const re = /(\/\/[^\n]*|\/\*[\s\S]*?\*\/)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|`(?:[^`\\]|\\.)*`)|(\/(?:[^/\\]|\\.)+\/[gimsuy]*)|(\b(?:0x[\da-fA-F]+|0o[0-7]+|0b[01]+|\d+\.?\d*(?:e[+-]?\d+)?)\b)|(\b(?:const|let|var|function|return|if|else|for|while|do|switch|case|break|continue|try|catch|finally|throw|new|class|extends|import|export|default|from|async|await|typeof|instanceof|in|of|true|false|null|undefined|this|super)\b)|(\b([a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?=\())/g
  let m, lastIdx = 0
  while ((m = re.exec(code)) !== null) {
    if (m.index > lastIdx) tokens.push({ t: 'd', v: code.slice(lastIdx, m.index), i: lastIdx })
    if (m[1]) tokens.push({ t: 'c', v: m[1], i: m.index })
    else if (m[2]) tokens.push({ t: 's', v: m[2], i: m.index })
    else if (m[3]) tokens.push({ t: 'r', v: m[3], i: m.index })
    else if (m[4]) tokens.push({ t: 'n', v: m[4], i: m.index })
    else if (m[5]) tokens.push({ t: 'k', v: m[5], i: m.index })
    else if (m[6]) tokens.push({ t: 'f', v: m[6], i: m.index })
    lastIdx = m.index + m[0].length
  }
  if (lastIdx < len) tokens.push({ t: 'd', v: code.slice(lastIdx), i: lastIdx })
  for (const tk of tokens) {
    if (tk.t === 'c') parts.push(span(C.comment, escapeHtml(tk.v)))
    else if (tk.t === 's') parts.push(span(C.string, escapeHtml(tk.v)))
    else if (tk.t === 'r') parts.push(span(C.regex, escapeHtml(tk.v)))
    else if (tk.t === 'n') parts.push(span(C.number, escapeHtml(tk.v)))
    else if (tk.t === 'k') parts.push(span(C.keyword, escapeHtml(tk.v)))
    else if (tk.t === 'f') parts.push(span(C.function, escapeHtml(tk.v)))
    else parts.push(span(C.default, escapeHtml(tk.v)))
  }
  return parts.join('')
}

function highlightPython(code, C) {
  const tokens = []
  const allRe = /("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(#[^\n]*)|(\b(?:0x[\da-fA-F]+|0o[0-7]+|0b[01]+|\d+\.?\d*(?:e[+-]?\d+)?[jJ]?)\b)|(\b(?:def|class|if|elif|else|for|while|try|except|finally|with|import|from|as|return|yield|pass|break|continue|and|or|not|in|is|None|True|False|lambda)\b)/g
  let m, lastIdx = 0
  while ((m = allRe.exec(code)) !== null) {
    if (m.index > lastIdx) tokens.push({ t: 'd', v: code.slice(lastIdx, m.index) })
    if (m[1]) tokens.push({ t: 's', v: m[1] })
    else if (m[2]) tokens.push({ t: 'c', v: m[2] })
    else if (m[3]) tokens.push({ t: 'n', v: m[3] })
    else if (m[4]) tokens.push({ t: 'k', v: m[4] })
    lastIdx = m.index + m[0].length
  }
  if (lastIdx < code.length) tokens.push({ t: 'd', v: code.slice(lastIdx) })
  return tokens.map(tk => {
    if (tk.t === 's') return span(C.string, escapeHtml(tk.v))
    if (tk.t === 'c') return span(C.comment, escapeHtml(tk.v))
    if (tk.t === 'n') return span(C.number, escapeHtml(tk.v))
    if (tk.t === 'k') return span(C.keyword, escapeHtml(tk.v))
    return span(C.default, escapeHtml(tk.v))
  }).join('')
}

function highlightJSON(code, C) {
  const parts = []
  const allRe = /("(?:[^"\\]|\\.)*")(\s*:)?|(-?\d+\.?\d*(?:e[+-]?\d+)?)|\b(true|false|null)\b/g
  let m, lastIdx = 0
  while ((m = allRe.exec(code)) !== null) {
    if (m.index > lastIdx) parts.push(span(C.default, escapeHtml(code.slice(lastIdx, m.index))))
    if (m[1]) {
      parts.push(span(m[2]?.includes(':') ? C.attr : C.string, escapeHtml(m[1])))
      if (m[2]) parts.push(span(C.default, escapeHtml(m[2])))
    } else if (m[3]) parts.push(span(C.number, escapeHtml(m[3])))
    else if (m[4]) parts.push(span(C.keyword, escapeHtml(m[4])))
    lastIdx = m.index + m[0].length
  }
  if (lastIdx < code.length) parts.push(span(C.default, escapeHtml(code.slice(lastIdx))))
  return parts.join('')
}

function highlightHTML(code, C) {
  const allRe = /(<!--[\s\S]*?-->)|(<\/?[a-zA-Z][a-zA-Z0-9]*\b)|([a-zA-Z-]+)=|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')/g
  const parts = []
  let m, lastIdx = 0
  while ((m = allRe.exec(code)) !== null) {
    if (m.index > lastIdx) parts.push(span(C.default, escapeHtml(code.slice(lastIdx, m.index))))
    if (m[1]) parts.push(span(C.comment, escapeHtml(m[1])))
    else if (m[2]) parts.push(span(C.tag, escapeHtml(m[2])))
    else if (m[3]) parts.push(span(C.attr, escapeHtml(m[3] + '=')))
    else if (m[4]) parts.push(span(C.string, escapeHtml(m[4])))
    lastIdx = m.index + m[0].length
  }
  if (lastIdx < code.length) parts.push(span(C.default, escapeHtml(code.slice(lastIdx))))
  return parts.join('')
}

function highlightCSS(code, C) {
  const allRe = /(\/\*[\s\S]*?\*\/)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|([.#]?[a-zA-Z_-][a-zA-Z0-9_-]*)\s*\{|([a-zA-Z-]+)\s*:|(#[a-fA-F0-9]{3,8}|rgba?\([^)]+\)|\d+\.?\d*(?:px|%|em|rem)?)/g
  const parts = []
  let m, lastIdx = 0
  while ((m = allRe.exec(code)) !== null) {
    if (m.index > lastIdx) parts.push(span(C.default, escapeHtml(code.slice(lastIdx, m.index))))
    if (m[1]) parts.push(span(C.comment, escapeHtml(m[1])))
    else if (m[2]) parts.push(span(C.string, escapeHtml(m[2])))
    else if (m[3]) parts.push(span(C.tag, escapeHtml(m[3])), span(C.default, ' {'))
    else if (m[4]) parts.push(span(C.attr, escapeHtml(m[4])), span(C.default, ': '))
    else if (m[5]) parts.push(span(C.number, escapeHtml(m[5])))
    lastIdx = m.index + m[0].length
  }
  if (lastIdx < code.length) parts.push(span(C.default, escapeHtml(code.slice(lastIdx))))
  return parts.join('')
}

function highlightBash(code, C) {
  const allRe = /(^#![^\n]*|#[^\n]*)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\b(?:if|then|else|elif|fi|for|do|done|while|until|case|esac|function|return|export|source)\b)|(\$[a-zA-Z_][a-zA-Z0-9_]*|\$\{[^}]+\})/gm
  const parts = []
  let m, lastIdx = 0
  while ((m = allRe.exec(code)) !== null) {
    if (m.index > lastIdx) parts.push(span(C.default, escapeHtml(code.slice(lastIdx, m.index))))
    if (m[1]) parts.push(span(C.comment, escapeHtml(m[1])))
    else if (m[2]) parts.push(span(C.string, escapeHtml(m[2])))
    else if (m[3]) parts.push(span(C.keyword, escapeHtml(m[3])))
    else if (m[4]) parts.push(span(C.param, escapeHtml(m[4])))
    lastIdx = m.index + m[0].length
  }
  if (lastIdx < code.length) parts.push(span(C.default, escapeHtml(code.slice(lastIdx))))
  return parts.join('')
}

const HIGHLIGHTERS = {
  javascript: highlightJS, js: highlightJS, typescript: highlightJS, ts: highlightJS,
  python: highlightPython, py: highlightPython, json: highlightJSON,
  html: highlightHTML, xml: highlightHTML, css: highlightCSS,
  bash: highlightBash, shell: highlightBash, sh: highlightBash,
  java: highlightJS, sql: highlightJS, go: highlightJS, php: highlightJS,
}

export function highlight(code, lang, themeId = 'vscode-dark') {
  if (!code) return ''
  const theme = getCodeTheme(themeId)
  const C = theme.colors
  const normal = (lang || '').toLowerCase().replace(/^lang(uage)?-?/, '')
  const fn = HIGHLIGHTERS[normal]
  if (fn) return fn(code, C)
  return escapeHtml(code)
}
