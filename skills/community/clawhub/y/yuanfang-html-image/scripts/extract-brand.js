#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { getMetaContent, getLinkHref, getThemeColor, extractFromHtml } = require('./extract.js');

const CACHE_DIR = path.join(process.cwd(), '.yuanfang', 'brand-specs');
const TTL_DAYS = 7;

const ENTRY_PREFIXES = ['www.', 'm.', 'mobile.', 'app.'];

function extractDomain(url) {
  try {
    let host = new URL(url).hostname.toLowerCase();
    for (const p of ENTRY_PREFIXES) {
      if (host.startsWith(p)) {
        host = host.slice(p.length);
        break;
      }
    }
    return host;
  } catch {
    return null;
  }
}

function resolveImageAsDataUrl(url) {
  return fetch(url, {
    headers: { 'User-Agent': 'yuanfang-skills/0.1' },
    redirect: 'follow',
  })
    .then(r => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return Promise.all([r.arrayBuffer(), r.headers.get('content-type')]);
    })
    .then(([buf, ct]) => {
      const mime = ct || 'image/png';
      return `data:${mime};base64,${Buffer.from(buf).toString('base64')}`;
    });
}

function dataUrlToBuffer(dataUrl) {
  const m = dataUrl.match(/^data:([^;]+);base64,(.+)$/);
  if (!m) return null;
  return { mime: m[1], buffer: Buffer.from(m[2], 'base64') };
}

function rgbToHex(r, g, b) {
  const h = n => n.toString(16).padStart(2, '0');
  return `#${h(r)}${h(g)}${h(b)}`.toUpperCase();
}

async function extractDominantColor(dataUrl) {
  // Returns a single hex representing the most prominent brand color.
  // Uses node-vibrant for perceptual color extraction (vs. sharp's 1x1 mean,
  // which is the image-wide average, not the dominant color).
  if (!dataUrl) return null;
  const parsed = dataUrlToBuffer(dataUrl);
  if (!parsed) return null;
  let Vibrant;
  try {
    Vibrant = require('node-vibrant/node').Vibrant;
  } catch {
    return fallbackAverageColor(parsed.buffer);
  }
  try {
    const palette = await Vibrant.from(parsed.buffer).quality(10).getPalette();
    // Prefer Vibrant → DarkVibrant → LightVibrant → Muted (in that order).
    // The first non-null is the most "brand-like" saturated color.
    const swatch = palette.Vibrant || palette.DarkVibrant || palette.LightVibrant || palette.Muted;
    return swatch ? swatch.hex : null;
  } catch {
    return fallbackAverageColor(parsed.buffer);
  }
}

async function extractBrandPalette(dataUrl) {
  // Returns a 6-swatch semantic palette: vibrant / darkVibrant / lightVibrant
  // / darkMuted / lightMuted / muted. Used by render.js to map to multiple
  // design tokens (--accent, --secondary, etc.) for the 60-30-10 rule.
  if (!dataUrl) return null;
  const parsed = dataUrlToBuffer(dataUrl);
  if (!parsed) return null;
  let Vibrant;
  try {
    Vibrant = require('node-vibrant/node').Vibrant;
  } catch {
    return null;
  }
  try {
    const palette = await Vibrant.from(parsed.buffer).quality(10).getPalette();
    const out = {};
    for (const [name, sw] of Object.entries(palette)) {
      if (sw) out[name] = { hex: sw.hex, population: sw.population };
    }
    return Object.keys(out).length > 0 ? out : null;
  } catch {
    return null;
  }
}

async function fallbackAverageColor(buffer) {
  // Used only when node-vibrant is unavailable. Returns the mean RGB.
  let sharp;
  try {
    sharp = require('sharp');
  } catch {
    return null;
  }
  try {
    const { data } = await sharp(buffer)
      .resize(1, 1, { fit: 'cover' })
      .removeAlpha()
      .raw()
      .toBuffer({ resolveWithObject: true });
    return rgbToHex(data[0], data[1], data[2]);
  } catch {
    return null;
  }
}

function extractBrandFromHtml(html, url) {
  const domain = extractDomain(url);
  const siteName = getMetaContent(html, 'site_name');
  const ogImage = getMetaContent(html, 'image');
  const appleIcon = getLinkHref(html, 'apple-touch-icon')
    || getLinkHref(html, 'apple-touch-icon-precomposed')
    || getLinkHref(html, 'icon');
  const themeColorLight = getThemeColor(html, 'light');
  const themeColorDark = getThemeColor(html, 'dark');
  const themeColor = themeColorLight;

  let logoUrl = null;
  if (ogImage) {
    logoUrl = ogImage.startsWith('http') ? ogImage : new URL(ogImage, url).href;
  } else if (appleIcon) {
    logoUrl = appleIcon.startsWith('http') ? appleIcon : new URL(appleIcon, url).href;
  }

  return {
    domain,
    url,
    name: siteName || domain,
    logo: null,
    logoUrl,
    colors: {
      primary: themeColor || null,
      primaryDark: themeColorDark || null,
      background: null,
      secondary: null,
    },
  };
}

async function fetchBrand(url) {
  const res = await fetch(url, {
    headers: { 'User-Agent': 'yuanfang-skills/0.1' },
    redirect: 'follow',
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} fetching ${url}`);
  const html = await res.text();
  const brand = extractBrandFromHtml(html, url);
  if (brand.logoUrl) {
    try {
      brand.logo = await resolveImageAsDataUrl(brand.logoUrl);
      if (!brand.colors.primary) {
        const logoColor = await extractDominantColor(brand.logo);
        if (logoColor) brand.colors.primary = logoColor;
      }
    } catch (e) {
      process.stderr.write(`warn: failed to download logo (${e.message})\n`);
    }
  }
  return brand;
}

function cachePath(domain) {
  return path.join(CACHE_DIR, `${domain}.json`);
}

function readCache(domain) {
  const p = cachePath(domain);
  if (!fs.existsSync(p)) return null;
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch {
    return null;
  }
}

function isExpired(spec) {
  if (!spec.extractedAt) return true;
  const ageMs = Date.now() - new Date(spec.extractedAt).getTime();
  return ageMs > TTL_DAYS * 24 * 60 * 60 * 1000;
}

function writeCache(spec) {
  fs.mkdirSync(CACHE_DIR, { recursive: true });
  const p = cachePath(spec.domain);
  fs.writeFileSync(p, JSON.stringify(spec, null, 2) + '\n');
  return p;
}

function parseArgs(argv) {
  const args = argv.slice(2);
  const forceRefresh = args.includes('--refresh-brand');
  const remaining = args.filter(a => a !== '--refresh-brand');
  if (remaining.length === 0) {
    throw new Error('Usage: extract-brand.js <url> [--refresh-brand] [--no-cache]');
  }
  return { url: remaining[0], forceRefresh };
}

async function main() {
  const { url, forceRefresh } = parseArgs(process.argv);
  const domain = extractDomain(url);
  if (!domain) throw new Error(`Could not parse domain from ${url}`);

  let spec = readCache(domain);
  const useCache = spec && !isExpired(spec) && !forceRefresh;

  if (useCache) {
    process.stderr.write(`cached (${spec.extractedAt}): ${cachePath(domain)}\n`);
  } else {
    if (forceRefresh && spec) {
      process.stderr.write(`--refresh-brand: ignoring cache\n`);
    } else if (spec) {
      process.stderr.write(`cache expired (>${TTL_DAYS} days), re-fetching\n`);
    }
    spec = await fetchBrand(url);
    spec.extractedAt = new Date().toISOString();
    const p = writeCache(spec);
    process.stderr.write(`saved: ${p}\n`);
  }

  process.stdout.write(JSON.stringify(spec, null, 2) + '\n');
}

module.exports = {
  extractDomain,
  extractBrandFromHtml,
  resolveImageAsDataUrl,
  dataUrlToBuffer,
  rgbToHex,
  extractDominantColor,
  extractBrandPalette,
  fetchBrand,
  readCache,
  writeCache,
  isExpired,
  cachePath,
  CACHE_DIR,
  TTL_DAYS,
  parseArgs,
};

if (require.main === module) {
  main().catch(err => { console.error(err.message); process.exit(1); });
}
