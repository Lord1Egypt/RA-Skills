#!/usr/bin/env node
// -*- coding: utf-8 -*-
/**
 * 微信公众平台文章发布工具
 *
 * 跨平台 Node.js 脚本，封装微信公众平台 API 的核心发布流程。
 * 仅依赖 Node.js 内置模块，无需 npm install。
 *
 * 用法：
 *   node wechat_publish.cjs <command> [args]
 *
 * 命令：
 *   token                    获取/刷新 access_token
 *   upload-thumb <图片路径>   上传封面图 → media_id
 *   upload-image <图片路径>   上传正文图片 → url
 *   create-draft <JSON路径>  创建草稿 → media_id
 *   publish <media_id>       发布草稿
 *   get-status <publish_id>  查询发布状态
 *   get-stats <开始> <结束>   获取图文数据统计
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const os = require('os');
const crypto = require('crypto');

// ============================================================
// 配置
// ============================================================

const API_BASE = 'https://api.weixin.qq.com';

function defaultEnvPath() {
  return path.join(os.homedir(), '.openclaw', 'workspace-content-team', '.env');
}

function defaultTokenCachePath() {
  return path.join(os.homedir(), '.openclaw', 'workspace-content-team', '.access_token');
}

const ENV_FILE = process.env.WECHAT_ENV_FILE || defaultEnvPath();
const TOKEN_CACHE = defaultTokenCachePath();

// ============================================================
// 工具函数
// ============================================================

const MIME_MAP = {
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.gif': 'image/gif',
  '.bmp': 'image/bmp',
  '.webp': 'image/webp',
};

function guessMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return MIME_MAP[ext] || 'application/octet-stream';
}

function loadEnv() {
  if (!fs.existsSync(ENV_FILE)) {
    console.error(`❌ 未找到 API 配置文件：${ENV_FILE}`);
    console.error('   请先运行 /wechat-content-team 配置微信 API 凭证');
    process.exit(1);
  }

  const config = {};
  const content = fs.readFileSync(ENV_FILE, 'utf-8');
  for (const rawLine of content.split('\n')) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;
    const idx = line.indexOf('=');
    if (idx > 0) {
      config[line.slice(0, idx).trim()] = line.slice(idx + 1).trim();
    }
  }

  if (!config.WECHAT_APP_ID || !config.WECHAT_APP_SECRET) {
    console.error(`❌ API 凭证不完整，请检查 ${ENV_FILE}`);
    process.exit(1);
  }

  return config;
}

/** 发送 HTTPS 请求，返回 Promise<object> */
function httpRequest(url, options = {}, body = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, { timeout: 30000, ...options }, (res) => {
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        try {
          resolve(JSON.parse(Buffer.concat(chunks).toString('utf-8')));
        } catch (e) {
          reject(new Error(`JSON 解析失败: ${Buffer.concat(chunks).toString('utf-8')}`));
        }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('请求超时')); });
    if (body) req.write(body);
    req.end();
  });
}

function apiGet(url) {
  return httpRequest(url).catch((e) => {
    console.error(`❌ 网络请求失败：${e.message}`);
    process.exit(1);
  });
}

function apiPostJson(url, data) {
  const body = Buffer.from(JSON.stringify(data), 'utf-8');
  return httpRequest(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Content-Length': body.length },
  }, body).catch((e) => {
    console.error(`❌ 网络请求失败：${e.message}`);
    process.exit(1);
  });
}

function apiPostMultipart(url, filePath, fieldName = 'media') {
  const boundary = `----WebKitFormBoundary${crypto.randomBytes(8).toString('hex')}`;
  const fileName = path.basename(filePath);
  const mimeType = guessMimeType(filePath);
  const fileData = fs.readFileSync(filePath);

  const header = Buffer.from(
    `--${boundary}\r\n` +
    `Content-Disposition: form-data; name="${fieldName}"; filename="${fileName}"\r\n` +
    `Content-Type: ${mimeType}\r\n` +
    `\r\n`,
    'utf-8'
  );
  const footer = Buffer.from(`\r\n--${boundary}--\r\n`, 'utf-8');
  const body = Buffer.concat([header, fileData, footer]);

  return new Promise((resolve, reject) => {
    const req = https.request(url, {
      method: 'POST',
      headers: {
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': body.length,
      },
      timeout: 60000,
    }, (res) => {
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        try {
          resolve(JSON.parse(Buffer.concat(chunks).toString('utf-8')));
        } catch (e) {
          reject(new Error(`JSON 解析失败`));
        }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('上传超时')); });
    req.write(body);
    req.end();
  }).catch((e) => {
    console.error(`❌ 文件上传失败：${e.message}`);
    process.exit(1);
  });
}

async function getAccessToken() {
  const config = loadEnv();

  // 检查缓存
  if (fs.existsSync(TOKEN_CACHE)) {
    try {
      const lines = fs.readFileSync(TOKEN_CACHE, 'utf-8').trim().split('\n');
      if (lines.length >= 2) {
        const cachedTime = parseInt(lines[0], 10);
        const cachedToken = lines[1];
        if (Math.floor(Date.now() / 1000) - cachedTime < 6900 && cachedToken) {
          return cachedToken;
        }
      }
    } catch (_) { /* cache miss */ }
  }

  // 请求新 token
  const url = `${API_BASE}/cgi-bin/token?grant_type=client_credential&appid=${config.WECHAT_APP_ID}&secret=${config.WECHAT_APP_SECRET}`;
  const data = await apiGet(url);

  const errcode = data.errcode || 0;
  if (errcode !== 0) {
    console.error(`❌ 获取 access_token 失败：[${errcode}] ${data.errmsg || 'unknown'}`);
    console.error('   常见原因：');
    console.error('   - IP 未加入白名单（公众平台 → 开发 → 基本配置 → IP 白名单）');
    console.error('   - AppID 或 AppSecret 错误');
    console.error('   - 账号类型无此权限');
    process.exit(1);
  }

  const token = data.access_token || '';
  if (!token) {
    console.error(`❌ 解析 access_token 失败，响应：${JSON.stringify(data)}`);
    process.exit(1);
  }

  // 写入缓存
  const cacheDir = path.dirname(TOKEN_CACHE);
  fs.mkdirSync(cacheDir, { recursive: true });
  fs.writeFileSync(TOKEN_CACHE, `${Math.floor(Date.now() / 1000)}\n${token}\n`, 'utf-8');

  return token;
}

// ============================================================
// 命令实现
// ============================================================

async function cmdToken() {
  const token = await getAccessToken();
  console.log('✅ access_token 获取成功（已缓存）');
  console.log(`   Token: ${token.slice(0, 20)}...`);
}

async function cmdUploadThumb(filePath) {
  if (!filePath || !fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
    console.log('用法：node wechat_publish.cjs upload-thumb <图片路径>');
    console.log('   支持格式：JPG/PNG，大小 < 2MB');
    process.exit(1);
  }

  const token = await getAccessToken();
  const url = `${API_BASE}/cgi-bin/material/add_material?access_token=${token}&type=thumb`;
  const data = await apiPostMultipart(url, filePath);

  if (!data.media_id) {
    console.error(`❌ 上传封面图失败：${JSON.stringify(data)}`);
    process.exit(1);
  }

  console.log('✅ 封面图上传成功');
  console.log(`   media_id: ${data.media_id}`);
}

async function cmdUploadImage(filePath) {
  if (!filePath || !fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
    console.log('用法：node wechat_publish.cjs upload-image <图片路径>');
    console.log('   支持格式：JPG/PNG，大小 < 1MB');
    process.exit(1);
  }

  const token = await getAccessToken();
  const url = `${API_BASE}/cgi-bin/media/uploadimg?access_token=${token}`;
  const data = await apiPostMultipart(url, filePath);

  if (!data.url) {
    console.error(`❌ 上传图片失败：${JSON.stringify(data)}`);
    process.exit(1);
  }

  console.log('✅ 图片上传成功');
  console.log(`   URL: ${data.url}`);
}

async function cmdCreateDraft(jsonFile) {
  if (!jsonFile || !fs.existsSync(jsonFile) || !fs.statSync(jsonFile).isFile()) {
    console.log('用法：node wechat_publish.cjs create-draft <文章JSON路径>');
    console.log();
    console.log('JSON 格式示例：');
    const example = {
      articles: [{
        title: '文章标题',
        author: '作者名',
        content: '<p>HTML正文内容</p>',
        thumb_media_id: '封面图media_id',
        digest: '文章摘要(64字以内)',
        need_open_comment: 1,
        only_fans_can_comment: 0,
      }],
    };
    console.log(JSON.stringify(example, null, 2));
    process.exit(1);
  }

  const articlesData = JSON.parse(fs.readFileSync(jsonFile, 'utf-8'));
  const token = await getAccessToken();
  const url = `${API_BASE}/cgi-bin/draft/add?access_token=${token}`;
  const data = await apiPostJson(url, articlesData);

  if (!data.media_id) {
    console.error(`❌ 创建草稿失败：${JSON.stringify(data)}`);
    process.exit(1);
  }

  console.log('✅ 草稿创建成功');
  console.log(`   media_id: ${data.media_id}`);
  console.log(`   下一步：确认后执行 node wechat_publish.cjs publish ${data.media_id}`);
}

async function cmdPublish(mediaId) {
  if (!mediaId) {
    console.log('用法：node wechat_publish.cjs publish <草稿media_id>');
    process.exit(1);
  }

  const token = await getAccessToken();
  const url = `${API_BASE}/cgi-bin/freepublish/submit?access_token=${token}`;
  const data = await apiPostJson(url, { media_id: mediaId });

  if ((data.errcode || 0) !== 0) {
    console.error(`❌ 发布失败：${JSON.stringify(data)}`);
    process.exit(1);
  }

  console.log('✅ 发布请求已提交');
  console.log(`   publish_id: ${data.publish_id || ''}`);
  console.log('   发布为异步操作，请稍后查询状态：');
  console.log(`   node wechat_publish.cjs get-status ${data.publish_id || ''}`);
}

async function cmdGetStatus(publishId) {
  if (!publishId) {
    console.log('用法：node wechat_publish.cjs get-status <publish_id>');
    process.exit(1);
  }

  const token = await getAccessToken();
  const url = `${API_BASE}/cgi-bin/freepublish/get?access_token=${token}`;
  const data = await apiPostJson(url, { publish_id: publishId });
  console.log(JSON.stringify(data, null, 2));
}

async function cmdGetStats(beginDate, endDate) {
  if (!beginDate || !endDate) {
    console.log('用法：node wechat_publish.cjs get-stats <开始日期> <结束日期>');
    console.log('   日期格式：YYYY-MM-DD，时间跨度不超过 1 天');
    console.log('   示例：node wechat_publish.cjs get-stats 2026-03-20 2026-03-20');
    process.exit(1);
  }

  const token = await getAccessToken();
  const url = `${API_BASE}/datacube/getarticlesummary?access_token=${token}`;
  const data = await apiPostJson(url, { begin_date: beginDate, end_date: endDate });

  console.log(`📊 图文数据统计（${beginDate} ~ ${endDate}）`);
  console.log(JSON.stringify(data, null, 2));
}

function printUsage() {
  console.log('微信公众平台发布工具');
  console.log();
  console.log('用法：node wechat_publish.cjs <command> [args]');
  console.log();
  console.log('命令：');
  console.log('  token                    获取/刷新 access_token');
  console.log('  upload-thumb <图片路径>   上传封面图 → media_id');
  console.log('  upload-image <图片路径>   上传正文图片 → url');
  console.log('  create-draft <JSON路径>  创建草稿 → media_id');
  console.log('  publish <media_id>       发布草稿');
  console.log('  get-status <publish_id>  查询发布状态');
  console.log('  get-stats <开始> <结束>   获取图文数据统计');
  console.log();
  console.log(`首次使用前请确保已配置 API 凭证：${ENV_FILE}`);
}

// ============================================================
// 主入口
// ============================================================

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printUsage();
    process.exit(0);
  }

  const command = args[0];

  const commands = {
    'token': () => cmdToken(),
    'upload-thumb': () => cmdUploadThumb(args[1] || null),
    'upload-image': () => cmdUploadImage(args[1] || null),
    'create-draft': () => cmdCreateDraft(args[1] || null),
    'publish': () => cmdPublish(args[1] || null),
    'get-status': () => cmdGetStatus(args[1] || null),
    'get-stats': () => cmdGetStats(args[1] || null, args[2] || null),
  };

  if (commands[command]) {
    await commands[command]();
  } else {
    console.error(`❌ 未知命令：${command}`);
    console.log();
    printUsage();
    process.exit(1);
  }
}

main().catch((e) => {
  console.error(`❌ 未预期的错误：${e.message}`);
  process.exit(1);
});
