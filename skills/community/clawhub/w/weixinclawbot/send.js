#!/usr/bin/env node
/**
 * weixinclaw-proactive-push/send.js
 *
 * 通过 WorkBuddy 已连接的 ClawBot 微信 bot 通道（weixinClawBot / ilink bot，非微信客服号）
 * 主动向老板微信推送消息：文本 / 图片 / 文件 / 视频。
 *
 * 【隐私说明】
 *   - 本脚本只读本机两处文件，不向任何文件写出凭据：
 *       ~/.workbuddy/settings.json                          （botToken / userId）
 *       ~/.workbuddy/claw-state/weixin/<ACCOUNT_ID>_im.bot.cursor.json （get_updates_buf 当 context_token）
 *   - 日志只打印 token 长度（ctx_len），【绝不】打印 token 明文 / botToken / userId。
 *   - 所有凭据均从本机配置文件现读，不依赖任何硬编码或外部传入的密钥。
 *   - ⚠️ claw-state/weixin/ 的 cursor 文件内嵌 bot 凭证镜像，切勿将其纳入分享 / 备份 / 提交。
 *
 * 【context_token 策略 — 文本默认空，媒体才取 cursor buf】
 *   - 文本推送：context_token 默认【空串】（会话存活时即可发送）。
 *       ⚠️ 2026-08-28 实测：会话过期后连空 token 文本也会 ret:-2 "prepare failed"，
 *       服务端校验的是用户侧下行会话（约 1 天无用户消息即过期），协议内无自激活手段。
 *   - 媒体推送（图片/文件/视频）：【必须】带非空 context_token，
 *       唯一来源 = claw-state/weixin 下 <ACCOUNT_ID>_im.bot.cursor.json 的 get_updates_buf。
 *   - get_updates_buf 是一个【base64 字符串】，用法极其严格：
 *       UTF-8 读 JSON → JSON.parse → 取 get_updates_buf 字段的【字符串原值】→ 原样当作 context_token 发出。
 *   - ❌ 严禁任何变换：base64 解码、重新编码、trim、URL-decode、转义、换行、截断。
 *       只要对原串做一步变换，服务端必返回 ret:-2。
 *   - 全程不读 context-token.json、不依赖任何 host 注入 hack。
 *
 * 【文件精确匹配，不靠 mtime 猜】
 *   - 从 settings.json 的 botToken 解析出 accountId（@im.bot: 之前那段），
 *     拼出唯一确定的文件名 <ACCOUNT_ID>_im.bot.cursor.json 直接读。
 *   - 这样即使目录里遗留了旧 accountId 的游标文件，也绝不会选错。
 *   - ⚠️ host 每轮长轮询都会改写 cursor 文件 mtime，mtime 变化【不代表】buf 值变了，
 *     也【不代表】凭证失效——mtime 仅用于"多份里挑活跃那份"，绝不能当失效依据。
 *
 * 【请求契约 — 严格对齐官方 @tencent-weixin/openclaw-weixin@2.4.6】
 *   - 头部（6 个，缺一不可）：Authorization: Bearer <完整botToken 含 accountId:前缀>、
 *           AuthorizationType: ilink_bot_token、X-WECHAT-UIN: <随机base64>、
 *           Content-Type: application/json、iLink-App-Id: bot、iLink-App-ClientVersion: 132102。
 *   - 正文顶层 base_info: { channel_version: "2.4.6", bot_agent: "OpenClaw" }。
 *   - msg.client_id: "cbc-<时间戳>-<随机>"（必须带 cbc- 前缀，非裸 uuid）。
 *   - msg.context_token: 上面的 get_updates_buf 原串。
 *
 * 【失败处理 — 不自动退避/重发，被拒即要求用户激活】
 *   - 本脚本只发一次。ret:-2 等错误会【直接、清晰地】报出来并以 exit 1 退出，
 *     不做任何 sleep / 轮询 / 等待激活 / 自动重试。
 *   - 若被拒（ret:-2）：【必须】先让老板/用户在微信给 ClawBot 发一条消息，
 *     激活 host 的发送游标，然后【手动重新运行】本命令；脚本不阻塞等待。
 *   - ⚠️ 文本推送平时用空 context_token 即可长期发送；一旦文本也被拒（ret:-2），
 *     大概率是底层 bot id / 凭证已轮换，【同样需要】发消息激活后重跑。
 *   - 媒体推送依赖 cursor buf，被拒同理：先激活刷新游标，再重跑。
 *
 * 用法:
 *   node send.js "文本消息"                                  # 主动推文本（默认空 context_token，无需激活）
 *   node send.js --text-file 内容.txt
 *   node send.js --image 截图.png --caption "看这张图"
 *   node send.js --file 报告.pdf --name "周报.pdf" --caption "请查阅"
 *   node send.js --video clip.mp4
 *   node send.js "回复" --context <token>                    # 手动指定 context_token 覆盖
 *   node send.js --verbose ...                              # 打印每步服务端响应
 *
 * 依赖: 仅 Node 内置 fetch / crypto / fs（Node 18+，推荐 managed node 22）。
 */

'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');

const SETTINGS_PATH = path.join(os.homedir(), '.workbuddy', 'settings.json');
const CLAW_STATE_DIR = path.join(os.homedir(), '.workbuddy', 'claw-state', 'weixin');
const CDN_BASE_URL = 'https://novac2c.cdn.weixin.qq.com/c2c';

// ── 权威契约常量（对齐官方 @tencent-weixin/openclaw-weixin@2.4.6）────────────
const CLIENT_ID_PREFIX = 'cbc-';                 // msg.client_id 必须以 cbc- 开头
const BASE_CHANNEL_VERSION = '2.4.6';            // base_info.channel_version（对齐官方，勿用旧值 cbc-1.0.0）
const BOT_AGENT = 'OpenClaw';                    // base_info.bot_agent
const ILINK_APP_CLIENT_VERSION = 132102;          // = buildClientVersion("2.4.6")，iLink-App-ClientVersion 头部

let VERBOSE = false;
// ⚠️ 仅打印调试信息，绝不打印任何 token 明文（只包含长度等非敏感字段）
function dbg(...a) { if (VERBOSE) console.error('[dbg]', ...a); }

// ── 参数解析 ────────────────────────────────────────────
function parseArgs(argv) {
  const a = { text: null, textFile: null, image: null, file: null, video: null,
               caption: null, name: null, context: '', verbose: false };
  for (let i = 2; i < argv.length; i++) {
    const t = argv[i];
    if (t === '--text-file') a.textFile = argv[++i];
    else if (t === '--image') a.image = argv[++i];
    else if (t === '--file') a.file = argv[++i];
    else if (t === '--video') a.video = argv[++i];
    else if (t === '--caption') a.caption = argv[++i];
    else if (t === '--name') a.name = argv[++i];
    else if (t === '--context' || t === '--ctx') a.context = argv[++i] || '';
    else if (t === '--verbose' || t === '-v') a.verbose = true;
    else if (t.startsWith('--')) { /* 忽略未知选项 */ }
    else if (a.text === null) a.text = t;
  }
  return a;
}

// ── 工具 ───────────────────────────────────────────────
function randomWechatUin() {
  return Buffer.from(String(crypto.randomBytes(4).readUInt32BE(0)), 'utf-8').toString('base64');
}
function buildClientId() {
  // "cbc-<时间戳>-<随机>"：必须带 cbc- 前缀，对齐 host 契约
  const rand = crypto.randomBytes(6).toString('hex');
  return `${CLIENT_ID_PREFIX}${Date.now()}-${rand}`;
}
function aesEcbEncrypt(data, key) {
  const c = crypto.createCipheriv('aes-128-ecb', key, null);
  return Buffer.concat([c.update(data), c.final()]);
}
function md5Hex(buf) { return crypto.createHash('md5').update(buf).digest('hex'); }
function buildHeaders(token) {
  // 严格对齐官方 @tencent-weixin/openclaw-weixin@2.4.6 契约：6 个头部，缺一不可
  return {
    'Content-Type': 'application/json',
    AuthorizationType: 'ilink_bot_token',
    'X-WECHAT-UIN': randomWechatUin(),
    // ⚠️ token 必须是【完整 botToken 串（含 accountId: 前缀）】，否则 errcode:-14 session timeout
    Authorization: `Bearer ${token}`,
    'iLink-App-Id': 'bot',
    'iLink-App-ClientVersion': String(ILINK_APP_CLIENT_VERSION),
  };
}
function buildBaseInfo() { return { channel_version: BASE_CHANNEL_VERSION, bot_agent: BOT_AGENT }; }
function chunkText(s, size) {
  if (s.length <= size) return [s];
  const out = [];
  for (let i = 0; i < s.length; i += size) out.push(s.slice(i, i + size));
  return out;
}

// ── 定位通道 ───────────────────────────────────────────
function findWeixinClawBot(cfg) {
  const users = cfg && cfg.claw && cfg.claw.users;
  if (users) {
    for (const uid of Object.keys(users)) {
      const channels = users[uid].channels || {};
      for (const cid of Object.keys(channels)) {
        const ch = channels[cid];
        const isTarget = cid === 'weixinClawBot' ||
          (ch && ch.baseUrl && ch.baseUrl.includes('ilinkai.weixin.qq.com'));
        if (isTarget) return { name: cid, ...ch };
      }
    }
  }
  throw new Error('weixinClawBot channel not found in settings.json');
}

// ── 读取 cursor buf（精确匹配文件名，不做任何变换）─────────
// 从 settings 的 botToken 解析 accountId（@im.bot: 之前那段），
// 直接拼出唯一文件名读取，避免多份游标文件时选错。
function loadContextToken(channel) {
  try {
    if (!fs.existsSync(CLAW_STATE_DIR)) { dbg('loadContextToken: 目录不存在'); return ''; }
    const accountId = (channel.botToken || '').split('@')[0];
    const exact = accountId ? `${accountId}_im.bot.cursor.json` : null;
    const exactPath = exact ? path.join(CLAW_STATE_DIR, exact) : null;

    let fileUsed = null;
    if (exactPath && fs.existsSync(exactPath)) {
      fileUsed = exactPath;
    } else {
      // 退化：目录里若恰好只有一份，也允许直接用（兼容拿不到 accountId 的极端情况）
      const files = fs.readdirSync(CLAW_STATE_DIR).filter((f) => f.endsWith('_im.bot.cursor.json'));
      if (files.length === 1) fileUsed = path.join(CLAW_STATE_DIR, files[0]);
      else { dbg('loadContextToken: 找不到匹配', accountId, '的 cursor 文件'); return ''; }
    }
    const j = JSON.parse(fs.readFileSync(fileUsed, 'utf-8'));
    const buf = j.get_updates_buf || '';
    dbg('loadContextToken: 来源', path.basename(fileUsed), 'buf长度', buf.length);
    return buf;
  } catch (e) {
    dbg('loadContextToken 失败:', e.message);
    return '';
  }
}

// ── 底层 POST ───────────────────────────────────────────
async function ilinkPost(channel, endpoint, body, timeout = 15000) {
  const base = channel.baseUrl || 'https://ilinkai.weixin.qq.com';
  const url = new URL(endpoint, base.endsWith('/') ? base : base + '/').toString();
  body.base_info = buildBaseInfo();
  const res = await fetch(url, {
    method: 'POST',
    headers: buildHeaders(channel.botToken),
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(timeout),
  });
  const raw = await res.text();
  dbg(`POST ${endpoint} -> ${res.status}`, VERBOSE ? raw : '');
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${raw}`);
  let json = {};
  try { json = JSON.parse(raw); } catch { /* 空响应 = 成功 */ }
  if (json && json.ret && json.ret !== 0) throw new Error(`API ret=${json.ret} errmsg=${json.errmsg}`);
  if (json && json.errcode && json.errcode !== 0) throw new Error(`API errcode=${json.errcode} errmsg=${json.errmsg}`);
  return json;
}

// ── 发送文本（自动分片）──────────────────────────────────
async function sendText(channel, to, text, ctx) {
  const chunks = chunkText(text, 4000);
  for (const c of chunks) {
    await ilinkPost(channel, 'ilink/bot/sendmessage', {
      msg: {
        from_user_id: '', to_user_id: to, client_id: buildClientId(),
        message_type: 2, message_state: 2,
        item_list: [{ type: 1, text_item: { text: c } }],
        context_token: ctx,
      },
    });
  }
  return chunks.length;
}

// ── 媒体上传（CDN + AES-128-ECB）────────────────────────
async function uploadMedia(channel, filePath, to, mediaType) {
  if (!fs.existsSync(filePath)) throw new Error(`文件不存在: ${filePath}`);
  const aesKey = crypto.randomBytes(16);
  const aesKeyHex = aesKey.toString('hex');
  let raw = fs.readFileSync(filePath);
  // 文本类文件补 UTF-8 BOM，避免 Windows/微信查看器按 GBK 解码导致中文乱码
  if (mediaType === 3) {
    const ext = path.extname(filePath).toLowerCase();
    if (['.txt', '.md', '.csv', '.log', '.json', '.xml', '.yml', '.yaml', '.text'].includes(ext)) {
      if (raw.length < 3 || raw[0] !== 0xEF || raw[1] !== 0xBB || raw[2] !== 0xBF) {
        raw = Buffer.concat([Buffer.from([0xEF, 0xBB, 0xBF]), raw]);
        dbg('preset UTF-8 BOM for text file');
      }
    }
  }
  const rawSize = raw.length;
  const rawMd5 = md5Hex(raw);
  const cipher = aesEcbEncrypt(raw, aesKey);
  const cipherSize = cipher.length;
  const filekey = aesKeyHex;

  const resp = await ilinkPost(channel, 'ilink/bot/getuploadurl', {
    filekey, media_type: mediaType, to_user_id: to,
    rawsize: rawSize, rawfilemd5: rawMd5, filesize: cipherSize,
    no_need_thumb: true, aeskey: aesKeyHex,
  }, 20000);
  dbg('getuploadurl resp keys=', Object.keys(resp));

  const uploadFullUrl = (resp.upload_full_url || '').trim();
  const uploadParam = resp.upload_param;
  let cdnUrl;
  if (uploadFullUrl) cdnUrl = uploadFullUrl;
  else if (uploadParam) cdnUrl = `${CDN_BASE_URL}/upload?encrypted_query_param=${encodeURIComponent(uploadParam)}&filekey=${encodeURIComponent(filekey)}`;
  else throw new Error('getuploadurl 未返回 upload_full_url / upload_param');

  const cdnRes = await fetch(cdnUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/octet-stream' },
    body: new Uint8Array(cipher),
    signal: AbortSignal.timeout(120000),
  });
  dbg('CDN upload ->', cdnRes.status);
  if (cdnRes.status >= 400 && cdnRes.status < 500) {
    const msg = cdnRes.headers.get('x-error-message') || (await cdnRes.text().catch(() => ''));
    throw new Error(`CDN 上传客户端错误 ${cdnRes.status}: ${msg}`);
  }
  if (!cdnRes.ok) {
    const msg = cdnRes.headers.get('x-error-message') || `status ${cdnRes.status}`;
    throw new Error(`CDN 上传失败 ${cdnRes.status}: ${msg}`);
  }
  const downloadParam = cdnRes.headers.get('x-encrypted-param');
  if (!downloadParam) throw new Error('CDN 响应缺少 x-encrypted-param');

  return {
    encrypt_query_param: downloadParam,
    aes_key_b64: Buffer.from(aesKeyHex).toString('base64'),
    cipher_size: cipherSize,
    raw_size: rawSize,
  };
}

async function sendImage(channel, to, filePath, caption, ctx) {
  const m = await uploadMedia(channel, filePath, to, 1);
  const items = [];
  if (caption) items.push({ type: 1, text_item: { text: caption } });
  items.push({ type: 2, image_item: { media: { encrypt_query_param: m.encrypt_query_param, aes_key: m.aes_key_b64, encrypt_type: 1 }, mid_size: m.cipher_size } });
  await sendMediaItems(channel, to, items, ctx, 'sendImage');
}
async function sendFile(channel, to, filePath, fileName, caption, ctx) {
  const m = await uploadMedia(channel, filePath, to, 3);
  const items = [];
  if (caption) items.push({ type: 1, text_item: { text: caption } });
  items.push({ type: 4, file_item: { media: { encrypt_query_param: m.encrypt_query_param, aes_key: m.aes_key_b64, encrypt_type: 1 }, file_name: fileName, len: String(m.raw_size) } });
  await sendMediaItems(channel, to, items, ctx, 'sendFile');
}
async function sendVideo(channel, to, filePath, caption, ctx) {
  const m = await uploadMedia(channel, filePath, to, 2);
  const items = [];
  if (caption) items.push({ type: 1, text_item: { text: caption } });
  items.push({ type: 5, video_item: { media: { encrypt_query_param: m.encrypt_query_param, aes_key: m.aes_key_b64, encrypt_type: 1 }, video_size: m.cipher_size } });
  await sendMediaItems(channel, to, items, ctx, 'sendVideo');
}
async function sendMediaItems(channel, to, items, ctx, label) {
  for (const item of items) {
    await ilinkPost(channel, 'ilink/bot/sendmessage', {
      msg: { from_user_id: '', to_user_id: to, client_id: buildClientId(), message_type: 2, message_state: 2, item_list: [item], context_token: ctx },
    });
  }
  dbg(label, 'sent', items.length, 'items');
}

// ── main ────────────────────────────────────────────────
(async () => {
  const a = parseArgs(process.argv);
  VERBOSE = a.verbose;
  if (!fs.existsSync(SETTINGS_PATH)) throw new Error(`settings.json not found at ${SETTINGS_PATH}`);
  const cfg = JSON.parse(fs.readFileSync(SETTINGS_PATH, 'utf-8'));
  const channel = findWeixinClawBot(cfg);
  if (!channel.botToken) throw new Error('settings.json 中 weixinClawBot 缺少 botToken');
  if (!channel.userId) throw new Error('settings.json 中 weixinClawBot 缺少 userId（老板的 im.wechat id）');
  const to = channel.userId;

  // ── context_token 策略 ─────────────────────────────────
  // 文本：默认【空串】即可发送（无需 cursor、无需激活）。
  // 媒体（图片/文件/视频）：【必须】带非空 token → 从 cursor 读 get_updates_buf。
  // --context 显式传入 → 任何类型都优先用它覆盖。
  const isMedia = !!(a.image || a.video || a.file);
  const explicitCtx = !!a.context;
  let ctx = a.context || '';
  const ctxSrc = explicitCtx ? 'override' : (isMedia ? 'cursor_buf' : 'empty');
  if (!ctx && isMedia) {
    ctx = loadContextToken(channel);
    if (!ctx) {
      console.error('[weixinclaw] ⚠️ 媒体推送需要非空 context_token，但 claw-state/weixin 下无有效 cursor buf。');
      console.error('[weixinclaw] 【必须】请先到微信给 ClawBot 发一条消息激活（host 才会写出/刷新游标），');
      console.error('[weixinclaw]        激活后再重跑本命令即可；或用 --context <token> 显式传入已知有效的 token。');
      process.exit(2);
    }
  }
  // ⚠️ 只打印长度，绝不打印 token 明文
  console.log(`[weixinclaw] channel=${channel.name} to=${to} mode=proactive ctx_src=${ctxSrc} ctx_len=${ctx.length}`);

  let n = 0;
  let label = '';
  if (a.image) {
    await sendImage(channel, to, a.image, a.caption || '', ctx); label = '图片';
  } else if (a.video) {
    await sendVideo(channel, to, a.video, a.caption || '', ctx); label = '视频';
  } else if (a.file) {
    await sendFile(channel, to, a.file, a.name || path.basename(a.file), a.caption || '', ctx); label = '文件';
  } else if (a.textFile) {
    const t = fs.readFileSync(a.textFile, 'utf-8').replace(/\r\n/g, '\n').trim();
    n = await sendText(channel, to, t, ctx); label = '文本';
  } else if (a.text != null) {
    n = await sendText(channel, to, a.text, ctx); label = '文本';
  } else {
    n = await sendText(channel, to, '🦐 ClawBot 微信主动推送测试：若你在微信里单独收到这条 bot 消息（不是对话气泡），说明主动推送已打通。', ctx); label = '文本';
  }

  console.log(`[weixinclaw] OK — 已推送 ${label}（${n} 条消息），请老板在微信确认是否收到 ClawBot 推送。`);
})().catch((e) => {
  const isCtx = e.message.includes('ret=-2');
  console.error('[weixinclaw] FAILED:', e.message);
  if (isCtx) {
    console.error('');
    console.error('[weixinclaw] ⚠️ 推送被拒（ret:-2）：会话已失效 / 底层 bot id 已轮换，不可发送。');
    console.error('[weixinclaw]    （文本平时用空 token 即可；一旦文本也被拒，大概率是 bot id 变了，同样需激活。）');
    console.error('[weixinclaw] 【必须】请先到微信，给 ClawBot 发一条任意消息（激活 host 的发送游标），');
    console.error('[weixinclaw]         激活后再重跑本命令即可，send.js 会自动读取刷新后的最新 buf。');
  }
  process.exit(1);
});
