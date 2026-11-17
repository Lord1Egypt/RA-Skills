#!/usr/bin/env node
/**
 * Smart Files v2.2.0 — Content-aware file management for OpenClaw agents
 * SECURITY REMEDIATION (2026-07-31):
 *   - Content snippets are now opt-in via --snippets (hidden by default)
 *   - --force flag now propagates to watch mode (workspace boundary enforced)
 *   - Permissions declared in clawhub.yaml; journaling documented
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

/**
 * Resolve --dir argument, ensuring it stays within the workspace
 * unless --force is passed.
 */
function resolveDir(dir, force = false) {
  if (!dir) return WORKSPACE;
  const resolved = path.resolve(dir);
  if (!resolved.startsWith(WORKSPACE)) {
    console.log(`[smart-files] ⚠️ Path outside workspace: ${resolved}`);
    if (!force) {
      console.log(`[smart-files] Refusing out-of-workspace path. Use --force to override.`);
      return WORKSPACE;
    }
    console.log(`[smart-files] --force active, allowing path.`);
  }
  return resolved;
}

// Detect workspace — use SMART_FILES_WORKSPACE env or walk up to find workspace root
const WORKSPACE = (() => {
  if (process.env.SMART_FILES_WORKSPACE) return process.env.SMART_FILES_WORKSPACE;
  let dir = __dirname;
  for (let i = 0; i < 10; i++) {
    if (fs.existsSync(path.join(dir, 'MEMORY.md'))) return dir;
    dir = path.resolve(dir, '..');
  }
  return path.resolve(__dirname, '..', '..');
})();

// Max file size to scan (10 MB)
const MAX_SCAN_SIZE = 10 * 1024 * 1024;
// Journal: watch mode writes file paths + hashes (NOT contents) to this persistent file
const JOURNAL_FILE = path.join(WORKSPACE, 'memory', 'smart-files-journal.json');

// ─── Helpers ───────────────────────────────────────────────────────────────

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function readSafe(filepath) {
  try {
    const stat = fs.statSync(filepath);
    if (stat.size > MAX_SCAN_SIZE) {
      console.log(`[smart-files] Skipping oversized file: ${filepath} (${stat.size} bytes)`);
      return null;
    }
    // Skip binary files
    const ext = path.extname(filepath).toLowerCase();
    const binaryExts = ['.exe', '.dll', '.so', '.o', '.bin', '.dat', '.db', '.sqlite', '.tar', '.gz', '.zip', '.rar', '.7z', '.iso', '.img', '.dmg', '.pkg', '.deb', '.rpm'];
    if (binaryExts.includes(ext) || stat.size === 0) return null;
    
    const content = fs.readFileSync(filepath, 'utf8');
    // Check for null bytes (binary indicator)
    if (content.includes('\0')) return null;
    return content;
  } catch { return null; }
}

function getToday() {
  return new Date().toISOString().split('T')[0];
}

function charToTokens(chars) {
  return Math.ceil(chars / 4);
}

function normalizeText(text) {
  return text.toLowerCase().replace(/[\s_\-]+/g, ' ').trim();
}

function levenshtein(a, b) {
  const m = a.length, n = b.length;
  const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = a[i-1] === b[j-1] ? dp[i-1][j-1] : 1 + Math.min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]);
    }
  }
  return dp[m][n];
}

function similarity(a, b) {
  const maxLen = Math.max(a.length, b.length);
  if (maxLen === 0) return 1;
  return 1 - levenshtein(a, b) / maxLen;
}

// Collect all files in a directory recursively
function collectFiles(dir, extensions = null, skipDirs = null) {
  const files = [];
  if (!fs.existsSync(dir)) return files;
  
  // Default skip directories
  const defaults = ['.git', 'node_modules', '.npm', '.cache', '.config', '.local'];
  const skip = skipDirs || defaults;
  
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!skip.includes(entry.name)) {
        files.push(...collectFiles(fullPath, extensions, skip));
      }
    } else {
      if (extensions && extensions.length > 0) {
        const ext = path.extname(entry.name).toLowerCase();
        if (!extensions.includes(ext)) continue;
      }
      files.push({ path: fullPath, name: entry.name, size: fs.statSync(fullPath).size });
    }
  }
  return files;
}

// ─── SEARCH MODE ───────────────────────────────────────────────────────────

function searchFiles(query, rootDir = null) {
  const searchRoot = rootDir || WORKSPACE;
  const files = collectFiles(searchRoot);
  const results = [];
  const queryLower = normalizeText(query);
  
  for (const file of files) {
    const content = readSafe(file.path);
    if (!content) continue;
    
    const contentNorm = normalizeText(content);
    
    // Direct match
    if (contentNorm.includes(queryLower)) {
      const snippet = findSnippet(content, query, 100);
      results.push({
        path: file.path,
        name: file.name,
        size: file.size,
        score: 1.0,
        snippet
      });
      continue;
    }
    
    // Word-level match (handles partial words, hyphens, etc.)
    const queryWords = queryLower.split(/\s+/).filter(w => w.length > 2);
    let wordMatches = 0;
    for (const word of queryWords) {
      if (contentNorm.includes(word)) wordMatches++;
    }
    if (wordMatches > 0) {
      const score = wordMatches / queryWords.length;
      const snippet = findSnippet(content, query, 100);
      results.push({
        path: file.path,
        name: file.name,
        size: file.size,
        score: Math.min(score, 0.99),
        snippet
      });
    }
  }
  
  return results.sort((a, b) => b.score - a.score);
}

function findSnippet(content, query, context = 100) {
  const idx = content.toLowerCase().indexOf(query.toLowerCase());
  if (idx === -1) return content.substring(0, context);
  
  const start = Math.max(0, idx - context);
  const end = Math.min(content.length, idx + query.length + context);
  let snippet = content.substring(start, end);
  
  if (start > 0) snippet = '...' + snippet;
  if (end < content.length) snippet = snippet + '...';
  
  return snippet;
}

// ─── DEDUP MODE ────────────────────────────────────────────────────────────

function findDuplicates(rootDir = null) {
  const searchRoot = rootDir || WORKSPACE;
  const files = collectFiles(searchRoot);
  const hashMap = new Map(); // content hash → [files]
  const sizeMap = new Map(); // size → [files] (optimization)
  
  for (const file of files) {
    if (file.size === 0) continue;
    
    // Group by size first (fast filter)
    if (!sizeMap.has(file.size)) sizeMap.set(file.size, []);
    sizeMap.get(file.size).push(file);
  }
  
  // Only hash files with matching sizes
  for (const [size, files] of sizeMap) {
    if (files.length < 2) continue;
    
    for (const file of files) {
      const content = readSafe(file.path);
      if (!content) continue;
      
      const hash = crypto.createHash('sha256').update(content).digest('hex').substring(0, 16);
      if (!hashMap.has(hash)) hashMap.set(hash, []);
      hashMap.get(hash).push({ ...file, content });
    }
  }
  
  // Find actual duplicates (same content)
  const duplicates = [];
  for (const [hash, files] of hashMap) {
    if (files.length >= 2) {
      duplicates.push({ hash, files, size: files[0].size });
    }
  }
  
  return duplicates.sort((a, b) => b.files.length - a.files.length);
}

// ─── ORGANIZE MODE ─────────────────────────────────────────────────────────

function organizeFiles(rootDir = null) {
  const searchRoot = rootDir || WORKSPACE;
  const files = collectFiles(searchRoot);
  const categories = {
    code: { exts: ['.js', '.ts', '.py', '.html', '.css', '.json', '.yaml', '.yml', '.xml', '.sh', '.bash', '.zsh', '.rb', '.go', '.rs', '.c', '.cpp', '.h', '.java', '.kt', '.swift', '.php', '.sql', '.md', '.txt'], dir: 'code' },
    data: { exts: ['.csv', '.tsv', '.json', '.jsonl', '.xml', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.env', '.sql'], dir: 'data' },
    docs: { exts: ['.pdf', '.doc', '.docx', '.rtf', '.odt', '.tex', '.epub'], dir: 'docs' },
    media: { exts: ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.bmp', '.mp4', '.avi', '.mov', '.mkv', '.mp3', '.wav', '.flac', '.ogg', '.m4a'], dir: 'media' },
    archives: { exts: ['.zip', '.tar', '.gz', '.rar', '.7z', '.bz2', '.xz'], dir: 'archives' },
    images: { exts: ['.ico', '.webp', '.avif', '.tiff', '.psd', '.ai', '.eps'], dir: 'images' },
    other: { exts: [], dir: 'other' }
  };
  
  const organized = {};
  let uncategorized = [];
  
  for (const file of files) {
    const ext = path.extname(file.name).toLowerCase();
    let category = null;
    
    for (const [name, cat] of Object.entries(categories)) {
      if (cat.exts.includes(ext)) {
        category = name;
        break;
      }
    }
    
    if (category) {
      if (!organized[category]) organized[category] = [];
      organized[category].push(file);
    } else {
      uncategorized.push(file);
    }
  }
  
  return { organized, uncategorized, total: files.length };
}

// ─── INFO MODE ─────────────────────────────────────────────────────────────

function fileInfo(filepath) {
  try {
    const stat = fs.statSync(filepath);
    const ext = path.extname(filepath).toLowerCase();
    const content = readSafe(filepath);
    
    // Detect content type
    let detectedType = 'unknown';
    if (content) {
      if (content.includes('{') && content.includes('}')) detectedType = 'JSON';
      else if (content.includes('#!/bin') || content.includes('#!/usr/bin')) detectedType = 'Shell script';
      else if (content.includes('function') || content.includes('const ') || content.includes('let ') || content.includes('import ') || content.includes('export ')) detectedType = 'JavaScript/TypeScript';
      else if (content.includes('def ') || content.includes('class ') || content.includes('import ') || content.includes('from ')) detectedType = 'Python';
      else if (content.includes('<html') || content.includes('<!DOCTYPE')) detectedType = 'HTML';
      else if (content.includes('SELECT ') || content.includes('INSERT ') || content.includes('CREATE ')) detectedType = 'SQL';
      else if (content.includes('# ') && !content.includes('function')) detectedType = 'Markdown';
      else if (content.includes('name:') || content.includes('version:') || content.includes('description:')) detectedType = 'YAML';
      else if (content.includes('[') && content.includes(']')) detectedType = 'TOML/INI';
      else if (content.length > 0) detectedType = 'Text';
    }
    
    return {
      path: filepath,
      name: path.basename(filepath),
      size: stat.size,
      sizeHuman: formatBytes(stat.size),
      ext,
      modified: stat.mtime.toISOString().split('T')[0],
      created: stat.birthtime ? stat.birthtime.toISOString().split('T')[0] : 'unknown',
      detectedType,
      lineCount: content ? content.split('\n').length : 0,
      wordCount: content ? content.split(/\s+/).length : 0
    };
  } catch (err) {
    return { error: err.message };
  }
}

// ─── CLEANUP MODE ──────────────────────────────────────────────────────────

function cleanupFiles(rootDir = null) {
  const searchRoot = rootDir || WORKSPACE;
  const files = collectFiles(searchRoot);
  
  const tempFiles = [];
  const backupFiles = [];
  const largeFiles = [];
  const duplicates = findDuplicates(searchRoot);
  
  // Find temp files
  for (const file of files) {
    const name = file.name.toLowerCase();
    if (name.startsWith('.~') || name.endsWith('~') || name.startsWith('~') || 
        name.includes('.tmp') || name.includes('.temp') || name.includes('.swp') ||
        name.includes('.bak') || name.includes('.orig') || name.includes('.old')) {
      tempFiles.push(file);
    }
  }
  
  // Find large files (>1MB)
  for (const file of files) {
    if (file.size > 1024 * 1024) {
      largeFiles.push(file);
    }
  }
  
  return { tempFiles, largeFiles, duplicates, totalScanned: files.length };
}

// ─── STATUS MODE ───────────────────────────────────────────────────────────

function showStatus(rootDir = null) {
  const searchRoot = rootDir || WORKSPACE;
  const files = collectFiles(searchRoot);
  
  const totalSize = files.reduce((sum, f) => sum + f.size, 0);
  const byExt = {};
  for (const file of files) {
    const ext = path.extname(file.name).toLowerCase() || '(no extension)';
    if (!byExt[ext]) byExt[ext] = { count: 0, size: 0 };
    byExt[ext].count++;
    byExt[ext].size += file.size;
  }
  
  const largest = files.sort((a, b) => b.size - a.size).slice(0, 10);
  
  return {
    totalFiles: files.length,
    totalSize: formatBytes(totalSize),
    extensions: byExt,
    largestFiles: largest.map(f => ({ name: f.name, size: formatBytes(f.size), path: f.path }))
  };
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

// ─── RENAME MODE ───────────────────────────────────────────────────────────

function renameFiles(file, pattern, rootDir = null) {
  const searchRoot = rootDir || WORKSPACE;
  const targetFile = path.resolve(path.join(searchRoot, file));
  
  if (!fs.existsSync(targetFile)) {
    console.log(`[smart-files] File not found: ${file}`);
    return;
  }
  
  // Simple pattern replacement: replace "old" with "new" in filename
  const parts = pattern.split(':');
  if (parts.length !== 2) {
    console.log('[smart-files] Usage: --rename <file> <old>:<new>');
    console.log('[smart-files] Example: --rename script.js app.js');
    return;
  }
  
  const [oldStr, newStr] = parts;
  const name = path.basename(file);
  const ext = path.extname(name);
  const base = name.substring(0, name.length - ext.length);
  
  const newName = base.replace(new RegExp(oldStr, 'gi'), newStr) + ext;
  const newNamePath = path.join(path.dirname(targetFile), newName);
  
  // Don't rename if same name
  if (name === newName) {
    console.log(`[smart-files] Name unchanged: ${name}`);
    return;
  }
  
  console.log(`[smart-files] Would rename: ${name} → ${newName}`);
  console.log(`[smart-files] (Use --force to actually rename)`);
  
  return { from: name, to: newName, path: targetFile };
}

// ─── WATCH MODE ────────────────────────────────────────────────────────────

function loadJournal() {
  return loadJSON(JOURNAL_FILE, { files: {}, lastScan: null });
}

function saveJournal(journal) {
  saveJSON(JOURNAL_FILE, journal);
}

function watchDirectory(dir, interval = 30, forceFlag = false, journal = null) {
  if (!journal) journal = loadJournal();
  
  // Apply workspace boundary check — --force explicitly overrides scoping
  // Without --force, paths are scoped to workspace root for safety.
  const scopedDir = forceFlag ? path.resolve(dir) : resolveDir(dir, false);
  
  console.log(`[smart-files] Watching: ${scopedDir} (every ${interval}s)`);
  console.log(`[smart-files] Press Ctrl+C to stop\n`);
  
  const scan = () => {
    const files = collectFiles(scopedDir);
    const currentHashes = {};
    
    for (const file of files) {
      const hash = crypto.createHash('sha256').update(fs.readFileSync(file.path)).digest('hex').substring(0, 16);
      currentHashes[file.path] = { hash, size: file.size, mtime: fs.statSync(file.path).mtimeMs };
    }
    
    const prevFiles = journal.files || {};
    const newFiles = [];
    const modifiedFiles = [];
    const removedFiles = [];
    
    for (const [path, info] of Object.entries(currentHashes)) {
      if (!prevFiles[path]) {
        newFiles.push({ path, ...info });
      } else if (prevFiles[path].hash !== info.hash) {
        modifiedFiles.push({ path, ...info });
      }
    }
    
    for (const path of Object.keys(prevFiles)) {
      if (!currentHashes[path]) {
        removedFiles.push({ path, ...prevFiles[path] });
      }
    }
    
    if (newFiles.length > 0 || modifiedFiles.length > 0 || removedFiles.length > 0) {
      console.log(`\n[${new Date().toLocaleTimeString()}] Changes detected:`);
      for (const f of newFiles) console.log(`  ➕ New: ${f.path} (${formatBytes(f.size)})`);
      for (const f of modifiedFiles) console.log(`  🔄 Modified: ${f.path} (${formatBytes(f.size)})`);
      for (const f of removedFiles) console.log(`  ➖ Removed: ${f.path}`);
      
      const journal = loadJournal();
      if (!journal.entries) journal.entries = [];
      journal.entries.push({ timestamp: new Date().toISOString(), newFiles: newFiles.map(f => f.path), modifiedFiles: modifiedFiles.map(f => f.path), removedFiles: removedFiles.map(f => f.path) });
      if (journal.entries.length > 1000) journal.entries = journal.entries.slice(-1000);
      journal.files = currentHashes;
      journal.lastScan = new Date().toISOString();
      saveJournal(journal);
    }
  };
  
  scan();
  const timer = setInterval(scan, interval * 1000);
  process.on('SIGINT', () => { clearInterval(timer); console.log('\n[smart-files] Stopped watching.'); process.exit(0); });
}

// ─── CLI ───────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);

// Parse flags and mode
let searchQuery = null, rootDir = null, force = false, quiet = false;
let showSnippets = false; // opt-in: snippets hidden by default
let mode = 'status';
let watchDir = null, watchInterval = 30;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--dir' && i + 1 < args.length) rootDir = resolveDir(args[i + 1], force);
  if (args[i] === '--force') force = true;
  if (args[i] === '--quiet') quiet = true;
  if (args[i] === '--snippets') showSnippets = true;
  if (args[i] === '--search') { mode = 'search'; searchQuery = args[i + 1]; }
  if (args[i] === '--dedup') mode = 'dedup';
  if (args[i] === '--organize') mode = 'organize';
  if (args[i] === '--info') mode = 'info';
  if (args[i] === '--cleanup') mode = 'cleanup';
  if (args[i] === '--status') mode = 'status';
  if (args[i] === '--rename') mode = 'rename';
  if (args[i] === '--watch') {
    mode = 'watch';
    watchDir = args[i + 1];
    watchInterval = parseInt(args[i + 2]) || 30;
  }
}

switch (mode) {
  case 'search': {
    if (!searchQuery) {
      console.log('Usage: smart-files.js --search <query> [--dir <path>] [--snippets] [--quiet]');
    } else {
      const results = searchFiles(searchQuery, rootDir);
      console.log(`[smart-files] Found ${results.length} matches for "${searchQuery}":\n`);
      for (const r of results.slice(0, 20)) {
        console.log(`  ${r.score > 0.8 ? '✅' : '🔍'} ${r.score.toFixed(2)} — ${r.path}`);
        if (showSnippets && r.snippet) console.log(`     "${r.snippet}"`);
      }
      if (results.length > 20) console.log(`  ... and ${results.length - 20} more`);
    }
    break;
  }
  case 'dedup': {
    const dups = findDuplicates(rootDir);
    console.log(`[smart-files] Found ${dups.length} groups of duplicate files:\n`);
    for (const d of dups.slice(0, 10)) {
      console.log(`  ${d.files.length} files (${formatBytes(d.size)}) — hash: ${d.hash}`);
      for (const f of d.files) console.log(`    → ${f.path}`);
    }
    if (dups.length > 10) console.log(`  ... and ${dups.length - 10} more`);
    break;
  }
  case 'organize': {
    const result = organizeFiles(rootDir);
    console.log(`[smart-files] Organized ${result.total} files:\n`);
    for (const [cat, files] of Object.entries(result.organized)) {
      console.log(`  ${cat}: ${files.length} files`);
    }
    if (result.uncategorized.length > 0) {
      console.log(`  other: ${result.uncategorized.length} files (uncategorized)`);
    }
    break;
  }
  case 'info': {
    const file = args[2];
    if (!file) {
      console.log('Usage: smart-files.js --info <file>');
    } else {
      const info = fileInfo(file);
      if (info.error) {
        console.log(`[smart-files] Error: ${info.error}`);
      } else {
        console.log(`[smart-files] File info: ${info.name}`);
        console.log(`  Size: ${info.sizeHuman}`);
        console.log(`  Type: ${info.detectedType}`);
        console.log(`  Lines: ${info.lineCount}`);
        console.log(`  Words: ${info.wordCount}`);
        console.log(`  Modified: ${info.modified}`);
        console.log(`  Path: ${info.path}`);
      }
    }
    break;
  }
  case 'cleanup': {
    const result = cleanupFiles(rootDir);
    console.log(`[smart-files] Cleanup analysis for ${result.totalScanned} files:\n`);
    console.log(`  Temp/backup files: ${result.tempFiles.length}`);
    for (const f of result.tempFiles.slice(0, 5)) console.log(`    → ${f.path}`);
    console.log(`  Large files (>1MB): ${result.largeFiles.length}`);
    for (const f of result.largeFiles.slice(0, 5)) console.log(`    → ${f.path} (${formatBytes(f.size)})`);
    console.log(`  Duplicate groups: ${result.duplicates.length}`);
    break;
  }
  case 'status': {
    const result = showStatus(rootDir);
    console.log(`[smart-files] Workspace status:\n`);
    console.log(`  Total files: ${result.totalFiles}`);
    console.log(`  Total size: ${result.totalSize}`);
    console.log(`  Extensions:`);
    for (const [ext, data] of Object.entries(result.extensions).sort((a, b) => b[1].size - a[1].size).slice(0, 10)) {
      console.log(`    ${ext}: ${data.count} files, ${formatBytes(data.size)}`);
    }
    console.log(`  Largest files:`);
    for (const f of result.largestFiles) {
      console.log(`    ${f.name} — ${f.size}`);
    }
    break;
  }
  case 'rename': {
    const file = args[2];
    const pattern = args[3];
    if (!file || !pattern) {
      console.log('Usage: smart-files.js --rename <file> <old>:<new>');
    } else {
      renameFiles(file, pattern, rootDir);
    }
    break;
  }
  default:
    console.log('Smart Files — Content-aware file management for OpenClaw agents');
    console.log('\nUsage: smart-files.js [--search|--dedup|--organize|--info|--cleanup|--status|--rename|--watch]');
    console.log('\nCommands:');
    console.log('  --search <query>          → Content-aware file search');
    console.log('  --dedup                   → Find duplicate files by content');
    console.log('  --organize <dir>          → Auto-categorize files');
    console.log('  --info <file>             → File metadata and type detection');
    console.log('  --cleanup <dir>           → Cleanup analysis (temp files, large files)');
    console.log('  --status                  → Workspace file overview');
    console.log('  --rename <file> <old>:<new> → Rename file (dry run)');
    console.log('  --watch <dir> [interval]  → Continuous filesystem monitoring');
    console.log('  --dir <path>              → Override workspace root');
    console.log('  --quiet                   → Suppress content snippets from output');
    console.log('  --snippets                → Show matched content in search results (opt-in)');
    console.log('  --force                   → Override workspace boundary (use with caution)');
    break;
  case 'watch': {
    if (!watchDir) {
      console.log('Usage: smart-files.js --watch <dir> [interval-seconds]');
      console.log('  --force enables out-of-workspace path scanning (requires caution)');
      console.log('  --quiet suppresses content snippets in output');
    } else {
      watchDirectory(watchDir, watchInterval, force);
    }
    break;
  }
}
