/**
 * TKSeller 卡片工具与本地状态。
 *
 * - card_map.json: 短编号 ↔ video_id 映射(按日重置)
 * - processed_events.json: 已 ack 的 event_id 集合(去重,防 ack 失败重发)
 * - poll_state.json: 轮询状态(started_at, active)
 * - 卡片发送通过 OpenClaw message 工具，自动适配所有渠道(discord/feishu/telegram/slack等)
 * - 使用统一 presentation 格式 + 渠道自动检测
 * - 媒体 URL 由 data-service 提供 HTTP(S) 公网 URL
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync, unlinkSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { execSync, spawn } from 'child_process';
import { homedir } from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// ========== 路径 / 常量 ==========
export const SKILL_DIR = dirname(__dirname);
export const CONFIG_PATH = join(SKILL_DIR, 'config.json');
export const DATA_DIR = join(SKILL_DIR, 'data');

const MAP_PATH = join(DATA_DIR, 'card_map.json');
const PROCESSED_PATH = join(DATA_DIR, 'processed_events.json');
const POLL_STATE_PATH = join(DATA_DIR, 'poll_state.json');

const OPENCLAW_CONFIG = join(homedir(), '.openclaw', 'openclaw.json');
export const GATEWAY_URL = 'http://127.0.0.1:18789/tools/invoke';

// 卡片过期时间: 30min
const CARD_TTL_SECONDS = 30 * 60;
const DISCORD_EPOCH_MS = 1420070400000;

const CRON_JOB_NAME = 'tkseller-poll';
const PID_PATH = join(DATA_DIR, 'poll_loop.pid');

// ========== gateway token / config ==========
function _openclawCfg() {
  return JSON.parse(readFileSync(OPENCLAW_CONFIG, 'utf-8'));
}

export function _gatewayToken() {
  return _openclawCfg().gateway.auth.token;
}

/**
 * 检测消息应发往哪个渠道。
 *
 * 优先使用运行时指定的渠道（从触发来源传入），
 * 否则自动检测用户配置的通讯渠道。
 *
 * 优先级：feishu > discord > telegram > slack > whatsapp > signal > 其他
 * 返回 { channel: string, target: string|null }
 */
let _channelCache = null;
let _runtimeChannel = null;

/**
 * 设置运行时渠道（由触发脚本根据来源设置）。
 * 设置后 detectChannel() 优先返回此渠道。
 */
export function setRuntimeChannel(channel, target = null) {
  _runtimeChannel = { channel, target };
  _channelCache = null; // 清缓存
}

export function detectChannel() {
  if (_runtimeChannel) {
    // 运行时指定的渠道也必须验证凭证，防止 sessions 残留误导
    if (!_runtimeChannel.channel) return { channel: null, target: null };
    const cfg = _openclawCfg();
    const chCfg = (cfg.channels || {})[_runtimeChannel.channel];
    if (!chCfg || chCfg.enabled === false || !_hasCredentials(_runtimeChannel.channel, chCfg)) {
      return { channel: null, target: null };
    }
    return _runtimeChannel;
  }
  if (_channelCache) return _channelCache;
  const cfg = _openclawCfg();
  const channels = cfg.channels || {};

  // 按优先级检测
  const priorities = ['feishu', 'discord', 'telegram', 'slack', 'whatsapp', 'signal',
    'wecom', 'msteams', 'mattermost', 'line', 'qqbot'];

  for (const ch of priorities) {
    const chCfg = channels[ch];
    if (!chCfg) continue;
    if (chCfg.enabled === false) continue;
    // 必须有实际凭证才算"已配置"（防止空壳配置误判）
    if (!_hasCredentials(ch, chCfg)) continue;
    // 有配置且没被禁用且有凭证 → 用它
    const target = _getTarget(ch, chCfg, cfg);
    _channelCache = { channel: ch, target };
    return _channelCache;
  }

  // 兜底：找第一个有配置的
  for (const ch of Object.keys(channels)) {
    const chCfg = channels[ch];
    if (chCfg && chCfg.enabled !== false && _hasCredentials(ch, chCfg)) {
      const target = _getTarget(ch, chCfg, cfg);
      _channelCache = { channel: ch, target };
      return _channelCache;
    }
  }

  // 啥都没配
  _channelCache = { channel: null, target: null };
  return _channelCache;
}

/**
 * 检查渠道是否有实际凭证（token/appId等）。
 * 防止空壳配置（有字段但没填 token）被误判为"已配置"。
 */
function _hasCredentials(ch, chCfg) {
  switch (ch) {
    case 'discord':
      return !!(chCfg.token && chCfg.token.length > 10);
    case 'feishu':
      return !!(chCfg.appId && chCfg.appSecret);
    case 'telegram':
      return !!(chCfg.token && chCfg.token.length > 10);
    case 'slack':
      return !!(chCfg.botToken || chCfg.token);
    case 'whatsapp':
    case 'signal':
      return !!(chCfg.phone || chCfg.number || chCfg.token);
    default:
      // 其他渠道默认有配置就算有凭证
      return true;
  }
}

function _getTarget(channel, chCfg, fullCfg) {
  switch (channel) {
    case 'discord': {
      const guilds = chCfg.guilds || {};
      for (const guildId of Object.keys(guilds)) {
        const chs = guilds[guildId].channels || {};
        const keys = Object.keys(chs);
        if (keys.length) return keys[0];
      }
      // 没配 guilds → 返回 null，后续 detectChannel 会走 detectChannelFromSessions 兜底
      return null;
    }
    case 'feishu': {
      const groups = chCfg.groups || {};
      const groupIds = Object.keys(groups);
      if (groupIds.length) return groupIds[0];
      return null;
    }
        case 'telegram': {
      // Telegram target 是 chat_id
      const allowFrom = chCfg.allowFrom || [];
      if (allowFrom.length) return String(allowFrom[0]);
      return null;
    }
    default:
      return null;
  }
}

// 兼容旧代码
export function _discordTarget() {
  const { channel, target } = detectChannel();
  return target;
}

export function _skillCfg() {
  return JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'));
}

// ========== card_map ==========
export function _ensureDir() {
  mkdirSync(DATA_DIR, { recursive: true });
}

function _today() {
  return new Date().toISOString().slice(0, 10);
}

export function loadMap() {
  const today = _today();
  if (!existsSync(MAP_PATH)) return { date: today, next_id: 1, cards: {} };
  try {
    const m = JSON.parse(readFileSync(MAP_PATH, 'utf-8'));
    if (m.date !== today) return { date: today, next_id: 1, cards: {} };
    return m;
  } catch {
    return { date: today, next_id: 1, cards: {} };
  }
}

export function saveMap(m) {
  _ensureDir();
  writeFileSync(MAP_PATH, JSON.stringify(m, null, 2), 'utf-8');
}

function _cardAgeSeconds(info) {
  const ts = info.createdAt;
  if (ts) return Math.floor(Date.now() / 1000) - Number(ts);
  const mid = info.messageId;
  if (mid) {
    try {
      const ms = (BigInt(mid) >> 22n) + BigInt(DISCORD_EPOCH_MS);
      return Math.floor(Date.now() / 1000) - Number(ms / 1000n);
    } catch { return null; }
  }
  return null;
}

export function pruneExpiredCards(m = null, ttl = CARD_TTL_SECONDS) {
  const external = m !== null;
  if (m === null) m = loadMap();
  const expired = [];
  for (const [sid, info] of Object.entries(m.cards || {})) {
    const age = _cardAgeSeconds(info);
    if (age !== null && age > ttl) {
      expired.push(sid);
      delete m.cards[sid];
    }
  }
  if (expired.length && !external) saveMap(m);
  return expired;
}

export function reserveShortId(videoId, step) {
  const m = loadMap();
  pruneExpiredCards(m);
  const shortId = m.next_id;
  m.next_id = shortId + 1;
  const prevOrder = { review_1: 0, review_1_5: 1, review_2: 2 };
  const cur = prevOrder[step] ?? -1;
  const toRemove = [];
  for (const [sid, info] of Object.entries(m.cards || {})) {
    if (info.video_id === videoId && (prevOrder[info.step] ?? -1) < cur) {
      toRemove.push(sid);
    }
  }
  for (const sid of toRemove) delete m.cards[sid];
  m.cards[String(shortId)] = {
    video_id: videoId,
    step,
    messageId: null,
    createdAt: Math.floor(Date.now() / 1000),
  };
  saveMap(m);
  return shortId;
}

export function updateMapMessageId(shortId, messageId) {
  const m = loadMap();
  if (m.cards && m.cards[String(shortId)]) {
    m.cards[String(shortId)].messageId = messageId;
    saveMap(m);
  }
}

export function lookupByShortId(shortId) {
  const m = loadMap();
  const info = (m.cards || {})[String(shortId)];
  if (!info) return null;
  const age = _cardAgeSeconds(info);
  if (age !== null && age > CARD_TTL_SECONDS) {
    delete m.cards[String(shortId)];
    saveMap(m);
    return null;
  }
  return info;
}

export function removeShortId(shortId) {
  const m = loadMap();
  if (m.cards) delete m.cards[String(shortId)];
  saveMap(m);
}

export function findShortIdByVideo(videoId, step = null) {
  const m = loadMap();
  for (const [sid, info] of Object.entries(m.cards || {})) {
    if (info.video_id === videoId) {
      if (step === null || info.step === step) return sid;
    }
  }
  return null;
}

// ========== processed events ==========
function _loadProcessed() {
  if (!existsSync(PROCESSED_PATH)) return { ids: [] };
  try { return JSON.parse(readFileSync(PROCESSED_PATH, 'utf-8')); }
  catch { return { ids: [] }; }
}

function _saveProcessed(d) {
  _ensureDir();
  if (d.ids.length > 5000) d.ids = d.ids.slice(-5000);
  writeFileSync(PROCESSED_PATH, JSON.stringify(d, null, 2), 'utf-8');
}

export function isEventProcessed(eventId) {
  const d = _loadProcessed();
  return (d.ids || []).includes(eventId);
}

export function markEventProcessed(eventId) {
  const d = _loadProcessed();
  if (!d.ids.includes(eventId)) {
    d.ids.push(eventId);
    _saveProcessed(d);
  }
}

// ========== poll state ==========
export function pollStateLoad() {
  if (!existsSync(POLL_STATE_PATH)) return { started_at: 0, active: false };
  try { return JSON.parse(readFileSync(POLL_STATE_PATH, 'utf-8')); }
  catch { return { started_at: 0, active: false }; }
}

export function pollStateSave(d) {
  _ensureDir();
  writeFileSync(POLL_STATE_PATH, JSON.stringify(d, null, 2), 'utf-8');
}

export function pollStarted(channel = null) {
  const state = { started_at: Math.floor(Date.now() / 1000), active: true };
  if (channel) {
    state.channel = channel;
  } else if (_runtimeChannel) {
    state.channel = _runtimeChannel.channel;
    if (_runtimeChannel.target) state.target = _runtimeChannel.target;
  }
  pollStateSave(state);
}

export function pollStopped() {
  const s = pollStateLoad();
  s.active = false;
  pollStateSave(s);
}

export function pollDuration() {
  const s = pollStateLoad();
  if (!s.started_at) return 0;
  return Math.floor(Date.now() / 1000) - Number(s.started_at);
}

// ========== 自动检测来源渠道 ==========
/**
 * 从 gateway sessions_list 查最近活跃的通讯会话，
 * 返回 { channel, target } 或 null。
 * 非硬编码：每个用户的 OpenClaw 实例查的是自己的 sessions。
 */
export async function detectChannelFromSessions() {
  try {
    // 交叉验证：session 里的渠道必须在 cfg.channels 中且 enabled !== false
    // 防止历史 session 残留（比如用户删了 cfg 但 OpenClaw 内存里还有 bot）误导
    const cfg = _openclawCfg();
    const cfgChannels = cfg?.channels || {};
    function isCfgEnabled(ch) {
      const c = cfgChannels[ch];
      return c && c.enabled !== false;
    }

    const body = JSON.stringify({ tool: 'sessions_list', args: { limit: 20 } });
    const r = await fetch(GATEWAY_URL, {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + _gatewayToken(),
        'Content-Type': 'application/json',
      },
      body,
      signal: AbortSignal.timeout(5000),
    });
    if (!r.ok) return null;
    const d = await r.json();
    const text = d?.result?.content?.[0]?.text;
    if (!text) return null;
    const parsed = JSON.parse(text);
    const sessions = parsed.sessions || [];
    // 找最近有 deliveryContext.to 的非 webchat session（按 updatedAt 已排序）
    for (const s of sessions) {
      const ch = s.channel;
      if (!ch || ch === 'webchat' || ch === 'unknown') continue;
      // 交叉验证：cfg 里没这个渠道或被禁用了 → 跳过
      if (!isCfgEnabled(ch)) continue;
      const to = s.deliveryContext?.to;
      if (to) return { channel: ch, target: to };
      // 没有 to 但有 chat_id 在 key 里（如飞书 oc_xxx）
      const m = s.key?.match(/(oc_[a-f0-9]+)/);
      if (m) return { channel: ch, target: m[1] };
    }
  } catch { /* */ }
  return null;
}

// ========== Gateway 调用 ==========
export async function _gatewayInvoke(tool, args, timeoutMs = 30000) {
  const payload = { tool, args };
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const r = await fetch(GATEWAY_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${_gatewayToken()}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    clearTimeout(timer);
    if (!r.ok) throw new Error(`gateway ${r.status}`);
    return await r.json();
  } catch (e) {
    clearTimeout(timer);
    throw e;
  }
}

// ========== 轮询进程控制 ==========
function _readPid() {
  if (!existsSync(PID_PATH)) return null;
  try { return parseInt(readFileSync(PID_PATH, 'utf-8').trim(), 10) || null; }
  catch { return null; }
}

function _pidAlive(pid) {
  if (!pid) return false;
  try {
    if (process.platform === 'win32') {
      const out = execSync(`tasklist /FI "PID eq ${pid}" /FO CSV /NH`, {
        encoding: 'utf-8', timeout: 5000, stdio: ['pipe', 'pipe', 'pipe'],
      });
      return out.includes(`"${pid}"`);
    } else {
      // Unix: send signal 0 to check
      process.kill(pid, 0);
      return true;
    }
  } catch { return false; }
}

function _killPid(pid) {
  if (!pid) return;
  try {
    if (process.platform === 'win32') {
      execSync(`taskkill /F /PID ${pid}`, { timeout: 5000, stdio: 'ignore' });
    } else {
      process.kill(pid, 'SIGKILL');
    }
  } catch { /* ignore */ }
}

function _sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export async function startPollProcess() {
  // 1) 清理 OpenClaw cron 残留
  try {
    const resp = await _gatewayInvoke('cron', { action: 'list' });
    for (const j of (resp.jobs || [])) {
      if (j.name === CRON_JOB_NAME) {
        try { await _gatewayInvoke('cron', { action: 'remove', id: j.id }); } catch { /* */ }
      }
    }
  } catch { /* */ }

  // 2) 检查现有进程
  const pid = _readPid();
  if (pid && _pidAlive(pid)) {
    // 进程还在跑，只确保 active=true，不刷新 started_at
    const s = pollStateLoad();
    if (!s.active) {
      s.active = true;
      pollStateSave(s);
    }
    return { ok: true, pid, reused: true };
  }

  // 3) 启动新进程
  const script = join(__dirname, 'poll-loop.mjs');
  pollStarted();

  const child = spawn(process.execPath, [script], {
    cwd: SKILL_DIR,
    stdio: 'ignore',
    detached: true,
    windowsHide: true,
  });
  child.unref();

  return { ok: true, pid: child.pid, started: true };
}

export async function stopPollProcess() {
  pollStopped();

  const pid = _readPid();
  if (pid && _pidAlive(pid)) {
    // 给进程几秒自然退出
    for (let i = 0; i < 3; i++) {
      await _sleep(1000);
      if (!_pidAlive(pid)) break;
    }
    if (_pidAlive(pid)) _killPid(pid);
  }

  try { if (existsSync(PID_PATH)) unlinkSync(PID_PATH); } catch { /* */ }

  // 清理 cron 残留
  try {
    const resp = await _gatewayInvoke('cron', { action: 'list' });
    for (const j of (resp.jobs || [])) {
      if (j.name === CRON_JOB_NAME) {
        try { await _gatewayInvoke('cron', { action: 'remove', id: j.id }); } catch { /* */ }
      }
    }
  } catch { /* */ }
}

// 兼容别名
export const cronStartPolling = startPollProcess;
export const cronStopPolling = stopPollProcess;

// ========== 媒体 URL ==========
export function mediaUrl(sourceUrl) {
  if (!sourceUrl) throw new Error('media_url: source_url 为空');
  if (!sourceUrl.startsWith('http://') && !sourceUrl.startsWith('https://')) {
    throw new Error(`media_url 只接受 HTTP(S) URL: ${sourceUrl}`);
  }
  return sourceUrl;
}

// ========== 统一消息发送（自动适配所有渠道） ==========

/**
 * 发带按钮的卡片消息。使用 OpenClaw presentation 格式，自动适配所有渠道。
 *
 * @param {string} text - 卡片正文（markdown）
 * @param {string} mediaUrlValue - 媒体预览 URL（图片/视频）
 * @param {Array} buttons - [{label, style}] 按钮列表
 * @param {string} mediaDescription - 媒体描述
 */
export async function sendCard(text, mediaUrlValue, buttons, mediaDescription = '预览') {
  let { channel, target } = detectChannel();
  if (!channel) {
    throw new Error('NO_CHANNEL: 未配置任何通讯渠道。请先运行 `openclaw channels login --channel <feishu|discord|telegram>` 配置一个渠道。');
  }
  if (!target) {
    const fallback = await detectChannelFromSessions();
    if (fallback && fallback.target) {
      channel = fallback.channel || channel;
      target = fallback.target;
    }
  }

  // 构建消息参数
  const args = {
    action: 'send',
    channel,
    message: text,
  };
  if (target) {
    if (channel === 'discord' && !target.startsWith('channel:') && !target.startsWith('user:')) {
      args.target = 'channel:' + target;
    } else {
      args.target = target;
    }
  }

  // Discord：message + components（图片 + 按钮）
  if (channel === 'discord') {
    const compBlocks = [];
    if (mediaUrlValue) {
      compBlocks.push({
        type: 'media-gallery',
        items: [{ url: mediaUrlValue, description: mediaDescription }],
      });
    }
    if (buttons && buttons.length) {
      compBlocks.push({
        type: 'actions',
        buttons: buttons.map(b => ({ ...b, allowedUsers: ['*'] })),
      });
    }
    if (compBlocks.length) {
      args.components = {
        flags: 32768,
        blocks: compBlocks,
        reusable: true,
      };
    }
  } else {
    // 其他渠道：用 presentation 格式
    const presentationBlocks = [];
    presentationBlocks.push({ type: 'text', text });
    if (mediaUrlValue) {
      presentationBlocks.push({ type: 'image', url: mediaUrlValue, alt: mediaDescription });
    }
    if (buttons && buttons.length) {
      presentationBlocks.push({
        type: 'buttons',
        buttons: buttons.map(b => ({
          label: b.label,
          value: b.label,
          style: _mapStyle(b.style),
        })),
      });
    }
    args.presentation = { blocks: presentationBlocks };
  }

  const payload = { tool: 'message', args };

  const r = await fetch(GATEWAY_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${_gatewayToken()}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(60000),
  });
  if (!r.ok) throw new Error(`gateway sendCard ${r.status}`);
  const d = await r.json();
  try {
    return d?.result?.details?.result?.messageId || null;
  } catch { return null; }
}

/**
 * 发纯文本消息。自动适配所有渠道。
 */
export async function sendText(text, trackToolCalls = false) {
  let { channel, target } = detectChannel();
  if (!channel) {
    console.error('[tkseller] NO_CHANNEL: 未配置任何通讯渠道');
    return 0;
  }
  // target 为空时尝试从活跃 session 兜底
  if (!target) {
    const fallback = await detectChannelFromSessions();
    if (fallback && fallback.target) {
      channel = fallback.channel || channel;
      target = fallback.target;
    }
  }
  const args = { action: 'send', channel, message: text };
  if (target) {
    if (channel === 'discord' && !target.startsWith('channel:') && !target.startsWith('user:')) {
      args.target = 'channel:' + target;
    } else {
      args.target = target;
    }
  }
  if (trackToolCalls === false) args.trackToolCalls = false;
  const payload = { tool: 'message', args };
  try {
    const r = await fetch(GATEWAY_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${_gatewayToken()}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(30000),
    });
    return r.status;
  } catch { return 0; }
}

export const sendProgress = sendText;

/**
 * 发带按钮的纯文本卡片（无媒体）。用于数字人选择等场景。
 */
export async function sendButtonCard(text, buttonRows) {
  let { channel, target } = detectChannel();
  if (!channel) {
    throw new Error('NO_CHANNEL: 未配置任何通讯渠道。请先运行 `openclaw channels login --channel <feishu|discord|telegram>` 配置一个渠道。');
  }
  if (!target) {
    const fallback = await detectChannelFromSessions();
    if (fallback && fallback.target) {
      channel = fallback.channel || channel;
      target = fallback.target;
    }
  }


  // presentation 格式（按行分块）
  const presentationBlocks = [{ type: 'text', text }];
  // buttonRows: [[{label, style}], [{label, style}]] — 多行按钮
  for (const row of buttonRows) {
    const rowBtns = row.map(b => ({
      label: b.label,
      value: b.label,
      style: _mapStyle(b.style),
    }));
    if (rowBtns.length) {
      presentationBlocks.push({ type: 'buttons', buttons: rowBtns });
    }
  }

  const args = {
    action: 'send',
    channel,
    message: text,
    presentation: { blocks: presentationBlocks },
  };
  if (target) {
    if (channel === 'discord' && !target.startsWith('channel:') && !target.startsWith('user:')) {
      args.target = 'channel:' + target;
    } else {
      args.target = target;
    }
  }

  // Discord 增强
  if (channel === 'discord') {
    args.components = {
      flags: 32768,
      blocks: buttonRows.map(row => ({
        type: 'actions',
        buttons: row.map(b => ({ ...b, allowedUsers: ['*'] })),
      })),
      reusable: true,
    };
    // 有 modal 的场景由调用者额外传入
  }

  const payload = { tool: 'message', args };
  const r = await fetch(GATEWAY_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${_gatewayToken()}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(60000),
  });
  if (!r.ok) throw new Error(`gateway sendButtonCard ${r.status}`);
  const d = await r.json();
  try {
    return d?.result?.details?.result?.messageId || null;
  } catch { return null; }
}

/**
 * 发带媒体 + 多行按钮的卡片。buttonRows: [[{label, style}], ...]
 */
export async function sendCardRows(text, mediaUrlValue, buttonRows, mediaDescription = '预览') {
  let { channel, target } = detectChannel();
  if (!channel) {
    throw new Error('NO_CHANNEL: 未配置任何通讯渠道。请先运行 `openclaw channels login --channel <feishu|discord|telegram>` 配置一个渠道。');
  }
  if (!target) {
    const fallback = await detectChannelFromSessions();
    if (fallback && fallback.target) {
      channel = fallback.channel || channel;
      target = fallback.target;
    }
  }

  const args = { action: 'send', channel, message: text };
  if (target) {
    if (channel === 'discord' && !target.startsWith('channel:') && !target.startsWith('user:')) {
      args.target = 'channel:' + target;
    } else {
      args.target = target;
    }
  }

  if (channel === 'discord') {
    const compBlocks = [];
    if (mediaUrlValue) {
      compBlocks.push({
        type: 'media-gallery',
        items: [{ url: mediaUrlValue, description: mediaDescription }],
      });
    }
    for (const row of buttonRows) {
      if (row && row.length) {
        compBlocks.push({
          type: 'actions',
          buttons: row.map(b => ({ ...b, allowedUsers: ['*'] })),
        });
      }
    }
    if (compBlocks.length) {
      args.components = { flags: 32768, blocks: compBlocks, reusable: true };
    }
  } else {
    const presentationBlocks = [{ type: 'text', text }];
    if (mediaUrlValue) {
      presentationBlocks.push({ type: 'image', url: mediaUrlValue, alt: mediaDescription });
    }
    for (const row of buttonRows) {
      if (row && row.length) {
        presentationBlocks.push({
          type: 'buttons',
          buttons: row.map(b => ({ label: b.label, value: b.label, style: _mapStyle(b.style) })),
        });
      }
    }
    args.presentation = { blocks: presentationBlocks };
  }

  const payload = { tool: 'message', args };
  const r = await fetch(GATEWAY_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${_gatewayToken()}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(60000),
  });
  if (!r.ok) throw new Error(`gateway sendCardRows ${r.status}`);
  const d = await r.json();
  try {
    return d?.result?.details?.result?.messageId || null;
  } catch { return null; }
}

// presentation style 映射
function _mapStyle(discordStyle) {
  const map = {
    success: 'success',
    primary: 'primary',
    secondary: 'secondary',
    danger: 'danger',
    link: 'secondary',
  };
  return map[discordStyle] || 'secondary';
}
