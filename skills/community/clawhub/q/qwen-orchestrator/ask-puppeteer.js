#!/usr/bin/env node
/**
 * Qwen Chat Orchestrator — Puppeteer-based interaction with chat.qwen.ai
 * Adapted from ai-orchestrator (DeepSeek) for Qwen Chat
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Local diagnostics + local auth check. Keep qwen-orchestrator fully self-contained.
let Diagnostics;
let requireAuth;
try {
  ({ Diagnostics } = require(path.join(__dirname, 'diagnostics.js')));
} catch (e) {
  Diagnostics = class { start(){} succeed(){} fail(){} skip(){} printSummary(){} save(){} summary(){} finish(){} };
}
try {
  ({ requireAuth } = require(path.join(__dirname, 'auth-check.js')));
} catch (e) {
  requireAuth = async () => true;
}

// ═══ Configuration ═══════════════════════════════════════════════════════
const SCRIPT_DIR = path.dirname(process.argv[1]);
const BASE_DIR = path.resolve(SCRIPT_DIR);
const CONFIG_PATH = path.join(BASE_DIR, '.qwen.json');

const DEFAULT_CONFIG = {
  browserLaunchTimeout: 30000,
  answerTimeout: 600000,
  composerTimeout: 10000,
  navigationTimeout: 30000,
  idleTimeout: 15000,
  heartbeatInterval: 15000,
  domErrorIdleMs: 25000,
  shortAnswerStableMs: 300,
  minResponseLength: 50,
  maxContinueRounds: 30,
  deltaThreshold: 100,
  rateLimitMs: 5000,
  followUpHydrationTimeoutMs: 20000,
  followUpStableMs: 2000,
  followUpMinVisibleHistoryNodes: 1,
  preferredModel: 'Qwen3.6-Max-Preview',
  debugMode: false,
  logToFile: false,
  logPath: '.logs/qwen.log',
};

function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      const user = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
      return { ...DEFAULT_CONFIG, ...user };
    }
  } catch (e) {}
  return DEFAULT_CONFIG;
}

const CONFIG = loadConfig();
const TIMEOUT_ANSWER = CONFIG.answerTimeout;
const TIMEOUT_BROWSER = CONFIG.browserLaunchTimeout;
const MIN_RESPONSE = CONFIG.minResponseLength;
const PREFERRED_MODEL = String(CONFIG.preferredModel || 'Qwen3.6-Max-Preview').trim();
const OVERSIZE_RETRY_MIN_CHARS = 4000;
const OVERSIZE_RETRY_KEEP_RATIO = 0.85;
const OVERSIZE_MAX_RETRIES = 6;

if (CONFIG.logToFile) {
  const logPath = path.resolve(BASE_DIR, CONFIG.logPath);
  try {
    fs.mkdirSync(path.dirname(logPath), { recursive: true });
    const origLog = console.log;
    console.log = (...args) => {
      const line = args.map(a => typeof a === 'object' ? JSON.stringify(a) : a).join(' ');
      fs.appendFileSync(logPath, `[${new Date().toISOString()}] ${line}\n`);
      origLog(...args);
    };
  } catch (e) {}
}

// ═══ CDP Interceptor state ═══════════════════════════════════════════════
var cdpInterceptor = null;
let answerBaseline = null;

const argv = process.argv.slice(2);
const isVisible = argv.includes('--visible');
const waitForAuth = argv.includes('--wait');
const shouldClose = argv.includes('--close');
const endSession = argv.includes('--end-session');
const newChat = argv.includes('--new-chat');
const useDaemon = argv.includes('--daemon');
const dryRun = argv.includes('--dry-run');
const doSearch = argv.includes('--search');
const VERBOSE = argv.includes('--verbose');
const DEBUG = argv.includes('--debug');
const FILE_ARG_IDX = argv.indexOf('--file');
const FILE_PROMPT_PATH = FILE_ARG_IDX !== -1 ? argv[FILE_ARG_IDX + 1] : null;

// ═══ Auto-detect Chrome ══════════════════════════════════════════════════
let executablePath;
try {
  const bundled = require('puppeteer').executablePath();
  if (bundled && fs.existsSync(bundled)) executablePath = bundled;
} catch {}
if (!executablePath) {
  try {
    const w = require('child_process').execSync(
      'which chromium 2>/dev/null || which chromium-browser 2>/dev/null || which google-chrome 2>/dev/null || echo ""',
      { encoding: 'utf8' }
    ).trim();
    if (w && fs.existsSync(w)) executablePath = w;
  } catch {}
}

// ═══ Helpers ═════════════════════════════════════════════════════════════
function log(...a) { console.log(...a); }
function debugLog(...a) { if (VERBOSE || DEBUG) console.log(...a); }
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
function ensureDirSync(d) { try { fs.mkdirSync(d, { recursive: true }); } catch {} }

function shortenPromptForRetry(prompt, attempt) {
  if (typeof prompt !== 'string') return prompt;
  const lines = prompt.split('\n');
  if (lines.length <= 6) {
    const hardMax = Math.max(OVERSIZE_RETRY_MIN_CHARS, Math.floor(prompt.length * Math.pow(OVERSIZE_RETRY_KEEP_RATIO, attempt)));
    return prompt.slice(0, hardMax).trimEnd();
  }
  const header = lines.slice(0, Math.min(6, lines.length)).join('\n');
  const body = lines.slice(Math.min(6, lines.length)).join('\n');
  const targetLen = Math.max(OVERSIZE_RETRY_MIN_CHARS, Math.floor(body.length * Math.pow(OVERSIZE_RETRY_KEEP_RATIO, attempt)));
  return `${header}\n\n[TRUNCATED_FOR_SUBMIT_RETRY: prompt shortened after silent oversize submit block]\n\n${body.slice(0, targetLen).trimEnd()}`;
}

function withExitCode(err, exitCode) {
  if (err && typeof err === 'object' && !err.exitCode) err.exitCode = exitCode;
  return err;
}

// ═══ Qwen-specific constants ═════════════════════════════════════════════
const QWEN_URL = 'https://chat.qwen.ai/';
const QWEN_CHAT_RE = /^https:\/\/chat\.qwen\.ai\/c\//;

function safePageUrl(page) {
  try { return page?.url?.() || ''; } catch { return ''; }
}

function isQwenChatUrl(url) {
  return typeof url === 'string' && QWEN_CHAT_RE.test(url);
}

function getQwenChatId(url) {
  if (typeof url !== 'string' || !url) return null;
  try {
    const u = new URL(url);
    const parts = u.pathname.split('/').filter(Boolean);
    return parts[0] === 'c' ? (parts[1] || null) : null;
  } catch {
    return null;
  }
}

function sameQwenChat(urlA, urlB) {
  const a = getQwenChatId(urlA);
  const b = getQwenChatId(urlB);
  return !!a && !!b && a === b;
}

function isPersistableQwenChatUrl(url) {
  if (!isQwenChatUrl(url)) return false;
  const chatId = getQwenChatId(url) || '';
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(chatId);
}

function describeContinuityMismatch(expectedUrl, currentUrl) {
  if (!expectedUrl || !currentUrl) return null;
  if (sameQwenChat(expectedUrl, currentUrl)) return null;
  if (currentUrl.includes('/c/new-chat')) {
    return `перешёл в new-chat (${currentUrl}) вместо ожидаемого чата`;
  }
  if (isQwenChatUrl(currentUrl)) {
    return `перешёл в другой чат (${currentUrl}) вместо ожидаемого`;
  }
  return `ушёл с ожидаемого chat URL на ${currentUrl}`;
}

async function waitForSameFollowUpChatStable(page, expectedUrl, timeoutMs = 12000, stableMs = 1500) {
  if (!expectedUrl) return safePageUrl(page);
  const started = Date.now();
  let stableSince = null;
  let lastGoodUrl = '';
  while (Date.now() - started < timeoutMs) {
    const currentUrl = safePageUrl(page);
    const mismatch = describeContinuityMismatch(expectedUrl, currentUrl);
    if (!mismatch) {
      if (currentUrl !== lastGoodUrl) {
        stableSince = Date.now();
        lastGoodUrl = currentUrl;
      } else if (stableSince !== null && Date.now() - stableSince >= stableMs) {
        return currentUrl;
      }
    } else {
      stableSince = null;
      lastGoodUrl = currentUrl;
    }
    await sleep(150);
  }
  const finalUrl = safePageUrl(page);
  throw new Error(`Follow-up chat did not stabilize: ожидался чат ${expectedUrl}, текущий URL ${finalUrl || '(empty)'}`);
}

async function rebindFollowUpChat(page, expectedUrl, reason = 'follow-up-rebind') {
  if (!expectedUrl) return safePageUrl(page);
  log(`♻️ Rebinding follow-up chat (${reason}): ${expectedUrl.substring(0, 80)}`);
  await page.goto(expectedUrl, { waitUntil: 'domcontentloaded', timeout: CONFIG.navigationTimeout });
  await page.waitForFunction(() => document.readyState === 'complete' || document.readyState === 'interactive', {
    timeout: Math.min(CONFIG.navigationTimeout, 5000),
  }).catch(() => {});
  const stableUrl = await waitForSameFollowUpChatStable(page, expectedUrl, 6000, 500);
  log(`♻️ Follow-up chat rebound: ${stableUrl.substring(0, 80)}`);
  return stableUrl;
}

async function waitForFollowUpChatReady(page, composerSelector, expectedUrl, options = {}) {
  if (!expectedUrl) return safePageUrl(page);
  const {
    timeoutMs = CONFIG.followUpHydrationTimeoutMs,
    stableMs = CONFIG.followUpStableMs,
    expectedChatTitle = null,
    expectHistory = true,
    minVisibleHistoryNodes = CONFIG.followUpMinVisibleHistoryNodes,
  } = options;

  const started = Date.now();
  let stableSince = null;
  let lastGoodUrl = '';
  let titleActivationTried = false;
  let hardRebindTried = false;

  while (Date.now() - started < timeoutMs) {
    const currentUrl = safePageUrl(page);
    const mismatch = describeContinuityMismatch(expectedUrl, currentUrl);
    if (mismatch) {
      stableSince = null;
      lastGoodUrl = currentUrl;
      await sleep(120);
      continue;
    }

    const remaining = Math.max(250, timeoutMs - (Date.now() - started));
    const composerReady = await page.waitForSelector(composerSelector, {
      visible: true,
      timeout: Math.min(1200, remaining),
    }).then(() => true).catch(() => false);

    const state = composerReady ? await page.evaluate(({ expectedTitle, expectHistory, minVisibleHistoryNodes }) => {
      const norm = (s) => (s || '').trim().replace(/\s+/g, ' ');
      const isVisible = (node) => {
        if (!node) return false;
        const s = getComputedStyle(node);
        const r = node.getBoundingClientRect();
        return s.visibility !== 'hidden' && s.display !== 'none' && r.width > 0 && r.height > 0;
      };
      const visibleCount = (sel) => Array.from(document.querySelectorAll(sel)).filter(isVisible).length;
      const messageSelectors = [
        'article',
        'div[class*="markdown-body" i]',
        'div[class*="message-content" i]',
        '.prose',
        '[data-testid*="message" i]',
        '[class*="message-item" i]',
        '[class*="conversation-item" i]'
      ];
      const visibleHistoryNodes = messageSelectors.reduce((sum, sel) => sum + visibleCount(sel), 0);
      const bodyText = norm(document.body?.innerText || '');
      const titleNorm = norm(expectedTitle || '');
      const activeTitleMatch = titleNorm ? Array.from(document.querySelectorAll('[aria-label="chat-item"], a, button, [role="button"]')).some((el) => {
        const txt = norm(el.innerText || el.textContent || '');
        if (!txt || !isVisible(el)) return false;
        const active = el.getAttribute('aria-current') === 'page'
          || el.getAttribute('aria-selected') === 'true'
          || /active|selected|current/i.test(typeof el.className === 'string' ? el.className : '');
        return active && (txt === titleNorm || txt.includes(titleNorm));
      }) : false;
      const newChatRoots = [
        '[data-page="new-chat"]',
        '[data-testid*="new-chat" i]',
        '[class*="new-chat" i]',
        '[href="/c/new-chat"]',
      ];
      const visibleNewChatRoots = newChatRoots.reduce((sum, sel) => sum + visibleCount(sel), 0);
      const hasMessageText = visibleHistoryNodes > 0 && bodyText.length > 0;
      const shellOnly = visibleHistoryNodes === 0 && (visibleNewChatRoots > 0 || /^(new chat|новый чат)/i.test(bodyText));
      const historyReady = !expectHistory || (visibleHistoryNodes >= minVisibleHistoryNodes && hasMessageText);
      const detectionPath = [
        `historyNodes=${visibleHistoryNodes}`,
        `newChatRoots=${visibleNewChatRoots}`,
        `hasMessageText=${hasMessageText}`,
        `activeTitle=${activeTitleMatch}`,
        `shellOnly=${shellOnly}`,
      ];
      return {
        visibleHistoryNodes,
        visibleNewChatRoots,
        hasMessageText,
        shellOnly,
        historyReady,
        activeTitleMatch,
        detectionPath,
        bodyPreview: bodyText.slice(0, 240),
      };
    }, { expectedTitle: expectedChatTitle, expectHistory, minVisibleHistoryNodes }).catch(() => ({ visibleHistoryNodes: 0, visibleNewChatRoots: 0, hasMessageText: false, shellOnly: false, historyReady: false, activeTitleMatch: false, detectionPath: ['state-eval-failed'], bodyPreview: '' })) : { visibleHistoryNodes: 0, visibleNewChatRoots: 0, hasMessageText: false, shellOnly: false, historyReady: false, activeTitleMatch: false, detectionPath: ['composer-not-ready'], bodyPreview: '' };

    const hydrated = composerReady && state.historyReady && !state.shellOnly;
    if (hydrated) {
      if (currentUrl !== lastGoodUrl) {
        stableSince = Date.now();
        lastGoodUrl = currentUrl;
      } else if (stableSince !== null && Date.now() - stableSince >= stableMs) {
        log(`🔒 Follow-up чат готов: ${currentUrl.substring(0, 80)} | ${state.detectionPath.join(' | ')}`);
        return currentUrl;
      }
    } else {
      stableSince = null;
      if (!titleActivationTried && expectedChatTitle && composerReady && Date.now() - started > 1200) {
        titleActivationTried = true;
        log(`ℹ️ Follow-up hydration not ready; title=${expectedChatTitle}, but sidebar title activation is disabled because duplicate titles can misbind chats`);
      }
      if (!hardRebindTried && composerReady && Date.now() - started > Math.max(3000, Math.floor(timeoutMs * 0.4))) {
        hardRebindTried = true;
        log(`♻️ Follow-up hydration still not ready; делаю hard rebind на ${expectedUrl.substring(0, 80)}`);
        await rebindFollowUpChat(page, expectedUrl, 'follow-up-hydration').catch(() => safePageUrl(page));
        await sleep(700);
        continue;
      }
    }

    await sleep(150);
  }
  const finalUrl = safePageUrl(page);
  throw new Error(`Chat continuity preflight failed: ожидался чат ${expectedUrl}, текущий URL ${finalUrl || '(empty)'}`);
}

async function fetchQwenChatMetadata(page, chatId) {
  if (!chatId) return null;
  try {
    return await page.evaluate(async (id) => {
      const res = await fetch(`/api/v2/chats/${id}`, { credentials: 'include' });
      const text = await res.text();
      let json = null;
      try { json = JSON.parse(text); } catch {}
      return { ok: res.ok, status: res.status, json, text: text.slice(0, 1000) };
    }, chatId);
  } catch (e) {
    debugLog(`⚠️ fetchQwenChatMetadata failed: ${e.message}`);
    return null;
  }
}

function extractQwenChatTitle(meta) {
  if (!meta || !meta.ok || !meta.json) return null;
  return meta.json?.title
    || meta.json?.name
    || meta.json?.data?.title
    || meta.json?.data?.name
    || null;
}

async function clickChatItemByTitle(page, title, timeoutMs = 5000) {
  if (!title) return false;
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    const result = await page.evaluate((expectedTitle) => {
      const norm = (s) => (s || '').trim().replace(/\s+/g, ' ');
      const target = norm(expectedTitle);
      const nodes = Array.from(document.querySelectorAll('[aria-label="chat-item"], a, button, [role="button"]'));
      const hit = nodes.find((el) => {
        const txt = norm(el.innerText || el.textContent || '');
        if (!txt) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        if (s.display === 'none' || s.visibility === 'hidden' || r.width <= 0 || r.height <= 0) return false;
        return txt === target || txt.includes(target);
      });
      if (!hit) return { clicked: false };
      hit.scrollIntoView({ block: 'center' });
      hit.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
      hit.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
      hit.click();
      return { clicked: true, text: target };
    }, title).catch(() => ({ clicked: false }));
    if (result.clicked) {
      log(`🧷 Активировал chat-item по заголовку: ${title}`);
      return true;
    }
    await sleep(250);
  }
  return false;
}

async function stabilizeFollowUpChatBinding(page, expectedUrl, options = {}) {
  if (!expectedUrl) return { page, expectedChatTitle: null };
  const expectedChatId = getQwenChatId(expectedUrl);
  log(`🧷 Усиливаю привязку follow-up чата: ${expectedUrl.substring(0, 80)}`);

  if (!sameQwenChat(safePageUrl(page), expectedUrl)) {
    await page.goto(expectedUrl, { waitUntil: 'domcontentloaded', timeout: CONFIG.navigationTimeout });
    await page.waitForFunction(() => document.readyState === 'complete' || document.readyState === 'interactive', {
      timeout: Math.min(CONFIG.navigationTimeout, 5000),
    }).catch(() => {});
  }

  const meta = await fetchQwenChatMetadata(page, expectedChatId);
  const title = extractQwenChatTitle(meta);

  const finalUrl = safePageUrl(page);
  const mismatch = describeContinuityMismatch(expectedUrl, finalUrl);
  if (mismatch) {
    throw new Error(`Chat continuity activation failed: ${mismatch}; expected ${expectedUrl}`);
  }
  log(`🧷 Follow-up чат активирован: ${finalUrl.substring(0, 80)}${title ? ` | title=${title}` : ''}`);
  return { page, expectedChatTitle: title || null };
}

async function assertFollowUpContinuityAfterSubmit(page, expectedUrl, timeoutMs = 1800) {
  if (!expectedUrl) return safePageUrl(page);
  const started = Date.now();
  let lastUrl = safePageUrl(page);
  while (Date.now() - started < timeoutMs) {
    const currentUrl = safePageUrl(page);
    const mismatch = describeContinuityMismatch(expectedUrl, currentUrl);
    if (mismatch) {
      throw new Error(`Chat continuity broken on follow-up submit: ${mismatch}; expected ${expectedUrl}`);
    }
    if (currentUrl) lastUrl = currentUrl;
    await sleep(100);
  }
  log(`🔒 Follow-up continuity OK after submit: ${lastUrl.substring(0, 80)}`);
  return lastUrl;
}

async function submitPromptBoundToComposer(page, composerHandle, options = {}) {
  const { expectedChatUrl = null, strictContinuity = false } = options;

  const submitInfo = await page.evaluate((el) => {
    const isVisible = (node) => {
      if (!node) return false;
      const s = getComputedStyle(node);
      const r = node.getBoundingClientRect();
      return s.visibility !== 'hidden' && s.display !== 'none' && r.width > 0 && r.height > 0;
    };

    const gatherButton = (btn, strategy) => ({
      strategy,
      usesButton: true,
      disabled: !!btn.disabled,
      cls: typeof btn.className === 'string' ? btn.className : '',
      aria: btn.getAttribute('aria-label') || '',
      text: (btn.innerText || btn.textContent || '').trim(),
    });

    const root = el.closest('form, .message-input, .message-input-wrapper, .input-wrap, .chat-input, .input-area, .composer, .footer') || el.parentElement || document.body;
    const candidateGroups = [root, root?.parentElement, el.parentElement, document.body].filter(Boolean);

    for (const group of candidateGroups) {
      const buttons = Array.from(group.querySelectorAll('button, [role="button"]')).filter(isVisible);
      const preferred = buttons.find((btn) => {
        const cls = (typeof btn.className === 'string' ? btn.className : '').toLowerCase();
        const aria = (btn.getAttribute('aria-label') || '').toLowerCase();
        const text = (btn.innerText || btn.textContent || '').trim().toLowerCase();
        return cls.includes('send-button')
          || cls.includes('send')
          || aria.includes('send')
          || aria.includes('отправ')
          || text === 'send'
          || text === 'отправить';
      });
      if (preferred) return gatherButton(preferred, 'nearest-send-button');
    }

    const form = el.closest('form');
    if (form && typeof form.requestSubmit === 'function') {
      return { strategy: 'form-request-submit', usesButton: false };
    }
    if (form) {
      return { strategy: 'form-submit', usesButton: false };
    }
    return { strategy: 'keyboard-enter', usesButton: false };
  }, composerHandle);

  if (submitInfo.usesButton) {
    log(`📨 Submit method: ${submitInfo.strategy}`);
    const clicked = await page.evaluate((el) => {
      const isVisible = (node) => {
        if (!node) return false;
        const s = getComputedStyle(node);
        const r = node.getBoundingClientRect();
        return s.visibility !== 'hidden' && s.display !== 'none' && r.width > 0 && r.height > 0;
      };
      const root = el.closest('form, .message-input, .message-input-wrapper, .input-wrap, .chat-input, .input-area, .composer, .footer') || el.parentElement || document.body;
      const candidateGroups = [root, root?.parentElement, el.parentElement, document.body].filter(Boolean);
      for (const group of candidateGroups) {
        const buttons = Array.from(group.querySelectorAll('button, [role="button"]')).filter(isVisible);
        const preferred = buttons.find((btn) => {
          const cls = (typeof btn.className === 'string' ? btn.className : '').toLowerCase();
          const aria = (btn.getAttribute('aria-label') || '').toLowerCase();
          const text = (btn.innerText || btn.textContent || '').trim().toLowerCase();
          return (cls.includes('send-button') || cls.includes('send') || aria.includes('send') || aria.includes('отправ') || text === 'send' || text === 'отправить') && !btn.disabled;
        });
        if (preferred) {
          preferred.focus?.();
          preferred.click();
          return true;
        }
      }
      return false;
    }, composerHandle).catch(() => false);
    if (!clicked) {
      throw new Error(`Submit button strategy failed: ${submitInfo.strategy}`);
    }
  } else if (submitInfo.strategy === 'form-request-submit') {
    log('📨 Submit method: form-request-submit');
    await page.evaluate((el) => el.closest('form')?.requestSubmit(), composerHandle);
  } else if (submitInfo.strategy === 'form-submit') {
    log('📨 Submit method: form-submit');
    await page.evaluate((el) => el.closest('form')?.submit(), composerHandle);
  } else {
    log('📨 Submit method: composer Enter');
    await composerHandle.focus();
    await page.keyboard.press('Enter');
  }

  if (strictContinuity && expectedChatUrl) {
    await sleep(120);
    await assertFollowUpContinuityAfterSubmit(page, expectedChatUrl, 3000);
    const currentUrl = safePageUrl(page);
    if (!sameQwenChat(expectedChatUrl, currentUrl)) {
      throw new Error(`Chat continuity broken on follow-up submit: current chat ${currentUrl || '(empty)'} != expected ${expectedChatUrl}`);
    }
    const postSubmitComposerGone = await page.evaluate((el) => {
      const isVisible = (node) => {
        if (!node) return false;
        const s = getComputedStyle(node);
        const r = node.getBoundingClientRect();
        return s.visibility !== 'hidden' && s.display !== 'none' && r.width > 0 && r.height > 0;
      };
      if (!el || !document.contains(el)) return true;
      return !isVisible(el);
    }, composerHandle).catch(() => true);
    if (!postSubmitComposerGone) {
      debugLog('ℹ️ Composer still visible immediately after follow-up submit; relying on submit outcome + network/DOM progress checks');
    }
  }

  return submitInfo;
}

async function inspectSubmitOutcome(page, composerSelector, beforeUrl, prompt, timeoutMs = 5000) {
  const started = Date.now();
  let sawExpectedRequest = false;
  while (Date.now() - started < timeoutMs) {
    const network = cdpInterceptor?.consumeResponse ? cdpInterceptor.consumeResponse() : null;
    if (network) sawExpectedRequest = true;
    const snapshot = await page.evaluate((sel, promptStart) => {
      const el = document.querySelector(sel);
      const value = el ? ('value' in el ? el.value : (el.textContent || '')) : '';
      const body = document.body?.innerText || '';
      return {
        valueLen: value.length,
        userPromptVisible: !!(promptStart && body.includes(promptStart)),
        articleCount: document.querySelectorAll('article').length,
        url: location.href,
      };
    }, composerSelector, prompt.slice(0, 40)).catch(() => ({ valueLen: 0, userPromptVisible: false, articleCount: 0, url: safePageUrl(page) }));

    const urlChanged = !!(snapshot.url && beforeUrl && snapshot.url !== beforeUrl);
    const textareaCleared = snapshot.valueLen < Math.max(16, Math.floor(prompt.length * 0.05));
    const accepted = sawExpectedRequest || urlChanged || textareaCleared || snapshot.userPromptVisible || snapshot.articleCount > 0;
    if (accepted) {
      return {
        accepted: true,
        reason: sawExpectedRequest ? 'network-request' : urlChanged ? 'url-changed' : textareaCleared ? 'textarea-cleared' : snapshot.userPromptVisible ? 'prompt-visible' : 'article-visible',
        sawExpectedRequest,
        ...snapshot,
      };
    }
    await sleep(150);
  }

  const finalSnapshot = await page.evaluate((sel, promptStart) => {
    const el = document.querySelector(sel);
    const value = el ? ('value' in el ? el.value : (el.textContent || '')) : '';
    const body = document.body?.innerText || '';
    return {
      valueLen: value.length,
      userPromptVisible: !!(promptStart && body.includes(promptStart)),
      articleCount: document.querySelectorAll('article').length,
      url: location.href,
    };
  }, composerSelector, prompt.slice(0, 40)).catch(() => ({ valueLen: 0, userPromptVisible: false, articleCount: 0, url: safePageUrl(page) }));

  return {
    accepted: false,
    reason: 'silent-submit-block',
    sawExpectedRequest,
    ...finalSnapshot,
  };
}

async function triggerComposerKeySubmit(page, composerSelector, mode = 'enter') {
  const composer = await page.$(composerSelector).catch(() => null);
  if (!composer) return false;
  await composer.focus().catch(() => {});
  await sleep(60);
  if (mode === 'ctrl-enter') {
    log('📨 Fallback submit: composer Ctrl+Enter');
    await page.keyboard.down('Control').catch(() => {});
    await page.keyboard.press('Enter').catch(() => {});
    await page.keyboard.up('Control').catch(() => {});
    return true;
  }
  log('📨 Fallback submit: composer Enter');
  await page.keyboard.press('Enter').catch(() => {});
  return true;
}

function persistSessionState(session, page, reason = 'state-sync', options = {}) {
  if (!session) return;
  const { expectedChatUrl = null, strictContinuity = false } = options;
  try {
    if (browser?.wsEndpoint) session.wsEndpoint = browser.wsEndpoint();
  } catch {}
  const url = safePageUrl(page);
  if (strictContinuity && expectedChatUrl) {
    const mismatch = describeContinuityMismatch(expectedChatUrl, url);
    if (mismatch) {
      log(`🛑 Не сохраняю chatUrl (${reason}): ${mismatch}`);
      saveSession(session.name, session);
      return;
    }
  }
  if (isPersistableQwenChatUrl(url)) {
    if (session.chatUrl !== url) {
      log(`💾 Сохраняю chatUrl (${reason}): ${url.substring(0, 80)}`);
    }
    session.chatUrl = url;
  } else if (url) {
    debugLog(`💾 Пропускаю сохранение chatUrl (${reason}): непостоянный или не-чат URL ${url}`);
  }
  saveSession(session.name, session);
}

async function logUrlTransition(page, beforeUrl, reason, timeoutMs = 5000) {
  const start = Date.now();
  let last = beforeUrl || '';
  while (Date.now() - start < timeoutMs) {
    const now = safePageUrl(page);
    if (now && now !== last) {
      log(`🔗 URL changed (${reason}): ${last || '(empty)'} -> ${now}`);
      return now;
    }
    await sleep(200);
  }
  debugLog(`🔗 URL unchanged after ${reason}: ${beforeUrl || '(empty)'}`);
  return safePageUrl(page);
}

// Input/composer selectors — try the most specific first
const COMPOSER = [
  '#chat-input',
  'textarea#chat-input',
  'textarea[id*="chat-input" i]',
  'textarea[placeholder*="Message" i]',
  'textarea[placeholder*="Send a message" i]',
  'textarea[placeholder*="Ask" i]',
  'textarea[placeholder]',
  'textarea',
  'div[contenteditable="true"]',
  'div[role="textbox"]',
  'div[class*="composer" i]',
];

// Response selectors
const RESPONSE_SELECTORS = [
  'div[class*="markdown-body" i]',
  'div[class*="md-preview" i]',
  'div[class*="message-content" i]',
  'article',
  '.prose',
  '[class*="message"][class*="assistant"]',
  '[class*="message"][class*="ai"]',
];

// API patterns for CDP interception
const API_PATTERNS = [
  '/api/v1/chat/completions',
  '/api/v2/chat/completions',
  '/api/v2/chats',
  '/api/v1/generate',
  '/api/v2/messages',
  '/chat/completions',
  '/generate',
];

// ═══ Session & file management ═══════════════════════════════════════════
const SESSIONS_DIR = path.join(BASE_DIR, '.sessions');
const PROFILE_DIR = path.join(BASE_DIR, '.profile');
const DAEMON_ENDPOINT_FILE = path.join(BASE_DIR, '.daemon-ws-endpoint');
const SESSION_IDX = argv.indexOf('--session');
const sessionName = SESSION_IDX !== -1 ? (argv[SESSION_IDX + 1] || 'default') : null;

const question = FILE_PROMPT_PATH
  ? fs.readFileSync(FILE_PROMPT_PATH, 'utf8').trim()
  : argv.filter(a => !a.startsWith('--') && (SESSION_IDX === -1 || argv.indexOf(a) !== SESSION_IDX + 1)).join(' ');

let browser = null;
let qwenPage = null;
let browserLaunchedByUs = false;
let browserConnectionMode = 'local';
const DAEMON_LOCK_FILE = path.join(BASE_DIR, '.daemon-request.lock');
const RATE_LIMIT_FILE = path.join(BASE_DIR, '.last_prompt_send_time');
let daemonLockHeld = false;

ensureDirSync(SESSIONS_DIR);
ensureDirSync(PROFILE_DIR);

function getSessionFile(name) { return path.join(SESSIONS_DIR, `${name}.json`); }
function loadSession(name) {
  try {
    const f = getSessionFile(name);
    if (fs.existsSync(f)) return JSON.parse(fs.readFileSync(f, 'utf8'));
  } catch {}
  return { name, messageCount: 0, created: null, lastUsed: null, chatUrl: null };
}
function saveSession(name, data) {
  try { fs.writeFileSync(getSessionFile(name), JSON.stringify(data, null, 2)); } catch {}
}
function deleteSession(name) { try { fs.unlinkSync(getSessionFile(name)); } catch {} }

// ═══ Profile lock cleanup ════════════════════════════════════════════════
async function killChromeProfile(profilePath) {
  try {
    const { execSync } = require('child_process');
    const pids = execSync(
      `ps aux | grep -i chrome | grep "${profilePath}" | grep -v grep | awk '{print $2}'`,
      { encoding: 'utf8' }
    ).split('\n').filter(p => p.trim());
    for (const pid of pids) {
      try { process.kill(pid.trim(), 'SIGKILL'); } catch {}
    }
    await sleep(1000);
    try { execSync('rm -rf /dev/shm/.com.google.Chrome.* 2>/dev/null || true'); } catch {}
    try { execSync('rm -rf /tmp/.com.google.Chrome.* 2>/dev/null || true'); } catch {}
  } catch {}
}

async function launchWithTimeout(options, timeoutMs = 30000) {
  const profileDir = options.userDataDir;
  if (profileDir && fs.existsSync(profileDir)) {
    for (const lock of ['SingletonLock', 'SingletonSocket', 'SingletonCookie']) {
      try { fs.unlinkSync(path.join(profileDir, lock)); } catch {}
    }
  }
  log(`🚀 Запуск браузера (timeout: ${timeoutMs}ms)...`);
  const p = puppeteer.launch(options);
  const t = new Promise((_, rj) => setTimeout(() => rj(new Error(`Launch timeout after ${timeoutMs}ms`)), timeoutMs));
  const b = await Promise.race([p, t]);
  log('✅ Браузер запущен');
  return b;
}

async function isBrowserAlive(ws) {
  try {
    const b = await puppeteer.connect({ browserWSEndpoint: ws, timeout: 5000 });
    const pgs = await b.pages();
    await b.disconnect();
    return pgs.length > 0;
  } catch { return false; }
}

async function connectToDaemon() {
  let ws = '';
  if (fs.existsSync(DAEMON_ENDPOINT_FILE)) {
    ws = fs.readFileSync(DAEMON_ENDPOINT_FILE, 'utf8').trim();
  } else {
    try {
      const dp = getSessionFile('daemon');
      if (fs.existsSync(dp)) {
        const ds = JSON.parse(fs.readFileSync(dp, 'utf8'));
        if (ds?.browserWSEndpoint) {
          ws = ds.browserWSEndpoint.trim();
          try { fs.writeFileSync(DAEMON_ENDPOINT_FILE, ws); } catch {}
        }
      }
    } catch {}
  }
  if (!ws) throw new Error('Демон не запущен. Запусти: node qwen-daemon.js');
  log('🔗 Подключаюсь к демону...');
  try {
    const b = await puppeteer.connect({ browserWSEndpoint: ws, defaultViewport: null });
    browserConnectionMode = 'daemon';
    return b;
  } catch (e) {
    try { fs.unlinkSync(DAEMON_ENDPOINT_FILE); } catch {}
    throw withExitCode(new Error(`Демон недоступен: ${e.message}`), 2);
  }
}

async function connectToExisting(session) {
  if (session?.wsEndpoint) {
    try {
      browser = await puppeteer.connect({ browserWSEndpoint: session.wsEndpoint });
      browserConnectionMode = 'session';
      const pgs = await browser.pages();
      qwenPage = pgs.find(p => { try { return p.url().includes('qwen'); } catch { return false; } }) || pgs[0];
      if (qwenPage) { log('🔗 Подключились к существующему браузеру'); return true; }
    } catch { log('⚠️ Не удалось подключиться, запускаю новый'); }
  }
  return false;
}

async function cleanup() {
  try {
    if (browser) {
      if (browserLaunchedByUs) {
        await browser.close().catch(() => {});
      } else {
        try { browser.disconnect(); } catch {}
      }
    }
  } finally {
    if (daemonLockHeld) {
      try { fs.unlinkSync(DAEMON_LOCK_FILE); } catch {}
      daemonLockHeld = false;
    }
    browser = null;
    qwenPage = null;
    browserLaunchedByUs = false;
    browserConnectionMode = 'local';
  }
}

async function acquireDaemonLock(timeoutMs = 120000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const fd = fs.openSync(DAEMON_LOCK_FILE, 'wx');
      fs.writeFileSync(fd, String(process.pid));
      fs.closeSync(fd);
      daemonLockHeld = true;
      return;
    } catch (e) {
      if (e.code !== 'EEXIST') throw e;
      try {
        const stat = fs.statSync(DAEMON_LOCK_FILE);
        if (Date.now() - stat.mtimeMs > timeoutMs) {
          fs.unlinkSync(DAEMON_LOCK_FILE);
          continue;
        }
      } catch {}
      await sleep(250);
    }
  }
  throw new Error('Не удалось получить daemon request lock вовремя');
}

async function ensureActivePage(preferredPage = null) {
  const candidate = preferredPage || qwenPage;
  if (candidate) {
    try {
      if (!candidate.isClosed()) {
        await candidate.title().catch(() => {});
        qwenPage = candidate;
        return candidate;
      }
    } catch {}
  }

  if (!browser) throw new Error('Browser handle is missing');

  const pages = await browser.pages().catch(() => []);
  const livePages = pages.filter((p) => {
    try { return p && !p.isClosed(); } catch { return false; }
  });
  const picked = livePages.find((p) => {
    try {
      const url = p.url();
      return url.includes('qwen') || url === 'about:blank';
    } catch {
      return false;
    }
  }) || livePages[0] || await browser.newPage();

  qwenPage = picked;
  return picked;
}

async function disableAnimations(page) {
  await page.evaluate(() => {
    const s = document.createElement('style');
    s.textContent = '*,*::before,*::after{animation-duration:0s!important;transition-duration:0s!important}';
    document.head.appendChild(s);
  });
}

// ═══ Page ready ══════════════════════════════════════════════════════════
async function waitUntilReady(page, timeout = 45000) {
  const start = Date.now();
  let i = 0;
  while (Date.now() - start < timeout) {
    i++;
    try {
      const url = page.url();
      if (/auth|login|signin|signup/i.test(url)) {
        throw new Error('Требуется авторизация — запусти с --visible --wait');
      }
    } catch (e) {
      if (e.message && e.message.includes('авторизация')) throw e;
    }
    for (const sel of COMPOSER) {
      try {
        const el = await page.$(sel);
        if (el) {
          log(`✅ Composer: ${sel} (${i} checks, ${((Date.now()-start)/1000).toFixed(1)}s)`);
          return sel;
        }
      } catch {}
    }
    await sleep(i <= 3 ? 500 : 1000);
  }
  throw new Error(`Qwen not ready after ${timeout}ms`);
}

// ═══ CDP Interceptor for Qwen API ════════════════════════════════════════
async function setupQwenInterceptor(page) {
  const client = await page.target().createCDPSession();
  await client.send('Network.enable');

  let reqCounter = 0;
  let expectedIds = new Set();
  let windowOpen = false;
  let pendingResolve = null;
  let pendingTimer = null;
  let respState = { resolved: false, result: null };

  function parseQwenBody(raw) {
    if (!raw || typeof raw !== 'string') return { text: null, finished: false };
    const trimmed = raw.trim();
    if (!trimmed) return { text: null, finished: false };

    // Try SSE format
    if (trimmed.includes('data:') || trimmed.includes('event:')) {
      return parseQwenSSE(trimmed);
    }

    // Try JSON
    try {
      const obj = JSON.parse(trimmed);
      if (obj.choices?.[0]?.message?.content) return { text: obj.choices[0].message.content, finished: true };
      if (obj.choices?.[0]?.delta?.content) {
        const finished = obj.choices?.[0]?.delta?.status === 'finished' || obj.choices?.[0]?.finish_reason != null;
        return { text: obj.choices[0].delta.content, finished };
      }
      if (obj.output?.text) return { text: obj.output.text, finished: true };
      if (obj.text) return { text: obj.text, finished: true };
      if (obj.output) return { text: obj.output, finished: true };
      if (obj.data?.chat?.history?.messages) {
        const msgs = obj.data.chat.history.messages;
        if (msgs) {
          const last = Object.values(msgs).find(m => m.role === 'assistant');
          if (last?.content) return { text: last.content, finished: true };
          if (Array.isArray(last?.content_list)) {
            const answer = last.content_list.filter(x => x.phase === 'answer').map(x => x.content || '').join('');
            if (answer) return { text: answer, finished: true };
          }
        }
      }
      return { text: null, finished: false };
    } catch { return { text: null, finished: false }; }
  }

  function parseQwenSSE(raw) {
    let acc = '';
    let finished = false;
    for (const line of raw.split('\n')) {
      if (!line.startsWith('data:') || line.includes('[DONE]')) continue;
      const payload = line.slice(5).trim();
      if (!payload) continue;
      try {
        const obj = JSON.parse(payload);
        const delta = obj.choices?.[0]?.delta;
        const phase = delta?.phase;
        const status = delta?.status;
        const content = delta?.content;
        if (typeof content === 'string' && (phase === 'answer' || !phase)) {
          acc += content;
        }
        if (phase === 'answer' && status === 'finished') finished = true;

        const msg = obj.choices?.[0]?.message?.content;
        if (typeof msg === 'string' && !acc) acc = msg;
        if (obj.output?.text && !acc) acc = obj.output.text;
        if (obj.text && !acc) acc = obj.text;
      } catch {}
    }
    return { text: acc.length > 0 ? acc : null, finished };
  }

  client.on('Network.requestWillBeSent', (ev) => {
    const url = ev.request.url;
    const isCompletion = ev.request.method === 'POST' && /\/api\/v2\/chat\/completions(\?|$)/.test(url);
    if (isCompletion) {
      if (!windowOpen || respState.resolved) return;
      windowOpen = false;
      expectedIds.add(ev.requestId);
      debugLog(`[CDP] caught Qwen completion API: ${ev.requestId} ${url}`);
    }
  });

  client.on('Network.loadingFinished', async (ev) => {
    if (!expectedIds.has(ev.requestId) || respState.resolved) return;
    try {
      const resp = await client.send('Network.getResponseBody', { requestId: ev.requestId });
      let body = resp.body;
      if (resp.base64Encoded) body = Buffer.from(body, 'base64').toString('utf8');
      const parsed = parseQwenBody(body);
      const text = parsed?.text || null;
      debugLog(`[CDP] Body: ${body.length} chars, parsed: ${text ? text.length + ' chars' : 'null'}, finished: ${!!parsed?.finished}`);
      respState.resolved = true;
      respState.result = { raw: body, text, finished: !!parsed?.finished, format: text ? 'parsed' : 'raw' };
      if (pendingResolve) { const r = pendingResolve; pendingResolve = null; if (pendingTimer) clearTimeout(pendingTimer); r(respState.result); }
      expectedIds.delete(ev.requestId);
    } catch (err) {
      debugLog(`[CDP] Error: ${err.message}`);
      if (!respState.resolved) {
        respState.resolved = true;
        respState.result = { raw: null, text: null, format: 'failed', error: err.message };
        if (pendingResolve) { const r = pendingResolve; pendingResolve = null; r(respState.result); }
        expectedIds.delete(ev.requestId);
      }
    }
  });

  client.on('Network.loadingFailed', (ev) => {
    if (!expectedIds.has(ev.requestId) || respState.resolved) return;
    respState.resolved = true;
    respState.result = { raw: null, text: null, format: 'failed', error: 'network_failed' };
    if (pendingResolve) { const r = pendingResolve; pendingResolve = null; r(respState.result); }
    expectedIds.delete(ev.requestId);
  });

  function prepareForRequest() {
    pendingResolve = null;
    if (pendingTimer) clearTimeout(pendingTimer);
    respState = { resolved: false, result: null };
    reqCounter++;
    windowOpen = true;
    debugLog(`[CDP] Ready #${reqCounter}`);
    return reqCounter;
  }

  async function waitForResponse(timeoutMs = 120000) {
    if (respState.resolved && respState.result) {
      return respState.result;
    }
    return new Promise((resolve) => {
      pendingResolve = resolve;
      pendingTimer = setTimeout(() => {
        if (pendingResolve) { pendingResolve = null; resolve(null); }
      }, timeoutMs);
    });
  }

  function consumeResponse() {
    if (!respState.resolved || !respState.result) return null;
    const r = respState.result;
    respState = { resolved: false, result: null };
    pendingResolve = null;
    if (pendingTimer) clearTimeout(pendingTimer);
    pendingTimer = null;
    return r;
  }

  return { prepareForRequest, waitForResponse, consumeResponse };
}

// ═══ Send prompt ═════════════════════════════════════════════════════════
async function sendPrompt(page, composerSelector, prompt, options = {}) {
  const {
    expectedChatUrl = null,
    strictContinuity = false,
    reuseAnswerBaseline = false,
    expectedHistory = true,
  } = options;
  let workingPrompt = prompt;

  for (let attempt = 0; attempt <= OVERSIZE_MAX_RETRIES; attempt++) {
    log(`📝 "${workingPrompt.substring(0, 60)}${workingPrompt.length > 60 ? '...' : ''}"`);

    if (CONFIG.rateLimitMs > 0) {
    let lastSend = 0;
    try {
      if (fs.existsSync(RATE_LIMIT_FILE)) {
        const content = fs.readFileSync(RATE_LIMIT_FILE, 'utf8').trim();
        lastSend = parseInt(content, 10) || 0;
      }
    } catch {}
    const elapsed = Date.now() - lastSend;
    if (lastSend > 0 && elapsed < CONFIG.rateLimitMs) {
      const waitMs = CONFIG.rateLimitMs - elapsed;
      log(`⏳ Rate limit: жду ${waitMs}ms перед отправкой`);
      await sleep(waitMs);
    }
  }

    if (!reuseAnswerBaseline || !Array.isArray(answerBaseline)) {
      answerBaseline = await captureAnswerBaseline(page).catch(() => []);
    }
    if (cdpInterceptor) { cdpInterceptor.prepareForRequest(); }

    const beforeUrl = safePageUrl(page);
    if (strictContinuity && expectedChatUrl) {
      const binding = await stabilizeFollowUpChatBinding(page, expectedChatUrl);
      await waitForFollowUpChatReady(page, composerSelector, expectedChatUrl, {
        timeoutMs: CONFIG.followUpHydrationTimeoutMs,
        stableMs: CONFIG.followUpStableMs,
        expectedChatTitle: binding.expectedChatTitle,
        expectHistory: expectedHistory,
        minVisibleHistoryNodes: CONFIG.followUpMinVisibleHistoryNodes,
      });
    }

    const el = await page.waitForSelector(composerSelector, { visible: true, timeout: 10000 });

    await el.evaluate((el, text) => {
      el.focus();
      if (el.isContentEditable || el.getAttribute('contenteditable') === 'true') {
        el.textContent = text;
        el.dispatchEvent(new Event('input', { bubbles: true }));
      } else if (el instanceof HTMLTextAreaElement || el instanceof HTMLInputElement) {
        const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
        const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
        if (setter) setter.call(el, text); else el.value = text;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
      } else {
        el.textContent = text;
        el.dispatchEvent(new Event('input', { bubbles: true }));
      }
    }, workingPrompt);

    await el.focus();
    await sleep(80);
    const submitInfo = await submitPromptBoundToComposer(page, el, {
      expectedChatUrl,
      strictContinuity,
    });
    if (CONFIG.rateLimitMs > 0) {
      try { fs.writeFileSync(RATE_LIMIT_FILE, String(Date.now())); } catch {}
    }

    let outcome = await inspectSubmitOutcome(page, composerSelector, beforeUrl, workingPrompt, 1400);
    if (!outcome.accepted && submitInfo?.strategy === 'nearest-send-button') {
      log(`⚠️ Button submit produced no observable progress (${outcome.reason}); trying keyboard fallback`);
      const enterTriggered = await triggerComposerKeySubmit(page, composerSelector, 'enter');
      if (enterTriggered) {
        outcome = await inspectSubmitOutcome(page, composerSelector, beforeUrl, workingPrompt, 1400);
      }
      if (!outcome.accepted) {
        const ctrlEnterTriggered = await triggerComposerKeySubmit(page, composerSelector, 'ctrl-enter');
        if (ctrlEnterTriggered) {
          outcome = await inspectSubmitOutcome(page, composerSelector, beforeUrl, workingPrompt, 2200);
        }
      }
    } else if (!outcome.accepted) {
      outcome = await inspectSubmitOutcome(page, composerSelector, beforeUrl, workingPrompt, 3600);
    }

    if (outcome.accepted) {
      const afterUrl = await logUrlTransition(page, beforeUrl, 'submit');
      return { afterUrl, promptUsed: workingPrompt, shortened: attempt > 0, submitOutcome: outcome };
    }

    log(`⚠️ Submit did not actually leave the page (${outcome.reason}); promptLen=${workingPrompt.length}; valueLen=${outcome.valueLen}; url=${outcome.url}`);
    if (attempt >= OVERSIZE_MAX_RETRIES || workingPrompt.length <= OVERSIZE_RETRY_MIN_CHARS) {
      const err = new Error(`QWEN_SUBMIT_BLOCKED_OVERSIZE_PROMPT: silent submit block after ${attempt + 1} attempt(s); final promptLen=${workingPrompt.length}`);
      err.exitCode = 3;
      err.submitOutcome = outcome;
      throw err;
    }
    workingPrompt = shortenPromptForRetry(workingPrompt, attempt + 1);
    log(`✂️ Retry with shortened prompt: newLen=${workingPrompt.length} (attempt ${attempt + 1}/${OVERSIZE_MAX_RETRIES})`);
    await sleep(500);
  }
}

// ═══ Enable web search ═══════════════════════════════════════════════════
async function readSearchModeInfo(page) {
  return page.evaluate(() => {
    const trigger = document.querySelector('[class*="globe" i], button[aria-label*="search" i], [class*="search-toggle" i]');
    if (!trigger) return { exists: false, active: false, text: '', ariaPressed: null, ariaLabel: '' };
    const text = (trigger.innerText || trigger.textContent || '').trim();
    const ariaPressed = trigger.getAttribute('aria-pressed');
    const ariaLabel = trigger.getAttribute('aria-label') || '';
    const cls = typeof trigger.className === 'string' ? trigger.className : '';
    const active = ariaPressed === 'true'
      || /active|selected|enabled|checked|on/i.test(cls)
      || /search on|disable search|web search on/i.test(`${text} ${ariaLabel}`);
    return { exists: true, active, text, ariaPressed, ariaLabel };
  }).catch(() => ({ exists: false, active: false, text: '', ariaPressed: null, ariaLabel: '' }));
}

async function enableWebSearch(page) {
  const before = await readSearchModeInfo(page);
  if (!before.exists) {
    log('⚠️ Переключатель Web Search не найден');
    return false;
  }
  if (before.active) {
    log('🔍 Web Search уже активен');
    return true;
  }

  log('🔍 Активирую Web Search...');
  await page.evaluate(() => {
    const btn = document.querySelector('[class*="globe" i], button[aria-label*="search" i], [class*="search-toggle" i]');
    if (btn && btn.offsetWidth > 0 && !btn.disabled) btn.click();
  }).catch(() => {});

  const verified = await page.waitForFunction(() => {
    const trigger = document.querySelector('[class*="globe" i], button[aria-label*="search" i], [class*="search-toggle" i]');
    if (!trigger) return false;
    const text = (trigger.innerText || trigger.textContent || '').trim();
    const ariaPressed = trigger.getAttribute('aria-pressed');
    const ariaLabel = trigger.getAttribute('aria-label') || '';
    const cls = typeof trigger.className === 'string' ? trigger.className : '';
    return ariaPressed === 'true'
      || /active|selected|enabled|checked|on/i.test(cls)
      || /search on|disable search|web search on/i.test(`${text} ${ariaLabel}`);
  }, { timeout: 1800 }).then(() => true).catch(() => false);

  if (verified) {
    log('🔍 Web Search включён');
    return true;
  }

  log('⚠️ Не удалось подтвердить включение Web Search');
  return false;
}

// ═══ Force preferred model ═══════════════════════════════════════════════
async function ensurePreferredModel(page, desiredModel = PREFERRED_MODEL) {
  const desired = String(desiredModel || '').trim();
  if (!desired) return false;

  const normalize = (s) => String(s || '').trim().replace(/\s+/g, ' ');
  const matchesDesired = (s) => normalize(s).toLowerCase() === desired.toLowerCase();

  const readCurrentModel = async () => page.evaluate(() => {
    const normalize = (s) => String(s || '').trim().replace(/\s+/g, ' ');
    const isVisible = (el) => {
      if (!el) return false;
      const s = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0;
    };
    const direct = Array.from(document.querySelectorAll('.header-left .ant-dropdown-trigger, .header-content .ant-dropdown-trigger, header .ant-dropdown-trigger')).find((el) => {
      if (!isVisible(el)) return false;
      const text = normalize(el.innerText || el.textContent || '');
      return /qwen\d/i.test(text);
    });
    if (direct) return normalize(direct.innerText || direct.textContent || '');

    const roots = Array.from(document.querySelectorAll('.header-left, header, .header-content')).filter(isVisible);
    const candidates = [];
    for (const root of roots) {
      const nodes = Array.from(root.querySelectorAll('[class*="model-selector-text" i], .ant-dropdown-trigger, [class*="model-selector" i], span, div')).filter(isVisible);
      for (const el of nodes) {
        const text = normalize(el.innerText || el.textContent || '');
        if (!text || !/qwen\d/i.test(text)) continue;
        const cls = typeof el.className === 'string' ? el.className : '';
        candidates.push({ text, cls, len: text.length });
      }
    }
    candidates.sort((a, b) => a.len - b.len);
    return candidates[0]?.text || '';
  }).catch(() => '');

  const openModelSelector = async () => {
    const openedByDomClick = await page.evaluate(() => {
      const normalize = (s) => String(s || '').trim().replace(/\s+/g, ' ');
      const isVisible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0;
      };

      const direct = Array.from(document.querySelectorAll('.header-left .ant-dropdown-trigger, .header-content .ant-dropdown-trigger, header .ant-dropdown-trigger')).find((el) => {
        if (!isVisible(el)) return false;
        const text = normalize(el.innerText || el.textContent || '');
        return /qwen\d/i.test(text);
      });

      const fallbackText = Array.from(document.querySelectorAll('.header-left [class*="model-selector-text" i], .header-content [class*="model-selector-text" i], header [class*="model-selector-text" i]')).find((el) => {
        if (!isVisible(el)) return false;
        const text = normalize(el.innerText || el.textContent || '');
        return /qwen\d/i.test(text);
      });

      const target = direct || fallbackText?.closest('.ant-dropdown-trigger') || fallbackText || null;
      if (!target) return false;
      target.scrollIntoView({ block: 'center', inline: 'center' });
      target.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
      target.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
      target.click();
      return true;
    }).catch(() => false);

    if (!openedByDomClick) {
      const info = await page.evaluate(() => {
        const normalize = (s) => String(s || '').trim().replace(/\s+/g, ' ');
        const isVisible = (el) => {
          if (!el) return false;
          const s = getComputedStyle(el);
          const r = el.getBoundingClientRect();
          return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0;
        };
        const direct = Array.from(document.querySelectorAll('.header-left .ant-dropdown-trigger, .header-content .ant-dropdown-trigger, header .ant-dropdown-trigger')).find((el) => {
          if (!isVisible(el)) return false;
          const text = normalize(el.innerText || el.textContent || '');
          return /qwen\d/i.test(text);
        });
        if (!direct) return null;
        const r = direct.getBoundingClientRect();
        return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
      }).catch(() => null);

      if (!info) {
        log('⚠️ Не удалось найти селектор модели');
        return false;
      }

      try {
        await page.mouse.move(info.x, info.y);
        await page.mouse.down();
        await sleep(80);
        await page.mouse.up();
      } catch {
        return false;
      }
    }

    return await page.waitForFunction(() => {
      const isVisible = (el) => {
        if (!el) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0;
      };
      return Array.from(document.querySelectorAll('body *')).some((el) => {
        if (!isVisible(el)) return false;
        const text = (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ');
        const cls = typeof el.className === 'string' ? el.className : '';
        return /qwen3\.6-(plus|max-preview|27b)/i.test(text) && /model-item|model-list|model-selector-popup/i.test(cls);
      });
    }, { timeout: 2000 }).then(() => true).catch(() => false);
  };

  const currentModel = normalize(await readCurrentModel());
  if (matchesDesired(currentModel)) {
    log(`🧠 Модель уже установлена: ${currentModel}`);
    return true;
  }

  log(`🧠 Переключаю модель: ${currentModel || 'unknown'} -> ${desired}`);

  const opened = await openModelSelector();
  if (!opened) {
    log('⚠️ Не удалось раскрыть селектор модели');
    return false;
  }

  const picked = await page.evaluate((desiredModel) => {
    const normalize = (s) => String(s || '').trim().replace(/\s+/g, ' ');
    const desired = normalize(desiredModel).toLowerCase();
    const isVisible = (el) => {
      if (!el) return false;
      const s = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0;
    };

    const nodes = Array.from(document.querySelectorAll('body *')).filter(isVisible);
    const modelItems = nodes.filter((el) => {
      const text = normalize(el.innerText || el.textContent || '');
      const cls = typeof el.className === 'string' ? el.className : '';
      return text && text.toLowerCase().includes(desired) && (/model-item|model-list|model-selector-popup/i.test(cls) || /qwen3\.6-/i.test(text));
    });

    const target = modelItems.map((el) => el.closest('[class*="model-item" i]') || el).find(Boolean);
    if (!target) return { ok: false, reason: 'no-model-option' };

    const r = target.getBoundingClientRect();
    target.scrollIntoView({ block: 'center' });
    target.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, clientX: r.x + r.width / 2, clientY: r.y + r.height / 2 }));
    target.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, clientX: r.x + r.width / 2, clientY: r.y + r.height / 2 }));
    target.click();
    return { ok: true, text: normalize(target.innerText || target.textContent || '') };
  }, desired).catch((e) => ({ ok: false, reason: e.message }));

  if (!picked?.ok) {
    log(`⚠️ Не удалось выбрать модель ${desired}: ${picked?.reason || 'unknown'}`);
    return false;
  }

  const confirmed = await page.waitForFunction((desiredModel) => {
    const normalize = (s) => String(s || '').trim().replace(/\s+/g, ' ');
    const desired = normalize(desiredModel).toLowerCase();
    const isVisible = (el) => {
      if (!el) return false;
      const s = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0;
    };
    const roots = Array.from(document.querySelectorAll('.header-left, header, .header-content')).filter(isVisible);
    return roots.some((root) => Array.from(root.querySelectorAll('[class*="model-selector-text" i], .ant-dropdown-trigger, [class*="model-selector" i], span, div')).some((el) => {
      if (!isVisible(el)) return false;
      const text = normalize(el.innerText || el.textContent || '');
      return text.toLowerCase() === desired;
    }));
  }, { timeout: 2500 }, desired).then(() => true).catch(() => false);

  const finalModel = normalize(await readCurrentModel());
  if (confirmed || matchesDesired(finalModel)) {
    log(`🧠 Модель установлена: ${finalModel || desired}`);
    return true;
  }

  log(`⚠️ Не удалось подтвердить модель ${desired} (после переключения: ${finalModel || 'unknown'})`);
  return false;
}

// ═══ Force thinking mode ═════════════════════════════════════════════════
async function ensureThinkingMode(page) {
  const readModeInfo = async () => {
    return page.evaluate(() => {
      const label = document.querySelector('.qwen-thinking-selector .qwen-select-thinking-label-text');
      const input = document.querySelector('.qwen-thinking-selector input[role="combobox"]');
      const trigger = document.querySelector('.qwen-thinking-selector .ant-select-selector, .qwen-thinking-selector');
      const rect = trigger ? trigger.getBoundingClientRect() : null;
      return {
        exists: !!label,
        current: label ? (label.textContent || '').trim() : '',
        expanded: input ? input.getAttribute('aria-expanded') : null,
        rect: rect ? { x: rect.x, y: rect.y, w: rect.width, h: rect.height } : null,
      };
    }).catch(() => ({ exists: false, current: '', expanded: null, rect: null }));
  };

  const confirmThinkingMode = async (timeoutMs = 2000) => {
    const ok = await page.waitForFunction(() => {
      const label = document.querySelector('.qwen-thinking-selector .qwen-select-thinking-label-text');
      const text = label ? (label.textContent || '').trim() : '';
      return /мышление|размыш|мышлен|think|reason/i.test(text);
    }, { timeout: timeoutMs }).then(() => true).catch(() => false);
    return ok;
  };

  const modeInfo = await readModeInfo();
  if (!modeInfo.exists) {
    log('⚠️ Переключатель режима не найден — пропускаю выбор thinking');
    return false;
  }

  if (/размыш|мышлен|think|reason/i.test(modeInfo.current)) {
    log(`🧠 Режим уже установлен: ${modeInfo.current}`);
    return true;
  }

  log(`🧠 Переключаю режим: ${modeInfo.current || 'unknown'} -> thinking`);

  let opened = false;
  if (modeInfo.rect) {
    const x = modeInfo.rect.x + modeInfo.rect.w / 2;
    const y = modeInfo.rect.y + modeInfo.rect.h / 2;
    try {
      await page.mouse.move(x, y);
      await page.mouse.down();
      await sleep(80);
      await page.mouse.up();
      await sleep(250);
      const probe = await readModeInfo();
      opened = probe.expanded === 'true';
    } catch {}
  }

  const triggerSelectors = [
    '.qwen-thinking-selector .ant-select-selector',
    '.qwen-thinking-selector .qwen-select-thinking-label',
    '.qwen-thinking-selector input[role="combobox"]',
    '.qwen-thinking-selector',
  ];

  if (!opened) {
    for (const selector of triggerSelectors) {
      const handle = await page.$(selector).catch(() => null);
      if (!handle) continue;
      try {
        await handle.click({ delay: 50 });
        await sleep(200);
      } catch {}
      const probe = await readModeInfo();
      if (probe.expanded === 'true') {
        opened = true;
        break;
      }
    }
  }

  if (!opened) {
    try {
      const handle = await page.$('.qwen-thinking-selector input[role="combobox"], .qwen-thinking-selector .ant-select-selector, .qwen-thinking-selector').catch(() => null);
      if (handle) {
        await handle.focus().catch(() => {});
        await page.keyboard.press('Enter').catch(() => {});
        await sleep(180);
        const probe = await readModeInfo();
        opened = probe.expanded === 'true';
      }
    } catch {}
  }

  if (!opened) {
    log('⚠️ Не удалось раскрыть селектор режима');
    return false;
  }

  const pickedByText = await page.evaluate(() => {
    const matcher = /^(мышление|thinking)$/i;
    const fallbackMatcher = /(мышление|размыш|мышлен|think|thinking|reason)/i;
    const candidates = Array.from(document.querySelectorAll('[role="option"], .ant-select-item-option, .ant-select-dropdown .ant-select-item, .ant-select-dropdown li, .ant-select-dropdown div'));
    const visible = candidates.filter((el) => {
      const text = (el.innerText || el.textContent || '').trim();
      if (!text) return false;
      const s = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      return !(s.visibility === 'hidden' || s.display === 'none' || r.width <= 0 || r.height <= 0);
    });
    const option = visible.find((el) => matcher.test((el.innerText || el.textContent || '').trim()))
      || visible.find((el) => fallbackMatcher.test((el.innerText || el.textContent || '').trim()));
    if (!option) {
      return {
        ok: false,
        reason: 'no-thinking-option',
        visibleTexts: visible.slice(0, 20).map((el) => (el.innerText || el.textContent || '').trim()),
      };
    }
    const r = option.getBoundingClientRect();
    return {
      ok: true,
      text: (option.innerText || option.textContent || '').trim(),
      rect: { x: r.x, y: r.y, w: r.width, h: r.height },
    };
  }).catch((e) => ({ ok: false, reason: e.message }));

  if (pickedByText.ok && pickedByText.rect) {
    try {
      const x = pickedByText.rect.x + pickedByText.rect.w / 2;
      const y = pickedByText.rect.y + pickedByText.rect.h / 2;
      await page.mouse.move(x, y);
      await page.mouse.down();
      await sleep(60);
      await page.mouse.up();
      await sleep(350);
    } catch {}
  }

  if (!pickedByText.ok) {
    for (let i = 0; i < 6; i++) {
      await page.keyboard.press('ArrowDown').catch(() => {});
      await sleep(120);
      const probe = await readModeInfo();
      if (/мышление|размыш|мышлен|think|reason/i.test(probe.current)) {
        log(`🧠 Режим мышления включён: ${probe.current}`);
        return true;
      }
      await page.keyboard.press('Enter').catch(() => {});
      await sleep(250);
      const afterEnter = await readModeInfo();
      if (/мышление|размыш|мышлен|think|reason/i.test(afterEnter.current)) {
        log(`🧠 Режим мышления включён: ${afterEnter.current}`);
        return true;
      }
    }
  }

  const confirmed = await confirmThinkingMode(2200);
  const finalLabel = await page.evaluate(() => {
    const label = document.querySelector('.qwen-thinking-selector .qwen-select-thinking-label-text');
    return label ? (label.textContent || '').trim() : '';
  }).catch(() => '');

  if (confirmed || /мышление|размыш|мышлен|think|reason/i.test(finalLabel)) {
    try {
      await page.keyboard.press('Escape').catch(() => {});
      await sleep(120);
      await page.click('body').catch(() => {});
      await sleep(120);
    } catch {}
    log(`🧠 Режим мышления включён: ${finalLabel || 'thinking'}`);
    return true;
  }

  log(`⚠️ Не удалось подтвердить thinking mode (после переключения: ${finalLabel || pickedByText.reason || 'unknown'})`);
  return false;
}

// ═══ New chat ════════════════════════════════════════════════════════════
async function startNewChat(page, force = false) {
  page = await ensureActivePage(page);
  log('🆕 Начинаю новый чат...');
  try {
    const url = page.url();
    if (QWEN_CHAT_RE.test(url) && !newChat && !force) {
      log('🆕 Уже в чате — продолжаем');
      return page;
    }
  } catch {}

  let clicked = null;
  try {
    clicked = await page.evaluate(() => {
      const candidates = document.querySelectorAll('button, [role="button"], a, i');
      for (const el of candidates) {
        const text = (el.textContent || el.innerText || '').trim().toLowerCase();
        const aria = (el.getAttribute('aria-label') || '').toLowerCase();
        const cls = (el.className || '').toLowerCase();
        if (el.offsetWidth > 0 && (
          text.includes('new chat') || text.includes('новый чат') || text.includes('новый') ||
          aria.includes('new chat') || cls.includes('new-chat') || cls.includes('sidebar-new') ||
          cls.includes('plus') || cls.includes('icon-line-plus')
        )) {
          el.click();
          return text || aria || cls;
        }
      }
      return null;
    });
  } catch (e) {
    if (/detached|Target closed|Execution context was destroyed/i.test(String(e?.message || ''))) {
      page = await ensureActivePage();
    } else {
      throw e;
    }
  }

  if (clicked) {
    log(`🆕 New chat: "${clicked}"`);
    await sleep(1500);
    page = await ensureActivePage(page);
    try { log(`🆕 URL after new-chat click: ${safePageUrl(page).substring(0, 80)}`); } catch {}
    return page;
  }

  log('📍 Переход на главную Qwen...');
  page = await ensureActivePage(page);
  try {
    await page.goto(QWEN_URL, { waitUntil: 'domcontentloaded', timeout: CONFIG.navigationTimeout });
  } catch (e) {
    const msg = String(e?.message || '');
    if (/ERR_ABORTED|detached|Target closed|Execution context was destroyed/i.test(msg)) {
      log('⚠️ Навигация была прервана или страница перепривязана; пробую восстановить handle');
      page = await ensureActivePage();
    } else {
      throw e;
    }
  }
  await sleep(1500);
  page = await ensureActivePage(page);
  try { log(`🆕 URL after new-chat navigation: ${safePageUrl(page).substring(0, 80)}`); } catch {}
  return page;
}

// ═══ Extract answer from DOM ═════════════════════════════════════════════
async function captureAnswerBaseline(page) {
  return page.evaluate(() => {
    const selectors = [
      'div[class*="markdown-body"]',
      'div[class*="md-preview"]',
      'div[class*="message-content"]',
      'article',
      '.prose',
    ];
    const out = [];
    for (const sel of selectors) {
      const els = Array.from(document.querySelectorAll(sel));
      for (const el of els) {
        if (el.closest('.sidebar, nav, aside, .history')) continue;
        if (el.closest('textarea, [contenteditable], [role="textbox"]')) continue;
        const txt = el.innerText?.trim();
        if (txt) out.push(txt.slice(0, 15000));
      }
    }
    return out;
  }).catch(() => []);
}

async function extractAnswerFromDOM(page, minLen = 50, baseline = null) {
  return page.evaluate(({ minLen, baseline }) => {
    const selectors = [
      'div[class*="markdown-body"]',
      'div[class*="md-preview"]',
      'div[class*="message-content"]',
      'article',
      '.prose',
    ];
    const baselineSet = new Set(Array.isArray(baseline) ? baseline : []);
    const candidates = [];
    for (const sel of selectors) {
      const els = Array.from(document.querySelectorAll(sel));
      for (const el of els) {
        if (el.closest('.sidebar, nav, aside, .history')) continue;
        if (el.closest('textarea, [contenteditable], [role="textbox"]')) continue;
        const txt = el.innerText?.trim();
        if (!txt) continue;
        const clipped = txt.slice(0, 15000);
        candidates.push(clipped);
      }
    }
    for (let i = candidates.length - 1; i >= 0; i--) {
      const txt = candidates[i];
      if (txt.length < minLen) continue;
      if (baselineSet.has(txt)) continue;
      return txt;
    }
    return null;
  }, { minLen, baseline }).catch(() => null);
}

// ═══ Wait for response ═══════════════════════════════════════════════════
async function waitForAnswer(page, timeout = TIMEOUT_ANSWER) {
  const start = Date.now();
  let idleSince = null;
  let lastText = '';
  let continueClicks = 0;

  async function clickContinueIfPresent() {
    const clicked = await page.evaluate(() => {
      const matcher = /^(continue|continue generating|продолжить|продолжить генерацию|далее|read more|show more|more)$/i;
      const rejectMatcher = /^(новый чат|new chat|projects|проекты|community|сообщество)$/i;
      const all = Array.from(document.querySelectorAll('button, [role="button"], a[role="button"]'));
      const btn = all.find((el) => {
        const text = (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ');
        if (!text) return false;
        if (rejectMatcher.test(text)) return false;
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        if (s.visibility === 'hidden' || s.display === 'none' || r.width <= 0 || r.height <= 0) return false;
        return matcher.test(text);
      });
      if (!btn) return { clicked: false };
      const text = (btn.innerText || btn.textContent || '').trim().replace(/\s+/g, ' ');
      const r = btn.getBoundingClientRect();
      btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, clientX: r.x + r.width / 2, clientY: r.y + r.height / 2 }));
      btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, clientX: r.x + r.width / 2, clientY: r.y + r.height / 2 }));
      btn.click();
      return { clicked: true, text };
    }).catch(() => ({ clicked: false }));
    return clicked;
  }

  while (Date.now() - start < timeout) {
    let networkFinished = false;
    try {
      if (cdpInterceptor) {
        let network = cdpInterceptor.consumeResponse ? cdpInterceptor.consumeResponse() : null;
        if (!network) {
          network = await cdpInterceptor.waitForResponse(250).catch(() => null);
          if (network && cdpInterceptor.consumeResponse) {
            const consumed = cdpInterceptor.consumeResponse();
            if (consumed) network = consumed;
          }
        }
        if (network?.text && network.text.length > lastText.length) {
          lastText = network.text;
          idleSince = null;
          debugLog(`🌐 Ответ из сети: ${lastText.length} символов`);
        }
        networkFinished = !!network?.finished;
      }
    } catch (e) { debugLog('Network check error:', e.message); }

    // DOM-based check
    try {
      const text = await extractAnswerFromDOM(page, MIN_RESPONSE, answerBaseline);
      if (text && text.length > lastText.length) {
        lastText = text;
        idleSince = null;
        debugLog(`📝 Ответ: ${lastText.length} символов`);
      }

      const continueBtn = await clickContinueIfPresent();
      if (continueBtn.clicked) {
        continueClicks += 1;
        log(`🔁 Continue clicked (${continueClicks}): ${continueBtn.text}`);
        idleSince = null;
        await sleep(2000);
        continue;
      }

      if (lastText.length > 0) {
        if (networkFinished) {
          if (cdpInterceptor?.consumeResponse) cdpInterceptor.consumeResponse();
          debugLog(`✅ Ответ готов по сети: ${lastText.length} символов`);
          return { text: lastText, source: 'network', complete: true, continueClicks };
        }

        if (idleSince === null) {
          idleSince = Date.now();
        } else if (Date.now() - idleSince > CONFIG.shortAnswerStableMs) {
          const isGenerating = await page.evaluate(() => {
            const hasVisible = (selectors) => selectors.some((sel) => {
              const nodes = Array.from(document.querySelectorAll(sel));
              return nodes.some((el) => {
                const s = getComputedStyle(el);
                const r = el.getBoundingClientRect();
                return s.visibility !== 'hidden' && s.display !== 'none' && r.width > 0 && r.height > 0;
              });
            });

            const bodyText = document.body?.innerText || '';
            return !!(
              hasVisible([
                '[class*="stop" i]',
                'button[aria-label*="stop" i]',
                '[class*="loading" i]',
                'i[class*="Stop" i]',
                'i[class*="loading" i]',
                '[class*="generating" i]',
                '[data-testid*="stop" i]'
              ]) ||
              bodyText.includes('The chat is in progress!')
            );
          }).catch(() => false);

          if (!isGenerating) {
            if (cdpInterceptor?.consumeResponse) cdpInterceptor.consumeResponse();
            debugLog(`✅ Ответ готов: ${lastText.length} символов`);
            return { text: lastText, source: lastText.length >= MIN_RESPONSE ? 'dom' : 'network', complete: true, continueClicks };
          } else {
            idleSince = null;
          }
        }
      }
    } catch (e) { debugLog('DOM check error:', e.message); }

    await sleep(500);
  }

  if (cdpInterceptor?.consumeResponse) cdpInterceptor.consumeResponse();
  log('⏰ Таймаут ожидания ответа');
  return { text: lastText || null, source: lastText.length >= MIN_RESPONSE ? 'dom' : 'network', complete: false, continueClicks };
}

// ═══ Ensure browser ══════════════════════════════════════════════════════
async function ensureBrowser(session) {
  if (browser && qwenPage) {
    try { await qwenPage.url(); return qwenPage; }
    catch (e) { browser = null; qwenPage = null; }
  }

  // Try daemon only when explicitly requested.
  if (useDaemon) {
    try {
      await acquireDaemonLock();
      browser = await connectToDaemon();
      const pages = await browser.pages().catch(() => []);
      const livePages = pages.filter((p) => {
        try { return p && !p.isClosed(); } catch { return false; }
      });
      qwenPage = ((session?.chatUrl && !newChat)
        ? livePages.find((p) => {
            try { return p.url() === session.chatUrl; } catch { return false; }
          })
        : null) || livePages.find((p) => {
          try { return p.url().includes('qwen'); } catch { return false; }
        }) || livePages[0];
      debugLog(`🔍 Daemon live pages: ${livePages.map((p) => { try { return p.url(); } catch { return '(unreadable)'; } }).join(' | ')}`);
      if (!qwenPage) {
        qwenPage = await browser.newPage();
      }
      try {
        await qwenPage.setViewport({ width: 1280, height: 800 });
      } catch {}

      const restoreUrl = session?.chatUrl && !newChat ? session.chatUrl : QWEN_URL;
      if (session?.chatUrl && !newChat) {
        log(`📂 Восстанавливаю чат в daemon page: ${session.chatUrl.substring(0, 60)}`);
      } else {
        log('📍 Навигация на Qwen Chat...');
      }
      await qwenPage.goto(restoreUrl, { waitUntil: 'domcontentloaded', timeout: 20000 });
      log(`🔗 Подключился к демону (singleton page URL: ${qwenPage.url().substring(0, 50)})`);
      return qwenPage;
    } catch (e) {
      if (e?.exitCode) throw e;
      throw withExitCode(new Error(`Демон недоступен: ${e.message}`), 2);
    }
  }

  // Try existing session
  if (session && await connectToExisting(session)) {
    return qwenPage;
  }

  // Launch new local browser.
  // Safety rule: local mode and daemon mode currently share the same Chromium profile.
  // Running a local browser while daemon owns that profile can disconnect the daemon browser.
  if (!useDaemon && fs.existsSync(DAEMON_ENDPOINT_FILE)) {
    const daemonWs = fs.readFileSync(DAEMON_ENDPOINT_FILE, 'utf8').trim();
    if (daemonWs) {
      const daemonAlive = await isBrowserAlive(daemonWs).catch(() => false);
      if (daemonAlive) {
        throw new Error('Локальный режим недоступен, пока активен qwen-daemon: общий Chromium profile может убить daemon-сессию. Используй --daemon или сначала останови qwen-daemon.');
      }
      try { fs.unlinkSync(DAEMON_ENDPOINT_FILE); } catch {}
    }
  }

  await cleanup();
  if (!session && shouldClose) await killChromeProfile(PROFILE_DIR);

  const launchOptions = {
    headless: isVisible ? false : 'new',
    userDataDir: PROFILE_DIR,
    args: [
      '--no-sandbox', '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--no-first-run', '--no-default-browser-check',
      '--disable-gpu', '--window-size=1280,800',
    ],
  };
  if (executablePath) launchOptions.executablePath = executablePath;

  browser = await launchWithTimeout(launchOptions, TIMEOUT_BROWSER);
  browserLaunchedByUs = true;
  browserConnectionMode = 'local';

  const pages = await browser.pages();
  qwenPage = pages[0] || await browser.newPage();
  await qwenPage.setUserAgent(
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
  );
  await qwenPage.setViewport({ width: 1280, height: 800 });
  await qwenPage.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => false });
  });

  if (session?.chatUrl && !newChat) {
    log(`📂 Открываю чат: ${session.chatUrl.substring(0, 60)}`);
    await qwenPage.goto(session.chatUrl, { waitUntil: 'domcontentloaded', timeout: CONFIG.navigationTimeout });
  } else {
    log('📍 Открываем Qwen Chat...');
    await qwenPage.goto(QWEN_URL, { waitUntil: 'domcontentloaded', timeout: CONFIG.navigationTimeout });
  }

  await disableAnimations(qwenPage);
  await sleep(150);

  if (isVisible && waitForAuth) {
    log('\n⚠️ Авторизуйтесь в Qwen и нажмите Enter...');
    if (process.stdin.isTTY) {
      await new Promise(r => { process.stdin.resume(); process.stdin.once('data', () => r()); });
    } else {
      await sleep(60000);
    }
  }

  if (session) {
    persistSessionState(session, qwenPage, 'ensureBrowser');
  }

  return qwenPage;
}

// ═══ MAIN ════════════════════════════════════════════════════════════════
async function main() {
  let diag = null;

  try {
    // End session
    if (endSession && sessionName) {
      deleteSession(sessionName);
      console.log(`Сессия '${sessionName}' завершена`);
      return;
    }

    if (!question && !dryRun) {
      console.error('Ошибка: нужен вопрос. ask-qwen.sh "вопрос"');
      process.exit(1);
    }

    diag = new Diagnostics({
      traceId: `tr-qwen-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
      sessionName,
      promptPreview: question?.substring(0, 80) || '',
      logDir: path.join(BASE_DIR, '.diagnostics'),
    });
    diag.start('INIT');

    // Determine session
    let session = null;
    if (sessionName) {
      const isNew = !fs.existsSync(getSessionFile(sessionName));
      session = loadSession(sessionName);
      if (isNew) {
        session.created = new Date().toISOString();
        session.name = sessionName;
      }
      session.lastUsed = new Date().toISOString();
      saveSession(session.name, session);
    }
    const expectedFollowUpChatUrl = (session && session.chatUrl && !newChat) ? session.chatUrl : null;
    const strictFollowUpContinuity = !!expectedFollowUpChatUrl;

    // Ensure browser
    if (diag) diag.start('BROWSER_LAUNCH');
    let page = await ensureBrowser(session);
    if (diag) diag.succeed('BROWSER_LAUNCH');

    // New chat? Force a fresh chat for standalone requests so previous in-progress chats do not poison extraction.
    if (!session) {
      page = await startNewChat(page, true);
    } else if (newChat || !session.chatUrl) {
      page = await startNewChat(page);
    }

    // Wait for page ready
    if (diag) diag.start('COMPOSER_WAIT');
    const composerSel = await waitUntilReady(page);
    if (diag) diag.succeed('COMPOSER_WAIT', { selector: composerSel });

    // Auth check
    if (diag) diag.start('AUTH_CHECK');
    const authOk = await requireAuth(page, null, log);
    if (!authOk) {
      if (diag) diag.fail('AUTH_CHECK', 'Not authenticated');
      console.error('❌ Требуется авторизация в Qwen Chat');
      console.error('Запусти с --visible --wait для ручной авторизации');
      process.exit(1);
    }
    if (diag) diag.succeed('AUTH_CHECK');

    // Configure CDP interceptor before any prompt send.
    cdpInterceptor = await setupQwenInterceptor(page);

    // Dry run
    if (dryRun) {
      log('\n✅ Dry run успешен — Qwen Chat авторизован и готов');
      await cleanup();
      return;
    }

    // Force preferred model + thinking mode before every prompt
    await ensurePreferredModel(page);
    await ensureThinkingMode(page);

    // Enable search
    if (doSearch) await enableWebSearch(page);

    const fullQuestion = question.startsWith('[Дата:') ? question : `[Дата: ${new Date().toLocaleString('ru-RU', { timeZone: 'Asia/Irkutsk' })}]\n\n${question}`;

    // Send prompt
    const reuseAnswerBaseline = !!(session && session.messageCount > 0 && strictFollowUpContinuity && Array.isArray(answerBaseline));
    if (diag) diag.start('PROMPT_SEND');
    const sendMeta = await sendPrompt(page, composerSel, fullQuestion, {
      expectedChatUrl: expectedFollowUpChatUrl,
      strictContinuity: strictFollowUpContinuity,
      reuseAnswerBaseline,
    });
    if (session) {
      persistSessionState(session, page, 'post-submit', {
        expectedChatUrl: expectedFollowUpChatUrl,
        strictContinuity: strictFollowUpContinuity,
      });
    }
    if (diag) diag.succeed('PROMPT_SEND', { promptLength: fullQuestion.length, promptUsedLength: sendMeta?.promptUsed?.length || fullQuestion.length, shortened: !!sendMeta?.shortened, submitReason: sendMeta?.submitOutcome?.reason || null });

    // Wait for response
    if (diag) diag.start('ANSWER_WAIT');
    const result = await waitForAnswer(page);
    if (diag) {
      diag.answerComplete = !!result?.complete;
      diag.incompleteReason = result?.complete ? null : 'не полный';
      diag.charactersExtracted = result?.text?.length || 0;
      diag.continueRounds = result?.continueClicks || 0;
      diag.succeed('ANSWER_WAIT', { chars: result?.text?.length || 0, complete: !!result?.complete, continueClicks: result?.continueClicks || 0 });
    }

    // Extract from DOM as fallback
    if (!result?.text && !result?.complete) {
      if (diag) diag.start('ANSWER_EXTRACT');
      const domText = await extractAnswerFromDOM(page, 20, answerBaseline);
      if (domText) {
        result.text = domText;
        result.complete = true;
        if (diag) {
          diag.answerComplete = true;
          diag.incompleteReason = null;
          diag.charactersExtracted = domText.length;
          diag.succeed('ANSWER_EXTRACT', { chars: domText.length });
        }
      } else {
        if (diag) diag.fail('ANSWER_EXTRACT', 'No text found in DOM');
      }
    }

    // Output response
    if (result?.text) {
      console.log(`\n═══════════════════════════════════════════`);
      console.log(result.text);
      console.log(`═══════════════════════════════════════════\n`);
      console.log(`📦 Ответ: ${result.text.length} символов`);
      console.log(`✅ Статус: ${result.complete ? 'полный' : 'может быть неполный'}`);
    } else {
      console.error('\n⚠️ Ответ не получен');
      // Dump page content for debugging
      try {
        const url = page.url();
        console.error(`📍 URL: ${url}`);
        const title = await page.title();
        console.error(`📄 Title: ${title}`);
      } catch {}
    }

    // Save session
    if (session) {
      session.messageCount = (session.messageCount || 0) + 2;
      persistSessionState(session, page, 'post-answer', {
        expectedChatUrl: expectedFollowUpChatUrl,
        strictContinuity: strictFollowUpContinuity,
      });
    }

    if (diag) {
      diag.printSummary(result?.text?.length || 0);
      diag.save();
    }

  } catch (err) {
    console.error(`\n❌ Ошибка: ${err.message}`);
    if (diag) { diag.fail('INIT', err.message); diag.printSummary(0); diag.save(); }
    debugLog(err.stack);
    process.exit(err.exitCode || 1);
  } finally {
    if (browser) {
      const shouldCleanup = useDaemon || shouldClose || !sessionName || dryRun;
      if (shouldCleanup) {
        await cleanup();
      }
    }
  }
}

main().catch(err => { console.error('Fatal:', err.message); process.exit(err.exitCode || 1); });