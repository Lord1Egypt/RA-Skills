#!/usr/bin/env node
/**
 * 微信公众号发布工具 - Node.js 版本
 * 完整方案：marked 转换 + 内联样式 + 微信 API
 *
 * 用法:
 *   node wx-publish.js draft <md-file> --title "标题" [--thumb <封面图>]
 *   node wx-publish.js publish <md-file> --title "标题" [--thumb <封面图>]
 *   node wx-publish.js drafts
 *   node wx-publish.js del <media_id>
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { marked } = require('marked');

// ── 配置 ─────────────────────────────────────────────────

function loadConfig() {
  return JSON.parse(fs.readFileSync(path.join(os.homedir(), '.config/wx-mp/config.json'), 'utf8'));
}
function loadTokenCache() {
  const p = path.join(os.homedir(), '.config/wx-mp/.token_cache.json');
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return {}; }
}
function saveTokenCache(data) {
  const dir = path.join(os.homedir(), '.config/wx-mp');
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, '.token_cache.json'), JSON.stringify(data, null, 2), 'utf8');
}

// ── HTTP ─────────────────────────────────────────────────

function httpReq(method, hostname, port, urlPath, bodyBuf, contentType) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname,
      port: port || 443,
      path: urlPath,
      method,
      headers: {},
    };
    if (bodyBuf) options.headers['Content-Length'] = bodyBuf.length;
    if (contentType) options.headers['Content-Type'] = contentType;

    const req = https.request(options, (res) => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        const raw = Buffer.concat(chunks);
        try {
          resolve(JSON.parse(raw.toString('utf8')));
        } catch {
          resolve(raw.toString('utf8'));
        }
      });
    });
    req.on('error', reject);
    req.setTimeout(20000, () => { req.destroy(); reject(new Error('请求超时')); });
    if (bodyBuf) req.write(bodyBuf);
    req.end();
  });
}

// ── Access Token ─────────────────────────────────────────

async function getToken() {
  const cache = loadTokenCache();
  const now = Date.now();
  if (cache.expires_at && cache.expires_at > now + 200000) return cache.access_token;
  const { appId, appSecret } = loadConfig();
  const body = await httpReq('GET', 'api.weixin.qq.com', 443,
    `/cgi-bin/token?grant_type=client_credential&appid=${appId}&secret=${appSecret}`);
  if (body.errcode) throw new Error(`[${body.errcode}] ${body.errmsg}`);
  const data = { access_token: body.access_token, expires_at: now + body.expires_in * 1000 };
  saveTokenCache(data);
  return body.access_token;
}

// ── API Call ─────────────────────────────────────────────

async function apiCall(apiPath, method = 'GET', body = null) {
  const token = await getToken();
  const sep = apiPath.includes('?') ? '&' : '?';
  const urlPath = `/cgi-bin${apiPath}${sep}access_token=${token}`;
  const bodyBuf = body ? Buffer.from(JSON.stringify(body), 'utf8') : null;
  const res = await httpReq(method, 'api.weixin.qq.com', 443, urlPath, bodyBuf, 'application/json');
  if (res && res.errcode && res.errcode !== 0) {
    const err = new Error(`[${res.errcode}] ${res.errmsg}`);
    err.errcode = res.errcode;
    throw err;
  }
  return res;
}

// ── Markdown → HTML 转换（微信友好） ───────────────────

// 配置 marked，输出简单的 HTML
marked.setOptions({
  breaks: false,   // 不要把换行转成 <br>
  gfm: true,
});

// 内联样式映射
const STYLES = {
  h1: 'font-size:24px;font-weight:bold;text-align:center;margin:30px 0 15px;color:#135ce0;',
  h2: 'font-size:22px;font-weight:bold;margin:25px 0 12px;padding-bottom:6px;border-bottom:2px solid #135ce0;color:#135ce0;',
  h3: 'font-size:18px;font-weight:bold;margin:20px 0 10px;color:#135ce0;',
  h4: 'font-size:16px;font-weight:bold;margin:15px 0 8px;color:#333;',
  p: 'margin:10px 0;line-height:1.8;font-size:15px;color:#333;',
  blockquote: 'margin:15px 0;padding:10px 15px;border-left:4px solid #135ce0;background:#f7f7f7;color:#666;font-size:14px;',
  code_inline: 'background:#f0f0f0;padding:2px 6px;border-radius:3px;font-size:13px;color:#c7254e;font-family:Menlo,Monaco,Consolas,monospace;',
  code_block: 'background:#2d2d2d;color:#ccc;padding:15px;border-radius:5px;font-size:13px;line-height:1.6;overflow-x:auto;font-family:Menlo,Monaco,Consolas,monospace;margin:15px 0;',
  table: 'border-collapse:collapse;width:100%;margin:15px 0;font-size:14px;',
  th: 'border:1px solid #ddd;padding:10px 12px;background:#f5f5f5;text-align:left;font-weight:bold;color:#333;',
  td: 'border:1px solid #ddd;padding:8px 12px;color:#333;',
  img: 'max-width:100%;height:auto;border-radius:4px;margin:10px 0;display:block;',
  a: 'color:#135ce0;text-decoration:none;',
  hr: 'border:none;border-top:1px solid #ddd;margin:20px 0;',
  ul: 'margin:10px 0;padding-left:25px;color:#333;font-size:15px;line-height:1.8;',
  ol: 'margin:10px 0;padding-left:25px;color:#333;font-size:15px;line-height:1.8;',
  li: 'margin:5px 0;line-height:1.8;',
};

function applyInlineStyles(html) {
  // h1-h4
  html = html.replace(/<h1([^>]*)>/g, `<h1 style="${STYLES.h1}"$1>`);
  html = html.replace(/<h2([^>]*)>/g, `<h2 style="${STYLES.h2}"$1>`);
  html = html.replace(/<h3([^>]*)>/g, `<h3 style="${STYLES.h3}"$1>`);
  html = html.replace(/<h4([^>]*)>/g, `<h4 style="${STYLES.h4}"$1>`);
  // p（不带 style 的）
  html = html.replace(/<p([^>]*)>/g, (m, attrs) => {
    if (attrs.includes('style=')) return m;
    return `<p style="${STYLES.p}"${attrs}>`;
  });
  // blockquote
  html = html.replace(/<blockquote([^>]*)>/g, `<blockquote style="${STYLES.blockquote}"$1>`);
  // code inline
  html = html.replace(/<code([^>]*)>/g, (m, attrs) => {
    if (attrs.includes('style=')) return m;
    return `<code style="${STYLES.code_inline}"$1>`;
  });
  // pre
  html = html.replace(/<pre([^>]*)>/g, (m, attrs) => {
    if (attrs.includes('style=')) return m;
    return `<pre style="${STYLES.code_block}"$1>`;
  });
  // img
  html = html.replace(/<img([^>]*)>/g, (m, attrs) => {
    if (attrs.includes('style=')) return m;
    return `<img style="${STYLES.img}"${attrs}>`;
  });
  // a
  html = html.replace(/<a([^>]*)>/g, (m, attrs) => {
    if (attrs.includes('style=')) return m;
    return `<a style="${STYLES.a}"$1>`;
  });
  // hr
  html = html.replace(/<hr\s*\/?>/g, `<hr style="${STYLES.hr}">`);
  // table
  html = html.replace(/<table>/g, `<table style="${STYLES.table}">`);
  html = html.replace(/<th>/g, `<th style="${STYLES.th}">`);
  html = html.replace(/<td>/g, `<td style="${STYLES.td}">`);
  // ul/ol
  html = html.replace(/<ul>/g, `<ul style="${STYLES.ul}">`);
  html = html.replace(/<ol>/g, `<ol style="${STYLES.ol}">`);
  html = html.replace(/<li>/g, `<li style="${STYLES.li}">`);
  return html;
}

function mdToHtml(md) {
  // marked 转换为 HTML
  let html = marked.parse(md);
  // 应用内联样式
  html = applyInlineStyles(html);
  return html;
}

// ── 上传封面图 ─────────────────────────────────────────

async function uploadThumb(filePath) {
  const token = await getToken();
  const boundary = '----NodeForm' + Math.random().toString(36).slice(2);
  const ext = path.extname(filePath).toLowerCase().slice(1);
  const mime = ext === 'jpg' ? 'image/jpeg' : `image/${ext}`;
  const fileBuf = fs.readFileSync(filePath);
  const filename = path.basename(filePath);
  const head = Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="media"; filename="${filename}"\r\nContent-Type: ${mime}\r\n\r\n`, 'utf8');
  const tail = Buffer.from(`\r\n--${boundary}--\r\n`, 'utf8');
  const bodyBuf = Buffer.concat([head, fileBuf, tail]);
  // 用永久素材接口，不要用临时素材接口（临时素材media_id在草稿中不兼容）
  const res = await httpReq('POST', 'api.weixin.qq.com', 443,
    `/cgi-bin/material/add_material?access_token=${token}&type=image`,
    bodyBuf, `multipart/form-data; boundary=${boundary}`);
  if (res.errcode) throw new Error(`[${res.errcode}] ${res.errmsg}`);
  return res.media_id;
}

// ── 创建草稿 ────────────────────────────────────────────

async function createDraft(articles) {
  return apiCall('/draft/add', 'POST', { articles });
}

// ── 发布 ────────────────────────────────────────────────

async function submitPublish(mediaId) {
  return apiCall('/freepublish/submit', 'POST', { media_id: mediaId });
}

// ── 轮询发布状态 ────────────────────────────────────────

async function pollPublish(publishId) {
  for (let i = 0; i < 10; i++) {
    await new Promise(r => setTimeout(r, 3000));
    const res = await apiCall('/freepublish/get', 'POST', { publish_id: publishId });
    const s = res.publish_status;
    if (s === '0') { console.log('✅ 发布成功!'); return; }
    if (s === '2') { console.log('❌ 发布被删除'); return; }
    if (s === '3') { console.log('❌ 发布失败:', res.fail_reason); return; }
    console.log(`⏳ 发布中... (${i+1}/10)`);
  }
  console.log('⏰ 等待超时，请在公众号后台查看发布状态');
}

// ── CLI ─────────────────────────────────────────────────

function getArg(flag) {
  const i = args.indexOf(flag);
  return i > -1 ? args[i + 1] : null;
}

const args = process.argv.slice(2);
const cmd = args[0];

async function main() {
  try {
    if (cmd === 'drafts') {
      const res = await apiCall('/draft/batchget', 'POST', { offset: 0, count: 20, no_content: 0 });
      const items = res.item || [];
      console.log(`📋 草稿列表 (共 ${items.length} 个)`);
      console.log('─'.repeat(60));
      if (!items.length) { console.log('暂无草稿'); return; }
      for (const item of items) {
        for (const art of (item.content?.news_item || [])) {
          const t = art.update_time ? new Date(art.update_time * 1000).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' }) : 'N/A';
          console.log(`  📄 ${art.title || '(无标题)'}`);
          console.log(`     media_id: ${item.media_id}`);
          console.log(`     更新时间: ${t}`);
          console.log();
        }
      }
    } else if (cmd === 'del') {
      const mediaId = args[1];
      if (!mediaId) { console.error('❌ 用法: node wx-publish.js del <media_id>'); process.exit(1); }
      await apiCall('/draft/delete', 'POST', { media_id: mediaId });
      console.log(`✅ 已删除: ${mediaId}`);
    } else if (cmd === 'draft' || cmd === 'publish') {
      const mdFile = args[1];
      const title = getArg('--title');
      const thumbFile = getArg('--thumb');
      if (!mdFile) { console.error('❌ 用法: node wx-publish.js draft <file.md> --title "标题" [--thumb <封面图>]'); process.exit(1); }

      // 读取并转换 MD
      let content = fs.readFileSync(mdFile, 'utf8');
      // 去除 YAML frontmatter
      content = content.replace(/^---\n[\s\S]*?\n---\n/, '');
      const contentHtml = mdToHtml(content);

      const cfg = loadConfig();
      let thumbMediaId = cfg.defaultThumbMediaId;
      if (thumbFile) {
        console.log(`🖼️  上传封面图: ${thumbFile}`);
        thumbMediaId = await uploadThumb(thumbFile);
        console.log(`   thumb_media_id: ${thumbMediaId}`);
      } else if (thumbMediaId) {
        console.log('🖼️  使用默认封面图');
      } else {
        console.error('❌ 未指定封面图（--thumb），且未配置 defaultThumbMediaId');
        process.exit(1);
      }

      const article = {
        title: title || '无标题',
        author: cfg.defaultAuthor || '',
        digest: '',
        content: contentHtml,
        thumb_media_id: thumbMediaId,
        need_open_comment: 1,
        only_fans_can_comment: 0,
      };

      console.log('📤 创建草稿...');
      const draftRes = await createDraft([article]);
      console.log(`✅ 草稿创建成功`);
      console.log(`   media_id: ${draftRes.media_id}`);
      console.log(`   标题: ${article.title}`);

      if (cmd === 'publish') {
        console.log('🚀 提交发布...');
        const pubRes = await submitPublish(draftRes.media_id);
        if (pubRes.errcode) throw new Error(`[${pubRes.errcode}] ${pubRes.errmsg}`);
        console.log(`✅ 已提交发布 publish_id=${pubRes.publish_id}`);
        await pollPublish(pubRes.publish_id);
      }
    } else {
      console.log('用法:');
      console.log('  node wx-publish.js draft <md-file> --title "标题" [--thumb <封面图>]');
      console.log('  node wx-publish.js publish <md-file> --title "标题" [--thumb <封面图>]');
      console.log('  node wx-publish.js drafts');
      console.log('  node wx-publish.js del <media_id>');
    }
  } catch (e) {
    console.error('❌ 错误:', e.message);
    if (e.errcode) console.error('   errcode:', e.errcode);
    process.exit(1);
  }
}

main();
