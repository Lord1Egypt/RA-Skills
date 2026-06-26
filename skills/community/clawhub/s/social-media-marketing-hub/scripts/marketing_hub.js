#!/usr/bin/env node
/**
 * 社交媒体营销中心 v8.1 - 抖音版 + 记忆学习系统
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const CONFIG_FILE = path.join(__dirname, 'config.js');
const MEMORY_DIR = path.join(__dirname, 'memory');

function loadConfig() {
  // 优先读取环境变量，兼容旧配置文件的 fallback
  const fromEnv = { TIKHUB_TOKEN: process.env.TIKHUB_TOKEN || '', DEEPSEEK_KEY: process.env.DEEPSEEK_KEY || '' };
  if (fromEnv.TIKHUB_TOKEN || fromEnv.DEEPSEEK_KEY) return fromEnv;
  return fs.existsSync(CONFIG_FILE) ? require(CONFIG_FILE) : { TIKHUB_TOKEN: '', DEEPSEEK_KEY: '' };
}

function saveConfig(tikhubToken, deepseekKey) {
  // 推荐使用环境变量 TIKHUB_TOKEN / DEEPSEEK_KEY
  console.log('\n⚠️ 建议使用环境变量配置 API Key，更安全:\n');
  console.log('  export TIKHUB_TOKEN=' + (tikhubToken || '你的Token'));
  console.log('  export DEEPSEEK_KEY=' + (deepseekKey || '你的Key'));
  console.log('\n或者在启动 openclaw 的 shell 环境中设置这些变量。\n');
}

function initMemory() {
  if (!fs.existsSync(MEMORY_DIR)) fs.mkdirSync(MEMORY_DIR, { recursive: true });
}

function getMemory(keyword) {
  initMemory();
  const file = path.join(MEMORY_DIR, `${keyword}.json`);
  return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) : null;
}

function saveMemory(keyword, data) {
  initMemory();
  const file = path.join(MEMORY_DIR, `${keyword}.json`);
  const existing = fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) : {};
  const merged = {
    keyword: data.keyword || keyword,
    count: (existing.count || 0) + 1,
    updatedAt: new Date().toISOString(),
    openingPatterns: [...new Set([...(existing.openingPatterns || []), ...(data.openingPatterns || [])])].slice(0, 20),
    structures: [...new Set([...(existing.structures || []), ...(data.structures || [])])].slice(0, 10),
    topTags: data.topTags || existing.topTags || [],
    titleTemplates: [...new Set([...(existing.titleTemplates || []), ...(data.titleTemplates || [])])].slice(0, 30),
    commentNeeds: [...new Set([...(existing.commentNeeds || []), ...(data.commentNeeds || [])])].slice(0, 20),
    bestDuration: data.bestDuration || existing.bestDuration,
    stats: data.stats || existing.stats,
    videos: [...(data.videos || []), ...(existing.videos || [])].slice(0, 20),
    insights: data.insights || existing.insights || [],
    products: data.products || existing.products || [],
    // 作者/选品分析专用字段
    type: data.type || existing.type || null,
    topTitles: data.topTitles || existing.topTitles || [],
    analysisText: data.analysisText || existing.analysisText || '',
    productInsights: [...new Set([...(existing.productInsights || []), ...(data.productInsights || [])])].slice(0, 10),
  };
  fs.writeFileSync(file, JSON.stringify(merged, null, 2));
  return merged;
}

function listMemory() {
  initMemory();
  return fs.readdirSync(MEMORY_DIR).filter(f => f.endsWith('.json')).map(f => {
    const d = JSON.parse(fs.readFileSync(path.join(MEMORY_DIR, f), 'utf8'));
    return { keyword: f.replace('.json', ''), count: d.count || 0, updatedAt: d.updatedAt || '' };
  });
}

function parseArgs(args) {
  const r = { positional: [], flags: {} };
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const [k, v] = args[i].slice(2).split('=');
      r.flags[k] = v === undefined ? true : v;
    } else r.positional.push(args[i]);
  }
  return r;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 自然语言路由解析
// 把 "用浏览器分析风水" → { cmd: 'analyze', keyword: '风水', flags: { browser: true } }
// 把 "小红书分析护肤" → { cmd: 'xhs', keyword: '护肤', flags: {} }
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function parseNaturalLanguage(input) {
  if (!input || typeof input !== 'string') return null;
  const text = input.trim();

  // 模式检测：浏览器 vs API
  const isBrowser = /浏览器|browser|chrom|开浏览器/i.test(text);

  // 平台检测

  const isDouyin = /抖音|douyin/i.test(text);

  // 动作检测
  const isAnalyze = /分析|学习|调研|研究/i.test(text);
  const isQuick = /快速|快看|^a$|a\s/i.test(text);
  const isTitles = /标题|title|爆款标题/i.test(text);
  const isScript = /脚本|文案|内容生成/i.test(text);
  const isProduct = /商品|带货|佣金|product/i.test(text);
  const isDashboard = /看板|dashboard|面板|可视化/i.test(text);
  const isMemory = /记忆|学过的|已分析|看记忆/i.test(text);
  const isExport = /导出|csv|表格/i.test(text);
  const isFull = /全套|一键|all/i.test(text);

  // 提取关键词
  function extractKeyword(raw) {
    let kw = raw
      .replace(/用(浏览器|API|接口|直接)?/g, ' ')
      .replace(/(分析|学习|调研|研究|搜索|查找|找一下|快速|快看|生成)/g, ' ')
      .replace(/(抖音|douyin)/gi, ' ')
      .replace(/(视频|做成视频|生成视频|拍视频|看板|dashboard|面板|可视化|记忆|学过的|已分析|看记忆|导出|csv|表格|标题|爆款标题|脚本|文案|内容生成|商品|带货|佣金|product|全套|一键|all)/g, ' ')
      .replace(/--browser|--api|-n|--days|--sort|--has-product/g, ' ')
      .replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim()
      .split(/\s+/)
      .filter(w => w.length > 1)
      .join(' ');
    return kw || '';
  }

  let keyword = extractKeyword(text);

  // 单独说平台名时当关键词用

  if (!keyword && isDouyin) { return { cmd: 'analyze', keyword: '抖音', flags: {} }; }

  // 确定命令（优先级：动作 > 平台）
  let cmd = 'help';
  if (isFull) cmd = 'full';
  else if (isDashboard) cmd = 'dashboard';
  else if (isExport) cmd = 'export';
  else if (isTitles) cmd = 'titles';
  else if (isScript) cmd = 'script';
  else if (isProduct) cmd = 'product';
  else if (isMemory) cmd = 'memory';
  else if (isDouyin && (isQuick || isTitles || isScript || isProduct)) cmd = 'analyze';
  else if (isAnalyze) cmd = 'analyze';
  else if (isQuick) cmd = 'a';
  else if (isDouyin) cmd = 'analyze';
  else if (keyword) cmd = 'analyze';

  const flags = {};
  if (isBrowser) flags.browser = true;

  return { cmd, keyword, flags, raw: text };
}

let _lastNetError = null;
function httpRequest(options, payload = null) {
  _lastNetError = null;
  return new Promise((res, rej) => {
    const req = https.request(options, (r) => {
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => {
        try { res(JSON.parse(d)); }
        catch { _lastNetError = '响应解析失败'; res(null); }
      });
    });
    req.on('error', (e) => { _lastNetError = '网络连接失败: ' + e.message; res(null); });
    req.setTimeout(60000, () => { req.destroy(); _lastNetError = '请求超时（60s）'; res(null); });
    if (payload) req.write(typeof payload === 'string' ? payload : JSON.stringify(payload));
    req.end();
  });
}
function clearNetError() { _lastNetError = null; }
function hasNetError() { return !!_lastNetError; }

function callAI(prompt, retries = 2) {
  return new Promise((res) => {
    if (!DEEPSEEK_KEY) { res('请配置DeepSeek API'); return; }
    const body = JSON.stringify({ model: 'deepseek-chat', messages: [{ role: 'user', content: prompt }], temperature: 0.8, max_tokens: 2000 });
    const opts = {
      hostname: 'api.deepseek.com',
      path: '/v1/chat/completions',
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + DEEPSEEK_KEY }
    };
    const tryReq = (attempt) => {
      httpRequest(opts, body).then(result => {
        if (!result || !result.choices?.[0]?.message?.content) {
          if (attempt < retries) { tryReq(attempt + 1); return; }
          res(''); return;
        }
        res(result.choices[0].message.content);
      }).catch(() => {
        if (attempt < retries) { tryReq(attempt + 1); return; }
        res('');
      });
    };
    tryReq(1);
  });
}

function formatNumber(n) {
  if (n >= 10000) return (n / 10000).toFixed(1) + 'w';
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k';
  return String(n || 0);
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 浏览器搜索模式（支持本地 OpenClaw 有头/无头浏览器）
// 自动检测环境：本地有桌面 → 打开真实浏览器 | 云端无桌面 → 用 Xvfb
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

const CHROME_BIN = '/usr/bin/google-chrome';

// 自动检测是否有真实桌面环境
function hasDesktop() {
  const desktop = process.env.DESKTOP_SESSION || '';
  const display = process.env.DISPLAY || '';
  const xdgSession = process.env.XDG_SESSION_TYPE || '';
  // 本地桌面：DESKTOP_SESSION 有值 或 DISPLAY 有值（Linux/Mac/Windows WSL）
  return !!(desktop || display || xdgSession);
}

// 获取可用的 DISPLAY（云端用 Xvfb，本地直接用 :0 或空）
function getDisplay() {
  if (hasDesktop()) {
    // 本地：尝试 :0 或当前 DISPLAY
    const current = process.env.DISPLAY || ':0';
    return current;
  } else {
    // 云端：用 Xvfb，启动或复用已有的
    return ensureXvfb();
  }
}

let _xvfbDisplay = null;
function ensureXvfb() {
  if (_xvfbDisplay) return _xvfbDisplay;
  const { execSync } = require('child_process');
  try {
    // 检查 :99 是否已在运行
    execSync('xdpyinfo -display :99 >/dev/null 2>&1', { stdio: 'ignore' });
    _xvfbDisplay = ':99';
    return ':99';
  } catch {
    // 启动新的 Xvfb
    execSync('pkill -f "Xvfb :[0-9]*" 2>/dev/null; sleep 1', { stdio: 'ignore' });
    const rand = Math.floor(Math.random() * 10) + 90;
    execSync(`Xvfb :${rand} -screen 0 1280x720x24 >/dev/null 2>&1 &`, { stdio: 'ignore' });
    sleep(2);
    _xvfbDisplay = `:${rand}`;
    return _xvfbDisplay;
  }
}

function sleep(ms) {
  return new Promise(res => setTimeout(res, ms));
}

async function chromeSearch(keyword, opts = {}) {
  const { headless = false, sort = '2' } = opts;
  const sortMap = { '2': '9', '1': '1', '0': '0' }; // 综合/最新/最热
  const url = `https://www.douyin.com/search/${encodeURIComponent(keyword)}?type=video&publish_time=${sortMap[sort] || '0'}`;
  const isLocal = hasDesktop();
  const display = getDisplay();
  
  console.log(`  🖥️ 检测环境: ${isLocal ? '本地桌面（真实浏览器）' : '云端服务器（虚拟显示器）'} → DISPLAY=${display}`);
  
  const args = [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-blink-features=AutomationControlled',
    `--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36`
  ];
  
  if (headless || !isLocal) {
    // 云端用无头，本地可选
    args.push('--headless=new');
  } else {
    // 本地有头：打开真实浏览器窗口（用户能看到！）
    args.push('--start-fullscreen');
    args.push('--new-window');
  }
  
  args.push(`--window-size=1280,720`);
  args.push('--dump-dom');
  args.push(url);
  
  return new Promise((resolve) => {
    const start = Date.now();
    const { execSync } = require('child_process');
    let output = '';
    try {
      const cmd = `DISPLAY=${display} ${CHROME_BIN} ${args.join(' ')} 2>/dev/null`;
      output = execSync(cmd, { timeout: 45000, encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 });
    } catch (e) {
      output = e.stdout || '';
    }
    const elapsed = Date.now() - start;
    
    // 解析 DOM 中的视频数据
    const videos = [];
    const videoIdRegex = /\/video\/(\d+)/g;
    let match;
    const seen = new Set();
    
    while ((match = videoIdRegex.exec(output)) !== null) {
      if (seen.has(match[1])) continue;
      seen.add(match[1]);
      const blockStart = Math.max(0, match.index - 500);
      const block = output.substring(blockStart, match.index + 200);
      const likes = extractNum(block, '赞');
      const comments = extractNum(block, '评论');
      if (likes > 0 || comments > 0) {
        videos.push({
          aweme_id: match[1],
          desc: block.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim().substring(0, 80),
          statistics: { digg_count: likes, comment_count: comments }
        });
      }
    }
    
    console.log(`  [浏览器] 抓取到 ${videos.length} 条数据 (${elapsed}ms)`);
    resolve(videos);
  });
}

function extractNum(text, label) {
  const patterns = [
    new RegExp(`(\\d+\\.?\\d*)\\s*${label}`, 'i'),
    new RegExp(`${label}[^0-9]*(\\d+\\.?\\d*[万万千]?)`, 'i'),
  ];
  for (const p of patterns) {
    const m = text.match(p);
    if (m) {
      const s = m[1].toLowerCase();
      if (s.includes('万')) return Math.round(parseFloat(s) * 10000);
      if (s.includes('千')) return Math.round(parseFloat(s) * 1000);
      return parseInt(s) || 0;
    }
  }
  return 0;
}

async function douyinSearch(keyword, opts = {}) {
  const { sort = '0', days = '0', hasProduct = false } = opts;
  if (!TIKHUB_TOKEN) return [];
  const payload = { keyword, cursor: 0, sort_type: sort, publish_time: days, filter_duration: '0', content_type: '0', search_id: '', backtrace: '' };
  const data = await httpRequest({
    hostname: 'api.tikhub.dev',
    path: '/api/v1/douyin/search/fetch_video_search_v1',
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + TIKHUB_TOKEN, 'Content-Type': 'application/json' }
  }, payload);
  if (!data || data.code !== 200) return [];
  let videos = data.data?.data || [];
  if (hasProduct) videos = videos.filter(v => v.aweme_info?.product_info?.product_id);
  return videos;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 抖音博主搜索（通过 TikHub API）
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
async function douyinSearchUser(keyword) {
  if (!TIKHUB_TOKEN) return [];
  // 通过搜索视频来找对应作者
  const payload = { keyword, cursor: 0, sort_type: '0', publish_time: '0', filter_duration: '0', content_type: '0', search_id: '', backtrace: '' };
  const data = await httpRequest({
    hostname: 'api.tikhub.dev',
    path: '/api/v1/douyin/search/fetch_video_search_v1',
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + TIKHUB_TOKEN, 'Content-Type': 'application/json' }
  }, payload);
  if (!data || data.code !== 200) return [];
  // 按作者名过滤去重
  const seen = new Set();
  const users = [];
  const videos = data.data?.data || [];
  for (const v of videos) {
    const author = v.aweme_info?.author;
    if (!author) continue;
    const nick = author.nickname || '';
    if (nick.toLowerCase().includes(keyword.toLowerCase()) || keyword.toLowerCase().includes(nick.toLowerCase())) {
      if (!seen.has(author.sec_uid)) {
        seen.add(author.sec_uid);
        users.push({
          sec_uid: author.sec_uid,
          nickname: nick,
          follower_count: author.follower_count || 0,
          total_favorited: author.total_favorited || 0,
          video_count: author.aweme_count || 0,
          avatar: author.avatar_url || '',
        });
      }
    }
  }
  return users;
}

async function douyinUserVideos(secUserId, maxCount = 20) {
  if (!TIKHUB_TOKEN) return [];
  const data = await httpRequest({
    hostname: 'api.tikhub.dev',
    path: '/api/v1/douyin/app/v3/fetch_user_post_videos?sec_user_id=' + secUserId + '&count=' + maxCount,
    method: 'GET',
    headers: { 'Authorization': 'Bearer ' + TIKHUB_TOKEN, 'Content-Type': 'application/json' }
  }, null);
  if (!data || data.code !== 200) return [];
  // 用户视频列表在 aweme_list 字段
  return data.data?.aweme_list || [];
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 记忆可视化 Dashboard
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function cmdDashboard(keyword) {
  const mem = getMemory(keyword);
  if (!mem) { console.log('❌ 暂无"' + keyword + '"的记忆，请先 analyze'); return; }

  console.log('\n📊 ' + keyword + ' 赛道路径 Dashboard');
  console.log('='.repeat(50));
  console.log('  学习次数: ' + (mem.count || 1) + '次');
  console.log('  更新于: ' + ((mem.updatedAt || '').substring(0, 10) || '未知'));

  // 数据趋势
  if (mem.stats) {
    const s = mem.stats;
    console.log('\n📈 数据基准:');
    console.log('  均点赞: ' + formatNumber(s.avgLikes || 0));
    console.log('  均评论: ' + formatNumber(s.avgComments || 0));
    console.log('  最佳时长: ' + (mem.bestDuration || '?') + 's');
    if (s.topTags?.length) {
      console.log('  热门标签: ' + s.topTags.slice(0, 6).map(([t, c]) => '#' + t + '(' + c + ')').join(' '));
    }
  }

  // 爆款开头模式
  if (mem.openingPatterns?.length) {
    console.log('\n🔥 爆款开头 TOP5:');
    mem.openingPatterns.slice(0, 5).forEach((p, i) => console.log('  ' + (i+1) + '. ' + p));
  }

  // 内容结构
  if (mem.structures?.length) {
    console.log('\n📐 内容结构:');
    mem.structures.slice(0, 3).forEach((s, i) => console.log('  ' + (i+1) + '. ' + s));
  }

  // 标题模板
  if (mem.titleTemplates?.length) {
    console.log('\n✍️ 高转化标题模板:');
    mem.titleTemplates.slice(0, 5).forEach((t, i) => console.log('  ' + (i+1) + '. ' + t));
  }

  // 用户需求
  if (mem.commentNeeds?.length) {
    console.log('\n💬 用户核心需求:');
    mem.commentNeeds.slice(0, 5).forEach((c, i) => console.log('  ' + (i+1) + '. ' + c));
  }

  // 带货商品
  if (mem.products?.length) {
    console.log('\n🛒 热门带货商品:');
    mem.products.slice(0, 3).forEach((p, i) => {
      console.log('  ' + (i+1) + '. ' + p.title + ' | 💰' + p.price + ' | 📦' + formatNumber(p.sales || 0) + '件');
    });
  }

  // 行动建议
  console.log('\n🎯 AI 行动建议:');
  const insights = mem.insights || [];
  if (insights.length) {
    insights.slice(0, 3).forEach((ins, i) => console.log('  ' + (i+1) + '. ' + ins));
  } else {
    console.log('  建议先 analyze 积累更多数据');
  }
  console.log('');
}



function analyzeVideos(videos, keyword) {
  const top = videos.filter(v => (v.aweme_info?.statistics?.digg_count || 0) > 0)
    .sort((a, b) => (b.aweme_info?.statistics?.digg_count || 0) - (a.aweme_info?.statistics?.digg_count || 0)).slice(0, 20);
  if (!top.length) return null;

  const durations = top.map(v => (v.aweme_info?.video?.duration || 0) / 1000);
  const avgDuration = durations.reduce((a, b) => a + b, 0) / durations.length;
  const tagCounter = {};
  top.forEach(v => { (v.aweme_info?.chaes?.flat() || []).forEach(t => { tagCounter[t] = (tagCounter[t] || 0) + 1; }); });
  const topTags = Object.entries(tagCounter).sort((a, b) => b[1] - a[1]).slice(0, 15);
  const durRanges = { '0-15s': 0, '15-30s': 0, '30-60s': 0, '60s+': 0 };
  durations.forEach(d => { if (d <= 15) durRanges['0-15s']++; else if (d <= 30) durRanges['15-30s']++; else if (d <= 60) durRanges['30-60s']++; else durRanges['60s+']++; });

  const stats = {
    total: videos.length, analyzed: top.length,
    avgLikes: Math.round(top.reduce((s, v) => s + (v.aweme_info?.statistics?.digg_count || 0), 0) / top.length),
    avgComments: Math.round(top.reduce((s, v) => s + (v.aweme_info?.statistics?.comment_count || 0), 0) / top.length),
    avgDuration: Math.round(avgDuration), topTags, durationRanges: durRanges
  };

  const videoList = top.map((v, i) => {
    const a = v.aweme_info || {};
    const s = a.statistics || {};
    const likes = s.digg_count || 0;
    const comments = s.comment_count || 0;
    return {
      rank: i + 1, videoId: a.aweme_id || '', author: a.author?.nickname || '未知',
      title: a.desc || '', duration: Math.round((a.video?.duration || 0) / 1000),
      likes, comments, shares: s.share_count || 0,
      commentRate: likes > 0 ? (comments / likes * 100).toFixed(1) : '0',
      hasProduct: !!a.product_info?.product_id,
      product: a.product_info ? { title: a.product_info.title || '', price: a.product_info.price || 0, sales: a.product_info.sales || 0 } : null,
      tags: (a.chaes?.flat() || []).slice(0, 5),
      url: 'https://www.douyin.com/video/' + (a.aweme_id || '')
    };
  });

  return { stats, videos: videoList };
}

async function cmdAnalyze(keyword, flags) {
  console.log('\n📊 分析 + 学习: "' + keyword + '"');
  console.log('='.repeat(60));

  let videos;
  if (flags.browser) {
    const mode = hasDesktop() ? '有头浏览器（真实窗口）' : '无头浏览器（云服务器）';
    console.log(`  🌐 模式: 浏览器搜索 [${mode}]`);
    videos = await chromeSearch(keyword, { headless: !hasDesktop(), sort: '2' });
  } else {
    clearNetError(); videos = await douyinSearch(keyword, { sort: '2', days: flags.days || '0', hasProduct: flags.hasProduct });
  }
  if (!videos.length) { if (!TIKHUB_TOKEN) { console.log('⚠️ 未配置 TikHub Token，请先设置环境变量 TIKHUB_TOKEN'); } else if (hasNetError()) { console.log('⚠️ 网络异常: ' + _lastNetError); console.log('   请检查网络连接或 API 配置'); } else { console.log('❌ 未找到视频，请尝试其他关键词'); } return; }

  const data = analyzeVideos(videos, keyword);
  if (!data) { console.log('❌ 数据不足'); return; }

  const { stats, videos: vl } = data;

  console.log('\n📈 聚合: ' + stats.analyzed + '个视频 | 均赞' + formatNumber(stats.avgLikes) + ' | 均时' + stats.avgDuration + 's');
  console.log('⏱️ 时长: 0-15s:' + stats.durationRanges['0-15s'] + ' 15-30s:' + stats.durationRanges['15-30s'] + ' 30-60s:' + stats.durationRanges['30-60s'] + ' 60s+:' + stats.durationRanges['60s+']);

  console.log('\n🔥 TOP10:');
  vl.slice(0, 10).forEach(v => {
    const prod = v.hasProduct ? '🛒' : '❌';
    console.log('  ' + v.rank.toString().padStart(2) + '. [' + v.duration + 's] 👍' + formatNumber(v.likes) + ' 💬' + formatNumber(v.comments) + '(' + v.commentRate + '%) ' + prod + ' @' + v.author + ' | ' + v.title.substring(0, 30));
  });

  if (stats.topTags.length) {
    console.log('\n🏷️ ' + stats.topTags.slice(0, 8).map(([t]) => '#' + t).join(' '));
  }

  console.log('\n\n🤖 AI分析爆款逻辑...');

  const prompt = '分析"' + keyword + '"的' + stats.analyzed + '个爆款视频，给出JSON格式结论：\n' +
    vl.slice(0, 8).map(v => v.rank + '. "' + v.title.substring(0, 40) + '" @' + v.author + ' | ' + v.duration + 's | 👍' + formatNumber(v.likes) + ' | 💬' + formatNumber(v.comments) + ' | ' + v.tags.map(t => '#' + t).join(' ')).join('\n') +
    '\n时长分布：' + Object.entries(stats.durationRanges).map(([k, v]) => k + ':' + v + '个').join(' ') +
    '\n均点赞:' + formatNumber(stats.avgLikes) + ' | 均时:' + stats.avgDuration + 's\n\n输出JSON：\n{\n  "openingPatterns": ["开头1","开头2"...],\n  "structures": ["结构1"...],\n  "commentNeeds": ["用户关心1"...],\n  "titleTemplates": ["模板1"...],\n  "insights": ["洞察1"...],\n  "bestDuration": "最佳时长",\n  "tagStrategy": "标签策略"\n}';

  let insights = { openingPatterns: [], structures: [], commentNeeds: [], titleTemplates: [], insights: [], bestDuration: '15-30秒', tagStrategy: '' };
  try {
    const result = await callAI(prompt);
    insights = JSON.parse(result.replace(/```json|```/g, '').trim());
  } catch (e) { console.log('⚠️ AI解析失败，仅保存数据'); }

  const memoryData = { keyword, stats, videos: vl.slice(0, 10), ...insights, topTags: stats.topTags };
  const saved = saveMemory(keyword, memoryData);
  console.log('\n✅ 已学习: "' + keyword + '" (累计' + saved.count + '次)');
}

async function cmdAnalyzeSimple(keyword) {
  console.log('\n📊 快速分析: "' + keyword + '"');
  clearNetError(); const videos = await douyinSearch(keyword, { sort: '2' });
  if (!videos.length) { if (!TIKHUB_TOKEN) { console.log('⚠️ 未配置 TikHub Token，请先设置环境变量 TIKHUB_TOKEN'); } else if (hasNetError()) { console.log('⚠️ 网络异常: ' + _lastNetError); console.log('   请检查网络连接或 API 配置'); } else { console.log('❌ 未找到视频，请尝试其他关键词'); } return; }
  const data = analyzeVideos(videos, keyword);
  if (!data) { console.log('❌ 数据不足'); return; }
  const { stats, videos: vl } = data;
  console.log('\n📈 ' + stats.analyzed + '个 | 均赞' + formatNumber(stats.avgLikes) + ' | 均时' + stats.avgDuration + 's');
  vl.slice(0, 5).forEach(v => console.log('  ' + v.rank + '. [' + v.duration + 's] 👍' + formatNumber(v.likes) + ' | ' + v.title.substring(0, 35)));
  if (stats.topTags.length) console.log('\n🏷️ ' + stats.topTags.slice(0, 6).map(([t]) => '#' + t).join(' '));
  saveMemory(keyword, { keyword, stats, videos: vl.slice(0, 5), topTags: stats.topTags });
  console.log('\n✅ 已记录');
}

async function cmdGenerateTitles(keyword, count) {
  console.log('\n✍️ 生成标题: "' + keyword + '"');
  const mem = getMemory(keyword);
  const recent = mem?.titleTemplates || [];
  const templates = recent.slice(0, 5).map(t => `"${t}"`).join(' | ');
  // 优先用作者记忆，其次用商品记忆
  let insight = '';
  if (mem?.type === 'author' && mem?.analysisText) {
    insight = '\n\n【该账号/赛道口播规律参考】：' + mem.analysisText.substring(0, 1500);
  } else if (mem?.type === 'product' && mem?.analysisText) {
    insight = '\n\n【选品记忆参考】：' + mem.analysisText.substring(0, 800);
  } else if (mem?.analysisText) {
    insight = '\n\n【赛道记忆】：' + mem.analysisText.substring(0, 500);
  }
  const prompt = `为"${keyword}"生成${count}条抖音爆款标题：\n已知模板：${templates || '无'}${insight}\n分3类：1.引流型(悬念/反差) 2.转化型(紧迫感) 3.身份型(代入感)\n每条评分：好奇心|情绪共鸣|平台适配|总分。格式：类型:\n1.[分] 标题`;
  console.log(await callAI(prompt));
}

async function cmdGenerateScript(keyword, type, product, price) {
  const typeMap = { traffic: ['15-30秒', '引流款'], seed: ['30-60秒', '种草型'], sales: ['60秒+', '逼单型'] };
  const [dur, label] = typeMap[type] || ['60秒+', '通用型'];
  const mem = getMemory(keyword);
  // 作者记忆优先调用
  let authorInsight = '';
  if (mem?.type === 'author' && mem?.analysisText) {
    authorInsight = '\n\n【该账号口播风格参考】：' + mem.analysisText.substring(0, 1500);
  } else if (mem?.type === 'product' && mem?.analysisText) {
    authorInsight = '\n\n【选品记忆参考】：' + mem.analysisText.substring(0, 800);
  } else if (mem?.analysisText) {
    authorInsight = '\n\n【赛道记忆】：' + mem.analysisText.substring(0, 500);
  }
  const prompt = '生成' + dur + label + '口播脚本，主题："' + keyword + '"' + (product ? ' | 产品:' + product + (price ? ' | 价格:' + price : '') : '') + '\n学习到的开头：' + (mem?.openingPatterns || []).slice(0, 3).join(' | ') + '\n学习到的结构：' + (mem?.structures || []).slice(0, 2).join(' | ') + authorInsight + '\n避开词：算命|占卜|通灵|化解|驱邪|保佑|神仙|菩萨|太岁|冲煞|属相|命格|八卦|生辰|天机|宿命|轮回\n用词：传统文化|生活智慧|心理暗示|空间能量|生活美学|文化传承|东方智慧';
  console.log(await callAI(prompt));
}

async function cmdProduct(keyword) {
  console.log('\n🛒 选品分析: "' + keyword + '"');
  console.log('📡 搜索视频中...');
  clearNetError(); const videos = await douyinSearch(keyword, { sort: '2' });
  if (!videos.length) { if (!TIKHUB_TOKEN) { console.log('⚠️ 未配置 TikHub Token，请先设置环境变量 TIKHUB_TOKEN'); } else if (hasNetError()) { console.log('⚠️ 网络异常: ' + _lastNetError); console.log('   请检查网络连接或 API 配置'); } else { console.log('❌ 未找到视频，请尝试其他关键词'); } return; }
  console.log('   找到 ' + videos.length + ' 个视频，分析中...\n');

  // 整理视频数据
  const videoList = videos.map(v => ({
    title: v.aweme_info?.desc || v.desc || '',
    likes: v.aweme_info?.statistics?.digg_count || 0,
    comments: v.aweme_info?.statistics?.comment_count || 0,
    author: v.aweme_info?.author?.nickname || '未知',
    duration: Math.round((v.aweme_info?.video?.duration || 0) / 1000),
  }));

  // AI 选品分析
  const topVideos = videoList.sort((a, b) => b.likes - a.likes).slice(0, 10);
  const topData = topVideos.map((v, i) =>
    (i+1) + '. 👍' + formatNumber(v.likes) + ' | ' + v.duration + 's | @' + v.author + ' | ' + v.title.substring(0, 50)
  ).join('\n');

  const prompt = '你是抖音带货选品分析师。分析关键词"' + keyword + '"下的视频，识别带货/种草型视频并给出选品建议。\n\nTOP10视频：\n' + topData + '\n\n请分析：\n1. 哪些视频像带货/种草视频（看标题/口吻/产品词）\n2. 推断带的货是什么类型\n3. 适合该关键词的商品类型、价格区间、带货话术特点\n4. 给出3个具体选品建议（品类+参考价格+切入角度）\n5. 该赛道带货的3个关键成功要素';

  console.log('🤖 AI 选品分析中...');
  const analysis = await callAI(prompt);
  console.log('\n' + (analysis || '分析生成失败'));

  // 保存记忆（含选品分析结果）
  const productMem = {
    keyword,
    type: 'product',
    stats: { videos: videos.length, avgLikes: Math.round(videoList.reduce((s,v) => s+v.likes, 0) / videos.length) },
    analysisText: (analysis || '').substring(0, 3000),
    topTags: topVideos.map(v => v.title.substring(0, 40)),
    insights: [],
  };
  const saved = saveMemory(keyword, productMem);
  console.log('\n📚 选品记忆已保存 (累计' + saved.count + '次)');
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
async function cmdAuthor(authorQuery) {
  console.log('\n🔍 竞品分析: @"' + authorQuery + '"');
  console.log('='.repeat(50));

  // 搜索博主
  console.log('\n📡 搜索博主...');
  clearNetError(); const users = await douyinSearchUser(authorQuery);
  if (!users.length) {
    console.log('❌ 未找到该博主，尝试直接搜索视频...');
    clearNetError(); const searched = await douyinSearch(authorQuery);
    const authorVideos = searched.filter(v => {
      const nick = (v.aweme_info?.author?.nickname || '').toLowerCase();
      return nick.includes(authorQuery.toLowerCase());
    });
    if (!authorVideos.length) { console.log('❌ 找不到相关内容'); return; }
    // 取找到的作者
    const secUid = authorVideos[0].aweme_info?.author?.sec_uid;
    if (!secUid) { console.log('❌ 无法获取博主信息'); return; }
    const rawVideos = await douyinUserVideos(secUid, 20);
    if (!rawVideos.length) { console.log('❌ 无法获取该博主视频'); return; }
    const nickname = authorVideos[0].aweme_info?.author?.nickname || authorQuery;
    console.log('\n📌 @' + nickname);
    console.log('   找到 ' + rawVideos.length + ' 条视频');
    await analyzeAuthorData(rawVideos, authorQuery, nickname);
    return;
  }

  const user = users[0];
  console.log('\n📌 @' + user.nickname + ' | 粉丝 ' + formatNumber(user.follower_count));
  console.log('   视频数: ' + user.video_count + ' | 获赞: ' + formatNumber(user.total_favorited));

  // 获取视频列表
  console.log('\n📡 获取视频列表...');
  const rawVideos = await douyinUserVideos(user.sec_uid, 20);
  if (!rawVideos.length) { console.log('❌ 无法获取该博主视频'); return; }
  console.log('   成功获取 ' + rawVideos.length + ' 条视频');
  await analyzeAuthorData(rawVideos, authorQuery, user.nickname);
}

async function analyzeAuthorData(rawVideos, authorQuery, nickname) {
  // 整理视频数据
  const videos = rawVideos.map(v => v.aweme_id ? v : { aweme_id: v.aweme_id, desc: v.desc, statistics: v.statistics, product_info: v.product_info, author: v.author, video: v.video });

  let totalLikes = 0, totalComments = 0, totalShares = 0, totalCollect = 0;
  let withProduct = 0;
  const productVideos = [];
  const durationRanges = { '0-15s': 0, '15-30s': 0, '30-60s': 0, '60s+': 0 };

  videos.forEach(v => {
    const st = v.statistics || {};
    const dur = (v.video?.duration || 0) / 1000;
    totalLikes += st.digg_count || 0;
    totalComments += st.comment_count || 0;
    totalShares += st.share_count || 0;
    totalCollect += st.collect_count || 0;
    if (v.product_info?.product_id) { withProduct++; productVideos.push(v); }
    if (dur < 15) durationRanges['0-15s']++;
    else if (dur < 30) durationRanges['15-30s']++;
    else if (dur < 60) durationRanges['30-60s']++;
    else durationRanges['60s+']++;
  });

  const avgLikes = videos.length > 0 ? Math.round(totalLikes / videos.length) : 0;
  const avgDuration = videos.length > 0 ? Math.round(videos.reduce((s, v) => s + ((v.video?.duration || 0) / 1000), 0) / videos.length) : 0;
  const avgComments = videos.length > 0 ? Math.round(totalComments / videos.length) : 0;
  const avgShares = videos.length > 0 ? Math.round(totalShares / videos.length) : 0;
  const avgCollect = videos.length > 0 ? Math.round(totalCollect / videos.length) : 0;

  // 计算互动率指标
  const engagementRate = avgLikes > 0 ? ((avgComments + avgShares + avgCollect) / avgLikes * 100).toFixed(1) : '0';

  console.log('\n📊 基础数据:');
  console.log('  视频总数: ' + videos.length);
  console.log('  总点赞: ' + formatNumber(totalLikes) + ' | 均赞: ' + formatNumber(avgLikes));
  console.log('  总评论: ' + formatNumber(totalComments) + ' | 均评论: ' + formatNumber(avgComments));
  console.log('  总分享: ' + formatNumber(totalShares) + ' | 均分享: ' + formatNumber(avgShares));
  console.log('  总收藏: ' + formatNumber(totalCollect) + ' | 均收藏: ' + formatNumber(avgCollect));
  console.log('  均时长: ' + avgDuration + 's');
  console.log('  互动率(评+转+藏/赞): ' + engagementRate + '%');
  console.log('  时长分布: 0-15s:' + durationRanges['0-15s'] + ' | 15-30s:' + durationRanges['15-30s'] + ' | 30-60s:' + durationRanges['30-60s'] + ' | 60s+:' + durationRanges['60s+']);
  console.log('  带货视频: ' + withProduct + ' 条');

  // TOP5
  const top5 = [...videos].sort((a, b) => ((b.statistics?.digg_count) || 0) - ((a.statistics?.digg_count) || 0)).slice(0, 5);
  const bottom5 = [...videos].sort((a, b) => ((a.statistics?.digg_count) || 0) - ((b.statistics?.digg_count) || 0)).slice(0, 5);
  console.log('\n🔥 TOP5 爆款:');
  top5.forEach((v, i) => {
    const st = v.statistics || {};
    const dur = Math.round(((v.video?.duration || 0) / 1000));
    const title = (v.desc || '').substring(0, 50);
    const cmts = st.comment_count || 0;
    const coll = st.collect_count || 0;
    const sr = st.share_count || 0;
    const er = st.digg_count > 0 ? ((cmts + coll + sr) / st.digg_count * 100).toFixed(1) : '0';
    console.log('  ' + (i+1) + '. 👍' + formatNumber(st.digg_count||0) + ' | 📝' + formatNumber(cmts) + ' | 📤' + formatNumber(sr) + ' | ⭐' + formatNumber(coll) + ' | ' + dur + 's | ' + title);
  });

  console.log('\n📉 低赞5条:');
  bottom5.forEach((v, i) => {
    const st = v.statistics || {};
    const dur = Math.round(((v.video?.duration || 0) / 1000));
    const title = (v.desc || '').substring(0, 50);
    console.log('  ' + (i+1) + '. 👍' + formatNumber(st.digg_count||0) + ' | ' + dur + 's | ' + title);
  });

  // 带商品的视频
  if (productVideos.length) {
    console.log('\n🛒 带货视频 (' + productVideos.length + ' 条):');
    productVideos.slice(0, 5).forEach(v => {
      const prod = v.product_info || {};
      const st = v.statistics || {};
      console.log('  · 👍' + formatNumber(st.digg_count||0) + ' | ' + (prod.title||'').substring(0,40) + ' | ¥' + (prod.price||'?'));
    });
  }

  // 提取所有视频标题（用于分析关键词频率）
  const allTitles = videos.map(v => v.desc || '').join('\\n');
  const allHashtags = videos.map(v => {
    const tags = (v.desc || '').match(/#[\\u4e00-\\u9fa5A-Za-z0-9]+/g) || [];
    return tags.join(' ');
  }).join(' ');

  // 转写TOP视频口播内容（独立保护，失败不影响主流程）
  let transcriptionText = '';
  try {
    transcriptionText = await (async () => {
    const topForTranscribe = [...videos].sort((a,b) => ((b.statistics?.digg_count)||0) - ((a.statistics?.digg_count)||0)).slice(0, 3);
    if (topForTranscribe.length === 0) return '';
    const tmpDir = '/tmp/hub_' + Date.now();
    fs.mkdirSync(tmpDir, { recursive: true });
    try {
      console.log('\n🎤 正在转写TOP' + topForTranscribe.length + '条视频口播...');
      const allTrans = [];
      for (let i = 0; i < topForTranscribe.length; i++) {
        const v = topForTranscribe[i];
        const videoUrl = v.video?.play_addr?.url_list?.[0];
        if (!videoUrl) continue;
        const idx = i + 1;
        const mp4Path = tmpDir + '/v' + idx + '.mp4';
        const wavPath = tmpDir + '/v' + idx + '.wav';
        const title = (v.desc || '').substring(0, 40);
        console.log('  [' + idx + '/' + topForTranscribe.length + '] ' + title + '...');
        await new Promise((res, rej) => {
          const dl = exec('curl -s -L -A "Mozilla/5.0" "' + videoUrl + '" -o "' + mp4Path + '" --max-time 60', err => err ? rej(err) : res());
          dl.on('error', rej);
        });
        if (!fs.existsSync(mp4Path) || fs.statSync(mp4Path).size < 10000) { console.log('    下载失败，跳过'); continue; }
        await new Promise((res, rej) => {
          const ex = exec('ffmpeg -i "' + mp4Path + '" -vn -acodec pcm_s16le -ar 48000 -ac 2 -y "' + wavPath + '"', err => err ? rej(err) : res());
          ex.on('error', rej);
        });
        if (!fs.existsSync(wavPath)) { console.log('    音频提取失败，跳过'); continue; }
        const transcribed = await new Promise(res => {
          const wh = exec('whisper "' + wavPath + '" --language Chinese --model small --fp16 False --temperature 0', { encoding: 'utf8', timeout: 300000 }, (err, stdout) => {
            if (err) { res(''); return; }
            const lines = stdout.split('\n').filter(l => l.includes('-->'));
            const texts = lines.map(l => l.replace(/\[\d{2}:\d{2}\.\d{3}\s-->/, '').trim()).filter(t => t.length > 0);
            res(texts.join(' '));
          });
        });
        if (transcribed && transcribed.length > 10) {
          allTrans.push('【视频' + idx + '】' + title + '：' + transcribed.substring(0, 500));
          console.log('    转写完成: ' + transcribed.substring(0, 60) + '...');
        }
        try { fs.unlinkSync(mp4Path); fs.unlinkSync(wavPath); } catch(e) {}
      }
      return allTrans.join('\n\n');
    } finally {
      try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch(e) {}
    }
  })();
  } catch(e) { console.log('⚠️ 口播转写出错（' + e.message.substring(0,50) + '），跳过转写继续分析'); }

  // AI 深度分析

  // AI 深度分析
  console.log('\n🤖 AI 深度分析中...');
  const top5Data = top5.map((v, i) => {
    const st = v.statistics || {};
    const dur = Math.round(((v.video?.duration || 0) / 1000));
    return (i+1) + '. 【' + dur + 's】👍' + formatNumber(st.digg_count||0) + ' 📝' + formatNumber(st.comment_count||0) + ' 📤' + formatNumber(st.share_count||0) + ' ⭐' + formatNumber(st.collect_count||0) + ' | ' + (v.desc||'').substring(0,60);
  }).join('\n');

  const transcriptionSection = transcriptionText ? '\n\n【TOP视频口播原文】\n' + transcriptionText.substring(0, 3000) : '';
  const basePrompt = '你是抖音高级运营分析师。请深度分析博主 @' + nickname + ' 的' + videos.length + '个视频。' + transcriptionSection + '\n\n基础指标：均赞' + formatNumber(avgLikes) + ' | 均评' + formatNumber(avgComments) + ' | 均转' + formatNumber(avgShares) + ' | 均藏' + formatNumber(avgCollect) + ' | 均时' + avgDuration + 's | 互动率' + engagementRate + '% | 带商品' + withProduct + '个\n时长分布：15s内:' + durationRanges['0-15s'] + '个 15-30s:' + durationRanges['15-30s'] + '个 30-60s:' + durationRanges['30-60s'] + '个 60s+:' + durationRanges['60s+'] + '个\n\nTOP5爆款：\n' + top5Data + '\n\n低赞案例：\n' + bottom5.map((v,i) => (i+1) + '. 👍' + formatNumber(v.statistics?.digg_count||0) + ' | ' + (v.desc||'').substring(0,45)).join('\n') + '\n\n核心标签：' + allHashtags.substring(0, 500) + '\n\n请输出深度分析（每条必须有数据支撑）：\n\n## 一、账号定位与竞争壁垒\n- 赛道定位、人群精准度、差异化优势\n\n## 二、爆款因子拆解（重点）\n- TOP1爆款爆的3个核心原因\n- 低赞视频失败的根本原因（结合具体数据）\n\n## 三、口播文案风格分析（重点）\n- 分析口播的语气、节奏、话术套路\n- 典型台词示例摘录\n\n## 四、粉丝互动质量\n- 互动率解读（评/转/藏分别反映什么）\n- 粉丝真实诉求和潜在痛点\n\n## 五、带货与变现\n- 账号变现能力评估、最适合产品类型、距离带货王差什么\n\n## 六、可复制技巧（3条具体可操作）\n- 技巧+具体动作+为什么有效\n\n## 七、紧急改进建议（1-2条）';
  const prompt = basePrompt;

  let analysis = '';
  try { analysis = await callAI(prompt); } catch(e) { console.log('AI调用异常:', e.message); }
  if (!analysis || analysis.trim().length < 50) {
    console.log('⚠️ AI分析生成失败，将输出原始数据分析...');
    analysis = `\n## 基础分析（AI分析服务暂时不可用，仅供参考）\n\n账号基础数据：${videos.length}个视频，平均点赞${formatNumber(avgLikes)}，平均时长${avgDuration}秒。\n互动率${engagementRate}%属于${parseFloat(engagementRate) > 50 ? '优秀水平' : parseFloat(engagementRate) > 20 ? '良好水平' : '一般水平'}，说明${parseFloat(engagementRate) > 50 ? '粉丝活跃度和内容共鸣度很高' : parseFloat(engagementRate) > 20 ? '粉丝互动意愿尚可' : '粉丝互动偏弱，需要加强内容吸引力'}\n\nTOP1爆款分析：${top5[0]?.desc?.substring(0,50) || '无数据'}\n该视频点赞${formatNumber(top5[0]?.statistics?.digg_count||0)}，评论${formatNumber(top5[0]?.statistics?.comment_count||0)}，转发${formatNumber(top5[0]?.statistics?.share_count||0)}，收藏${formatNumber(top5[0]?.statistics?.collect_count||0)}\n`;
    console.log(analysis);
  } else {
    console.log('\n' + analysis);
  }

  const outFile = path.join(MEMORY_DIR, 'author_' + authorQuery + '.json');
  fs.writeFileSync(outFile, JSON.stringify({
    author: authorQuery, nickname,
    stats: { videos: videos.length, avgLikes, avgComments, avgShares, avgCollect, avgDuration, engagementRate, durationRanges, withProduct },
    top5: top5.map(v => ({ title: (v.desc||'').substring(0,80), likes: v.statistics?.digg_count||0, comments: v.statistics?.comment_count||0, shares: v.statistics?.share_count||0, collects: v.statistics?.collect_count||0, duration: Math.round((v.video?.duration||0)/1000) })),
    analysis
  }, null, 2));
  console.log('\n💾 分析已保存: ' + outFile);

  // 写入记忆库，供 titles/script/product 命令调用
  try {
    const authorStats = { videos: videos.length, avgLikes, avgComments, avgShares, avgCollect, avgDuration, engagementRate, durationRanges, withProduct };
    const authorMem = {
      keyword: nickname,
      type: 'author',
      stats: authorStats,
      topTags: allHashtags.substring(0, 300),
      topTitles: top5.map(v => (v.desc||'').substring(0,60)),
      insights: [],
      analysisText: (analysis || '').substring(0, 3000)
    };
    const saved = saveMemory(nickname, authorMem);
    console.log('📚 作者记忆已保存: @' + nickname + ' (累计' + saved.count + '次)');
  } catch(e) { console.log('⚠️ 记忆保存失败:', e.message); }
}

async function cmdMemory(keyword) {
  if (keyword) {
    const mem = getMemory(keyword);
    if (!mem) { console.log('❌ 暂无"' + keyword + '"的记忆'); return; }
    console.log('\n📚 "' + keyword + '" (学习' + mem.count + '次)');
    console.log('='.repeat(50));
    console.log('⏱️ 最佳时长: ' + (mem.bestDuration || '未知'));
    if (mem.openingPatterns?.length) console.log('\n🔥 开头: ' + mem.openingPatterns.slice(0, 5).join(' | '));
    if (mem.structures?.length) console.log('\n📐 结构: ' + mem.structures.slice(0, 3).join(' | '));
    if (mem.titleTemplates?.length) console.log('\n✍️ 模板: ' + mem.titleTemplates.slice(0, 5).join(' | '));
    if (mem.topTags?.length) console.log('\n🏷️ ' + mem.topTags.slice(0, 8).map(([t]) => '#' + t).join(' '));
    if (mem.insights?.length) console.log('\n💡 ' + mem.insights.join(' | '));
  } else {
    const all = listMemory();
    if (!all.length) { console.log('❌ 暂无记忆'); return; }
    console.log('\n📚 记忆库:');
    all.forEach(m => console.log('  ' + m.keyword + ' (' + m.count + '次) | ' + (m.updatedAt || '').substring(0, 10)));
  }
}

const config = loadConfig();
const TIKHUB_TOKEN = config.TIKHUB_TOKEN || '';
const DEEPSEEK_KEY = config.DEEPSEEK_KEY || '';

const args = process.argv.slice(2);
const rawCmd = args[0] || '';
const parsed = parseArgs(args.slice(1));
const pos = parsed.positional;

// 自然语言路由：把 "用浏览器分析风水" 转为 { cmd, keyword, flags }
const knownCmds = ['config','analyze','a','titles','script','product','author','memory','dashboard','full','help'];
let finalCmd = rawCmd;
let finalKw = pos[0] || '';
let finalFlags = { ...parsed.flags };

// 如果第一个参数不是已知命令，尝试自然语言解析
if (rawCmd && !knownCmds.includes(rawCmd) && rawCmd.length > 3) {
  const nl = parseNaturalLanguage(rawCmd + (pos[0] ? ' ' + pos[0] : ''));
  if (nl && nl.cmd && nl.cmd !== 'help') {
    console.log(`\n🌐 自然语言理解: "${nl.raw}" → 命令[${nl.cmd}] 关键词[${nl.keyword || '无'}] 模式[${nl.flags.browser ? '浏览器' : 'API'}]`);
    finalCmd = nl.cmd;
    finalKw = nl.keyword || pos[0] || '';
    finalFlags = { ...nl.flags, ...parsed.flags };
  }
}

const cmd = finalCmd;
const keyword = finalKw;
const flags = finalFlags;

console.log('\n🎯 社交营销中心 v8.1 | TikHub:' + (TIKHUB_TOKEN ? '✅' : '❌') + ' | DeepSeek:' + (DEEPSEEK_KEY ? '✅' : '❌'));
console.log('='.repeat(50));

(async () => {
if (cmd === 'config' && pos[0]) { saveConfig(pos[0], pos[1]); console.log('✅ 配置已保存'); }
else if (cmd === 'analyze') { await cmdAnalyze(keyword || '风水', flags); }
else if (cmd === 'a') { await cmdAnalyzeSimple(keyword || '风水'); }
else if (cmd === 'titles') { await cmdGenerateTitles(keyword || '风水', parseInt(flags.n || '10')); }
else if (cmd === 'script') { await cmdGenerateScript(keyword || '风水', pos[1] || 'sales', pos[2], pos[3]); }
else if (cmd === 'product') { await cmdProduct(keyword || '风水'); }
else if (cmd === 'author') { await cmdAuthor(keyword || '博主名', keyword || ''); }
else if (cmd === 'memory') { await cmdMemory(keyword || ''); }
else if (cmd === 'dashboard') { cmdDashboard(keyword || ''); }

else if (cmd === 'full') {
  const kw = keyword || '风水';
  await cmdAnalyze(kw, {});
  await cmdGenerateTitles(kw, 10);
  await cmdGenerateScript(kw, 'sales', pos[1], pos[2]);
}
else {
  console.log('\n📋 社交营销中心 v8.1 | 抖音版\n');
  console.log('📊 抖音分析:');
  console.log('  analyze <词>   深度分析+学习规律 [--browser] [--days=7] [--has-product]');
  console.log('  a <词>        快速分析\n');
  console.log('✍️  生成:');
  console.log('  titles <词>   生成爆款标题 [-n=10]');
  console.log('  script <词> <sales|seed|traffic> [产品] [价格]\n');
  console.log('🛒 选品:');
  console.log('  product <词>  选品分析+带货机会识别\n');
  console.log('🔍 竞品账号:');
  console.log('  author <博主名>  竞品账号深度分析\n');
  console.log('📚 记忆库:');
  console.log('  memory        查看所有记忆');
  console.log('  memory <词>  查看赛道记忆');
  console.log('  dashboard <词> 可视化分析面板\n');
  console.log('🚀 一键全套:');
  console.log('  full <词> [产品] [价格]\n');
  console.log('💡 参数: --browser --days=7 --has-product -n=10');
}
})().catch(e => { console.error(e.message || e); process.exit(1); });
