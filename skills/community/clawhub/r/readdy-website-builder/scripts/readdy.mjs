#!/usr/bin/env node

/**
 * Readdy Website Builder CLI
 *
 * Lightweight script for creating and managing websites via the Readdy.ai platform.
 * Usage: node readdy.mjs <command> [options]
 *
 * Config:
 *   node readdy.mjs config --apiKey <key>           Save API Key
 */

import path from 'path';
import os from 'os';
import { createInterface } from 'readline';
import { loadApiKey, saveApiKey, getCredentialsPath } from './config-store.mjs';

// ─── config ──────────────────────────────────────────────────────────────────

const CREDENTIALS_FILE = getCredentialsPath();
const API_HOST = 'https://readdy.ai';
const GENERATE_API_PATH = '/gapi/project/generate';
const PROJECT_MESSAGES_API_PATH = '/api/project/msg_list';
const PROJECT_SHARE_API_PATH = '/api/project/share';
const SUBDOMAIN_INFO_API_PATH = '/api/project/subdomain/info';
const SUBDOMAIN_GENERATE_API_PATH = '/api/project/subdomain/generate';
const SUBDOMAIN_PUBLISH_API_PATH = '/api/project/subdomain/publish';
const SUBDOMAIN_PUBLISH_CHECK_API_PATH = '/api/project/subdomain/publish_check';

let API_KEY = '';
let TOKEN = null;
const DEFAULT_FRAMEWORK = 'react_v2';
const DEFAULT_DEVICE = 'web';
const DEFAULT_CATEGORY = 2;

// ─── helpers ────────────────────────────────────────────────────────────────

function die(msg, code = 1) {
  console.error(`[ERROR] ${msg}`);
  process.exit(code);
}

function info(msg) {
  console.log(`[INFO] ${msg}`);
}

function warn(msg) {
  console.warn(`[WARN] ${msg}`);
}

/** Exchange API Key for a temporary token */
async function resolveToken() {
  if (!API_KEY) die('API Key not configured. Run: node readdy.mjs config --apiKey <your-key>');
  info('Resolving token from API Key...');
  try {
    const res = await fetch(`${API_HOST}/api/public/apikey/decrypt`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key: API_KEY }),
    });
    const data = await res.json().catch(() => null);
    if (!res.ok || !data || (data.code && data.code !== 'OK')) {
      die(`Failed to resolve token: ${data?.meta?.message || data?.meta?.detail || res.statusText}`);
    }
    const accessToken = data?.data?.token?.accessToken;
    if (!accessToken) {
      die(`Failed to resolve token: response missing accessToken (${JSON.stringify(data).slice(0, 200)})`);
    }
    TOKEN = accessToken;
    info('Token resolved successfully');
  } catch (err) {
    if (err?.cause?.code === 'ENOTFOUND' || err?.cause?.code === 'ECONNREFUSED') {
      die('Network connection failed. Check your network or disable VPN and retry.');
    }
    die(`Token request failed: ${err.message}`);
  }
}

async function api(method, path, body, projectId, options = {}) {
  if (!TOKEN) die('Token not initialized. Ensure API Key is configured: node readdy.mjs config --apiKey <your-key>');
  const acceptedCodes = new Set(options.acceptCodes || []);

  const url = `${API_HOST}${path}`;
  const headers = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${TOKEN}`,
  };
  if (projectId) headers['X-Project-ID'] = projectId;

  const opts = { method, headers };
  if (body && method !== 'GET') opts.body = JSON.stringify(body);

  let finalUrl = url;
  if (method === 'GET' && body) {
    const qs = new URLSearchParams(
      Object.entries(body).filter(([, v]) => v !== undefined).map(([k, v]) => [k, String(v)])
    ).toString();
    if (qs) finalUrl = `${url}?${qs}`;
  }
  try {
    const res = await fetch(finalUrl, opts);
    const data = await res.json().catch(() => null);

    if (!res.ok) {
      const errMsg = data?.meta?.message || data?.meta?.detail || res.statusText;
      const errCode = data?.code || res.status;
      handleError(errCode, errMsg);
      return null;
    }

    if (data?.code && data.code !== 'OK' && !acceptedCodes.has(data.code)) {
      handleError(data.code, data?.meta?.message || data?.meta?.detail || 'Unknown error');
      return null;
    }

    return data;
  } catch (err) {
    if (err?.cause?.code === 'ENOTFOUND' || err?.cause?.code === 'ECONNREFUSED') {
      die('Network connection failed. Check your network or disable VPN and retry.');
    }
    die(`Request failed: ${err.message}`);
  }
}

/** SSE streaming request for /gapi/project/generate */
async function apiSSE(path, body, projectId) {
  if (!TOKEN) die('Token not initialized. Ensure API Key is configured: node readdy.mjs config --apiKey <your-key>');

  const url = `${API_HOST}${path}`;
  const headers = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${TOKEN}`,
  };
  if (projectId) headers['X-Project-ID'] = projectId;

  let res;
  try {
    res = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
    });
  } catch (err) {
    warn(`SSE connection failed: ${err.message}`);
    return null;
  }

  // If response is JSON instead of SSE, it's an error
  if (res.headers.get('Content-Type')?.includes('application/json')) {
    const json = await res.json().catch(() => null);
    if (json?.code && json.code !== 'OK') {
      handleError(json.code, json?.meta?.message || json?.meta?.detail || 'Generate failed');
      return null;
    }
    return json;
  }

  if (!res.ok) {
    handleError(res.status, res.statusText);
    return null;
  }

  // Parse SSE stream — aligned with frontend SSEReaderHandle + Reader state machine
  const reader = res.body.getReader();
  const decoder = new TextDecoder();

  let buffer = '';
  let currentEvent = '';

  // Metadata (extracted from response events)
  let versionId = null;
  let showId = null;
  let revertShowId = null;
  let sessionId = null;
  let sessionStatus = null;
  let language = null;
  let requestId = null;
  let errorInfo = null;

  // eventData collection — aligned with frontend Reader.getEventDataItem() output format
  const eventData = [];

  // thinking state
  let thinkingStart = null;

  // data accumulation (frontend DataReader: accumulate text until action tag or event switch)
  let accumulatedText = '';

  // tool state (frontend ToolReader: same-name tool data accumulates into one entry)
  let currentToolEntry = null;
  let currentToolName = '';
  let currentToolPartBuf = '';

  const ACTION_START = '<action';
  const ACTION_END = '</action>';

  /** Split <action>...</action> tags from text, aligned with frontend DataReader + ActionReader */
  function splitAndPushTextWithAction(text) {
    const actionIdx = text.indexOf(ACTION_START);
    if (actionIdx === -1) {
      if (text) eventData.push({ event: 'data', data: { text } });
      return;
    }
    const cleanText = text.slice(0, actionIdx);
    if (cleanText) eventData.push({ event: 'data', data: { text: cleanText } });

    const remaining = text.slice(actionIdx);
    const endIdx = remaining.indexOf(ACTION_END);
    if (endIdx === -1) {
      if (remaining) eventData.push({ event: 'data', data: { text: remaining } });
      return;
    }
    const actionBlock = remaining.slice(0, endIdx + ACTION_END.length);
    const nameMatch = actionBlock.match(/<action[^>]*\bname=["']([^"']+)["']/);
    const actionName = nameMatch ? nameMatch[1] : '';
    let actionDataStr = '';
    if (actionName === 'nextStep') {
      const steps = [];
      const stepRe = /<step>([\s\S]*?)<\/step>/g;
      let m, n = 1;
      while ((m = stepRe.exec(actionBlock)) !== null) steps.push({ step: n++, data: m[1].trim() });
      actionDataStr = JSON.stringify({ steps });
    }
    eventData.push({ event: 'action', data: { action: actionName, status: 'ready', data: actionDataStr } });

    const afterAction = remaining.slice(endIdx + ACTION_END.length);
    if (afterAction.trim()) splitAndPushTextWithAction(afterAction);
  }

  /** Flush current reader state */
  function flushCurrent() {
    if (accumulatedText && currentEvent === 'data') {
      splitAndPushTextWithAction(accumulatedText);
      accumulatedText = '';
    }
    if (thinkingStart !== null && currentEvent === 'thinking') {
      eventData.push({ event: 'thinking', data: { duration: Date.now() - thinkingStart, isThinking: false } });
      thinkingStart = null;
    }
    if (currentToolEntry && currentEvent === 'tool') {
      if (currentToolPartBuf) {
        try {
          currentToolEntry.data.toolData = JSON.parse(currentToolPartBuf);
        } catch {}
        currentToolPartBuf = '';
      }
      eventData.push(currentToolEntry);
      currentToolEntry = null;
      currentToolName = '';
    }
  }

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('event:')) {
          const newEvent = line.slice(6).trim();
          // Flush on event type change
          if (newEvent !== currentEvent) {
            flushCurrent();
          }
          currentEvent = newEvent;
          if (currentEvent === 'thinking') thinkingStart = Date.now();
        } else if (line.startsWith('data:')) {
          const data = line.slice(5);

          // ── Dispatch by event type ──
          if (currentEvent === 'thinking') {
            process.stdout.write(data);
          } else if (currentEvent === 'data') {
            process.stdout.write(data);
            accumulatedText += data;
            // Aligned with frontend DataReader: detect <action tags in real-time and split
            if (accumulatedText.indexOf(ACTION_START) !== -1 && accumulatedText.indexOf(ACTION_END) !== -1) {
              splitAndPushTextWithAction(accumulatedText);
              accumulatedText = '';
            }
          } else if (currentEvent === 'tool') {
            try {
              const toolObj = JSON.parse(data);
              const name = toolObj.name || toolObj.tool;
              if (name && name !== currentToolName) {
                // New tool — flush old one (parse accumulated parts), start new entry
                if (currentToolEntry) {
                  if (currentToolPartBuf) {
                    try {
                      currentToolEntry.data.toolData = JSON.parse(currentToolPartBuf);
                    } catch {}
                    currentToolPartBuf = '';
                  }
                  eventData.push(currentToolEntry);
                }
                currentToolName = name;
                currentToolPartBuf = '';
                process.stdout.write('\n');
                info(`  [tool] ${name}`);
                const toolData = { name };
                if (toolObj.files) toolData.files = toolObj.files;
                if (toolObj.toolData) toolData.toolData = toolObj.toolData;
                currentToolEntry = { event: 'tool', data: toolData };
              } else if (toolObj.part !== undefined) {
                // Accumulate part fragments for current tool
                currentToolPartBuf += toolObj.part;
              } else if (currentToolEntry) {
                // Same-name tool subsequent data — accumulate files/toolData
                if (toolObj.files) currentToolEntry.data.files = toolObj.files;
                if (toolObj.toolData) currentToolEntry.data.toolData = { ...(currentToolEntry.data.toolData || {}), ...toolObj.toolData };
              }
            } catch {}
          } else if (currentEvent === 'action') {
            // Standalone action SSE event
            try {
              const actionObj = JSON.parse(data);
              eventData.push({ event: 'action', data: { action: actionObj.action || '', status: actionObj.status || 'ready', data: actionObj.data || '' } });
            } catch {
              // Non-JSON — possibly raw action tag text
              const nameMatch = data.match(/<action[^>]*\bname=["']([^"']+)["']/);
              if (nameMatch) {
                eventData.push({ event: 'action', data: { action: nameMatch[1], status: 'ready', data: '' } });
              }
            }
          }

          // response event — extract metadata (aligned with frontend ResponseReader)
          if (currentEvent === 'response' || currentEvent === 'finish') {
            try {
              const r = JSON.parse(data);
              // error
              if (r.error) {
                errorInfo = { type: 'normal', code: r.error.err_code || 'UnknownError', status: r.error.status || 0, message: r.error.err_code || '' };
              }
              if (r.project_version_id) versionId = r.project_version_id;
              if (r.show_id) showId = r.show_id;
              if (r.revert_show_id) revertShowId = r.revert_show_id;
              if (r.session_id) sessionId = r.session_id;
              if (r.session_status) sessionStatus = r.session_status;
              if (r.language) language = r.language;
              if (r.request_id) requestId = r.request_id;
            } catch {}
          }
        }
      }
    }
  } catch (err) {
    warn(`SSE stream interrupted: ${err.message}`);
  }
  // Flush remaining state
  flushCurrent();
  if (accumulatedText) {
    splitAndPushTextWithAction(accumulatedText);
    accumulatedText = '';
  }
  if (thinkingStart !== null) {
    eventData.push({ event: 'thinking', data: { duration: Date.now() - thinkingStart, isThinking: false } });
  }
  // Flush any remaining tool entry not yet pushed
  if (currentToolEntry) {
    if (currentToolPartBuf) {
      try { currentToolEntry.data.toolData = JSON.parse(currentToolPartBuf); } catch {}
    }
    eventData.push(currentToolEntry);
  }
  process.stdout.write('\n');

  return { eventData, versionId, showId, revertShowId, sessionId, sessionStatus, language, requestId, errorInfo };
}

// ─── error handling ─────────────────────────────────────────────────────────

function handleError(code, message) {
  const errorMap = {
    401: 'Authentication failed. Token expired or invalid. Check your API Key: node readdy.mjs config --apiKey <new-key>',
    403: 'Access denied. Current role cannot perform this operation.',
    AccessDenied: 'Access denied. Current role cannot perform this operation.',
    ProjectNotFound: 'Project not found or has been deleted.',
    ProjectMax: 'Project limit reached. Upgrade your subscription or delete old projects.',
    ApiKeyInvalid: 'API Key is invalid or expired.',
    ImageTooLarge: 'Image size cannot exceed 3.5MB.',
    SubscriptionInGracePeriod: 'Subscription is in grace period. Please update payment info.',
    RequestTimeout: 'Request timed out. Please try again later.',
    InvalidParameter: `Invalid parameter: ${message}`,
    PromptTooLong: 'Request content too long. Please simplify and retry.',
    InternalError: 'Internal server error. Please try again later.',
    PreviewError: `Preview error: ${message}`,
  };
  const msg = errorMap[code] || `[${code}] ${message || 'Unknown error. Check your network or contact support.'}`;
  console.error(`[ERROR] ${msg}`);
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function toEpochMs(value) {
  const num = Number(value || 0);
  if (!Number.isFinite(num) || num <= 0) return 0;
  return num > 1e12 ? num : num * 1000;
}

function formatDateTime(value) {
  const epochMs = toEpochMs(value);
  if (!epochMs) return '-';
  return new Date(epochMs).toLocaleString();
}

function parseJsonSafe(value) {
  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}

function extractVersionEntriesFromMessage(msg) {
  if (!msg || msg.role !== 0) return [];
  const content = parseJsonSafe(msg.content);
  if (!content || !Array.isArray(content.content)) return [];

  const createdAt = toEpochMs(msg.createdAt);

  return content.content
    .map((item) => {
      const versionId = Number(item?.data?.projectVersionId || 0);
      const showId = Number(item?.data?.showId || 0);
      if (versionId <= 0 || showId <= 0) return null;
      return {
        versionId,
        showId,
        createdAt,
        msgId: Number(msg.id || 0),
        recordStatus: Number(item?.data?.recordStatus || 0),
      };
    })
    .filter(Boolean);
}

async function fetchAllProjectMessages(projectId, pageSize = 100) {
  const allMessages = [];
  const normalizedPageSize = Math.max(1, Number(pageSize) || 100);
  let pageNum = 1;
  let total = Infinity;

  while (allMessages.length < total) {
    const res = await api('POST', PROJECT_MESSAGES_API_PATH, {
      projectId,
      isTemplate: false,
      page: { pageNum, pageSize: normalizedPageSize },
    }, projectId);
    if (!res?.data) break;

    const { projectMsgs = [], page = {} } = res.data;
    allMessages.push(...projectMsgs);
    total = Number(page.total || projectMsgs.length || 0);

    if (projectMsgs.length === 0 || allMessages.length >= total) {
      break;
    }
    pageNum += 1;
  }

  return allMessages;
}

async function getProjectVersions(projectId, pageSize = 100) {
  const messages = await fetchAllProjectMessages(projectId, pageSize);
  const merged = new Map();

  for (const msg of messages) {
    for (const entry of extractVersionEntriesFromMessage(msg)) {
      const prev = merged.get(entry.versionId);
      if (
        !prev ||
        entry.showId > prev.showId ||
        entry.createdAt > prev.createdAt
      ) {
        merged.set(entry.versionId, entry);
      }
    }
  }

  return Array.from(merged.values()).sort((a, b) => {
    if (b.versionId !== a.versionId) return b.versionId - a.versionId;
    if (b.showId !== a.showId) return b.showId - a.showId;
    return b.createdAt - a.createdAt;
  });
}

async function getLatestProjectVersion(projectId) {
  const versions = await getProjectVersions(projectId);
  return versions[0] || null;
}

async function getProjectSubdomainInfo(projectId) {
  const res = await api('GET', SUBDOMAIN_INFO_API_PATH, { projectId }, projectId);
  return res?.data || null;
}

async function ensureProjectSubdomain(projectId) {
  const existing = await getProjectSubdomainInfo(projectId);
  if (existing?.domain) {
    return existing;
  }

  info('Generating project subdomain...');
  const res = await api(
    'POST',
    `${SUBDOMAIN_GENERATE_API_PATH}?projectId=${encodeURIComponent(projectId)}`,
    undefined,
    projectId
  );
  return res?.data || null;
}

async function pollSubdomainPublish(projectId, maxAttempts = 12, intervalMs = 5000) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    await sleep(intervalMs);
    const result = await api(
      'POST',
      `${SUBDOMAIN_PUBLISH_CHECK_API_PATH}?projectId=${encodeURIComponent(projectId)}`,
      undefined,
      projectId,
      { acceptCodes: ['ProjectBuildAsyncCheck'] }
    );

    if (!result) return null;

    const status = Number(result?.data?.status || 0);

    if (result.code === 'OK' && status !== 3) {
      return result;
    }

    if (status === 3) {
      warn(`  Publish failed${result?.meta?.message ? `: ${result.meta.message}` : ''}`);
      return result;
    }

    info(`  Publish still processing (${attempt}/${maxAttempts})...`);
  }

  warn('Publish status check timed out. Please re-run the publish or versions command in a moment.');
  return null;
}

/** Read a line of user input from stdin */
function readUserInput(prompt) {
  return new Promise((resolve) => {
    process.stdout.write(prompt);
    const rl = createInterface({ input: process.stdin, output: process.stdout });
    rl.once('line', (line) => {
      rl.close();
      resolve(line.trim());
    });
    rl.once('close', () => resolve(''));
  });
}

// ─── build + session continuation ────────────────────────────────────────────

/**
 * Build project and poll for status
 * @returns {{ buildOk: boolean, buildError: string }}
 */
async function buildAndCheck(projectId, versionId) {
  info('  Building project...');
  const buildRes = await api('POST', '/api/project/build', { projectId, versionId }, projectId);
  if (!buildRes) warn('Build request failed');

  info('  Checking build status...');
  let buildOk = false;
  let buildError = '';
  for (let i = 0; i < 30; i++) {
    await sleep(2000);
    const checkRes = await api('POST', '/api/project/build_check', { projectId, versionId }, projectId);
    if (checkRes?.code === 'OK' && checkRes.data?.previewUrl) {
      buildOk = true;
      info(`  Build succeeded! Preview: ${checkRes.data.previewUrl}`);
      break;
    }
    if (checkRes?.data?.compileError) {
      buildError = checkRes.data.compileError;
      warn(`  Build error: ${buildError.slice(0, 200)}`);
      break;
    }
  }
  if (!buildOk && !buildError) warn('Build did not complete within timeout');
  return { buildOk, buildError };
}

/**
 * Execute generate -> build/ask_user -> session continuation loop
 * Aligned with frontend GeneratePageSession SessionStatus handling:
 *   - waiting_build: execute build then continue
 *   - waiting_input: prompt user input then continue (CLI reads from stdin)
 *   - completed: session ended normally
 *   - failed: session failed
 * @returns {{ allEventData, versionId, finalRequestId, finalSessionId, finalSessionStatus, finalShowId, language, hasBuilt }}
 */
async function generateWithSessionLoop(projectId, generateParams) {
  let allEventData = [];
  let versionId = null;
  let finalRequestId = '';
  let finalSessionId = '';
  let finalSessionStatus = '';
  let finalShowId = 0;
  let lang = '';
  let hasBuilt = false;
  let currentParams = { ...generateParams };
  let round = 0;
  const MAX_ROUNDS = 10;

  while (round < MAX_ROUNDS) {
    round++;
    info(`  Generate round ${round}...`);

    const sseResult = await apiSSE(GENERATE_API_PATH, currentParams, projectId);
    if (!sseResult) {
      warn('SSE generation failed');
      break;
    }

    allEventData = [...allEventData, ...sseResult.eventData];
    if (sseResult.versionId) versionId = sseResult.versionId;
    if (sseResult.showId) finalShowId = sseResult.showId;
    if (sseResult.requestId) finalRequestId = sseResult.requestId;
    if (sseResult.sessionId) finalSessionId = sseResult.sessionId;
    if (sseResult.sessionStatus) finalSessionStatus = sseResult.sessionStatus;
    if (sseResult.language) lang = sseResult.language;

    info(`  versionId: ${versionId || '(none)'}, sessionStatus: ${finalSessionStatus || '(none)'}`);

    if (sseResult.errorInfo) {
      warn(`  Generate returned error: [${sseResult.errorInfo.code}] ${sseResult.errorInfo.message}`);
      break;
    }

    // ── Decide next step based on sessionStatus ──

    if (finalSessionStatus === 'failed') {
      warn('  Session failed, aborting generation');
      break;
    }

    if (finalSessionStatus === 'completed' || !finalSessionId) {
      // Session ended normally or no sessionId — exit loop
      break;
    }

    if (finalSessionStatus === 'waiting_build' && versionId) {
      // waiting_build — execute build then continue
      info('  Session requires build before continuing...');
      const { buildOk, buildError } = await buildAndCheck(projectId, versionId);
      hasBuilt = true;

      currentParams = {
        ...generateParams,
        sessionId: finalSessionId,
        buildResult: { success: buildOk, error: buildError || '' },
        language: lang,
      };
      continue;
    }

    if (finalSessionStatus === 'waiting_input') {
      // waiting_input (ask_user) — prompt user for input, then continue generate
      // Extract question text from ask_user tool event in SSE data
      let questionText = '';
      for (const ev of sseResult.eventData) {
        if (ev.event === 'tool' && ev.data?.name === 'ask_user' && ev.data?.toolData?.questions) {
          const questions = ev.data.toolData.questions;
          if (questions.length > 0 && questions[0].question) {
            questionText = questions[0].question;
          }
          break;
        }
      }

      info(`  Session waiting for user input (ask_user)...`);
      if (questionText) info(`  Question: ${questionText}`);

      const userInput = await readUserInput('Enter your reply (press Enter to submit): ');
      if (!userInput) {
        warn('  No user input provided, aborting generation');
        break;
      }

      // Format query as "Q1: question\nA1: answer" aligned with frontend behavior
      const formattedQuery = questionText
        ? `Q1: ${questionText}\nA1: ${userInput}`
        : userInput;

      currentParams = {
        ...generateParams,
        query: formattedQuery,
        sessionId: finalSessionId,
        language: lang,
      };
      continue;
    }

    // Unknown status or no continuation needed — exit
    break;
  }

  if (round >= MAX_ROUNDS) warn('Session continuation rounds reached limit');

  return { allEventData, versionId, finalRequestId, finalSessionId, finalSessionStatus, finalShowId, language: lang, hasBuilt };
}

// ─── message helpers ─────────────────────────────────────────────────────────

/** Create user message (role=1) */
async function createUserMsg(projectId, query, imageUrl) {
  const contentItems = [];
  if (imageUrl) contentItems.push({ type: 1, data: { url: imageUrl } });
  contentItems.push({ type: 0, data: { text: query } });
  const content = JSON.stringify({ content: contentItems, status: 0, type: 0 });
  const res = await api('POST', '/api/project/msg', { projectId, role: 1, content }, projectId);
  return res?.data?.id || null;
}

/** Create AI placeholder message (role=0, recordStatus=2) */
async function createAiMsg(projectId, fromMsgId, recordReference = 0) {
  const content = JSON.stringify({
    content: [{ type: 3, data: { recordStatus: 2, showId: 0, eventData: [{ event: 'analyzing', data: {} }], requestId: '' } }],
    status: 0,
    type: 1,
    recordReference,
    fromMsgId
  });
  const res = await api('POST', '/api/project/msg', { projectId, role: 0, content }, projectId);
  return res?.data?.id || null;
}

/** Update AI message — aligned with frontend GenerateResponseHandler.message structure */
async function updateAiMsg(projectId, msgId, { versionId = 0, showId = 0, recordStatus = 0, requestId = '', fromMsgId = 0, recordReference = 0, eventData = [], sessionId = '', sessionStatus = '', revertShowId } = {}) {
  const msgData = { projectVersionId: versionId, recordStatus, showId, eventData, requestId };
  if (sessionId) msgData.sessionId = sessionId;
  if (sessionStatus) msgData.sessionStatus = sessionStatus;
  const msgContent = {
    content: [{ type: 3, data: msgData }],
    status: 0,
    type: 1,
    recordReference,
    fromMsgId
  };
  if (revertShowId) msgContent.revertShowId = revertShowId;
  const content = JSON.stringify(msgContent);
  await api('PUT', '/api/project/msg', { projectId, msgId, role: 0, content }, projectId);
}

// ─── commands ───────────────────────────────────────────────────────────────

/** 1. List projects */
async function listProjects(pageNum = 1, pageSize = 50) {
  info('Fetching project list...');
  const res = await api('POST', '/api/page_gen/project/list', {
    page: { pageNum: Number(pageNum), pageSize: Number(pageSize) },
  });
  if (!res) return;

  const { projects, page } = res.data;
  console.log(`\nTotal ${page.total} projects (page ${page.pageNum}, ${page.pageSize} per page):\n`);
  console.log('ID'.padEnd(28) + 'Name'.padEnd(30) + 'Framework'.padEnd(12) + 'Published'.padEnd(10) + 'Device'.padEnd(10) + 'Role');
  console.log('-'.repeat(100));
  for (const p of projects) {
    console.log(
      (p.id || '').padEnd(28) +
      (p.name || '(unnamed)').padEnd(30) +
      (p.framework || '-').padEnd(12) +
      (p.isPublish ? 'Yes' : 'No').padEnd(10) +
      (p.device || '-').padEnd(10) +
      (p.role || '-')
    );
  }
  return projects;
}

/** 2. Get project info */
async function getProjectInfo(projectId) {
  if (!projectId) die('--id (projectId) is required');

  info(`Fetching project ${projectId} info...`);
  const res = await api('GET', '/api/page_gen/project', { projectId }, projectId);
  if (!res) return null;

  console.log('\nProject info:');
  console.log(JSON.stringify(res.data, null, 2));
  return res.data;
}

/** 3. Get project message history */
async function getProjectMessages(projectId, pageNum = 1, pageSize = 50) {
  if (!projectId) die('--id (projectId) is required');

  info('Fetching project message history...');
  const res = await api('POST', PROJECT_MESSAGES_API_PATH, {
    projectId,
    page: { pageNum: Number(pageNum), pageSize: Number(pageSize) },
  }, projectId);
  if (!res) return null;

  const { projectMsgs, page } = res.data;
  console.log(`\nTotal ${page.total} messages (page ${page.pageNum}):\n`);
  for (const msg of projectMsgs) {
    const role = msg.role === 1 ? 'USER' : 'AI';
    const time = new Date(msg.createdAt * 1000).toLocaleString();
    const content = msg.content.length > 100 ? msg.content.slice(0, 100) + '...' : msg.content;
    console.log(`[${role}] (id:${msg.id}) ${time}\n  ${content}\n`);
  }
  return projectMsgs;
}

/** 4.1 List publishable versions */
async function listProjectVersions(projectId, pageSize = 100) {
  if (!projectId) die('--id (projectId) is required');

  info(`Fetching publish versions for ${projectId}...`);
  const [versions, subdomainInfo] = await Promise.all([
    getProjectVersions(projectId, pageSize),
    getProjectSubdomainInfo(projectId),
  ]);

  const liveShowId = Number(subdomainInfo?.showId || 0);
  const liveDomain = subdomainInfo?.domain || '';
  const latestVersion = versions[0] || null;

  console.log('\nPublish version summary:');
  console.log(`Project ID: ${projectId}`);
  console.log(`Subdomain: ${liveDomain ? `https://${liveDomain}` : '(not generated yet)'}`);
  console.log(`Live version: ${liveShowId > 0 ? `V${liveShowId}` : 'Unpublished'}`);
  console.log(
    `Latest version: ${
      latestVersion ? `V${latestVersion.showId} (versionId: ${latestVersion.versionId})` : 'No publishable version'
    }`
  );

  if (versions.length === 0) {
    console.log('\nNo publishable versions found yet. Create or modify the project first.');
    return { versions, subdomainInfo };
  }

  console.log('\nAvailable publish versions:\n');
  console.log(
    'Version ID'.padEnd(14) +
    'Show ID'.padEnd(10) +
    'Created At'.padEnd(24) +
    'Flags'
  );
  console.log('-'.repeat(70));

  for (const version of versions) {
    const flags = [];
    if (version === latestVersion) flags.push('LATEST');
    if (liveShowId > 0 && version.showId === liveShowId) flags.push('LIVE');

    console.log(
      String(version.versionId).padEnd(14) +
      `V${version.showId}`.padEnd(10) +
      formatDateTime(version.createdAt).padEnd(24) +
      (flags.join(', ') || '-')
    );
  }

  return { versions, subdomainInfo };
}

/** 4. Create project — full workflow (aligned with HAR capture + frontend source) */
async function createProject(opts) {
  const { query, device, framework, lib, category } = opts;
  if (!query) die('--query is required (project description/requirements)');

  info('This process may take over 10 minutes. Please be patient...');

  const deviceType = device || DEFAULT_DEVICE;
  const fw = framework || DEFAULT_FRAMEWORK;

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 1/8: gen_section (generate page modules) + suggest_title (generate project name) in parallel
  // ═══════════════════════════════════════════════════════════════════════════
  info('Step 1/8: Generating page modules and project name in parallel...');
  const [sectionRes, titleRes] = await Promise.all([
    api('POST', '/api/project/gen_section', { query }),
    api('POST', '/api/page_gen/suggest/page_title', { query }),
  ]);

  // Parse gen_section result
  let sections = [], pages = [], logoPrompt = '';
  if (sectionRes?.data) {
    sections = sectionRes.data.sections || [];
    pages = sectionRes.data.pages || [];
    logoPrompt = sectionRes.data.logo || '';
    const items = pages.length > 0 ? pages : sections;
    info(`  Got ${items.length} ${pages.length > 0 ? 'pages' : 'sections'}`);
    items.forEach((item, i) => console.log(`    ${i + 1}. ${item}`));
  } else {
    warn('[Step 1] gen_section failed, subsequent generation may lack page structure');
  }

  // Parse suggest_title result
  let projectName = 'New Project';
  if (titleRes?.data?.title) {
    projectName = titleRes.data.title;
    info(`  Project name: ${projectName}`);
  } else {
    warn('[Step 1] suggest_title failed, using default name: New Project');
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 2/8: gen_logo (depends on logoPrompt from gen_section)
  // ═══════════════════════════════════════════════════════════════════════════
  let logoUrl = '';
  if (logoPrompt) {
    info('Step 2/8: Generating logo...');
    const logoRes = await api('POST', '/api/project/gen_logo', { query: logoPrompt });
    if (logoRes?.data?.imageUrl) {
      logoUrl = logoRes.data.imageUrl;
      info(`  Logo generated: ${logoUrl}`);
    } else {
      warn('[Step 2] Logo generation failed, skipping logo');
    }
  } else {
    info('Step 2/8: Skipped (gen_section did not return logo prompt)');
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 3/8: Create project (POST /api/page_gen/project)
  // ═══════════════════════════════════════════════════════════════════════════
  info('Step 3/8: Creating project...');
  const createParams = {
    name: projectName,
    framework: fw,
    lib: lib || '',
    category: category !== undefined ? Number(category) : DEFAULT_CATEGORY,
    device: deviceType,
  };
  const createRes = await api('POST', '/api/page_gen/project', createParams);
  if (!createRes?.data?.id) die('[Step 3] Project creation failed, cannot continue');
  const projectId = createRes.data.id;
  info(`  Project created: ${projectId}`);

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 4/8: Save logo to project (PUT /api/page_gen/project)
  // ═══════════════════════════════════════════════════════════════════════════
  if (logoUrl) {
    info('Step 4/8: Saving logo...');
    const logoSaveRes = await api('PUT', '/api/page_gen/project', { projectId, logo: logoUrl }, projectId);
    if (!logoSaveRes) warn('[Step 4] Logo save failed, project will have no logo');
  } else {
    info('Step 4/8: Skipped (no logo)');
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 5/8: Create message records + initiate generate (parallel, aligned with frontend behavior)
  //
  // Frontend timing: user message, AI placeholder message, and generate are sent almost simultaneously
  // - User message: POST /api/project/msg (role=1)
  // - AI placeholder: POST /api/project/msg (role=0, recordStatus=2)
  // - Generate: POST /gapi/project/generate (SSE)
  // ═══════════════════════════════════════════════════════════════════════════
  info('Step 5/8: Creating message records and generating project content...');

  // Build pageSection — HAR shows all sections are used
  const pageSection = pages.length > 0
    ? pages.map(p => `<webpage>${p}</webpage>`).join('')
    : sections.map(s => `<section>${s}</section>`).join('');

  // Build generate params — strictly aligned with HAR first generate request
  const generateParams = {
    projectID: projectId,
    parentVersionID: 0,
    query: query + ', no ask me',
    route: '/',
    browser: { language: 'zh-CN', timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || 'Asia/Shanghai' },
    parentShowID: 0,
    apiVersion: 'v2',
    language: '',                        // Empty string for first call, filled by generateWithSessionLoop on continuation
    role: '',
    elementCode: '',
    xpath: '',
    ...(pageSection && { pageSection }),
    ...(logoUrl && { logoUrl }),
  };

  // Parallel: user message + AI message + generate
  // Don't wait for message creation before starting generate, aligned with frontend behavior
  const userMsgPromise = createUserMsg(projectId, query);
  const aiMsgPromise = (async () => {
    // AI message needs fromMsgId, but doesn't block generate
    const userMsgId = await userMsgPromise;
    return createAiMsg(projectId, userMsgId);
  })();
  const generatePromise = generateWithSessionLoop(projectId, generateParams);

  // Wait for all to complete
  const [userMsgId, aiMsgId, result] = await Promise.all([
    userMsgPromise,
    aiMsgPromise,
    generatePromise,
  ]);

  if (!userMsgId) warn('[Step 5] User message creation failed, message record incomplete');
  if (!aiMsgId) warn('[Step 5] AI message creation failed, message record incomplete');

  const versionId = result.versionId;

  if (!versionId) {
    warn('[Step 5] generate did not return versionId, cannot build');
    if (aiMsgId) {
      await updateAiMsg(projectId, aiMsgId, { fromMsgId: userMsgId, eventData: result.allEventData });
    }
    console.log(`\nProject created (no version generated)! ID: ${projectId}`);
    return { projectId };
  }

  info(`  versionId: ${versionId}`);

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 6/8: Final build (if not already built during session continuation)
  //
  // Frontend handleCompleted():
  //   hasBuiltSuccessfully -> skip
  //   has versionId but not built -> execute fallback build
  // ═══════════════════════════════════════════════════════════════════════════
  if (!result.hasBuilt) {
    info('Step 6/8: Executing final build...');
    const { buildOk, buildError } = await buildAndCheck(projectId, versionId);
    if (!buildOk) {
      warn(`[Step 6] Build failed${buildError ? ': ' + buildError.slice(0, 200) : ''}`);
    }
  } else {
    info('Step 6/8: Skipped (already built during continuation)');
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 7/8: Set showId (POST /api/project/set_show_id)
  //
  // Frontend retry strategy: timerRetryFetch([0, 2000, 2000, 2000, 2000])
  // First attempt may return showID=0, needs retry
  // ═══════════════════════════════════════════════════════════════════════════
  info('Step 7/8: Setting showId...');
  let finalShowId = result.finalShowId || 0;
  if (!finalShowId || finalShowId <= 0) {
    // Aligned with frontend timerRetryFetch([0, 2000, 2000, 2000, 2000]): retry on business value
    const delays = [0, 2000, 2000, 2000, 2000];
    for (let i = 0; i < delays.length; i++) {
      if (delays[i]) await sleep(delays[i]);
      const res = await api('POST', '/api/project/set_show_id',
        { projectId, versionID: versionId }, projectId);
      finalShowId = res?.data?.showID || 0;
      if (finalShowId > 0) {
        info(`  showId: ${finalShowId}`);
        break;
      }
      if (i < delays.length - 1) info(`  showId still 0, retrying (${i + 1}/${delays.length})...`);
    }
    if (!finalShowId || finalShowId <= 0) {
      warn('[Step 7] set_show_id still returned showId=0 after multiple retries');
    }
  } else {
    info(`  showId: ${finalShowId} (from SSE response)`);
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 8/8: Update AI message to completed state (PUT /api/project/msg)
  //
  // recordStatus: 2 -> 0, showId: final value, eventData: complete event stream
  // ═══════════════════════════════════════════════════════════════════════════
  info('Step 8/8: Updating message to completed state...');
  if (aiMsgId) {
    await updateAiMsg(projectId, aiMsgId, {
      versionId,
      showId: finalShowId,
      fromMsgId: userMsgId,
      eventData: result.allEventData,
      requestId: result.finalRequestId,
      sessionId: result.finalSessionId,
      sessionStatus: result.finalSessionStatus,
    });
    info('  Message updated');
  } else {
    warn('[Step 8] No AI message ID, skipping message update');
  }

  console.log(`\nProject created! ID: ${projectId}, versionId: ${versionId}, showId: ${finalShowId}`);
  return { projectId, versionId, showId: finalShowId };
}

/** 5. Modify project — full workflow (AI regeneration) */
async function modifyProject(opts) {
  const { id, query } = opts;
  if (!id) die('--id (projectId) is required');
  if (!query) die('--query is required (modification requirements)');

  info('This process may take over 10 minutes. Please be patient...');

  // Step 1: Get project info
  info('Step 1/6: Fetching project info...');
  const projectRes = await api('GET', '/api/page_gen/project', { projectId: id }, id);
  if (!projectRes) die('[Step 1] Failed to fetch project info');
  const project = projectRes.data;
  info(`  Project: ${project?.name || id}`);

  // Step 2: Get message history
  info('Step 2/6: Fetching message history...');
  const msgRes = await api('POST', '/api/project/msg_list', {
    projectId: id,
    isTemplate: false,
    page: { pageNum: 1, pageSize: 100 },
  }, id);
  const messages = msgRes?.data?.projectMsgs || [];
  info(`  Got ${messages.length} history messages`);

  // Extract parentVersionID, parentShowID, parentSessionId from history, build history JSON
  let parentVersionID = 0;
  let parentShowID = 0;
  let parentSessionId = '';
  const historyEntries = [];

  for (const msg of messages) {
    try {
      const content = JSON.parse(msg.content);
      if (msg.role === 0 && Array.isArray(content.content)) {
        // AI message: extract projectVersionId, showId, sessionId
        for (const item of content.content) {
          if (item.data?.projectVersionId && item.data.projectVersionId > parentVersionID) {
            parentVersionID = item.data.projectVersionId;
          }
          if (item.data?.versionId && item.data.versionId > parentVersionID) {
            parentVersionID = item.data.versionId;
          }
          if (item.data?.showId && item.data.showId > parentShowID) {
            parentShowID = item.data.showId;
          }
          if (item.data?.sessionId) {
            parentSessionId = item.data.sessionId;
          }
        }
      }
      // Build history JSON: user messages + corresponding AI events
      if (msg.role === 1 && Array.isArray(content.content)) {
        const text = content.content.filter(c => c.type === 0).map(c => c.data?.text || '').join('');
        if (text) historyEntries.push({ user: text, events: [] });
      }
      if (msg.role === 0 && Array.isArray(content.content) && historyEntries.length > 0) {
        const lastEntry = historyEntries[historyEntries.length - 1];
        for (const item of content.content) {
          if (item.data?.eventData && Array.isArray(item.data.eventData)) {
            for (const ev of item.data.eventData) {
              if (ev.event === 'tool') {
                const toolName = ev.data?.name || '';
                const files = ev.data?.files || [];
                const toolData = ev.data?.toolData ? JSON.stringify(ev.data.toolData) : '';
                lastEntry.events.push({ type: 'tool_info', tool: toolName, info: toolData || files.join(',') });
              } else if (ev.event === 'data') {
                const text = ev.data?.text || '';
                if (text) lastEntry.events.push({ type: 'text', content: text });
              }
            }
          }
        }
      }
    } catch {}
  }
  info(`  parentVersionID: ${parentVersionID}, parentShowID: ${parentShowID}, parentSessionId: ${parentSessionId || '(none)'}`);

  // Build history JSON string
  const historyJSON = historyEntries.length > 0 ? JSON.stringify(historyEntries) : '';

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 3/6: Create message records + initiate generate (parallel, aligned with frontend behavior)
  //
  // Frontend timing: user message, AI placeholder message, and generate are sent almost simultaneously
  // - User message: POST /api/project/msg (role=1)
  // - AI placeholder: POST /api/project/msg (role=0, recordStatus=2)
  // - Generate: POST /gapi/project/generate (SSE)
  // ═══════════════════════════════════════════════════════════════════════════
  info('Step 3/6: Creating message records and generating modifications...');

  const generateParams = {
    parentVersionID,
    projectID: id,
    query: query + ', no ask me',
    route: '/',
    parentShowID,
    browser: { language: 'zh-CN', timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || 'Asia/Shanghai' },
    apiVersion: 'v2',
    currentDevice: project?.device || DEFAULT_DEVICE,
    console: [],
    network: [],
    language: '',                        // Empty string for first call, filled by generateWithSessionLoop on continuation
    role: project?.role || '',           // Get user role from project info
    embedCode: '',
    ...(parentSessionId && { parentSessionId }),
    ...(historyJSON && { history: historyJSON }),
  };

  // Parallel: user message + AI message + generate (aligned with frontend executeSend behavior)
  const userMsgPromise = createUserMsg(id, query);
  const aiMsgPromise = (async () => {
    const userMsgId = await userMsgPromise;
    return createAiMsg(id, userMsgId, parentVersionID);
  })();
  const generatePromise = generateWithSessionLoop(id, generateParams);

  const [userMsgId, aiMsgId, result] = await Promise.all([
    userMsgPromise,
    aiMsgPromise,
    generatePromise,
  ]);

  if (!userMsgId) warn('[Step 3] User message creation failed, message record incomplete');
  if (!aiMsgId) warn('[Step 3] AI message creation failed, message record incomplete');
  const versionId = result.versionId;

  if (!versionId) {
    warn('[Step 3] generate did not return versionId, cannot build');
    if (aiMsgId) await updateAiMsg(id, aiMsgId, { fromMsgId: userMsgId, recordReference: parentVersionID, eventData: result.allEventData });
    console.log('\nModification complete (no new version generated)');
    return { projectId: id };
  }

  info(`  versionId: ${versionId}`);

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 4/6: Final build (if not already built during session continuation)
  // ═══════════════════════════════════════════════════════════════════════════
  if (!result.hasBuilt) {
    info('Step 4/6: Executing final build...');
    const { buildOk, buildError } = await buildAndCheck(id, versionId);
    if (!buildOk) {
      warn(`[Step 4] Build failed${buildError ? ': ' + buildError.slice(0, 200) : ''}`);
    }
  } else {
    info('Step 4/6: Skipped (already built during continuation)');
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 5/6: Set showId (POST /api/project/set_show_id)
  // ═══════════════════════════════════════════════════════════════════════════
  info('Step 5/6: Setting showId...');
  let finalShowId = result.finalShowId || 0;
  if (!finalShowId || finalShowId <= 0) {
    const delays = [0, 2000, 2000, 2000, 2000];
    for (let i = 0; i < delays.length; i++) {
      if (delays[i]) await sleep(delays[i]);
      const res = await api('POST', '/api/project/set_show_id',
        { projectId: id, versionID: versionId }, id);
      finalShowId = res?.data?.showID || 0;
      if (finalShowId > 0) {
        info(`  showId: ${finalShowId}`);
        break;
      }
      if (i < delays.length - 1) info(`  showId still 0, retrying (${i + 1}/${delays.length})...`);
    }
    if (!finalShowId || finalShowId <= 0) {
      warn('[Step 5] set_show_id still returned showId=0 after multiple retries');
    }
  } else {
    info(`  showId: ${finalShowId} (from SSE response)`);
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 6/6: Update AI message to completed state (PUT /api/project/msg)
  // ═══════════════════════════════════════════════════════════════════════════
  info('Step 6/6: Updating message to completed state...');
  if (aiMsgId) {
    await updateAiMsg(id, aiMsgId, {
      versionId, showId: finalShowId, fromMsgId: userMsgId, recordReference: parentVersionID,
      eventData: result.allEventData, requestId: result.finalRequestId,
      sessionId: result.finalSessionId, sessionStatus: result.finalSessionStatus,
    });
    info('  Message updated');
  } else {
    warn('[Step 6] No AI message ID, skipping message update');
  }

  console.log(`\nProject modified! ID: ${id}, versionId: ${versionId}, showId: ${finalShowId}`);
  return { projectId: id, versionId, showId: finalShowId };
}

/** 6. Update project properties (name/description/logo etc.) */
async function updateProject(opts) {
  const { id, name, background, referBackground, businessName, introduction,
    phoneNumber, businessHour, languageStyle, email, logo, notifyEmail } = opts;
  if (!id) die('--id (projectId) is required');

  const params = { projectId: id };
  const fields = { name, background, referBackground, businessName, introduction,
    phoneNumber, businessHour, languageStyle, email, logo, notifyEmail };
  let hasUpdate = false;
  for (const [k, v] of Object.entries(fields)) {
    if (v !== undefined) { params[k] = v; hasUpdate = true; }
  }
  if (!hasUpdate) die('At least one field to update is required (e.g. --name, --background, --logo)');

  info(`Updating project ${id}...`);
  const res = await api('PUT', '/api/page_gen/project', params, id);
  if (!res) return;

  console.log('Project properties updated!');
  return res;
}

/** 7. Delete project */
async function deleteProject(projectId) {
  if (!projectId) die('--id (projectId) is required');

  info(`Deleting project ${projectId}...`);
  const res = await api('DELETE', '/api/page_gen/project', { projectId }, projectId);
  if (!res) return;

  console.log('Project deleted.');
  return res;
}

/** 8. Publish project to subdomain */
async function publishProjectVersion(projectId, versionId) {
  if (!projectId) die('--id (projectId) is required');

  info('Fetching version info before publish...');
  const { versions, subdomainInfo: existingSubdomainInfo } = await listProjectVersions(projectId);
  if (versions.length === 0) {
    die('No publishable version found. Create or modify the project first.');
  }

  const requestedVersionId = versionId ? Number(versionId) : undefined;
  if (versionId && (!Number.isFinite(requestedVersionId) || requestedVersionId <= 0)) {
    die('--versionId must be a positive number');
  }

  const selectedVersion = requestedVersionId
    ? versions.find((item) => item.versionId === requestedVersionId)
    : versions[0] || null;

  if (requestedVersionId && !selectedVersion) {
    die(`versionId ${requestedVersionId} was not found. Run: node readdy.mjs versions --id ${projectId}`);
  }

  const targetLabel = selectedVersion
    ? `V${selectedVersion.showId} (versionId: ${selectedVersion.versionId})`
    : 'latest version';

  const effectiveVersionId = selectedVersion?.versionId;
  if (!effectiveVersionId) {
    die('Failed to resolve the selected versionId from version info.');
  }

  info(`Preparing to publish selected version ${targetLabel}...`);
  const subdomainInfo = existingSubdomainInfo?.domain ? existingSubdomainInfo : await ensureProjectSubdomain(projectId);
  if (subdomainInfo?.domain) {
    info(`Publishing to https://${subdomainInfo.domain}`);
  }

  const params = new URLSearchParams({ projectId });
  params.set('versionId', String(effectiveVersionId));

  let result = await api(
    'POST',
    `${SUBDOMAIN_PUBLISH_API_PATH}?${params.toString()}`,
    undefined,
    projectId,
    { acceptCodes: ['ProjectBuildAsyncCheck'] }
  );
  if (!result) return null;

  const initialStatus = Number(result?.data?.status || 0);

  if (result.code === 'ProjectBuildAsyncCheck' || initialStatus === 1) {
    info('Publish is processing asynchronously...');
    result = await pollSubdomainPublish(projectId);
    if (!result) return null;
  }

  const finalStatus = Number(result?.data?.status || 0);

  if (result.code !== 'OK' || !result.data || finalStatus === 3) {
    if (result?.meta?.message) warn(result.meta.message);
    return result;
  }

  console.log(
    `\nProject published! Domain: https://${result.data.domain}, versionId: ${result.data.versionId ?? effectiveVersionId}, showId: ${result.data.showId}`
  );
  return result.data;
}

/** 9. Preview project */
async function previewProject(projectId, versionId) {
  if (!projectId) die('--id (projectId) is required');

  // If no versionId specified, extract the latest from message history
  if (!versionId) {
    info('Extracting latest versionId from message history...');
    const latestVersion = await getLatestProjectVersion(projectId);
    if (latestVersion?.versionId) {
      versionId = latestVersion.versionId;
      info(`  Extracted versionId: ${versionId} (showId: ${latestVersion.showId})`);
    } else {
      die('versionId not found. Please specify with --versionId');
    }
  }

  // Get preview link via share API (aligned with frontend behavior)
  info('Fetching preview link...');
  const shareRes = await api('GET', PROJECT_SHARE_API_PATH, {
    projectId,
    versionId: Number(versionId),
  }, projectId);

  if (shareRes?.data?.url) {
    console.log(`\nPreview URL: ${shareRes.data.url}`);
  } else {
    warn('Failed to get preview URL');
  }

  return shareRes?.data;
}

/** Config management */
function configCommand(opts) {
  if (opts.apiKey) {
    saveApiKey(opts.apiKey);
    info(`apiKey saved → ${CREDENTIALS_FILE}`);
  } else {
    const key = loadApiKey();
    if (key) {
      info(`apiKey: ${key.slice(0, 8)}***  ← ${CREDENTIALS_FILE}`);
    } else {
      die('API Key not configured. Run: node readdy.mjs config --apiKey <your-key>');
    }
  }
}

// ─── CLI arg parser ─────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = argv.slice(2);
  const command = args[0];
  const opts = {};
  for (let i = 1; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith('--')) {
        opts[key] = next;
        i++;
      } else {
        opts[key] = true;
      }
    }
  }
  return { command, opts };
}

function printUsage() {
  console.log(`
Readdy Website Builder CLI

Usage: node readdy.mjs <command> [options]

Commands:
  list    [--page <n>] [--pageSize <n>]           List all projects
  info    --id <projectId>                         Get project info
  messages --id <projectId>                        Get project message history
  versions --id <projectId> [--pageSize <n>]       List publishable versions
  create  --query <description>                    Create website (full workflow)
          [--device web|mobile]
          [--framework <f>] [--lib <l>]
          [--category <c>]
  modify  --id <projectId> --query <requirements>  Modify website (AI regeneration)
  update  --id <projectId> [--name <n>]            Update project properties
          [--background <b>] [--logo <url>]
          [--businessName <bn>] [--email <e>]
  publish --id <projectId> [--versionId <v>]       Publish latest or selected version to subdomain
  delete  --id <projectId>                         Delete project
  preview --id <projectId> [--versionId <v>]       Preview project
  config  [--apiKey <key>]                          Configure API Key
`);
}

// ─── main ───────────────────────────────────────────────────────────────────

async function main() {
  const { command, opts } = parseArgs(process.argv);

  if (command && command !== 'config') {
    API_KEY = loadApiKey();
    if (!API_KEY) die('API Key not configured. Run: node readdy.mjs config --apiKey <your-key>');
  }

  const needsAuth = command && command !== 'config';
  if (needsAuth) await resolveToken();

  switch (command) {
    case 'list':
      await listProjects(opts.page, opts.pageSize);
      break;
    case 'info':
      await getProjectInfo(opts.id);
      break;
    case 'messages':
      await getProjectMessages(opts.id, opts.page, opts.pageSize);
      break;
    case 'versions':
      await listProjectVersions(opts.id, opts.pageSize);
      break;
    case 'create':
      await createProject(opts);
      break;
    case 'modify':
      await modifyProject(opts);
      break;
    case 'update':
      await updateProject(opts);
      break;
    case 'publish':
      await publishProjectVersion(opts.id, opts.versionId);
      break;
    case 'delete':
      await deleteProject(opts.id);
      break;
    case 'preview':
      await previewProject(opts.id, opts.versionId);
      break;
    case 'config':
      configCommand(opts);
      break;
    default:
      printUsage();
      if (command) die(`Unknown command: ${command}`);
      break;
  }
}

main().catch(err => {
  console.error(`[FATAL] ${err.message}`);
  process.exit(1);
});
