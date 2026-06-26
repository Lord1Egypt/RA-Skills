#!/usr/bin/env node

/**
 * Session Digest v4 - 只负责提取对话，总结交给 agent
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const OPENCLAW_DIR = process.env.OPENCLAW_DIR || path.join(process.env.HOME, '.openclaw');
const AGENTS_DIR = path.join(OPENCLAW_DIR, 'agents');

function parseDate(arg) {
  return arg || new Date().toISOString().split('T')[0];
}

function isOnDate(timestamp, dateStr) {
  return new Date(timestamp).toISOString().split('T')[0] === dateStr;
}

function getAllJsonlFiles() {
  const files = [];
  const agents = fs.readdirSync(AGENTS_DIR).filter(f => {
    return fs.statSync(path.join(AGENTS_DIR, f)).isDirectory();
  });

  for (const agent of agents) {
    const sessionsDir = path.join(AGENTS_DIR, agent, 'sessions');
    if (!fs.existsSync(sessionsDir)) continue;

    const jsonlFiles = fs.readdirSync(sessionsDir).filter(f => f.endsWith('.jsonl'));
    for (const file of jsonlFiles) {
      if (file.includes(':run:')) continue;
      files.push(path.join(sessionsDir, file));
    }
  }
  return files;
}

function cleanText(text) {
  let clean = text;
  clean = clean.replace(/```[\s\S]*?```/g, '');
  clean = clean.replace(/Conversation info.*$/gim, '');
  clean = clean.replace(/Sender.*$/gim, '');
  clean = clean.replace(/System:.*$/gm, '');
  clean = clean.replace(/\[Thread starter[^\]]*\]/g, '');
  clean = clean.replace(/\n{3,}/g, '\n\n').trim();
  return clean;
}

async function extractMessages(jsonlPath, dateStr) {
  if (!fs.existsSync(jsonlPath)) return [];
  const messages = [];
  const rl = readline.createInterface({ input: fs.createReadStream(jsonlPath), crlfDelay: Infinity });

  for await (const line of rl) {
    if (!line.trim()) continue;
    try {
      const entry = JSON.parse(line);
      if (entry.type !== 'message' || !entry.message) continue;
      if (!entry.timestamp || !isOnDate(entry.timestamp, dateStr)) continue;

      const { role, content } = entry.message;
      let text = typeof content === 'string' ? content :
                 Array.isArray(content) ? content.filter(c => c.type === 'text').map(c => c.text).join('\n') : '';
      text = cleanText(text);
      if (text.length < 10) continue;

      messages.push({ role, text: text.slice(0, 800) });
    } catch (e) {}
  }
  return messages;
}

function formatConversation(messages) {
  const lines = [];
  let currentRole = null;
  let buffer = [];

  for (const msg of messages) {
    if (msg.role !== currentRole) {
      if (buffer.length > 0) {
        lines.push(`【${currentRole === 'user' ? '用户' : '助手'}】`);
        lines.push(buffer.join('\n'));
        lines.push('');
        buffer = [];
      }
      currentRole = msg.role;
    }
    buffer.push(msg.text);
  }
  if (buffer.length > 0) {
    lines.push(`【${currentRole === 'user' ? '用户' : '助手'}】`);
    lines.push(buffer.join('\n'));
  }

  return lines.join('\n');
}

async function main() {
  const dateStr = parseDate(process.argv[2]);

  const files = getAllJsonlFiles();
  const allMessages = [];
  for (const file of files) {
    const msgs = await extractMessages(file, dateStr);
    allMessages.push(...msgs);
  }

  if (allMessages.length === 0) {
    console.log(`${dateStr} 没有对话记录`);
    return;
  }

  const text = formatConversation(allMessages);

  // 输出到临时文件
  const tmpFile = `/tmp/session-digest-${dateStr}.txt`;
  fs.writeFileSync(tmpFile, text);

  console.log(`${dateStr} 对话已提取到 ${tmpFile}`);
  console.log(`${files.length} 个 session，${allMessages.length} 条消息，${text.length} 字符`);
}

main().catch(e => { console.error(e); process.exit(1); });
