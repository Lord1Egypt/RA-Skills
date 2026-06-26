#!/usr/bin/env node
const fs = require('fs');

function htmlDecode(s) {
  if (!s) return s;
  return s
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&#x([0-9a-fA-F]+);/g, (_, h) => String.fromCharCode(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCharCode(parseInt(d, 10)));
}

function getMetaContent(html, name) {
  let m = html.match(new RegExp(
    `<meta\\s+name=["']${name}["']\\s+content=["']([^"']*)["']`, 'i'));
  if (m) return htmlDecode(m[1]);
  m = html.match(new RegExp(
    `<meta\\s+content=["']([^"']*)["']\\s+name=["']${name}["']`, 'i'));
  if (m) return htmlDecode(m[1]);
  m = html.match(new RegExp(
    `<meta\\s+property=["']og:${name}["']\\s+content=["']([^"']*)["']`, 'i'));
  if (m) return htmlDecode(m[1]);
  m = html.match(new RegExp(
    `<meta\\s+content=["']([^"']*)["']\\s+property=["']og:${name}["']`, 'i'));
  if (m) return htmlDecode(m[1]);
  return null;
}

function getLinkHref(html, rel) {
  const patterns = [
    new RegExp(`<link[^>]+rel=["']${rel}["'][^>]+href=["']([^"']+)["']`, 'i'),
    new RegExp(`<link[^>]+href=["']([^"']+)["'][^>]+rel=["']${rel}["']`, 'i'),
  ];
  for (const re of patterns) {
    const m = html.match(re);
    if (m) return m[1];
  }
  return null;
}

function getThemeColor(html, scheme = 'light') {
  const want = scheme === 'dark' ? 'dark' : 'light';
  const reWithMedia = new RegExp(
    `<meta\\s+name=["']theme-color["']\\s+content=["']([^"']+)["']\\s+media=["']\\([^)]*prefers-color-scheme:\\s*${want}[^)]*\\)["']`, 'i');
  let m = html.match(reWithMedia);
  if (m) return htmlDecode(m[1]);
  const reMediaFirst = new RegExp(
    `<meta\\s+media=["']\\([^)]*prefers-color-scheme:\\s*${want}[^)]*\\)[^>]*name=["']theme-color["']\\s+content=["']([^"']+)["']`, 'i');
  m = html.match(reMediaFirst);
  if (m) return htmlDecode(m[1]);
  if (scheme === 'light') {
    return getMetaContent(html, 'theme-color');
  }
  return null;
}

function stripTags(html) {
  return html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
}

function extractTitle(html) {
  return getMetaContent(html, 'og:title')
    || getMetaContent(html, 'twitter:title')
    || getMetaContent(html, 'title')
    || (() => {
        const m = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
        return m ? stripTags(m[1]) : null;
      })()
    || '';
}

function extractBody(html) {
  return getMetaContent(html, 'og:description')
    || getMetaContent(html, 'description')
    || getMetaContent(html, 'twitter:description')
    || (() => {
        const m = html.match(/<p[^>]*>([\s\S]*?)<\/p>/i);
        return m ? stripTags(m[1]) : '';
      })();
}

function extractBrand(html, url) {
  return getMetaContent(html, 'site_name')
    || getMetaContent(html, 'application-name')
    || (url ? new URL(url).hostname.replace(/^www\./, '') : '');
}

function extractBrandImage(html) {
  return getMetaContent(html, 'image')
    || getLinkHref(html, 'apple-touch-icon')
    || getLinkHref(html, 'apple-touch-icon-precomposed')
    || getLinkHref(html, 'icon');
}

function extractPoints(html) {
  const points = [];
  const listMatch = html.match(/<(ul|ol)[^>]*>([\s\S]*?)<\/\1>/i);
  if (listMatch) {
    const items = listMatch[2].matchAll(/<li[^>]*>([\s\S]*?)<\/li>/gi);
    for (const m of items) {
      const t = stripTags(m[1]);
      if (t && t.length < 80) points.push(t);
      if (points.length >= 3) break;
    }
  }
  if (points.length === 0) {
    const headings = html.matchAll(/<h[23][^>]*>([\s\S]*?)<\/h[23]>/gi);
    for (const m of headings) {
      const t = stripTags(m[1]);
      if (t && t.length < 60) points.push(t);
      if (points.length >= 3) break;
    }
  }
  return points;
}

function extractPointsFromBody(body) {
  if (!body || !body.includes('、')) return { points: [], body };
  // Match "、" separated Chinese enumeration: e.g. "知识库/发布双版本、多渠道接入、AI Agent"
  const re = /((?:[\u4e00-\u9fff\u3040-\u309f\w\/\+\s-]+[、])+[\u4e00-\u9fff\u3040-\u309f\w\/\+\s-]+)/;
  const m = body.match(re);
  if (m) {
    const items = m[1].split('、').map(s => s.trim()).filter(Boolean);
    if (items.length >= 2 && items.every(i => i.length >= 2 && i.length <= 40)) {
      let newBody = body.replace(m[1], '').replace(/[，,]\s*(?=[。！？])/g, '').replace(/[，,]\s*$/, '').replace(/\s{2,}/g, ' ').trim();
      if (!newBody) newBody = body;
      return { points: items.slice(0, 4), body: newBody };
    }
  }
  return { points: [], body };
}

function extractFromHtml(html, url) {
  let body = extractBody(html) || '';
  let points = extractPoints(html);

  if (points.length === 0) {
    const fallback = extractPointsFromBody(body);
    if (fallback.points.length > 0) {
      points = fallback.points;
      body = fallback.body;
    }
  }

  return {
    title: stripTags(extractTitle(html) || ''),
    body: body,
    points: points,
    brand: extractBrand(html, url),
    brandImage: extractBrandImage(html) || undefined,
  };
}

function extractFromText(text) {
  const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
  const title = lines[0] || '';
  const body = lines.find((l, i) => i > 0 && !l.match(/^[-•*]\s/) && !l.match(/^公众号[\s:：]/)) || '';
  const points = lines
    .filter(l => l.match(/^[-•*]\s/))
    .map(l => l.replace(/^[-•*]\s+/, ''))
    .slice(0, 3);
  let brand = '';
  const brandMatch = text.match(/(?:公众号|来源|来自|from|by|via)[\s:：]+([^\n]+)/i);
  if (brandMatch) brand = brandMatch[1].trim();
  return { title, body, points, brand };
}

async function extractFromUrl(url) {
  const res = await fetch(url, {
    headers: { 'User-Agent': 'yuanfang-skills/0.1 (+https://github.com/yuanfang)' },
    redirect: 'follow',
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} fetching ${url}`);
  const html = await res.text();
  return extractFromHtml(html, url);
}

function parseArgs(argv) {
  const args = argv.slice(2);
  if (args.length === 0) {
    throw new Error('Usage: extract.js <url> | --text "..." | --file <path>');
  }
  if (args[0] === '--text') {
    return { mode: 'text', text: args.slice(1).join(' ') };
  }
  if (args[0] === '--file') {
    if (!args[1]) throw new Error('--file requires a path');
    return { mode: 'file', path: args[1] };
  }
  return { mode: 'url', url: args[0] };
}

async function main() {
  const args = parseArgs(process.argv);
  let result;

  if (args.mode === 'url') {
    result = await extractFromUrl(args.url);
  } else if (args.mode === 'text') {
    result = extractFromText(args.text);
  } else if (args.mode === 'file') {
    const text = fs.readFileSync(args.path, 'utf8');
    result = extractFromText(text);
  }

  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
}

module.exports = {
  htmlDecode,
  getMetaContent,
  getLinkHref,
  getThemeColor,
  stripTags,
  extractTitle,
  extractBody,
  extractBrand,
  extractBrandImage,
  extractPoints,
  extractPointsFromBody,
  extractFromHtml,
  extractFromText,
  extractFromUrl,
  parseArgs,
};

if (require.main === module) {
  main().catch(err => { console.error(err.message); process.exit(1); });
}
