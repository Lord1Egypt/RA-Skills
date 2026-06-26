// fetch_topics.js — 知识星球帖子抓取
//
// 子命令:
//   node fetch_topics.js topics <group_id> [count] [scope]    获取帖子（scope: all|digests，默认 all）
//   node fetch_topics.js digests <group_id> [count]           获取精华帖（等价于 topics <id> [count] digests）
//   node fetch_topics.js topic <group_id> <topic_id_or_url>   获取指定帖子详情（支持 ID 或完整链接）
//   node fetch_topics.js groups                               列出已加入的星球
//
// 环境变量:
//   ZSXQ_TOKEN (可选) — 知识星球 zsxq_access_token cookie 值
//   如未设置，自动从 {baseDir}/token.json 读取持久化 token
//
// 输出：JSON 到 stdout，日志到 stderr

const https = require('https');
const { URL } = require('url');
const fs = require('fs');
const path = require('path');

// ── 认证 ────────────────────────────────────────────────────
// Token 持久化配置
const TOKEN_FILE = path.join(__dirname, 'token.json');
const DEFAULT_TOKEN = '9D2CC578-94F2-4F89-96FE-86FD85745325_3E93F3D4F8C2DD6B';

function loadToken() {
  // 优先级：环境变量 > 持久化文件 > 默认 token
  if (process.env.ZSXQ_TOKEN) {
    return process.env.ZSXQ_TOKEN;
  }
  
  // 尝试从文件读取
  try {
    if (fs.existsSync(TOKEN_FILE)) {
      const data = JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf-8'));
      if (data.token && data.token.trim()) {
        console.error('[zsxq] loaded token from token.json');
        return data.token;
      }
    }
  } catch (err) {
    console.error(`[zsxq] failed to load token file: ${err.message}`);
  }
  
  // 使用默认 token
  console.error('[zsxq] using default persisted token');
  return DEFAULT_TOKEN;
}

function saveToken(token) {
  try {
    fs.writeFileSync(TOKEN_FILE, JSON.stringify({ token, updated_at: new Date().toISOString() }, null, 2), 'utf-8');
    console.error('[zsxq] token saved to token.json');
  } catch (err) {
    console.error(`[zsxq] failed to save token: ${err.message}`);
  }
}

const ZSXQ_TOKEN = loadToken();
if (!ZSXQ_TOKEN) {
  console.error(JSON.stringify({ error: 'ZSXQ_TOKEN not configured' }));
  process.exit(1);
}

const BASE_URL = 'https://api.zsxq.com/v2';

const HEADERS = {
  'Cookie': `zsxq_access_token=${ZSXQ_TOKEN}`,
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Origin': 'https://wx.zsxq.com',
  'Referer': 'https://wx.zsxq.com/',
  'Accept': 'application/json',
  'X-Timestamp': String(Math.floor(Date.now() / 1000)),
};

const subcommand = process.argv[2] || 'topics';

// ── HTTP 请求 ───────────────────────────────────────────────
function httpGet(url, options = {}) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const reqOptions = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method: 'GET',
      headers: { ...HEADERS, ...(options.headers || {}) },
      timeout: options.timeout || 15000,
    };

    const req = https.request(reqOptions, (res) => {
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        const body = Buffer.concat(chunks);
        resolve({ statusCode: res.statusCode, headers: res.headers, body: body.toString('utf-8') });
      });
    });

    req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
    req.on('error', reject);
    req.end();
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// 指数退避重试
async function httpGetWithRetry(url, options = {}, maxRetries = 3) {
  let lastErr;
  for (let i = 0; i < maxRetries; i++) {
    try {
      const res = await httpGet(url, options);
      if (res.statusCode === 429) {
        const wait = Math.pow(2, i + 1) * 1000; // 2s, 4s, 8s
        console.error(`[zsxq] 429 rate limited, waiting ${wait}ms...`);
        await sleep(wait);
        continue;
      }
      return res;
    } catch (err) {
      lastErr = err;
      if (i < maxRetries - 1) {
        const wait = Math.pow(2, i + 1) * 1000;
        console.error(`[zsxq] request error: ${err.message}, retrying in ${wait}ms...`);
        await sleep(wait);
      }
    }
  }
  throw lastErr || new Error('max retries exceeded');
}

// ── 帖子内容解析 ────────────────────────────────────────────
function parseTopicContent(topic, textLimit = 5000) {
  const talk = topic.talk || {};
  const question = topic.question || {};
  const answer = topic.answer || {};

  // 提取文本（talk 类型 / question+answer 类型）
  let text = '';
  if (talk.text) {
    text = talk.text;
  } else if (question.text) {
    text = '【提问】' + question.text;
    if (answer.text) {
      text += '\n【回答】' + answer.text;
    }
  }

  // 图片
  const allImages = [];
  if (talk.images && talk.images.length > 0) {
    for (const img of talk.images) {
      allImages.push({ image_id: img.image_id, type: img.type });
    }
  }

  // owner 在 talk.owner / question.owner 里
  const ownerObj = talk.owner || question.owner || topic.owner || null;

  return {
    topic_id: String(topic.topic_id),
    type: topic.type,
    title: topic.title || '',
    text: text.substring(0, textLimit),
    create_time: topic.create_time,
    owner: ownerObj ? { user_id: String(ownerObj.user_id), name: ownerObj.name } : null,
    likes_count: topic.likes_count || 0,
    comments_count: topic.comments_count || 0,
    reading_count: topic.reading_count || 0,
    readers_count: topic.readers_count || 0,
    digested: topic.digested || false,
    image_count: allImages.length,
  };
}

// ── topics / digests ────────────────────────────────────────
async function fetchTopics() {
  const groupId = process.argv[3];
  const count = parseInt(process.argv[4]) || 20;
  const scope = process.argv[5] || 'all'; // all | digests

  if (!groupId) {
    console.error(JSON.stringify({ error: 'Usage: node fetch_topics.js topics <group_id> [count] [scope]' }));
    process.exit(1);
  }

  const isDigests = scope === 'digests' || subcommand === 'digests';
  const endpoint = isDigests
    ? `${BASE_URL}/groups/${groupId}/topics?scope=digests&count=${Math.min(count, 30)}`
    : `${BASE_URL}/groups/${groupId}/topics?scope=all&count=${Math.min(count, 30)}`;

  console.error(`[zsxq] fetching ${isDigests ? 'digests' : 'all'} topics for group ${groupId} (count=${count})...`);

  const allTopics = [];
  let url = endpoint;
  let pages = 0;
  const maxPages = Math.ceil(count / 20) + 1;

  while (allTopics.length < count && pages < maxPages) {
    try {
      const res = await httpGetWithRetry(url);

      if (res.statusCode === 401) {
        console.log(JSON.stringify({ 
          error: 'unauthorized', 
          hint: 'Token 已过期，请更换新 token',
          action: '请提供新的知识星球 token，我将自动更新保存'
        }));
        return;
      }
      
      if (res.statusCode !== 200) {
        console.error(`[zsxq] HTTP ${res.statusCode}: ${res.body.substring(0, 300)}`);
        break;
      }

      let data;
      try { data = JSON.parse(res.body); } catch {
        console.error(`[zsxq] non-JSON response: ${res.body.substring(0, 300)}`);
        break;
      }

      if (!data.succeeded) {
        console.error(`[zsxq] API error: ${JSON.stringify(data)}`);
        break;
      }

      const topics = data.resp_data && data.resp_data.topics;
      if (!topics || topics.length === 0) {
        console.error('[zsxq] no more topics');
        break;
      }

      for (const t of topics) {
        allTopics.push(parseTopicContent(t));
        if (allTopics.length >= count) break;
      }

      console.error(`[zsxq] fetched ${allTopics.length}/${count} topics`);

      // 翻页：使用 end_time 参数
      const lastTopic = topics[topics.length - 1];
      if (lastTopic && lastTopic.create_time && allTopics.length < count) {
        const endTime = encodeURIComponent(lastTopic.create_time);
        url = endpoint + `&end_time=${endTime}`;
        pages++;
        await sleep(1000); // 翻页限速
      } else {
        break;
      }
    } catch (err) {
      console.error(`[zsxq] fetch error: ${err.message}`);
      break;
    }
  }

  const result = {
    group_id: groupId,
    scope: isDigests ? 'digests' : 'all',
    count: allTopics.length,
    topics: allTopics,
  };

  console.log(JSON.stringify(result, null, 2));
}

// ── topic（单条帖子详情）────────────────────────────────────
async function fetchTopic() {
  const groupId = process.argv[3];
  const input = process.argv[4];

  if (!groupId || !input) {
    console.error(JSON.stringify({ error: 'Usage: node fetch_topics.js topic <group_id> <topic_id_or_url>' }));
    process.exit(1);
  }

  // 支持完整链接 https://wx.zsxq.com/topic/{topic_id} 或纯 ID
  let topicId = input;
  const urlMatch = input.match(/wx\.zsxq\.com\/(?:[^/]+\/)*topic\/(\d+)|wx\.zsxq\.com\/topic\/(\d+)/);
  if (urlMatch) {
    topicId = urlMatch[1] || urlMatch[2];
  }

  console.error(`[zsxq] searching topic ${topicId} in group ${groupId}...`);

  // 知识星球无单帖直接查询接口，通过翻页帖子列表逐页匹配 topic_id
  const pageSize = 30;
  const maxPages = 10; // 最多翻 10 页（300 条）
  let url = `${BASE_URL}/groups/${groupId}/topics?scope=all&count=${pageSize}`;
  let pages = 0;

  try {
    while (pages < maxPages) {
      const res = await httpGetWithRetry(url);

      if (res.statusCode === 401) {
        console.log(JSON.stringify({ 
          error: 'unauthorized', 
          hint: 'Token 已过期，请更换新 token',
          action: '请提供新的知识星球 token，我将自动更新保存'
        }));
        return;
      }
      if (res.statusCode === 403) {
        console.log(JSON.stringify({ error: 'forbidden', hint: '无权限访问该星球，请确认已加入' }));
        return;
      }
      if (res.statusCode !== 200) {
        console.log(JSON.stringify({ error: `HTTP ${res.statusCode}`, detail: res.body.substring(0, 300) }));
        return;
      }

      let data;
      try { data = JSON.parse(res.body); } catch {
        console.log(JSON.stringify({ error: 'non_json_response' }));
        return;
      }

      if (!data.succeeded) {
        console.log(JSON.stringify({ error: 'api_error', resp: data }));
        return;
      }

      const topics = data.resp_data && data.resp_data.topics;
      if (!topics || topics.length === 0) {
        console.error('[zsxq] no more topics to search');
        break;
      }

      // 在本页中查找目标帖子
      const found = topics.find(t => String(t.topic_id) === String(topicId));
      if (found) {
        const result = parseTopicContent(found, 5000);
        result.url = `https://wx.zsxq.com/topic/${topicId}`;
        console.error(`[zsxq] found topic ${topicId} on page ${pages + 1}`);
        console.log(JSON.stringify(result, null, 2));
        return;
      }

      console.error(`[zsxq] page ${pages + 1}: not found yet, continuing...`);

      // 翻页
      const lastTopic = topics[topics.length - 1];
      if (lastTopic && lastTopic.create_time) {
        const endTime = encodeURIComponent(lastTopic.create_time);
        url = `${BASE_URL}/groups/${groupId}/topics?scope=all&count=${pageSize}&end_time=${endTime}`;
        pages++;
        await sleep(1000);
      } else {
        break;
      }
    }

    console.log(JSON.stringify({
      error: 'topic_not_found',
      topic_id: topicId,
      group_id: groupId,
      pages_searched: pages + 1,
      hint: '帖子未在最近 ' + (pages + 1) * pageSize + ' 条中找到，可能已超出翻页范围或不属于该星球',
    }));
  } catch (err) {
    console.log(JSON.stringify({ error: err.message, topic_id: topicId }));
  }
}

// ── groups ───────────────────────────────────────────────────
async function fetchGroups() {
  console.error('[zsxq] fetching joined groups...');

  try {
    const res = await httpGetWithRetry(`${BASE_URL}/groups`);

    if (res.statusCode === 401) {
      console.log(JSON.stringify({ 
        error: 'unauthorized', 
        hint: 'Token 已过期，请更换新 token',
        action: '请提供新的知识星球 token，我将自动更新保存'
      }));
      return;
    }

    if (res.statusCode !== 200) {
      console.log(JSON.stringify({ error: `HTTP ${res.statusCode}`, detail: res.body.substring(0, 300) }));
      return;
    }

    let data;
    try { data = JSON.parse(res.body); } catch {
      console.log(JSON.stringify({ error: 'non_json_response' }));
      return;
    }

    if (!data.succeeded) {
      console.log(JSON.stringify({ error: 'api_error', resp: data }));
      return;
    }

    const groups = (data.resp_data && data.resp_data.groups) || [];
    const result = groups.map(g => ({
      group_id: String(g.group_id),
      name: g.name,
      description: (g.description || '').substring(0, 200),
      member_count: g.member_count || 0,
      topics_count: g.topics_count || 0,
      owner: g.owner ? { user_id: String(g.owner.user_id), name: g.owner.name } : null,
    }));

    console.error(`[zsxq] found ${result.length} groups`);
    console.log(JSON.stringify({ groups: result }, null, 2));
  } catch (err) {
    console.log(JSON.stringify({ error: err.message }));
  }
}

// ── main ─────────────────────────────────────────────────────
(async () => {
  try {
    switch (subcommand) {
      case 'topics':
        await fetchTopics();
        break;
      case 'digests':
        // digests 是 topics 的快捷方式，scope 固定为 digests
        await fetchTopics();
        break;
      case 'topic':
        await fetchTopic();
        break;
      case 'groups':
        await fetchGroups();
        break;
      default:
        console.error(`Unknown subcommand: ${subcommand}. Use: topics, digests, topic, groups`);
        process.exit(1);
    }
  } catch (err) {
    console.error(`[zsxq] fatal error: ${err.message}`);
    process.exit(1);
  }
})();
