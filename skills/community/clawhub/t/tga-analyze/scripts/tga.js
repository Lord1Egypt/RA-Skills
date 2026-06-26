#!/usr/bin/env node
/**
 * TGA 登录与下载脚本。从本技能目录读取 .env 与 .tga-token。
 * 用法：
 *   node tga.js login
 *   node tga.js download <projectId> <dashboardId> [outputDir] [--task-id=<id>]
 * 若轮询中途断掉但服务端已生成完成，可用 --task-id=<上文的 taskId> 跳过启动、直接轮询并下载。
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const SKILL_DIR = path.resolve(__dirname, '..');
const ENV_PATH = path.join(SKILL_DIR, '.env');
const TOKEN_PATH = path.join(SKILL_DIR, '.tga-token');

const BASE = 'https://tga-web.hortorgames.com';

// 与 example.md 中 curl 完全一致的请求头（不精简）
const FULL_HEADERS = {
  'accept': 'application/json',
  'accept-language': 'zh-CN',
  'cache-control': 'no-cache',
  'pragma': 'no-cache',
  'priority': 'u=1, i',
  'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
  'x-requested-with': 'XMLHttpRequest',
};

function loadEnv() {
  if (!fs.existsSync(ENV_PATH)) {
    console.error('缺少 .env 文件，路径:', ENV_PATH);
    process.exit(1);
  }
  const raw = fs.readFileSync(ENV_PATH, 'utf8');
  const env = {};
  for (const line of raw.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eq = trimmed.indexOf('=');
    if (eq <= 0) continue;
    const key = trimmed.slice(0, eq).trim();
    let val = trimmed.slice(eq + 1).trim();
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'")))
      val = val.slice(1, -1);
    env[key] = val;
  }
  for (const k of ['TGA_LOGIN_NAME', 'TGA_ENCRYPTED_PASSWORD', 'TGA_COOKIES']) {
    if (!env[k]) {
      console.error('.env 中缺少:', k);
      process.exit(1);
    }
  }
  return env;
}

function loadToken() {
  if (!fs.existsSync(TOKEN_PATH)) return null;
  try {
    const j = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
    return j && j.token ? j.token : null;
  } catch {
    return null;
  }
}

function saveToken(token) {
  fs.writeFileSync(TOKEN_PATH, JSON.stringify({ token }, null, 0), 'utf8');
  console.log('Token 已写入:', TOKEN_PATH);
}

function request(options, body) {
  return new Promise((resolve, reject) => {
    const pathOrUrl = options.path;
    const url = pathOrUrl.startsWith('http') ? new URL(pathOrUrl) : new URL(pathOrUrl, BASE);
    const isHttps = url.protocol === 'https:';
    const lib = isHttps ? https : require('http');
    const baseHeaders = url.origin === BASE
      ? { ...FULL_HEADERS, 'origin': BASE, 'referer': options.referer || BASE + '/' }
      : { 'accept': '*/*', 'user-agent': FULL_HEADERS['user-agent'] };
    const req = lib.request({
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname + url.search,
      method: options.method || 'GET',
      headers: { ...baseHeaders, ...options.headers },
    }, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        const buf = Buffer.concat(chunks);
        if (options.binary) {
          resolve({ status: res.statusCode, headers: res.headers, body: buf });
        } else {
          resolve({ status: res.statusCode, headers: res.headers, body: buf.toString('utf8') });
        }
      });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

async function login() {
  const env = loadEnv();
  // 与 curl --data-raw 一致：body 原样发送。enPassword 在 .env 里已是前端/浏览器给出的编码值（含 %2B、%3D 等），不可再用 URLSearchParams 二次编码，否则 % 会变成 %25 导致登录失败
  const body = `loginName=${encodeURIComponent(env.TGA_LOGIN_NAME)}&enPassword=${env.TGA_ENCRYPTED_PASSWORD}&locale=zh_CN`;

  // 与 example.md 登录 curl 完全一致：全部 header + -b cookie
  const res = await request({
    method: 'POST',
    path: '/v1/oauth/loginForToken',
    referer: BASE + '/oauth/',
    headers: {
      'content-type': 'application/x-www-form-urlencoded',
      'cookie': env.TGA_COOKIES,
    },
  }, body);

  if (res.status !== 200) {
    console.error('登录请求失败 status:', res.status, res.body?.slice(0, 300));
    process.exit(1);
  }

  let data;
  try {
    data = JSON.parse(res.body);
  } catch {
    console.error('登录响应非 JSON:', res.body?.slice(0, 200));
    process.exit(1);
  }

  const token = data.data?.oAuthLoginInfo?.accessToken
    ?? data.data?.tokenInfo?.accessToken
    ?? data.data?.token
    ?? data.token;
  if (!token) {
    console.error('响应中未找到 token:', JSON.stringify(data).slice(0, 300));
    process.exit(1);
  }

  saveToken(token);
  console.log('登录成功');
}

function baseDate() {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const h = String(d.getHours()).padStart(2, '0');
  const min = String(d.getMinutes()).padStart(2, '0');
  const s = String(d.getSeconds()).padStart(2, '0');
  return `${y}-${m}-${day} ${h}:${min}:${s}`;
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function download(projectId, dashboardId, outputDir, taskIdOpt) {
  const token = loadToken();
  if (!token) {
    console.error('未找到 token，请先执行: node tga.js login');
    process.exit(1);
  }

  const env = loadEnv();
  const dir = outputDir || path.join(process.cwd(), 'tga-downloads');
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  let taskId = taskIdOpt;

  if (taskId == null) {
    // ---------- 1. 启动下载（example.md 启动下载指令）----------
    const startBody = JSON.stringify({
      dashboardId: Number(dashboardId),
      commonFilter: '',
      startTime: '',
      endTime: '',
      recentDay: '',
      baseDate: baseDate(),
    });

    const startRes = await request({
      method: 'POST',
      path: `/v1/ta/dashbord/dashboardReportsBatchDownload?projectId=${projectId}&zoneOffset=99`,
      referer: BASE + '/',
      headers: {
        'content-type': 'application/json',
        'authorization': 'bearer ' + token,
        'cookie': env.TGA_COOKIES,
        'content-translate': '',
      },
    }, startBody);

    if (startRes.status === 401) {
      console.error('Token 失效 (401)，请重新登录: node tga.js login');
      process.exit(1);
    }
    if (startRes.status !== 200) {
      console.error('启动下载失败 status:', startRes.status, startRes.body?.slice(0, 300));
      process.exit(1);
    }

    let startData;
    try {
      startData = JSON.parse(startRes.body);
    } catch {
      console.error('启动下载响应非 JSON:', startRes.body?.slice(0, 200));
      process.exit(1);
    }

    taskId = startData.data?.taskId ?? startData.taskId ?? startData.data?.data?.taskId;
    if (taskId == null && Array.isArray(startData.data) && startData.data[0]) taskId = startData.data[0].taskId;
    if (taskId == null) {
      console.error('响应中未找到 taskId:', JSON.stringify(startData).slice(0, 400));
      process.exit(1);
    }
    console.log('已提交任务 taskId:', taskId, '（若中途断掉可加 --task-id=' + taskId + ' 从进度轮询继续）');
  } else {
    console.log('使用已有 taskId:', taskId, '，跳过启动直接轮询并下载');
  }

  // ---------- 2. 轮询进度（example.md 查询进度），单次失败会重试不退出 ----------
  const progressPath = `/v1/ta/auth/manage/task/asyncTaskProgress`;
  const maxPolls = 120;
  const pollIntervalMs = 3000;
  const progressRetries = 4;

  for (let i = 0; i < maxPolls; i++) {
    await sleep(pollIntervalMs);

    let progressData = null;
    for (let r = 0; r < progressRetries; r++) {
      try {
        const q = `@t=${Date.now()}&projectId=${projectId}&taskIds=${taskId}`;
        const progressRes = await request({
          method: 'GET',
          path: `${progressPath}?${q}`,
          referer: BASE + '/',
          headers: {
            'content-type': 'application/x-www-form-urlencoded',
            'authorization': 'bearer ' + token,
            'cookie': env.TGA_COOKIES,
            'content-translate': '',
          },
        });

        if (progressRes.status !== 200) {
          if (r < progressRetries - 1) {
            await sleep(2000);
            continue;
          }
          break;
        }

        progressData = JSON.parse(progressRes.body);
        break;
      } catch (e) {
        if (r < progressRetries - 1) {
          console.log('查询进度请求异常，' + (r + 1) + '/' + progressRetries + ' 重试…');
          await sleep(2000);
        } else {
          console.log('查询进度多次失败，本轮跳过，继续轮询');
        }
      }
    }

    if (progressData == null) continue;

    const list = progressData.data;
    const item = Array.isArray(list) && list[0] ? list[0] : null;
    const status = item?.asyncTaskStatus;
    const progress = item?.progress;

    if (status === 'async_ok' && progress === 100) {
      console.log('任务已完成');
      break;
    }

    if (i === 0 || (i % 5 === 0)) {
      console.log(`进度: ${status || 'unknown'} ${progress != null ? progress + '%' : ''}`);
    }

    if (i === maxPolls - 1) {
      console.error('轮询超时，未等到 async_ok。可稍后用相同 taskId 继续: node tga.js download ' + projectId + ' ' + dashboardId + ' [outputDir] --task-id=' + taskId);
      process.exit(1);
    }
  }

  // ---------- 3. 真正的下载（example.md 真正的下载）----------
  const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const filename = `${projectId}_${dashboardId}_${ts}.zip`;
  const filepath = path.join(dir, filename);

  const downloadPath = `/v1/ta/auth/manage/task/taskFileDownload?access_token=${encodeURIComponent(token)}&projectId=${projectId}&taskId=${taskId}`;
  const downloadHeaders = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'cookie': env.TGA_COOKIES,
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': BASE + '/',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': FULL_HEADERS['user-agent'],
  };

  const fileRes = await request({
    method: 'GET',
    path: downloadPath,
    referer: BASE + '/',
    binary: true,
    headers: downloadHeaders,
  });

  if (fileRes.status !== 200) {
    console.error('下载文件失败 status:', fileRes.status);
    process.exit(1);
  }

  fs.writeFileSync(filepath, fileRes.body);
  console.log('已保存:', filepath);
  return filepath;
}

const cmd = process.argv[2];
if (cmd === 'login') {
  login().catch((e) => {
    console.error(e);
    process.exit(1);
  });
} else if (cmd === 'download') {
  const args = process.argv.slice(3).filter((a) => !a.startsWith('--task-id=') && !a.startsWith('--taskId='));
  let taskIdOpt = null;
  for (const a of process.argv) {
    if (a.startsWith('--task-id=')) taskIdOpt = a.slice('--task-id='.length);
    else if (a.startsWith('--taskId=')) taskIdOpt = a.slice('--taskId='.length);
  }
  const projectId = args[0];
  const dashboardId = args[1];
  const outputDir = args[2];
  if (!projectId || !dashboardId) {
    console.error('用法: node tga.js download <projectId> <dashboardId> [outputDir] [--task-id=<id>]');
    process.exit(1);
  }
  download(projectId, dashboardId, outputDir, taskIdOpt || undefined).catch((e) => {
    console.error(e);
    process.exit(1);
  });
} else {
  console.log('用法:');
  console.log('  node tga.js login');
  console.log('  node tga.js download <projectId> <dashboardId> [outputDir] [--task-id=<id>]');
  console.log('  若轮询中途断掉，任务已生成完成时可用 --task-id=<上文的 taskId> 直接轮询并下载');
  process.exit(1);
}
