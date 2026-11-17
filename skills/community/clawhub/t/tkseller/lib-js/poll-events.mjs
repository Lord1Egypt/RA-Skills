/**
 * 轮询事件处理。被 poll-loop.mjs 每 N 秒调用一次。
 *
 * 逻辑:
 *   1. 检查 poll_state.active: 不活跃 → 直接退出
 *   2. 调 events_pending() 拉所有未消费事件
 *   3. 对每个事件: 已 processed → 直接 ack；否则按 event_type 分发
 *   4. 检查终态事件 → 停轮询
 *   5. 输出 JSON 摘要
 */
import { readFileSync, writeFileSync, existsSync, unlinkSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import * as api from './api.mjs';
import * as ct from './card-tools.mjs';
import { send as sendReview1 } from './send-review-1.mjs';
import { send as sendReview15 } from './send-review-1-5.mjs';
import { send as sendReview2 } from './send-review-2.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PERSONA_LOCK_PATH = join(dirname(__dirname), 'data', 'persona_pending.json');

function _clearPersonaPending() {
  try { if (existsSync(PERSONA_LOCK_PATH)) unlinkSync(PERSONA_LOCK_PATH); } catch { /* */ }
}

function stopPolling(reason = '') {
  try { ct.cronStopPolling(); } catch { /* */ }
  return reason;
}

// ========== 事件处理 ==========
async function handleEvent(event) {
  const eventId = event.id;
  const eventType = event.event_type;
  const videoId = event.video_id;
  let data = event.data || {};
  if (typeof data === 'string') {
    try { data = JSON.parse(data); } catch { /* */ }
  }
  if (videoId != null && !data.video_id) data.video_id = videoId;

  try {
    if (eventType === 'review_1') return await sendReview1(data);
    if (eventType === 'review_1_5') return await sendReview15(data);
    if (eventType === 'review_2') return await sendReview2(data);

    // 数字人生成完成
    if (eventType === 'persona_created') {
      _clearPersonaPending();
      const payload = event.payload || data;
      const name = payload.name || '数字人';
      const description = payload.description || '';
      const imageUrl = payload.frontal_image || '';
      const personaId = payload.persona_id || null;

      const text =
        `✅ **数字人生成完成！**\n\n` +
        `**名称：** ${name}\n` +
        `**描述：** ${description}`;

      let confirmLabel = '✅ 确认使用';
      if (personaId) confirmLabel = `✅ 确认使用 #${personaId}`;

      const buttons = [
        { label: confirmLabel, style: 'success' },
        { label: '🔄 重新生成', style: 'primary' },
      ];

      await ct.sendCard(text, imageUrl, buttons, '数字人正面照');
      return { terminal: true };
    }

    // 数字人生成失败
    if (eventType === 'persona_failed') {
      _clearPersonaPending();
      const payload = event.payload || data;
      const error = payload.error || '未知错误';
      await ct.sendText(`❌ 数字人生成失败：${error}\n请重新选择或自定义。`);
      // 重新发数字人选择卡片
      const { send: sendPersonaCard } = await import('./send-persona-card.mjs');
      await sendPersonaCard();
      return { terminal: true };
    }

    if (eventType === 'published') {
      const short = ct.findShortIdByVideo(videoId) || '?';
      const platform = data.platform || '?';
      const status = data.status || 'success';
      if (status === 'success') {
        await ct.sendText(`✅ 视频 #${short} 已成功发布到 ${platform}!`);
      } else {
        await ct.sendText(`⚠️ 视频 #${short} 发布到 ${platform} 失败：${status}`);
      }
      if (short && short !== '?') ct.removeShortId(short);
      return { terminal: true };
    }

    if (eventType === 'publish_failed') {
      const short = ct.findShortIdByVideo(videoId) || '?';
      const error = data.error || '未知错误';
      await ct.sendText(`❌ 视频 #${short} 发布失败：${error}\n可以重新点"✅ 通过"重试发布。`);
      return { terminal: true };
    }

    if (eventType === 'no_match') {
      await ct.sendText('😅 这轮没找到合适的视频，稍后再试或换个 URL。');
      return { terminal: true };
    }

    if (eventType === 'error') {
      // 后端可能用 error_type/message（旧字段）或 step/error（flowdroid_error 实际发的字段）
      const etype = (data.error_type || data.step || '').trim();
      const rawMsg = (data.message || data.error || '').trim();
      // 后端推了一个空的 error 事件（无 type 无 message）→ 不干扰老板，静默跳过
      if (!etype && !rawMsg) {
        return { skipped_empty_error: true };
      }
      const msg = rawMsg || '未知错误';
      const short = ct.findShortIdByVideo(videoId) || '?';
      // 按环节给用户可操作的提示（而不是干巴巴的技术错误）
      const STEP_HINT = {
        generate_storyboard: `❌ 视频 #${short} 分镜生成失败了，请重新点「✅ 做分镜 #${short}」重试。`,
        generate_video: `❌ 视频 #${short} 视频生成失败了，请重新点「✅ 分镜通过 #${short}」重试。`,
        change_product: `❌ 视频 #${short} 换商品失败了，请重试。`,
        change_video: `❌ 视频 #${short} 换视频失败了，请重试。`,
      };
      if (etype === 'quota_exhausted') {
        await ct.sendText(`⚠️ API 余额不足，无法继续生成。请充值后重试。\n\n错误详情：${msg}`);
      } else if (STEP_HINT[etype]) {
        await ct.sendText(`${STEP_HINT[etype]}\n\n（原因：${msg}）`);
      } else if (etype) {
        await ct.sendText(`⚠️ 流程异常（${etype}）：${msg}`);
      } else {
        await ct.sendText(`⚠️ 流程异常：${msg}`);
      }
      return { terminal: true };
    }

    return { unknown_event_type: eventType };
  } catch (e) {
    await ct.sendText(`⚠️ 处理事件 #${eventId} (${eventType}) 失败：${e.message}\n下轮会重试。`);
    throw e;
  }
}

// ========== 主循环（单次扫描） ==========
export async function main() {
  const state = ct.pollStateLoad();
  if (!state.active) return { skip: true, reason: 'inactive' };

  // 拉事件
  let resp;
  try {
    resp = await api.eventsPending();
  } catch (e) {
    if (e instanceof api.InvalidToken) {
      stopPolling('invalid_token');
      await ct.sendText('❌ 身份已过期，轮询已停止。请重新发送账号和密码（空格隔开），例：`myname 123456`');
      return { stopped: true, reason: 'invalid_token' };
    }
    if (e instanceof api.ApiError) return { transient_error: e.message };
    return { exception: e.message };
  }

  const events = resp.events || [];
  let processed = 0;
  let duped = 0;
  let terminal = false;

  // 只处理本次轮询启动之后产生的事件，旧事件直接 ack 跳过
  const startedAt = state.started_at || 0;

  for (const ev of events) {
    const eid = ev.id;
    if (eid == null) continue;

    if (ct.isEventProcessed(eid)) {
      duped++;
      try { await api.eventAck(eid); } catch { /* */ }
      continue;
    }

    // 注意：不再按 started_at 时间过滤，只靠 processed_events.json 去重
    // 后端 created_at 时区不确定，时间比较容易误杀新事件

    try {
      const result = await handleEvent(ev);
      ct.markEventProcessed(eid);
      try { await api.eventAck(eid); } catch { /* */ }
      processed++;
      if (result && result.terminal) terminal = true;
    } catch {
      continue;
    }
  }

  // 检查活跃卡片
  const m = ct.loadMap();
  const activeCards = Object.entries(m.cards || {}).filter(
    ([, info]) => ['review_1', 'review_1_5', 'review_2'].includes(info.step)
  );

  const out = { processed, duped, active_cards: activeCards.length };

  if (terminal && !activeCards.length) {
    stopPolling('terminal');
    out.stopped = true;
  }
  return out;
}

// CLI 入口
// 被 exec 跑一轮时：只输出本轮处理攒在 buffer 的内容。
// 不读 pending 文件——积压内容由 poll-loop 自己重试 sessions_send 推送，
// 若这里也倒 pending 会把历史积压混进本次操作结果（用户困惑）。
if (process.argv[1] && process.argv[1].includes('poll-events.mjs')) {
  const _collectOutput = () => {
    try { return (ct.webchatFlush() || '').trim(); } catch { return ''; }
  };
  main().then(() => {
    const out = _collectOutput();
    console.log(out ? 'OUTPUT_AS_REPLY:' + out : 'NO_REPLY');
    process.exit(0);
  }).catch(() => {
    const out = _collectOutput();
    console.log(out ? 'OUTPUT_AS_REPLY:' + out : 'NO_REPLY');
    process.exit(1);
  });
}
