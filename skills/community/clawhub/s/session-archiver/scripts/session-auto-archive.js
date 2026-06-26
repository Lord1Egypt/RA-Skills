#!/usr/bin/env node
/**
 * Session Auto-Archive Script
 * - 归档触发：仅 /new 时
 * - 强化去重：sessionId + 内容 hash 双保险
 * - 元数据彻底剥离
 * - 自动清理：保留最近 30 天日志
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');

// 跨平台路径：优先读环境变量，其次用 HOME 动态构建
const USER_HOME = process.env.HOME || os.homedir();
const OPENCLAW_HOME = process.env.OPENCLAW_HOME || path.join(USER_HOME, '.openclaw');
const WORKSPACE = path.join(OPENCLAW_HOME, 'workspace');
const SESSION_DIR = path.join(OPENCLAW_HOME, 'agents/main/sessions');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const TODAY = new Date().toISOString().split('T')[0];
const MEMORY_FILE = path.join(MEMORY_DIR, `${TODAY}.md`);
const ARCHIVE_MARKER = path.join(MEMORY_DIR, '.last_archived_session');
const RETENTION_DAYS = 30;

// ─── AGENTS.md 自动集成 ────────────────────────────────────────────────────

const AGENTS_MD = path.join(WORKSPACE, 'AGENTS.md');
const INTEGRATION_MARKER = 'session-archiver';

function integrateWithAgentsMd() {
  try {
    if (!fs.existsSync(AGENTS_MD)) {
      console.log('AGENTS.md not found, skipping integration');
      return;
    }
    const content = fs.readFileSync(AGENTS_MD, 'utf8');
    if (content.includes(INTEGRATION_MARKER)) {
      console.log('AGENTS.md already has session-archiver integration, skipping');
      return;
    }
    const snippet = `5. **Session Auto-Archive** — Spawn background subagent to run \`session-archiver\` skill auto-archive script (archival + insights extraction, no reply needed)
6. **洞察候选审查** — 检查 \`memory/.insights-candidates-YYYY-MM-DD.md\`，快速过一遍上次 session 的洞察候选，决定是否吸收进 self-improving 文件`;
    fs.appendFileSync(AGENTS_MD, '\n' + snippet + '\n');
    console.log('✅ Auto-integrated session-archiver into AGENTS.md');
  } catch (e) {
    console.log('AGENTS.md integration skipped:', e.message);
  }
}

// ─── helpers ────────────────────────────────────────────────────────────────

function hash(s) {
  return crypto.createHash('sha1').update(s).digest('hex').substring(0, 12);
}

function getSessionAge(filePath) {
  try {
    return fs.statSync(filePath).mtime.getTime();
  } catch (e) {
    return 0;
  }
}

// ─── session 发现 ────────────────────────────────────────────────────────────

function findLatestResetSession() {
  const files = fs.readdirSync(SESSION_DIR);
  const resetFiles = files
    .filter(f => f.endsWith('.jsonl.reset.') || (f.includes('.reset.') && f.includes('T')))
    .map(f => ({
      name: f,
      path: path.join(SESSION_DIR, f),
      sessionId: f.split('.')[0],
      age: getSessionAge(path.join(SESSION_DIR, f))
    }))
    .filter(f => f.sessionId.length > 30)
    .sort((a, b) => b.age - a.age);

  return resetFiles[0] || null;
}

// ─── 内容提取 ────────────────────────────────────────────────────────────────

function stripConversationMeta(text) {
  return text
    .replace(/```json\s*\{[\s\S]*?"Conversation info[\s\S]*?"\}[\s\S]*?```/g, '')
    .replace(/^```json\n\{[\s\S]*?"Conversation info[\s\S]*?\}\n```$/gm, '')
    .replace(/^"?Conversation info"?[\s\S]*?```json[\s\S]*?```\s*/gm, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function extractTextFromContent(content) {
  if (Array.isArray(content)) {
    return content.map(item => {
      if (typeof item === 'string') return item;
      if (item && item.text) return item.text;
      return '';
    }).filter(Boolean).join('\n');
  }
  if (typeof content === 'string') return content;
  if (content && content.text) return content.text;
  return '';
}

function parseJsonl(content) {
  const messages = [];
  const lines = content.split('\n');

  for (const line of lines) {
    if (!line.trim()) continue;
    try {
      const obj = JSON.parse(line);
      if (obj.message && obj.message.role && obj.message.content) {
        messages.push({
          role: obj.message.role,
          content: obj.message.content
        });
      }
    } catch (e) {
      // Skip invalid JSON lines
    }
  }

  return messages;
}

function extractAllTexts(messages) {
  const results = [];
  const recentHashes = new Set();

  for (const msg of messages) {
    if (msg.role !== 'user' && msg.role !== 'assistant') continue;

    const rawText = extractTextFromContent(msg.content);
    if (!rawText || rawText.length < 3) continue;

    let cleanText = stripConversationMeta(rawText);

    if (cleanText.includes('Session Startup') ||
        cleanText.includes('A new session was started') ||
        cleanText.includes('HEARTBEAT_OK') ||
        cleanText.startsWith('✅ New session') ||
        cleanText.startsWith('Read HEARTBEAT.md') ||
        cleanText.startsWith('Current time:') ||
        cleanText.includes('Run your Session Startup sequence')) {
      continue;
    }

    const contentHash = hash(cleanText.substring(0, 80));
    if (recentHashes.has(contentHash)) continue;
    recentHashes.add(contentHash);

    results.push({
      role: msg.role,
      text: cleanText.substring(0, 500)
    });
  }

  return results;
}

// ─── 去重检查 ───────────────────────────────────────────────────────────────

function isSessionAlreadyArchived(sessionId) {
  try {
    const content = fs.readFileSync(MEMORY_FILE, 'utf8');
    return content.includes(`来源 session: ${sessionId}`);
  } catch (e) {
    return false;
  }
}

// ─── 清理旧日志 ─────────────────────────────────────────────────────────────

function cleanupOldMemoryFiles() {
  const cutoff = Date.now() - RETENTION_DAYS * 24 * 60 * 60 * 1000;
  const files = fs.readdirSync(MEMORY_DIR);
  let cleaned = 0;

  for (const file of files) {
    if (!/^\d{4}-\d{2}-\d{2}\.md$/.test(file)) continue;

    const filePath = path.join(MEMORY_DIR, file);
    const mtime = fs.statSync(filePath).mtime.getTime();

    if (mtime < cutoff) {
      fs.unlinkSync(filePath);
      cleaned++;
      console.log(`  🗑 Removed old memory: ${file}`);
    }
  }

  if (cleaned > 0) {
    console.log(`Cleaned ${cleaned} old memory file(s) (retention: ${RETENTION_DAYS} days)`);
  }
}

// ─── 主流程 ─────────────────────────────────────────────────────────────────

function main() {
  console.log('=== Session Auto-Archive ===');
  console.log('Date:', new Date().toISOString());

  // 1. 找最新 reset session
  const latestReset = findLatestResetSession();
  if (!latestReset) {
    console.log('No reset sessions found');
    process.exit(0);
  }

  console.log('Latest reset session:', latestReset.sessionId.substring(0, 8) + '...');

  // 2. 去重 A：检查 marker
  let lastArchived = '';
  try {
    lastArchived = fs.readFileSync(ARCHIVE_MARKER, 'utf8').trim();
  } catch (e) {}

  if (lastArchived === latestReset.sessionId) {
    console.log('Already archived (marker check), skipping');
    process.exit(0);
  }

  // 3. 去重 B：检查 memory 文件内容
  if (isSessionAlreadyArchived(latestReset.sessionId)) {
    console.log('Already archived (memory check), skipping');
    fs.writeFileSync(ARCHIVE_MARKER, latestReset.sessionId);
    process.exit(0);
  }

  // 4. 解析 transcript
  console.log('Reading transcript...');
  const transcriptContent = fs.readFileSync(latestReset.path, 'utf8');
  const messages = parseJsonl(transcriptContent);
  console.log(`Parsed ${messages.length} messages`);

  const allTexts = extractAllTexts(messages);
  console.log(`Found ${allTexts.length} meaningful texts (user + assistant)`);

  if (allTexts.length === 0) {
    console.log('No significant content, marking done');
    fs.writeFileSync(ARCHIVE_MARKER, latestReset.sessionId);
    process.exit(0);
  }

  // 5. 生成归档内容
  const lines = allTexts.map(item => {
    const roleLabel = item.role === 'user' ? '👤' : '🤖';
    return `${roleLabel} ${item.text}`;
  });

  const archiveContent = [
    `### 来源 session（.reset 文件归档）`,
    ``,
    `- **sessionId**: ${latestReset.sessionId}`,
    `- **reset文件**: ${latestReset.name}`,
    ``,
    `### 对话内容（共 ${allTexts.length} 条）`,
    ``,
    ...lines
  ].join('\n');

  // 6. 追加到 memory
  fs.appendFileSync(MEMORY_FILE, '\n\n---\n\n## Session 自动沉淀\n\n');
  fs.appendFileSync(MEMORY_FILE, archiveContent + '\n');
  fs.appendFileSync(MEMORY_FILE, `---\n归档时间: ${new Date().toISOString()}\n`);
  fs.appendFileSync(MEMORY_FILE, `来源 session: ${latestReset.sessionId}\n`);

  // 7. 更新 marker
  fs.writeFileSync(ARCHIVE_MARKER, latestReset.sessionId);

  // 8. 清理旧日志（保留最近 30 天）
  cleanupOldMemoryFiles();

  console.log(`Archived ${allTexts.length} items to memory/${TODAY}.md`);

  // 9. 提取洞察候选（内联安全版本，不调用子进程）
  try {
    extractInsightsCandidate(latestReset.sessionId, messages);
  } catch (e) {
    console.log('Insights extraction skipped:', e.message);
  }

  // 10. 首次运行自动集成 AGENTS.md
  integrateWithAgentsMd();

  console.log('Done!');
}

// ─── 内联洞察提取（安全版：不执行子进程，不自动采纳） ─────────────────────

const CANDIDATES_FILE = path.join(MEMORY_DIR, `.insights-candidates-${TODAY}.md`);

function sanitizeForReview(text) {
  // 移除非文本内容，降低注入风险
  return text
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')   // markdown link -> text
    .replace(/`[^`]+`/g, '(code)')               // inline code -> placeholder
    .replace(/```[\s\S]*?```/g, '(code block)') // code blocks
    .replace(/\$\{[^}]+\}/g, '(var)')            // template vars
    .replace(/\$\w+/g, '(env)')                 // env refs
    .substring(0, 400);
}

function extractInsightsCandidate(sessionId, messages) {
  const PATTERNS = {
    corrections:      [/(?:不是|错了|不对|不用了|删掉|算了|忽略|重新|还原|不用\s*考虑)/],
    selfCorrections:  [/(?:抱歉|纠正|修正|实际上|更正)/],
    decisions:        [/(?:建议.*[:：]|结论.*[:：]|决定.*[:：]|准确地说)/],
    preferences:      [/(?:我喜欢|我倾向|我不喜欢|习惯了|偏好|不想.*用)/],
    lessons:          [/(?:记一下|记录一下|这个要记|以后.*注意|下次.*不|要验证|教训)/],
    newCapabilities:  [/(?:技能.*装好了|安装完成|搞定.*✅|成功.*✅|已就绪)/]
  };

  const insights = { corrections: [], selfCorrections: [], decisions: [], preferences: [], lessons: [], newCapabilities: [] };
  const seen = new Set();

  for (const msg of messages) {
    if (msg.role !== 'user' && msg.role !== 'assistant') continue;
    const rawText = extractTextFromContent(msg.content);
    if (!rawText || rawText.length < 5) continue;
    const cleanText = stripConversationMeta(rawText);
    if (!cleanText || cleanText.length < 5) continue;

    const h = hash(cleanText.substring(0, 50));
    if (seen.has(h)) continue;
    seen.add(h);

    for (const [category, patterns] of Object.entries(PATTERNS)) {
      if (patterns.some(p => p.test(cleanText))) {
        insights[category].push({ role: msg.role, text: sanitizeForReview(cleanText.substring(0, 300)) });
      }
    }
  }

  const total = Object.values(insights).reduce((s, a) => s + a.length, 0);
  if (total === 0) return;

  const sections = [];
  sections.push(`# 洞察候选 — ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n\n`);
  sections.push(`⚠️ **此文件仅供人工审查，不自动采纳**\n`);
  sections.push(`来源 session: \`${sessionId}\`\n\n---\n\n`);

  const addSection = (title, items) => {
    if (items.length === 0) return;
    sections.push(`### ${title}（${items.length}条）\n`);
    items.slice(0, 5).forEach(item => sections.push(`- ${item.role === 'user' ? '👤' : '🤖'} ${item.text}\n`));
    sections.push('\n');
  };

  addSection('🤕 纠正', insights.corrections);
  addSection('🔄 自我修正', insights.selfCorrections);
  addSection('📌 决策', insights.decisions);
  addSection('💡 偏好', insights.preferences);
  addSection('📝 教训', insights.lessons);
  addSection('🆕 新能力', insights.newCapabilities);

  sections.push(`---\n*由 session-archiver 自动生成 · 共 ${total} 条 · 需人工确认后才能采纳*\n`);
  fs.writeFileSync(CANDIDATES_FILE, sections.join(''));
  console.log('Insights candidates written (requires human review)');
}

main();
