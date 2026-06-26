#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { execWenyan } = require('./wenyan_runner');

const BASE_DIR = __dirname;
const CATALOG_PATH = path.join(BASE_DIR, 'theme_catalog.json');
const SAMPLE_MD_PATH = path.join(BASE_DIR, 'theme_preview_sample.md');
const PREVIEW_DIR = path.join(BASE_DIR, 'theme_previews');
const PREVIEW_HTML_DIR = path.join(PREVIEW_DIR, 'html');
const GALLERY_HTML_PATH = path.join(PREVIEW_DIR, 'theme-gallery.html');
const GALLERY_IMAGE_PATH = path.join(PREVIEW_DIR, 'theme-gallery.png');

const catalog = JSON.parse(fs.readFileSync(CATALOG_PATH, 'utf-8'));

const DEFAULT_THEME_ID = catalog.default_theme;
const DEFAULT_HIGHLIGHT = catalog.default_highlight;

function getCatalogThemes() {
    return catalog.themes;
}

function getThemeMap() {
    return new Map(getCatalogThemes().map((theme) => [theme.id, theme]));
}

function previewPath(themeId) {
    return path.join(PREVIEW_DIR, `${themeId}.png`);
}

function previewHtmlPath(themeId) {
    return path.join(PREVIEW_HTML_DIR, `${themeId}.html`);
}

function ensureDir(dirPath) {
    fs.mkdirSync(dirPath, { recursive: true });
}

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function getInstalledWenyanThemes() {
    try {
        const output = execWenyan(['theme', '-l'], { encoding: 'utf-8', timeout: 20000 });
        const themes = new Map();
        for (const line of output.split('\n')) {
            const trimmed = line.trim();
            if (!trimmed.startsWith('- ')) continue;
            const item = trimmed.slice(2);
            const colonIndex = item.indexOf(':');
            const id = (colonIndex >= 0 ? item.slice(0, colonIndex) : item).trim();
            const description = colonIndex >= 0 ? item.slice(colonIndex + 1).trim() : '';
            themes.set(id, description);
        }
        return themes;
    } catch {
        return new Map();
    }
}

function availableThemeIds() {
    const ids = new Set(getCatalogThemes().map((theme) => theme.id));
    for (const key of getInstalledWenyanThemes().keys()) {
        ids.add(key);
    }
    return Array.from(ids).sort();
}

function resolveTheme(themeId = DEFAULT_THEME_ID, highlightOverride) {
    const requested = (themeId || DEFAULT_THEME_ID).trim() || DEFAULT_THEME_ID;
    const themeMap = getThemeMap();
    const installedThemes = getInstalledWenyanThemes();
    let resolved = themeMap.get(requested);

    if (!resolved) {
        const possibleCssPath = path.resolve(requested);
        if (fs.existsSync(possibleCssPath)) {
            resolved = {
                id: path.basename(possibleCssPath, path.extname(possibleCssPath)),
                label: path.basename(possibleCssPath, path.extname(possibleCssPath)),
                name_zh: '外部 CSS',
                source: 'custom',
                css_path: possibleCssPath,
                description: '使用外部 CSS 文件的自定义主题。',
                accent: '#334155',
                preview_background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
            };
        } else if (installedThemes.has(requested)) {
            resolved = {
                id: requested,
                label: requested,
                name_zh: '已安装主题',
                source: 'builtin',
                wenyan_theme: requested,
                description: installedThemes.get(requested) || '本地已安装的 wenyan 主题。',
                accent: '#334155',
                preview_background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
            };
        } else {
            throw new Error(`未知主题: ${requested}。\n可用主题: ${availableThemeIds().join(', ')}`);
        }
    }

    const theme = { ...resolved };
    theme.resolved_highlight = highlightOverride || theme.highlight || DEFAULT_HIGHLIGHT;
    theme.preview_path = previewPath(theme.id);
    theme.preview_html_path = previewHtmlPath(theme.id);
    theme.wenyan_theme = theme.wenyan_theme || '';
    if (theme.source === 'custom') {
        theme.css_path_abs = path.isAbsolute(theme.css_path)
            ? theme.css_path
            : path.resolve(BASE_DIR, theme.css_path);
    } else {
        theme.css_path_abs = '';
    }
    return theme;
}

function buildPublishArgs(filePath, theme) {
    const args = ['publish', '-f', filePath];
    if (theme.source === 'custom') {
        args.push('-c', theme.css_path_abs);
    } else {
        args.push('-t', theme.wenyan_theme);
    }
    args.push('-h', theme.resolved_highlight);
    return args;
}

function buildRenderArgs(filePath, theme) {
    const args = ['render', '-f', filePath];
    if (theme.source === 'custom') {
        args.push('-c', theme.css_path_abs);
    } else {
        args.push('-t', theme.wenyan_theme);
    }
    args.push('-h', theme.resolved_highlight);
    return args;
}

function renderTheme(theme) {
    return execWenyan(buildRenderArgs(SAMPLE_MD_PATH, theme), {
        encoding: 'utf-8',
        timeout: 30000,
    }).trim();
}

function previewDocument(theme, renderedHtml) {
    const title = `${theme.label}${theme.name_zh ? ` / ${theme.name_zh}` : ''}`;
    const accent = theme.accent || '#334155';
    const background = theme.preview_background || 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)';
    const command = `node publish.js article.md ${theme.id} ${theme.resolved_highlight}`;

    return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapeHtml(title)}</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 48px;
      min-height: 100vh;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: ${background};
      color: #0f172a;
    }
    .shell { width: 1040px; margin: 0 auto; }
    .hero {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 24px;
      margin-bottom: 28px;
    }
    .chip {
      display: inline-block;
      padding: 6px 12px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.7);
      color: ${accent};
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }
    h1 { margin: 12px 0 10px; font-size: 34px; line-height: 1.15; }
    .desc {
      margin: 0;
      max-width: 600px;
      color: #334155;
      font-size: 16px;
      line-height: 1.65;
    }
    .meta {
      min-width: 280px;
      padding: 18px 20px;
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.75);
      box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
      backdrop-filter: blur(10px);
    }
    .meta-item { margin: 0 0 10px; font-size: 14px; color: #475569; }
    .meta-item:last-child { margin-bottom: 0; }
    .meta-label {
      display: block;
      margin-bottom: 4px;
      font-size: 12px;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .phone {
      padding: 22px;
      border-radius: 30px;
      background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
      box-shadow: 0 24px 80px rgba(15, 23, 42, 0.14);
      border: 1px solid rgba(255, 255, 255, 0.8);
    }
    .bar {
      width: 120px;
      height: 8px;
      margin: 0 auto 18px;
      border-radius: 999px;
      background: #cbd5e1;
    }
    .content {
      padding: 18px 24px 26px;
      border-radius: 24px;
      background: #ffffff;
    }
    #wenyan { margin: 0; }
  </style>
</head>
<body>
  <div class="shell">
    <div class="hero">
      <div>
        <span class="chip">${escapeHtml(theme.source)}</span>
        <h1>${escapeHtml(title)}</h1>
        <p class="desc">${escapeHtml(theme.description || '')}</p>
      </div>
      <div class="meta">
        <p class="meta-item"><span class="meta-label">Theme ID</span>${escapeHtml(theme.id)}</p>
        <p class="meta-item"><span class="meta-label">Default Highlight</span>${escapeHtml(theme.resolved_highlight)}</p>
        <p class="meta-item"><span class="meta-label">Publish Command</span>${escapeHtml(command)}</p>
      </div>
    </div>
    <div class="phone">
      <div class="bar"></div>
      <div class="content">
        ${renderedHtml}
      </div>
    </div>
  </div>
</body>
</html>`;
}

function galleryDocument(themes) {
    const rows = [];
    for (let index = 0; index < themes.length; index += 3) {
        const chunk = themes.slice(index, index + 3);
        const cells = chunk.map((theme) => `
          <td class="grid-cell">
            <article class="card">
              <img src="${escapeHtml(path.basename(previewPath(theme.id)))}" alt="${escapeHtml(theme.label)}">
              <div class="card-body">
                <div class="card-meta">${escapeHtml(theme.source)} / ${escapeHtml(theme.resolved_highlight)}</div>
                <h2>${escapeHtml(theme.label)} <span>${escapeHtml(theme.name_zh || '')}</span></h2>
                <p>${escapeHtml(theme.description || '')}</p>
                <code>node publish.js article.md ${escapeHtml(theme.id)}</code>
              </div>
            </article>
          </td>`).join('');
        rows.push(`<tr>${cells}</tr>`);
    }

    return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>wechat-toolkit Theme Gallery</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #0f172a;
      background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
    }
    .page {
      width: min(1320px, calc(100vw - 48px));
      margin: 0 auto;
      padding: 48px 0 64px;
    }
    h1 { margin: 0 0 12px; font-size: 42px; }
    .lead {
      max-width: 780px;
      margin: 0 0 32px;
      color: #475569;
      line-height: 1.7;
      font-size: 18px;
    }
    .grid-table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 24px 24px;
      table-layout: fixed;
      margin: 0 -24px;
    }
    .grid-cell {
      width: 33.3333%;
      vertical-align: top;
    }
    .card {
      overflow: hidden;
      border-radius: 24px;
      background: rgba(255, 255, 255, 0.88);
      box-shadow: 0 20px 50px rgba(15, 23, 42, 0.12);
    }
    .card img {
      display: block;
      width: 100%;
      height: 320px;
      object-fit: cover;
      object-position: top center;
    }
    .card-body { padding: 18px 20px 22px; }
    .card-meta {
      margin-bottom: 8px;
      font-size: 12px;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .card h2 { margin: 0 0 10px; font-size: 24px; }
    .card h2 span {
      color: #64748b;
      font-size: 16px;
      font-weight: 500;
    }
    .card p {
      min-height: 72px;
      margin: 0 0 16px;
      color: #334155;
      line-height: 1.65;
    }
    code {
      display: block;
      padding: 10px 12px;
      border-radius: 12px;
      color: #0f172a;
      background: #f8fafc;
      overflow-wrap: anywhere;
    }
  </style>
</head>
<body>
  <main class="page">
    <h1>wechat-toolkit Theme Gallery</h1>
    <p class="lead">所有 bundled 主题都在这里。每张图都来自同一篇示例文章，方便直接比较标题、引用、代码块和表格的风格差异。</p>
    <table class="grid-table">
      <tbody>
        ${rows.join('')}
      </tbody>
    </table>
  </main>
</body>
</html>`;
}

function generatePreview(themeId) {
    const theme = resolveTheme(themeId);
    ensureDir(PREVIEW_DIR);
    ensureDir(PREVIEW_HTML_DIR);

    const renderedHtml = renderTheme(theme);
    const htmlPath = previewHtmlPath(theme.id);
    const imagePath = previewPath(theme.id);
    fs.writeFileSync(htmlPath, previewDocument(theme, renderedHtml), 'utf-8');

    execFileSync('wkhtmltoimage', [
        '--enable-local-file-access',
        '--quality', '92',
        '--width', '1160',
        '--height', '1740',
        htmlPath,
        imagePath,
    ], {
        stdio: 'pipe',
        timeout: 60000,
    });

    return imagePath;
}

function generatePreviews(themeIds) {
    const ids = themeIds && themeIds.length > 0
        ? themeIds
        : getCatalogThemes().map((theme) => theme.id);

    const generated = ids.map((themeId) => generatePreview(themeId));
    const themes = ids.map((themeId) => resolveTheme(themeId));
    fs.writeFileSync(GALLERY_HTML_PATH, galleryDocument(themes), 'utf-8');
    execFileSync('wkhtmltoimage', [
        '--enable-local-file-access',
        '--quality', '92',
        '--width', '1400',
        '--height', '2550',
        GALLERY_HTML_PATH,
        GALLERY_IMAGE_PATH,
    ], {
        stdio: 'pipe',
        timeout: 60000,
    });
    return generated;
}

function printThemeList() {
    console.log('可用主题：');
    for (const item of getCatalogThemes()) {
        const theme = resolveTheme(item.id);
        const source = theme.source === 'builtin' ? '内置' : '自定义';
        console.log(`- ${theme.id}: ${theme.label} / ${theme.name_zh || ''} / ${source} / 默认高亮 ${theme.resolved_highlight}`);
        console.log(`  ${theme.description || ''}`);
        console.log(`  预览图: ${theme.preview_path}`);
    }
    console.log(`\n总览页: ${GALLERY_HTML_PATH}`);
    console.log(`拼图总览: ${GALLERY_IMAGE_PATH}`);
}

function runCli(argv = process.argv.slice(2)) {
    const [command, ...rest] = argv;

    if (!command || command === '-h' || command === '--help') {
        console.log(`用法:
  node theme_catalog.js list
  node theme_catalog.js resolve-json <theme-id> [highlight]
  node theme_catalog.js generate-previews [theme-id ...]`);
        return 0;
    }

    if (command === 'list') {
        printThemeList();
        return 0;
    }

    if (command === 'resolve-json') {
        const theme = resolveTheme(rest[0], rest[1]);
        console.log(JSON.stringify(theme, null, 2));
        return 0;
    }

    if (command === 'generate-previews') {
        const generated = generatePreviews(rest);
        for (const item of generated) {
            console.log(item);
        }
        console.log(GALLERY_HTML_PATH);
        console.log(GALLERY_IMAGE_PATH);
        return 0;
    }

    console.error(`未知命令: ${command}`);
    return 1;
}

module.exports = {
    BASE_DIR,
    PREVIEW_DIR,
    GALLERY_HTML_PATH,
    GALLERY_IMAGE_PATH,
    DEFAULT_THEME_ID,
    DEFAULT_HIGHLIGHT,
    getCatalogThemes,
    resolveTheme,
    buildPublishArgs,
    generatePreviews,
    printThemeList,
};

if (require.main === module) {
    process.exit(runCli());
}
