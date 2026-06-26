/**
 * 发 review_2（成品视频审核）卡片。
 *
 * 输入 data 字段:
 *   video_id, video_url  （HTTP(S) URL）
 *   - 若 data 含 error 字段则发错误提示文字，不发卡片
 */
import * as ct from './card-tools.mjs';

export async function send(data) {
  const videoId = data.video_id;

  const err = data.error;
  if (err) {
    const short = ct.findShortIdByVideo(videoId) || '?';
    let msg = `⚠️ 视频 #${short} 生成失败：${err}`;
    if (data.error_type) msg += `\n类型：${data.error_type}`;
    await ct.sendText(msg);
    return { short_id: short, error: err };
  }

  const videoUrl = data.video_url;
  if (!videoUrl) return { skip: true, reason: 'no_video_url' };

  const shortId = ct.reserveShortId(videoId, 'review_2');
  const media = ct.mediaUrl(videoUrl);

  const text = `🛒 **成品审核 #${shortId}**\n请审核视频是否可以发布。`;

  const buttons = [
    { label: `✅ 通过 #${shortId}`, style: 'success' },
    { label: `🔄 重做 #${shortId}`, style: 'primary' },
    { label: `❌ 放弃 #${shortId}`, style: 'danger' },
  ];

  const msgId = await ct.sendCard(text, media, buttons, '成品视频');
  ct.updateMapMessageId(shortId, msgId);
  return { short_id: shortId, messageId: msgId };
}

// CLI 入口
if (process.argv[1] && process.argv[1].includes('send-review-2.mjs')) {
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
