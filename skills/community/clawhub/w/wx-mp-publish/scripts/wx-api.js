#!/usr/bin/env node
/**
 * 微信公众号 API 调用 - Node.js 版本
 * 解决 Python 版 JSON parsing 编码问题
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ── 配置 ─────────────────────────────────────────────────

function loadConfig() {
  const configPath = path.join(process.env.HOME || '/root', '.config/wx-mp/config.json');
  try {
    return JSON.parse(fs.readFileSync(configPath, 'utf8'));
  } catch (e) {
    console.error('❌ 配置文件不存在或格式错误:', configPath);
    console.error('   请创建:', configPath);
    process.exit(1);
  }
}

const config = loadConfig();
const APPID = config.appId;
const APPSECRET = config.appSecret;

// ── HTTP 请求 ────────────────────────────────────────────

function apiRequest(method, host, path, body = null, contentType = 'application/json') {
  return new Promise((resolve, reject) => {
    const isHttps = host.startsWith('https') || host.includes('weixin') || host.includes('qq.com');
    const h = isHttps ? https : http;

    const hostname = host.replace('https://', '').replace('http://', '').split(':')[0];
    const port = isHttps ? 443 : 80;

    const options = {
      hostname,
      port,
      path,
      method,
      headers: {
        'Content-Type': contentType,
      },
    };

    // 微信 API 必须用 UTF-8 编码
    let bodyStr = '';
    if (body) {
      bodyStr = typeof body === 'string' ? body : JSON.stringify(body);
      options.headers['Content-Length'] = Buffer.byteLength(bodyStr, 'utf8');
    }

    const req = h.request(options, (res) => {
      // 微信 API 返回 GBK 或 UTF-8，先收集原始 buffer
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        const rawBuffer = Buffer.concat(chunks);
        // 尝试解析为 JSON（API 通常返回 UTF-8）
        let text;
        try {
          text = JSON.parse(rawBuffer.toString('utf8'));
        } catch (e) {
          // 解析失败则输出原始内容以便调试
          text = rawBuffer.toString('utf8');
        }
        resolve(text);
      });
    });

    req.on('error', reject);
    req.setTimeout(30000, () => {
      req.destroy();
      reject(new Error('请求超时'));
    });

    if (bodyStr) req.write(bodyStr, 'utf8');
    req.end();
  });
}

// ── Access Token ─────────────────────────────────────────

function loadTokenCache() {
  const cachePath = path.join(process.env.HOME || '/root', '.config/wx-mp/.token_cache.json');
  try {
    return JSON.parse(fs.readFileSync(cachePath, 'utf8'));
  } catch {
    return {};
  }
}

function saveTokenCache(data) {
  const cacheDir = path.join(process.env.HOME || '/root', '.config/wx-mp');
  if (!fs.existsSync(cacheDir)) fs.mkdirSync(cacheDir, { recursive: true });
  const cachePath = path.join(cacheDir, '.token_cache.json');
  fs.writeFileSync(cachePath, JSON.stringify(data, null, 2), 'utf8');
}

async function getAccessToken() {
  const cache = loadTokenCache();
  const now = Date.now();

  // 缓存有效期 7000 秒（官方 7200 秒，提前 200 秒过期）
  if (cache.expires_at && cache.expires_at > now + 200000) {
    return cache.access_token;
  }

  console.log('   获取新的 access_token...');
  const res = await apiRequest(
    'GET',
    'api.weixin.qq.com',
    `/cgi-bin/token?grant_type=client_credential&appid=${APPID}&secret=${APPSECRET}`
  );

  if (res.errcode && res.errcode !== 0) {
    throw new Error(`[${res.errcode}] ${res.errmsg}`);
  }

  const tokenData = {
    access_token: res.access_token,
    expires_at: now + res.expires_in * 1000,
  };
  saveTokenCache(tokenData);
  return res.access_token;
}

// ── API 调用 ────────────────────────────────────────────

async function apiCall(accessToken, path, method = 'GET', body = null) {
  const res = await apiRequest(
    method,
    'api.weixin.qq.com',
    `/cgi-bin${path}${path.includes('?') ? '&' : '?'}access_token=${accessToken}`,
    body
  );

  if (res.errcode && res.errcode !== 0) {
    const err = new Error(`[${res.errcode}] ${res.errmsg}`);
    err.errcode = res.errcode;
    throw err;
  }
  return res;
}

// ── 上传封面图 ─────────────────────────────────────────

async function uploadThumb(filePath) {
  const token = await getAccessToken();
  const formData = createFormData({
    media: {
      value: fs.createReadStream(filePath),
      options: {
        filename: path.basename(filePath),
        contentType: 'image/' + (path.extname(filePath).slice(1) === 'jpg' ? 'jpeg' : 'png'),
      },
    },
  });

  const [host, pathname] = ['api.weixin.qq.com', `/cgi-bin/media/upload?access_token=${token}&type=thumb`];
  const res = await httpRequest('POST', host, pathname, formData, formData.getContentType());
  if (res.errcode) throw new Error(`[${res.errcode}] ${res.errmsg}`);
  return res.thumb_media_id;
}

// 简化版 form-data（不用第三方库）
function createFormData(parts) {
  const boundary = '----FormBoundary' + Math.random().toString(36).slice(2);
  const CRLF = '\r\n';
  let body = '';

  for (const [name, field] of Object.entries(parts)) {
    if (field.options) {
      // file field
      const filename = field.options.filename;
      const contentType = field.options.contentType;
      body += `--${boundary}${CRLF}` +
        `Content-Disposition: form-data; name="${name}"; filename="${filename}"${CRLF}` +
        `Content-Type: ${contentType}${CRLF}${CRLF}`;
      // 注意：这里需要同步读取文件内容
      const fileContent = fs.readFileSync(field.value, field.options.contentType ? 'binary' : 'utf8');
      body += fileContent + CRLF;
    } else {
      body += `--${boundary}${CRLF}` +
        `Content-Disposition: form-data; name="${name}"${CRLF}${CRLF}` +
        field.value + CRLF;
    }
  }
  body += `--${boundary}--${CRLF}`;

  const buf = Buffer.from(body, 'binary' || 'utf8');
  return {
    getContentType: () => `multipart/form-data; boundary=${boundary}`,
    getBuffer: () => buf,
  };
}

function httpRequest(method, host, pathname, postData, contentType) {
  return new Promise((resolve, reject) => {
    const isHttps = host.startsWith('https') || host.includes('weixin') || host.includes('qq.com');
    const h = isHttps ? https : http;
    const hostname = host.replace('https://', '').replace('http://', '').split(':')[0];
    const options = {
      hostname,
      port: isHttps ? 443 : 80,
      path: pathname,
      method,
      headers: { 'Content-Type': contentType },
    };

    const bodyBuf = typeof postData === 'object' && postData.getBuffer ? postData.getBuffer() : postData;
    if (bodyBuf) options.headers['Content-Length'] = bodyBuf.length;

    const req = h.request(options, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        const buf = Buffer.concat(chunks);
        try {
          resolve(JSON.parse(buf.toString('utf8')));
        } catch {
          resolve(buf.toString('utf8'));
        }
      });
    });
    req.on('error', reject);
    if (bodyBuf) req.write(bodyBuf);
    req.end();
  });
}

// ── 上传图片素材（文章内图片） ──────────────────────────

async function uploadImage(filePath) {
  const token = await getAccessToken();
  const formData = createFormData({
    media: {
      value: fs.createReadStream(filePath),
      options: {
        filename: path.basename(filePath),
        contentType: 'image/' + (path.extname(filePath).slice(1) === 'jpg' ? 'jpeg' : 'png'),
      },
    },
  });

  const [host, pathname] = ['api.weixin.qq.com', `/cgi-bin/media/upload?access_token=${token}&type=image`];
  const res = await httpRequest('POST', host, pathname, formData, formData.getContentType());
  if (res.errcode) throw new Error(`[${res.errcode}] ${res.errmsg}`);
  return res.url;
}

// ── 创建草稿 ────────────────────────────────────────────

async function addDraft(articles) {
  const token = await getAccessToken();
  return apiCall(token, '/draft/add', 'POST', {
    articles,
  });
}

// ── 发布草稿 ────────────────────────────────────────────

async function submit(mediaId) {
  const token = await getAccessToken();
  return apiCall(token, '/freepublish/submit', 'POST', {
    media_id: mediaId,
  });
}

// ── 查询发布状态 ────────────────────────────────────────

async function getPublishStatus(publishId) {
  const token = await getAccessToken();
  return apiCall(token, '/freepublish/get', 'POST', {
    publish_id: publishId,
  });
}

// ── 发布配额 ────────────────────────────────────────────

async function checkDailyPublish() {
  const token = await getAccessToken();
  return apiCall(token, '/freepublish/get_count', 'GET');
}

// ── 草稿列表 ───────────────────────────────────────────

async function listDrafts(offset = 0, count = 20) {
  const token = await getAccessToken();
  return apiCall(token, '/draft/count', 'GET').then(async (countRes) => {
    const drafts = await apiCall(token, '/draft/batchget', 'POST', { offset, count, no_content: 0 });
    return drafts;
  });
}

// ── 删除草稿（通过 media_id） ───────────────────────────

async function delDraft(mediaId) {
  const token = await getAccessToken();
  return apiCall(token, '/draft/delete', 'POST', { media_id: mediaId });
}

// ── 主命令 ──────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  try {
    if (cmd === 'drafts') {
      console.log('📋 草稿列表');
      console.log('─'.repeat(60));
      const res = await listDrafts();
      const items = res.item || [];
      if (!items.length) {
        console.log('暂无草稿');
        return;
      }
      for (const item of items) {
        const news = item.content?.news_item || [];
        for (const article of news) {
          const t = new Date(article.update_time * 1000).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
          console.log(`  📄 ${article.title}`);
          console.log(`     media_id: ${item.media_id}`);
          console.log(`     更新时间: ${t}`);
          console.log();
        }
      }
    } else if (cmd === 'status') {
      const quota = await checkDailyPublish();
      console.log('📊 公众号状态');
      console.log('─'.repeat(40));
      console.log(`今日已发布: ${quota.count} 篇`);
      console.log(`剩余可发布: ${quota.remaining} 篇`);
    } else if (cmd === 'del-draft') {
      const mediaId = args[1];
      if (!mediaId) { console.error('❌ 需要指定 media_id'); process.exit(1); }
      await delDraft(mediaId);
      console.log(`✅ 已删除草稿: ${mediaId}`);
    } else {
      console.log('用法:');
      console.log('  node wx-api.js drafts          # 列出草稿');
      console.log('  node wx-api.js status          # 查看配额');
      console.log('  node wx-api.js del-draft <id>  # 删除草稿');
    }
  } catch (e) {
    console.error('❌ 错误:', e.message);
    process.exit(1);
  }
}

main();
