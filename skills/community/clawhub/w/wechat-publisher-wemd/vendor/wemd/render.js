#!/usr/bin/env node
/**
 * WeMD rendering CLI - 微信公众号 Markdown 渲染命令行工具
 *
 * 用法:
 *   node render.js --markdown article.md --theme Luxury-Gold
 *   echo '{"markdown":"# Hi","theme":"Template"}' | node render.js --json
 *
 * 输出: JSON { ok, html, theme, error }
 */

const fs = require("fs");
const path = require("path");

const { createMarkdownParser, processHtml } = require("./core-dist/index.js");

// ── CSS 变量展开（从 WeMD 源码移植，纯文本处理） ──────────────────────────────

function findNextVarStart(value, startIndex) {
  let quote = null, escapeNext = false;
  for (let i = startIndex; i < value.length; i++) {
    const c = value[i];
    if (escapeNext) { escapeNext = false; continue; }
    if (c === "\\") { escapeNext = true; continue; }
    if (quote) { if (c === quote) quote = null; continue; }
    if (c === "'" || c === '"') { quote = c; continue; }
    if (c === "v" && value.slice(i, i + 4).toLowerCase() === "var(") return i;
  }
  return -1;
}

function findMatchingParen(value, openIndex) {
  let depth = 0, quote = null, escapeNext = false;
  for (let i = openIndex; i < value.length; i++) {
    const c = value[i];
    if (escapeNext) { escapeNext = false; continue; }
    if (c === "\\") { escapeNext = true; continue; }
    if (quote) { if (c === quote) quote = null; continue; }
    if (c === "'" || c === '"') { quote = c; continue; }
    if (c === "(") { depth++; continue; }
    if (c === ")") { depth--; if (depth === 0) return i; }
  }
  return -1;
}

function splitVarArgs(input) {
  let depth = 0, quote = null, escapeNext = false;
  for (let i = 0; i < input.length; i++) {
    const c = input[i];
    if (escapeNext) { escapeNext = false; continue; }
    if (c === "\\") { escapeNext = true; continue; }
    if (quote) { if (c === quote) quote = null; continue; }
    if (c === "'" || c === '"') { quote = c; continue; }
    if (c === "(") { depth++; continue; }
    if (c === ")") { depth--; continue; }
    if (c === "," && depth === 0) {
      return [input.slice(0, i).trim(), input.slice(i + 1).trim()];
    }
  }
  return [input.trim(), undefined];
}

function extractCustomProperties(css) {
  const vars = new Map();
  const regex = /(--[\w-]+)\s*:\s*([^;]+);/g;
  let m;
  while ((m = regex.exec(css)) !== null) {
    vars.set(m[1].trim(), m[2].trim());
  }
  return vars;
}

function resolveVarReferences(value, vars, resolving) {
  let result = "", cursor = 0;
  while (cursor < value.length) {
    const vi = findNextVarStart(value, cursor);
    if (vi < 0) { result += value.slice(cursor); break; }
    result += value.slice(cursor, vi);
    const op = vi + 3;
    const ci = findMatchingParen(value, op);
    if (ci < 0) { result += value.slice(vi); break; }
    const rawArgs = value.slice(op + 1, ci);
    const [varName, fallback] = splitVarArgs(rawArgs);
    let replacement = null;
    if (varName.startsWith("--") && !resolving.has(varName)) {
      const vv = vars.get(varName);
      if (vv !== undefined) {
        const nr = new Set(resolving); nr.add(varName);
        const resolved = resolveVarReferences(vv, vars, nr);
        replacement = (resolved.includes("var(") && fallback)
          ? resolveVarReferences(fallback, vars, new Set(resolving))
          : resolved;
      } else if (fallback) {
        replacement = resolveVarReferences(fallback, vars, new Set(resolving));
      }
    } else if (fallback) {
      replacement = resolveVarReferences(fallback, vars, new Set(resolving));
    }
    result += replacement ?? `var(${rawArgs})`;
    cursor = ci + 1;
  }
  return result;
}

function stripCustomPropertyDeclarations(css) {
  return css.replace(/([^{}]*)\{([^{}]*)\}/gs, (_m, sel, body) => {
    const lines = body.split(";").map(l => l.trim()).filter(l => l.length > 0 && !l.startsWith("--"));
    if (lines.length === 0) return "";
    return `${sel.trim()} { ${lines.join("; ")}; }`;
  });
}

function expandCSSVariables(css) {
  if (!css) return css;
  const hasVar = css.includes("var(");
  const vars = extractCustomProperties(css);
  if (!hasVar && vars.size === 0) return css;
  let expanded = css;
  if (hasVar) {
    const resolved = new Map();
    for (const [name, value] of vars) {
      resolved.set(name, resolveVarReferences(value, vars, new Set([name])));
    }
    expanded = resolveVarReferences(expanded, resolved, new Set());
  }
  if (vars.size > 0) expanded = stripCustomPropertyDeclarations(expanded);
  return expanded;
}

// ── 链接转脚注（简化版） ────────────────────────────────────────────────────

function convertLinksToFootnotes(html) {
  const links = [];
  const processed = html.replace(/<a\s+href="([^"]*)"[^>]*>(.*?)<\/a>/gi, (m, href, text) => {
    if (!href || href.startsWith("#") || href.startsWith("javascript:")) return text;
    links.push(href);
    const idx = links.length;
    return `${text}<sup style="font-size:12px;color:#1e6bb8;">[${idx}]</sup>`;
  });
  if (links.length === 0) return html;
  let footnoteHtml = '<section style="border-top:1px solid #ddd;margin-top:30px;padding-top:15px;font-size:13px;color:#888;">';
  footnoteHtml += '<p style="font-weight:bold;margin-bottom:8px;">引用链接</p>';
  links.forEach((url, i) => {
    footnoteHtml += `<p style="margin:2px 0;word-break:break-all;"><span style="color:#1e6bb8;">[${i+1}]</span> ${url}</p>`;
  });
  footnoteHtml += "</section>";
  return processed + footnoteHtml;
}

// ── checkbox 转 emoji ───────────────────────────────────────────────────────

function convertCheckboxesToEmoji(html) {
  let r = html.replace(/<input[^>]*checked[^>]*>/gi, "✅ ");
  r = r.replace(/<input[^>]*type=["']checkbox["'][^>]*>/gi, "⬜ ");
  return r;
}

// ── 微信兼容后处理 ──────────────────────────────────────────────────────────

function wechatPostProcess(html) {
  let result = html.replace(
    /<li([^>]*)>\s*<section([^>]*)>([\s\S]*?)<\/section>\s*<\/li>/gi,
    (m, liAttrs, secAttrs, inner) => `<li${liAttrs}><span${secAttrs}>${inner}</span></li>`
  );
  return result;
}

// ── 主渲染函数 ──────────────────────────────────────────────────────────────

function render(markdown, themeCss) {
  const parser = createMarkdownParser();
  const rawHtml = parser.render(markdown);
  const sourceHtml = convertLinksToFootnotes(rawHtml);
  const expandedCss = expandCSSVariables(themeCss);
  const styledHtml = processHtml(sourceHtml, expandedCss, true, true);
  const withCheckbox = convertCheckboxesToEmoji(styledHtml);
  const finalHtml = wechatPostProcess(withCheckbox);
  return finalHtml;
}

// ── 主题加载 ────────────────────────────────────────────────────────────────

const THEMES_DIR = path.join(__dirname, "themes");
const BASE_CSS_PATH = path.join(THEMES_DIR, "_base.css");
const CODE_CSS_PATH = path.join(THEMES_DIR, "_code-github.css");

let _baseCss = null;
let _codeCss = null;

function getBaseCss() {
  if (_baseCss === null) {
    _baseCss = fs.existsSync(BASE_CSS_PATH) ? fs.readFileSync(BASE_CSS_PATH, "utf-8") : "";
  }
  return _baseCss;
}

function getCodeCss() {
  if (_codeCss === null) {
    _codeCss = fs.existsSync(CODE_CSS_PATH) ? fs.readFileSync(CODE_CSS_PATH, "utf-8") : "";
  }
  return _codeCss;
}

function listThemes() {
  if (!fs.existsSync(THEMES_DIR)) return [];
  return fs.readdirSync(THEMES_DIR)
    .filter(f => f.endsWith(".css") && !f.startsWith("_"))
    .map(f => f.replace(/\.css$/, ""));
}

function loadThemeCss(themeName) {
  const cssPath = path.join(THEMES_DIR, `${themeName}.css`);
  if (!fs.existsSync(cssPath)) {
    throw new Error(`Theme not found: ${themeName}. Available: ${listThemes().join(", ")}`);
  }
  const themeCss = fs.readFileSync(cssPath, "utf-8");
  return getBaseCss() + "\n" + themeCss + "\n" + getCodeCss();
}

// ── CLI ─────────────────────────────────────────────────────────────────────

function main() {
  const args = process.argv.slice(2);

  if (args.includes("--list-themes")) {
    console.log(JSON.stringify({ themes: listThemes() }));
    process.exit(0);
  }

  let markdown = "";
  let themeName = "Template";

  if (args.includes("--json")) {
    const input = fs.readFileSync(0, "utf-8");
    const data = JSON.parse(input);
    markdown = data.markdown || "";
    themeName = data.theme || themeName;
    if (data.markdown_path) {
      markdown = fs.readFileSync(data.markdown_path, "utf-8");
    }
  } else {
    const mdIdx = args.indexOf("--markdown");
    if (mdIdx >= 0 && args[mdIdx + 1]) {
      markdown = fs.readFileSync(args[mdIdx + 1], "utf-8");
    }
    const thIdx = args.indexOf("--theme");
    if (thIdx >= 0 && args[thIdx + 1]) {
      themeName = args[thIdx + 1];
    }
  }

  if (!markdown) {
    console.error(JSON.stringify({ ok: false, error: "No markdown input" }));
    process.exit(1);
  }

  try {
    const css = loadThemeCss(themeName);
    const html = render(markdown, css);
    console.log(JSON.stringify({ ok: true, html, theme: themeName }));
  } catch (e) {
    console.error(JSON.stringify({ ok: false, error: e.message }));
    process.exit(1);
  }
}

main();
