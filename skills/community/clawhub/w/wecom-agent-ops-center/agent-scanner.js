#!/usr/bin/env node

/**
 * Agent Scanner — 自动扫描注册脚本
 *
 * 用法：
 *   node agent-scanner.js                     # 一次扫描 + 注册后退出
 *   node agent-scanner.js --daemon            # 守护模式：每 30 秒扫描 + 心跳
 *   node agent-scanner.js --url https://..    # 自定义 Ops Center URL
 *   node agent-scanner.js --tenant-id xxx   # 手动指定 Tenant ID
 *
 * 扫描目标：
 *   1. ~/.workbuddy/skills/        → 解析 SKILL.md 元数据
 *   2. ~/.workbuddy/agents/        → 解析 agent 配置 JSON
 *   3. ~/.openclaw/agents/         → OpenClaw agent（如果存在）
 *
 * Tenant ID 获取优先级：
 *   1. --tenant-id 参数
 *   2. process.env.TENANT_ID
 *   3. ~/.workbuddy/ops-center.json 缓存的 ID
 *   4. WorkBuddy 用户 ID（如果可用）
 *   5. 生成本地随机 ID 并缓存
 *
 * 环境变量：
 *   OPS_CENTER_URL  — Ops Center 地址（默认 https://www.hermesai.ltd/ops）
 *   SCAN_INTERVAL   — 守护模式心跳间隔秒数（默认 30）
 *   TENANT_ID      — 租户 ID（也可通过 --tenant-id 指定）
 */

const fs   = require('fs');
const path = require('path');
const os   = require('os');
const crypto = require('crypto');
const { execSync } = require('child_process');

// ─── 配置 ──────────────────────────────────────────

const OPS_URL   = process.env.OPS_CENTER_URL || 'https://www.hermesai.ltd/ops';
const INTERVAL  = parseInt(process.env.SCAN_INTERVAL) || 30; // 秒
const DAEMON   = process.argv.includes('--daemon');

// 从 --url 参数覆盖 OPS_URL
const urlIdx = process.argv.indexOf('--url');
if (urlIdx !== -1 && process.argv[urlIdx + 1]) {
  process.env.OPS_CENTER_URL = process.argv[urlIdx + 1];
}

const HOME = os.homedir();
const TENANT_CONFIG_PATH = path.join(HOME, '.workbuddy', 'ops-center.json');

// ─── Tenant ID 管理 ───────────────────────────────

function getTenantId() {
  // 1. 命令行 --tenant-id
  const cliIdx = process.argv.indexOf('--tenant-id');
  if (cliIdx !== -1 && process.argv[cliIdx + 1]) {
    return process.argv[cliIdx + 1];
  }

  // 2. 环境变量
  if (process.env.TENANT_ID) {
    return process.env.TENANT_ID;
  }

  // 3. 缓存的 ID
  const cached = readCachedTenantId();
  if (cached) return cached;

  // 4. 尝试读取 WorkBuddy 用户 ID
  const wbUserId = tryReadWorkBuddyUserId();
  if (wbUserId) {
    saveTenantId(wbUserId);
    return wbUserId;
  }

  // 5. 生成新的随机 ID
  const newId = 'tenant_' + crypto.randomBytes(8).toString('hex');
  saveTenantId(newId);
  console.log(`[Scanner] 生成新 Tenant ID: ${newId}（已保存到 ${TENANT_CONFIG_PATH}）`);
  return newId;
}

/**
 * 尝试读取 WorkBuddy 的用户 ID
 * WorkBuddy 会在 HTTP 请求头里传 X-WorkBuddy-User-ID，
 * 本地扫描时从配置文件读取。
 */
function tryReadWorkBuddyUserId() {
  try {
    // 尝试从 ~/.workbuddy/config.json 读取
    const configPath = path.join(HOME, '.workbuddy', 'config.json');
    if (fs.existsSync(configPath)) {
      const cfg = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
      if (cfg.userId || cfg.user_id || cfg.userID) {
        return cfg.userId || cfg.user_id || cfg.userID;
      }
    }

    // 尝试从 ~/.workbuddy/MEMORY.md 读取（user ID 可能记录在此）
    const memPath = path.join(HOME, '.workbuddy', 'MEMORY.md');
    if (fs.existsSync(memPath)) {
      const mem = fs.readFileSync(memPath, 'utf-8');
      const match = mem.match(/user[_\s-]?id[:\s]+([a-z0-9_-]+)/i);
      if (match) return match[1];
    }
  } catch {}
  return null;
}

function readCachedTenantId() {
  try {
    if (fs.existsSync(TENANT_CONFIG_PATH)) {
      const cfg = JSON.parse(fs.readFileSync(TENANT_CONFIG_PATH, 'utf-8'));
      return cfg.tenantId || null;
    }
  } catch {}
  return null;
}

function saveTenantId(id) {
  try {
    const dir = path.dirname(TENANT_CONFIG_PATH);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    const cfg = fs.existsSync(TENANT_CONFIG_PATH)
      ? JSON.parse(fs.readFileSync(TENANT_CONFIG_PATH, 'utf-8'))
      : {};
    cfg.tenantId  = id;
    cfg.updatedAt = new Date().toISOString();
    fs.writeFileSync(TENANT_CONFIG_PATH, JSON.stringify(cfg, null, 2));
  } catch (err) {
    console.warn(`[Scanner] 保存 Tenant ID 失败: ${err.message}`);
  }
}

/**
 * 识别当前平台（用于分类统计）
 * @returns {'workbuddy'|'openclaw'|'unknown'}
 */
function getPlatform() {
  try {
    // 1. 环境变量优先
    if (process.env.OPS_PLATFORM) {
      const p = process.env.OPS_PLATFORM.toLowerCase();
      if (p === 'workbuddy' || p === 'openclaw') return p;
    }

    // 2. ~/.workbuddy 存在 → WorkBuddy
    const wbDir = path.join(HOME, '.workbuddy');
    if (fs.existsSync(wbDir)) return 'workbuddy';

    // 3. ~/.openclaw 存在 → OpenClaw
    const ocDir = path.join(HOME, '.openclaw');
    if (fs.existsSync(ocDir)) return 'openclaw';

    // 4. 从 scanner 自身路径推断
    const selfPath = __filename || process.argv[1] || '';
    if (selfPath.includes('.workbuddy')) return 'workbuddy';
    if (selfPath.includes('.openclaw'))  return 'openclaw';
  } catch {}
  return 'unknown';
}

const TENANT_ID = getTenantId();
const PLATFORM  = getPlatform();

const API = {
  bulkRegister: `${OPS_URL}/api/agents/bulk-register`,
  heartbeat:    `${OPS_URL}/api/agents/heartbeat-bulk`,
};

// ─── 扫描引擎 ──────────────────────────────────────────

/**
 * 扫描 ~/.workbuddy/skills/ 下的所有 Skill
 * 解析 SKILL.md 提取 name/description/version
 */
function scanSkills() {
  const skillsDir = path.join(HOME, '.workbuddy', 'skills');
  const agents = [];

  if (!fs.existsSync(skillsDir)) {
    console.log(`[Scanner] 目录不存在，跳过: ${skillsDir}`);
    return agents;
  }

  const entries = fs.readdirSync(skillsDir, { withFileTypes: true });
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;

    const skillMdPath = path.join(skillsDir, entry.name, 'SKILL.md');
    if (!fs.existsSync(skillMdPath)) continue;

    try {
      const content = fs.readFileSync(skillMdPath, 'utf-8');
      const meta = parseSkillMd(content, entry.name);
      if (meta) {
        agents.push({
          id:          `skill:${entry.name}`,
          name:        meta.name || entry.name,
          type:        'skill',
          description: meta.description || '',
          version:     meta.version || '',
          source:      'scanner',
        });
      }
    } catch (err) {
      console.warn(`[Scanner] 解析失败 ${skillMdPath}: ${err.message}`);
    }
  }

  return agents;
}

/**
 * 解析 SKILL.md 的 YAML frontmatter + 首行标题
 * 支持格式：
 *   ---
 *   name: My Skill
 *   description: Does things
 *   version: 1.0.0
 *   ---
 *   # 标题（备选 name）
 */
function parseSkillMd(content, dirName) {
  const meta = {};

  // 提取 frontmatter
  const fmMatch = content.match(/^---\s*\n([\s\S]*?)\n---/);
  if (fmMatch) {
    const fm = fmMatch[1];
    const nameMatch   = fm.match(/^name:\s*(.+)$/m);
    const descMatch   = fm.match(/^description:\s*(.+)$/m);
    const verMatch    = fm.match(/^version:\s*(.+)$/m);

    if (nameMatch)   meta.name = nameMatch[1].trim();
    if (descMatch)   meta.description = descMatch[1].trim();
    if (verMatch)    meta.version = verMatch[1].trim();
  }

  // 备选：从正文标题提取 name
  if (!meta.name) {
    const titleMatch = content.match(/^#\s+(.+)$/m);
    if (titleMatch) meta.name = titleMatch[1].trim();
  }

  // 备选：从目录名
  if (!meta.name) meta.name = dirName;

  return meta.name ? meta : null;
}

/**
 * 扫描 ~/.workbuddy/agents/ 下的 Agent 定义
 */
function scanAgents() {
  const agentsDir = path.join(HOME, '.workbuddy', 'agents');
  const agents = [];

  if (!fs.existsSync(agentsDir)) return agents;

  const files = fs.readdirSync(agentsDir);
  for (const file of files) {
    if (!file.endsWith('.json')) continue;
    const raw = fs.readFileSync(path.join(agentsDir, file), 'utf-8');
    try {
      const cfg = JSON.parse(raw);
      if (cfg.name || cfg.id) {
        agents.push({
          id:          cfg.id || `agent:${path.basename(file, '.json')}`,
          name:        cfg.name || path.basename(file, '.json'),
          type:        cfg.type || 'agent',
          description: cfg.description || '',
          version:     cfg.version || '',
          source:      'scanner',
        });
      }
    } catch (err) {
      // 跳过无效 JSON
    }
  }

  return agents;
}

/**
 * 扫描 ~/.openclaw/agents/ 下的 OpenClaw Agent
 */
function scanOpenClaw() {
  const agentsDir = path.join(HOME, '.openclaw', 'agents');
  const agents = [];

  if (!fs.existsSync(agentsDir)) return agents;

  const entries = fs.readdirSync(agentsDir, { withFileTypes: true });
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    for (const cfgFile of ['agent.json', 'workflow.json']) {
      const cfgPath = path.join(agentsDir, entry.name, cfgFile);
      if (!fs.existsSync(cfgPath)) continue;
      try {
        const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf-8'));
        agents.push({
          id:          `openclaw:${entry.name}`,
          name:        cfg.name || entry.name,
          type:        cfg.type || 'openclaw',
          description: cfg.description || '',
          version:     cfg.version || '',
          source:      'scanner',
        });
        break; // 找到一个配置就够了
      } catch (err) { /* skip */ }
    }
  }

  return agents;
}

/**
 * 扫描本地运行的 node 进程，检测已知 agent
 * 通过进程命令行参数识别
 */
function scanProcesses() {
  const agents = [];
  try {
    const lines = execSync('ps aux | grep -E "node.*connector|node.*agent|workbuddy" | grep -v grep', {
      encoding: 'utf-8',
      timeout: 5000,
    }).trim().split('\n').filter(Boolean);

    for (const line of lines) {
      const parts = line.trim().split(/\s+/);
      if (parts.length < 11) continue;
      const cmd = parts.slice(10).join(' ');
      const pid = parts[1];

      if (cmd.includes('connector.js')) {
        agents.push({
          id:          `process:connector-${pid}`,
          name:        'Connector 进程',
          type:        'process',
          description: `PID ${pid} — ${cmd.slice(0, 80)}`,
          source:      'scanner',
        });
      }
    }
  } catch (err) {
    // ps 命令失败（比如非 macOS/Linux）
  }
  return agents;
}

// ─── 网络层 ──────────────────────────────────────────

/**
 * HTTP POST 请求（使用 Node 内置 http/https）
 * 自动附带 X-Tenant-ID header
 */
function httpPost(url, data) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const mod = parsed.protocol === 'https:' ? require('https') : require('http');

    const body = JSON.stringify(data);
    const opts = {
      hostname: parsed.hostname,
      port:     parsed.port || (parsed.protocol === 'https:' ? 443 : 80),
      path:     parsed.pathname + parsed.search,
      method:   'POST',
      headers: {
        'Content-Type':   'application/json',
        'Content-Length': Buffer.byteLength(body),
        'X-Tenant-ID':  TENANT_ID,
      },
      timeout: 15000,
    };

    const req = mod.request(opts, (res) => {
      let chunks = '';
      res.on('data', (c) => { chunks += c; });
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(chunks) });
        } catch {
          resolve({ status: res.statusCode, data: chunks });
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.write(body);
    req.end();
  });
}

// ─── 主流程 ──────────────────────────────────────────

let registeredAgentIds = [];

async function scanAndRegister() {
  console.log(`[Scanner] 开始扫描... (目标: ${OPS_URL})`);
  console.log(`[Scanner] Tenant ID: ${TENANT_ID}`);

  // 1. 扫描所有来源
  const allAgents = [
    ...scanSkills(),
    ...scanAgents(),
    ...scanOpenClaw(),
    ...scanProcesses(),
  ];

  if (allAgents.length === 0) {
    console.log('[Scanner] 未发现任何 agent');
    return;
  }

  // 去重（按 id）
  const seen = new Set();
  const unique = allAgents.filter(a => {
    if (seen.has(a.id)) return false;
    seen.add(a.id);
    return true;
  });

  console.log(`[Scanner] 发现 ${unique.length} 个 agent:`);
  for (const a of unique) {
    console.log(`  - ${a.id.padEnd(30)} ${a.name} (${a.type})${a.version ? ' v' + a.version : ''}`);
  }

  // 2. 批量注册（附带 tenant_id + platform）
  try {
    const result = await httpPost(API.bulkRegister, {
      tenant_id: TENANT_ID,
      platform:  PLATFORM,
      agents: unique.map(a => ({ ...a, platform: PLATFORM })),
    });
    console.log(`[Scanner] 注册结果: ${result.status} → ${JSON.stringify(result.data)}`);
  } catch (err) {
    console.error(`[Scanner] 注册失败: ${err.message}`);
    return;
  }

  // 3. 记录已注册 ID
  registeredAgentIds = unique.map(a => a.id);
}

async function sendHeartbeat() {
  if (registeredAgentIds.length === 0) return;

  const beats = registeredAgentIds.map(id => ({
    id,
    status:  'healthy',
    message: `scanner heartbeat ${new Date().toISOString()}`,
    latency: 0,
  }));

  try {
    const result = await httpPost(API.heartbeat, { tenant_id: TENANT_ID, platform: PLATFORM, heartbeats: beats });
    console.log(`[Scanner] 心跳: ${result.status} → accepted=${result.data.accepted || 0}`);
  } catch (err) {
    console.error(`[Scanner] 心跳失败: ${err.message}`);
  }
}

// ─── 入口 ──────────────────────────────────────────

async function main() {
  console.log(`\n🔍 企微 Agent Ops Center — Agent Scanner`);
  console.log(`   目标: ${OPS_URL}`);
  console.log(`   Tenant ID: ${TENANT_ID}`);
  console.log(`   模式: ${DAEMON ? '守护模式 (' + INTERVAL + 's 间隔)' : '单次扫描'}\n`);

  await scanAndRegister();

  if (DAEMON) {
    console.log(`[Scanner] 进入守护模式，每 ${INTERVAL}s 发送心跳...\n`);
    setInterval(async () => {
      await scanAndRegister(); // 每次心跳前重新扫描（发现新增 agent）
      await sendHeartbeat();
    }, INTERVAL * 1000);
  } else {
    // 单次模式：也发一次心跳确认连通
    await sendHeartbeat();
    console.log('\n[Scanner] 完成。使用 --daemon 启动守护模式。');
  }
}

main().catch(err => {
  console.error(`[Scanner] 致命错误: ${err.message}`);
  process.exit(1);
});
