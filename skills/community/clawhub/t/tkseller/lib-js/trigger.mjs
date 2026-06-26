/**
 * TKSeller 入口脚本:登录 / 推荐 / 启动轮询。
 *
 * 用法:
 *   node trigger.mjs "<老板原始消息文本>"
 *
 * 支持的消息形态:
 *   /tkseller                       → 热门推荐
 *   /tkseller url:https://...       → 指定视频
 *   /推荐 https://...                → 指定视频
 *   推荐 https://...                 → 指定视频
 *   https://...                      → 指定视频
 *   alice 密码                       → 登录(不需要"登录"二字)
 *   alice 123456                    → 登录(账号 密码两个词)
 */
import { existsSync, mkdirSync, writeFileSync, readFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';
import { homedir } from 'os';
import * as api from './api.mjs';
import * as ct from './card-tools.mjs';
import { send as sendPersonaCard } from './send-persona-card.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// ========== 数字人检查 ==========
const PERSONA_LOCK_PATH = join(dirname(fileURLToPath(import.meta.url)), '..', 'data', 'persona_pending.json');

function isPersonaPending() {
  try {
    if (!existsSync(PERSONA_LOCK_PATH)) return false;
    const d = JSON.parse(readFileSync(PERSONA_LOCK_PATH, 'utf-8'));
    // 5分钟超时自动失效
    if (d.ts && (Date.now() / 1000 - d.ts) > 300) return false;
    return d.pending === true;
  } catch { return false; }
}

async function checkPersona() {
  // 如果正在创建数字人,返回特殊标记(不发卡片也不跳过)
  if (isPersonaPending()) return 'PENDING';
  try {
    const resp = await api.personaActive();
    if (resp.ok && resp.persona) {
      if (resp.persona.confirmed) return resp.persona; // 已确认,可以带货
      return 'UNCONFIRMED'; // 有数字人但未确认
    }
    return null; // 没有数字人
  } catch { return null; }
}

async function sendExistingPersonaForReview() {
  // 拉服务端已有的数字人信息,发审核卡片让用户确认
  let persona = null;
  try {
    const resp = await api.personaActive();
    if (resp.ok && resp.persona) persona = resp.persona;
  } catch { /* */ }
  if (!persona) {
    await sendPersonaCard();
    return;
  }
  const name = persona.name || '数字人';
  const description = persona.description || '';
  const imageUrl = persona.frontal_image || '';
  const personaId = persona.id || null;

  const text =
    `🎭 **你已有一个数字人,请确认是否使用:**\n\n` +
    `**名称:** ${name}\n` +
    `**描述:** ${description}`;

  let confirmLabel = '✅ 确认使用';
  if (personaId) confirmLabel = `✅ 确认使用 #${personaId}`;

  const buttons = [
    { label: confirmLabel, style: 'success' },
    { label: '🔄 重新生成', style: 'primary' },
  ];

  try {
    await ct.sendCard(text, imageUrl, buttons, '数字人正面照');
  } catch (e) {
    // 发卡片失败(渠道配置问题),输出提示让 LLM 转发
    throw new Error(`__FORWARD__:⚠️ 发送卡片失败(${e.message})。\n请检查 Discord 渠道配置是否正确:\n1. Bot Token 是否有效\n2. Bot 是否已加入服务器\n3. 频道配置是否完整`);
  }
}

// 根据渠道配置动态生成登录提示
function getLoginHint() {
  const { channel } = ct.detectChannel();

  // Discord 默认需要 @bot,除非明确设了 requireMention: false
  if (channel === 'discord') {
    let mentionDisabled = false;
    try {
      const cfg = ct._openclawCfg();
      const chCfg = (cfg.channels || {}).discord;
      if (chCfg) {
        // 频道级优先
        const guilds = chCfg.guilds || {};
        for (const g of Object.values(guilds)) {
          for (const c of Object.values(g.channels || {})) {
            if (c.requireMention === false) mentionDisabled = true;
          }
        }
        // 频道级没设则看顶层
        if (!mentionDisabled && chCfg.requireMention === false) mentionDisabled = true;
      }
    } catch { /* */ }

    if (mentionDisabled) {
      return '🔑 欢迎使用 TKSeller。\n' +
        '请回复:`登录 用户名 密码`\n' +
        '例如:`登录 myname 123456`';
    } else {
      return '🔑 欢迎使用 TKSeller。\n' +
        '请 @我 发送登录指令:\n' +
        '例如:`@bot 登录 myname 123456`';
    }
  }

  // 其他渠道不需要 @bot
  return '🔑 欢迎使用 TKSeller。\n' +
    '请回复:`登录 用户名 密码`\n' +
    '例如:`登录 myname 123456`';
}

// ========== 解析 ==========
function extractUrl(msg) {
  if (!msg) return null;
  let s = msg.trim();
  s = s.replace(/^\s*(?:\/tkseller|\/tkseller|\/推荐|推荐|来一个)\s*/i, '');
  s = s.replace(/^\s*url\s*[::]\s*/i, '');
  s = s.trim().replace(/^[<>]+|[<>]+$/g, '').replace(/^["'「」『』]+|["'「」『』]+$/g, '').trim();
  if (/^https?:\/\//i.test(s)) return s;
  return null;
}

function extractLogin(msg) {
  if (!msg) return null;
  // 格式:登录 用户名 密码(必须有"登录"/"login"前缀,避免跟普通聊天混淆)
  const m = msg.trim().match(/^\s*(?:登录|login)\s+(\S+)\s+(\S+)\s*$/i);
  if (m) {
    const [, user, pwd] = m;
    if (user.startsWith('/') || user.startsWith('http')) return null;
    return [user, pwd];
  }
  return null;
}

// ========== 推荐 ==========
async function doRecommend(url) {
  // 双重检查:没 token 绝对不往下走
  if (!api.hasToken()) {
    await ct.sendText(getLoginHint());
    return { ok: false, reason: 'not_logged_in' };
  }
  // 先调 API,成功后再发 ack,避免未登录/失败时也发"已启动"
  let resp;
  try {
    resp = await api.recommend(url);
  } catch (e) {
    if (e instanceof api.InvalidToken) {
      await ct.sendText('❌ 身份已过期,请重新发送账号和密码(空格隔开),例:`myname 123456`');
      return { ok: false, reason: 'invalid_token' };
    }
    if (e instanceof api.ApiError) {
      await ct.sendText(`❌ 推荐启动失败:${e.message}`);
      return { ok: false, reason: 'api_error', detail: e.message };
    }
    throw e;
  }

  // API 成功后才发 ack
  if (url) {
    await ct.sendText(`⏳ 指定视频已接收,正在抓取分析,完成后给您发审核卡片。\n${url}`);
  } else {
    await ct.sendText('⏳ 已启动热门推荐,找到合适的视频再给您发审核卡片。');
  }

  try {
    await ct.cronStartPolling();
  } catch (e) {
    await ct.sendText(`⚠️ 轮询任务启动失败:${e.message}\n请告诉老板。`);
    return { ok: false, reason: 'cron_start_failed', recommend_resp: resp, detail: e.message };
  }

  return { ok: true, mode: url ? 'url' : 'trending', recommend_resp: resp };
}

// ========== 登录 ==========
async function doLogin(username, password) {
  try {
    const resp = await api.login(username, password);
    if (!resp.ok) {
      await ct.sendText(`❌ 账号验证失败:${resp.error || 'unknown'}`);
      return { ok: false, reason: 'server_reject', detail: resp };
    }
    await ct.sendText(`✅ 登录成功(用户:${username})`);
    return { ok: true, username };
  } catch (e) {
    if (e instanceof api.InvalidToken) {
      await ct.sendText('❌ 账号或密码错误,请确认后重试。');
      return { ok: false, reason: 'invalid_credentials' };
    }
    if (e instanceof api.ApiError) {
      await ct.sendText(`❌ 账号验证失败:${e.message}`);
      return { ok: false, reason: 'api_error', detail: e.message };
    }
    await ct.sendText(`❌ 验证请求异常:${e.message}`);
    return { ok: false, reason: 'exception', detail: e.message };
  }
}

// ========== Discord 命令自动注册(仅 Discord 渠道) ==========
const REGISTERED_FLAG = join(dirname(__dirname), 'data', 'registered');

function _autoRegister() {
  // 检查用户是否配置了 Discord(不管当前触发来源是什么渠道)
  try {
    const cfg = JSON.parse(readFileSync(join(homedir(), '.openclaw', 'openclaw.json'), 'utf-8'));
    const discordCfg = cfg?.channels?.discord;
    if (!discordCfg || !discordCfg.token || discordCfg.token.length < 10) {
      return { registered: false, reason: 'discord_not_configured' };
    }
  } catch {
    return { registered: false, reason: 'config_read_error' };
  }
  if (existsSync(REGISTERED_FLAG)) return { registered: false, reason: 'already_registered' };
  try {
    const script = join(__dirname, 'register-discord.mjs');
    const output = execSync(`"${process.execPath}" "${script}"`, {
      timeout: 30000,
      encoding: 'utf-8',
    });
    // 检查注册结果,只有成功才写标记
    try {
      const result = JSON.parse(output);
      if (!result.ok) return { registered: false, reason: 'register_failed', output };
    } catch { /* 解析失败也不写标记 */
      return { registered: false, reason: 'parse_failed', output };
    }
    mkdirSync(dirname(REGISTERED_FLAG), { recursive: true });
    writeFileSync(REGISTERED_FLAG, '1', 'utf-8');
    return { registered: true, output };
  } catch (e) {
    return { registered: false, reason: 'error', error: e.message };
  }
}

// ========== 轮询进程自动恢复 ==========
async function _autoRecoverPoll() {
  try {
    const state = ct.pollStateLoad();
    if (!state.active) return;
    // 检查进程是否存活(通过 startPollProcess 内部幂等逻辑处理)
    await ct.startPollProcess();
  } catch { /* */ }
}

// ========== 主入口 ==========
async function main(rawMsg) {
  const msg = rawMsg || '';

  // ====== 第一步：检测渠道配置是否完整（必须能发出消息才继续）======
  const { channel, target } = ct.detectChannel();

  // 情况1：完全没配渠道（没 token）
  if (!channel) {
    return {
      ok: false,
      reason: 'no_channel',
      __forward_text__:
        '⚠️ 你还没有配置消息渠道。\n\n' +
        '📖 配置教程: https://docs.openclaw.ai/channels/discord\n\n' +
        '按文档里的 Quick setup 走完 6 步（创建 Discord 应用、拿 Bot Token、邀请加服务器、粘贴到 OpenClaw）。\n' +
        '配置完成后再发 `/tkseller` 或 `带货` 即可开始使用。',
    };
  }

  // 情况2：有渠道但没有 target（有 token 但没配 guilds/频道）
  // 先尝试从活跃 session 里找 target
  let resolvedTarget = target;
  if (!resolvedTarget) {
    const fromSessions = await ct.detectChannelFromSessions();
    if (fromSessions && fromSessions.target) {
      resolvedTarget = fromSessions.target;
      ct.setRuntimeChannel(fromSessions.channel, fromSessions.target);
    }
  }

  // 还是没有 target → 配置不完整，直接告诉用户
  if (!resolvedTarget) {
    return {
      ok: false,
      reason: 'no_target',
      __forward_text__:
        '⚠️ Discord 渠道配置不完整。\n\n' +
        'Bot Token 已配置，但缺少频道信息。请在 OpenClaw 配置文件中添加 `guilds` 配置：\n\n' +
        '```json\n' +
        '"discord": {\n' +
        '  "guilds": {\n' +
        '    "*": {\n' +
        '      "channels": {\n' +
        '        "你的频道ID": { "requireMention": false }\n' +
        '      }\n' +
        '    }\n' +
        '  }\n' +
        '}\n' +
        '```\n\n' +
        '频道ID 获取方法：Discord 设置 → 开启开发者模式 → 右键频道 → 复制频道ID。\n' +
        '配置完成后重启网关(`openclaw gateway restart`)再试。',
    };
  }

  // 情况3：有 target，探测渠道是否真的能发出去
  const probeStatus = await ct.sendText('\u200b');
  if (probeStatus === 0 || probeStatus >= 400) {
    return {
      ok: false,
      reason: 'channel_unreachable',
      __forward_text__:
        '⚠️ Discord 已配置但连接失败(Bot 可能未上线或 Token 无效)。\n\n' +
        '请检查：\n' +
        '1. Bot Token 是否正确\n' +
        '2. Bot 是否已加入服务器\n' +
        '3. 网络/代理是否正常\n\n' +
        '确认后重启网关(`openclaw gateway restart`)再试。',
    };
  }

  // 首次触发自动注册(静默执行,不发消息给用户,不中断流程)
  _autoRegister();

  // 恢复轮询
  await _autoRecoverPoll();

  // 0) 按钮回调统一入口:任何按钮点击都转发给 handle-button 处理
  // 匹配:Clicked 前缀 / 数字人预设 label / 审核按钮 label / 确认使用 / 跳过 / 重新生成
  const BUTTON_PATTERNS = [
    /^Clicked\s+/i,
    /^👩\s/,  // 👩 亚洲女 / 欧美女 / 拉丁裔女
    /^👨\s/,  // 👨 亚洲男 / 欧美男 / 拉丁裔男
    /^✅\s/,   // ✅ 做 / ✅ 分镜通过 / ✅ 通过 / ✅ 确认使用
    /^⏭️\s/,  // ⏭️ 换一个 / ⏭️ 跳过
    /^🔄\s/,  // 🔄 换商品 / 🔄 重新生成 / 重做
    /^❌\s/,   // ❌ 放弃
    /^📝\s/,  // 📝 自定义
    /^Form\s+["'""「」]?自定义数字人/,  // Modal 提交
  ];
  if (BUTTON_PATTERNS.some(p => p.test(msg))) {
    const { main: handleButton } = await import('./handle-button.mjs');
    // 去掉 Clicked 前缀和引号
    const label = msg.replace(/^Clicked\s+["'""]?/i, '').replace(/["'""]?\s*$/, '').trim();
    return await handleButton(label || msg);
  }

  // 1) 优先识别登录
  const loginInfo = extractLogin(msg);
  if (loginInfo) {
    const [username, password] = loginInfo;
    const result = await doLogin(username, password);
    if (!result.ok) return result;
    // 检查数字人
    const persona = await checkPersona();
    if (persona === 'PENDING') {
      // 正在创建中,不发卡片也不进推荐
      return { ok: true, login: result, awaiting_persona: true };
    }
    if (persona === 'UNCONFIRMED') {
      // 服务端有数字人但用户没审核,发审核卡片
      await sendExistingPersonaForReview();
      return { ok: true, login: result, awaiting_persona: true };
    }
    if (!persona) {
      await sendPersonaCard();
      return { ok: true, login: result, awaiting_persona: true };
    }
    // 登录成功+有数字人已确认 → 提示后直接开始推荐
    await ct.sendText(`✅ 已检测到数字人,开始推荐商品...`);
    return doRecommend(null);
  }

  // 2) 未登录
  if (!api.hasToken()) {
    await ct.sendText(getLoginHint());
    return { ok: false, reason: 'not_logged_in' };
  }

  // 3) 检查数字人
  const persona = await checkPersona();
  if (persona === 'PENDING') {
    // 正在创建中,不发卡片也不进推荐
    return { ok: true, awaiting_persona: true };
  }
  if (persona === 'UNCONFIRMED') {
    // 服务端有数字人但用户没审核,发审核卡片
    await sendExistingPersonaForReview();
    return { ok: true, awaiting_persona: true };
  }
  if (!persona) {
    await sendPersonaCard();
    return { ok: true, awaiting_persona: true };
  }

  // 4) 推荐流程
  const url = extractUrl(msg);
  if (!url && !msg.trim().startsWith('/')) {
    const plain = msg.trim().toLowerCase();
    if (['tkseller', 'tkseller', '带货', '开始', '推荐'].includes(plain)) {
      await ct.sendText('✅ 准备就绪,发 `/tkseller` 开始带货吧!');
      return { ok: true, hint_only: true };
    }
  }
  return doRecommend(url);
}

// CLI 入口
// 用法: node trigger.mjs "<消息>" [<channel>] [<target>]
// channel 可选:discord / feishu / telegram / slack 等
// 注意:PowerShell 会吞掉空字符串 ""  导致参数错位,所以用智能检测
const KNOWN_CHANNELS = ['discord', 'feishu', 'telegram', 'slack', 'whatsapp', 'signal', 'wecom', 'msteams', 'mattermost', 'line', 'qqbot', 'webchat'];

let rawArg = '';
let channelArg = '';
let targetArg = '';

// 智能解析参数:找到哪个是 channel,哪个是 target,剩下的是消息
const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  const a = args[i].trim();
  if (!channelArg && KNOWN_CHANNELS.includes(a.toLowerCase())) {
    channelArg = a.toLowerCase();
  } else if (!targetArg && (a.startsWith('channel:') || a.startsWith('user:') || a.match(/^\d{10,}$/))) {
    targetArg = a;
  } else if (!rawArg && a) {
    rawArg = a;
  }
}
if (channelArg && channelArg !== 'webchat') {
  // LLM 明确指定了外部渠道(discord/feishu/telegram 等)
  ct.setRuntimeChannel(channelArg, targetArg || null);
} else {
  // webchat 或未传渠道参数 → 自动检测用户配置的外部渠道
  const detected = await ct.detectChannelFromSessions();
  if (detected) {
    ct.setRuntimeChannel(detected.channel, detected.target);
  }
  // 如果检测不到,detectChannel() 会读配置文件兜底
}
const isWebchat = !channelArg || channelArg === 'webchat';
main(rawArg).then(out => {
  if (out && out.__forward_text__) {
    console.log('OUTPUT_AS_REPLY:' + out.__forward_text__);
  } else if (out && out.awaiting_persona) {
    // 数字人正在生成/等待审核,卡片已发到渠道
    console.log('OUTPUT_AS_REPLY:✅ 收到');
  } else if (out && out.ok === false && out.reason === 'not_logged_in') {
    // 登录提示已发到渠道
    console.log('OUTPUT_AS_REPLY:✅ 收到');
  } else if (out && out.hint_only) {
    // 提示已发到渠道
    console.log('OUTPUT_AS_REPLY:✅ 收到');
  } else if (out && out.ok !== false) {
    // 流程正常启动,消息已发到渠道
    console.log('OUTPUT_AS_REPLY:✅ 收到');
  } else {
    // 其他失败情况,消息已通过 sendText 发到渠道
    console.log('OUTPUT_AS_REPLY:✅ 收到');
  }
}).catch(e => {
  if (e.message && e.message.startsWith('__FORWARD__:')) {
    console.log('OUTPUT_AS_REPLY:' + e.message.replace('__FORWARD__:', ''));
  } else {
    console.log('OUTPUT_AS_REPLY:⚠️ 执行异常,请稍后重试。');
  }
  process.exit(1);
});
