import nodeFetch from 'node-fetch';
import pool from '../browser.js';

/**
 * Smart content fetcher. Tries the lightest approach first:
 * HTTP + markdown extraction → browser rendering → screenshot
 *
 * @param {string} url - URL to fetch
 * @param {object} options
 * @param {string} options.format - 'markdown' | 'html' | 'json' | 'screenshot' (default: 'markdown')
 * @param {boolean} options.javascript - Force browser rendering (default: false)
 * @param {object} options.headers - Additional HTTP headers
 * @param {string} options.session - Session/cookie domain to use
 * @returns {object} { content, format, source, url }
 */
export async function fetch(url, options = {}) {
  const {
    format = 'markdown',
    javascript = false,
    headers = {},
    session = null,
  } = options;

  // Screenshot always needs browser
  if (format === 'screenshot') {
    return await fetchWithBrowser(url, 'screenshot', session);
  }

  // If JS explicitly requested, go straight to browser
  if (javascript) {
    return await fetchWithBrowser(url, format, session);
  }

  // Try HTTP first (fast path)
  try {
    const result = await fetchWithHTTP(url, format, headers);
    if (result.content && result.content.length > 50) {
      return result;
    }
    // Content too short — probably a JS-rendered SPA, fall through to browser
    console.log('[fetch] HTTP content too short, trying browser');
  } catch (e) {
    console.log(`[fetch] HTTP failed: ${e.message}, trying browser`);
  }

  // Fall back to browser
  return await fetchWithBrowser(url, format, session);
}

async function fetchWithHTTP(url, format, headers = {}) {
  const response = await nodeFetch(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      ...headers,
    },
    timeout: 15000,
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status} ${response.statusText}`);
  }

  const contentType = response.headers.get('content-type') || '';

  // JSON format — return parsed JSON
  if (format === 'json' || contentType.includes('application/json')) {
    const json = await response.json();
    return { content: json, format: 'json', source: 'http', url };
  }

  const html = await response.text();

  if (format === 'html') {
    return { content: html, format: 'html', source: 'http', url };
  }

  // Default: convert to markdown
  const markdown = htmlToMarkdown(html);
  return { content: markdown, format: 'markdown', source: 'http', url };
}

async function fetchWithBrowser(url, format, session) {
  const domain = pool.getDomain(url);
  const page = await pool.getPage(session || domain);

  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

    if (format === 'screenshot') {
      const filepath = await pool.screenshot(page, domain);
      return { content: filepath, format: 'screenshot', source: 'browser', url };
    }

    if (format === 'json') {
      const text = await page.innerText('body');
      try {
        const json = JSON.parse(text);
        return { content: json, format: 'json', source: 'browser', url };
      } catch {
        return { content: text, format: 'text', source: 'browser', url };
      }
    }

    if (format === 'html') {
      const html = await page.content();
      return { content: html, format: 'html', source: 'browser', url };
    }

    // Default: markdown from rendered page
    const text = await page.innerText('body');
    return { content: text.trim(), format: 'markdown', source: 'browser', url };
  } finally {
    await page.close();
  }
}

/**
 * Basic HTML to markdown conversion.
 * Strips tags, preserves structure. Not perfect — good enough for MVP.
 */
function htmlToMarkdown(html) {
  let text = html;

  // Remove script and style blocks
  text = text.replace(/<script[\s\S]*?<\/script>/gi, '');
  text = text.replace(/<style[\s\S]*?<\/style>/gi, '');
  text = text.replace(/<noscript[\s\S]*?<\/noscript>/gi, '');

  // Convert headings
  text = text.replace(/<h1[^>]*>([\s\S]*?)<\/h1>/gi, '\n# $1\n');
  text = text.replace(/<h2[^>]*>([\s\S]*?)<\/h2>/gi, '\n## $1\n');
  text = text.replace(/<h3[^>]*>([\s\S]*?)<\/h3>/gi, '\n### $1\n');
  text = text.replace(/<h4[^>]*>([\s\S]*?)<\/h4>/gi, '\n#### $1\n');
  text = text.replace(/<h5[^>]*>([\s\S]*?)<\/h5>/gi, '\n##### $1\n');
  text = text.replace(/<h6[^>]*>([\s\S]*?)<\/h6>/gi, '\n###### $1\n');

  // Convert links
  text = text.replace(/<a[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi, '[$2]($1)');

  // Convert bold/italic
  text = text.replace(/<(strong|b)[^>]*>([\s\S]*?)<\/\1>/gi, '**$2**');
  text = text.replace(/<(em|i)[^>]*>([\s\S]*?)<\/\1>/gi, '*$2*');

  // Convert code
  text = text.replace(/<code[^>]*>([\s\S]*?)<\/code>/gi, '`$1`');
  text = text.replace(/<pre[^>]*>([\s\S]*?)<\/pre>/gi, '\n```\n$1\n```\n');

  // Convert lists
  text = text.replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, '- $1\n');

  // Convert paragraphs and line breaks
  text = text.replace(/<br\s*\/?>/gi, '\n');
  text = text.replace(/<p[^>]*>([\s\S]*?)<\/p>/gi, '\n$1\n');
  text = text.replace(/<div[^>]*>([\s\S]*?)<\/div>/gi, '\n$1\n');

  // Remove all remaining tags
  text = text.replace(/<[^>]+>/g, '');

  // Decode HTML entities
  text = text.replace(/&amp;/g, '&');
  text = text.replace(/&lt;/g, '<');
  text = text.replace(/&gt;/g, '>');
  text = text.replace(/&quot;/g, '"');
  text = text.replace(/&#39;/g, "'");
  text = text.replace(/&nbsp;/g, ' ');

  // Clean up whitespace
  text = text.replace(/\n{3,}/g, '\n\n');
  text = text.trim();

  return text;
}

export { htmlToMarkdown };
