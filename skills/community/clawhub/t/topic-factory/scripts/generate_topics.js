/**
 * generate_topics.js - 自媒体素材库生成脚本
 *
 * 功能：每天自动抓取 4 大平台热榜 → 关键词匹配 → 流量分排序 → 输出 Markdown 选题库
 * 使用：node generate_topics.js
 * 依赖：Node.js >= 18（原生 fetch），agent-browser（抖音热榜）
 *
 * 作者：Claude
 * 日期：2026-08-14
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ============================================================
// 1. 路径配置
// ============================================================

// 选题库输出目录：${TOPICS_DIR}/claude-hub/topics/
const TOPICS_DIR = path.join(
  process.env.HOME || require('os').homedir(),
  '.openclaw/workspace/claude-hub/topics'
);

// 历史归档目录
const HISTORY_DIR = path.join(TOPICS_DIR, 'history');

// 日志目录（记录每次抓取的原始数据）
const LOG_DIR = path.join(__dirname, 'logs');

// 确保目录存在
[TOPICS_DIR, HISTORY_DIR, LOG_DIR].forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

// ============================================================
// 2. 关键词库（6 大类，119 词，直接 hardcode 在代码里）
//    与 design doc 保持一致，便于用户随时增删
// ============================================================

const KEYWORD_DB = {
  A: {
    name: '财经投资',
    keywords: [
      '半导体', '存储', '新质生产力', '医疗', '生物医药', '大健康', '储能',
      '低空经济', '人形机器人', '商业航天', '机器人产业链', 'A股', '股市',
      '股票', '基金', '理财', '投资', '财报', '新股', 'IPO', '上市', 'CPI',
      'PPI', 'M2', 'PMI', '社融', '汇率', '北向', '融资融券', '龙虎榜', '主力'
    ]
  },
  B: {
    name: '房产',
    keywords: [
      '城市更新', '文旅地产', '产业导入', '旅游', '文创', 'EOD', '乡村振兴',
      '全域治理', '全域整治', '公寓', 'TOD', '产业园', '众创空间', '人才公寓',
      '长租公寓', '共有产权', '租赁住房', 'REITs', '保障房', '政策性住房',
      '限购', '限售', '户口', '平急两用', '城中村改造', '楼市', '房价', '土拍',
      '专项债', 'PSL'
    ]
  },
  C: {
    name: '政策类',
    keywords: [
      '楼市新政', '公积金', '贷款利率', '消费贷利率', '房贷利率', '社保',
      '降息', '加息', '央行', '证监会'
    ]
  },
  D: {
    name: 'AI科技',
    keywords: [
      'AI', '人工智能', '大模型', 'ChatGPT', 'Claude', 'GPT', 'Gemini', '芯片',
      '算力', 'GPU', '英伟达', 'AMD', '华为', '机器人', 'AI编程', 'AI写作',
      'AI视频', 'Sora', 'Runway', 'Agent', '智能体', 'Manus', 'Coze', '扣子',
      'Dify', 'Cursor', 'Devin', 'AutoGPT', 'LangChain', 'MCP', 'Skills'
    ]
  },
  E: {
    name: '中国大模型公司',
    keywords: [
      '智谱', 'GLM', '月之暗面', 'Kimi', '百川', '零一万物', 'DeepSeek',
      '通义千问', 'Qwen', '文心一言', '混元', '豆包', '星火', '盘古', '商量',
      '阶跃星辰', '阿里', '百度', '腾讯', '字节'
    ]
  }
};

// 用户的自媒体 4 方向优先级（设计文档第 5 节）
// D=AI科技 权重最高，其次 A=财经投资，B=房产，C=政策
const KENT_PRIORITY = ['D', 'A', 'B', 'C'];

// 各类目在流量分中的权重系数（设计文档第 6 节）
const CAT_WEIGHT = {
  D: 1.5,   // AI科技 最高权重
  A: 1.3,   // 财经投资
  B: 1.2,   // 房产
  C: 1.0,   // 政策类
  E: 1.1    // 大模型公司 介于 A 和 C 之间
};

// ============================================================
// 3. 工具函数
// ============================================================

/**
 * 智能截断：找最近的句子结束符
 * @param {string} text - 待截断文本
 * @param {number} maxLen - 最大长度
 * @returns {string} 截断后文本
 */
function truncateHook(text, maxLen = 30) {
  if (text.length <= maxLen) return text;
  // 在 [maxLen-8, maxLen-1] 范围内找最近的句子结束符
  for (let i = maxLen - 1; i > Math.max(maxLen - 8, 0); i--) {
    if (/[。，！？、,!?]/.test(text[i])) {
      return text.slice(0, i + 1);
    }
  }
  return text.slice(0, maxLen - 3) + '...';
}

/**
 * 禁用词后处理替换（公众号标题用）
 *
 * LLM 偶尔会违反 prompt 约束（最常见："背后"、"真相"）。
 * 在生成 markdown 时做一次后处理，避免用户手动清理。
 *
 * 替换策略：禁用词 → 同义中性词
 *   "背后" → "原因"
 *   "真相" → "事实"
 *   "答案" → "回复"
 *   "原来如此" → "原来这样"
 *   "万万没想到" → "没想到"
 *   "太可怕了" → "值得关注"
 *
 * @param {string} text
 * @returns {string}
 */
function sanitizeForbiddenWords(text) {
  if (!text) return text;
  const replacements = {
    '背后': '原因',
    '真相': '事实',
    '答案': '回复',
    '原来如此': '原来这样',
    '万万没想到': '没想到',
    '太可怕了': '值得关注'
  };
  let result = text;
  for (const [bad, good] of Object.entries(replacements)) {
    result = result.replace(new RegExp(bad, 'g'), good);
  }
  return result;
}

/**
 * 带超时的 fetch 封装
 * @param {string} url - 请求地址
 * @param {number} timeoutMs - 超时毫秒数
 * @returns {Promise<any>} JSON 响应体
 */
async function fetchWithTimeout(url, timeoutMs = 8000, options = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  // 默认 headers（Desktop Chrome UA），可被 options.headers 覆盖
  const defaultHeaders = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9'
  };
  const headers = { ...defaultHeaders, ...(options.headers || {}) };

  try {
    const resp = await fetch(url, {
      signal: controller.signal,
      headers,
      ...options
    });
    clearTimeout(timer);
    const contentType = resp.headers.get('content-type') || '';
    if (contentType.includes('application/json')) {
      return await resp.json();
    } else {
      // RSS XML 等非 JSON 响应
      return await resp.text();
    }
  } catch (err) {
    clearTimeout(timer);
    throw err;
  }
}

/**
 * 记录日志到 logs/ 目录（当次抓取的原始数据，便于排查）
 * @param {string} source - 数据源名称
 * @param {any} data - 原始数据
 */
function logRaw(source, data) {
  const ts = new Date().toISOString().replace(/[:.]/g, '-');
  const logPath = path.join(LOG_DIR, `${source}_${ts}.json`);
  try {
    fs.writeFileSync(logPath, JSON.stringify(data, null, 2));
  } catch (_) {
    // 日志写入失败不影响主流程
  }
}

/**
 * 关键词匹配
 *
 * 算法（设计文档第 5 节）：
 *   1. 遍历 5 个类目，统计每个类目命中的关键词数量
 *   2. rawCats = 有命中的类目列表
 *   3. extended = 用户优先级顺序中还未命中的类目（用于延伸方向提示）
 *
 * @param {string} text - 待匹配的文本（标题 + 描述）
 * @returns {{ rawHit: Object, rawCats: string[], extended: string[] }}
 */
function matchKeywords(text) {
  const rawHit = {};

  // 遍历每个类目，统计命中关键词
  for (const [cat, info] of Object.entries(KEYWORD_DB)) {
    const hits = info.keywords.filter(kw => text.includes(kw));
    if (hits.length > 0) {
      rawHit[cat] = hits;
    }
  }

  // 有命中的类目
  const rawCats = Object.keys(rawHit);

  // 按用户优先级补充还未命中的类目（延伸方向）
  const extended = KENT_PRIORITY.filter(c => !rawCats.includes(c));

  return { rawHit, rawCats, extended };
}

/**
 * 流量分计算
 *
 * 算法（设计文档第 6 节）：
 *   score = heat(热度对数归一化) × hook(钩子词加成) × catWeight(类目权重)
 *
 * @param {Object} item - 选题对象，需包含 hotValue、text、primaryCat
 * @returns {number} 流量分（越高越值得做）
 */
function flowScore(item) {
  // heat：热度值取对数归一化，最高 10 分
  // 假设热度值最大 1000 万，log10(10^7)/7 ≈ 1，取 min 上限 10
  const heat = Math.min(
    Math.log10(item.hotValue || 10000) / 7,
    10
  );

  // hook：钩子词加成（数据感、转折感、新闻感）
  let hook = 1.0;
  if (/\d+万|\d+亿|\d+倍/.test(item.text)) hook += 0.3;    // 数据感
  if (/看似|实际|却|反而|意外/.test(item.text)) hook += 0.2; // 转折感
  if (/新|首次|突破|创/.test(item.text)) hook += 0.2;       // 新闻感
  // 感叹号过多可能是标题党，轻微扣分
  if (/[!?！？]/.test(item.text)) hook -= 0.5;

  // 类目权重
  const catWeight = CAT_WEIGHT[item.primaryCat] || 1.0;

  return heat * hook * catWeight;
}

/**
 * 确定主要类目（rawCats 中优先级最高的）
 * @param {string[]} rawCats - 命中的类目列表
 * @returns {string} 优先级最高的类目字母
 */
function primaryCat(rawCats) {
  // 按 KENT_PRIORITY 顺序，第一个命中的就是主类目
  for (const c of KENT_PRIORITY) {
    if (rawCats.includes(c)) return c;
  }
  return rawCats[0] || 'A';
}

// ============================================================
// 4. 四个数据源抓取函数
// ============================================================

/**
 * 4.1 头条热榜
 *
 * URL: https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc
 * 超时: 5 秒
 * 返回格式: JSON { data: [{ Title, HotValue, Label, Url, InterestCategory }] }
 * 过滤: InterestCategory ∈ {finance, technology} 优先 + 关键词兜底
 * 取 Top 8 条
 */
async function fetchToutiaoHot() {
  console.log('[头条] 开始抓取...');

  const json = await fetchWithTimeout(
    'https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc',
    5000
  );

  logRaw('toutiao', json);

  // 解析数据
  const rawList = json?.data || [];
  const items = [];

  for (const item of rawList) {
    const text = item.Title || '';
    const { rawCats } = matchKeywords(text);

    // 优先取财经(finance)和科技(technology)类目，兜底用关键词命中
    const isPriorityCat =
      item.InterestCategory === 'finance' ||
      item.InterestCategory === 'technology';

    if (isPriorityCat || rawCats.length > 0) {
      items.push({
        platform: '头条',
        text,
        hotValue: item.HotValue || 0,
        url: item.Url || '',
        label: item.Label || '',
        primaryCat: primaryCat(rawCats),
        match: matchKeywords(text)
      });
    }

    if (items.length >= 50) break;
  }

  console.log(`[头条] 获取 ${items.length} 条`);
  return items;
}

/**
 * 4.2 微博热搜
 *
 * URL: https://api.weibo.cn/2/guest/search/hot/word
 * 超时: 5 秒
 * 返回格式: JSON { data: [{ word, num, flag }] }
 * 过滤: 关键词命中
 * 取 Top 5 条
 */
async function fetchWeiboHot() {
  console.log('[微博] 开始抓取...');

  const json = await fetchWithTimeout(
    'https://api.weibo.cn/2/guest/search/hot/word',
    5000
  );

  logRaw('weibo', json);

  const rawList = json?.data || [];
  const items = [];

  for (const item of rawList) {
    const text = item.word || '';
    const { rawCats } = matchKeywords(text);

    if (rawCats.length > 0) {
      items.push({
        platform: '微博',
        text,
        hotValue: item.num || 0,
        url: `https://s.weibo.com/weibo?q=${encodeURIComponent(text)}`,
        label: item.flag || '',
        primaryCat: primaryCat(rawCats),
        match: matchKeywords(text)
      });
    }

    if (items.length >= 50) break;
  }

  console.log(`[微博] 获取 ${items.length} 条`);
  return items;
}

/**
 * 4.3 B站热搜
 *
 * URL: https://api.bilibili.com/x/web-interface/search/square?limit=50
 * 超时: 5 秒
 * 返回格式: JSON { data: { trending: { list: [{ keyword, hot_value }] } } }
 * 过滤: 关键词命中
 * 取 Top 5 条
 */
async function fetchBilibiliHot() {
  console.log('[B站] 开始抓取...');

  const json = await fetchWithTimeout(
    'https://api.bilibili.com/x/web-interface/search/square?limit=50',
    5000
  );

  logRaw('bilibili', json);

  const rawList = json?.data?.trending?.list || [];
  const items = [];

  for (const item of rawList) {
    const text = item.keyword || '';
    const { rawCats } = matchKeywords(text);

    if (rawCats.length > 0) {
      items.push({
        platform: 'B站',
        text,
        hotValue: item.hot_value || 0,
        url: `https://search.bilibili.com/all?keyword=${encodeURIComponent(text)}`,
        label: '',
        primaryCat: primaryCat(rawCats),
        match: matchKeywords(text)
      });
    }

    if (items.length >= 50) break;
  }

  console.log(`[B站] 获取 ${items.length} 条`);
  return items;
}

/**
 * 4.4 抖音热榜（HTTP API，移动端 UA）
 *
 * URL: https://www.douyin.com/aweme/v1/web/hot/search/list/?aid=6383&count=50
 * 超时: 8 秒
 * 移动端 UA 是必须的（桌面 UA 返回空）
 * 响应: { data: { word_list: [{ word, hot_value, position, video_count, ... }] } }
 * 过滤: 关键词命中
 * 取 Top 50 条
 */
async function fetchDouyinHotAPI() {
  console.log('[抖音] 开始抓取（HTTP API）...');

  try {
    const json = await fetchWithTimeout(
      'https://www.douyin.com/aweme/v1/web/hot/search/list/?aid=6383&count=50',
      8000,
      {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
          'Referer': 'https://www.douyin.com/'
        }
      }
    );

    logRaw('douyin', json);

    const wordList = json?.data?.word_list || [];
    const items = [];

    for (const item of wordList) {
      const text = item.word || '';
      if (!text) continue;

      const { rawCats } = matchKeywords(text);
      if (rawCats.length === 0) continue;

      items.push({
        platform: '抖音',
        text,
        hotValue: item.hot_value || 0,
        url: 'https://www.douyin.com/hot',
        label: `热度 ${item.hot_value || 0}`,
        primaryCat: primaryCat(rawCats),
        match: matchKeywords(text)
      });

      if (items.length >= 50) break;
    }

    console.log(`[抖音] 获取 ${items.length} 条`);
    return items;
  } catch (e) {
    console.error(`[抖音] 抓取失败: ${e.message}`);
    return [];
  }
}

/**
 * 4.5 知乎热榜
 *
 * URL: https://api.zhihu.com/topstory/hot-lists/total?limit=50
 * 超时: 8 秒
 * 响应: { data: [{ target: { title, url, ... }, detail_text, ... }] }
 * 过滤: 关键词命中
 * 取 Top 50 条
 */
async function fetchZhihuHot() {
  console.log('[知乎] 开始抓取...');

  try {
    const json = await fetchWithTimeout(
      'https://api.zhihu.com/topstory/hot-lists/total?limit=50',
      8000,
      {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
      }
    );

    logRaw('zhihu', json);

    const data = json?.data || [];
    const items = [];

    for (const item of data) {
      const target = item.target || {};
      const text = target.title || item.detail_text || '';
      if (!text) continue;

      const { rawCats } = matchKeywords(text);
      if (rawCats.length === 0) continue;

      items.push({
        platform: '知乎',
        text,
        hotValue: 0,  // 知乎热榜没明确的热度数字
        url: target.url || `https://www.zhihu.com/question/${target.id}`,
        label: item.detail_text?.slice(0, 20) || '',
        primaryCat: primaryCat(rawCats),
        match: matchKeywords(text)
      });

      if (items.length >= 50) break;
    }

    console.log(`[知乎] 获取 ${items.length} 条`);
    return items;
  } catch (e) {
    console.error(`[知乎] 抓取失败: ${e.message}`);
    return [];
  }
}

/**
 * 4.6 36 氪 RSS（科技/创业新闻）
 *
 * URL: https://www.36kr.com/feed
 * 超时: 8 秒
 * 响应: RSS XML
 * 过滤: 关键词命中
 * 取 Top 50 条
 */
async function fetch36krRSS() {
  console.log('[36氪] 开始抓取（RSS）...');

  // 36 小时时间窗口：过滤编辑推荐段的旧文章
  // 修复：RSS feed 第 1-10 条是"编辑推荐"（混合多日数据，不按时间排序）
  // 不加窗口会导致 8/14、8/15 的旧文章命中关键词后霸占选题
  const TIME_WINDOW_HOURS = 36;
  const cutoffMs = Date.now() - TIME_WINDOW_HOURS * 60 * 60 * 1000;
  let filteredOld = 0;

  try {
    const xml = await fetchWithTimeout(
      'https://www.36kr.com/feed',
      8000,
      {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
      }
    );

    logRaw('36kr', { raw: String(xml).slice(0, 200) });

    // 简单 XML 解析（不引入额外依赖）
    // 提取 <item>...</item> 块
    const itemRegex = /<item>([\s\S]*?)<\/item>/g;
    const items = [];
    let match;

    while ((match = itemRegex.exec(String(xml))) !== null) {
      const itemXml = match[1];
      // 提取标题
      const titleMatch = itemXml.match(/<title><!\[CDATA\[([\s\S]*?)\]\]><\/title>/) ||
                         itemXml.match(/<title>([\s\S]*?)<\/title>/);
      if (!titleMatch) continue;
      const text = titleMatch[1].trim();
      if (!text) continue;

      const { rawCats } = matchKeywords(text);
      if (rawCats.length === 0) continue;

      // 提取发布时间（先提取，用于时间窗口判断）
      const dateMatch = itemXml.match(/<pubDate>([\s\S]*?)<\/pubDate>/);
      const dateStr = dateMatch ? dateMatch[1].trim() : '';

      // 时间窗口过滤：跳过 36 小时之前的文章
      if (dateStr) {
        const itemTime = new Date(dateStr).getTime();
        if (!isNaN(itemTime) && itemTime < cutoffMs) {
          filteredOld++;
          continue;
        }
      }

      // 提取链接
      const linkMatch = itemXml.match(/<link><!\[CDATA\[([\s\S]*?)\]\]><\/link>/) ||
                        itemXml.match(/<link>([\s\S]*?)<\/link>/);
      const url = linkMatch ? linkMatch[1].trim() : 'https://36kr.com';

      items.push({
        platform: '36氪',
        text,
        hotValue: 0,
        url,
        label: dateStr.slice(0, 16),
        primaryCat: primaryCat(rawCats),
        match: matchKeywords(text)
      });

      if (items.length >= 50) break;
    }

    console.log(`[36氪] 获取 ${items.length} 条（过滤 ${filteredOld} 条 ${TIME_WINDOW_HOURS}h 之前旧文章）`);
    return items;
  } catch (e) {
    console.error(`[36氪] 抓取失败: ${e.message}`);
    return [];
  }
}


/**
 * 将热度字符串转换为数字
 *   "770万" → 7700000
 *   "1.2亿" → 120000000
 *   "5000"  → 5000
 *
 * @param {string} hotStr
 * @returns {number}
 */
function parseHotString(hotStr) {
  if (!hotStr) return 0;
  hotStr = hotStr.trim();

  if (/亿/.test(hotStr)) {
    return parseFloat(hotStr.replace('亿', '')) * 100000000;
  }
  if (/万/.test(hotStr)) {
    return parseFloat(hotStr.replace('万', '')) * 10000;
  }
  return parseFloat(hotStr) || 0;
}

// ============================================================
// 5. 钩子文案生成（LLM 调用）
// ============================================================

/**
 * LLM 调用重试封装
 * @param {Function} fn - 要执行的异步函数
 * @param {number} retries - 剩余重试次数
 * @param {string} label - 日志标签
 */
async function withRetry(fn, retries = 2, label = 'LLM') {
  for (let attempt = 1; attempt <= retries + 1; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (attempt > retries) {
        throw err;
      }
      console.warn(`[${label}] 第 ${attempt} 次失败: ${err.message}，3 秒后重试...`);
      await new Promise(r => setTimeout(r, 3000));
    }
  }
}

/**
 * 调用 LLM 生成钩子文案（60秒口播钩子 + 公众号标题候选）
 *
 * @param {Object} item - 选题对象
 * @returns {Promise<{hook: string, gzhTitles: string[]}>}
 */
async function generateHookCopy(item) {
  const baseUrl = ((process.env.ANTHROPIC_BASE_URL || 'https://api.anthropic.com').replace(/\/$/, '')) + '/v1';
  const apiKey = process.env.ANTHROPIC_AUTH_TOKEN;

  const hotStr = item.label || formatHotValue(item.hotValue);
  const hitWords = Object.values(item.match.rawHit).flat().slice(0, 3).join('、');

  const prompt = `你是一个抖音/公众号自媒体运营专家，只看数据说话。

【选题信息】
标题：${item.text}
热度：${hotStr}
命中关键词：${hitWords}
类目：${KEYWORD_DB[item.primaryCat]?.name || '综合'}
参考时间：2026年8月

【约束清单——必须严格执行】
1. 禁止词（绝对不能出现）：颠覆、沉默、看完、惊呆、吓傻、颤抖、泪目、破防、笑死、气死、真相、背后、答案、原来如此、万万没想到、太可怕了、一定涨、一定跌、稳赚、翻倍、必涨、抄底、逃顶、暴富、血亏、梭哈、加仓、解套
2. 禁止句末标点：标题候选不得以'！'或'？'结尾
3. 禁止主观判断：不得使用'好''坏''对''错''应该''必须'等词
4. 禁止口号和涨跌预测

【输出要求】
1. 抖音60秒口播钩子（20-30字）：必须包含≥1个具体数字（百万/千万/亿/倍/百分比）+ 时间戳（2026年8月）
2. 公众号标题候选2个（各15-25字，无句末标点）：用数据感标题风格

请直接输出JSON（不要任何其他文字）：
{
  "hook": "口播钩子（数字+时间戳，数据感或转折感）",
  "gzhTitles": ["标题1（15-25字，无！无？）", "标题2（15-25字，无！无？）"]
}`;

  if (!apiKey) {
    return fallbackHookCopy(item);
  }

  try {
    const result = await withRetry(async () => {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 15000);

      const resp = await fetch(`${baseUrl}/messages`, {
        method: 'POST',
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
          model: process.env.LLM_MODEL || 'claude-3-5-sonnet-20241022',
          max_tokens: 300,
          messages: [{ role: 'user', content: prompt }]
        })
      });

      clearTimeout(timer);

      if (!resp.ok) {
        const body = await resp.text().catch(() => '');
        throw new Error(`LLM API error: ${resp.status} - ${body.slice(0, 100)}`);
      }

      const json = await resp.json();
      const text = json.content?.[0]?.text || '';

      // 提取 JSON
      const jsonMatch = text.match(/\{[\s\S]*?\}/);
      if (!jsonMatch) {
        throw new Error('No JSON in LLM response');
      }

      const parsed = JSON.parse(jsonMatch[0]);
      return {
        hook: parsed.hook || fallbackHookCopy(item).hook,
        gzhTitles: Array.isArray(parsed.gzhTitles) ? parsed.gzhTitles : []
      };
    }, 2, 'LLM-钩子');

    return result;
  } catch (err) {
    console.warn(`[LLM] 钩子生成失败: ${err.message}，使用模板兜底`);
    return fallbackHookCopy(item);
  }
}

/**
 * 模板兜底钩子文案
 * @param {Object} item
 * @returns {{hook: string, gzhTitles: string[]}}
 */
function fallbackHookCopy(item) {
  const cat = item.primaryCat;
  const catName = KEYWORD_DB[cat]?.name || '综合';
  const hotStr = item.label || formatHotValue(item.hotValue);
  const platform = item.platform;
  const hitWords = Object.values(item.match.rawHit).flat();

  const templates = {
    D: [
      `${platform}热榜：${item.text}，${hotStr}，2026年8月AI赛道数据盘点`,
      `${hotStr}！${item.text}在${platform}爆了，2026年8月从业者关注`
    ],
    A: [
      `${platform}财经热榜：${item.text}，${hotStr}关注度，2026年8月板块数据`,
      `${hotStr}！${item.text}登上${platform}热榜，2026年8月投资聚焦`
    ],
    B: [
      `${platform}热议：${item.text}，${hotStr}热度，2026年8月楼市数据盘点`,
      `${hotStr}！${item.text}在${platform}引发关注，2026年8月房产动态`
    ],
    C: [
      `${platform}政策面：${item.text}，${hotStr}关注度，2026年8月政策解读`,
      `${hotStr}！${item.text}在${platform}成热点，2026年8月政策观察`
    ]
  };

  const pool = templates[cat] || templates.A;
  const hook = pool[Math.floor(Math.random() * pool.length)];
  return { hook, gzhTitles: [] };
}

/**
 * 格式化热度值为可读字符串
 * @param {number} val
 * @returns {string}
 */
function formatHotValue(val) {
  if (val >= 100000000) return (val / 100000000).toFixed(1) + '亿';
  if (val >= 10000) return (val / 10000).toFixed(1) + '万';
  return String(val);
}

// ============================================================
// 5.1 数据点补充（LLM 生成）
// ============================================================

/**
 * 调用 LLM 生成 3 个数据点（数字 + 时间 + 来源）
 *
 * @param {Object} item - 选题对象
 * @returns {Promise<Array<{text: string, source: string}>>}
 */
async function generateDataPoints(item) {
  const baseUrl = ((process.env.ANTHROPIC_BASE_URL || 'https://api.anthropic.com').replace(/\/$/, '')) + '/v1';
  const apiKey = process.env.ANTHROPIC_AUTH_TOKEN;

  const prompt = `你是一个数据分析师，只引用真实可查证的数据。

【选题信息】
标题：${item.text}
平台：${item.platform}
命中关键词：${Object.values(item.match.rawHit).flat().slice(0, 5).join('、')}
当前参考时间：2026年8月

【约束清单——必须严格执行】
1. 禁止词（绝对不能出现）：颠覆、沉默、看完、惊呆、吓傻、颤抖、泪目、破防、笑死、气死、真相、背后、答案、原来如此、万万没想到、太可怕了、一定涨、一定跌、稳赚、翻倍、必涨、抄底、逃顶、暴富、血亏、梭哈、加仓、解套
2. 禁止主观判断：不得使用'好''坏''对''错''应该''必须'
3. 禁止编造具体新闻事件（只提供行业数据、统计数字、报告结论）
4. 每个数据点必须包含：具体数字（百万/千万/亿/倍/百分比）+ 时间戳（近年）+ 数据来源

【输出要求】
生成3个事实型数据点，格式如下（JSON数组，不要任何其他文字）：
[
  {"text": "数据点描述，包含具体数字和近年时间（如2024年、2025年上半年等）", "source": "权威来源（如：Wind、IDC、中国汽车工业协会等）"},
  {"text": "数据点描述，包含具体数字和近年时间", "source": "权威来源"},
  {"text": "数据点描述，包含具体数字和近年时间", "source": "权威来源"}
]`;

  if (!apiKey) {
    return [
      { text: `⚠️ 待手动补充（LLM API key 未配置）`, source: '—' },
      { text: '⚠️ 待手动补充', source: '—' },
      { text: '⚠️ 待手动补充', source: '—' }
    ];
  }

  try {
    const result = await withRetry(async () => {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 15000);

      const resp = await fetch(`${baseUrl}/messages`, {
        method: 'POST',
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
          model: process.env.LLM_MODEL || 'claude-3-5-sonnet-20241022',
          max_tokens: 400,
          messages: [{ role: 'user', content: prompt }]
        })
      });

      clearTimeout(timer);

      if (!resp.ok) {
        const body = await resp.text().catch(() => '');
        throw new Error(`LLM API error: ${resp.status} - ${body.slice(0, 100)}`);
      }

      const json = await resp.json();
      const text = json.content?.[0]?.text || '';

      const jsonMatch = text.match(/\[[\s\S]*?\]/);
      if (!jsonMatch) {
        throw new Error('No JSON array in LLM response');
      }

      const parsed = JSON.parse(jsonMatch[0]);
      if (!Array.isArray(parsed) || parsed.length < 3) {
        throw new Error('Invalid LLM response format');
      }

      return parsed.slice(0, 3).map(p => ({
        text: p.text || '⚠️ 待手动补充',
        source: p.source || '—'
      }));
    }, 2, 'LLM-数据点');

    return result;
  } catch (err) {
    console.warn(`[LLM] 数据点生成失败: ${err.message}`);
    return [
      { text: '⚠️ 待手动补充', source: '—' },
      { text: '⚠️ 待手动补充', source: '—' },
      { text: '⚠️ 待手动补充', source: '—' }
    ];
  }
}

// ============================================================
// 6. Markdown 生成
// ============================================================

/**
 * 生成选题库 Markdown 文件
 *
 * 模板参考设计文档第 7 节
 *
 * @param {Object[]} top10 - 排序后的 Top 10 选题
 * @param {string} dateStr - 日期字符串 YYYYMMDD
 * @returns {string} Markdown 内容
 */
function generateMarkdown(top10, dateStr) {
  const dateDisplay = `${dateStr.slice(0, 4)}-${dateStr.slice(4, 6)}-${dateStr.slice(6, 8)}`;

  // 统计各类目数量
  const catCount = { A: 0, B: 0, C: 0, D: 0, E: 0 };
  for (const item of top10) {
    catCount[item.primaryCat] = (catCount[item.primaryCat] || 0) + 1;
  }

  // 推送数量（用户逻辑：> 10 推 10，≤ 10 全推）
  const sendCount = Math.min(top10.length, 10);
  const starred = top10;  // 全部推送（top10 本身 ≤ 10）

  let md = `# 自媒体素材库 · ${dateDisplay}
文件路径：${TOPICS_DIR}/claude-hub/topics/${dateStr}_topics.md

## 今日总览
- 选题数量：${top10.length} 个（推送 ${sendCount} 个）
- 分布：A 财经 ${catCount.A} / B 房产 ${catCount.B} / C 政策 ${catCount.C} / D AI ${catCount.D} / E 公司 ${catCount.E || 0}
- ⭐ 推送选题：${Array.from({length: sendCount}, (_, i) => `选题 ${i + 1}`).join('、')}
- 工作流提示：每天 04:00 生成 → 用户 10:00 前挑 1-2 个 → 周累计 3 个发布

---

`;

  // 生成每个选题卡片
  top10.forEach((item, idx) => {
    const rank = idx + 1;
    const isStar = rank <= sendCount ? '⭐推送' : '';
    const catName = KEYWORD_DB[item.primaryCat]?.name || '综合';

    // 原始命中关键词描述
    const hitDescs = Object.entries(item.match.rawHit)
      .map(([cat, kws]) => `${cat} ${KEYWORD_DB[cat]?.name}(命中词：${kws.join('、')})`)
      .join('；');

    // 延伸方向
    const extendedDescs = item.match.extended
      .map(c => `${c} ${KEYWORD_DB[c]?.name}`)
      .join('、');

    // 钩子文案（来自 LLM 或兜底），智能截断到 30 字 + 禁用词过滤
    const rawHook = item.hookCopy?.hook || fallbackHookCopy(item).hook;
    const hookCopy = sanitizeForbiddenWords(truncateHook(rawHook, 30));

    // 公众号标题候选，智能截断到 25 字 + 禁用词后处理
    const rawGzhTitles = item.hookCopy?.gzhTitles || [];
    const gzhTitles = rawGzhTitles.map(t => sanitizeForbiddenWords(truncateHook(t, 25)));

    // 格式化热度
    const hotDisplay = item.label || formatHotValue(item.hotValue);

    // 数据点
    const dataPoints = item.dataPoints || [
      { text: '⚠️ 待手动补充', source: '—' },
      { text: '⚠️ 待手动补充', source: '—' },
      { text: '⚠️ 待手动补充', source: '—' }
    ];

    md += `## 选题 ${rank} · ${isStar}
**${item.platform}「${item.text}」${hotDisplay}热度**

- **原始命中**：${hitDescs}
- **延伸方向**：${extendedDescs || '无'}
- **目标平台**：${item.platform}短视频 + 公众号图文

**钩子文案（用户可直接用）**
- ${hookCopy}
${gzhTitles.length > 0 ? gzhTitles.map((t, i) => `  - 公众号候选${i + 1}：${t}`).join('\n') : ''}

**3 个数据点（必填）**
1. ${dataPoints[0]?.text || '⚠️ 待手动补充'}${dataPoints[0]?.source && dataPoints[0]?.source !== '—' ? `（${dataPoints[0].source}）` : ''}
2. ${dataPoints[1]?.text || '⚠️ 待手动补充'}${dataPoints[1]?.source && dataPoints[1]?.source !== '—' ? `（${dataPoints[1].source}）` : ''}
3. ${dataPoints[2]?.text || '⚠️ 待手动补充'}${dataPoints[2]?.source && dataPoints[2]?.source !== '—' ? `（${dataPoints[2].source}）` : ''}

**来源链接**
- ${item.url}

**用户操作**
- 想采用本选题：把下面注释改为 \`<!-- __ADOPTED__: 选题 ${rank} ✓ -->\`
- 不采用：保持注释不变，用户编辑该 .md 文件加备注

<!-- __ADOPTED__: 选题 ${rank} -->
- [ ] 备注修改意见
- [ ] 触发 LLM 写完整公众号长文

---
`;
  });

  // 页脚
  md += `
> 🤖 由 generate_topics.js 自动生成 · ${new Date().toLocaleString('zh-CN')}
> 关键词库版本：${dateStr} · 共 ${Object.keys(KEYWORD_DB).length} 个类目
`;

  return md;
}

// ============================================================
// 7. 主入口
// ============================================================

async function main() {
  const startTime = Date.now();
  console.log('='.repeat(50));
  console.log(`[素材库生成] 开始运行 ${new Date().toLocaleString('zh-CN')}`);
  console.log('='.repeat(50));

  let toutiao = [], weibo = [], bili = [], douyin = [], zhihu = [], kr36 = [];

  try {
    // Step 1: 顺序抓取 4 大平台（避免 AbortController 并行竞争）
    // 1.1 头条
    console.log('[头条] 开始抓取...');
    try {
      toutiao = await fetchToutiaoHot();
      console.log(`[头条] ✓ 抓取成功，获取 ${toutiao.length} 条`);
    } catch (err) {
      console.error(`[头条] ✗ 抓取失败: ${err.message}`);
      toutiao = [];
    }

    // 1.2 微博
    console.log('[微博] 开始抓取...');
    try {
      weibo = await fetchWeiboHot();
      console.log(`[微博] ✓ 抓取成功，获取 ${weibo.length} 条`);
    } catch (err) {
      console.error(`[微博] ✗ 抓取失败: ${err.message}`);
      weibo = [];
    }

    // 1.3 B站
    console.log('[B站] 开始抓取...');
    try {
      bili = await fetchBilibiliHot();
      console.log(`[B站] ✓ 抓取成功，获取 ${bili.length} 条`);
    } catch (err) {
      console.error(`[B站] ✗ 抓取失败: ${err.message}`);
      bili = [];
    }

    // 1.4 抖音
    console.log('[抖音] 开始抓取...');
    try {
      douyin = await fetchDouyinHotAPI();
      console.log(`[抖音] ✓ 抓取成功，获取 ${douyin.length} 条`);
    } catch (err) {
      console.error(`[抖音] ✗ 抓取失败: ${err.message}`);
      douyin = [];
    }

    // 1.5 知乎
    console.log('[知乎] 开始抓取...');
    try {
      zhihu = await fetchZhihuHot();
      console.log(`[知乎] ✓ 抓取成功，获取 ${zhihu.length} 条`);
    } catch (err) {
      console.error(`[知乎] ✗ 抓取失败: ${err.message}`);
      zhihu = [];
    }

    // 1.6 36氪
    console.log('[36氪] 开始抓取...');
    try {
      kr36 = await fetch36krRSS();
      console.log(`[36氪] ✓ 抓取成功，获取 ${kr36.length} 条`);
    } catch (err) {
      console.error(`[36氪] ✗ 抓取失败: ${err.message}`);
      kr36 = [];
    }

    // Step 2: 合并所有数据
    const all = [...toutiao, ...weibo, ...bili, ...douyin, ...zhihu, ...kr36];
    console.log(`\n[合并] 共 ${all.length} 条原始数据`);

    // Step 3: 关键词匹配 + 过滤（只保留有命中的）
    const matched = all.map(item => ({
      ...item,
      flowScore: flowScore(item)
    })).filter(item => item.match.rawCats.length > 0);

    console.log(`[匹配] 关键词命中 ${matched.length} 条`);

    // Step 4: 按流量分降序排序
    matched.sort((a, b) => b.flowScore - a.flowScore);

    // Step 5: 取 Top 10
    const top10 = matched.slice(0, 10);

    if (top10.length === 0) {
      console.error('[错误] 没有匹配到任何选题，请检查关键词库和网络连接');
      process.exit(1);
    }

    // Step 6: 生成钩子文案（LLM）+ 数据点补充（LLM）
    for (const item of top10) {
      const [hookResult, dataPoints] = await Promise.all([
        generateHookCopy(item),
        generateDataPoints(item)
      ]);
      item.hookCopy = hookResult;
      item.dataPoints = dataPoints;
    }

    // Step 7: 生成 Markdown（使用北京时间）
    const dateStr = new Date().toLocaleString('en-CA', {
      timeZone: 'Asia/Shanghai',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    }).replace(/-/g, '');
    const md = generateMarkdown(top10, dateStr);

    // Step 8: 写入文件
    const outPath = path.join(TOPICS_DIR, `${dateStr}_topics.md`);
    fs.writeFileSync(outPath, md, 'utf-8');

    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
    console.log(`\n[完成] 生成文件: ${outPath}`);
    console.log(`[完成] 文件大小: ${md.length} 字节`);
    console.log(`[完成] 耗时: ${elapsed}s`);
    console.log(`[完成] 选题数: ${top10.length} 个`);

  } catch (err) {
    console.error('[致命错误]', err);
    process.exit(1);
  }
}

// 直接运行（node generate_topics.js）
main();
