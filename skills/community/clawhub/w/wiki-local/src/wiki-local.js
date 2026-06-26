/**
 * WikiLocal — Personal Knowledge Wiki
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');
const path = require('path');

class WikiLocal {
  constructor(options = {}) {
    this.wikiDir = options.wikiDir || './wiki/articles';
    this.indexFile = options.indexFile || './wiki/index.json';
    if (!fs.existsSync(this.wikiDir)) fs.mkdirSync(this.wikiDir, { recursive: true });
  }

  add(title, content, tags = [], relatedTo = []) {
    const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    if (!slug) return { error: 'Title must contain alphanumeric characters' };
    const file = path.join(this.wikiDir, slug + '.md');
    const header = `# ${title}\nTags: ${tags.join(', ')}\nRelated: ${relatedTo.join(', ')}\n\n`;
    fs.writeFileSync(file, header + content);
    this._updateIndex(slug, title, tags, relatedTo);
    // Create stubs for related articles that don't exist
    for (const r of relatedTo) {
      const rSlug = r.toLowerCase().replace(/[^a-z0-9]+/g, '-');
      const rFile = path.join(this.wikiDir, rSlug + '.md');
      if (!fs.existsSync(rFile)) {
        fs.writeFileSync(rFile, `# ${r}\n\n*Stub — expand this article.*\n`);
        this._updateIndex(rSlug, r, [], [title]);
      }
    }
    return { slug, title, file, linked: relatedTo.length };
  }

  get(titleOrSlug) {
    const slug = titleOrSlug.toLowerCase().replace(/[^a-z0-9]+/g, '-');
    const file = path.join(this.wikiDir, slug + '.md');
    try { return fs.readFileSync(file, 'utf8'); } catch { return null; }
  }

  search(query) {
    const q = query.toLowerCase();
    const index = this._getIndex();
    const results = [];
    const escaped = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    for (const [slug, meta] of Object.entries(index)) {
      const content = this.get(slug) || '';
      if (meta.title.toLowerCase().includes(q) || content.toLowerCase().includes(q) || meta.tags.some(t => t.toLowerCase().includes(q))) {
        results.push({ slug, title: meta.title, matches: (content.match(new RegExp(escaped, 'gi')) || []).length });
      }
    }
    return results.sort((a, b) => b.matches - a.matches);
  }

  backlinks(titleOrSlug) {
    const slug = titleOrSlug.toLowerCase().replace(/[^a-z0-9]+/g, '-');
    const index = this._getIndex();
    return Object.entries(index).filter(([, meta]) => meta.relatedTo.some(r => r.toLowerCase().replace(/[^a-z0-9]+/g, '-') === slug)).map(([s, m]) => ({ slug: s, title: m.title }));
  }

  stats() {
    const index = this._getIndex();
    const articles = Object.keys(index).length;
    const stubs = Object.values(index).filter(m => m.tags.length === 0 && m.relatedTo.length === 0).length;
    return { articles, stubs, complete: articles - stubs };
  }

  _getIndex() { try { return JSON.parse(fs.readFileSync(this.indexFile, 'utf8')); } catch { return {}; } }
  _updateIndex(slug, title, tags, relatedTo) {
    const index = this._getIndex();
    index[slug] = { title, tags, relatedTo, updated: new Date().toISOString() };
    fs.writeFileSync(this.indexFile, JSON.stringify(index, null, 2));
  }
}

module.exports = { WikiLocal };
