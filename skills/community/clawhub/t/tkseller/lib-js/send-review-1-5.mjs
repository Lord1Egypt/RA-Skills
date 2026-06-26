/**
 * 发 review_1_5（分镜审核）卡片。
 *
 * 输入 data 字段:
 *   video_id, storyboard_url  （HTTP(S) URL，由 data-service 提供）
 *   - 若 data 含 error 字段则发错误提示文字，不发卡片
 */
import * as ct from './card-tools.mjs';

export async function send(data) {
  const videoId = data.video_id;

  // 错误兜底
  const err = data.error;
  if (err) {
    const short = ct.findShortIdByVideo(videoId) || '?';
    let msg = `⚠️ 视频 #${short} 分镜生成失败：${err}`;
    if (data.error_type) msg += `\n类型：${data.error_type}`;
    await ct.sendText(msg);
    return { short_id: short, error: err };
  }

  const storyboardUrl = data.storyboard_url;
  if (!storyboardUrl) return { skip: true, reason: 'no_storyboard_url' };

  const shortId = ct.reserveShortId(videoId, 'review_1_5');
  const media = ct.mediaUrl(storyboardUrl);

  const text = `🛒 **分镜审核 #${shortId}**\n请审核分镜图是否符合预期。`;

  const buttons = [
    { label: `✅ 分镜通过 #${shortId}`, style: 'success' },
    { label: `🔄 重新生成 #${shortId}`, style: 'primary' },
    { label: `❌ 放弃 #${shortId}`, style: 'danger' },
  ];

  const msgId = await ct.sendCard(text, media, buttons, '分镜图');
  ct.updateMapMessageId(shortId, msgId);
  return { short_id: shortId, messageId: msgId };
}

// CLI 入口
if (process.argv[1] && process.argv[1].includes('send-review-1-5.mjs')) {
  let data;
  if (process.argv[2] && process.argv[2] !== '-' && process.argv[2] !== '--stdin') {
    data = JSON.parse(process.argv[2]);
  } else {
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    const raw = Buffer.concat(chunks).toString('utf-8').replace(/^\ufeff/, '');
    data = JSON.parse(raw);
  }
  send(data).then(r => console.log(JSON.stringify(r))).catch(e => { console.error(e); process.exit(1); });
}
