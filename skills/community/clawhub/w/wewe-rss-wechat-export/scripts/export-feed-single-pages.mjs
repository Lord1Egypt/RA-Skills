import fs from 'node:fs/promises';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const [feedBaseUrl, outputDir, countArg = '100', batchArg = '2', ...optionArgs] =
  process.argv.slice(2);

const MAX_BATCH_SIZE = 5;
const CURL_TIMEOUT_SECONDS = 60;
const IMAGE_TIMEOUT_MS = 30_000;
const MIN_TEXT_LENGTH = 80;
const TAIL_MARKERS = [
  '往期推荐',
  '相关阅读',
  '推荐阅读',
  '延伸阅读',
  '更多关于',
  '合作与反馈',
  '点击下方名片',
  '继续滑动看下一个',
  '点击蓝字关注',
  '扫码关注',
  '欢迎关注',
];
const VOID_TAGS = new Set(['br', 'hr', 'img']);
const ALLOWED_TAGS = new Set([
  'a',
  'b',
  'blockquote',
  'br',
  'code',
  'div',
  'em',
  'figcaption',
  'figure',
  'h1',
  'h2',
  'h3',
  'h4',
  'h5',
  'h6',
  'hr',
  'i',
  'img',
  'li',
  'ol',
  'p',
  'pre',
  'section',
  'span',
  'strong',
  'sub',
  'sup',
  'table',
  'tbody',
  'td',
  'th',
  'thead',
  'tr',
  'u',
  'ul',
]);

if (!feedBaseUrl || !outputDir) {
  console.error(
    'Usage: node scripts/export-feed-single-pages.mjs <feed-json-base-url> <output-dir> [count] [batchSize]',
  );
  process.exit(1);
}

const requestedTotal = Number.parseInt(countArg, 10);
if (!Number.isInteger(requestedTotal) || requestedTotal <= 0) {
  console.error(`Invalid count: ${countArg}`);
  process.exit(1);
}

const requestedBatchSize = Number.parseInt(batchArg, 10);
if (!Number.isInteger(requestedBatchSize) || requestedBatchSize <= 0) {
  console.error(`Invalid batch size: ${batchArg}`);
  process.exit(1);
}

let outputMode = 'docx';
let renameMode = 'dated';

for (let index = 0; index < optionArgs.length; index += 1) {
  const arg = optionArgs[index];
  if (arg === '--output-mode') {
    outputMode = optionArgs[index + 1] || '';
    index += 1;
    continue;
  }
  if (arg === '--rename-mode') {
    renameMode = optionArgs[index + 1] || '';
    index += 1;
    continue;
  }

  console.error(`Unknown option: ${arg}`);
  process.exit(1);
}

if (!['docx', 'full'].includes(outputMode)) {
  console.error(`Invalid output mode: ${outputMode}`);
  process.exit(1);
}

if (!['dated', 'plain'].includes(renameMode)) {
  console.error(`Invalid rename mode: ${renameMode}`);
  process.exit(1);
}

const total = requestedTotal;
const batchSize = Math.max(1, Math.min(requestedBatchSize, MAX_BATCH_SIZE));

if (requestedBatchSize !== batchSize) {
  console.warn(
    `[warn] Requested batch size ${requestedBatchSize}, adjusted to ${batchSize}.`,
  );
}

const pad = (n) => String(n).padStart(3, '0');

const sanitizeFileName = (value = '') =>
  String(value)
    .replace(/[\u200B-\u200D\uFEFF]/g, '')
    .replace(/[<>:"/\\|?*\u0000-\u001F]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 80) || 'untitled';

const escapeHtml = (value = '') =>
  String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

const escapeRegExp = (value = '') =>
  String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

const formatDate = (value) => {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return new Intl.DateTimeFormat('zh-CN', {
    dateStyle: 'long',
    timeStyle: 'medium',
    timeZone: 'Asia/Shanghai',
  }).format(date);
};

const formatDateForFileName = (value) => {
  if (!value) return 'undated';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return 'undated';

  const parts = new Intl.DateTimeFormat('en', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    timeZone: 'Asia/Shanghai',
  }).formatToParts(date);

  const lookup = Object.fromEntries(
    parts
      .filter((part) => part.type !== 'literal')
      .map((part) => [part.type, part.value]),
  );

  if (!lookup.year || !lookup.month || !lookup.day) {
    return 'undated';
  }

  return `${lookup.year}-${lookup.month}-${lookup.day}`;
};

const buildPageUrl = (baseUrl, page) => {
  const url = new URL(baseUrl);
  url.searchParams.set('limit', String(batchSize));
  url.searchParams.set('page', String(page));
  return url.toString();
};

const curlJson = (url) => {
  const stdout = execFileSync(
    'curl',
    [
      '--http1.1',
      '--compressed',
      '--silent',
      '--show-error',
      '--location',
      '--max-time',
      String(CURL_TIMEOUT_SECONDS),
      '--user-agent',
      'Mozilla/5.0 Claude Export Script',
      '--header',
      'accept: application/json,text/plain,*/*',
      url,
    ],
    { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 },
  );
  return JSON.parse(stdout);
};

const renderProgress = (current, totalCount, title = '') => {
  const width = 24;
  const ratio = totalCount === 0 ? 0 : current / totalCount;
  const filled = Math.round(width * ratio);
  const bar = `${'#'.repeat(filled)}${'-'.repeat(width - filled)}`;
  const shortTitle = title ? ` ${title.slice(0, 36)}` : '';
  process.stdout.write(`\r[${bar}] ${current}/${totalCount}${shortTitle}`);
  if (current === totalCount) process.stdout.write('\n');
};

const normalizeUrl = (value = '', baseUrl = 'https://mp.weixin.qq.com/') => {
  const trimmed = String(value || '').trim();
  if (!trimmed) return '';
  if (trimmed.startsWith('data:')) return trimmed;

  try {
    const url = new URL(trimmed, baseUrl);
    if (!['http:', 'https:'].includes(url.protocol)) {
      return '';
    }
    return url.toString();
  } catch {
    return '';
  }
};

const guessExtension = (url, contentType = '') => {
  const normalizedType = contentType.split(';')[0].trim().toLowerCase();
  const typeMap = {
    'image/jpeg': 'jpg',
    'image/jpg': 'jpg',
    'image/png': 'png',
    'image/gif': 'gif',
    'image/webp': 'webp',
    'image/svg+xml': 'svg',
    'image/bmp': 'bmp',
  };

  if (typeMap[normalizedType]) {
    return typeMap[normalizedType];
  }

  try {
    const pathname = new URL(url).pathname;
    const ext = path.extname(pathname).replace('.', '').toLowerCase();
    if (/^[a-z0-9]{2,5}$/.test(ext)) {
      return ext;
    }
  } catch {}

  return 'img';
};

const textToHtml = (value = '') => {
  const blocks = String(value)
    .split(/\n{2,}/)
    .map((item) => item.trim())
    .filter(Boolean);

  if (blocks.length === 0) {
    return '';
  }

  return blocks
    .map((block) => `<p>${escapeHtml(block).replace(/\n/g, '<br>')}</p>`)
    .join('\n');
};

const decodeEntities = (value = '') =>
  String(value)
    .replace(/&nbsp;/gi, ' ')
    .replace(/&#39;/g, "'")
    .replace(/&quot;/gi, '"')
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&amp;/gi, '&');

const stripTags = (value = '') =>
  decodeEntities(
    String(value)
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<\/(p|div|section|li|blockquote|tr|h[1-6])>/gi, '\n')
      .replace(/<[^>]+>/g, ' '),
  )
    .replace(/\s+/g, ' ')
    .trim();

const parseAttributes = (source = '') => {
  const attrs = new Map();
  const attrRegex =
    /([a-zA-Z_:][-a-zA-Z0-9_:.]*)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g;
  let match;

  while ((match = attrRegex.exec(source))) {
    const name = match[1].toLowerCase();
    const value = match[2] ?? match[3] ?? match[4] ?? '';
    attrs.set(name, value);
  }

  return attrs;
};

const buildAttrString = (attrs) => {
  const entries = Array.from(attrs.entries()).filter(([, value]) => value !== '');
  if (entries.length === 0) {
    return '';
  }

  return entries.map(([key, value]) => ` ${key}="${escapeHtml(value)}"`).join('');
};

const extractBalancedElement = (html, match) => {
  const tagName = match[1].toLowerCase();
  const start = match.index;
  const tokenRegex = new RegExp(`<\\/?${escapeRegExp(tagName)}\\b[^>]*>`, 'gi');
  tokenRegex.lastIndex = start;

  let depth = 0;
  let token;
  while ((token = tokenRegex.exec(html))) {
    const chunk = token[0];
    const isClosing = chunk.startsWith('</');
    const isSelfClosing = /\/\s*>$/.test(chunk) || VOID_TAGS.has(tagName);

    if (!isClosing) {
      depth += 1;
      if (isSelfClosing) {
        depth -= 1;
      }
    } else {
      depth -= 1;
    }

    if (depth === 0) {
      return html.slice(start, tokenRegex.lastIndex);
    }
  }

  return html.slice(start);
};

const findElementById = (html, id) => {
  const regex = new RegExp(
    `<([a-zA-Z][\\w:-]*)\\b[^>]*\\bid=("|')${escapeRegExp(id)}\\2[^>]*>`,
    'i',
  );
  const match = regex.exec(html);
  return match ? extractBalancedElement(html, match) : '';
};

const findElementByClass = (html, className) => {
  const regex = /<([a-zA-Z][\w:-]*)\b[^>]*\bclass=("|')([\s\S]*?)\2[^>]*>/gi;
  let match;
  while ((match = regex.exec(html))) {
    const classes = match[3].split(/\s+/).filter(Boolean);
    if (classes.includes(className)) {
      return extractBalancedElement(html, match);
    }
  }
  return '';
};

const findElementByTag = (html, tagName) => {
  const regex = new RegExp(`<(${escapeRegExp(tagName)})\\b[^>]*>`, 'i');
  const match = regex.exec(html);
  return match ? extractBalancedElement(html, match) : '';
};

const sanitizeHtmlTags = (html, originalUrl) =>
  html.replace(/<\/?([a-zA-Z][\w:-]*)\b[^>]*>/g, (full, rawTagName) => {
    const tagName = rawTagName.toLowerCase();
    if (!ALLOWED_TAGS.has(tagName)) {
      return '';
    }

    if (full.startsWith('</')) {
      return VOID_TAGS.has(tagName) ? '' : `</${tagName}>`;
    }

    const attrSource = full
      .replace(/^<[a-zA-Z][\w:-]*/i, '')
      .replace(/\/?\s*>$/, '');
    const attrs = parseAttributes(attrSource);
    const kept = new Map();

    if (tagName === 'a') {
      const href = normalizeUrl(attrs.get('href') || '', originalUrl);
      if (href) {
        kept.set('href', href);
      }
    }

    if (tagName === 'img') {
      const src = normalizeUrl(
        attrs.get('data-src') ||
          attrs.get('data-original') ||
          attrs.get('data-actualsrc') ||
          attrs.get('src') ||
          attrs.get('data-lazy-src') ||
          '',
        originalUrl,
      );
      if (!src) {
        return '';
      }
      kept.set('src', src);

      const alt = (attrs.get('alt') || '').trim();
      const title = (attrs.get('title') || '').trim();
      if (alt) kept.set('alt', alt);
      if (title) kept.set('title', title);

      return `<img${buildAttrString(kept)} />`;
    }

    if (tagName === 'td' || tagName === 'th') {
      const colspan = (attrs.get('colspan') || '').trim();
      const rowspan = (attrs.get('rowspan') || '').trim();
      if (/^\d+$/.test(colspan)) kept.set('colspan', colspan);
      if (/^\d+$/.test(rowspan)) kept.set('rowspan', rowspan);
    }

    return `<${tagName}${buildAttrString(kept)}>`;
  });

const collapseWrapperTags = (html) => {
  let current = html;
  let previous = '';

  while (current !== previous) {
    previous = current;
    current = current
      .replace(/<(span|div|section)>(\s*<(?:span|div|section|strong|b|em|i|u|a|img|br)\b[\s\S]*?<\/\1>|\s*[^<>]+\s*)<\/\1>/gi, (_match, tag, inner) => {
        const normalizedInner = inner.trim();
        if (!normalizedInner) {
          return '';
        }
        if (tag === 'span') {
          return normalizedInner;
        }
        return `<${tag}>${normalizedInner}</${tag}>`;
      })
      .replace(/<(span|div|section)>\s*<\/(span|div|section)>/gi, '');
  }

  return current;
};

const normalizeStructure = (html) =>
  html
    .replace(/<\/?span\b[^>]*>/gi, '')
    .replace(/<\/?(div|section)\b[^>]*>/gi, '\n')
    .replace(/<p>\s*(?:<br\s*\/?>|&nbsp;|\s)*<\/p>/gi, '')
    .replace(/([A-Za-z0-9])\n(?=[A-Za-z0-9])/g, '$1 ')
    .replace(/([\u4e00-\u9fff])\n(?=[A-Za-z0-9])/g, '$1 ')
    .replace(/([A-Za-z0-9])\n(?=[\u4e00-\u9fff])/g, '$1 ')
    .replace(/\n{3,}/g, '\n\n');

const stripEmptyContainers = (html) => {
  let current = html;
  let previous = '';

  while (current !== previous) {
    previous = current;
    current = collapseWrapperTags(normalizeStructure(current))
      .replace(
        /<(p|div|section|span|strong|b|em|i|u|blockquote|pre|code|figure|figcaption|li|a|h[1-6])>\s*(?:<br\s*\/?>\s*)*<\/\1>/gi,
        '',
      )
      .replace(/(?:<br\s*\/?>\s*){3,}/gi, '<br /><br />');
  }

  return current;
};

const pickContentHtml = (rawHtml) =>
  findElementById(rawHtml, 'js_content') ||
  findElementByClass(rawHtml, 'rich_media_content') ||
  findElementByTag(rawHtml, 'article') ||
  findElementByTag(rawHtml, 'main') ||
  findElementByTag(rawHtml, 'body') ||
  rawHtml;

const removeTailSections = (html) => {
  let current = html;

  for (const marker of TAIL_MARKERS) {
    const index = current.indexOf(marker);
    if (index > 0) {
      const before = current.slice(0, index);
      const after = current.slice(index);
      const imageCountAfter = (after.match(/<img\b/gi) || []).length;
      if (imageCountAfter <= 1) {
        current = before.trim();
        break;
      }
    }
  }

  return current;
};

const cleanupArticleHtml = (rawHtml, fallbackText, originalUrl) => {
  const hasHtml = /<[^>]+>/.test(String(rawHtml || ''));
  const initialHtml = hasHtml ? pickContentHtml(String(rawHtml)) : textToHtml(fallbackText);

  if (!initialHtml.trim()) {
    throw new Error('Article body is empty.');
  }

  let bodyHtml = initialHtml
    .replace(/<!DOCTYPE[^>]*>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/<(script|style|title|noscript|iframe|canvas|object|embed|form|button|select|textarea)\b[\s\S]*?<\/\1>/gi, '')
    .replace(/<(meta|link|base|input)\b[^>]*>/gi, '')
    .replace(/\s+(class|id|style|aria-[\w:-]+|role|contenteditable|spellcheck|draggable|tabindex|leaf|nodeleaf|textstyle|type|width|height|loading|decoding|crossorigin|referrerpolicy|nonce|reportloaderror)=("[^"]*"|'[^']*'|[^\s>]+)/gi, '')
    .replace(/\s+on[a-z]+=(("[^"]*")|('[^']*')|([^\s>]+))/gi, '');

  bodyHtml = sanitizeHtmlTags(bodyHtml, originalUrl);
  bodyHtml = removeTailSections(bodyHtml);
  bodyHtml = stripEmptyContainers(bodyHtml)
    .replace(/(?:^|\n)\s*([1-9]\d{0,1})\s*(?=\n\n(?:核心突破|做坚实的技术赋能者|#|<p>|[^\d\n]))/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();

  const textContent = stripTags(bodyHtml);
  const imageCount = (bodyHtml.match(/<img\b/gi) || []).length;

  if (!bodyHtml) {
    throw new Error('Article body is empty after cleanup.');
  }

  if (/(<(script|style|meta|link|head|html|body)\b|badjs\.weixinbridge\.com)/i.test(bodyHtml)) {
    throw new Error('Article body still contains page-level garbage tags.');
  }

  if (textContent.length < MIN_TEXT_LENGTH && imageCount === 0) {
    throw new Error(
      `Article body looks too short after cleanup (${textContent.length} chars).`,
    );
  }

  return {
    bodyHtml,
    textLength: textContent.length,
    imageCount,
  };
};

const downloadBinary = async (url) => {
  const response = await fetch(url, {
    headers: {
      'user-agent': 'Mozilla/5.0 Claude Export Script',
      accept: 'image/*,*/*;q=0.8',
      referer: 'https://mp.weixin.qq.com/',
    },
    signal: AbortSignal.timeout(IMAGE_TIMEOUT_MS),
  });

  if (!response.ok) {
    throw new Error(`Image fetch failed: ${response.status} ${response.statusText}`);
  }

  const arrayBuffer = await response.arrayBuffer();
  return {
    buffer: Buffer.from(arrayBuffer),
    extension: guessExtension(url, response.headers.get('content-type') || ''),
  };
};

const localizeImages = async (bodyHtml, assetDir, assetDirName, originalUrl) => {
  const imgRegex = /<img\b[^>]*\bsrc="([^"]+)"[^>]*\/>/gi;
  const downloadedByUrl = new Map();
  let nextImageIndex = 1;
  let downloadedImages = 0;
  let imageCount = 0;
  let lastIndex = 0;
  let result = '';
  let match;

  await fs.mkdir(assetDir, { recursive: true });

  while ((match = imgRegex.exec(bodyHtml))) {
    imageCount += 1;
    result += bodyHtml.slice(lastIndex, match.index);
    lastIndex = imgRegex.lastIndex;

    const currentSrc = normalizeUrl(match[1], originalUrl);
    if (!currentSrc) {
      continue;
    }

    if (currentSrc.startsWith('data:')) {
      result += match[0];
      continue;
    }

    let relativeSrc = downloadedByUrl.get(currentSrc);
    if (!relativeSrc) {
      try {
        const { buffer, extension } = await downloadBinary(currentSrc);
        const fileName = `image-${pad(nextImageIndex)}.${extension}`;
        nextImageIndex += 1;
        await fs.writeFile(path.join(assetDir, fileName), buffer);
        relativeSrc = `${assetDirName}/${fileName}`.split(path.sep).join('/');
        downloadedByUrl.set(currentSrc, relativeSrc);
        downloadedImages += 1;
      } catch {
        relativeSrc = currentSrc;
      }
    }

    result += match[0].replace(
      /\bsrc="([^"]+)"/i,
      `src="${escapeHtml(relativeSrc)}"`,
    );
  }

  result += bodyHtml.slice(lastIndex);

  return {
    bodyHtml: result.trim(),
    imageCount,
    downloadedImages,
  };
};

const buildArticleHtmlDocument = ({
  feedTitle,
  title,
  published,
  originalUrl,
  pageUrl,
  bodyHtml,
}) => {
  const displayTitle = published ? `${published} ${title}` : title;

  return `<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <title>${escapeHtml(displayTitle)}</title>
    <style>
      body {
        font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
        color: #222;
        line-height: 1.8;
        margin: 32px auto;
        max-width: 820px;
        padding: 0 24px;
        word-break: normal;
        overflow-wrap: break-word;
      }
      h1 {
        line-height: 1.4;
        margin-bottom: 12px;
      }
      .meta {
        color: #666;
        font-size: 14px;
        margin-bottom: 24px;
      }
      .meta p {
        margin: 4px 0;
      }
      img {
        display: block;
        height: auto;
        margin: 16px auto;
        max-width: 100%;
      }
      table {
        border-collapse: collapse;
        margin: 16px 0;
        width: 100%;
      }
      th,
      td {
        border: 1px solid #ddd;
        padding: 8px;
        vertical-align: top;
      }
      blockquote {
        border-left: 4px solid #ddd;
        color: #555;
        margin: 16px 0;
        padding-left: 12px;
      }
      pre,
      code {
        white-space: pre-wrap;
        word-break: break-word;
      }
      a {
        color: #0b57d0;
      }
    </style>
  </head>
  <body>
    <main>
      <h1>${escapeHtml(displayTitle)}</h1>
      <section class="meta">
        <p>订阅源：${escapeHtml(feedTitle || 'WeWe RSS Export')}</p>
        ${published ? `<p>发布时间：${escapeHtml(published)}</p>` : ''}
        ${originalUrl ? `<p>原文链接：<a href="${escapeHtml(originalUrl)}">${escapeHtml(originalUrl)}</a></p>` : ''}
        <p>导出来源：<a href="${escapeHtml(pageUrl)}">${escapeHtml(pageUrl)}</a></p>
      </section>
      <article>
        ${bodyHtml}
      </article>
    </main>
  </body>
</html>
`;
};

const writeArticleFiles = async (baseDir, index, feedTitle, item, pageUrl) => {
  const prefix = pad(index);
  const title = item.title || `文章 ${index}`;
  const safeTitle = sanitizeFileName(title);
  const originalUrl = item.url || item.external_url || '';
  const publishedSource = item.date_published || item.date_modified;
  const published = formatDate(publishedSource);
  const datePrefix = formatDateForFileName(publishedSource);
  const fileBaseName =
    renameMode === 'plain' ? `${prefix}-${safeTitle}` : `${datePrefix}-${prefix}-${safeTitle}`;

  const cleaned = cleanupArticleHtml(
    item.content_html || '',
    item.content_text || '',
    originalUrl,
  );

  const assetDirName = `${fileBaseName}.assets`;
  const assetDir = path.join(baseDir, assetDirName);
  const localized = await localizeImages(
    cleaned.bodyHtml,
    assetDir,
    assetDirName,
    originalUrl,
  );

  const html = buildArticleHtmlDocument({
    feedTitle,
    title,
    published,
    originalUrl,
    pageUrl,
    bodyHtml: localized.bodyHtml,
  });

  const htmlPath = path.join(baseDir, `${fileBaseName}.html`);
  const mdPath = path.join(baseDir, `${fileBaseName}.md`);
  const docxPath = path.join(baseDir, `${fileBaseName}.docx`);

  await fs.writeFile(htmlPath, html, 'utf8');

  if (outputMode === 'full') {
    execFileSync('pandoc', ['-f', 'html', '-t', 'gfm', path.basename(htmlPath), '-o', path.basename(mdPath)], {
      cwd: baseDir,
      stdio: 'pipe',
      maxBuffer: 64 * 1024 * 1024,
    });
  }

  execFileSync('pandoc', ['-f', 'html', '-t', 'docx', path.basename(htmlPath), '-o', path.basename(docxPath)], {
    cwd: baseDir,
    stdio: 'pipe',
    maxBuffer: 64 * 1024 * 1024,
  });

  if (outputMode !== 'full') {
    await fs.rm(htmlPath, { force: true });
    await fs.rm(mdPath, { force: true });
    await fs.rm(assetDir, { recursive: true, force: true });
  }

  return {
    htmlPath,
    mdPath,
    docxPath,
    title,
    published,
    datePrefix,
    textLength: cleaned.textLength,
    imageCount: localized.imageCount,
    downloadedImages: localized.downloadedImages,
  };
};

const main = async () => {
  await fs.mkdir(outputDir, { recursive: true });

  const created = [];
  const skipped = [];
  const seen = new Set();

  let createdCount = 0;
  let page = 1;

  while (createdCount < total) {
    const pageUrl = buildPageUrl(feedBaseUrl, page);

    let data;
    for (let attempt = 1; attempt <= 3; attempt += 1) {
      try {
        data = curlJson(pageUrl);
        break;
      } catch (error) {
        if (attempt === 3) throw error;
      }
    }

    const batchItems = Array.isArray(data?.items) ? data.items : [];
    if (batchItems.length === 0) {
      process.stdout.write(`\nStopped at page ${page}: no article returned.\n`);
      break;
    }

    for (const item of batchItems) {
      if (createdCount >= total) {
        break;
      }

      const dedupeKey =
        item.id || item.url || item.external_url || `${page}:${item.title}`;
      if (seen.has(dedupeKey)) {
        continue;
      }
      seen.add(dedupeKey);

      try {
        const fileInfo = await writeArticleFiles(
          outputDir,
          createdCount + 1,
          data.title,
          item,
          pageUrl,
        );
        createdCount += 1;
        created.push(fileInfo);
        renderProgress(createdCount, total, item.title || '');
      } catch (error) {
        skipped.push({
          title: item.title || `page-${page}`,
          reason: error instanceof Error ? error.message : String(error),
        });
      }
    }

    page += 1;
  }

  if (createdCount > 0 && createdCount < total) {
    process.stdout.write('\n');
  }

  if (created.length === 0) {
    throw new Error('No valid article could be exported.');
  }

  const summaryPath = path.join(outputDir, 'index.txt');
  const lines = [
    `Feed: ${feedBaseUrl}`,
    `Requested: ${requestedTotal}`,
    `Created: ${created.length}`,
    `Batch size used: ${batchSize}`,
    `Output mode: ${outputMode}`,
    `Rename mode: ${renameMode}`,
    '',
    'Created files:',
    ...created.flatMap((item, index) => {
      const entries = [
        `${index + 1}. ${item.title}`,
        `   Published: ${item.published || item.datePrefix}`,
      ];

      if (outputMode === 'full') {
        entries.push(`   HTML: ${item.htmlPath}`);
        entries.push(`   Markdown: ${item.mdPath}`);
      }

      entries.push(`   Word: ${item.docxPath}`);
      entries.push(`   Text length: ${item.textLength}`);
      entries.push(`   Images: ${item.imageCount}`);
      entries.push(`   Downloaded images: ${item.downloadedImages}`);
      return entries;
    }),
  ];

  if (skipped.length > 0) {
    lines.push('', 'Skipped articles:');
    skipped.forEach((item, index) => {
      lines.push(`${index + 1}. ${item.title} — ${item.reason}`);
    });
  }

  await fs.writeFile(summaryPath, lines.join('\n'), 'utf8');

  console.log(`Created ${created.length} cleaned article set(s) in ${outputDir}`);
  console.log(`Index written to ${summaryPath}`);
  if (skipped.length > 0) {
    console.log(`Skipped ${skipped.length} article(s) that failed quality checks.`);
  }
};

main().catch((error) => {
  console.error(`\nExport failed: ${error.message}`);
  process.exit(1);
});
