#!/usr/bin/env node
/**
 * Extract Insights from Session Archive
 * - 分析归档内容，提取值得沉淀到 self-improving 的洞察
 * - 输出到 .insights-candidates.md 供主 agent 下次启动时审查
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 跨平台路径：优先读环境变量，其次用 HOME 动态构建
const USER_HOME = process.env.HOME || os.homedir();
const OPENCLAW_HOME = process.env.OPENCLAW_HOME || path.join(USER_HOME, '.openclaw');
const WORKSPACE = path.join(OPENCLAW_HOME, 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const SELF_IMPROVING_DIR = path.join(USER_HOME, 'self-improving');
const TODAY = new Date().toISOString().split('T')[0];
const CANDIDATES_FILE = path.join(MEMORY_DIR, `.insights-candidates-${TODAY}.md`);

// ─── 模式定义 ────────────────────────────────────────────────────────────────

const PATTERNS = {
  // 用户纠正了 AI 的行为
  corrections: [
    /不是\s*[,，.]/,
    /错了\s*[,，.]/,
    /不对\s*[,，.]/,
    /不用了\s*[,，.]/,
    /删掉\s*[,，.]/,
    /算了\s*[,，.]/,
    /忽略\s*[,，.]/,
    /重新/,
    /还原/,
    /不用\s*考虑/i
  ],

  // AI 承认错误或改进
  selfCorrections: [
    /抱歉\s*[,，.]/,
    /错了\s*[,，.]/,
    /纠正/i,
    /修正/i,
    /实际上/i,
    /更正/i
  ],

  // 新决策或结论
  decisions: [
    /建议.*是[:：]/,
    /结论.*[:：]/,
    /决定.*[:：]/,
    /.*更好$/m,
    /.*更合适$/m,
    /.*最优$/m,
    /.*合理$/m,
    /准确地说/i,
    /所以$/m
  ],

  // 用户偏好表达
  preferences: [
    /我喜欢/i,
    /我倾向.*不/i,
    /我不喜欢/i,
    /习惯了/i,
    /偏好/i,
    /不想.*用/i
  ],

  // 工作流程变化
  workflowChanges: [
    /统一走\s*subagent/i,
    /改用/i,
    /改回/i,
    /换成/i,
    /现在.*用/i,
    /任务分工/i
  ],

  // 教训总结
  lessons: [
    /记一下/i,
    /记录一下/i,
    /这个要记/i,
    /以后.*注意/i,
    /下次.*不/i,
    /要验证/i,
    /教训/i
  ],

  // 新技能/工具
  newCapabilities: [
    /技能.*装好了/i,
    /安装完成/i,
    /搞定.*✅/,
    /成功.*✅/,
    /已就绪/i
  ]
};

// ─── 辅助函数 ───────────────────────────────────────────────────────────────

function hash(s) {
  const crypto = require('crypto');
  return crypto.createHash('sha1').update(s).digest('hex').substring(0, 12);
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
    } catch (e) {}
  }

  return messages;
}

function stripConversationMeta(text) {
  return text
    .replace(/```json\s*\{[\s\S]*?"Conversation info[\s\S]*?"\}[\s\S]*?```/g, '')
    .replace(/^```json\n\{[\s\S]*?"Conversation info[\s\S]*?\}\n```$/gm, '')
    .replace(/^"?Conversation info"?[\s\S]*?```json[\s\S]*?```\s*/gm, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function matchPatterns(text, patterns) {
  return patterns.some(p => {
    if (p instanceof RegExp) return p.test(text);
    return false;
  });
}

// ─── 洞察提取 ───────────────────────────────────────────────────────────────

function extractInsights(sessionPath) {
  const content = fs.readFileSync(sessionPath, 'utf8');
  const messages = parseJsonl(content);

  const insights = {
    corrections: [],
    selfCorrections: [],
    decisions: [],
    preferences: [],
    workflowChanges: [],
    lessons: [],
    newCapabilities: []
  };

  const seen = new Set();

  for (const msg of messages) {
    if (msg.role !== 'user' && msg.role !== 'assistant') continue;

    const rawText = extractTextFromContent(msg.content);
    if (!rawText || rawText.length < 5) continue;

    const cleanText = stripConversationMeta(rawText).substring(0, 300);
    if (!cleanText || cleanText.length < 5) continue;

    // 去重
    const h = hash(cleanText.substring(0, 50));
    if (seen.has(h)) continue;
    seen.add(h);

    const roleLabel = msg.role === 'user' ? '👤' : '🤖';

    if (matchPatterns(cleanText, PATTERNS.corrections)) {
      insights.corrections.push({ role: msg.role, text: sanitizeForReview(cleanText) });
    }
    if (matchPatterns(cleanText, PATTERNS.selfCorrections)) {
      insights.selfCorrections.push({ role: msg.role, text: sanitizeForReview(cleanText) });
    }
    if (matchPatterns(cleanText, PATTERNS.decisions)) {
      insights.decisions.push({ role: msg.role, text: sanitizeForReview(cleanText) });
    }
    if (matchPatterns(cleanText, PATTERNS.preferences)) {
      insights.preferences.push({ role: msg.role, text: sanitizeForReview(cleanText) });
    }
    if (matchPatterns(cleanText, PATTERNS.workflowChanges)) {
      insights.workflowChanges.push({ role: msg.role, text: sanitizeForReview(cleanText) });
    }
    if (matchPatterns(cleanText, PATTERNS.lessons)) {
      insights.lessons.push({ role: msg.role, text: sanitizeForReview(cleanText) });
    }
    if (matchPatterns(cleanText, PATTERNS.newCapabilities)) {
      insights.newCapabilities.push({ role: msg.role, text: sanitizeForReview(cleanText) });
    }
  }

  return insights;
}

// ─── 生成候选报告 ───────────────────────────────────────────────────────────

function sanitizeForReview(text) {
  // 移除非文本内容，降低注入风险
  return text
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/`[^`]+`/g, '(code)')
    .replace(/```[\s\S]*?```/g, '(code block)')
    .replace(/\$\{[^}]+\}/g, '(var)')
    .replace(/\$\w+/g, '(env)')
    .substring(0, 400);
}

function generateCandidatesReport(sessionId, insights) {
  const total = Object.values(insights).reduce((sum, arr) => sum + arr.length, 0);

  if (total === 0) {
    return null;
  }

  const sections = [];

  const addSection = (title, items) => {
    if (items.length === 0) return;
    sections.push(`### ${title}（${items.length}条）\n`);
    items.slice(0, 5).forEach(item => {
      const label = item.role === 'user' ? '👤' : '🤖';
      sections.push(`- ${label} ${sanitizeForReview(item.text)}\n`);
    });
    sections.push('\n');
  };

  sections.push(`# 洞察候选 — ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n\n`);
  sections.push(`⚠️ **此文件仅供人工审查，不自动采纳**\n`);
  sections.push(`来源 session: \`${sessionId}\`\n\n`);
  sections.push('---\n\n');

  addSection('🤕 纠正（用户纠正了AI或有不同意见）', insights.corrections);
  addSection('🔄 自我修正（AI承认错误或改进）', insights.selfCorrections);
  addSection('📌 决策（形成明确结论）', insights.decisions);
  addSection('💡 偏好（用户表达了明确偏好）', insights.preferences);
  addSection('⚙️ 工作流变化', insights.workflowChanges);
  addSection('📝 教训（需要记住的规则）', insights.lessons);
  addSection('🆕 新能力/工具（技能安装完成）', insights.newCapabilities);

  sections.push('---\n');
  sections.push(`*由 extract-insights.js 自动生成 · 共 ${total} 条 · 需人工确认后才能采纳*\n`);

  return sections.join('');
}

// ─── 主流程 ─────────────────────────────────────────────────────────────────

function main() {
  console.log('=== Extract Insights ===');

  // 找到最新的 reset session
  const SESSION_DIR = path.join(OPENCLAW_HOME, 'agents/main/sessions');
  const files = fs.readdirSync(SESSION_DIR);
  const resetFiles = files
    .filter(f => f.includes('.reset.') && f.includes('T'))
    .map(f => ({
      name: f,
      path: path.join(SESSION_DIR, f),
      sessionId: f.split('.')[0],
      mtime: fs.statSync(path.join(SESSION_DIR, f)).mtime.getTime()
    }))
    .filter(f => f.sessionId.length > 30)
    .sort((a, b) => b.mtime - a.mtime);

  if (resetFiles.length === 0) {
    console.log('No reset sessions found');
    process.exit(0);
  }

  const latest = resetFiles[0];
  console.log('Analyzing:', latest.sessionId.substring(0, 8) + '...');

  const insights = extractInsights(latest.path);
  const total = Object.values(insights).reduce((sum, arr) => sum + arr.length, 0);
  console.log('Found insights:', total);

  if (total === 0) {
    process.exit(0);
  }

  const report = generateCandidatesReport(latest.sessionId, insights);
  if (report) {
    fs.writeFileSync(CANDIDATES_FILE, report);
    console.log('Candidates written to:', CANDIDATES_FILE);
  }
}

main();
