/**
 * 按钮回调:从 Discord 点击 label 提取 short_id → 查映射 → 调对应 /api/v1/* 接口。
 *
 * 用法:
 *   node handle-button.mjs "<clicked_label>"
 * 例:
 *   node handle-button.mjs "✅ 做 #4"
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync, unlinkSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import * as api from './api.mjs';
import * as ct from './card-tools.mjs';
import { PERSONA_PRESETS, send as sendPersonaCard } from './send-persona-card.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// ========== 数字人状态锁 ==========
const PERSONA_LOCK_PATH = join(dirname(__dirname), 'data', 'persona_pending.json');

function _setPersonaPending() {
  mkdirSync(dirname(PERSONA_LOCK_PATH), { recursive: true });
  writeFileSync(PERSONA_LOCK_PATH, JSON.stringify({ pending: true, ts: Math.floor(Date.now() / 1000) }), 'utf-8');
}

function _clearPersonaPending() {
  try { if (existsSync(PERSONA_LOCK_PATH)) unlinkSync(PERSONA_LOCK_PATH); } catch { /* */ }
}

// ========== 按钮去重 ==========
const DEDUP_PATH = join(dirname(__dirname), 'data', 'button_dedup.json');
const DEDUP_WINDOW_SEC = 60;

function _loadDedup() {
  if (!existsSync(DEDUP_PATH)) return {};
  try { return JSON.parse(readFileSync(DEDUP_PATH, 'utf-8')); }
  catch { return {}; }
}

function _saveDedup(d) {
  mkdirSync(dirname(DEDUP_PATH), { recursive: true });
  writeFileSync(DEDUP_PATH, JSON.stringify(d), 'utf-8');
}

function _checkAndMarkDedup(shortId, action) {
  const key = `${shortId}:${action}`;
  let d = _loadDedup();
  const now = Math.floor(Date.now() / 1000);
  // 清理过期
  const cleaned = {};
  for (const [k, v] of Object.entries(d)) {
    if (now - Number(v) < DEDUP_WINDOW_SEC) cleaned[k] = v;
  }
  d = cleaned;
  if (d[key]) {
    _saveDedup(d);
    return true;
  }
  d[key] = now;
  _saveDedup(d);
  return false;
}

// (action_key, progress_template_or_null)
const BUTTON_MAP = {
  '✅ 做分镜': ['approve', '#{short_id} 开始生成分镜图,预计 5 分钟左右,请稍候...'],
  '⏭️ 换视频': ['change_video', null],
  '⏭️ 换一个': ['change_all', null],
  '🔄 换商品': ['change_product', '🔄 正在重新匹配商品...'],
  '✅ 分镜通过': ['approve', '⏳ 分镜已确认,正在生成视频提示词和视频,预计8-10分钟...'],
  '🔄 重新生成': ['redo', '🔄 正在重新生成分镜图...'],
  '❌ 放弃': ['reject', '❌ 已放弃视频 #{short_id}'],
  '✅ 通过': ['approve', '📤 视频 #{short_id} 正在提交发布...'],
  '🔄 重做': ['redo', '🔄 视频 #{short_id} 重新生成中...'],
};

function matchButton(label) {
  const m = label.match(/#(\d+)/);
  const shortId = m ? m[1] : null;
  const prefix = label.replace(/\s*#\d+\s*$/, '').trim();
  return [prefix, shortId];
}

async function callApiFor(action, videoId, step) {
  if (action === 'approve') return api.taskApprove(videoId, step);
  if (action === 'reject') return api.taskReject(videoId);
  if (action === 'change_product') return api.taskChangeProduct(videoId);
  if (action === 'redo') {
    if (step === 'review_1_5') return api.taskStoryboardRedo(videoId);
    if (step === 'review_2') return api.taskVideoRedo(videoId);
    throw new Error(`redo 不支持 step=${step}`);
  }
  throw new Error(`未知 action: ${action}`);
}

async function _sendPersonaResult(name, description, imageUrl, personaId = null) {
  const text =
    `✅ **数字人生成完成!**\n\n` +
    `**名称:** ${name}\n` +
    `**描述:** ${description}`;

  let confirmLabel = '✅ 确认使用';
  if (personaId) confirmLabel = `✅ 确认使用 #${personaId}`;

  const buttons = [
    { label: confirmLabel, style: 'success' },
    { label: '🔄 重新生成', style: 'primary' },
  ];

  // 用统一 sendCard 发送(自动适配渠道)
  try {
    await ct.sendCard(text, imageUrl || '', buttons, '数字人正面照');
  } catch { /* */ }
}

export async function main(clickedLabel) {
  const stripped = clickedLabel.trim();

  // ========== 自定义数字人 Modal 提交 ==========
  // 触发消息形如：
  //   Form "自定义数字人" submitted.
  //   - 描述你想要的数字人形象: 23岁长发女生
  const formMatch = stripped.match(/Form\s+["'""「」]?自定义数字人["'""「」]?\s*submitted[\s\S]*?[:：]\s*([^\r\n]+)\s*$/);
  if (formMatch) {
    const customDesc = formMatch[1].trim();
    if (!customDesc) {
      await ct.sendText('⚠️ 描述为空，请重新填写。');
      return { action: 'persona_create_custom', error: 'empty_description' };
    }
    const dedupKey = 'custom:' + customDesc.substring(0, 32);
    if (_checkAndMarkDedup('persona', dedupKey)) {
      return { action: 'persona_create_custom', desc: customDesc, skipped: true, reason: 'duplicate_submit' };
    }
    _setPersonaPending();
    await ct.sendText(`⏳ 正在生成你的专属数字人（自定义），约 3 分钟...`);
    try {
      const resp = await api.personaCreate(customDesc);
      if (!resp.ok) {
        _clearPersonaPending();
        await ct.sendText(`❌ 数字人生成提交失败：${JSON.stringify(resp)}`);
        return { action: 'persona_create_custom', desc: customDesc, error: 'submit_failed' };
      }
      // 异步生成，启动轮询等 persona_created 事件
      await ct.cronStartPolling();
    } catch (e) {
      _clearPersonaPending();
      if (e instanceof api.InvalidToken) {
        await ct.sendText('❌ 身份已过期，请重新发送账号和密码（空格隔开），例：`myname 123456`');
      } else if (e instanceof api.ApiError) {
        await ct.sendText(`❌ 数字人生成失败：${e.message}`);
      } else {
        await ct.sendText(`❌ 数字人生成异常：${e.message}`);
      }
      return { action: 'persona_create_custom', desc: customDesc, error: e.message };
    }
    return { action: 'persona_create_custom', desc: customDesc, polling: true };
  }

  // ========== 数字人卡片按钮 ==========
  if (stripped in PERSONA_PRESETS) {
    if (_checkAndMarkDedup('persona', stripped)) {
      return { action: 'persona_create', preset: stripped, skipped: true, reason: 'duplicate_click' };
    }
    const desc = PERSONA_PRESETS[stripped];
    _setPersonaPending();
    await ct.sendText(`⏳ 正在生成你的专属数字人 (${stripped})，约 3 分钟...`);
    try {
      const resp = await api.personaCreate(desc);
      if (!resp.ok) {
        _clearPersonaPending();
        await ct.sendText(`❌ 数字人生成提交失败：${JSON.stringify(resp)}`);
        return { action: 'persona_create', preset: stripped, error: 'submit_failed' };
      }
      // 异步生成，启动轮询等 persona_created 事件
      await ct.cronStartPolling();
    } catch (e) {
      _clearPersonaPending();
      if (e instanceof api.InvalidToken) {
        await ct.sendText('❌ 身份已过期，请重新发送账号和密码（空格隔开），例：`myname 123456`');
      } else if (e instanceof api.ApiError) {
        await ct.sendText(`❌ 数字人生成失败：${e.message}`);
      } else {
        await ct.sendText(`❌ 数字人生成异常：${e.message}`);
      }
      return { action: 'persona_create', preset: stripped, error: e.message };
    }
    return { action: 'persona_create', preset: stripped, polling: true };
  }

  // 跳过
  if (stripped === '⏭️ 跳过') {
    await ct.sendText('👌 已跳过数字人创建,现在可以发 `/tkseller` 或 `推荐` 开始带货。');
    return { action: 'persona_skip' };
  }

  // 确认使用数字人
  if (stripped.startsWith('✅ 确认使用')) {
    if (_checkAndMarkDedup('persona', 'confirm')) {
      return { action: 'persona_confirm', skipped: true, reason: 'duplicate_click' };
    }
    const pidMatch = clickedLabel.match(/#(\d+)/);
    // 调服务端确认接口
    try {
      await api.personaConfirm(pidMatch ? Number(pidMatch[1]) : null);
    } catch (e) {
      if (e instanceof api.InvalidToken) {
        await ct.sendText('❌ 身份已过期，请重新发送账号和密码（空格隔开），例：`myname 123456`');
        return { action: 'persona_confirm', error: 'invalid_token' };
      }
      // 非致命错误，继续流程
    }
    await ct.sendText('✅ 数字人已确认，开始推荐...\
\
💡 下次发 `@bot 带货` 或 `/tkseller` 即可开始');
    try {
      await api.recommend();
    } catch (e) {
      if (e instanceof api.InvalidToken) {
        await ct.sendText('❌ 身份已过期,请重新发送账号和密码(空格隔开),例:`myname 123456`');
        return { action: 'persona_confirm', recommend: false };
      }
      if (e instanceof api.ApiError) {
        await ct.sendText(`❌ 推荐启动失败:${e.message}`);
        return { action: 'persona_confirm', recommend: false };
      }
    }
    try { await ct.cronStartPolling(); } catch { /* */ }
    return { action: 'persona_confirm', recommend: true };
  }

  // 重新生成数字人
  if (stripped === '🔄 重新生成') {
    if (_checkAndMarkDedup('persona', 'regenerate')) {
      return { action: 'persona_regenerate', skipped: true, reason: 'duplicate_click' };
    }
    await sendPersonaCard();
    return { action: 'persona_regenerate' };
  }

  // ========== 审核卡片按钮 ==========
  const [prefix, shortId] = matchButton(clickedLabel);
  if (shortId === null) return { error: `无法从 label 提取 short_id: ${clickedLabel}` };
  if (!BUTTON_MAP[prefix]) return { error: `未知按钮前缀: ${prefix}` };

  const [action, progressTpl] = BUTTON_MAP[prefix];

  // 特殊: 换视频 (调 taskChangeVideo，保持商品不变)
  if (prefix === '⏭️ 换视频') {
    if (_checkAndMarkDedup(shortId, action)) {
      return { short_id: shortId, action, skipped: true, reason: 'duplicate_click' };
    }
    const info = ct.lookupByShortId(shortId);
    if (!info) {
      await ct.sendText(`⚠️ 按钮 #${shortId} 查不到映射(可能已过期),请老板确认。`);
      return { error: `short_id ${shortId} 不在映射` };
    }
    const videoId = info.video_id;
    const out = { short_id: shortId, video_id: videoId, action: 'change_video' };
    try {
      await api.taskChangeVideo(videoId);
    } catch (e) {
      if (e instanceof api.InvalidToken) {
        await ct.sendText('❌ 身份已过期,请重新发送账号和密码(空格隔开),例:`myname 123456`');
        await ct.cronStopPolling();
        return { ...out, error: 'invalid_token' };
      }
      await ct.sendText(`❌ 换视频失败:${e.message}`);
      return { ...out, error: e.message };
    }
    ct.removeShortId(shortId);
    await ct.cronStartPolling();
    return out;
  }

  // 特殊: 换一个 (reject + recommend，视频商品都换)
  if (prefix === '⏭️ 换一个') {
    if (_checkAndMarkDedup(shortId, action)) {
      return { short_id: shortId, action, skipped: true, reason: 'duplicate_click' };
    }
    const info = ct.lookupByShortId(shortId);
    const out = { short_id: shortId, action };
    if (info) {
      const videoId = info.video_id;
      try {
        await api.taskReject(videoId);
      } catch (e) {
        if (e instanceof api.InvalidToken) {
          await ct.sendText('❌ 身份已过期,请重新发送账号和密码(空格隔开),例:`myname 123456`');
          await ct.cronStopPolling();
          return { ...out, error: 'invalid_token' };
        }
        out.reject_error = e.message;
      }
      ct.removeShortId(shortId);
      out.video_id = videoId;
    }
    try {
      await api.recommend();
    } catch (e) {
      if (e instanceof api.InvalidToken) {
        await ct.sendText('❌ 身份已过期,请重新发送账号和密码(空格隔开),例:`myname 123456`');
        await ct.cronStopPolling();
        out.error = 'invalid_token';
        return out;
      }
      out.recommend_error = e.message;
    }
    await ct.cronStartPolling();
    return out;
  }

  // 查映射
  const info = ct.lookupByShortId(shortId);
  if (!info) {
    await ct.sendText(`⚠️ 按钮 #${shortId} 查不到映射(可能已过期),请老板确认。`);
    return { error: `short_id ${shortId} 不在映射` };
  }

  const videoId = info.video_id;
  const step = info.step;

  // 去重
  if (_checkAndMarkDedup(shortId, action)) {
    return { short_id: shortId, video_id: videoId, step, action, skipped: true, reason: 'duplicate_click' };
  }

  // 发进度
  if (progressTpl) {
    await ct.sendText(progressTpl.replace(/\{short_id\}/g, shortId));
  }

  // 调 API
  let resp;
  try {
    resp = await callApiFor(action, videoId, step);
  } catch (e) {
    if (e instanceof api.InvalidToken) {
      await ct.sendText('❌ 身份已过期,请重新发送账号和密码(空格隔开),例:`myname 123456`');
      await ct.cronStopPolling();
      return { error: 'invalid_token' };
    }
    if (e instanceof api.ApiError) {
      await ct.sendText(`❌ 操作失败:${e.message}`);
      return { error: e.message };
    }
    await ct.sendText(`❌ 操作异常:${e.message}`);
    return { error: e.message };
  }

  // 终态
  const isTerminal = (action === 'reject') || (step === 'review_2' && action === 'approve');
  // 换商品删旧映射，但不停轮询（服务端会异步推新 review_1）
  if (action === 'change_product') {
    ct.removeShortId(shortId);
    await ct.cronStartPolling();
  } else if (isTerminal) {
    ct.removeShortId(shortId);
    const m = ct.loadMap();
    const active = Object.values(m.cards || {}).filter(
      i => ['review_1', 'review_1_5', 'review_2'].includes(i.step)
    );
    if (!active.length) await ct.cronStopPolling();
  } else {
    await ct.cronStartPolling();
  }

  return { short_id: shortId, video_id: videoId, step, action, api_resp: resp, terminal: isTerminal };
}

// CLI 入口
// 用法: node handle-button.mjs "<clicked_label>" [<channel>]
if (process.argv[1] && process.argv[1].includes('handle-button.mjs')) {
  (async () => {
    const channelArg = process.argv[3] || '';
    const targetArg = process.argv[4] || '';
    if (channelArg) {
      ct.setRuntimeChannel(channelArg, targetArg || null);
    } else {
      const detected = await ct.detectChannelFromSessions();
      if (detected) ct.setRuntimeChannel(detected.channel, detected.target);
    }
    const r = await main(process.argv[2] || '');
    // 所有消息已通过 sendText/sendCard 发送，输出固定回复堵死 LLM
    console.log('OUTPUT_AS_REPLY:✅ 收到');
    process.exit(0);
  })().catch(e => {
    console.log('OUTPUT_AS_REPLY:⚠️ 执行异常，请稍后重试。');
    process.exit(1);
  });
}
