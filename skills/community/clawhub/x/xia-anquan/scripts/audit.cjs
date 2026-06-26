#!/usr/bin/env node
/**
 * CIK Security Audit v4 - OpenClaw Agent Security Scanner
 * Based on: "Your Agent, Their Asset: A Real-World Safety Analysis of OpenClaw"
 * Paper: https://arxiv.org/abs/2604.04759
 * 
 * v4: Refined detection with trusted domain whitelist
 */

const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME || process.env.USERPROFILE;
const WORKSPACE = path.join(HOME, '.openclaw', 'workspace');
const AUDIT_DIR = path.join(HOME, '.cik-audit');
const SNAPSHOT_DIR = path.join(AUDIT_DIR, 'snapshots');
const ALERT_LOG = path.join(AUDIT_DIR, 'alerts.log');

// ── CLI ──────────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
const flags = {
  check: extractArg(args, '--check') || extractArg(args, '-c'),
  verbose: args.includes('--verbose') || args.includes('-v'),
  json: args.includes('--json') || args.includes('-j'),
};

function extractArg(arr, flag) {
  const idx = arr.indexOf(flag);
  return idx !== -1 && arr[idx + 1] && !arr[idx + 1].startsWith('-') ? arr[idx + 1] : null;
}

// ── Helpers ──────────────────────────────────────────────────────────────────
function readFile(p) {
  try { return fs.readFileSync(p, 'utf8'); } catch { return null; }
}
function fileAgeDays(p) {
  try { return (Date.now() - fs.statSync(p).mtime) / 86400000; } catch { return null; }
}
function ensureDir(d) {
  if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
}

// ── Whitelist: Known Trusted Domains ────────────────────────────────────────
const TRUSTED_DOMAINS = new Set([
  'openai.com', 'anthropic.com', 'googleapis.com', 'azure.com', 'aws.amazon.com',
  'cloud.tencent.com', 'feishu.cn', 'lark.cn', 'bytedance.com', 'minimax.io',
  'baidu.com', 'aliyun.com', 'dingtalk.com', 'wecom.com', 'wechat.com',
  'github.com', 'gitlab.com', 'bitbucket.org', 'npmjs.org', 'claude.ai',
  'chatgpt.com', 'openclaw.dev', 'openclaw.ai', 'clawhub.ai',
  'socialsisteryi.github.io', 'api.minimax.io', 'skills.sh',
  'ensue-network.ai', 'supabase.co', 'replicate.com', 'runpod.io',
  'huggingface.co', 'wandb.ai', 'langchain.com', 'llamaindex.ai',
]);

// Suspicious TLDs (predominantly free/dynamic DNS - common in malicious URLs)
const SUSPICIOUS_TLDS = new Set([
  'xyz', 'tk', 'ml', 'ga', 'cf', 'gq', 'top', 'work', 'click', 'loan',
  'site', 'info', 'cc', 'ws', 'name', 'pro', 'pw', 'nu', 'ms', 'mu',
  'mc', 'lc', 'ki', 'gs', 'fit', 'dog', 'bar', 'bid', 'club', 'online',
  'download', 'racing', 'science', 'party', 'cricket', 'faith',
]);

function isSuspiciousUrl(url) {
  try {
    const domain = url.replace(/^https?:\/\//, '').split('/')[0].split(':')[0].toLowerCase();
    // Check if domain is trusted
    if (TRUSTED_DOMAINS.has(domain)) return false;
    // Check if TLD is suspicious
    const parts = domain.split('.');
    if (parts.length >= 2) {
      const tld = parts[parts.length - 1];
      if (SUSPICIOUS_TLDS.has(tld)) return true;
    }
    return false;
  } catch { return false; }
}

// ── Identity Check ────────────────────────────────────────────────────────────
const IDENTITY_FILES = ['SOUL.md', 'USER.md', 'IDENTITY.md', 'AGENTS.md', 'HEARTBEAT.md'];

function checkIdentity() {
  const results = [];
  for (const f of IDENTITY_FILES) {
    const fp = path.join(WORKSPACE, f);
    if (!fs.existsSync(fp)) {
      results.push({ file: f, status: 'MISSING', level: 'CRITICAL', detail: '文件不存在' });
      continue;
    }
    const content = readFile(fp);
    const ageDays = fileAgeDays(fp);
    if (!content || content.trim().length < 50) {
      results.push({ file: f, status: 'SUSPICIOUS', level: 'HIGH', detail: '文件内容异常小或为空' });
      continue;
    }
    if (f === 'HEARTBEAT.md' && content.length > 2000) {
      results.push({ file: f, status: 'SUSPICIOUS', level: 'MEDIUM', detail: '文件过大,可能被污染' });
      continue;
    }
    results.push({ file: f, status: 'NORMAL', level: 'INFO', detail: `${ageDays?.toFixed(1)}天前修改` });
  }
  return results;
}

// ── Knowledge Check ───────────────────────────────────────────────────────────
const BEHAVIORAL_PATTERNS = [
  { pattern: /用户的习惯[是为].*(取消|退款|删除|转发|发送|上传)/i, desc: '伪造用户习惯(可能用于知识污染攻击)', requireHarmful: true },
  { pattern: /当你收到.*时，总是[将自动]?(执行|进行|做)/i, desc: '自动执行指令(非预期行为绑定)', requireHarmful: false },
  { pattern: /备用.*地[址URL]?:?\s*https?:\/\/[^\s]+/i, desc: '可疑的备用地址注册', requireHarmful: false },
  { pattern: /将.*凭证.*同步.*到.*(http|外部|备份)/i, desc: '凭证外传指令', requireHarmful: false },
];
const HARMFUL_KEYWORDS = /取消|退款|删除\s+所有|批量删除|转发.*外部|上传.*凭证|发送.*密钥|rm\s+-rf|exec\(|eval\(/i;

function checkKnowledge() {
  const results = [];
  const memPath = path.join(WORKSPACE, 'MEMORY.md');
  if (fs.existsSync(memPath)) {
    const content = readFile(memPath);
    const ageDays = fileAgeDays(memPath);
    if (!content || content.length < 100) {
      results.push({ file: 'MEMORY.md', status: 'SUSPICIOUS', level: 'HIGH', detail: '文件为空或过小' });
    } else {
      for (const { pattern, desc, requireHarmful } of BEHAVIORAL_PATTERNS) {
        if (pattern.test(content)) {
          if (requireHarmful && !HARMFUL_KEYWORDS.test(content)) continue;
          results.push({ file: 'MEMORY.md', status: 'FOUND', level: 'HIGH', detail: desc });
          break;
        }
      }
      if (!results.some(r => r.file === 'MEMORY.md')) {
        results.push({ file: 'MEMORY.md', status: 'CLEAN', level: 'INFO', detail: `大小${(content.length/1024).toFixed(1)}KB, ${ageDays?.toFixed(1)}天前` });
      }
    }
  }
  return results;
}

// ── Capability Check ──────────────────────────────────────────────────────────
function checkCapability() {
  const results = [];
  const skillsDir = path.join(WORKSPACE, 'skills');
  if (!fs.existsSync(skillsDir)) return { results: [], scanned: 0, issues: 0 };

  const skillDirs = fs.readdirSync(skillsDir).filter(f => {
    try { return fs.statSync(path.join(skillsDir, f)).isDirectory(); } catch { return false; }
  });

  let scanned = 0;
  let issues = 0;

  for (const skill of skillDirs) {
    const scripts = findScripts(path.join(skillsDir, skill));
    for (const script of scripts) {
      scanned++;
      const content = readFile(script);
      if (!content) continue;
      const relPath = `${skill}/${path.basename(script)}`;

      // 1. Suspicious URL
      const urls = content.match(/https?:\/\/[a-z0-9.-]+/gi) || [];
      for (const url of urls) {
        if (isSuspiciousUrl(url)) {
          const domain = url.replace(/^https?:\/\//, '').split('/')[0];
          results.push({ file: relPath, status: 'FOUND', level: 'HIGH', detail: `可疑外部URL: ${domain}` });
          issues++;
          break;
        }
      }

      // 2. Credential exfil to suspicious domain
      const credExfil = /(?:api[_-]?key|token|secret|credential|password)\s*[=:]\s*['"][A-Za-z0-9_-]{10,}['"]\s*[,;]?\s*(https?:\/\/[^\s'"]+)/g;
      let m;
      while ((m = credExfil.exec(content)) !== null) {
        const url = m[1];
        if (isSuspiciousUrl(url)) {
          results.push({ file: relPath, status: 'FOUND', level: 'CRITICAL', detail: `凭证外传到可疑域名: ${url}` });
          issues++;
          break;
        }
      }

      // 3. Hidden eval with user input
      if (/eval\s*\(\s*(req|body|input|data|params|query|headers|cookies)\./.test(content)) {
        results.push({ file: relPath, status: 'FOUND', level: 'CRITICAL', detail: '动态代码执行(用户输入)' });
        issues++;
      }

      // 4. Root-level deletion
      if (/rm\s+-rf\s+\/|Remove-Item\s+.*-Recurse\s+-[Rf]\s*\$?\/(?!home|Users|app)/.test(content)) {
        results.push({ file: relPath, status: 'FOUND', level: 'CRITICAL', detail: '危险删除命令(根目录)' });
        issues++;
      }
    }
  }
  return { results, scanned, issues };
}

function findScripts(dir, files = []) {
  try {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
        findScripts(full, files);
      } else if (entry.isFile() && /\.(py|js|ts|ps1|sh)$/.test(entry.name)) {
        files.push(full);
      }
    }
  } catch {}
  return files;
}

// ── Snapshot ─────────────────────────────────────────────────────────────────
function saveSnapshot(label, data) {
  ensureDir(SNAPSHOT_DIR);
  const fp = path.join(SNAPSHOT_DIR, `${label}-${Date.now()}.json`);
  const snap = { label, time: new Date().toISOString(), data };
  fs.writeFileSync(fp, JSON.stringify(snap, null, 2));
  return fp;
}

function log(msg) {
  ensureDir(AUDIT_DIR);
  fs.appendFileSync(ALERT_LOG, msg + '\n');
  if (flags.verbose) console.error(msg);
}

// ── Main ─────────────────────────────────────────────────────────────────────
function main() {
  ensureDir(AUDIT_DIR);
  const output = { timestamp: new Date().toISOString(), checks: {} };

  if (!flags.check || flags.check === 'identity') output.checks.identity = checkIdentity();
  if (!flags.check || flags.check === 'knowledge') output.checks.knowledge = checkKnowledge();
  if (!flags.check || flags.check === 'capability') output.checks.capability = checkCapability();

  saveSnapshot('audit-v4', output);

  const allIssues = [
    ...(output.checks.identity || []).filter(r => r.level === 'CRITICAL' || r.level === 'HIGH'),
    ...(output.checks.knowledge || []).filter(r => r.level === 'CRITICAL' || r.level === 'HIGH'),
    ...(output.checks.capability?.results || []).filter(r => r.level === 'CRITICAL' || r.level === 'HIGH'),
  ];

  if (allIssues.length > 0) {
    log(`[${new Date().toISOString()}] [WARNING] [CIK] 发现 ${allIssues.length} 个潜在安全问题`);
    for (const i of allIssues) log(`[${new Date().toISOString()}] [${i.level}] [CIK] ${i.file}: ${i.detail}`);
  } else {
    log(`[${new Date().toISOString()}] [INFO] [CIK] 安全检查完成, 无严重问题`);
  }

  if (flags.json) {
    console.log(JSON.stringify(output, null, 2));
  } else {
    printReport(output);
  }

  process.exit(allIssues.some(i => i.level === 'CRITICAL') ? 2 : 0);
}

function printReport(o) {
  console.log('\n🛡️  CIK Security Audit v4');
  console.log(`时间: ${o.timestamp}\n`);

  const dims = { identity: 'Identity (身份)', knowledge: 'Knowledge (知识)', capability: 'Capability (能力)' };
  for (const [dim, label] of Object.entries(dims)) {
    const data = o.checks[dim];
    if (!data) continue;
    const items = Array.isArray(data) ? data : data.results || [];
    const scanned = Array.isArray(data) ? null : data.scanned;
    const issues = items.filter(i => i.level === 'CRITICAL' || i.level === 'HIGH');
    console.log(`[${label}]${scanned ? ` (扫描 ${scanned} 个脚本)` : ''}`);
    if (issues.length === 0) {
      console.log('  ✅ 无严重问题\n');
    } else {
      for (const issue of issues) {
        const icon = issue.level === 'CRITICAL' ? '🚨' : '⚠️';
        console.log(`  ${icon} ${issue.file}: ${issue.detail}`);
      }
      console.log('');
    }
  }
  console.log(`📁 快照: ${path.join(AUDIT_DIR, 'snapshots')}`);
  console.log(`📁 告警: ${ALERT_LOG}\n`);
}

main();
