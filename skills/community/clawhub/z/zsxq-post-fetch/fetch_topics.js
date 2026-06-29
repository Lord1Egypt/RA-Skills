// fetch_topics.js — 知识星球帖子抓取
//
// 子命令:
//   node fetch_topics.js topics <group_id> [count] [scope]            获取帖子（scope: all|digests，默认 all）
//   node fetch_topics.js digests <group_id> [count]                   获取精华帖
//   node fetch_topics.js topic <group_id> <topic_id_or_url>             获取指定帖子详情
//   node fetch_topics.js topics-by-date <group_id> <start> [end] [count] 按日期范围抓取帖子
//   node fetch_topics.js search <group_id> <keyword> [count]             按关键词搜索帖子
//   node fetch_topics.js groups                                         列出已加入的星球
//
// 环境变量:
//   ZSXQ_BACKEND=cli|http — 默认 cli；http 为 legacy 私有 API fallback
//   ZSXQ_TOKEN — 仅 legacy HTTP fallback 需要的 zsxq_access_token cookie 值
//
// 输出：JSON 到 stdout，日志到 stderr

const { execFile } = require('child_process');
const https = require('https');
const zlib = require('zlib');
const { URL } = require('url');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://api.zsxq.com/v2';
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const RETRY_BASE_MS = 1000;
const RETRY_JITTER_RATIO = 0.25;
const RETRY_MAX_DELAY_MS = 30000;

// ── 纯函数 helpers ───────────────────────────────────────────
function resolveToken(env = process.env) {
  return (env.ZSXQ_TOKEN || '').trim();
}

function resolveBackend(config = {}, env = process.env) {
  const envBackend = String(env.ZSXQ_BACKEND || '').trim().toLowerCase();
  if (envBackend) return envBackend === 'http' ? 'http' : 'cli';

  const configBackend = String(config.backend || '').trim().toLowerCase();
  return configBackend === 'http' ? 'http' : 'cli';
}

function parseTopicId(input) {
  const value = String(input || '').trim();
  const urlMatch = value.match(/(?:topic|topic_detail)\/(\d+)/);
  return urlMatch ? urlMatch[1] : value;
}

function classifyTopicDate(createTime, startDate, endDate) {
  const topicTime = new Date(createTime).getTime();
  const startTs = new Date(startDate + 'T00:00:00+08:00').getTime();
  const endTs = new Date(endDate + 'T23:59:59+08:00').getTime();

  if (topicTime < startTs) return 'before-range';
  if (topicTime > endTs) return 'after-range';
  return 'in-range';
}

function getTopicAttachmentDir(outputDir, groupId, topicDate) {
  return path.join(outputDir, String(groupId), String(topicDate));
}

function sanitizeAttachmentFilename(name, fallback) {
  const value = String(name || fallback || '').trim();
  const filename = value
    .replace(/[\u0000-\u001f\u007f]/g, '_')
    .replace(/[\\/<>:"|?*]/g, '_')
    .replace(/\s+/g, '_');
  return filename || String(fallback || 'attachment');
}

function getAttachmentFilename(topicId, name) {
  const safeTopicId = sanitizeAttachmentFilename(String(topicId || 'topic'), 'topic');
  const safeName = sanitizeAttachmentFilename(name, 'attachment');
  return `${safeTopicId}_${safeName}`;
}

function createBrowserHeaders() {
  return {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Origin': 'https://wx.zsxq.com',
    'Referer': 'https://wx.zsxq.com/',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
  };
}

function createAuthHeaders(token = ZSXQ_TOKEN) {
  const headers = {
    ...createBrowserHeaders(),
    'X-Timestamp': String(Math.floor(Date.now() / 1000)),
    'X-Request-Id': `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`,
    'X-Version': '2.32.0',
  };
  if (token) headers.Cookie = `zsxq_access_token=${token}`;
  return headers;
}

function resolveAttachmentDir(config = {}, env = process.env) {
  return (env.ZSXQ_ATTACHMENT_DIR || env.ATTACHMENT_DIR || config.attachment_dir || '').trim();
}

function parseCliArgs(argv = process.argv) {
  const raw = argv.slice(2);
  const subcommand = raw[0] || 'topics';
  const args = [];
  let markdown = false;
  let downloadAttachments = false;

  for (const arg of raw.slice(1)) {
    if (arg === '--markdown') {
      markdown = true;
    } else if (arg === '--download-attachments') {
      downloadAttachments = true;
    } else {
      args.push(arg);
    }
  }

  return { subcommand, args, markdown, downloadAttachments };
}

function buildCliGroupsArgs(options = {}) {
  const limit = clampNumber(parseInt(options.limit, 10) || 200, 1, 200);
  const scope = String(options.scope || 'all');
  return ['group', '+list', '--json', '--limit', String(limit), '--scope', scope];
}

function buildCliTopicsArgs(groupId, options = {}) {
  const limit = clampNumber(parseInt(options.limit, 10) || 30, 1, 30);
  const args = ['group', '+topics', '--group-id', String(groupId), '--limit', String(limit)];
  if (options.endTime) args.push('--end-time', String(options.endTime));
  args.push('--json');
  return args;
}

function buildCliTopicDetailArgs(topicId) {
  return ['topic', '+detail', '--topic-id', String(topicId), '--json'];
}

function buildCliSearchTopicsArgs(groupId, query) {
  return [
    'api',
    'call',
    'search_topics',
    '--params',
    JSON.stringify({ group_id: String(groupId), query: String(query) }),
    '--format',
    'json',
  ];
}

function shouldDownloadAttachments(config = {}, cli = {}) {
  return Boolean(cli.downloadAttachments || config.download_attachments);
}

function defaultZsxqCliRunner(command, args, options = {}) {
  return new Promise((resolve, reject) => {
    execFile(command, args, {
      timeout: options.timeout || 60000,
      maxBuffer: options.maxBuffer || 10 * 1024 * 1024,
    }, (error, stdout, stderr) => {
      if (error && error.code === 'ENOENT') {
        reject(error);
        return;
      }

      resolve({
        code: error ? (typeof error.code === 'number' ? error.code : 1) : 0,
        stdout: String(stdout || ''),
        stderr: String(stderr || error?.message || ''),
      });
    });
  });
}

function looksLikeAuthError(message) {
  return /login|logged in|auth|unauthorized|forbidden|401|403|认证|登录|未授权|未登录/i.test(message);
}

async function runZsxqCliJson(args, runner = defaultZsxqCliRunner, options = {}) {
  const command = options.command || process.env.ZSXQ_CLI || 'zsxq-cli';

  let result;
  try {
    result = await runner(command, args, options);
  } catch (err) {
    if (err && err.code === 'ENOENT') {
      return {
        ok: false,
        error: 'zsxq_cli_missing',
        hint: '未找到官方 zsxq-cli，请先运行：npm install -g zsxq-cli，然后运行：zsxq-cli auth login',
      };
    }
    return {
      ok: false,
      error: 'zsxq_cli_failed',
      detail: String(err?.message || err || '').slice(0, 500),
      hint: '请确认 zsxq-cli 可执行且已完成：zsxq-cli auth login',
    };
  }

  const code = result.code ?? result.status ?? 0;
  const stdout = String(result.stdout || '').trim();
  const stderr = String(result.stderr || '').trim();
  const detail = (stderr || stdout).slice(0, 500);

  if (code !== 0) {
    if (looksLikeAuthError(stderr || stdout)) {
      return {
        ok: false,
        error: 'zsxq_cli_not_authenticated',
        hint: '请先运行：zsxq-cli auth login；可用 zsxq-cli auth status 检查登录状态',
        detail,
      };
    }
    return {
      ok: false,
      error: 'zsxq_cli_failed',
      exit_code: code,
      detail,
      hint: '请运行 zsxq-cli auth status 检查官方 CLI 状态',
    };
  }

  if (!stdout) {
    return {
      ok: false,
      error: 'zsxq_cli_non_json',
      detail: 'empty stdout',
      hint: '官方 zsxq-cli 未输出 JSON，请确认命令支持 --json 并已登录',
    };
  }

  try {
    return { ok: true, data: JSON.parse(stdout), stderr };
  } catch {
    return {
      ok: false,
      error: 'zsxq_cli_non_json',
      detail: stdout.slice(0, 500),
      hint: '官方 zsxq-cli 返回了非 JSON 输出，请确认命令支持 --json 并已登录',
    };
  }
}

function hasOwn(obj, key) {
  return Object.prototype.hasOwnProperty.call(obj || {}, key);
}

function firstDefined(...values) {
  for (const value of values) {
    if (value !== undefined && value !== null && value !== '') return value;
  }
  return undefined;
}

function asNumber(value, fallback = 0) {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function normalizeCliOwner(owner) {
  if (!owner || typeof owner !== 'object') return null;
  const userId = firstDefined(owner.user_id, owner.userId, owner.id, owner.uid);
  const name = firstDefined(owner.name, owner.nickname, owner.display_name, owner.displayName, owner.nick);
  if (userId === undefined && name === undefined) return null;
  return {
    user_id: userId === undefined ? '' : String(userId),
    name: name === undefined ? '' : String(name),
  };
}

function normalizeCliImage(img = {}) {
  const url = firstDefined(
    img.large?.url,
    img.original?.url,
    img.thumbnail?.url,
    img.url,
    img.src,
    img.download_url,
    img.downloadUrl,
  );
  return {
    image_id: firstDefined(img.image_id, img.imageId, img.id) || '',
    type: firstDefined(img.type, img.ext, img.extension) || 'jpg',
    large: img.large || (url ? { url } : null),
    thumbnail: img.thumbnail || null,
    original: img.original || (url ? { url } : null),
  };
}

function normalizeCliFile(file = {}) {
  return {
    file_id: firstDefined(file.file_id, file.fileId, file.id) || '',
    name: firstDefined(file.name, file.filename, file.file_name, file.fileName, file.title) || '',
    size: asNumber(firstDefined(file.size, file.file_size, file.fileSize), 0),
    url: firstDefined(file.url, file.link, file.download_url, file.downloadUrl) || null,
    download_url: firstDefined(file.download_url, file.downloadUrl) || null,
  };
}

function getSearchableTopicText(topic = {}) {
  const parts = [
    topic.title,
    topic.text,
    topic.owner?.name,
    ...(Array.isArray(topic.files) ? topic.files.map((file) => file.name || file.filename || file.title) : []),
  ];
  return parts.filter(Boolean).join('\n').toLowerCase();
}

function topicMatchesQuery(topic = {}, query = '') {
  const keywords = String(query || '')
    .trim()
    .toLowerCase()
    .split(/\s+/)
    .filter(Boolean);
  if (keywords.length === 0) return false;
  const haystack = getSearchableTopicText(topic);
  return keywords.every((keyword) => haystack.includes(keyword));
}

function filterTopicsByQuery(topics = [], query = '') {
  return topics.filter((topic) => topicMatchesQuery(topic, query));
}

function normalizeSearchResult(raw = {}) {
  const topic = raw.topic && typeof raw.topic === 'object' ? raw.topic : raw;
  return {
    topic_id: String(firstDefined(topic.topic_id, topic.topicId, topic.id) || ''),
    raw,
  };
}

function topicHasDigestMarker(topic = {}) {
  const value = topic.topic && typeof topic.topic === 'object' ? topic.topic : topic;
  return hasOwn(value, 'digested') || hasOwn(value, 'is_digested') || hasOwn(value, 'digest') || hasOwn(value, 'isDigest');
}

function normalizeCliTopic(rawTopic = {}, textLimit = 20000) {
  const topic = rawTopic.topic && typeof rawTopic.topic === 'object' ? rawTopic.topic : rawTopic;
  const talk = topic.talk || {};
  const question = topic.question || {};
  const answer = topic.answer || {};

  let text = firstDefined(talk.text, talk.content, topic.text, topic.content, topic.body, topic.summary) || '';
  if (!text && firstDefined(question.text, question.content)) {
    text = '【提问】' + firstDefined(question.text, question.content);
    if (firstDefined(answer.text, answer.content)) {
      text += '\n【回答】' + firstDefined(answer.text, answer.content);
    }
  }

  const images = [
    ...(Array.isArray(talk.images) ? talk.images : []),
    ...(Array.isArray(topic.images) ? topic.images : []),
  ].map(normalizeCliImage);
  const files = [
    ...(Array.isArray(talk.files) ? talk.files : []),
    ...(Array.isArray(topic.files) ? topic.files : []),
  ].map(normalizeCliFile);
  const ownerObj = talk.owner || talk.author || question.owner || topic.owner || topic.author || topic.user || null;
  const digestValue = firstDefined(topic.digested, topic.is_digested, topic.digest, topic.isDigest);

  return {
    topic_id: String(firstDefined(topic.topic_id, topic.topicId, topic.id) || ''),
    type: firstDefined(topic.type, topic.topic_type, topic.topicType) || '',
    title: firstDefined(topic.title, talk.title) || '',
    text: String(text).substring(0, textLimit),
    create_time: firstDefined(topic.create_time, topic.createTime, topic.created_at, topic.createdAt, topic.time) || '',
    owner: normalizeCliOwner(ownerObj),
    likes_count: asNumber(firstDefined(topic.likes_count, topic.likesCount, topic.likes, topic.stats?.likes, topic.statistics?.likes), 0),
    comments_count: asNumber(firstDefined(topic.comments_count, topic.commentsCount, topic.comments, topic.stats?.comments, topic.statistics?.comments), 0),
    reading_count: asNumber(firstDefined(topic.reading_count, topic.readingCount, topic.read_count, topic.readCount, topic.reads, topic.stats?.reads, topic.statistics?.reads), 0),
    readers_count: asNumber(firstDefined(topic.readers_count, topic.readersCount, topic.readers, topic.stats?.readers, topic.statistics?.readers), 0),
    digested: Boolean(digestValue),
    image_count: images.length,
    file_count: files.length,
    images,
    files,
  };
}

function normalizeCliGroup(rawGroup = {}) {
  const group = rawGroup.group && typeof rawGroup.group === 'object' ? rawGroup.group : rawGroup;
  return {
    group_id: String(firstDefined(group.group_id, group.groupId, group.id) || ''),
    name: firstDefined(group.name, group.title) || '',
    description: String(firstDefined(group.description, group.intro, group.summary) || '').substring(0, 200),
    member_count: asNumber(firstDefined(group.member_count, group.memberCount, group.members_count, group.stats?.members), 0),
    topics_count: asNumber(firstDefined(group.topics_count, group.topicsCount, group.topic_count, group.stats?.topics), 0),
    owner: normalizeCliOwner(group.owner || group.author),
  };
}

function unwrapCliPayload(data = {}) {
  if (data && typeof data === 'object') {
    if (data.resp_data && typeof data.resp_data === 'object') return data.resp_data;
    if (data.data && typeof data.data === 'object') return data.data;
    if (data.result && typeof data.result === 'object') return data.result;
  }
  return data;
}

function extractCliArray(data, keys) {
  const payload = unwrapCliPayload(data);
  const candidates = [payload, data];
  for (const item of candidates) {
    if (Array.isArray(item)) return item;
    if (!item || typeof item !== 'object') continue;
    for (const key of keys) {
      if (Array.isArray(item[key])) return item[key];
    }
    if (Array.isArray(item.items)) return item.items;
    if (Array.isArray(item.list)) return item.list;
  }
  return [];
}

function extractCliTopics(data) {
  return extractCliArray(data, ['topics']);
}

function extractCliSearchTopics(data) {
  return extractCliArray(data, ['topics', 'results', 'matches']);
}

function extractCliGroups(data) {
  return extractCliArray(data, ['groups']);
}

function extractCliTopic(data) {
  const payload = unwrapCliPayload(data);
  const candidates = [payload?.topic, payload?.data?.topic, payload?.data, payload, data?.topic, data];
  for (const item of candidates) {
    if (item && typeof item === 'object' && !Array.isArray(item)) return item;
  }
  return null;
}

function extractCliNextEndTime(data, rawTopics = []) {
  const payload = unwrapCliPayload(data);
  const lastTopic = rawTopics[rawTopics.length - 1] || {};
  return firstDefined(
    payload?.end_time,
    payload?.endTime,
    payload?.next_end_time,
    payload?.nextEndTime,
    payload?.cursor?.end_time,
    payload?.cursor?.endTime,
    lastTopic.create_time,
    lastTopic.createTime,
    lastTopic.created_at,
    lastTopic.createdAt,
  );
}

function cliErrorPayload(result) {
  const { ok, ...payload } = result;
  return payload;
}

function getTopicDate(topic) {
  const createTime = String(topic.create_time || '');
  const match = createTime.match(/^(\d{4}-\d{2}-\d{2})/);
  if (match) return match[1];

  const parsed = new Date(createTime);
  if (!Number.isNaN(parsed.getTime())) return parsed.toISOString().slice(0, 10);

  return 'unknown-date';
}

function getMarkdownPath(attachmentDir, groupId, date) {
  return path.join(attachmentDir, String(groupId), `${date}.md`);
}

function toMarkdownLinkPath(markdownPath, targetPath) {
  return path.relative(path.dirname(markdownPath), targetPath).split(path.sep).join('/');
}

function renderTopicMarkdown(topic, markdownPath, index = 1) {
  const owner = topic.owner?.name || '未知作者';
  const topicUrl = topic.url || `https://wx.zsxq.com/topic/${topic.topic_id}`;
  const localAttachments = Array.isArray(topic.attachments_local) ? topic.attachments_local : [];
  const localImages = localAttachments.filter((item) => item.type === 'image' && item.path && !item.error);
  const localFiles = localAttachments.filter((item) => item.type === 'file' && item.path && !item.error);
  const lines = [
    `## ${index}. ${topic.title || owner}`,
    '',
    `- 作者: ${owner}`,
    `- 时间: ${topic.create_time || ''}`,
    `- 互动: 阅读 ${topic.reading_count || 0} / 点赞 ${topic.likes_count || 0} / 评论 ${topic.comments_count || 0}`,
    `- 原帖: ${topicUrl}`,
    '',
    topic.text || '',
    '',
  ];

  if (localImages.length > 0 || (topic.images && topic.images.length > 0)) {
    lines.push('### 图片', '');
    if (localImages.length > 0) {
      for (const image of localImages) {
        lines.push(`![${image.filename || path.basename(image.path)}](${toMarkdownLinkPath(markdownPath, image.path)})`);
      }
    } else {
      for (const [imageIndex, image] of topic.images.entries()) {
        const url = image.large?.url || image.original?.url || image.thumbnail?.url;
        if (url) lines.push(`![image_${imageIndex + 1}](${url})`);
      }
    }
    lines.push('');
  }

  if (localFiles.length > 0 || (topic.files && topic.files.length > 0)) {
    lines.push('### 文件', '');
    if (localFiles.length > 0) {
      for (const file of localFiles) {
        lines.push(`- [${file.filename || path.basename(file.path)}](${toMarkdownLinkPath(markdownPath, file.path)})`);
      }
    } else {
      for (const file of topic.files) {
        const url = file.download_url || file.url;
        if (url) lines.push(`- [${file.name || file.file_id || 'file'}](${url})`);
      }
    }
    lines.push('');
  }

  return lines.join('\n').trimEnd() + '\n';
}

function writeMarkdownByDate(result, attachmentDir) {
  if (!attachmentDir) {
    throw new Error('attachment_dir not configured; set ZSXQ_ATTACHMENT_DIR or config.json attachment_dir');
  }

  const groupId = result.group_id;
  const topicsByDate = new Map();
  for (const topic of result.topics || []) {
    const date = getTopicDate(topic);
    if (!topicsByDate.has(date)) topicsByDate.set(date, []);
    topicsByDate.get(date).push(topic);
  }

  const markdownPaths = [];
  for (const [date, topics] of topicsByDate.entries()) {
    const markdownPath = getMarkdownPath(attachmentDir, groupId, date);
    const lines = [
      `# 知识星球帖子导出 - ${date}`,
      '',
      `- 星球 ID: ${groupId}`,
      `- 帖子数: ${topics.length}`,
      '',
    ];

    topics.forEach((topic, index) => {
      lines.push(renderTopicMarkdown(topic, markdownPath, index + 1));
    });

    fs.mkdirSync(path.dirname(markdownPath), { recursive: true });
    fs.writeFileSync(markdownPath, lines.join('\n').trimEnd() + '\n', 'utf-8');
    markdownPaths.push(markdownPath);
  }

  return markdownPaths;
}

const ZSXQ_TOKEN = resolveToken();

// 附件下载配置
function loadConfig() {
  const configFile = path.join(__dirname, 'config.json');
  if (!fs.existsSync(configFile)) return {};
  try {
    return JSON.parse(fs.readFileSync(configFile, 'utf-8'));
  } catch (err) {
    console.error(`[zsxq] failed to load config.json: ${err.message}`);
    return {};
  }
}

const CONFIG = loadConfig();
const ATTACHMENT_DIR = resolveAttachmentDir(CONFIG);

// 下载文件到指定路径
function downloadFile(url, outputPath) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const reqOptions = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method: 'GET',
      headers: createAuthHeaders(),
      timeout: 30000,
    };

    const req = https.request(reqOptions, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        // 跟随重定向
        return downloadFile(res.headers.location, outputPath).then(resolve).catch(reject);
      }
      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}`));
        return;
      }
      const file = fs.createWriteStream(outputPath);
      res.pipe(file);
      file.on('finish', () => {
        file.close();
        const size = fs.statSync(outputPath).size;
        resolve({ success: true, path: outputPath, size });
      });
    });

    req.on('timeout', () => { req.destroy(); reject(new Error('Download timeout')); });
    req.on('error', (err) => reject(err));
    req.end();
  });
}

async function getFileDownloadUrl(file) {
  if (file.download_url) return file.download_url;
  if (file.url) return file.url;

  const fileId = file.file_id || file.id;
  if (!fileId) return null;

  const res = await httpGetWithRetry(`${BASE_URL}/files/${encodeURIComponent(String(fileId))}/download_url`);
  if (res.statusCode !== 200) {
    throw new Error(`download_url HTTP ${res.statusCode}`);
  }

  let data;
  try {
    data = JSON.parse(res.body);
  } catch {
    throw new Error('download_url non-JSON response');
  }

  if (!data.succeeded) {
    const detail = data.resp_data?.error || data.error || data.message || 'unknown error';
    throw new Error(`download_url API error: ${JSON.stringify(detail)}`);
  }

  const downloadUrl = data.resp_data && data.resp_data.download_url;
  if (!downloadUrl) {
    throw new Error('download_url missing in response');
  }

  return downloadUrl;
}

// 下载帖子中的图片和文件附件
async function downloadTopicAttachments(topic, groupId, outputDir) {
  const topicDate = getTopicDate(topic);
  const topicDir = getTopicAttachmentDir(outputDir, groupId, topicDate);
  if (!fs.existsSync(topicDir)) {
    fs.mkdirSync(topicDir, { recursive: true });
  }

  const downloaded = [];

  // 下载图片
  if (topic.images && topic.images.length > 0) {
    for (let i = 0; i < topic.images.length; i++) {
      const img = topic.images[i];
      const url = img.large?.url || img.thumbnail?.url || img.original?.url;
      if (!url) continue;

      const ext = img.type || 'jpg';
      const filename = getAttachmentFilename(topic.topic_id, `image_${i + 1}.${ext}`);
      const outputPath = path.join(topicDir, filename);

      if (fs.existsSync(outputPath)) {
        console.error(`[zsxq] skip existing: ${filename}`);
        downloaded.push({ type: 'image', filename, path: outputPath, skipped: true });
        continue;
      }

      try {
        await sleep(500); // 下载限速
        const result = await downloadFile(url, outputPath);
        downloaded.push({ type: 'image', filename, ...result });
        console.error(`[zsxq] downloaded: ${filename}`);
      } catch (err) {
        console.error(`[zsxq] download failed: ${filename} - ${err.message}`);
        downloaded.push({ type: 'image', filename, error: err.message });
      }
    }
  }

  // 下载文件附件
  if (topic.files && topic.files.length > 0) {
    for (let i = 0; i < topic.files.length; i++) {
      const file = topic.files[i];
      const filename = getAttachmentFilename(topic.topic_id, file.name || `file_${i + 1}`);
      const outputPath = path.join(topicDir, filename);

      if (fs.existsSync(outputPath)) {
        console.error(`[zsxq] skip existing: ${filename}`);
        downloaded.push({ type: 'file', filename, path: outputPath, skipped: true });
        continue;
      }

      try {
        const url = await getFileDownloadUrl(file);
        if (!url) {
          throw new Error('missing file_id, url, or download_url');
        }
        await sleep(500);
        const result = await downloadFile(url, outputPath);
        downloaded.push({ type: 'file', filename, ...result });
        console.error(`[zsxq] downloaded: ${filename}`);
      } catch (err) {
        console.error(`[zsxq] download failed: ${filename} - ${err.message}`);
        downloaded.push({ type: 'file', filename, error: err.message });
      }
    }
  }

  return downloaded;
}

async function maybeDownloadTopicAttachments(parsed, groupId, options = {}) {
  const shouldDownload = shouldDownloadAttachments(CONFIG, { downloadAttachments: options.force });
  if (shouldDownload && ATTACHMENT_DIR && (parsed.images.length > 0 || parsed.files.length > 0)) {
    try {
      const downloaded = await downloadTopicAttachments(parsed, groupId, ATTACHMENT_DIR);
      parsed.attachments_local = downloaded;
      console.error(`[zsxq] downloaded ${downloaded.length} attachments for topic ${parsed.topic_id}`);
    } catch (err) {
      console.error(`[zsxq] attachment download failed: ${err.message}`);
      parsed.attachments_local = { error: err.message };
    }
  }
  return parsed;
}

// ── HTTP 请求 ───────────────────────────────────────────────
function httpGet(url, options = {}) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const reqOptions = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method: 'GET',
      headers: { ...createAuthHeaders(), ...(options.headers || {}) },
      timeout: options.timeout || 15000,
    };

    const req = https.request(reqOptions, (res) => {
      const chunks = [];
      const encoding = String(res.headers['content-encoding'] || '').toLowerCase();
      let stream = res;
      if (encoding === 'gzip') {
        stream = res.pipe(zlib.createGunzip());
      } else if (encoding === 'deflate') {
        stream = res.pipe(zlib.createInflate());
      } else if (encoding === 'br') {
        stream = res.pipe(zlib.createBrotliDecompress());
      }
      stream.on('data', (chunk) => chunks.push(chunk));
      stream.on('end', () => {
        const body = Buffer.concat(chunks);
        resolve({ statusCode: res.statusCode, headers: res.headers, body: body.toString('utf-8') });
      });
      stream.on('error', (err) => reject(new Error(`Stream error: ${err.message}`)));
    });

    req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
    req.on('error', reject);
    req.end();
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function clampNumber(value, min, max) {
  if (!Number.isFinite(value)) return min;
  return Math.min(max, Math.max(min, value));
}

function calculateRetryDelayMs(attemptIndex, options = {}) {
  const baseMs = options.baseMs ?? RETRY_BASE_MS;
  const jitterRatio = options.jitterRatio ?? RETRY_JITTER_RATIO;
  const maxMs = options.maxMs ?? RETRY_MAX_DELAY_MS;
  const random = typeof options.random === 'function' ? options.random : Math.random;
  const exponential = Math.min(Math.pow(2, attemptIndex + 1) * baseMs, maxMs);
  const randomUnit = clampNumber(random(), 0, 1);
  const jitter = exponential * jitterRatio * ((randomUnit * 2) - 1);
  return clampNumber(Math.round(exponential + jitter), 0, maxMs);
}

// 指数退避重试
async function httpGetWithRetry(url, options = {}, maxRetries = 3) {
  let lastErr;
  for (let i = 0; i < maxRetries; i++) {
    try {
      const res = await httpGet(url, options);
      if (res.statusCode === 429) {
        const wait = calculateRetryDelayMs(i);
        console.error(`[zsxq] 429 rate limited, waiting ${wait}ms...`);
        await sleep(wait);
        continue;
      }
      return res;
    } catch (err) {
      lastErr = err;
      if (i < maxRetries - 1) {
        const wait = calculateRetryDelayMs(i);
        console.error(`[zsxq] request error: ${err.message}, retrying in ${wait}ms...`);
        await sleep(wait);
      }
    }
  }
  throw lastErr || new Error('max retries exceeded');
}

// ── 子命令路由 ─────────────────────────────────────────────────
function parseTopicContent(topic, textLimit = 20000) {
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

  // 图片 — 保存完整信息（含 URL）
  const images = [];
  if (talk.images && talk.images.length > 0) {
    for (const img of talk.images) {
      images.push({
        image_id: img.image_id,
        type: img.type,
        large: img.large || null,
        thumbnail: img.thumbnail || null,
        original: img.original || null,
      });
    }
  }

  // 文件附件
  const files = [];
  if (talk.files && talk.files.length > 0) {
    for (const f of talk.files) {
      files.push({
        file_id: f.file_id,
        name: f.name,
        size: f.size,
        url: f.url || null,
        download_url: f.download_url || null,
      });
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
    image_count: images.length,
    file_count: files.length,
    images: images,
    files: files,
  };
}

// ── topics / digests ────────────────────────────────────────
async function fetchTopicsHttp() {
  const cli = parseCliArgs();
  const groupId = cli.args[0];
  const count = parseInt(cli.args[1]) || 500;
  const scope = cli.args[2] || 'all'; // all | digests

  if (!groupId) {
    console.error(JSON.stringify({ error: 'Usage: node fetch_topics.js topics <group_id> [count] [scope]' }));
    process.exit(1);
  }

  const isDigests = scope === 'digests' || cli.subcommand === 'digests';
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
          action: '请设置新的 ZSXQ_TOKEN 环境变量'
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
        const parsed = parseTopicContent(t);
        // 自动下载附件（如果配置了）
        if (CONFIG.download_attachments && ATTACHMENT_DIR && (parsed.images.length > 0 || parsed.files.length > 0)) {
          try {
            const downloaded = await downloadTopicAttachments(parsed, groupId, ATTACHMENT_DIR);
            parsed.attachments_local = downloaded;
            console.error(`[zsxq] downloaded ${downloaded.length} attachments for topic ${parsed.topic_id}`);
          } catch (err) {
            console.error(`[zsxq] attachment download failed: ${err.message}`);
            parsed.attachments_local = { error: err.message };
          }
        }
        allTopics.push(parsed);
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

  if (cli.markdown) {
    result.markdown_paths = writeMarkdownByDate(result, ATTACHMENT_DIR);
  }

  console.log(JSON.stringify(result, null, 2));
}

// 新增：按日期抓取帖子
async function fetchTopicsByDateHttp() {
  const cli = parseCliArgs();
  const groupId = cli.args[0];
  const startDate = cli.args[1]; // YYYY-MM-DD
  const endDate = cli.args[2] || new Date().toISOString().split('T')[0]; // 默认今天
  const count = parseInt(cli.args[3]) || Infinity;

  if (!groupId || !startDate) {
    console.error(JSON.stringify({ error: 'Usage: node fetch_topics.js topics-by-date <group_id> <start_date> [end_date] [count]' }));
    console.error('  date format: YYYY-MM-DD');
    console.error('  example: node fetch_topics.js topics-by-date YOUR_GROUP_ID 2026-06-01 2026-06-13');
    process.exit(1);
  }

  // 验证日期格式
  if (!DATE_RE.test(startDate) || !DATE_RE.test(endDate)) {
    console.error(JSON.stringify({ error: 'Invalid date format. Use YYYY-MM-DD' }));
    process.exit(1);
  }

  console.error(`[zsxq] fetching topics for group ${groupId} from ${startDate} to ${endDate}...`);

  const endpoint = `${BASE_URL}/groups/${groupId}/topics?scope=all&count=30`;
  const allTopics = [];
  let url = endpoint;
  let pages = 0;
  const maxPages = 50; // 最多翻 50 页（1500 条）
  let shouldStop = false;

  while (allTopics.length < count && pages < maxPages && !shouldStop) {
    try {
      const res = await httpGetWithRetry(url);

      if (res.statusCode === 401) {
        console.log(JSON.stringify({ error: 'unauthorized', hint: 'Token 已过期，请更换新 token' }));
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
        const parsed = parseTopicContent(t);
        const dateState = classifyTopicDate(parsed.create_time, startDate, endDate);

        // 如果帖子时间早于开始日期，停止翻页（帖子按时间倒序）
        if (dateState === 'before-range') {
          shouldStop = true;
          break;
        }

        // 如果帖子时间在日期范围内，保留
        if (dateState === 'in-range') {
          // 自动下载附件
          if (CONFIG.download_attachments && ATTACHMENT_DIR && (parsed.images.length > 0 || parsed.files.length > 0)) {
            try {
              const downloaded = await downloadTopicAttachments(parsed, groupId, ATTACHMENT_DIR);
              parsed.attachments_local = downloaded;
            } catch (err) {
              parsed.attachments_local = { error: err.message };
            }
          }
          allTopics.push(parsed);
          if (allTopics.length >= count) {
            shouldStop = true;
            break;
          }
        }
      }

      console.error(`[zsxq] fetched ${allTopics.length} topics in range (${pages + 1} pages)`);

      // 翻页
      const lastTopic = topics[topics.length - 1];
      if (lastTopic && lastTopic.create_time && !shouldStop) {
        const endTime = encodeURIComponent(lastTopic.create_time);
        url = endpoint + `&end_time=${endTime}`;
        pages++;
        await sleep(1000);
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
    date_range: { start: startDate, end: endDate },
    count: allTopics.length,
    topics: allTopics,
  };

  if (cli.markdown) {
    result.markdown_paths = writeMarkdownByDate(result, ATTACHMENT_DIR);
  }

  console.log(JSON.stringify(result, null, 2));
}
async function fetchTopicHttp() {
  const cli = parseCliArgs();
  const groupId = cli.args[0];
  const input = cli.args[1];

  if (!groupId || !input) {
    console.error(JSON.stringify({ error: 'Usage: node fetch_topics.js topic <group_id> <topic_id_or_url>' }));
    process.exit(1);
  }

  // 支持完整链接 https://wx.zsxq.com/topic/{topic_id} 或纯 ID
  const topicId = parseTopicId(input);

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
          action: '请设置新的 ZSXQ_TOKEN 环境变量'
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
        const result = parseTopicContent(found, 20000);
        result.url = `https://wx.zsxq.com/topic/${topicId}`;
        // 自动下载附件（如果配置了）
        if (CONFIG.download_attachments && ATTACHMENT_DIR && (result.images.length > 0 || result.files.length > 0)) {
          try {
            const downloaded = await downloadTopicAttachments(result, groupId, ATTACHMENT_DIR);
            result.attachments_local = downloaded;
            console.error(`[zsxq] downloaded ${downloaded.length} attachments for topic ${result.topic_id}`);
          } catch (err) {
            console.error(`[zsxq] attachment download failed: ${err.message}`);
            result.attachments_local = { error: err.message };
          }
        }
        console.error(`[zsxq] found topic ${topicId} on page ${pages + 1}`);
        if (cli.markdown) {
          result.markdown_paths = writeMarkdownByDate({
            group_id: groupId,
            count: 1,
            topics: [result],
          }, ATTACHMENT_DIR);
        }
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
async function fetchGroupsHttp() {
  console.error('[zsxq] fetching joined groups...');

  try {
    const res = await httpGetWithRetry(`${BASE_URL}/groups`);

    if (res.statusCode === 401) {
      console.log(JSON.stringify({ 
        error: 'unauthorized', 
        hint: 'Token 已过期，请更换新 token',
        action: '请设置新的 ZSXQ_TOKEN 环境变量'
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

async function fetchSearchHttp() {
  const cli = parseCliArgs();
  const groupId = cli.args[0];
  const query = cli.args[1];
  const count = parseInt(cli.args[2], 10) || 50;

  if (!groupId || !query) {
    console.error(JSON.stringify({ error: 'Usage: node fetch_topics.js search <group_id> <keyword> [count]' }));
    process.exit(1);
  }

  console.error(`[zsxq] searching topics for group ${groupId} via legacy HTTP local filter (query=${query}, count=${count})...`);
  const allTopics = [];
  let url = `${BASE_URL}/groups/${groupId}/topics?scope=all&count=30`;
  let pages = 0;
  const maxPages = Math.ceil(Math.max(count * 3, 90) / 30);

  while (allTopics.length < count && pages < maxPages) {
    const res = await httpGetWithRetry(url);
    if (res.statusCode !== 200) {
      console.log(JSON.stringify({ error: `HTTP ${res.statusCode}`, detail: res.body.substring(0, 300) }));
      return;
    }

    let data;
    try {
      data = JSON.parse(res.body);
    } catch {
      console.log(JSON.stringify({ error: 'non_json_response' }));
      return;
    }

    if (!data.succeeded) {
      console.log(JSON.stringify({ error: 'api_error', resp: data }));
      return;
    }

    const rawTopics = data.resp_data?.topics || [];
    if (rawTopics.length === 0) break;

    for (const rawTopic of rawTopics) {
      const parsed = parseTopicContent(rawTopic);
      if (!topicMatchesQuery(parsed, query)) continue;
      await maybeDownloadTopicAttachments(parsed, groupId, { force: cli.downloadAttachments });
      allTopics.push(parsed);
      if (allTopics.length >= count) break;
    }

    const lastTopic = rawTopics[rawTopics.length - 1];
    if (!lastTopic?.create_time || allTopics.length >= count) break;
    url = `${BASE_URL}/groups/${groupId}/topics?scope=all&count=30&end_time=${encodeURIComponent(lastTopic.create_time)}`;
    pages++;
    await sleep(1000);
  }

  const result = {
    group_id: groupId,
    query,
    backend: 'http',
    count: allTopics.length,
    topics: allTopics,
  };

  if (cli.markdown) {
    result.markdown_paths = writeMarkdownByDate(result, ATTACHMENT_DIR);
  }

  console.log(JSON.stringify(result, null, 2));
}

// ── official zsxq-cli backend ────────────────────────────────
async function collectSearchTopicsCli(options = {}) {
  const {
    groupId,
    query,
    count = 50,
    cli = {},
    runner = runZsxqCliJson,
    config = CONFIG,
    downloadAttachments = maybeDownloadTopicAttachments,
  } = options;

  const response = await runner(buildCliSearchTopicsArgs(groupId, query));
  if (!response.ok) {
    return { error: cliErrorPayload(response) };
  }

  const hits = extractCliSearchTopics(response.data).map(normalizeSearchResult);
  const topics = [];

  for (const hit of hits) {
    if (topics.length >= count) break;
    if (!hit.topic_id) continue;

    const detail = await runner(buildCliTopicDetailArgs(hit.topic_id));
    let topic;
    if (!detail.ok) {
      topic = normalizeCliTopic(hit.raw);
      topic.detail_error = detail.error || 'topic_detail_failed';
    } else {
      const rawTopic = extractCliTopic(detail.data);
      topic = normalizeCliTopic(rawTopic || hit.raw);
    }

    topic.url = `https://wx.zsxq.com/topic/${topic.topic_id || hit.topic_id}`;

    if (shouldDownloadAttachments(config, cli)) {
      await downloadAttachments(topic, groupId, { force: cli.downloadAttachments });
    }

    topics.push(topic);
  }

  return { topics };
}

async function fetchSearchCli() {
  const cli = parseCliArgs();
  const groupId = cli.args[0];
  const query = cli.args[1];
  const count = parseInt(cli.args[2], 10) || 50;

  if (!groupId || !query) {
    console.error(JSON.stringify({ error: 'Usage: node fetch_topics.js search <group_id> <keyword> [count]' }));
    process.exit(1);
  }

  console.error(`[zsxq] searching topics for group ${groupId} via zsxq-cli MCP search_topics (query=${query}, count=${count})...`);
  const collected = await collectSearchTopicsCli({ groupId, query, count, cli });
  if (collected.error) {
    console.log(JSON.stringify(collected.error, null, 2));
    return;
  }

  const result = {
    group_id: groupId,
    query,
    backend: 'cli',
    count: collected.topics.length,
    topics: collected.topics,
  };

  if (cli.markdown) {
    result.markdown_paths = writeMarkdownByDate(result, ATTACHMENT_DIR);
  }

  console.log(JSON.stringify(result, null, 2));
}

async function fetchTopicsCli() {
  const cli = parseCliArgs();
  const groupId = cli.args[0];
  const count = parseInt(cli.args[1], 10) || 500;
  const scope = cli.args[2] || 'all';

  if (!groupId) {
    console.error(JSON.stringify({ error: 'Usage: node fetch_topics.js topics <group_id> [count] [scope]' }));
    process.exit(1);
  }

  const isDigests = scope === 'digests' || cli.subcommand === 'digests';
  console.error(`[zsxq] fetching ${isDigests ? 'digests' : 'all'} topics for group ${groupId} via zsxq-cli (count=${count})...`);

  const allTopics = [];
  let endTime = null;
  let pages = 0;
  const maxPages = Math.ceil(count / 30) + 1;

  while (allTopics.length < count && pages < maxPages) {
    const limit = Math.min(30, count - allTopics.length);
    const response = await runZsxqCliJson(buildCliTopicsArgs(groupId, { limit, endTime }));
    if (!response.ok) {
      console.log(JSON.stringify(cliErrorPayload(response), null, 2));
      return;
    }

    const rawTopics = extractCliTopics(response.data);
    if (rawTopics.length === 0) {
      console.error('[zsxq] no more topics from zsxq-cli');
      break;
    }

    const pageHasDigestMarker = rawTopics.some(topicHasDigestMarker);
    if (isDigests && !pageHasDigestMarker) {
      console.log(JSON.stringify({
        error: 'digests_unavailable_from_cli',
        hint: '官方 zsxq-cli 输出未包含精华标记；请使用 topics all，或显式设置 ZSXQ_BACKEND=http 使用 legacy HTTP fallback',
      }, null, 2));
      return;
    }

    for (const rawTopic of rawTopics) {
      const parsed = normalizeCliTopic(rawTopic);
      if (isDigests && !parsed.digested) continue;
      await maybeDownloadTopicAttachments(parsed, groupId);
      allTopics.push(parsed);
      if (allTopics.length >= count) break;
    }

    console.error(`[zsxq] fetched ${allTopics.length}/${count} topics`);
    endTime = extractCliNextEndTime(response.data, rawTopics);
    if (!endTime || allTopics.length >= count) break;
    pages++;
    await sleep(1000);
  }

  const result = {
    group_id: groupId,
    scope: isDigests ? 'digests' : 'all',
    backend: 'cli',
    count: allTopics.length,
    topics: allTopics,
  };

  if (cli.markdown) {
    result.markdown_paths = writeMarkdownByDate(result, ATTACHMENT_DIR);
  }

  console.log(JSON.stringify(result, null, 2));
}

async function fetchTopicsByDateCli() {
  const cli = parseCliArgs();
  const groupId = cli.args[0];
  const startDate = cli.args[1];
  const endDate = cli.args[2] || new Date().toISOString().split('T')[0];
  const count = parseInt(cli.args[3], 10) || Infinity;

  if (!groupId || !startDate) {
    console.error(JSON.stringify({ error: 'Usage: node fetch_topics.js topics-by-date <group_id> <start_date> [end_date] [count]' }));
    console.error('  date format: YYYY-MM-DD');
    console.error('  example: node fetch_topics.js topics-by-date YOUR_GROUP_ID 2026-06-01 2026-06-13');
    process.exit(1);
  }

  if (!DATE_RE.test(startDate) || !DATE_RE.test(endDate)) {
    console.error(JSON.stringify({ error: 'Invalid date format. Use YYYY-MM-DD' }));
    process.exit(1);
  }

  console.error(`[zsxq] fetching topics for group ${groupId} from ${startDate} to ${endDate} via zsxq-cli...`);

  const allTopics = [];
  let endTime = null;
  let pages = 0;
  const maxPages = 50;
  let shouldStop = false;

  while (allTopics.length < count && pages < maxPages && !shouldStop) {
    const remaining = Number.isFinite(count) ? count - allTopics.length : 30;
    const response = await runZsxqCliJson(buildCliTopicsArgs(groupId, { limit: Math.min(30, remaining), endTime }));
    if (!response.ok) {
      console.log(JSON.stringify(cliErrorPayload(response), null, 2));
      return;
    }

    const rawTopics = extractCliTopics(response.data);
    if (rawTopics.length === 0) {
      console.error('[zsxq] no more topics from zsxq-cli');
      break;
    }

    for (const rawTopic of rawTopics) {
      const parsed = normalizeCliTopic(rawTopic);
      const dateState = classifyTopicDate(parsed.create_time, startDate, endDate);

      if (dateState === 'before-range') {
        shouldStop = true;
        break;
      }

      if (dateState === 'in-range') {
        await maybeDownloadTopicAttachments(parsed, groupId);
        allTopics.push(parsed);
        if (allTopics.length >= count) {
          shouldStop = true;
          break;
        }
      }
    }

    console.error(`[zsxq] fetched ${allTopics.length} topics in range (${pages + 1} pages)`);
    endTime = extractCliNextEndTime(response.data, rawTopics);
    if (!endTime || shouldStop) break;
    pages++;
    await sleep(1000);
  }

  const result = {
    group_id: groupId,
    date_range: { start: startDate, end: endDate },
    backend: 'cli',
    count: allTopics.length,
    topics: allTopics,
  };

  if (cli.markdown) {
    result.markdown_paths = writeMarkdownByDate(result, ATTACHMENT_DIR);
  }

  console.log(JSON.stringify(result, null, 2));
}

async function fetchTopicCli() {
  const cli = parseCliArgs();
  const groupId = cli.args[0];
  const input = cli.args[1];

  if (!groupId || !input) {
    console.error(JSON.stringify({ error: 'Usage: node fetch_topics.js topic <group_id> <topic_id_or_url>' }));
    process.exit(1);
  }

  const topicId = parseTopicId(input);
  console.error(`[zsxq] fetching topic ${topicId} via zsxq-cli...`);

  const response = await runZsxqCliJson(buildCliTopicDetailArgs(topicId));
  if (!response.ok) {
    console.log(JSON.stringify(cliErrorPayload(response), null, 2));
    return;
  }

  const rawTopic = extractCliTopic(response.data);
  if (!rawTopic) {
    console.log(JSON.stringify({
      error: 'topic_not_found',
      topic_id: topicId,
      group_id: groupId,
      hint: '官方 zsxq-cli 未返回该帖子详情，请确认 topic_id 和账号权限',
    }, null, 2));
    return;
  }

  const result = normalizeCliTopic(rawTopic, 20000);
  result.url = `https://wx.zsxq.com/topic/${topicId}`;
  await maybeDownloadTopicAttachments(result, groupId);

  if (cli.markdown) {
    result.markdown_paths = writeMarkdownByDate({
      group_id: groupId,
      count: 1,
      topics: [result],
    }, ATTACHMENT_DIR);
  }

  console.log(JSON.stringify(result, null, 2));
}

async function fetchGroupsCli() {
  console.error('[zsxq] fetching joined groups via zsxq-cli...');
  const response = await runZsxqCliJson(buildCliGroupsArgs());
  if (!response.ok) {
    console.log(JSON.stringify(cliErrorPayload(response), null, 2));
    return;
  }

  const groups = extractCliGroups(response.data).map(normalizeCliGroup);
  console.error(`[zsxq] found ${groups.length} groups`);
  console.log(JSON.stringify({ backend: 'cli', groups }, null, 2));
}

async function fetchTopics(backend = resolveBackend(CONFIG)) {
  return backend === 'http' ? fetchTopicsHttp() : fetchTopicsCli();
}

async function fetchTopicsByDate(backend = resolveBackend(CONFIG)) {
  return backend === 'http' ? fetchTopicsByDateHttp() : fetchTopicsByDateCli();
}

async function fetchTopic(backend = resolveBackend(CONFIG)) {
  return backend === 'http' ? fetchTopicHttp() : fetchTopicCli();
}

async function fetchGroups(backend = resolveBackend(CONFIG)) {
  return backend === 'http' ? fetchGroupsHttp() : fetchGroupsCli();
}

async function fetchSearch(backend = resolveBackend(CONFIG)) {
  return backend === 'http' ? fetchSearchHttp() : fetchSearchCli();
}

module.exports = {
  resolveToken,
  resolveBackend,
  parseTopicId,
  classifyTopicDate,
  getTopicAttachmentDir,
  sanitizeAttachmentFilename,
  getAttachmentFilename,
  resolveAttachmentDir,
  createBrowserHeaders,
  createAuthHeaders,
  calculateRetryDelayMs,
  parseCliArgs,
  getTopicDate,
  getMarkdownPath,
  renderTopicMarkdown,
  writeMarkdownByDate,
  parseTopicContent,
  downloadTopicAttachments,
  buildCliGroupsArgs,
  buildCliTopicsArgs,
  buildCliTopicDetailArgs,
  buildCliSearchTopicsArgs,
  shouldDownloadAttachments,
  runZsxqCliJson,
  extractCliSearchTopics,
  collectSearchTopicsCli,
  normalizeCliTopic,
  normalizeCliGroup,
  topicMatchesQuery,
  filterTopicsByQuery,
  normalizeSearchResult,
  topicHasDigestMarker,
  fetchSearch,
};

// ── main ─────────────────────────────────────────────────────
async function main() {
  const backend = resolveBackend(CONFIG);

  if (backend === 'http' && !ZSXQ_TOKEN) {
    console.error(JSON.stringify({
      error: 'ZSXQ_TOKEN not configured',
      hint: '当前使用 legacy HTTP fallback，请先设置：export ZSXQ_TOKEN="your_token"；默认官方 CLI 路径请取消 ZSXQ_BACKEND=http 并运行 zsxq-cli auth login',
    }));
    process.exit(1);
  }

  const { subcommand } = parseCliArgs();

  try {
    switch (subcommand) {
      case 'topics':
        await fetchTopics(backend);
        break;
      case 'digests':
        // digests 是 topics 的快捷方式，scope 固定为 digests
        await fetchTopics(backend);
        break;
      case 'topic':
        await fetchTopic(backend);
        break;
      case 'topics-by-date':
        await fetchTopicsByDate(backend);
        break;
      case 'search':
        await fetchSearch(backend);
        break;
      case 'groups':
        await fetchGroups(backend);
        break;
      default:
        console.error(`Unknown subcommand: ${subcommand}. Use: topics, digests, topic, topics-by-date, search, groups`);
        process.exit(1);
    }
  } catch (err) {
    console.error(`[zsxq] fatal error: ${err.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
