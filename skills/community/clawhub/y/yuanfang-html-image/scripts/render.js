#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SCRIPT_DIR = __dirname;
const REPO_ROOT = path.join(SCRIPT_DIR, '..', '..');
const DESIGN_DIR = path.join(REPO_ROOT, 'yuanfang-design');
const BASE_CSS_PATH = path.join(DESIGN_DIR, 'base.css');
const THEMES_DIR = path.join(DESIGN_DIR, 'themes');
const LAYOUTS_DIR = path.join(DESIGN_DIR, 'layout-types');

const ALL_PLATFORMS = {
  'xiaohongshu-v':    { id: 'xiaohongshu-v',    width: 1080, height: 1440, label: '小红书竖版' },
  'xiaohongshu-s':    { id: 'xiaohongshu-s',    width: 1080, height: 1080, label: '小红书方版' },
  'wechat-cover':     { id: 'wechat-cover',     width: 900,  height: 383,  label: '公众号头图' },
  'wechat-thumb':     { id: 'wechat-thumb',     width: 300,  height: 300,  label: '公众号小图' },
  'moments':          { id: 'moments',          width: 1080, height: 1080, label: '朋友圈' },
  'weibo':            { id: 'weibo',            width: 1080, height: 608,  label: '微博' },
  'toutiao':          { id: 'toutiao',          width: 1080, height: 500,  label: '头条号' },
  'douyin-cover':     { id: 'douyin-cover',     width: 1080, height: 1920, label: '抖音封面' },
  'bilibili-cover':   { id: 'bilibili-cover',   width: 1920, height: 1080, label: 'B站封面' },
  'twitter':          { id: 'twitter',          width: 1200, height: 675,  label: 'Twitter/X' },
  'a4':               { id: 'a4',               width: 2480, height: 3508, label: 'A4海报(300dpi)' },
  'a3':               { id: 'a3',               width: 3508, height: 4960, label: 'A3海报(300dpi)' },
};

const GROUPS = {
  'xiaohongshu': ['xiaohongshu-v', 'xiaohongshu-s'],
  'wechat':      ['wechat-cover', 'wechat-thumb', 'moments'],
};

function listThemes() {
  if (!fs.existsSync(THEMES_DIR)) return [];
  return fs.readdirSync(THEMES_DIR)
    .filter(f => f.endsWith('.css'))
    .map(f => f.replace(/\.css$/, ''))
    .sort();
}

function listLayouts() {
  if (!fs.existsSync(LAYOUTS_DIR)) return [];
  return fs.readdirSync(LAYOUTS_DIR)
    .filter(f => f.endsWith('.html'))
    .map(f => f.replace(/\.html$/, ''))
    .sort();
}

function loadTheme(themeName) {
  const p = path.join(THEMES_DIR, `${themeName}.css`);
  if (!fs.existsSync(p)) throw new Error(`Theme not found: ${themeName}. Available: ${listThemes().join(', ')}`);
  return fs.readFileSync(p, 'utf-8');
}

function loadLayout(layoutName) {
  const p = path.join(LAYOUTS_DIR, `${layoutName}.html`);
  if (!fs.existsSync(p)) throw new Error(`Layout not found: ${layoutName}. Available: ${listLayouts().join(', ')}`);
  return fs.readFileSync(p, 'utf-8');
}

function loadBaseCSS() {
  if (!fs.existsSync(BASE_CSS_PATH)) throw new Error(`base.css not found at ${BASE_CSS_PATH}`);
  return fs.readFileSync(BASE_CSS_PATH, 'utf-8');
}

function extractThemeDefault(themeCSS, varName) {
  const m = themeCSS.match(new RegExp(`--${varName}:\\s*"?([^";]+)"?`));
  return m ? m[1].trim() : '';
}

function assembleHTML({ themeName, themeCSS, baseCSS, layoutHTML, content, width = 1080, height = 1080, brandOverrideCss = '' }) {
  const brandHtml = content.brandImage
    ? `<img class="cover__brand-img" src="${content.brandImage}" alt="${escapeHtml(content.brand || 'logo')}" />`
    : '';
  const qrHtml = resolveQrHtml(content.qr);
  const tokens = {
    '{{TITLE}}':       escapeHtml(String(content.title || '')),
    '{{CONTENT}}':     escapeHtml(String(content.body || content.content || '')).replace(/\n/g, '<br>'),
    '{{SOURCE}}':      escapeHtml(content.source || ''),
    '{{BRAND}}':       brandHtml,
    '{{QR}}':          qrHtml,
    '{{SEAL}}':        escapeHtml(content.seal || extractThemeDefault(themeCSS, 'seal')),
    '{{BADGE}}':       escapeHtml(content.badge || ''),
    '{{POINTS_HTML}}': (content.points || []).map(p => `<li>${escapeHtml(p)}</li>`).join(''),
    '{{THEME}}':       themeName,
  };
  let body = layoutHTML;
  for (const [k, v] of Object.entries(tokens)) {
    body = body.split(k).join(v);
  }
  const direction = detectDirection(content.title, content.body);
  return `<!DOCTYPE html>
<html lang="${direction.lang}" dir="${direction.dir}" data-theme="${themeName}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=${width}, height=${height}">
<title>${escapeHtml(content.title || '')}</title>
<style>
${baseCSS}
${themeCSS}
${brandOverrideCss}
body { margin: 0; padding: 0; width: ${width}px; height: ${height}px; overflow: hidden; }
.cover { width: ${width}px; height: ${height}px; }
</style>
</head>
<body>
${body}
</body>
</html>`;
}

function renderHTML(layoutHTML, content, config, platform) {
  let html = layoutHTML;
  if (config.colors) {
    const colorMap = {};
    for (const k of Object.keys(config.colors)) colorMap[k.toLowerCase()] = config.colors[k];
    html = html.replace(/\{\{(\w+?)__A(\d\d)\}\}/g, (_, colorName, alphaHex) => {
      const hex = colorMap[colorName.toLowerCase()];
      if (!hex) return _;
      const r = parseInt(hex.slice(1, 3), 16);
      const g = parseInt(hex.slice(3, 5), 16);
      const b = parseInt(hex.slice(5, 7), 16);
      const a = (parseInt(alphaHex, 16) / 255).toFixed(3);
      return `rgba(${r},${g},${b},${a})`;
    });
  }
  return assembleHTML({
    themeName: config.themeName || 'minimal-white',
    themeCSS: config.themeCSS || '',
    baseCSS: config.baseCSS || '',
    layoutHTML: html,
    content,
    width: platform.width,
    height: platform.height,
  });
}

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      if (i + 1 < argv.length && !argv[i + 1].startsWith('--')) {
        args[key] = argv[++i];
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

const LEGACY_TEMPLATE_MAP = {
  '1':  { theme: 'minimal-white',           layout: 'cover' },
  '2':  { theme: 'dark-gold',               layout: 'cover' },
  '3':  { theme: 'editorial',               layout: 'cover' },
  '4':  { theme: 'warm-handdrawn',          layout: 'cover' },
  '5':  { theme: 'tech-modern',             layout: 'cover' },
  '6':  { theme: 'bold-poster',             layout: 'cover' },
  '7':  { theme: 'data-infographic',        layout: 'cover' },
  '8':  { theme: 'eastern',                 layout: 'cover' },
  '9':  { theme: 'magazine-cover',          layout: 'cover' },
  '10': { theme: 'split-screen',            layout: 'cover' },
  '11': { theme: 'minimal-white-editorial', layout: 'cover' },
  '12': { theme: 'list-ranking',            layout: 'cover' },
};

function resolveTemplate(args) {
  let theme = args.theme;
  let layout = args.layout || 'cover';
  if (!theme && args.template) {
    const tplKey = String(args.template).replace(/^0+/, '') || '0';
    const mapped = LEGACY_TEMPLATE_MAP[tplKey];
    if (mapped) { theme = mapped.theme; layout = mapped.layout; }
    else { theme = 'minimal-white'; }
  }
  if (!theme) theme = 'minimal-white';
  return { theme, layout };
}

function resolvePlatforms(args) {
  if (!args.platforms) {
    return [
      { id: 'vertical', width: 1080, height: 1440, label: '3:4 竖版' },
      { id: 'square',   width: 1080, height: 1080, label: '1:1 方版' },
      { id: 'wide',     width: 1920, height: 1080, label: '16:9 横版' },
      { id: 'cover',    width: 1800, height: 766,  label: '2.35:1 封面' },
      { id: 'og',       width: 1200, height: 630,  label: '1.9:1 OG卡片' },
    ];
  }
  const ids = args.platforms.split(',').map(s => s.trim().toLowerCase());
  const out = [];
  const unknown = [];
  for (const id of ids) {
    if (id === 'all') return Object.values(ALL_PLATFORMS);
    if (GROUPS[id]) {
      for (const sub of GROUPS[id]) {
        if (!out.includes(sub)) out.push(sub);
      }
    } else if (ALL_PLATFORMS[id]) {
      if (!out.includes(id)) out.push(id);
    } else {
      unknown.push(id);
    }
  }
  if (unknown.length > 0) {
    process.stderr.write(`warning: unknown platform(s) ignored: ${unknown.join(', ')}\n`);
    process.stderr.write(`available: ${Object.keys(ALL_PLATFORMS).join(', ')}\n`);
  }
  if (out.length === 0 && ids.length > 0) {
    throw new Error(`no valid platforms. Unknown: ${unknown.join(', ')}. Available: ${Object.keys(ALL_PLATFORMS).join(', ')}`);
  }
  return out.map(id => ALL_PLATFORMS[id]).filter(Boolean);
}

function takeScreenshot(html, outputPath, platform) {
  const tmp = path.join(path.dirname(outputPath), `_tmp_${Date.now()}.html`);
  fs.writeFileSync(tmp, html, 'utf-8');
  const url = `file://${path.resolve(tmp)}`;
  const cmd = `npx playwright screenshot --viewport-size=${platform.width},${platform.height} --wait-for-timeout=1500 "${url}" "${outputPath}"`;
  try {
    execSync(cmd, { stdio: 'pipe', timeout: 60000 });
    console.log(`  [OK] ${platform.label} (${platform.width}x${platform.height})`);
  } catch (e) {
    console.error(`  [FAIL] ${platform.label}: ${e.message}`);
  }
  if (fs.existsSync(tmp)) fs.unlinkSync(tmp);
}

function detectDirection(title, body) {
  // Returns {lang, dir} for the <html> element. Detects RTL scripts (Arabic,
  // Hebrew, Persian, Urdu) and sets dir="rtl" so logical CSS properties
  // (padding-inline-end, margin-inline-start) flip correctly. Default is
  // Chinese LTR since that's yuanfang's primary use case.
  const text = `${title || ''} ${body || ''}`;
  // U+0600-U+06FF Arabic, U+0590-U+05FF Hebrew, U+FB50-U+FDFF Arabic Presentation Forms
  const rtlRegex = /[\u0600-\u06FF\u0590-\u05FF\uFB50-\uFDFF]/;
  if (rtlRegex.test(text)) {
    return { lang: 'ar', dir: 'rtl' };
  }
  return { lang: 'zh-CN', dir: 'ltr' };
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function isImageRef(s) {
  if (!s) return false;
  if (s.startsWith('data:image/')) return true;
  if (/\.(png|jpg|jpeg|gif|webp|svg)(\?|#|$)/i.test(s)) return true;
  return false;
}

function resolveQrHtml(qr) {
  if (!qr) return '';
  if (isImageRef(qr)) {
    return `<img class="cover__qr-img" src="${qr}" alt="QR" />`;
  }
  let QR;
  try {
    QR = require('qrcode');
  } catch {
    return '';
  }
  try {
    const matrix = QR.create(qr, { errorCorrectionLevel: 'M' });
    const size = matrix.modules.size;
    const data = matrix.modules.data;
    let path = '';
    for (let y = 0; y < size; y++) {
      for (let x = 0; x < size; x++) {
        if (data[y * size + x]) {
          path += `M${x} ${y}h1v1h-1z`;
        }
      }
    }
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}" shape-rendering="crispEdges"><path d="${path}" fill="black"/></svg>`;
    const dataUrl = 'data:image/svg+xml;base64,' + Buffer.from(svg).toString('base64');
    return `<img class="cover__qr-img" src="${dataUrl}" alt="QR" />`;
  } catch {
    return '';
  }
}

function dateStamp() {
  const d = new Date();
  return `${d.getFullYear()}${String(d.getMonth()+1).padStart(2,'0')}${String(d.getDate()).padStart(2,'0')}`;
}
function safeDirName(t) {
  const cleaned = (t || '').replace(/[\/\\:*?"<>|\n\r\t&']/g, '_').trim();
  return cleaned || 'untitled';
}
function resolveOutputDir(content, args) {
  if (args.output) return path.resolve(args.output);
  const today = dateStamp();
  const root = path.join(SCRIPT_DIR, '..', 'output');
  fs.mkdirSync(root, { recursive: true });
  const prefix = `${today}_${safeDirName(content.title)}`;
  const existing = fs.readdirSync(root).filter(d => d.startsWith(prefix));
  const seq = existing.length > 0
    ? Math.max(...existing.map(d => { const m = d.match(/_(\d+)$/); return m ? parseInt(m[1]) : 0; })) + 1
    : 1;
  return path.join(root, `${prefix}_${String(seq).padStart(3, '0')}`);
}

function findBrandSpec(content, args) {
  if (args['brand-spec']) {
    const p = path.resolve(args['brand-spec']);
    if (fs.existsSync(p) && p.endsWith('.json')) {
      return JSON.parse(fs.readFileSync(p, 'utf-8'));
    }
  }
  const searchDirs = [];
  if (args.file) searchDirs.push(path.dirname(path.resolve(args.file)));
  searchDirs.push(process.cwd());

  for (const dir of searchDirs) {
    const brandDir = path.join(dir, '.yuanfang', 'brand-specs');
    if (!fs.existsSync(brandDir)) continue;
    const files = fs.readdirSync(brandDir).filter(f => f.endsWith('.json'));
    if (files.length === 0) continue;
    if (files.length === 1) {
      return JSON.parse(fs.readFileSync(path.join(brandDir, files[0]), 'utf-8'));
    }
    if (content.brandDomain) {
      const target = path.join(brandDir, `${content.brandDomain}.json`);
      if (fs.existsSync(target)) {
        return JSON.parse(fs.readFileSync(target, 'utf-8'));
      }
    }
    for (const f of files) {
      const spec = JSON.parse(fs.readFileSync(path.join(brandDir, f), 'utf-8'));
      if (spec.name && content.brand && spec.name.toLowerCase() === content.brand.toLowerCase()) {
        return spec;
      }
    }
    if (content.brand) {
      process.stderr.write(`note: multiple brand-specs (${files.length}), no match for "${content.brand}"; using first (${files[0]})\n`);
    }
    return JSON.parse(fs.readFileSync(path.join(brandDir, files[0]), 'utf-8'));
  }
  return null;
}

function mergeBrandSpec(content, spec) {
  if (!spec) return content;
  const out = { ...content };
  if (!out.brand && spec.name) out.brand = spec.name;
  if (!out.brandImage && spec.logo) out.brandImage = spec.logo;
  if (!out.brandDomain && spec.domain) out.brandDomain = spec.domain;
  return out;
}

function buildBrandOverrideCss(spec, themeName) {
  if (!spec || !spec.colors) return '';
  const c = spec.colors;
  const map = {
    '--accent': c.primary,
    '--bg': c.background,
    '--secondary': c.secondary,
  };
  const decls = Object.entries(map)
    .filter(([, v]) => v)
    .map(([k, v]) => `  ${k}: ${v};`)
    .join('\n');
  if (!decls) return '';
  return `[data-theme="${themeName}"] {\n${decls}\n}\n`;
}

function main() {
  const args = parseArgs(process.argv);

  if (args['list-themes']) {
    console.log(listThemes().join('\n'));
    return;
  }
  if (args['list-layouts']) {
    console.log(listLayouts().join('\n'));
    return;
  }

  const content = args.file
    ? JSON.parse(fs.readFileSync(args.file, 'utf-8'))
    : {
        title: args.title || '',
        body: args.body || args.content || '',
        source: args.source || args.url || '',
        points: (args.points || '').split('|').filter(Boolean),
      };

  const spec = findBrandSpec(content, args);
  const merged = mergeBrandSpec(content, spec);

  // ── Hard gate: detect skipped Step 2 user confirmations ──
  // If the user didn't make brand decisions and theme is default, the agent
  // likely skipped Step 2's three rounds. Refuse to render and tell it why.
  const themeIsDefault = !args.theme;
  const noBrandDecision = !merged.brand && !merged.brandImage && !content.brandImage;
  if (themeIsDefault && noBrandDecision) {
    throw new Error(
      'render.js: 检测到 Step 2 用户确认未完成。\n' +
      '你必须先让用户确认以下决策才能渲染：\n' +
      '  - logo:  用抓到的 / 换 URL / 不要（→ content.brandImage）\n' +
      '  - 品牌名: 用抓到的 / 换名（→ content.brand）\n' +
      '  - 主题:  12 个主题里选一个（→ --theme）\n' +
      '  - 平台:  12 个平台里选 1-N 个（→ --platforms）\n' +
      '参考 SKILL.md Step 2 三轮询问。'
    );
  }

  const { theme, layout } = resolveTemplate(args);
  const themeCSS = loadTheme(theme);
  const baseCSS = loadBaseCSS();
  const layoutHTML = loadLayout(layout);
  const brandOverrideCss = buildBrandOverrideCss(spec, theme);

  const platforms = resolvePlatforms(args);
  const outputDir = resolveOutputDir(content, args);
  fs.mkdirSync(outputDir, { recursive: true });

  console.log(`\nTheme: ${theme}    Layout: ${layout}`);
  console.log(`Content: ${content.title || '(no title)'}`);
  console.log(`Output:  ${outputDir}\n`);

  for (const platform of platforms) {
    const html = assembleHTML({
      themeName: theme, themeCSS, baseCSS, layoutHTML, content: merged, brandOverrideCss,
      width: platform.width, height: platform.height,
    });

    if (args.preview) {
      const previewPath = path.join(outputDir, `_preview_${platform.id}.html`);
      fs.writeFileSync(previewPath, html, 'utf-8');
      console.log(`  [HTML] ${previewPath}`);
    } else {
      const safe = safeDirName(content.title).slice(0, 40);
      takeScreenshot(html, path.join(outputDir, `${safe}_${platform.id}.png`), platform);
    }
  }
  console.log(`\nDone: ${outputDir}`);
}

if (require.main === module) {
  try {
    main();
  } catch (err) {
    console.error(`Error: ${err.message}`);
    if (process.env.DEBUG) console.error(err.stack);
    process.exit(1);
  }
}

module.exports = {
  listThemes, listLayouts, loadTheme, loadLayout, loadBaseCSS,
  assembleHTML, renderHTML, parseArgs, resolveTemplate, resolvePlatforms,
  findBrandSpec, mergeBrandSpec, buildBrandOverrideCss,
  isImageRef, resolveQrHtml,
};
