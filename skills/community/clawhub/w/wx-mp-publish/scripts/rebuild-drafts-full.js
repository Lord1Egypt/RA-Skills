#!/usr/bin/env node
/**
 * 用完整内容重建公众号草稿
 */
const fs = require('fs');
const path = require('path');
const https = require('https');
const os = require('os');
const { marked } = require('marked');

// 草稿映射：标题 -> { file: Hugo文章路径, thumbMediaId: 新封面media_id }
const DRAFTS = [
  {
    title: '为什么越忙越不想动？聊聊决策疲劳这件事',
    file: '/root/hugo-site/content/posts/life-006.md',
    thumbMediaId: 'A83aYO34D2tkzY601CqYdzqPsuWqpqlrGHaNEw8sQ-9NTNVHBDSLg4sqRdaI1Ep1',
    oldMediaId: 'A83aYO34D2tkzY601CqYd9UqwCQQwNj8g0RZWUhNPlfSEc9XtTfq5idPP6t3xIHZ',
  },
  {
    title: 'AI写文章、AI画画、AI做视频——内容创作者该焦虑吗？',
    file: '/root/hugo-site/content/posts/life-005.md',
    thumbMediaId: 'A83aYO34D2tkzY601CqYd-O1Mp9vLYMuKXmch4xTlfTflK4BScPHqpMt2n1EG6Sx',
    oldMediaId: 'A83aYO34D2tkzY601CqYdwMr518kQ8yiDhFoFmb7WGC5sxSSm6RefnO9JhUQTCDH',
  },
  {
    title: 'AI能帮你做什么？这10个场景比你想的更实用',
    file: '/root/hugo-site/content/posts/life-004.md',
    thumbMediaId: 'A83aYO34D2tkzY601CqYdyA099OamY4MytSw4OUBjyfaeY3ks-69b6Dto4mMo47T',
    oldMediaId: 'A83aYO34D2tkzY601CqYd83h7NfoU7gQXVchTJL5Zh_xwXsHPLyxU2Qp8rfk3bze',
  },
  {
    title: '30岁以后我才明白的5件事',
    file: '/root/hugo-site/content/posts/life-003.md',
    thumbMediaId: 'A83aYO34D2tkzY601CqYdzBcLfNEZoVeKPR4fFZCSYCOArOjXov_BkSSDJDmad-z',
    oldMediaId: 'A83aYO34D2tkzY601CqYd_tUmraty2UqHV4VEl04dA3LQVAXwwJvCM80Ss6ODs4P',
  },
  {
    title: '和AI聊天一年后，我的三个变化',
    file: '/root/hugo-site/content/posts/life-life-010.md',
    thumbMediaId: 'A83aYO34D2tkzY601CqYd1IAFuLlmU1scIYM-wSLkWmVJwbzBqRdzWoWZFtk2O0A',
    oldMediaId: 'A83aYO34D2tkzY601CqYd6LMnq5L5KhWbl2_eLfzj_ccmYHdtHw8ESfm5TbkU2ZO',
  },
  {
    title: '搬到通勤路上之后，我的生活发生了什么变化',
    file: '/root/hugo-site/content/posts/life-009.md',
    thumbMediaId: 'A83aYO34D2tkzY601CqYdxqFlSXcoV1rjGJNwzs-Wj9wYvkcnbjeTvkdEYqWOVpM',
    oldMediaId: 'A83aYO34D2tkzY601CqYdxZyyTJW2kkpTSMyr42UXJ-1yGQyPCFymRF-7hFzDADo',
  },
];

marked.setOptions({ breaks: false, gfm: true });

function loadConfig() {
  return JSON.parse(fs.readFileSync(path.join(os.homedir(), '.config/wx-mp/config.json'), 'utf8'));
}
function loadTokenCache() {
  const p = path.join(os.homedir(), '.config/wx-mp/.token_cache.json');
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return {}; }
}
function httpReq(method, hostname, port, urlPath, bodyBuf, contentType) {
  return new Promise((resolve, reject) => {
    const options = { hostname, port: port || 443, path: urlPath, method, headers: {} };
    if (bodyBuf) options.headers['Content-Length'] = bodyBuf.length;
    if (contentType) options.headers['Content-Type'] = contentType;
    const req = https.request(options, (res) => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        const raw = Buffer.concat(chunks);
        try { resolve(JSON.parse(raw.toString('utf8'))); } catch { resolve(raw.toString('utf8')); }
      });
    });
    req.on('error', reject);
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('请求超时')); });
    if (bodyBuf) req.write(bodyBuf);
    req.end();
  });
}
async function getToken() {
  const cache = loadTokenCache();
  const now = Date.now();
  if (cache.expires_at && cache.expires_at > now + 200000) return cache.access_token;
  const { appId, appSecret } = loadConfig();
  const body = await httpReq('GET', 'api.weixin.qq.com', 443,
    '/cgi-bin/token?grant_type=client_credential&appid=' + appId + '&secret=' + appSecret);
  if (body.errcode) throw new Error(body.errmsg);
  return body.access_token;
}
async function apiCall(apiPath, method, body) {
  const token = await getToken();
  const sep = apiPath.includes('?') ? '&' : '?';
  const urlPath = '/cgi-bin' + apiPath + sep + 'access_token=' + token;
  const bodyBuf = body ? Buffer.from(JSON.stringify(body), 'utf8') : null;
  const res = await httpReq(method, 'api.weixin.qq.com', 443, urlPath, bodyBuf, 'application/json');
  if (res && res.errcode && res.errcode !== 0) throw new Error('[' + res.errcode + '] ' + res.errmsg);
  return res;
}
async function deleteDraft(mediaId) {
  return apiCall('/draft/delete', 'POST', { media_id: mediaId });
}
async function createDraft(article) {
  return apiCall('/draft/add', 'POST', { articles: [article] });
}

const STYLES = {
  p: 'margin:10px 0;line-height:1.8;font-size:15px;color:#333;',
  h2: 'font-size:22px;font-weight:bold;margin:25px 0 12px;padding-bottom:6px;border-bottom:2px solid #135ce0;color:#135ce0;',
  h3: 'font-size:18px;font-weight:bold;margin:20px 0 10px;color:#135ce0;',
  blockquote: 'margin:15px 0;padding:10px 15px;border-left:4px solid #135ce0;background:#f7f7f7;color:#666;font-size:14px;',
  img: 'max-width:100%;height:auto;border-radius:4px;margin:10px 0;display:block;',
  hr: 'border:none;border-top:1px solid #ddd;margin:20px 0;',
};

function applyInlineStyles(html) {
  html = html.replace(/<h2([^>]*)>/g, `<h2 style="${STYLES.h2}"$1>`);
  html = html.replace(/<h3([^>]*)>/g, `<h3 style="${STYLES.h3}"$1>`);
  html = html.replace(/<p([^>]*)>/g, (m, attrs) => {
    if (attrs.includes('style=')) return m;
    return `<p style="${STYLES.p}"${attrs}>`;
  });
  html = html.replace(/<blockquote([^>]*)>/g, `<blockquote style="${STYLES.blockquote}"$1>`);
  html = html.replace(/<img([^>]*)>/g, `<img style="${STYLES.img}"$1>`);
  html = html.replace(/<hr\s*\/?>/g, `<hr style="${STYLES.hr}">`);
  return html;
}

function mdToHtml(md) {
  let html = marked.parse(md);
  html = applyInlineStyles(html);
  return html;
}

async function main() {
  for (const draft of DRAFTS) {
    if (!draft.file) {
      console.log('⚠️  跳过(未找到文件):', draft.title);
      continue;
    }
    console.log('📄 处理:', draft.title);

    // 读取并转换内容
    let content = fs.readFileSync(draft.file, 'utf8');
    content = content.replace(/^---\n[\s\S]*?\n---\n/, ''); // 去除 frontmatter
    const contentHtml = mdToHtml(content);

    // 删除旧草稿
    try {
      await deleteDraft(draft.oldMediaId);
      console.log('  🗑️ 已删除旧草稿');
    } catch (e) {
      console.log('  ⚠️ 删除失败:', e.message);
    }

    // 创建新草稿
    const article = {
      title: draft.title,
      author: '你的名字',
      digest: draft.title.substring(0, 54),
      content: contentHtml,
      thumb_media_id: draft.thumbMediaId,
      need_open_comment: 1,
      only_fans_can_comment: 0,
    };
    const res = await createDraft(article);
    console.log('  ✅ 新草稿创建成功:', res.media_id);
  }
  console.log('\n🎉 全部完成!');
}
main().catch(e => console.error('❌:', e.message));