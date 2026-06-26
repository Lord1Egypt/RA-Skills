/**
 * WebClip — Save & Summarize Web Pages
 * @author @TheShadowRose
 * @license MIT
 */
const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

class WebClip {
  constructor(options = {}) {
    this.cacheDir = options.cacheDir || './web-cache';
    if (!fs.existsSync(this.cacheDir)) fs.mkdirSync(this.cacheDir, { recursive: true });
  }

  async fetch(url) {
    const html = await this._get(url);
    const title = (html.match(/<title[^>]*>(.*?)<\/title>/is) || [, url])[1].trim();
    const text = this._stripHtml(html);
    const markdown = this._toMarkdown(html, title);
    const metadata = { url, title, fetchedAt: new Date().toISOString(), wordCount: text.split(/\s+/).length };
    return { title, text, markdown, metadata, html };
  }

  async batchFetch(urls) {
    return Promise.all(urls.map(u => this.fetch(u).catch(e => ({ url: u, error: e.message }))));
  }

  save(clip, filename) {
    const slug = (clip.title || 'untitled').replace(/[^a-z0-9]/gi, '-').substring(0, 60).replace(/^-|-$/g, '') || 'clip';
    const file = path.join(this.cacheDir, filename || slug + '.md');
    fs.writeFileSync(file, clip.markdown);
    return file;
  }

  _get(url, _redirects = 0) {
    if (_redirects > 5) return Promise.reject(new Error('Too many redirects'));
    // Block internal/metadata URLs
    const parsed = new URL(url);
    const h = parsed.hostname.replace(/^\[|\]$/g, ''); // Strip IPv6 brackets
    if (/^(127\.|10\.|172\.(1[6-9]|2\d|3[01])\.|192\.168\.|169\.254\.|0\.|localhost$|::1$|::ffff:|0{1,4}:|fe80:)/i.test(h)) {
      return Promise.reject(new Error('Blocked: internal URL'));
    }
    const client = url.startsWith('https') ? https : http;
    return new Promise((resolve, reject) => {
      const req = client.get(url, { headers: { 'User-Agent': 'WebClip/1.0' }, timeout: 10000 }, res => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          return this._get(res.headers.location, _redirects + 1).then(resolve).catch(reject);
        }
        let data = '';
        const maxSize = 10 * 1024 * 1024; // 10MB max
        res.on('data', c => { data += c; if (data.length > maxSize) { req.destroy(); reject(new Error('Response too large')); } });
        res.on('end', () => resolve(data));
      });
      req.on('error', reject);
      req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
    });
  }

  _stripHtml(html) {
    return html
      .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
      .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
      .replace(/<nav[^>]*>[\s\S]*?<\/nav>/gi, '')
      .replace(/<footer[^>]*>[\s\S]*?<\/footer>/gi, '')
      .replace(/<header[^>]*>[\s\S]*?<\/header>/gi, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/\s+/g, ' ')
      .trim();
  }

  _toMarkdown(html, title) {
    let md = `# ${title}\n\n`;
    const body = (html.match(/<body[^>]*>([\s\S]*)<\/body>/i) || [, html])[1];
    md += body
      .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
      .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
      .replace(/<h1[^>]*>(.*?)<\/h1>/gi, '\n# $1\n')
      .replace(/<h2[^>]*>(.*?)<\/h2>/gi, '\n## $1\n')
      .replace(/<h3[^>]*>(.*?)<\/h3>/gi, '\n### $1\n')
      .replace(/<li[^>]*>(.*?)<\/li>/gi, '- $1\n')
      .replace(/<p[^>]*>(.*?)<\/p>/gi, '\n$1\n')
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<a[^>]*href="([^"]*)"[^>]*>(.*?)<\/a>/gi, '[$2]($1)')
      .replace(/<strong[^>]*>(.*?)<\/strong>/gi, '**$1**')
      .replace(/<em[^>]*>(.*?)<\/em>/gi, '*$1*')
      .replace(/<code[^>]*>(.*?)<\/code>/gi, '\x60$1\x60')
      .replace(/<[^>]+>/g, '')
      .replace(/\n{3,}/g, '\n\n')
      .trim();
    return md;
  }
}

module.exports = { WebClip };
