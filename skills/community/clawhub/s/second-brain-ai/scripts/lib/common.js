const fs = require('fs');
const path = require('path');

function resolveVaultPath() {
  const raw = process.env.SECOND_BRAIN_VAULT || '';
  if (!raw.trim()) {
    throw new Error('SECOND_BRAIN_VAULT is required. Set it to an explicit local Markdown vault path before using this skill.');
  }
  return path.resolve(raw);
}

const VAULT_PATH = resolveVaultPath();
const INDEX_DIR = path.join(VAULT_PATH, '.secondbrain');
const INDEX_DB_PATH = path.join(INDEX_DIR, 'index.db');

const DEFAULT_IGNORE_PATTERNS = [
  '.git', '.obsidian', '.logseq', '.trash', 'node_modules', '.DS_Store',
  'README.md', 'README', 'CHANGELOG.md', 'LICENSE.md', 'CONTRIBUTING.md', 'templates'
];

function getDb() { return null; }
function hasIndex() { return false; }
function getVaultPath() { return VAULT_PATH; }
function getIndexPath() { return INDEX_DB_PATH; }

function loadIgnorePatterns() {
  const ignoreFile = path.join(VAULT_PATH, '.secondbrainignore');
  const patterns = [...DEFAULT_IGNORE_PATTERNS];
  if (fs.existsSync(ignoreFile)) {
    try {
      const content = fs.readFileSync(ignoreFile, 'utf-8');
      const lines = content.split('\n').map(x => x.trim()).filter(x => x && !x.startsWith('#'));
      patterns.push(...lines);
    } catch (_) {}
  }
  return patterns;
}

function shouldIgnore(filePath, ignorePatterns) {
  const basename = path.basename(filePath);
  const relativePath = path.relative(VAULT_PATH, filePath);
  for (const pattern of ignorePatterns) {
    if (basename === pattern) return true;
    if (relativePath.includes('/' + pattern + '/')) return true;
    if (relativePath.startsWith(pattern + '/')) return true;
    if (pattern.includes('*')) {
      const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$');
      if (regex.test(basename)) return true;
    }
  }
  return false;
}

function readVaultDir(dir, files = [], ignorePatterns = null) {
  if (!fs.existsSync(dir)) return files;
  const patterns = ignorePatterns || loadIgnorePatterns();
  for (const item of fs.readdirSync(dir)) {
    const fullPath = path.join(dir, item);
    if (shouldIgnore(fullPath, patterns)) continue;
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) readVaultDir(fullPath, files, patterns);
    else if (item.endsWith('.md')) files.push(fullPath);
  }
  return files;
}

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return { frontmatter: {}, body: content };
  const frontmatter = {};
  for (const line of match[1].split('\n')) {
    const i = line.indexOf(':');
    if (i > 0) {
      const key = line.slice(0, i).trim();
      const value = line.slice(i + 1).trim();
      if (value.startsWith('[') && value.endsWith(']')) {
        frontmatter[key] = value.slice(1, -1).split(',').map(s => s.trim()).filter(Boolean);
      } else {
        frontmatter[key] = value;
      }
    }
  }
  return { frontmatter, body: content.slice(match[0].length).trim() };
}

function extractWikiLinks(content) {
  const links = [];
  const regex = /\[\[([^\]]+)\]\]/g;
  let match;
  while ((match = regex.exec(content)) !== null) links.push(match[1]);
  return [...new Set(links)];
}

function extractTags(content) {
  const tags = [];
  const regex = /#([a-zA-Z0-9_\u4e00-\u9fa5]+)/g;
  let match;
  while ((match = regex.exec(content)) !== null) tags.push(match[1]);
  return [...new Set(tags)];
}

function generateId() {
  return new Date().toISOString().slice(0, 10).replace(/-/g, '');
}

function sanitizeFilename(title) {
  return title.replace(/[<>:"/\\|?*]/g, '-').replace(/\s+/g, '-').slice(0, 50);
}

function buildFrontmatter(data) {
  const today = new Date().toISOString().split('T')[0];
  const lines = ['---'];
  lines.push(`id: ${data.id || generateId()}`);
  lines.push(`title: ${data.title}`);
  lines.push(`type: ${data.type || 'note'}`);
  if (data.tags && data.tags.length > 0) lines.push(`tags: [${data.tags.join(', ')}]`);
  lines.push(`created: ${today}`);
  lines.push(`updated: ${today}`);
  lines.push('status: active');
  if (data.links && data.links.length > 0) {
    lines.push('links:');
    for (const link of data.links) lines.push(`  - ${link}`);
  }
  lines.push('---');
  return lines.join('\n');
}

function resolveInput(input, ...keys) {
  for (const key of keys) if (input[key] !== undefined) return input[key];
  return undefined;
}

function requireWriteApproval(data, flag = 'allow_write') {
  if (!data || data[flag] !== true) throw new Error(`Explicit ${flag}=true is required for write operations in this skill.`);
}

function indexNote() { return false; }
function rebuildIndex() {
  return {
    status: 'skipped',
    reason: 'SQLite indexing is not implemented in this repair build; Markdown remains the source of truth and file-scan mode is active.'
  };
}

function findNoteByTitle(title) {
  const files = readVaultDir(VAULT_PATH);
  for (const filePath of files) {
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const { frontmatter } = parseFrontmatter(content);
      const fileTitle = frontmatter.title || path.basename(filePath, '.md');
      if (fileTitle.toLowerCase() === title.toLowerCase()) {
        return { path: path.relative(VAULT_PATH, filePath), title: fileTitle, ...frontmatter };
      }
    } catch (_) {}
  }
  return null;
}

module.exports = {
  VAULT_PATH,
  INDEX_DIR,
  INDEX_DB_PATH,
  getDb,
  hasIndex,
  getVaultPath,
  getIndexPath,
  loadIgnorePatterns,
  shouldIgnore,
  readVaultDir,
  parseFrontmatter,
  extractWikiLinks,
  extractTags,
  generateId,
  sanitizeFilename,
  buildFrontmatter,
  resolveInput,
  requireWriteApproval,
  indexNote,
  rebuildIndex,
  findNoteByTitle,
};
