/**
 * 发 review_1（一审）卡片。
 *
 * 输入 data 字段（来自 events.data）:
 *   video_id, video_url, author, view_count, score, summary,
 *   product_name, product_url, product_image_url
 */
import * as ct from './card-tools.mjs';

function fmtViews(n) {
  if (n == null) return '?';
  const num = Number(n);
  if (isNaN(num)) return String(n);
  if (num >= 1_000_000) return `${(num / 1_000_000).toFixed(1)}M`;
  if (num >= 1_000) return `${(num / 1_000).toFixed(1)}K`;
  return String(num);
}

export async function send(data) {
  const videoId = data.video_id;
  const shortId = ct.reserveShortId(videoId, 'review_1');

  const text =
    `🛒 **视频审核 #${shortId}**\n` +
    `📹 原视频:${data.video_url || ''}\n` +
    `👤 作者:${data.author || ''}\n` +
    `📊 播放 ${fmtViews(data.view_count)} | ` +
    `🤖 AI评分:${data.score ?? '?'}/100\n\n` +
    `📝 ${data.summary || ''}\n\n` +
    `🛒 **推荐商品:** ${data.product_name || ''}\n` +
    `🔗 ${data.product_url || ''}`;

  const productImage = data.product_image_url;
  if (!productImage) throw new Error('缺少 product_image_url');
  const media = ct.mediaUrl(productImage);

  const buttonRows = [
    [
      { label: `⏭️ 换视频 #${shortId}`, style: 'primary' },
      { label: `🔄 换商品 #${shortId}`, style: 'primary' },
    ],
    [
      { label: `✅ 做分镜 #${shortId}`, style: 'success' },
      { label: `⏭️ 换一个 #${shortId}`, style: 'secondary' },
    ],
  ];

  const msgId = await ct.sendCardRows(text, media, buttonRows, '产品图');
  ct.updateMapMessageId(shortId, msgId);
  return { short_id: shortId, messageId: msgId };
}

// CLI 入口
if (process.argv[1] && process.argv[1].includes('send-review-1.mjs')) {
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
