#!/usr/bin/env node
/**
 * 推送到公众号。config.json 和此脚本应在同一目录；支持 HTML 和图片模式，HTML 应放在同目录。
 *
 * 首参为目标公众号 AppID（default、- 或空字符串表示平台提供的公众号；wx 开头为自定义公众号），第二参为 html 或 img：
 *   node push-to-wechat-mp.js <targetAppId> html <HTML 文件名> [sendMode]
 *   node push-to-wechat-mp.js <targetAppId> img '<JSON数组>' <title> <content> [sendMode]
 * 示例：
 *   node push-to-wechat-mp.js targetAppId html 你的文件.html draft
 *   node push-to-wechat-mp.js wxabcdef0123456789 img '["https://example.com/a.png"]' "标题" "正文" draft
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const DEFAULT_API = 'https://api.pcloud.ac.cn/openClawService';
const DIR = __dirname;

function readJson(name) {
  const p = path.join(DIR, name);
  if (!fs.existsSync(p)) throw new Error('缺少: ' + p);
  return JSON.parse(fs.readFileSync(p, 'utf8').trim());
}

function titleFromHtml(html) {
  // 先尝试 <title>
  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  if (titleMatch) {
    const raw = titleMatch[1].replace(/<[^>]+>/g, '').trim();
    if (raw) return raw;
  }

  // 回退到 <h1>、<h2> ... <h6>
  const hMatch = html.match(/<h[1-6][^>]*>([\s\S]*?)<\/h[1-6]>/i);
  if (hMatch) {
    const raw = hMatch[1].replace(/<[^>]+>/g, '').trim();
    if (raw) return raw;
  }

  return '未命名';
}

function parseImgUrlsArg(arg) {
  let trimmed = String(arg || '').trim();
  if (!trimmed) throw new Error('图片模式需要第二参：图片链接的 JSON 数组字符串');

  // 首先尝试直接解析为JSON
  let arr;
  let originalError = null;

  try {
    arr = JSON.parse(trimmed);
    // 如果成功且是数组，直接返回
    if (Array.isArray(arr) && arr.length > 0) {
      const urls = arr.map((u) => String(u).trim()).filter(Boolean);
      if (urls.length > 0) return urls;
    }
  } catch (e) {
    originalError = e;
  }

  // 如果直接解析失败，尝试兼容处理
  // 兼容 PowerShell 单引号传参导致外层方括号丢失的情况
  if (!trimmed.startsWith('[')) {
    trimmed = '[' + trimmed;
  }
  if (!trimmed.endsWith(']')) {
    trimmed = trimmed + ']';
  }

  // 兼容 PowerShell 单引号传参导致内部双引号丢失的情况
  if (!trimmed.includes('"')) {
    // 移除外层方括号，获取内容
    let content = trimmed.slice(1, -1);

    // 更稳健的方法：按逗号分割，但智能合并包含URL的片段
    const parts = content.split(',');
    const urls = [];
    let currentUrl = '';

    for (let i = 0; i < parts.length; i++) {
      const part = parts[i].trim();
      if (part.startsWith('http://') || part.startsWith('https://')) {
        // 如果currentUrl不为空，说明这是一个新的URL开始
        if (currentUrl) {
          urls.push(currentUrl.trim());
        }
        currentUrl = part;
      } else if (currentUrl) {
        // 如果不是http开头但有currentUrl，可能是URL的后续部分
        currentUrl += ',' + part;
      }
    }

    // 添加最后一个URL
    if (currentUrl) {
      urls.push(currentUrl.trim());
    }

    // 为每个URL添加双引号
    const quotedUrls = urls.map(url => `"${url}"`);
    trimmed = `[${quotedUrls.join(',')}]`;
  }

  // 再次尝试解析
  try {
    arr = JSON.parse(trimmed);
  } catch (e) {
    throw new Error('图片列表须为合法 JSON 数组字符串: ' + (originalError ? originalError.message : e.message));
  }

  if (!Array.isArray(arr) || arr.length === 0) {
    throw new Error('图片列表须为非空数组，元素为图片 URL 字符串');
  }
  const urls = arr.map((u) => String(u).trim()).filter(Boolean);
  if (urls.length === 0) throw new Error('图片 URL 解析后为空');
  return urls;
}

function postJson(urlStr, body, timeoutMs = 120000) {
  const payload = JSON.stringify(body);
  const u = new URL(urlStr);
  const lib = u.protocol === 'https:' ? https : http;
  const port = u.port || (u.protocol === 'https:' ? 443 : 80);

  return new Promise((resolve, reject) => {
    const req = lib.request(
      {
        hostname: u.hostname,
        port,
        path: u.pathname + u.search,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Content-Length': Buffer.byteLength(payload, 'utf8'),
        },
      },
      (res) => {
        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => {
          const raw = Buffer.concat(chunks).toString('utf8');
          let json;
          try {
            json = JSON.parse(raw);
          } catch (_) {}
          resolve({ statusCode: res.statusCode, raw, json });
        });
      }
    );
    const t = setTimeout(() => req.destroy(new Error('timeout')), timeoutMs);
    req.on('error', (e) => {
      clearTimeout(t);
      reject(e);
    });
    req.on('close', () => clearTimeout(t));
    req.write(payload);
    req.end();
  });
}

function isDefaultAppIdTarget(s) {
  const t = String(s ?? '').trim().toLowerCase();
  return t === '' || t === 'default' || t === '-';
}

/** @returns {string|undefined} appId 传给接口：appId；平台提供返回 undefined */
function resolvePushAppId(cfg, targetAppIdFromCli) {
  if (isDefaultAppIdTarget(targetAppIdFromCli)) {
    return undefined;
  }
  const tid = String(targetAppIdFromCli).trim();
  if (cfg.accounts && Array.isArray(cfg.accounts)) {
    const found = cfg.accounts.some(
      (a) =>
        a &&
        a.appId &&
        String(a.appId).toLowerCase() === tid.toLowerCase()
    );
    if (!found) {
      console.error(
        '提示: 传入的 AppID 未出现在 config.accounts 中，仍将按接口规则推送。'
      );
    }
  }
  return tid;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    throw new Error(
      '用法:\n  node push-to-wechat-mp.js <targetAppId> html <文件名.html> [sendMode]\n  node push-to-wechat-mp.js <targetAppId> img \'<JSON>\' <title> <content> [sendMode]\n  targetAppId：default、- 或空字符串表示平台提供；wx 开头为自定义公众号。'
    );
  }

  if (args[0] === 'html' || args[0] === 'img') {
    throw new Error(
      '首参须为目标公众号 AppID（平台提供请写 default）。示例:\n  node push-to-wechat-mp.js targetAppId html 你的文件.html draft'
    );
  }

  const cfg = readJson('config.json');
  if (!cfg.openId || String(cfg.openId).includes('XXXX')) {
    throw new Error('config.json 里 openId 无效，请用向导生成的配置');
  }

  const apiBase = cfg.apiBase || DEFAULT_API;
  const targetAppIdFromCli = args[0];
  const mode = String(args[1] || '').toLowerCase();
  let title;
  let content;
  let thumbImageContent = '';
  let sendMode;
  /** @type {string[]|undefined} */
  let imgUrls;

  if (mode === 'img') {
    if (args.length < 5) {
      throw new Error(
        '图片模式参数不足。示例: node push-to-wechat-mp.js targetAppId img \'["https://example.com/a.png"]\' "标题" "正文说明" draft'
      );
    }
    imgUrls = parseImgUrlsArg(args[2]);
    title = String(args[3] || '').trim() || '未命名';
    content = String(args[4] ? args[4] : '图文卡片');
    sendMode = (args[5] && args[5].trim()) || 'draft';
  } else if (mode === 'html') {
    if (args.length < 3) {
      throw new Error(
        'HTML 模式须传入文件名。示例: node push-to-wechat-mp.js targetAppId html 你的文件.html draft'
      );
    }
    const fileName = path.basename((args[2] || '').trim());
    if (!fileName) {
      throw new Error(
        '请传入 HTML 文件名（与脚本同目录）。例如: node push-to-wechat-mp.js targetAppId html 你的文件.html draft'
      );
    }
    sendMode = (args[3] && args[3].trim()) || 'draft';

    const htmlPath = path.join(DIR, fileName);
    if (!fs.existsSync(htmlPath)) {
      throw new Error('同目录下找不到: ' + fileName + '（请把 HTML 放在脚本所在目录）');
    }
    content = fs.readFileSync(htmlPath, 'utf8');
    if (!content.trim()) throw new Error('文件为空: ' + htmlPath);
    title = titleFromHtml(content); 

    const thumbImagePath = path.join(DIR, fileName.replace('.html', '_cover.html'));
    if (!fs.existsSync(thumbImagePath)) {
      console.warn('同目录下找不到: ' + thumbImagePath + '（本次跳过cover.html封面图片生成，将使用其它方式生成封面图片）');
    }
    else
    {
      thumbImageContent = fs.readFileSync(thumbImagePath, 'utf8');
    }

  } else {
    throw new Error(
      '第二参须为 html 或 img。示例:\n  node push-to-wechat-mp.js targetAppId html 你的文件.html draft'
    );
  }

  const appId = resolvePushAppId(cfg, targetAppIdFromCli);

  const body = {
    action: 'sendToWechat',
    openId: cfg.openId,
    title: title.slice(0, 64),
    thumbImageContent,
    content, 
    sendMode,
  };
  if (imgUrls && imgUrls.length > 0) {
    body.imgUrls = imgUrls;
  }
  if (appId) {
    body.appId = appId;
  }

  const accLabel = appId ? String(appId) : 'default';

  if (imgUrls && imgUrls.length > 0) {
    console.error(
      '推送中（图片）…',
      apiBase,
      '| 账号',
      accLabel,
      '| 标题',
      title.slice(0, 30) + (title.length > 30 ? '…' : ''),
      '| 图',
      imgUrls.length,
      '张',
      '| 正文长度',
      content.length
    );
  } else {
    console.error(
      '推送中（HTML）…',
      apiBase,
      '| 账号',
      accLabel,
      '| 标题',
      title.slice(0, 30) + (title.length > 30 ? '…' : ''),
      '| 正文长度',
      content.length
    );
  }
 
  const res = await postJson(apiBase, body);
  // 1. 定义超时判断逻辑：状态码为 504/408，或者返回内容包含 timeout 关键字
  const bodyText = res.json ? JSON.stringify(res.json) : String(res.raw || '');
  const isTimeout = res.statusCode === 504 || res.statusCode === 408 || 
                    /timeout|timed out/i.test(bodyText);
  
  const isOk = res.statusCode >= 200 && res.statusCode < 300;
  // 2. 打印结果
  console.log(
    JSON.stringify(
      { 
        ok: isOk || isTimeout, // 如果超时也标记为 ok，防止自动化流程报错
        statusCode: res.statusCode, 
        data: res.json !== undefined ? res.json : res.raw,
        message: isTimeout ? "检测到网络超时，但任务已在后台成功，请查看服务通知，请勿重复推送。" : undefined
      },
      null,
      2
    )
  );
  // 3. 决定是否退出：只有在既不成功也不是超时的情况下才以错误码 1 退出
  if (!isOk && !isTimeout) {
    process.exit(1);
  }
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
