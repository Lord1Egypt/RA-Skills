const http = require('http');
const fs = require('fs');
const path = require('path');
const WebSocket = require('ws');
const crypto = require('crypto');

const { execSync } = require('child_process');
const os = require('os');

const PORT = process.env.RTS_PORT || 4320;
const GATEWAY_PORT = process.env.OPENCLAW_GATEWAY_PORT || 18789;
const GATEWAY_URL = `http://127.0.0.1:${GATEWAY_PORT}`;
const HOME = os.homedir();
const OPENCLAW_HOME = process.env.OPENCLAW_HOME || path.join(HOME, '.openclaw');

// --- 跨平台查找 openclaw 安装目录 ---
function findOpenclawDir() {
  // 策略1: require.resolve — 最快
  try {
    return path.dirname(require.resolve('openclaw/package.json'));
  } catch {}
  // 策略2: 从可执行文件反推
  try {
    const cmd = process.platform === 'win32' ? 'where openclaw' : 'which openclaw';
    const binPath = execSync(cmd, { encoding: 'utf8', timeout: 3000 }).trim().split('\n')[0];
    let dir = path.dirname(fs.realpathSync(binPath));
    while (dir !== path.dirname(dir)) {
      const pkg = path.join(dir, 'package.json');
      if (fs.existsSync(pkg)) {
        try { if (JSON.parse(fs.readFileSync(pkg, 'utf8')).name === 'openclaw') return dir; } catch {}
      }
      dir = path.dirname(dir);
    }
  } catch {}
  // 策略3: npm root -g
  try {
    const root = execSync('npm root -g', { encoding: 'utf8', timeout: 5000 }).trim();
    const candidate = path.join(root, 'openclaw');
    if (fs.existsSync(path.join(candidate, 'package.json'))) return candidate;
  } catch {}
  // 策略4: 常见路径兜底
  const fallbacks = process.platform === 'win32'
    ? [path.join(HOME, 'AppData', 'Roaming', 'npm', 'node_modules', 'openclaw')]
    : [
        '/usr/local/lib/node_modules/openclaw',
        '/usr/lib/node_modules/openclaw',
        path.join(HOME, '.npm-global', 'lib', 'node_modules', 'openclaw'),
      ];
  for (const p of fallbacks) {
    if (fs.existsSync(path.join(p, 'package.json'))) return p;
  }
  return null;
}

const OPENCLAW_DIR = findOpenclawDir();
if (OPENCLAW_DIR) console.log('[RTS] OpenClaw found:', OPENCLAW_DIR);
else console.warn('[RTS] ⚠ OpenClaw installation not found, built-in skills will be unavailable');

// --- Gateway 认证 token 自动发现 ---
function getGatewayToken() {
  // 优先级: 环境变量 > openclaw.json
  if (process.env.OPENCLAW_GATEWAY_TOKEN) return process.env.OPENCLAW_GATEWAY_TOKEN;
  try {
    const config = JSON.parse(fs.readFileSync(path.join(OPENCLAW_HOME, 'openclaw.json'), 'utf8'));
    return config?.gateway?.auth?.token || null;
  } catch { return null; }
}
const GATEWAY_TOKEN = getGatewayToken();
if (GATEWAY_TOKEN) console.log('[RTS] Gateway token: found');
else console.log('[RTS] Gateway token: not configured (chat.send may fail if gateway requires auth)');

// --- Ed25519 设备签名（正经的 Gateway 认证） ---
const DEVICE_KEYS_PATH = path.join(__dirname, '.device-keys.json');

function base64UrlEncode(buf) {
  return Buffer.from(buf).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function loadOrCreateDeviceKeys() {
  try {
    if (fs.existsSync(DEVICE_KEYS_PATH)) {
      const saved = JSON.parse(fs.readFileSync(DEVICE_KEYS_PATH, 'utf8'));
      // 验证密钥可用
      crypto.createPrivateKey({ key: Buffer.from(saved.privateKeyRaw, 'base64'), type: 'pkcs8', format: 'der' });
      return saved;
    }
  } catch { /* regenerate */ }
  
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
  const publicKeyDer = publicKey.export({ type: 'spki', format: 'der' });
  const privateKeyDer = privateKey.export({ type: 'pkcs8', format: 'der' });
  // Ed25519 SPKI = 12 byte prefix + 32 byte raw key
  const publicKeyRaw = publicKeyDer.subarray(12); // skip SPKI prefix
  const deviceId = crypto.createHash('sha256').update(publicKeyRaw).digest('hex');
  
  const keys = {
    deviceId,
    publicKeyB64Url: base64UrlEncode(publicKeyRaw),
    privateKeyRaw: privateKeyDer.toString('base64'),
  };
  fs.writeFileSync(DEVICE_KEYS_PATH, JSON.stringify(keys, null, 2));
  console.log('[RTS] Generated new device keypair, id:', deviceId.substring(0, 16) + '...');
  return keys;
}

const DEVICE_KEYS = loadOrCreateDeviceKeys();
console.log('[RTS] Device ID:', DEVICE_KEYS.deviceId.substring(0, 16) + '...');

function signConnectChallenge(nonce, connectParams) {
  const privateKey = crypto.createPrivateKey({
    key: Buffer.from(DEVICE_KEYS.privateKeyRaw, 'base64'), type: 'pkcs8', format: 'der'
  });
  const signedAt = Date.now();
  const token = connectParams.auth?.token || '';
  const scopes = (connectParams.scopes || []).join(',');
  const platform = (connectParams.client?.platform || '').toLowerCase();
  // v3 payload: version|deviceId|clientId|clientMode|role|scopes|signedAtMs|token|nonce|platform|deviceFamily
  const payload = ['v3', DEVICE_KEYS.deviceId, connectParams.client.id, connectParams.client.mode,
    connectParams.role, scopes, String(signedAt), token, nonce, platform, ''].join('|');
  const signature = base64UrlEncode(crypto.sign(null, Buffer.from(payload, 'utf8'), privateKey));
  return {
    id: DEVICE_KEYS.deviceId,
    publicKey: DEVICE_KEYS.publicKeyB64Url,
    signature,
    signedAt,
    nonce,
  };
}

function httpGet(url, timeoutMs = 2000) {
  return new Promise((resolve) => {
    const req = http.get(url, { timeout: timeoutMs }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ ok: res.statusCode === 200, data }));
    });
    req.on('error', () => resolve({ ok: false, data: '' }));
    req.on('timeout', () => { req.destroy(); resolve({ ok: false, data: '' }); });
  });
}

// --- Agents (JSON.parse, 健壮) ---
function getAgents() {
  try {
    const raw = fs.readFileSync(path.join(OPENCLAW_HOME, 'openclaw.json'), 'utf8');
    const config = JSON.parse(raw);
    const list = config?.agents?.list || [];
    return list.map(a => ({
      id: a.id,
      name: a.name || a.id,
      model: a.model?.primary || a.models?.primary || '--',
      deployedSkills: a.deployedSkills || null,
    })).filter(a => a.id);
  } catch (e) {
    console.warn('[RTS] Failed to parse agents:', e.message);
    return [];
  }
}

// --- Skills (跨平台) ---
function getSkillDirs() {
  const dirs = [
    { path: path.join(HOME, '.agents', 'skills'), category: '用户' },
  ];
  // 扫描每个 agent 的 workspace/skills/ 目录
  try {
    const raw = fs.readFileSync(path.join(OPENCLAW_HOME, 'openclaw.json'), 'utf8');
    const config = JSON.parse(raw);
    const agents = config?.agents?.list || [];
    for (const a of agents) {
      if (a.workspace) {
        const agentSkillDir = path.join(a.workspace, 'skills');
        if (fs.existsSync(agentSkillDir)) {
          dirs.push({ path: agentSkillDir, category: a.name || a.id });
        }
      }
    }
  } catch {}
  if (OPENCLAW_DIR) {
    dirs.push({ path: path.join(OPENCLAW_DIR, 'skills'), category: '内置' });
    // 自动扫描所有 extensions/*/skills/
    const extDir = path.join(OPENCLAW_DIR, 'extensions');
    try {
      for (const e of fs.readdirSync(extDir, { withFileTypes: true })) {
        if (e.isDirectory()) {
          const s = path.join(extDir, e.name, 'skills');
          if (fs.existsSync(s)) dirs.push({ path: s, category: '扩展' });
        }
      }
    } catch {}
  }
  return dirs;
}

function getSkills() {
  const skills = [];
  const seen = new Set();
  for (const d of getSkillDirs()) {
    try {
      if (!fs.existsSync(d.path)) continue;
      const entries = fs.readdirSync(d.path, { withFileTypes: true });
      for (const e of entries) {
        if (!e.isDirectory()) continue;
        if (seen.has(e.name)) continue;
        seen.add(e.name);
        skills.push({ id: e.name, name: e.name, category: d.category });
      }
    } catch {}
  }
  return skills;
}

// --- Active agent cache: keep agents visible for at least 5 min after last activity ---
const GRACE_MS = 5 * 60 * 1000; // 5 minutes
const activeCache = {}; // { agentId: { lastSeenActive: timestamp, sessionData: {...} } }

// Load deployedSkills from openclaw.json (JSON.parse)
let agentDeployedSkills = {};
try {
  const openclawRaw = fs.readFileSync(path.join(OPENCLAW_HOME, 'openclaw.json'), 'utf8');
  const config = JSON.parse(openclawRaw);
  const list = config?.agents?.list || [];
  for (const a of list) {
    if (a.id && Array.isArray(a.deployedSkills) && a.deployedSkills.length > 0) {
      agentDeployedSkills[a.id] = a.deployedSkills;
    }
  }
} catch (e) { console.log('Failed to load deployedSkills:', e.message); }

function getSessions() {
  const sessions = [];
  const agentsDir = path.join(OPENCLAW_HOME, 'agents');
  const nowActiveLock = new Set(); // agents with .lock right now
  try {
    if (!fs.existsSync(agentsDir)) return returnWithCache(sessions, nowActiveLock);
    const agentDirs = fs.readdirSync(agentsDir, { withFileTypes: true }).filter(d => d.isDirectory());
    for (const aDir of agentDirs) {
      const sessDir = path.join(agentsDir, aDir.name, 'sessions');
      if (!fs.existsSync(sessDir)) continue;
      const lockFiles = fs.readdirSync(sessDir).filter(f => f.endsWith('.jsonl.lock'));
      
      // 也检查最近修改的 .jsonl 文件（捕获执行太快、lock 已消失的 session）
      const recentJsonl = fs.readdirSync(sessDir)
        .filter(f => f.endsWith('.jsonl') && !f.endsWith('.lock') && f !== 'sessions.json')
        .filter(f => {
          try {
            const stat = fs.statSync(path.join(sessDir, f));
            return (Date.now() - stat.mtimeMs) < 60000; // 最近 1 分钟内有修改
          } catch { return false; }
        });
      
      if (lockFiles.length === 0 && recentJsonl.length === 0) continue;
      nowActiveLock.add(aDir.name);
      
      // 优先用 lock 文件，没有则用最近活跃的 jsonl
      const sessionFiles = lockFiles.length > 0 
        ? lockFiles.map(f => f.replace('.jsonl.lock', ''))
        : recentJsonl.map(f => f.replace('.jsonl', '')).slice(0, 1);
      
      for (const sessionId of sessionFiles) {
        // Try to get details from sessions.json
        const sessFile = path.join(sessDir, 'sessions.json');
        let model = '--', channel = '--', skills = [];
        
        // Use deployedSkills from config if available
        if (agentDeployedSkills[aDir.name]) {
          skills = agentDeployedSkills[aDir.name];
        } else {
          // Fallback to skillsSnapshot.skills
          try {
            const raw = fs.readFileSync(sessFile, 'utf8');
            const idx = raw.indexOf(sessionId);
            if (idx !== -1) {
              const chunk = raw.substring(Math.max(0, idx - 200), Math.min(raw.length, idx + 2000));
              model = (chunk.match(/"model"\s*:\s*"([^"]+)"/) || [])[1] || '--';
              channel = (chunk.match(/"lastChannel"\s*:\s*"([^"]+)"/) || [])[1] || '--';
              const skillsChunk = raw.substring(idx, Math.min(raw.length, idx + 50000));
              const snapshotIdx = skillsChunk.indexOf('"skillsSnapshot"');
              if (snapshotIdx !== -1) {
                const afterSnapshot = skillsChunk.substring(snapshotIdx);
                const skillsArrMatch = afterSnapshot.match(/"skills"\s*:\s*\[/);
                if (skillsArrMatch) {
                  const arrStart = afterSnapshot.indexOf(skillsArrMatch[0]) + skillsArrMatch[0].length;
                  let depth = 1, arrEnd = arrStart;
                  for (let ci = arrStart; ci < afterSnapshot.length && depth > 0; ci++) {
                    if (afterSnapshot[ci] === '[') depth++;
                    if (afterSnapshot[ci] === ']') depth--;
                    if (depth === 0) { arrEnd = ci; break; }
                  }
                  const arrContent = afterSnapshot.substring(arrStart, arrEnd);
                  const nameMatches = arrContent.matchAll(/"name"\s*:\s*"([^"]+)"/g);
                  const seen = new Set();
                  for (const m of nameMatches) {
                    const name = m[1];
                    if (!seen.has(name) && name.length < 40 && !name.includes(':') && !name.endsWith('.md') && !name.includes('_')) {
                      seen.add(name);
                      skills.push(name);
                    }
                  }
                }
              }
            }
          } catch {}
        }
        // Get last activity from jsonl file modification time
        let lastActivity = '';
        try {
          const jsonlPath = path.join(sessDir, sessionId + '.jsonl');
          if (fs.existsSync(jsonlPath)) {
            const stat = fs.statSync(jsonlPath);
            lastActivity = stat.mtime.toISOString();
            // Read tail of file for recent messages (up to full file, stop early)
            const tailContent = fs.readFileSync(jsonlPath, 'utf8');
            const lines = tailContent.trim().split('\n');
            // Extract recent conversation: find last user msg + last assistant msg (up to 4 total)
            let currentTask = '';
            const recentMessages = [];
            let foundUser = false, foundAssistant = false;
            for (let i = lines.length - 1; i >= 0 && recentMessages.length < 4; i--) {
              try {
                const entry = JSON.parse(lines[i]);
                const role = entry.role || (entry.message && entry.message.role);
                const rawContent = entry.content || (entry.message && entry.message.content);
                if ((role === 'user' || role === 'assistant') && rawContent) {
                  let text = '';
                  if (typeof rawContent === 'string') {
                    text = rawContent;
                  } else if (Array.isArray(rawContent)) {
                    for (const part of rawContent) {
                      if (part.type === 'text' && part.text) { text = part.text; break; }
                    }
                  }
                  if (!text || !text.trim()) continue;
                  if (role === 'user') {
                    text = text.replace(/Sender \(untrusted metadata\):[\s\S]*?```[\s\S]*?```\s*/g, '').trim();
                    text = text.replace(/Conversation info \(untrusted metadata\):[\s\S]*?```[\s\S]*?```\s*/g, '').trim();
                    text = text.replace(/^\[.*?\]\s*/g, '').trim();
                    // Skip system-injected messages
                    if (!text || text.startsWith('System:') || text.startsWith('To send') || text.startsWith('Read HEARTBEAT') || text.startsWith('A new session')) continue;
                  }
                  if (!text) continue;
                  // Skip duplicate assistant msgs if we already have 2 and still need user
                  if (role === 'assistant' && foundAssistant && !foundUser && recentMessages.length >= 2) continue;
                  text = text.substring(0, 150);
                  recentMessages.unshift({ role, text });
                  if (role === 'user') { foundUser = true; if (!currentTask) currentTask = text; }
                  if (role === 'assistant') foundAssistant = true;
                  // Stop once we have both roles
                  if (foundUser && foundAssistant && recentMessages.length >= 2) break;
                  if (role === 'user' && !currentTask) currentTask = text;
                }
              } catch {}
            }
            sessions.push({
              id: `agent:${aDir.name}:${sessionId.substring(0,8)}`,
              agent: aDir.name,
              status: 'executing',
              model, channel, skills,
              sessionId, lastActivity,
              currentTask,
              recentMessages
            });
          }
        } catch {
          sessions.push({ id: `agent:${aDir.name}:${sessionId.substring(0,8)}`, agent: aDir.name, status: 'executing', model, channel, skills, sessionId, lastActivity: '', currentTask: '' });
        }
      }
    }
  } catch {}
  
  // 扫描 sessions.json 中的 subagent sessions（它们可能存在父 agent 目录下）
  try {
    const agentDirs2 = fs.readdirSync(path.join(OPENCLAW_HOME, 'agents'), { withFileTypes: true }).filter(d => d.isDirectory());
    for (const aDir of agentDirs2) {
      const sessFile = path.join(OPENCLAW_HOME, 'agents', aDir.name, 'sessions', 'sessions.json');
      if (!fs.existsSync(sessFile)) continue;
      try {
        const sessData = JSON.parse(fs.readFileSync(sessFile, 'utf8'));
        for (const [key, val] of Object.entries(sessData)) {
          if (!key.includes(':subagent:')) continue;
          if (!val.sessionId) continue;
          // 检查这个 session 是否有 lock 文件（活跃中）
          const sessDir = path.join(OPENCLAW_HOME, 'agents', aDir.name, 'sessions');
          const lockPath = path.join(sessDir, val.sessionId + '.jsonl.lock');
          const jsonlPath = path.join(sessDir, val.sessionId + '.jsonl');
          const hasLock = fs.existsSync(lockPath);
          const recentlyModified = fs.existsSync(jsonlPath) && (Date.now() - fs.statSync(jsonlPath).mtimeMs) < 60000;
          if (!hasLock && !recentlyModified) continue;
          // 已经在 sessions 列表中的跳过
          if (sessions.find(s => s.sessionId === val.sessionId)) continue;
          // 从 key 中提取信息，尝试匹配 agent 配置来找目标 agent
          // key 格式: agent:butler:subagent:<uuid>
          const subagentLabel = val.label || val.spawnedAgent || 'subagent';
          // 尝试从 jsonl 读取最近消息
          let lastActivity = '', currentTask = '', recentMessages = [];
          try {
            if (fs.existsSync(jsonlPath)) {
              const stat = fs.statSync(jsonlPath);
              lastActivity = stat.mtime.toISOString();
              const content = fs.readFileSync(jsonlPath, 'utf8');
              const lines = content.trim().split('\n');
              for (let i = lines.length - 1; i >= 0 && recentMessages.length < 4; i--) {
                try {
                  const entry = JSON.parse(lines[i]);
                  const role = entry.role || (entry.message && entry.message.role);
                  const rawContent = entry.content || (entry.message && entry.message.content);
                  if ((role === 'user' || role === 'assistant') && rawContent) {
                    let text = typeof rawContent === 'string' ? rawContent : '';
                    if (Array.isArray(rawContent)) { for (const p of rawContent) { if (p.type === 'text' && p.text) { text = p.text; break; } } }
                    if (!text || !text.trim()) continue;
                    if (role === 'user') {
                      text = text.replace(/Sender \(untrusted metadata\):[\s\S]*?```[\s\S]*?```\s*/g, '').trim();
                      text = text.replace(/^\[.*?\]\s*/g, '').trim();
                      if (!text || text.startsWith('System:') || text.startsWith('Read HEARTBEAT')) continue;
                    }
                    text = text.substring(0, 150);
                    recentMessages.unshift({ role, text });
                    if (role === 'user' && !currentTask) currentTask = text;
                  }
                } catch {}
              }
            }
          } catch {}
          sessions.push({
            id: `subagent:${aDir.name}:${val.sessionId.substring(0,8)}`,
            agent: subagentLabel,
            parentAgent: aDir.name,
            status: hasLock ? 'executing' : 'executing',
            model: val.model ? (val.modelProvider ? val.modelProvider + '/' + val.model : val.model) : '--',
            channel: val.lastChannel || '--',
            skills: [],
            sessionId: val.sessionId,
            lastActivity,
            currentTask,
            recentMessages,
            isSubagent: true
          });
        }
      } catch {}
    }
  } catch {}
  
  return returnWithCache(sessions, nowActiveLock);
}

// Merge live sessions with cached ones (grace period)
function returnWithCache(liveSessions, nowActiveLock) {
  const now = Date.now();
  // Update cache for currently active agents
  for (const s of liveSessions) {
    activeCache[s.agent] = { lastSeenActive: now, sessionData: s };
  }
  // Build result: live sessions + cached sessions still within grace period
  const result = [...liveSessions];
  const liveAgents = new Set(liveSessions.map(s => s.agent));
  for (const [agentId, cached] of Object.entries(activeCache)) {
    if (liveAgents.has(agentId)) continue; // already in live
    const elapsed = now - cached.lastSeenActive;
    if (elapsed < GRACE_MS) {
      // Still within grace period - show as "cooling down"
      const remaining = Math.ceil((GRACE_MS - elapsed) / 1000);
      result.push({
        ...cached.sessionData,
        status: 'cooldown',
        cooldownSeconds: remaining
      });
    } else {
      // Grace period expired, remove from cache
      delete activeCache[agentId];
    }
  }
  return result;
}

// --- Gateway ---
async function getGatewayStatus() {
  const res = await httpGet(`${GATEWAY_URL}/`);
  // Gateway is online if it responds at all (even 503 when Control UI is missing)
  return { online: res.ok || res.data.length > 0, port: GATEWAY_PORT };
}

// --- Vitals (real-time CPU via delta sampling) ---
let prevCpuTimes = null;
let cachedCpuPercent = 0;

function sampleCpuTimes() {
  const cpus = os.cpus();
  let idle = 0, total = 0;
  for (const cpu of cpus) {
    for (const t in cpu.times) total += cpu.times[t];
    idle += cpu.times.idle;
  }
  return { idle, total };
}

// 每 2 秒采样一次，计算真实 CPU 使用率
setInterval(() => {
  const cur = sampleCpuTimes();
  if (prevCpuTimes) {
    const dIdle = cur.idle - prevCpuTimes.idle;
    const dTotal = cur.total - prevCpuTimes.total;
    cachedCpuPercent = dTotal > 0 ? Math.round((1 - dIdle / dTotal) * 100) : 0;
  }
  prevCpuTimes = cur;
}, 2000);
// 初始化第一次采样
prevCpuTimes = sampleCpuTimes();

function getSystemVitals() {
  const cpus = os.cpus();
  const totalMem = os.totalmem(), freeMem = os.freemem(), usedMem = totalMem - freeMem;
  return {
    cpuPercent: cachedCpuPercent,
    memUsed: Math.round(usedMem / 1024 / 1024), memTotal: Math.round(totalMem / 1024 / 1024),
    memPercent: Math.round(usedMem / totalMem * 100),
    uptime: os.uptime(), hostname: os.hostname(), platform: os.platform(), cpuCount: cpus.length,
    cpuModel: cpus[0]?.model || 'unknown'
  };
}

// --- Cron ---
async function getCronJobs() {
  const cronPath = path.join(OPENCLAW_HOME, 'cron', 'jobs.json');
  try {
    if (!fs.existsSync(cronPath)) return [];
    const raw = fs.readFileSync(cronPath, 'utf8');
    const data = JSON.parse(raw);
    const jobs = Array.isArray(data) ? data : (data.jobs || []);
    return jobs.map(j => ({
      id: j.id || j.jobId, name: j.name || 'unnamed',
      schedule: j.schedule?.expr || j.schedule?.kind || '--', enabled: j.enabled !== false
    }));
  } catch { return []; }
}

// --- All sessions with active grace period ---
const sessionActiveCache = {}; // { sessionId: lastSeenActiveMs }

function getAllSessionsList() {
  const allSessions = [];
  const agentsDir = path.join(OPENCLAW_HOME, 'agents');
  const now = Date.now();
  try {
    if (!fs.existsSync(agentsDir)) return allSessions;
    const agentDirs = fs.readdirSync(agentsDir, { withFileTypes: true }).filter(d => d.isDirectory());
    for (const aDir of agentDirs) {
      const sessDir = path.join(agentsDir, aDir.name, 'sessions');
      if (!fs.existsSync(sessDir)) continue;
      const lockFiles = new Set(fs.readdirSync(sessDir).filter(f => f.endsWith('.jsonl.lock')).map(f => f.replace('.jsonl.lock', '')));
      const jsonls = fs.readdirSync(sessDir).filter(f => f.endsWith('.jsonl') && !f.includes('.lock') && !f.includes('.reset') && f !== 'sessions.json');
      for (const f of jsonls) {
        try {
          const fullPath = path.join(sessDir, f);
          const stat = fs.statSync(fullPath);
          const sessionId = f.replace('.jsonl', '');
          const isLocked = lockFiles.has(sessionId);
          const minutesAgo = Math.round((now - stat.mtimeMs) / 60000);
          
          // 更新活跃缓存
          if (isLocked) {
            sessionActiveCache[sessionId] = now;
          }
          
          // 判断是否活跃（有 lock 或在 5 分钟冷却期内）
          const cachedTime = sessionActiveCache[sessionId] || 0;
          const isActive = isLocked || (now - cachedTime) < GRACE_MS;
          const cooldownSeconds = (!isLocked && cachedTime > 0 && (now - cachedTime) < GRACE_MS)
            ? Math.ceil((GRACE_MS - (now - cachedTime)) / 1000) : 0;
          
          // 清理过期缓存
          if (!isActive && sessionActiveCache[sessionId]) {
            delete sessionActiveCache[sessionId];
          }
          
          let channel = '--';
          try {
            const sessFile = path.join(sessDir, 'sessions.json');
            if (fs.existsSync(sessFile)) {
              const raw = fs.readFileSync(sessFile, 'utf8');
              const idx = raw.indexOf(sessionId);
              if (idx !== -1) {
                const chunk = raw.substring(idx, Math.min(raw.length, idx + 500));
                channel = (chunk.match(/"lastChannel"\s*:\s*"([^"]+)"/) || [])[1] || '--';
              }
            }
          } catch {}
          allSessions.push({
            id: sessionId.substring(0, 8),
            agent: aDir.name,
            active: isActive,
            locked: isLocked,
            cooldownSeconds,
            channel,
            lastActive: stat.mtime.toISOString(),
            minutesAgo,
            sizeKB: Math.round(stat.size / 1024)
          });
        } catch {}
      }
    }
  } catch {}
  const thirtyDaysMs = 30 * 24 * 60 * 60 * 1000;
  return allSessions
    .filter(s => s.minutesAgo < 30 * 24 * 60)
    .sort((a, b) => a.minutesAgo - b.minutesAgo);
}

// --- Collect ---
async function collectAllData() {
  const [gateway, cronJobs] = await Promise.all([getGatewayStatus(), getCronJobs()]);
  return {
    timestamp: Date.now(), gateway, vitals: getSystemVitals(),
    sessions: getSessions(), cronJobs, agents: getAgents(), skills: getSkills(),
    allSessions: getAllSessionsList()
  };
}

// --- HTTP ---
const server = http.createServer(async (req, res) => {
  if (req.url === '/api/state') {
    try {
      const data = await collectAllData();
      res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
      res.end(JSON.stringify(data));
    } catch (e) { res.writeHead(500); res.end(JSON.stringify({ error: e.message })); }
    return;
  }
  
  // Session history API
  if (req.url.startsWith('/api/session-history?')) {
    const params = new URL(req.url, 'http://localhost').searchParams;
    const agent = params.get('agent');
    const sessionId = params.get('sessionId');
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*' });
    if (!agent || !sessionId) {
      res.end(JSON.stringify({ error: 'Missing agent or sessionId' }));
      return;
    }
    try {
      const jsonlPath = path.join(OPENCLAW_HOME, 'agents', agent, 'sessions', sessionId + '.jsonl');
      if (!fs.existsSync(jsonlPath)) {
        res.end(JSON.stringify({ messages: [], error: 'Session file not found' }));
        return;
      }
      const content = fs.readFileSync(jsonlPath, 'utf8');
      const lines = content.trim().split('\n');
      const messages = [];
      for (const line of lines) {
        try {
          const entry = JSON.parse(line);
          const role = entry.role || (entry.message && entry.message.role);
          const rawContent = entry.content || (entry.message && entry.message.content);
          if ((role === 'user' || role === 'assistant') && rawContent) {
            let text = '';
            if (typeof rawContent === 'string') {
              text = rawContent;
            } else if (Array.isArray(rawContent)) {
              for (const part of rawContent) {
                if (part.type === 'text' && part.text) { text += part.text + '\n'; }
              }
            }
            if (!text || !text.trim()) continue;
            if (role === 'user') {
              text = text.replace(/Sender \(untrusted metadata\):[\s\S]*?```[\s\S]*?```\s*/g, '').trim();
              text = text.replace(/Conversation info \(untrusted metadata\):[\s\S]*?```[\s\S]*?```\s*/g, '').trim();
              text = text.replace(/^\[.*?\]\s*/g, '').trim();
              if (!text || text.startsWith('System:') || text.startsWith('To send') || text.startsWith('Read HEARTBEAT') || text.startsWith('A new session')) continue;
            }
            if (!text.trim()) continue;
            messages.push({ role, text: text.trim() });
          }
        } catch {}
      }
      res.end(JSON.stringify({ messages }));
    } catch (e) {
      res.end(JSON.stringify({ messages: [], error: e.message }));
    }
    return;
  }

  // 网关控制 API
  if (req.url === '/api/gateway/restart' && req.method === 'POST') {
    res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
    try {
      const { execSync } = require('child_process');
      execSync('openclaw gateway restart', { timeout: 15000, stdio: 'pipe' });
      res.end(JSON.stringify({ ok: true, action: 'restart', message: '网关重启成功' }));
    } catch (e) {
      res.end(JSON.stringify({ ok: false, action: 'restart', message: e.message }));
    }
    return;
  }
  
  if (req.url === '/api/gateway/stop' && req.method === 'POST') {
    res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
    try {
      const { execSync } = require('child_process');
      execSync('openclaw gateway stop', { timeout: 15000, stdio: 'pipe' });
      res.end(JSON.stringify({ ok: true, action: 'stop', message: '网关已关闭' }));
    } catch (e) {
      res.end(JSON.stringify({ ok: false, action: 'stop', message: e.message }));
    }
    return;
  }
  
  // 聊天消息 API - 通过 Gateway WebSocket chat.send 发送
  if (req.url === '/api/chat' && req.method === 'POST') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
      try {
        const { agent, sessionId, message } = JSON.parse(body);
        if (!agent || !message) {
          res.end(JSON.stringify({ ok: false, error: '缺少 agent 或 message' }));
          return;
        }
        const WsClient = require('ws');
        const gwWs = new WsClient(`ws://127.0.0.1:${GATEWAY_PORT}/webchat/ws`, { origin: 'http://127.0.0.1:4320' });
        let responded = false;
        const timeout = setTimeout(() => {
          if (!responded) { responded = true; gwWs.close(); res.end(JSON.stringify({ ok: false, error: 'timeout' })); }
        }, 15000);
        
        let phase = 'connecting'; // connecting -> challenge -> connected -> sending
        gwWs.on('open', () => { phase = 'waiting-challenge'; });
        
        gwWs.on('message', (data) => {
          try {
            const msg = JSON.parse(data.toString());
            
            // Gateway sends connect.challenge event first
            if (msg.type === 'event' && msg.event === 'connect.challenge') {
              phase = 'sending-connect';
              const nonce = msg.payload?.nonce || '';
              const connectId = 'c-' + Date.now();
              const connectParams = {
                minProtocol: 3, maxProtocol: 3,
                client: { id: 'openclaw-control-ui', version: '1.0', platform: os.platform(), mode: 'webchat' },
                role: 'operator', scopes: ['operator.admin','operator.read','operator.write'],
                caps: []
              };
              // Token 认证
              const token = getGatewayToken();
              if (token) connectParams.auth = { token };
              // Ed25519 设备签名
              connectParams.device = signConnectChallenge(nonce, connectParams);
              gwWs.send(JSON.stringify({
                type: 'req', id: connectId, method: 'connect',
                params: connectParams
              }));
              return;
            }
            
            // Connect response
            if (msg.type === 'res' && phase === 'sending-connect') {
              if (msg.ok === false) {
                if (!responded) {
                  responded = true; clearTimeout(timeout); gwWs.close();
                  res.end(JSON.stringify({ ok: false, error: msg.error?.message || 'connect failed' }));
                }
                return;
              }
              phase = 'connected';
              // Now send chat message
              const sessionKey = sessionId ? `agent:${agent}:${sessionId}` : `agent:${agent}:main`;
              const chatId = 'm-' + Date.now();
              const idempotencyKey = 'rts-' + Date.now() + '-' + Math.random().toString(36).substring(2, 8);
              gwWs.send(JSON.stringify({
                type: 'req', id: chatId, method: 'chat.send',
                params: { sessionKey, message, idempotencyKey }
              }));
              return;
            }
            
            // Chat send response
            if (msg.type === 'res' && phase === 'connected' && !responded) {
              responded = true; clearTimeout(timeout); gwWs.close();
              if (msg.ok !== false) {
                res.end(JSON.stringify({ ok: true, method: 'chat.send', payload: msg.payload }));
              } else {
                res.end(JSON.stringify({ ok: false, error: msg.error?.message || 'chat.send failed' }));
              }
            }
          } catch {}
        });
        
        gwWs.on('error', (err) => {
          if (!responded) { responded = true; clearTimeout(timeout); res.end(JSON.stringify({ ok: false, error: 'WS error: ' + err.message })); }
        });
      } catch (e) { res.end(JSON.stringify({ ok: false, error: e.message })); }
    });
    return;
  }
  
  // CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET,POST,OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' });
    res.end();
    return;
  }
  let urlPath = req.url.split('?')[0]; // 去掉查询参数
  let filePath = urlPath === '/' ? '/index.html' : urlPath;
  filePath = path.join(__dirname, 'public', filePath);
  const ext = path.extname(filePath);
  const mime = { '.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'application/javascript; charset=utf-8','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.gif':'image/gif','.svg':'image/svg+xml' };
  try { const c = fs.readFileSync(filePath); res.writeHead(200,{'Content-Type':mime[ext]||'application/octet-stream','Cache-Control':'no-cache, no-store, must-revalidate','Expires':'0'}); res.end(c); }
  catch(e) { console.log('Static err:',e.message,filePath); res.writeHead(404); res.end('Not found'); }
});

const wss = new WebSocket.Server({ server });
async function broadcast() { try { const d = JSON.stringify(await collectAllData()); wss.clients.forEach(c => { if (c.readyState === WebSocket.OPEN) c.send(d); }); } catch {} }
setInterval(broadcast, 3000);
wss.on('connection', async ws => { try { ws.send(JSON.stringify(await collectAllData())); } catch {} });
server.listen(PORT, '127.0.0.1', () => console.log(`[RTS-Dashboard] ⚡ Online at http://127.0.0.1:${PORT}`));
