/**
 * qwen_chat.js — Talk to Qwen Chat via Chrome Relay
 * 
 * Usage:
 *   node qwen_chat.js status
 *   node qwen_chat.js read
 *   node qwen_chat.js send "message" [--wait 20] [--format text|markdown|html]
 * 
 * Requires: ws npm package (npm install ws)
 */

const WebSocket = require('ws');
const crypto = require('crypto');
const fs = require('fs');
const http = require('http');
const path = require('path');

// --- Config ---
const GATEWAY_PORT = 18789;
const RELAY_PORT = GATEWAY_PORT + 3; // 18792
const RELAY_CONTEXT = 'openclaw-extension-relay-v1';
const DEFAULT_WAIT_SEC = 45;
const STUCK_THINKING_NO_GROWTH_MS = 35000;
const PHASE2_GRACE_MS = 10000;
const DEBUG_EXTRACT = process.env.QWEN_CHAT_DEBUG_EXTRACT === '1' || process.argv.includes('--debug-extract');

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
function safeJsonParse(text, fallback) {
  try { return JSON.parse(text); } catch (_) { return fallback; }
}
function normalizeText(s) {
  return String(s || '').replace(/\r\n/g, '\n').trim();
}

// --- HTML to Markdown Converter (for Qwen's DOM structure) ---
function htmlToMarkdown(html) {
  if (!html) return '';
  
  // Simple regex-based HTML to Markdown converter optimized for Qwen's structure
  let md = html;
  
  // Remove script and style tags
  md = md.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '');
  md = md.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '');
  
  // Headings
  md = md.replace(/<h1[^>]*>([\s\S]*?)<\/h1>/gi, '\n# $1\n\n');
  md = md.replace(/<h2[^>]*>([\s\S]*?)<\/h2>/gi, '\n## $1\n\n');
  md = md.replace(/<h3[^>]*>([\s\S]*?)<\/h3>/gi, '\n### $1\n\n');
  md = md.replace(/<h4[^>]*>([\s\S]*?)<\/h4>/gi, '\n#### $1\n\n');
  md = md.replace(/<h5[^>]*>([\s\S]*?)<\/h5>/gi, '\n##### $1\n\n');
  md = md.replace(/<h6[^>]*>([\s\S]*?)<\/h6>/gi, '\n###### $1\n\n');
  
  // Monaco Editor code blocks - extract from view-lines
  md = md.replace(/<div class="monaco-editor[^"]*"[^>]*>([\s\S]*?)<\/div>\s*<\/div>\s*<\/div>\s*<\/div>\s*<\/div>/gi, function(match) {
    // Try to find view-lines which contains the actual code
    const viewLinesMatch = match.match(/<div class="view-lines"[^>]*>([\s\S]*?)<\/div>/i);
    if (viewLinesMatch) {
      let code = viewLinesMatch[1];
      // Extract text from each line
      const lines = code.match(/<div class="view-line"[^>]*>([\s\S]*?)<\/div>/gi) || [];
      const codeLines = lines.map(line => {
        // Remove HTML tags, keep text
        return line.replace(/<[^>]+>/g, '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
      });
      return codeLines.join('\n');
    }
    return '';
  });
  
  // Code blocks - generic patterns
  md = md.replace(/<pre[^>]*class="[^"]*language-(\w+)[^"]*"[^>]*><code[^>]*>([\s\S]*?)<\/code><\/pre>/gi, '\n```$1\n$2\n```\n\n');
  md = md.replace(/<pre[^>]*><code[^>]*>([\s\S]*?)<\/code><\/pre>/gi, '\n```\n$1\n```\n\n');
  
  // Inline code
  md = md.replace(/<code[^>]*>([\s\S]*?)<\/code>/gi, '`$1`');
  
  // Strong/Bold
  md = md.replace(/<(strong|b)[^>]*>([\s\S]*?)<\/\1>/gi, '**$2**');
  
  // Emphasis/Italic
  md = md.replace(/<(em|i)[^>]*>([\s\S]*?)<\/\1>/gi, '*$2*');
  
  // Links
  md = md.replace(/<a[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi, '[$2]($1)');
  
  // Images
  md = md.replace(/<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*\/?>/gi, '![$2]($1)');
  
  // Tables
  md = md.replace(/<table[^>]*>([\s\S]*?)<\/table>/gi, function(match, tableContent) {
    let result = '\n';
    const rows = tableContent.match(/<tr[^>]*>([\s\S]*?)<\/tr>/gi) || [];
    let headerProcessed = false;
    
    rows.forEach((row, idx) => {
      const cells = row.match(/<t[hd][^>]*>([\s\S]*?)<\/t[hd]>/gi) || [];
      const cellContents = cells.map(cell => {
        let content = cell.replace(/<t[hd][^>]*>/i, '').replace(/<\/t[hd]>/i, '');
        content = content.replace(/<[^>]+>/g, '').trim();
        return content || ' ';
      });
      
      if (cellContents.length > 0) {
        result += '| ' + cellContents.join(' | ') + ' |\n';
        // Add header separator after first row (assuming it's header)
        if (!headerProcessed && (row.includes('<th') || idx === 0)) {
          result += '| ' + cellContents.map(() => '---').join(' | ') + ' |\n';
          headerProcessed = true;
        }
      }
    });
    
    return result + '\n';
  });
  
  // Lists - unordered
  md = md.replace(/<ul[^>]*>([\s\S]*?)<\/ul>/gi, function(match, listContent) {
    const items = listContent.match(/<li[^>]*>([\s\S]*?)<\/li>/gi) || [];
    return items.map(item => {
      let content = item.replace(/<li[^>]*>/i, '').replace(/<\/li>/i, '');
      content = content.replace(/<[^>]+>/g, '').trim();
      return '- ' + content + '\n';
    }).join('') + '\n';
  });
  
  // Lists - ordered
  md = md.replace(/<ol[^>]*>([\s\S]*?)<\/ol>/gi, function(match, listContent) {
    const items = listContent.match(/<li[^>]*>([\s\S]*?)<\/li>/gi) || [];
    return items.map((item, idx) => {
      let content = item.replace(/<li[^>]*>/i, '').replace(/<\/li>/i, '');
      content = content.replace(/<[^>]+>/g, '').trim();
      return (idx + 1) + '. ' + content + '\n';
    }).join('') + '\n';
  });
  
  // Paragraphs and divs
  md = md.replace(/<p[^>]*>([\s\S]*?)<\/p>/gi, '$1\n\n');
  md = md.replace(/<div[^>]*class="qwen-markdown-paragraph"[^>]*>([\s\S]*?)<\/div>/gi, '$1\n\n');
  md = md.replace(/<div[^>]*>([\s\S]*?)<\/div>/gi, '$1\n');
  
  // Line breaks
  md = md.replace(/<br\s*\/?>/gi, '\n');
  md = md.replace(/<hr[^>]*>/gi, '\n---\n\n');
  
  // Spans - just extract content
  md = md.replace(/<span[^>]*>([\s\S]*?)<\/span>/gi, '$1');
  
  // Remove remaining HTML tags
  md = md.replace(/<[^>]+>/g, '');
  
  // Decode HTML entities
  md = md.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'");
  md = md.replace(/&nbsp;/g, ' ');
  
  // Clean up whitespace
  md = md.replace(/\n{3,}/g, '\n\n');
  md = md.replace(/[ \t]+$/gm, '');
  md = md.replace(/^[ \t]+/gm, '');
  
  return md.trim();
}
function isNoiseLine(line) {
  const t = normalizeText(line).toLowerCase();
  if (!t) return true;
  if (t === 'thinking completed' || t === 'auto' || t === 'a') return true;
  if (/generated content may not be accurate/.test(t)) return true;
  return false;
}
function cleanExtractedText(raw) {
  let text = normalizeText(raw)
    .replace(/^Thinking completed\s*/i, '')
    .replace(/\n?Auto\s*$/i, '')
    .replace(/\n?[AI]-?generated content may not be accurate\.\s*$/i, '')
    .trim();
  const lines = text.split('\n').map(s => s.trim());
  while (lines.length && isNoiseLine(lines[0])) lines.shift();
  while (lines.length && isNoiseLine(lines[lines.length - 1])) lines.pop();
  text = lines.join('\n').trim();
  return text;
}
function isLikelyNoiseText(text, message) {
  const t = normalizeText(text).toLowerCase();
  if (!t) return true;
  if (t === normalizeText(message).toLowerCase()) return true;
  if (/^(thinking completed|auto)$/i.test(t)) return true;
  if (/generated content may not be accurate/.test(t)) return true;
  return false;
}
function diffLeafTexts(baselineLeaves, latestLeaves, message) {
  const counts = new Map();
  for (const leaf of baselineLeaves || []) {
    const key = normalizeText(leaf);
    if (!key) continue;
    counts.set(key, (counts.get(key) || 0) + 1);
  }
  const out = [];
  for (const leaf of latestLeaves || []) {
    const key = normalizeText(leaf);
    if (!key) continue;
    const cnt = counts.get(key) || 0;
    if (cnt > 0) {
      counts.set(key, cnt - 1);
      continue;
    }
    if (isLikelyNoiseText(key, message)) continue;
    out.push(key);
  }
  return out;
}
function extractAfterPrompt(fullText, message) {
  const all = normalizeText(fullText);
  const prompt = normalizeText(message);
  if (!all || !prompt) return '';
  const idx = all.lastIndexOf(prompt);
  if (idx < 0) return '';
  return normalizeText(all.slice(idx + prompt.length));
}

// --- Token derivation ---
function getRelayToken() {
  const home = process.env.HOME || process.env.USERPROFILE || '';
  const configPaths = [
    'E:\\.openclaw\\.openclaw\\openclaw.json',
    path.join(home, '.openclaw', '.openclaw', 'openclaw.json'),
    path.join(home, '.openclaw', 'openclaw.json'),
  ];
  let configPath;
  for (const p of configPaths) { if (fs.existsSync(p)) { configPath = p; break; } }
  if (!configPath) throw new Error('Cannot find openclaw.json');
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const token = config.gateway?.auth?.token;
  if (!token) throw new Error('No gateway.auth.token in config');
  return crypto.createHmac('sha256', token)
    .update(`${RELAY_CONTEXT}:${RELAY_PORT}`).digest('hex');
}

// --- HTTP helper ---
function httpGet(url, headers = {}) {
  return new Promise((resolve, reject) => {
    http.get(url, { headers }, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve({ status: res.statusCode, body: data }));
    }).on('error', reject);
  });
}

// --- CDP helpers ---
let msgId = 1;
function cdpSend(ws, method, params = {}, sid) {
  return new Promise((resolve, reject) => {
    const id = msgId++;
    const timer = setTimeout(() => reject(new Error(`CDP timeout: ${method}`)), 20000);
    const handler = (raw) => {
      const msg = JSON.parse(raw.toString());
      if (msg.id === id) {
        clearTimeout(timer);
        ws.removeListener('message', handler);
        if (msg.error) reject(new Error(msg.error.message));
        else resolve(msg.result);
      }
    };
    ws.on('message', handler);
    const payload = { id, method, params };
    if (sid) payload.sessionId = sid;
    ws.send(JSON.stringify(payload));
  });
}

async function connectCdp(token) {
  const ws = new WebSocket(`ws://127.0.0.1:${RELAY_PORT}/cdp`, {
    headers: { 'x-openclaw-relay-token': token }
  });
  await new Promise((resolve, reject) => { ws.on('open', resolve); ws.on('error', reject); });
  return ws;
}

async function getQwenTab(token) {
  const res = await httpGet(`http://127.0.0.1:${RELAY_PORT}/json`, {
    'x-openclaw-relay-token': token
  });
  if (res.status !== 200) throw new Error(`Relay /json failed: ${res.status}`);
  const tabs = JSON.parse(res.body);
  const qwen = tabs.find(t => t.url.includes('chat.qwen.ai'));
  if (!qwen) throw new Error('No Qwen Chat tab found. Open chat.qwen.ai in Chrome and attach extension.');
  return qwen;
}

// --- Eval helper with sessionId ---
function makeEval(ws, sid) {
  return (expr) => new Promise((resolve, reject) => {
    const id = msgId++;
    const timer = setTimeout(() => reject(new Error('eval timeout')), 15000);
    const handler = (raw) => {
      const msg = JSON.parse(raw.toString());
      if (msg.id === id) {
        clearTimeout(timer);
        ws.removeListener('message', handler);
        if (msg.error) reject(new Error(msg.error.message));
        else resolve(msg.result?.result?.value);
      }
    };
    ws.on('message', handler);
    ws.send(JSON.stringify({ id, method: 'Runtime.evaluate', params: { expression: expr, returnByValue: true }, sessionId: sid }));
  });
}

// --- Input helpers ---
async function typeText(ws, sid, text, evalCmd) {
  await evalCmd(`document.querySelector('textarea.message-input-textarea').focus()`);
  await cdpSend(ws, 'Input.insertText', { text }, sid);
}

async function pressEnter(ws, sid) {
  await cdpSend(ws, 'Input.dispatchKeyEvent', {
    type: 'keyDown', key: 'Enter', code: 'Enter',
    windowsVirtualKeyCode: 13, nativeVirtualKeyCode: 13
  }, sid);
  await cdpSend(ws, 'Input.dispatchKeyEvent', {
    type: 'keyUp', key: 'Enter', code: 'Enter',
    windowsVirtualKeyCode: 13, nativeVirtualKeyCode: 13
  }, sid);
}

// --- Core: get chat area stats (length + all leaves text) ---
// CHAT_AREA_JS: returns {chatLen, allText, leafCount} for message-like elements in main content.
// Uses selectors verified to work on chat.qwen.ai
const CHAT_AREA_JS = `(function(){
  var leaves = [];
  // Use the proven selector from diagnostic: custom-qwen-markdown contains the response text
  var els = document.querySelectorAll('.custom-qwen-markdown, .qwen-markdown, [class*="response-message-content"]');
  for(var i=0;i<els.length;i++){
    var e=els[i];
    if (e.closest('aside, nav, [class*="sidebar"], [class*="history"]')) continue;
    var b=e.getBoundingClientRect();
    if (b.width < 50 || b.height < 10) continue;
    // Skip wrapper elements that contain other markdown elements
    if(e.querySelector('.custom-qwen-markdown, .qwen-markdown')) continue;
    var t=(e.innerText||'').trim();
    if(t.length > 0) leaves.push({text:t, y:Math.round(b.y)});
  }
  leaves.sort(function(a,b){return a.y-b.y;});
  var totalLen = 0;
  var allTexts = [];
  leaves.forEach(function(l){totalLen += l.text.length; allTexts.push(l.text);});
  return JSON.stringify({chatLen:totalLen, allText:allTexts.join('\\n\\n'), leafCount:leaves.length, leaves:allTexts});
})()`;

// Preferred completion signal: page can send next message again.
const SEND_READY_JS = `(function(){
  var ta = document.querySelector('textarea.message-input-textarea')
    || document.querySelector('textarea')
    || document.querySelector('[contenteditable="true"]');

  var inputEditable = false;
  if (ta) {
    if (ta.tagName === 'TEXTAREA') {
      inputEditable = !ta.disabled && !ta.readOnly && ta.getAttribute('aria-disabled') !== 'true';
    } else {
      var ce = (ta.getAttribute('contenteditable') || '').toLowerCase();
      inputEditable = ce === '' || ce === 'true';
    }
  }

  var sendBtn = document.querySelector('button[aria-label*="Send"], button[aria-label*="发送"], button[data-testid*="send"]');
  var stopBtn = document.querySelector('button[aria-label*="Stop"], button[aria-label*="停止"], button[class*="stop"]');
  var sendEnabled = true;

  if (sendBtn) {
    sendEnabled = !sendBtn.disabled && sendBtn.getAttribute('aria-disabled') !== 'true';
  }
  var stopActive = !!(stopBtn && !stopBtn.disabled && stopBtn.getAttribute('aria-disabled') !== 'true');
  if (stopActive) {
    sendEnabled = false;
  }

  return JSON.stringify({
    canSend: !!(ta && inputEditable && sendEnabled && !stopActive),
    hasInput: !!ta,
    inputEditable: !!inputEditable,
    hasSendBtn: !!sendBtn,
    sendEnabled: !!sendEnabled,
    hasStopBtn: !!stopBtn,
    stopActive: !!stopActive
  });
})()`;

// --- Commands ---

async function status() {
  const token = getRelayToken();
  try {
    const res = await httpGet(`http://127.0.0.1:${RELAY_PORT}/extension/status`, {
      'x-openclaw-relay-token': token
    });
    const ext = JSON.parse(res.body);
    console.log(`Extension: ${ext.connected ? '✅ Connected' : '❌ Disconnected'}`);
    if (ext.connected) {
      const tabs = await httpGet(`http://127.0.0.1:${RELAY_PORT}/json`, {
        'x-openclaw-relay-token': token
      });
      const all = JSON.parse(tabs.body);
      const qwen = all.find(t => t.url.includes('chat.qwen.ai'));
      console.log(`Qwen tab: ${qwen ? '✅ ' + qwen.title : '❌ Not found'}`);
      if (qwen) console.log(`  URL: ${qwen.url}`);
    }
  } catch (e) {
    console.error('❌ Relay not reachable:', e.message);
    process.exit(1);
  }
}

async function readPage() {
  const token = getRelayToken();
  const tab = await getQwenTab(token);
  const ws = await connectCdp(token);
  try {
    const attached = await cdpSend(ws, 'Target.attachToTarget', { targetId: tab.id, flatten: true }, null);
    const sid = attached.sessionId;
    const evalCmd = makeEval(ws, sid);
    const info = await evalCmd('JSON.stringify({title:document.title, url:location.href, bodyLen:document.body.innerText.length})');
    console.log('Page info:', info);
    console.log('\n--- Page Text ---');
    console.log(await evalCmd('document.body.innerText'));
  } finally { ws.close(); }
}

async function sendMessage(message, waitSec, format = 'text') {
  const token = getRelayToken();
  const tab = await getQwenTab(token);
  const ws = await connectCdp(token);

  try {
    const attached = await cdpSend(ws, 'Target.attachToTarget', { targetId: tab.id, flatten: true }, null);
    const sid = attached.sessionId;
    const evalCmd = makeEval(ws, sid);

    // Clear input
    await evalCmd(`(function(){
      var ta = document.querySelector('textarea') || document.querySelector('[contenteditable="true"]');
      if(!ta) return 'no-input';
      ta.focus();
      if(ta.tagName==='TEXTAREA') ta.value=''; else ta.textContent='';
      ta.dispatchEvent(new Event('input',{bubbles:true}));
      return 'cleared';
    })()`);

    // Record baselines BEFORE sending
    const baselineLen = await evalCmd('document.body.innerText.length');
    const baselineChatRaw = await evalCmd(CHAT_AREA_JS);
    const baselineChat = safeJsonParse(baselineChatRaw || '{}', { chatLen: 0, allText: '', leafCount: 0, leaves: [] });
    const baselineChatText = typeof baselineChat.allText === 'string' ? baselineChat.allText : '';
    const baselineLeaves = Array.isArray(baselineChat.leaves) ? baselineChat.leaves : [];
    console.log(`📊 Baseline bodyLen: ${baselineLen}`);

    // Type and send
    console.log('📝 Typing message...');
    await typeText(ws, sid, message, evalCmd);
    console.log('🚀 Sending...');
    await pressEnter(ws, sid);

    // Wait for textarea to clear (message sent)
    for (var i = 0; i < 10; i++) {
      await sleep(500);
      const taVal = await evalCmd(`(function(){var ta=document.querySelector('textarea');return ta?ta.value:'';})()`);
      if (!taVal) break;
    }
    const postSendLen = await evalCmd('document.body.innerText.length');

    // Phase 1: Wait until page is ready to send next question
    const maxWaitSec = Number.isFinite(waitSec) && waitSec > 0 ? waitSec : DEFAULT_WAIT_SEC;
    const maxMs = maxWaitSec * 1000;
    const noGrowthLimitMs = Math.max(
      STUCK_THINKING_NO_GROWTH_MS,
      Math.min(90000, Math.floor(maxMs * 0.6))
    );
    const start = Date.now();
    const deadline = start + maxMs;
    const minReplyGrowth = Math.max(16, Math.floor(String(message || '').length * 0.8));
    let lastProgressLog = 0;
    console.log(`⏳ Waiting until page is send-ready again (max ${maxWaitSec}s)...`);

    // Wait for controls to become usable again.
    let largestLen = await evalCmd('document.body.innerText.length');
    let lastGrowthAt = Date.now();
    let timedOutInPhase1 = false;
    let readyDetected = false;
    let generationStarted = false;
    let replyGrowthSeen = false;
    while (Date.now() < deadline) {
      await sleep(2000);
      const readinessRaw = await evalCmd(SEND_READY_JS);
      const readiness = safeJsonParse(readinessRaw || '{}', {});
      const curLen = await evalCmd('document.body.innerText.length');

      if (curLen > largestLen + 20) {
        largestLen = curLen;
        lastGrowthAt = Date.now();
      }
      if (curLen > postSendLen + minReplyGrowth) replyGrowthSeen = true;
      if (!generationStarted) {
        if (!readiness.canSend || readiness.stopActive || curLen > postSendLen + 20) {
          generationStarted = true;
          console.log('🟢 Generation started, waiting for completion...');
        }
      }

      if (Date.now() - lastProgressLog >= 10000) {
        const elapsed = Math.round((Date.now() - start) / 1000);
        console.log(
          `⏱️ Progress: ${elapsed}s elapsed, bodyLen=${curLen}, canSend=${!!readiness.canSend}, ` +
          `inputEditable=${!!readiness.inputEditable}, sendEnabled=${!!readiness.sendEnabled}`
        );
        lastProgressLog = Date.now();
      }

      if (generationStarted && readiness.canSend && (replyGrowthSeen || Date.now() - start > 12000)) {
        await sleep(1000); // double-check
        const readinessRaw2 = await evalCmd(SEND_READY_JS);
        const readiness2 = safeJsonParse(readinessRaw2 || '{}', {});
        if (readiness2.canSend) {
          readyDetected = true;
          console.log('✅ Page is send-ready again.');
          break;
        }
      }

      // Fallback: no growth for too long, do best-effort extraction.
      if (
        generationStarted &&
        Date.now() - lastGrowthAt > noGrowthLimitMs &&
        largestLen > postSendLen + 20
      ) {
        console.log(`⚠️ No content growth for ${Math.round(noGrowthLimitMs / 1000)}s; moving on with best-effort extraction.`);
        break;
      }

      // Additional fallback: if canSend stays false but content is stable for long enough
      if (
        generationStarted &&
        !readiness.canSend &&
        Date.now() - lastGrowthAt > 25000 &&
        largestLen > postSendLen + 100
      ) {
        console.log('⚠️ canSend still false but content stable for 25s; moving on with extraction.');
        break;
      }
    }
    if (Date.now() >= deadline) {
      timedOutInPhase1 = true;
      console.log('⚠️ Reached wait timeout before send-ready signal, attempting best-effort extraction...');
    }
    if (!readyDetected) console.log('ℹ️ Send-ready signal not confirmed, entering stabilization phase...');
    console.log('✅ Waiting for content to stabilize...');

    // Phase 2: Wait for bodyLen to stabilize (no more growth)
    let lastLen = await evalCmd('document.body.innerText.length');
    let stableTicks = 0;
    let lastGrowthAtPhase2 = Date.now();
    const phase2Deadline = deadline + PHASE2_GRACE_MS;

    while (Date.now() < phase2Deadline) {
      await sleep(2000);
      const curLen = await evalCmd('document.body.innerText.length');
      if (curLen > lastLen + 20) {
        // Still growing
        stableTicks = 0;
        lastLen = curLen;
        lastGrowthAtPhase2 = Date.now();
      } else {
        // Stable
        stableTicks++;
        if (stableTicks >= 2) { // stable for 4+ seconds
          console.log(`✅ Content stable at bodyLen ${curLen}`);
          break;
        }
      }

      if (Date.now() - lastProgressLog >= 10000) {
        const elapsed = Math.round((Date.now() - start) / 1000);
        console.log(`⏱️ Stabilizing: ${elapsed}s elapsed, bodyLen=${curLen}, stableTicks=${stableTicks}`);
        lastProgressLog = Date.now();
      }

      if (Date.now() >= deadline && Date.now() - lastGrowthAtPhase2 > 6000) {
        console.log('⚠️ Wait budget exhausted and no recent growth; finalizing current result.');
        break;
      }
    }

    // Extract NEW content from chat area first (less noisy than full body).
    const latestChatRaw = await evalCmd(CHAT_AREA_JS);
    const latestChat = safeJsonParse(latestChatRaw || '{}', { chatLen: 0, allText: '', leafCount: 0, leaves: [] });
    const latestChatText = typeof latestChat.allText === 'string' ? latestChat.allText : '';
    const latestLeaves = Array.isArray(latestChat.leaves) ? latestChat.leaves : [];
    const latestBodyLen = await evalCmd('document.body.innerText.length');
    let newContent = '';
    let usedPath = '';
    
    // Strategy 1: If chat area grew, use that
    const leafDiff = diffLeafTexts(baselineLeaves, latestLeaves, message);
    if (leafDiff.length > 0 && leafDiff.join('').length > 50) {
      newContent = leafDiff.join('\n\n').trim();
      usedPath = 'leafDiff';
    }
    // Strategy 2: chatText grew - slice from baseline
    if (!newContent && latestChatText.length > baselineChatText.length + 30) {
      const idx = latestChatText.lastIndexOf(baselineChatText);
      if (idx >= 0) {
        newContent = latestChatText.slice(idx + baselineChatText.length).trim();
        usedPath = 'chatText-slice';
      }
    }
    // Strategy 3: bodyLen changed significantly (may indicate page reflow) - use anchor
    if (!newContent || isLikelyNoiseText(newContent, message)) {
      const fullText = await evalCmd('document.body.innerText');
      // Try prompt-anchored extraction first
      const anchored = extractAfterPrompt(fullText, message);
      if (anchored && anchored.length > 30 && !isLikelyNoiseText(anchored, message)) {
        newContent = anchored;
        usedPath = 'anchor-after-prompt';
      } else if (latestBodyLen > baselineLen + 50) {
        // bodyLen grew, but we couldn't extract - take the delta
        newContent = fullText.slice(baselineLen).trim();
        usedPath = 'bodyLen-delta';
      } else {
        // Last resort: get text from main content area, then find the latest reply
        // Use a more robust method: find the LAST occurrence of the prompt in main
        const mainText = await evalCmd(`(function(){
          var main = document.querySelector('main.main-content') || document.querySelector('main');
          return main ? main.innerText : '';
        })()`);
        if (mainText && mainText.length > 50) {
          // Find the last occurrence of the user's message
          // But also look for common patterns that indicate a new Q&A pair
          let idx = mainText.lastIndexOf(message);
          
          // If found, take everything after it
          if (idx >= 0) {
            newContent = mainText.slice(idx + message.length).trim();
            usedPath = 'main-anchored';
          } else {
            // Fallback: look for the last "Thinking completed" or similar marker
            // and take content after that
            const markers = ['Thinking completed', 'Auto', 'AI-generated content'];
            let lastMarkerIdx = -1;
            for (const marker of markers) {
              const mIdx = mainText.lastIndexOf(marker);
              if (mIdx > lastMarkerIdx) lastMarkerIdx = mIdx;
            }
            if (lastMarkerIdx >= 0) {
              // Take content before this marker (the actual reply)
              newContent = mainText.slice(0, lastMarkerIdx).trim();
              // But we need to find where the reply starts
              // Try to find the prompt before this marker
              const beforeMarker = mainText.slice(0, lastMarkerIdx);
              const promptIdx = beforeMarker.lastIndexOf(message);
              if (promptIdx >= 0) {
                newContent = beforeMarker.slice(promptIdx + message.length).trim();
              }
            }
            usedPath = 'main-marker';
          }
        }
      }
    }

    let text = cleanExtractedText(newContent);

    // Format conversion
    if (format === 'markdown' || format === 'html') {
      // Find the response block that comes AFTER the user's message
      // Use direct string return to avoid JSON.stringify issues with special characters
      const formatResult = await evalCmd(`(function(){
        var main = document.querySelector('main.main-content') || document.querySelector('main');
        if (!main) return '';
        var prompt = ${JSON.stringify(message)};
        
        // Find all user message containers
        var userMessages = main.querySelectorAll('[class*="chat-user-message"], [class*="user-message"], [class*="message-user"]');
        
        // Find all response containers
        var responses = main.querySelectorAll('.custom-qwen-markdown, .qwen-markdown');
        
        var targetResponse = null;
        
        // If we have both, find the last user message and the response after it
        if (userMessages.length > 0 && responses.length > 0) {
          var lastUserMsg = null;
          for (var i = userMessages.length - 1; i >= 0; i--) {
            if (userMessages[i].innerText.indexOf(prompt) !== -1) {
              lastUserMsg = userMessages[i];
              break;
            }
          }
          
          if (lastUserMsg) {
            var userRect = lastUserMsg.getBoundingClientRect();
            for (var j = 0; j < responses.length; j++) {
              var respRect = responses[j].getBoundingClientRect();
              if (respRect.top > userRect.bottom) {
                targetResponse = responses[j];
                break;
              }
            }
          }
        }
        
        if (!targetResponse && responses.length > 0) {
          targetResponse = responses[responses.length - 1];
        }
        
        if (!targetResponse) return '';
        
        if ('${format}' === 'html') {
          return targetResponse.outerHTML;
        }
        
        // Convert response to markdown
        function nodeToMarkdown(node) {
          if (node.nodeType === Node.TEXT_NODE) {
            return node.textContent;
          }
          if (node.nodeType !== Node.ELEMENT_NODE) return '';
          
          var tag = node.tagName.toLowerCase();
          var result = '';
          var children = node.childNodes;
          
          // Handle specific element types
          if (tag === 'h1') {
            return '# ' + node.innerText.trim() + '\\n\\n';
          } else if (tag === 'h2') {
            return '## ' + node.innerText.trim() + '\\n\\n';
          } else if (tag === 'h3') {
            return '### ' + node.innerText.trim() + '\\n\\n';
          } else if (tag === 'h4') {
            return '#### ' + node.innerText.trim() + '\\n\\n';
          } else if (tag === 'strong' || tag === 'b') {
            var inner = '';
            for (var i = 0; i < children.length; i++) inner += nodeToMarkdown(children[i]);
            return '**' + inner.trim() + '**';
          } else if (tag === 'em' || tag === 'i') {
            var inner = '';
            for (var i = 0; i < children.length; i++) inner += nodeToMarkdown(children[i]);
            return '*' + inner.trim() + '*';
          } else if (tag === 'code') {
            var inner = '';
            for (var i = 0; i < children.length; i++) inner += nodeToMarkdown(children[i]);
            return '\`' + inner + '\`';
          } else if (tag === 'a') {
            var inner = '';
            for (var i = 0; i < children.length; i++) inner += nodeToMarkdown(children[i]);
            return '[' + inner + '](' + (node.href || '') + ')';
          } else if (tag === 'pre') {
            // Monaco Editor code block
            var codeEl = node.querySelector('.view-lines');
            if (codeEl) {
              var codeLines = codeEl.querySelectorAll('.view-line');
              var code = '';
              for (var i = 0; i < codeLines.length; i++) {
                code += codeLines[i].innerText + '\\n';
              }
              return '\\n\`\`\`\\n' + code.trim() + '\\n\`\`\`\\n\\n';
            }
            // Fallback: use innerText
            return '\\n\`\`\`\\n' + node.innerText.trim() + '\\n\`\`\`\\n\\n';
          } else if (tag === 'table') {
            var rows = node.querySelectorAll('tr');
            var md = '\\n';
            var isFirst = true;
            for (var r = 0; r < rows.length; r++) {
              var cells = rows[r].querySelectorAll('th, td');
              var rowText = '|';
              for (var c = 0; c < cells.length; c++) {
                rowText += ' ' + cells[c].innerText.trim().replace(/\\|/g, '\\\\|') + ' |';
              }
              md += rowText + '\\n';
              if (isFirst && rows[r].querySelector('th')) {
                md += '|' + Array(cells.length).fill(' --- ').join('|') + '|\\n';
                isFirst = false;
              }
            }
            return md + '\\n';
          } else if (tag === 'ul') {
            var items = node.querySelectorAll(':scope > li');
            var md = '';
            for (var i = 0; i < items.length; i++) {
              md += '- ' + items[i].innerText.trim() + '\\n';
            }
            return md + '\\n';
          } else if (tag === 'ol') {
            var items = node.querySelectorAll(':scope > li');
            var md = '';
            for (var i = 0; i < items.length; i++) {
              md += (i + 1) + '. ' + items[i].innerText.trim() + '\\n';
            }
            return md + '\\n';
          } else if (tag === 'hr') {
            return '\\n---\\n\\n';
          } else if (tag === 'br') {
            return '\\n';
          } else if (tag === 'p' || tag === 'div') {
            for (var i = 0; i < children.length; i++) result += nodeToMarkdown(children[i]);
            return result + '\\n\\n';
          } else {
            // Default: process children
            for (var i = 0; i < children.length; i++) result += nodeToMarkdown(children[i]);
            return result;
          }
        }
        
        return nodeToMarkdown(targetResponse);
      })()`);
      
      if (formatResult && formatResult.length > 50) {
        text = formatResult;
        usedPath = usedPath ? usedPath + '-' + format : format + '-extract';
      }
    }

    if (DEBUG_EXTRACT) {
      console.log('\n[DEBUG] extraction summary:');
      console.log(`  baselineBodyLen: ${baselineLen}, latestBodyLen: ${latestBodyLen}`);
      console.log(`  baselineLeaves: ${baselineLeaves.length}, latestLeaves: ${latestLeaves.length}`);
      console.log(`  leafDiff count: ${leafDiff.length}`);
      console.log(`  baselineChatText len: ${baselineChatText.length}`);
      console.log(`  latestChatText len: ${latestChatText.length}`);
      console.log(`  newContent len (raw): ${newContent.length}`);
      console.log(`  final text len: ${text.length}`);
      console.log(`  extraction path: ${usedPath || 'none'}`);
      console.log(`  format: ${format}`);
    }

    if (isLikelyNoiseText(text, message)) text = '';
    if (!text) timedOutInPhase1 = true;

    if (!text && timedOutInPhase1) {
      text = '[Timeout] Qwen response was not fully captured before wait limit. Try increasing --wait (e.g. 120-180).';
    }

    console.log(`\n--- Qwen Response (${text.length} chars) ---`);
    console.log(text);
    return text;

  } finally { ws.close(); }
}

// --- Main ---
const args = process.argv.slice(2);
const cmd = args[0];

function parseFormat(args) {
  const formatIdx = args.indexOf('--format');
  if (formatIdx > -1) {
    const f = args[formatIdx + 1];
    if (f === 'markdown' || f === 'md') return 'markdown';
    if (f === 'html') return 'html';
  }
  return 'text';
}

(async () => {
  switch (cmd) {
    case 'status': await status(); break;
    case 'read': await readPage(); break;
    case 'send': {
      const msg = args[1];
      if (!msg) { console.error('Usage: qwen_chat.js send "message" [--wait N] [--format text|markdown|html]'); process.exit(1); }
      const waitIdx = args.indexOf('--wait');
      const waitSec = waitIdx > -1 ? parseInt(args[waitIdx + 1]) || DEFAULT_WAIT_SEC : DEFAULT_WAIT_SEC;
      const format = parseFormat(args);
      await sendMessage(msg, waitSec, format);
      break;
    }
    default:
      console.log(`Usage: node qwen_chat.js <command>

Commands:
  status              Check Chrome Relay + Qwen tab status
  read                Read current Qwen page content
  send "msg" [options]
                      Send message and get response

Options for send:
  --wait N            Maximum wait time in seconds (default: ${DEFAULT_WAIT_SEC})
  --format FORMAT     Output format: text, markdown, html (default: text)
  --debug-extract     Show extraction debugging info

Examples:
  node qwen_chat.js send "What is ML?" --wait 30
  node qwen_chat.js send "Write a Python function" --format markdown
  node qwen_chat.js send "debug me" --wait 60 --debug-extract
`);
  }
})().catch(e => { console.error('Error:', e.message); process.exit(1); });
