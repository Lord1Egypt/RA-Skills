import fs from 'node:fs';
import path from 'node:path';

const HISTORY_DIR = path.join(process.env.HOME, '.openclaw', 'workspace', '.session_history');
const CACHE_TTL_MS = 10 * 60 * 1000; // 10 分钟缓存过期
const cache = new Map(); // Map<sessionKey, { content, timestamp }>

// 输出到 openclaw 日志（通过 `openclaw logs` 查看）
function log(msg) {
  console.log(`[session-history] ${msg}`);
}

function sessionKeyToDir(sessionKey) {
  return sessionKey.replace(/:/g, '_');
}

function getLatestArchive(sessionKey) {
  // 检查缓存是否过期
  const cached = cache.get(sessionKey);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL_MS) {
    return cached.content;
  }

  try {
    const dirName = sessionKeyToDir(sessionKey);
    const dir = path.join(HISTORY_DIR, dirName);

    // 直接 readdir，不用 existsSync 做额外检查
    const files = fs.readdirSync(dir)
      .filter(f => f.endsWith('.md'))
      .sort()
      .reverse();

    if (files.length === 0) return null;

    const latest = path.join(dir, files[0]);
    const content = fs.readFileSync(latest, 'utf-8');

    if (!content || content.trim().length === 0) return null;

    // 更新缓存（带时间戳）
    cache.set(sessionKey, { content, timestamp: Date.now() });
    return content;
  } catch (err) {
    // 只在出错时记录日志
    if (err.code === 'ENOENT') return null;
    log(`Error reading archive: ${err.message}`);
    return null;
  }
}

export default async function handler(event) {
  const ctx = event.context || {};
  const sessionKey = event.sessionKey || ctx.sessionKey;
  const bootstrapFiles = ctx.bootstrapFiles;

  if (!sessionKey || !Array.isArray(bootstrapFiles)) return;

  const archive = getLatestArchive(sessionKey);
  if (!archive) return;

  log(`Injecting history for sessionKey=${sessionKey}`);

  const bootstrapIndex = bootstrapFiles.findIndex(f => f.name === 'BOOTSTRAP.md');

  if (bootstrapIndex >= 0) {
    const existing = bootstrapFiles[bootstrapIndex];
    const existingContent = existing.content || '';
    existing.content = `${existingContent}\n\n## Previous Session History\n${archive}`;
  } else {
    bootstrapFiles.push({
      name: 'BOOTSTRAP.md',
      path: path.join(HISTORY_DIR, sessionKeyToDir(sessionKey)),
      content: `## Previous Session History\n${archive}`,
      missing: false,
    });
  }
}
