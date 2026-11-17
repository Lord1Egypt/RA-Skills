#!/usr/bin/env node
// xhs-account-analyst：分析用户自己的小红书账号运营表现。
// 数据源：创作者后台官方数据看板（导出 Excel，官方口径为准）+ 小红书公开搜索结果（竞对仅用公开可见的标题/作者/点赞数）。
// 产出：HTML 报告（①数据总表 ②转化漏斗健康度诊断 ③逐条笔记的对标爆款表 + 3 条改进动作）。
//
// 架构（编排器）：确定性操作全部写代码（开 tab、点导出、page.eval 提取卡片、Excel 解析、
// 漏斗计算、HTML 渲染）；需要"理解"的 3 类任务交给 wc3-code.mjs 子会话（关键词提炼/对标爆款筛选/改进动作生成）。
// 浏览器操作只走 Extension Relay HTTP API（:3459），不使用其他浏览器自动化通道。
import { readFileSync, writeFileSync, mkdirSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { tmpdir, homedir } from 'node:os';
import { spawn } from 'node:child_process';

// ============ 常量 ============
const RELAY_URL = 'http://127.0.0.1:3459';
const CLI_DIR = import.meta.dirname;
const WC3_CODE = join(CLI_DIR, 'wc3-code.mjs'); // 子会话统一经本地 pipeline 服务代跑（skill 不直接 spawn CLI）
const TMP = join(tmpdir(), 'skill-run-' + process.pid);

const CREATOR_URL = 'https://creator.xiaohongshu.com/statistics/data-analysis';
const HOME_URL = 'https://www.xiaohongshu.com/';

// 时序常量（来自 explore 成功路径）
const SPA_WAIT_MS = 6000;        // tab.create 后等 SPA 渲染（url/title 为空是正常的）
const POLL_STEP_MS = 1500;       // 轮询步长
const EXPORT_POLL_MS = 12000;    // 等「导出数据」按钮出现
const EXPORT_DOWNLOAD_MS = 6000; // 点击导出后等浏览器下载完成
const SEARCH_NAV_POLL_MS = 20000;// 回车后等进入搜索结果页（title/url 信号，见陷阱：URL 不会立刻变）
const CARD_POLL_MS = 15000;      // 滚动后等卡片懒加载到齐
const BETWEEN_SEARCH_MS = 4000;  // 关键词间访问节奏控制
const CONCURRENCY = 2;           // 子会话并发上限（防限流/超时）
const MIN_CARDS = 8;             // 单关键词可接受的最低卡片数（不足则整词重试一次）
const MAX_CARDS_PER_NOTE = 60;   // 提交给子会话的卡片上限（控制 prompt 体积）

// 漏斗阈值（explore 验证口径，历史探索轮沉淀）
const CTR_OK_MIN = 0.10, CTR_OK_MAX = 0.20;
const INTERACT_HOT = 0.05, INTERACT_OK = 0.03; // 互动率 5%-10% 爆款线，>=3% 合格
const FAN_BREAK = 0.01;          // 涨粉率 <1% 记断档

// 留存断档阈值按笔记类型分设（v1.1.0 修正）：图文以「读完」为主，停留天然短于视频，
// 用同一把 10s 尺子会把正常图文误判成断档。
const RETENTION_BREAK_S_VIDEO = 10;  // 视频人均观看 <10s 记断档
const RETENTION_BREAK_S_IMAGE = 5;   // 图文人均观看 <5s 记断档
const RETENTION_BREAK_S = RETENTION_BREAK_S_VIDEO; // 体裁未识别时的兜底口径

// 对标爆款门槛（v1.1.0 新增）：低赞笔记不配进对标表，宁缺毋滥。
const BENCH_MIN_LIKES = 1000;    // 绝对门槛：低于 1000 赞一律不算爆款
const BENCH_MEDIAN_MULT = 3;     // 相对门槛：需达到该关键词结果集点赞中位数的 3 倍
const BENCH_MAX_LIKES_FLOOR = 3000; // 相对门槛上限：中位数极高时不至于把门槛推到无解

// ============ 基础工具 ============
const sleep = ms => new Promise(r => setTimeout(r, ms));

// Extension Relay HTTP API 封装（端口 3459）
async function relayCall(op, params = {}, timeout = 30000) {
  const res = await fetch(`${RELAY_URL}/api/call`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ op, params, timeout }),
  });
  const data = await res.json();
  if (data.error) throw new Error(data.error);
  return data.result;
}

// 本 skill 的浏览器运行时由 webclaw3 提供，是硬依赖。运行时失败必须自带修复路径：
// 平台没有 skill 间依赖机制，装本 skill 时不会自动装上 webclaw3，所以报错里必须点名 webclaw3
// 并给出安装命令，否则用户只看到一个陌生端口号，无从下手。
const WEBCLAW3_INSTALL_CMD = 'npx clawhub@latest install fatmind/webclaw3-browser-automation';
const WEBCLAW3_SKILL_URL = 'https://clawhub.ai/fatmind/skills/webclaw3-browser-automation';
const WEBCLAW3_REPO_URL = 'https://github.com/fatmind/webclaw3';

// 两种失败原因完全不同，修复动作也不同，不能合并成一条报错：
// ① relay 连不上   → webclaw3 没装，或 relay 没启动（第一层依赖：一条命令可解决）
// ② relay 通但扩展未连 → webclaw3 装了但 Chrome 扩展没加载 / Access Key 没配（第二层：webclaw3 自身首次配置）
async function ensureRelay() {
  let status;
  try {
    status = await (await fetch(`${RELAY_URL}/api/status`)).json();
  } catch (e) {
    throw new Error(
      `本 skill 需要 webclaw3 提供的浏览器运行时，但 ${RELAY_URL} 连不上（${e.message}）。\n` +
      `\n原因：webclaw3 没有安装，或它的 relay 没有启动。本 skill 无法独立运行——安装本 skill 时不会自动装上 webclaw3，需要单独装一次。\n` +
      `\n修复：\n` +
      `  1. 安装 webclaw3：${WEBCLAW3_INSTALL_CMD}\n` +
      `  2. 装好后对 Agent 说「检查 webclaw3 环境」，它会启动 relay 并校验配置\n` +
      `  3. 回来重跑本 skill\n` +
      `\n主品页面：${WEBCLAW3_SKILL_URL}\n安装指南（3 步，约 5 分钟）：${WEBCLAW3_REPO_URL}`
    );
  }
  if (!status.extensionConnected) {
    throw new Error(
      `webclaw3 的 relay 已在 ${RELAY_URL} 运行，但 Chrome 扩展没有连上，浏览器操作无法执行。\n` +
      `\n原因：webclaw3 的 Chrome 扩展没有加载（需在 chrome://extensions 开启开发者模式后手动加载），或 Access Key 没有配置。这是 webclaw3 自身的首次配置，只需做一次。\n` +
      `\n修复：对 Agent 说「检查 webclaw3 环境」，它会给出扩展加载与 Access Key 的具体步骤。\n` +
      `\n安装指南：${WEBCLAW3_REPO_URL}`
    );
  }
}

// 执行页面 JS 并解析返回值（page.eval 返回 JSON 字符串）。Extension 偶发 disconnected：
// 等 8-10s 让扩展自动重连后重试一次即可恢复（explore 实测 2 次均一次重试成功）。
async function evalJson(tabId, code, retries = 2) {
  for (let i = 0; i < retries; i++) {
    try {
      const raw = await relayCall('page.eval', { tabId, code });
      if (raw && typeof raw === 'object') return raw;
      try { return JSON.parse(raw); } catch (e) { return { err: String(raw) }; }
    } catch (e) {
      if (i < retries - 1) { console.error(`[eval] 第 ${i + 1} 次重试:`, e.message); await sleep(9000); }
      else return { err: String(e && e.message || e) };
    }
  }
}

// 带并发上限的批量执行（返回值格式与 Promise.allSettled 相同）
async function pMap(items, fn, { concurrency = CONCURRENCY } = {}) {
  const results = new Array(items.length);
  let idx = 0;
  const workers = Array.from({ length: Math.min(concurrency, items.length) }, async () => {
    while (idx < items.length) {
      const i = idx++;
      try { results[i] = { status: 'fulfilled', value: await fn(items[i], i) }; }
      catch (e) { results[i] = { status: 'rejected', reason: e }; }
    }
  });
  await Promise.all(workers);
  return results;
}

// tab 管理：只关自建 tab，用户原有 tab 不动
const createdTabs = new Set();
let GROUP_ID = null;             // 本任务 tab 分组（多任务并行隔离：建组 → tab 全进组 → 结束整组关闭）
function track(tab) { if (tab && tab.id) createdTabs.add(tab.id); return tab; }
async function closeTab(id) {
  if (!id || !createdTabs.has(id)) return;
  try { await relayCall('tab.close', { tabId: id }); } catch (e) { console.error('close tab fail:', id, e.message); }
  createdTabs.delete(id);
}
async function closeAllTabs() {
  for (const id of [...createdTabs]) await closeTab(id);
}

// ============ 子会话（wc3-code.mjs，经本地 pipeline 服务代跑）============
function callClaudeWithFile(promptContent, promptFile, outputFile, opts = {}) {
  writeFileSync(promptFile, promptContent, 'utf-8');
  return new Promise((resolve, reject) => {
    const args = ['--prompt-file', promptFile, '--output', outputFile];
    if (opts.timeout) args.push('--timeout', String(opts.timeout));
    if (opts.schema) args.push('--schema', opts.schema);
    const child = spawn('node', [WC3_CODE, ...args], { stdio: ['ignore', 'ignore', 'pipe'] });
    let stderr = '';
    child.stderr.on('data', d => { stderr += d; });
    child.on('close', code => {
      if (code !== 0) {
        const detail = stderr.slice(0, 500);
        // 子会话经 webclaw3 的本地 pipeline 服务（:3460）代跑。连不上时原始报错只说
        // 「无法连接 serve」，同样不点名 webclaw3，这里补成自带修复路径的文案。
        if (/无法连接\s*serve|ECONNREFUSED|fetch failed|3460/.test(detail)) {
          return reject(new Error(
            `本 skill 的分析环节需要 webclaw3 提供的本地 pipeline 服务（:3460），但连不上。\n` +
            `\n原因：webclaw3 没有安装，或它的 pipeline 服务没有启动。\n` +
            `\n修复：\n` +
            `  1. 安装 webclaw3：${WEBCLAW3_INSTALL_CMD}\n` +
            `  2. 对 Agent 说「检查 webclaw3 环境」，它会拉起 relay 与 pipeline\n` +
            `  3. 回来重跑本 skill\n` +
            `\n主品页面：${WEBCLAW3_SKILL_URL}\n` +
            `\n原始报错：${detail}`
          ));
        }
        return reject(new Error(`wc3-code exit ${code}: ${detail}`));
      }
      try { resolve(JSON.parse(readFileSync(outputFile, 'utf-8'))); }
      catch { resolve(readFileSync(outputFile, 'utf-8')); }
    });
    child.on('error', reject);
  });
}

let subsessionSeq = 0;
async function runSubsession(promptContent, schema, tag) {
  const n = subsessionSeq++;
  // --schema 必须传 JSON Schema 文件路径（先写临时文件），禁止传内联 JSON 字符串
  const schemaFile = join(TMP, `${tag}-${n}-schema.json`);
  const promptFile = join(TMP, `${tag}-${n}-prompt.md`);
  const outFile = join(TMP, `${tag}-${n}-out.json`);
  writeFileSync(schemaFile, JSON.stringify(schema), 'utf-8');
  console.error(`[subsession] ${tag} 调用中...`);
  return await callClaudeWithFile(promptContent, promptFile, outFile, { schema: schemaFile });
}

// 子会话返回结构不稳定：先解 `result` 包裹层（可能是字符串化 JSON），再取值
function resolveObj(res) {
  let cur = res;
  for (let i = 0; i < 3; i++) {
    if (typeof cur === 'string') { try { cur = JSON.parse(cur); } catch (e) { return cur; } }
    if (cur && typeof cur === 'object' && !Array.isArray(cur) && 'result' in cur) { cur = cur.result; continue; }
    break;
  }
  return cur;
}
function getField(res, field) {
  const o = resolveObj(res);
  if (o && typeof o === 'object' && !Array.isArray(o)) return o[field];
  return undefined;
}
function getArray(res, field) { const v = getField(res, field); return Array.isArray(v) ? v : []; }
function getBool(res, field, def) {
  const v = getField(res, field);
  if (v === true || v === 'true' || v === 1 || v === '1') return true;
  if (v === false || v === 'false' || v === 0 || v === '0') return false;
  return def;
}
function getNum(res, field, def) {
  const v = getField(res, field);
  const n = Number(v);
  return Number.isFinite(n) ? n : def;
}
function getStr(res, field, def = '') {
  const v = getField(res, field);
  return v == null ? def : String(v);
}

// ============ 子会话 Schema（本地校验器只支持单 type；LLM 永远返回对象、禁止裸 null）============
const KEYWORD_SCHEMA = {
  type: 'object',
  properties: {
    keywords: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          // 注意：本地校验器用 typeof 比较类型，JS 数字一律是 "number"，写 'integer' 必校验失败
          index: { type: 'number' },
          title: { type: 'string' },
          keywords: { type: 'array', items: { type: 'string' } },
        },
        required: ['index', 'title', 'keywords'],
      },
    },
  },
  required: ['keywords'],
};

const BENCH_SCHEMA = {
  type: 'object',
  properties: {
    benchmarks: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          title: { type: 'string' },
          author: { type: 'string' },
          likes: { type: 'string' },
        },
        required: ['title', 'author', 'likes'],
      },
    },
    enough: { type: 'boolean' },
    actual_count: { type: 'number' },
    reason: { type: 'string' },
  },
  required: ['benchmarks', 'enough', 'actual_count', 'reason'],
};

const ACTION_SCHEMA = {
  type: 'object',
  properties: {
    actions: { type: 'array', items: { type: 'string' } },
  },
  required: ['actions'],
};

function normalizeKeywords(res) {
  const out = [];
  for (const it of getArray(res, 'keywords')) {
    if (!it || typeof it !== 'object') continue;
    const kws = (Array.isArray(it.keywords) ? it.keywords : []).map(k => String(k).trim()).filter(Boolean);
    if (!kws.length) continue;
    out.push({ index: Number(it.index), title: String(it.title || '').trim(), keywords: kws });
  }
  return out;
}
function normalizeBenchmarks(res, likesFloor = BENCH_MIN_LIKES) {
  const raw = getArray(res, 'benchmarks')
    .filter(b => b && typeof b === 'object' && b.title)
    .map(b => ({
      title: String(b.title).trim(),
      author: String(b.author || '').trim(),
      likes: String(b.likes || '').trim(),
      likes_num: parseLikes(b.likes),
    }));
  // 质量门槛（v1.1.0）：子会话为了凑满 3 条会把低赞笔记也塞进来（实测出现过 63 赞与 4494 赞同表），
  // 在代码侧硬过滤，宁缺毋滥——达不到门槛就记 partial，不许凑数。
  const kept = raw.filter(b => b.likes_num >= likesFloor);
  const benchmarks = kept.slice(0, 3).map(b => ({ title: b.title, author: b.author, likes: b.likes }));
  const dropped = raw.length - kept.length;
  // enough 判定以「过滤后可展示的对标行数」为准：不足 3 条记 partial
  const actual = benchmarks.length;
  const enough = benchmarks.length >= 3 && getBool(res, 'enough', true);
  let reason = getStr(res, 'reason');
  if (dropped > 0) {
    reason = `已按爆款门槛（≥${likesFloor} 赞）剔除 ${dropped} 条低赞笔记` + (reason ? `；子会话说明：${reason}` : '');
  }
  return { benchmarks, enough, actual_count: actual, reason, likes_floor: likesFloor, dropped };
}
function normalizeActions(res) {
  return getArray(res, 'actions').map(a => String(a).trim()).filter(Boolean).slice(0, 3);
}

// ============ 子会话 prompt ============
function buildKeywordPrompt(batch, kwPerNote) {
  return `你是小红书运营分析助手。以下是从创作者后台导出的笔记标题列表。为每条笔记提炼 ${kwPerNote} 个精准的小红书搜索关键词。
用途：这些关键词将用于在小红书搜索「相似爆款笔记」作对标分析，必须精准、可搜索、能有真实结果。
要求：
- 优先用产品名/工具名/话题核心词（例如「AI 写代码」「浏览器自动化」这类），避免口语化、故事化、悬念式表述。
- 不能过宽（如「AI」「工具」），过宽会混入大量无关内容；也不能过窄到没有搜索结果。
- 从笔记标题推断账号的内容主题，保证关键词与账号定位一致。
笔记列表（含 index，index 必须原样回传）：
${JSON.stringify(batch.map((n, i) => ({ index: i, title: n.title })))}
输出 ONLY JSON（无其他文字，无 markdown 代码围栏），格式：
{"keywords":[{"index":<对应输入 index>,"title":"<该笔记原标题，与输入完全一致>","keywords":["关键词1",...]}]}`;
}

// 爆款门槛按该关键词结果集的点赞中位数动态定档：不同赛道的"爆款"绝对值差异极大
//（美妆万赞起步、垂类工具千赞已是头部），只用固定值会一刀切。
function computeLikesFloor(cards) {
  const nums = cards.map(c => parseLikes(c.likes)).filter(n => n > 0).sort((a, b) => a - b);
  if (!nums.length) return BENCH_MIN_LIKES;
  const mid = nums.length % 2 ? nums[(nums.length - 1) / 2] : Math.round((nums[nums.length / 2 - 1] + nums[nums.length / 2]) / 2);
  const dynamic = mid * BENCH_MEDIAN_MULT;
  return Math.max(BENCH_MIN_LIKES, Math.min(BENCH_MAX_LIKES_FLOOR, dynamic));
}

function buildBenchmarkPrompt(note, keywords, cards, ownNickname, likesFloor) {
  const cardList = cards.slice(0, MAX_CARDS_PER_NOTE).map((c, i) => ({
    i, title: c.title, author: c.author, likes: c.likes, likes_num: parseLikes(c.likes),
  }));
  const nicknameRule = ownNickname
    ? `\n- 剔除作者等于本账号昵称「${ownNickname}」的笔记（本账号自己的笔记，不作对标）。`
    : `\n- 若搜索结果中出现标题与本笔记完全相同的条目，视为本账号自己的笔记，剔除。`;
  return `你是小红书运营分析助手。账号的一条笔记标题为「${note.title}」，为此笔记搜索了以下关键词：${keywords.join('、')}，得到以下搜索结果卡片（均为搜索结果页公开可见的标题/作者/点赞数）。
请筛选出与该笔记【题材+视角】最相似的爆款笔记作为对标。
视角类型例如：实测/使用体验、清单/合集、横评/对比、教程/攻略、血泪教训/避坑、测评、案例分享等。
筛选规则：
- 【硬门槛】只有 likes_num >= ${likesFloor} 的卡片才算"爆款"，低于此值的一律不得入选（本关键词结果集点赞中位数换算而来）。
- 按「题材/视角相似度」优先，点赞数作佐证（相似度相同时点赞高者优先）。
- 剔除与本笔记题材无关的混入内容（关键词过宽常混入榜单、新闻、其他领域内容）。${nicknameRule}
- 【宁缺毋滥】最多返回 3 条；同时满足门槛与相似度的不足 3 条时，如实只返回合格的条目并说明原因（如关键词过宽混入无关内容、该词下无高赞同题材笔记），**严禁用低赞或不相关笔记凑满 3 条**。
搜索结果卡片（JSON）：
${JSON.stringify(cardList)}
输出 ONLY JSON（无其他文字，无 markdown 代码围栏），格式：
{"benchmarks":[{"title":"爆款标题","author":"作者","likes":"点赞数原文"}],"enough":true或false,"actual_count":<实际合格条数>,"reason":"不足 3 条时的原因说明；充足时给一句话总结"}`;
}

function buildActionPrompt(note, benchmarks) {
  const type = noteType(note);
  const floor = retentionFloor(note);
  return `你是小红书运营分析师。请基于一条笔记的官方数据与对标爆款，为该笔记生成 3 条【具体可执行】的改进动作。
本笔记官方数据（创作者后台导出）：
${JSON.stringify({
    title: note.title, note_type: type, publish_time: note.publish_time,
    days_since_publish: daysSince(note.publish_time),
    exposure: note.exposure, exposure_per_day: perDay(note.exposure, note.publish_time),
    views: note.views, ctr_pct: (note.ctr * 100).toFixed(1) + '%', likes: note.likes, comments: note.comments,
    collects: note.collects, fans: note.fans, shares: note.shares, avg_watch_sec: note.avg_watch_sec,
    retention_break_sec: floor,
  })}
对标爆款（同题材高赞笔记，可能少于 3 条）：
${JSON.stringify(benchmarks)}
要求：
- 3 条动作必须具体可执行：给出标题改写示例句、封面/首段钩子写法、正文结构调整、收藏/评论引导话术等，禁止概念性泛泛建议。
- 针对本笔记数据弱点对症下药：点击率低→封面与标题；人均观看低于本体裁断档线（${type} 为 ${floor}s）→首段 3 秒钩子；无收藏→收藏引导；无评论→评论钩子等。
- 注意体裁差异：图文的"留存"是读完率，靠首图信息量与分段排版；视频靠前 3 秒画面与口播节奏。建议须与 ${type} 这一体裁匹配。
- 曝光要看 exposure_per_day（日均曝光）而不是曝光总量，老笔记曝光总量天然更高。
- 每条 60-150 字，中文。
输出 ONLY JSON（无其他文字，无 markdown 代码围栏），格式：
{"actions":["动作1","动作2","动作3"]}`;
}

// ============ 页面操作 JS 片段（全部单行，禁止在 eval 代码里写 \n 字面量）============
const JS_CREATOR_SNIPPET = 'JSON.stringify({url: location.href, title: document.title, bodySnippet: document.body.innerText.slice(0, 500)})';
// 导出按钮：叶子节点文本匹配（explore 实测为 span）
const JS_CLICK_EXPORT = '(function(){var els=[...document.querySelectorAll("button,span,div,a")];var t=els.find(function(e){return e.children.length===0 && /导出数据/.test(e.textContent||"")});if(!t)return JSON.stringify({found:false});t.click();return JSON.stringify({found:true,tag:t.tagName,text:t.textContent.trim()});})()';
const JS_HAS_TEXTAREA = 'JSON.stringify({hasBox: !!document.querySelector("textarea[name=aiSearchTextarea]")})';
const JS_SEARCH_STATE = 'JSON.stringify({url: location.href, title: document.title})';
// 输入是否被页面接受：任一可见 textarea 的 value 非空即算接受（Vue 组件会重置未被接受的输入为空）
const JS_CHECK_INPUT_VALUE = '(function(){var tas=[...document.querySelectorAll("textarea[name=aiSearchTextarea]")];for(var i=0;i<tas.length;i++){var r=tas[i].getBoundingClientRect();if(r.width>0&&r.height>0&&tas[i].value&&tas[i].value.length>0){return JSON.stringify({accepted:true});}}return JSON.stringify({accepted:false});})()';
const JS_SCROLL = 'window.scrollTo(0, document.body.scrollHeight); window.scrollBy(0, -200); setTimeout(function(){window.scrollTo(0, document.body.scrollHeight);}, 800); "scrolled"';
// 卡片提取：id 为空的行（"大家都在搜"/广告占位）必须过滤，否则脏数据进下游
const JS_EXTRACT_CARDS = '(function(){var cards=document.querySelectorAll("section.note-item");var out=[];for(var i=0;i<cards.length;i++){var c=cards[i];var id=c.getAttribute("data-note-id");if(!id)continue;var a=c.querySelector("a.cover.mask")||c.querySelector("a[href*=xsec_token]");var titleEl=c.querySelector(".title");var nameEl=c.querySelector(".author .name");var likeEl=c.querySelector(".like-wrapper .count");out.push({id:id,title:titleEl?titleEl.textContent.trim():"",author:nameEl?nameEl.textContent.trim():"",likes:likeEl?likeEl.textContent.trim():"",href:a?a.getAttribute("href"):""});}return JSON.stringify({count:cards.length, cards:out});})()';

// 受控输入组件：直接 el.value= 无效，必须 prototype value setter + input 事件 + Enter
//（首页搜索框原为 React，2026-08 改版为 Vue v-model；两者都靠该通用方式尝试触发）
function buildSearchInputJs(keyword) {
  const kw = JSON.stringify(keyword);
  return `(function(){var tas=[...document.querySelectorAll("textarea[name=aiSearchTextarea]")];var ta=tas.find(function(t){var r=t.getBoundingClientRect();return r.width>0&&r.height>0;})||tas[0];if(!ta)return JSON.stringify({ok:false,reason:"no textarea"});var proto=HTMLTextAreaElement.prototype;var desc=Object.getOwnPropertyDescriptor(proto,"value");desc.set.call(ta,${kw});ta.dispatchEvent(new InputEvent("input",{bubbles:true,inputType:"insertText",data:${kw}}));ta.dispatchEvent(new Event("change",{bubbles:true}));ta.focus();ta.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",code:"Enter",keyCode:13,which:13,bubbles:true}));ta.dispatchEvent(new KeyboardEvent("keyup",{key:"Enter",code:"Enter",keyCode:13,which:13,bubbles:true}));return JSON.stringify({ok:true,value:ta.value});})()`;
}

// ============ Excel 解析（本地 Python + openpyxl，非浏览器）============
// xlsx 是 zip+XML，Node 无内置解析；explore 验证 openpyxl 可用。脚本写入 TMP，不污染包目录。
const PY_XLSX_PARSE = String.raw`# -*- coding: utf-8 -*-
import json, re, sys, datetime
import openpyxl
path = sys.argv[1]
wb = openpyxl.load_workbook(path, data_only=True)
ws = wb[wb.sheetnames[0]]
rows = list(ws.iter_rows(values_only=True))
header_idx = None
for i, r in enumerate(rows[:5]):
    if r and any(c is not None and '笔记标题' in str(c) for c in r):
        header_idx = i
        break
if header_idx is None:
    print(json.dumps({'error': 'header not found'}, ensure_ascii=False)); sys.exit(1)
header = [str(c) if c is not None else '' for c in rows[header_idx]]
def col(name):
    for j, h in enumerate(header):
        if name in h:
            return j
    return -1
def num(v):
    if v is None: return 0
    if isinstance(v, (int, float)): return int(v)
    s = str(v).strip().replace(',', '').replace('%', '')
    try: return int(float(s))
    except Exception: return 0
def ctr_val(v):
    if v is None: return 0.0
    if isinstance(v, (int, float)): return float(v)
    s = str(v).strip().replace('%', '')
    try:
        f = float(s)
        return f / 100.0 if f > 1 else f
    except Exception: return 0.0
def pub_time(v):
    if v is None: return ''
    if isinstance(v, datetime.datetime): return v.strftime('%Y-%m-%d %H:%M:%S')
    s = str(v).strip()
    m = re.search(r'(\d{4})年(\d{2})月(\d{2})日(\d{2})时(\d{2})分(\d{2})秒', s)
    if m:
        y, mo, d, h, mi, se = m.groups()
        return '%s-%s-%s %s:%s:%s' % (y, mo, d, h, mi, se)
    m2 = re.search(r'(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})[ T](\d{1,2}):(\d{1,2})(?::(\d{1,2}))?', s)
    if m2:
        y, mo, d, h, mi, se = m2.groups(); se = se or '00'
        return '%04d-%02d-%02d %02d:%02d:%02d' % (int(y), int(mo), int(d), int(h), int(mi), int(se))
    return s
notes = []
for r in rows[header_idx + 1:]:
    if not r or all(c is None or str(c).strip() == '' for c in r):
        continue
    def g(name):
        j = col(name)
        return r[j] if j >= 0 and j < len(r) else None
    title = str(g('笔记标题') or '').strip()
    if not title:
        continue
    notes.append({
        'title': title,
        'publish_time': pub_time(g('首次发布')),
        'genre': str(g('体裁') or '').strip(),
        'exposure': num(g('曝光')),
        'views': num(g('观看')),
        'ctr': ctr_val(g('封面点击率')),
        'likes': num(g('点赞')),
        'comments': num(g('评论')),
        'collects': num(g('收藏')),
        'fans': num(g('涨粉')),
        'shares': num(g('分享')),
        'avg_watch_sec': num(g('人均观看时长')),
        'danmaku': num(g('弹幕')),
    })
print(json.dumps(notes, ensure_ascii=False))
`;

function runPython(script, args) {
  return new Promise((resolve, reject) => {
    // 为什么 stdio 是 ['ignore','pipe','pipe']：必须 'pipe' 捕获 stdout，否则 child.stdout 为 null，
    // child.stdout.on 会抛 TypeError（上一版把 stdout 配成 'ignore' 导致 Excel 解析崩溃）
    const child = spawn('python3', [script, ...args], { stdio: ['ignore', 'pipe', 'pipe'] });
    let out = '', err = '';
    child.stdout.on('data', d => { out += d; });
    child.stderr.on('data', d => { err += d; });
    child.on('close', code => {
      if (code !== 0) return reject(new Error('python exit ' + code + ': ' + err.slice(0, 300)));
      try { resolve(JSON.parse(out)); } catch (e) { reject(new Error('python output parse fail: ' + out.slice(0, 200))); }
    });
    child.on('error', reject);
  });
}

// 找 ~/Downloads 下的导出 Excel（同名已存在时 Chrome 会带 " (1)" 后缀）
function listExcelFiles() {
  const dl = join(homedir(), 'Downloads');
  try {
    return readdirSync(dl)
      .filter(f => /^笔记列表明细表.*\.xlsx$/.test(f))
      .map(f => { const full = join(dl, f); let m = 0; try { m = statSync(full).mtimeMs; } catch (e) { /* ignore */ } return { name: f, full, mtime: m }; })
      .sort((a, b) => b.mtime - a.mtime);
  } catch (e) { return []; }
}

// ============ 步骤 1-4：创作者后台导出 + 解析 ============
// 创作者后台页面展示口径与 Excel 可能不同，最终以 Excel 导出值为准（explore 实测存在差异）
async function exportNotesFromCreator() {
  const tab = track(await relayCall('tab.create', { url: CREATOR_URL, active: false, groupId: GROUP_ID }));
  try {
    await sleep(SPA_WAIT_MS);
    // 轮询等「导出数据」按钮出现（含"导出数据"字样即视为已登录且有数据）
    const deadline = Date.now() + EXPORT_POLL_MS;
    let snippet = '';
    while (Date.now() < deadline) {
      const st = await evalJson(tab.id, JS_CREATOR_SNIPPET);
      snippet = (st && st.bodySnippet) || '';
      if (snippet.includes('导出数据')) break;
      await sleep(POLL_STEP_MS);
    }
    if (!snippet.includes('导出数据')) {
      throw new Error('创作者后台未检测到「导出数据」按钮（可能未登录或账号无数据），页面片段: ' + snippet.slice(0, 200));
    }
    // 账号昵称在"创作服务平台"下一行（用于剔除本账号自己的笔记）
    const m = snippet.match(/创作服务平台\s*\n\s*([^\n]+)/);
    const nickname = m ? m[1].trim() : '';

    // 记录导出前已有文件的最新 mtime，点导出后只认比它新的文件
    const before = listExcelFiles();
    const baseline = before.length ? before[0].mtime : 0;

    const clickRes = await evalJson(tab.id, JS_CLICK_EXPORT);
    if (!clickRes || !clickRes.found) throw new Error('「导出数据」按钮点击失败');
    console.error(`[export] 已点击导出（${clickRes.text || ''}），等待下载...`);
    await sleep(EXPORT_DOWNLOAD_MS);

    const after = listExcelFiles();
    const fresh = after.find(f => f.mtime > baseline);
    if (!fresh) throw new Error('导出 Excel 未下载到 ~/Downloads（检查浏览器下载目录）');
    return { nickname, excelPath: fresh.full };
  } finally {
    await closeTab(tab.id);
  }
}

async function parseNotesExcel(excelPath) {
  const pyFile = join(TMP, 'xlsx_parse.py');
  writeFileSync(pyFile, PY_XLSX_PARSE, 'utf-8');
  const notes = await runPython(pyFile, [excelPath]);
  if (!Array.isArray(notes)) throw new Error('Excel 解析失败: ' + JSON.stringify(notes).slice(0, 200));
  return notes;
}

// ============ 步骤 6-9：关键词搜索（真人路径优先，搜索页直连兜底）============
// 为什么保留两条路径：explore 时首页搜索框「真人输入+回车」可触发导航；但该输入框是 Vue 组件，
// 站点改版后合成 input/keydown 事件不再被 v-model 接受（value 被重置、回车不导航），
// 实测 2026-08 首页输入路径时好时坏，而直接导航 search_result_ai 可稳定返回 40+ 卡片，
// 故真人路径失败时回退到搜索页直连（primer 提示直连易触发访问限制，因此只作兜底、不作首选）。
async function waitForTextarea(tabId, deadlineMs) {
  const deadline = Date.now() + deadlineMs;
  while (Date.now() < deadline) {
    const st = await evalJson(tabId, JS_HAS_TEXTAREA);
    if (st && st.hasBox) return { ok: true };
    await sleep(POLL_STEP_MS);
  }
  return { ok: false };
}

// 搜索成功判定：以 title 含「 - 小红书搜索」或 URL 含 search_result 为准。
// 陷阱：回车后 6s 内 URL 仍是 /explore、首屏 30 张 note-item 是首页信息流，不能据此判定。
async function waitForSearch(tabId, deadlineMs) {
  const deadline = Date.now() + deadlineMs;
  while (Date.now() < deadline) {
    const st = await evalJson(tabId, JS_SEARCH_STATE);
    const title = (st && st.title) || '';
    const url = (st && st.url) || '';
    if (title.includes('小红书搜索') || url.includes('search_result')) return { ok: true };
    await sleep(POLL_STEP_MS);
  }
  return { ok: false };
}

// 滚动触发懒加载 + 轮询到卡片到齐（保留历史最大值，避免抖动后取到更少）
async function pollCards(tabId, deadlineMs) {
  const deadline = Date.now() + deadlineMs;
  let best = [];
  while (Date.now() < deadline) {
    try { await evalJson(tabId, JS_SCROLL); } catch (e) { /* 忽略 */ }
    await sleep(2000);
    const res = await evalJson(tabId, JS_EXTRACT_CARDS);
    const cards = (res && Array.isArray(res.cards)) ? res.cards : [];
    if (cards.length > best.length) best = cards;
    if (best.length >= MIN_CARDS) break;
  }
  return best;
}

// 路径 A：首页搜索框真人输入 + 回车（explore 验证路径；站点改版后可能不触发导航）
async function searchViaHomeInput(keyword) {
  const tab = track(await relayCall('tab.create', { url: HOME_URL, active: false, groupId: GROUP_ID }));
  try {
    const ta = await waitForTextarea(tab.id, 10000);
    if (!ta.ok) return [];
    await sleep(1500);
    const inputRes = await evalJson(tab.id, buildSearchInputJs(keyword));
    if (!inputRes || inputRes.err || !inputRes.ok) return [];
    // 快速失败：Vue 组件会把未被接受的输入重置为空。输入 2s 后 value 仍为空 → 本路径不可用，
    // 直接返回空让上层走搜索页直连，避免白等 20s 导航超时。
    await sleep(2000);
    const val = await evalJson(tab.id, JS_CHECK_INPUT_VALUE);
    if (!(val && val.accepted)) {
      console.error(`[search] 「${keyword}」输入未被页面接受（Vue 重置），放弃首页路径`);
      return [];
    }
    const nav = await waitForSearch(tab.id, SEARCH_NAV_POLL_MS);
    if (!nav.ok) return [];
    return await pollCards(tab.id, CARD_POLL_MS);
  } finally {
    await closeTab(tab.id);
  }
}

// 路径 B：直接导航 AI 搜索页（2026-08 实测稳定返回 40+ 卡片）
async function searchViaDirectUrl(keyword) {
  const url = 'https://www.xiaohongshu.com/search_result_ai?keyword=' + encodeURIComponent(keyword);
  const tab = track(await relayCall('tab.create', { url, active: false, groupId: GROUP_ID }));
  try {
    const nav = await waitForSearch(tab.id, SEARCH_NAV_POLL_MS);
    if (!nav.ok) return [];
    return await pollCards(tab.id, CARD_POLL_MS);
  } finally {
    await closeTab(tab.id);
  }
}

async function searchKeyword(keyword) {
  const cards = await searchViaHomeInput(keyword);
  if (cards && cards.length) return cards;
  console.error(`[search] 「${keyword}」真人输入路径无结果，改用搜索页直连`);
  return await searchViaDirectUrl(keyword);
}

// 单次失败重试一次（吸收 Extension 偶发断开 / SPA 加载慢）
async function searchKeywordWithRetry(keyword) {
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const cards = await searchKeyword(keyword);
      if (cards.length) return cards;
      throw new Error('cards empty');
    } catch (e) {
      if (attempt === 0) { console.error(`[search] 「${keyword}」第 1 次失败，重试:`, e.message); await sleep(6000); }
      else throw e;
    }
  }
}

// ============ 笔记类型与时间归一化（v1.1.0） ============
// 体裁来自创作者后台导出 Excel 的「体裁」列（常见值：图文 / 视频）。
function noteType(n) {
  const g = String((n && n.genre) || '').trim();
  if (/视频|video/i.test(g)) return '视频';
  if (/图文|图片|image/i.test(g)) return '图文';
  // 兜底：图文笔记后台不给「人均观看时长」以外的视频指标，弹幕>0 基本可判定为视频
  if (Number(n && n.danmaku) > 0) return '视频';
  return '未知';
}
function retentionFloor(n) {
  const t = noteType(n);
  if (t === '视频') return RETENTION_BREAK_S_VIDEO;
  if (t === '图文') return RETENTION_BREAK_S_IMAGE;
  return RETENTION_BREAK_S;
}
// 已发布天数：曝光是随时间累积的存量，7 天的笔记和 46 天的笔记直接比曝光没有意义。
function daysSince(publishTime) {
  const t = Date.parse(String(publishTime || '').replace(/-/g, '/'));
  if (!Number.isFinite(t)) return 1;
  const d = Math.floor((Date.now() - t) / 86400000);
  return Math.max(1, d);
}
function perDay(value, publishTime) {
  const d = daysSince(publishTime);
  return Math.round((Number(value) || 0) / d);
}

// ============ 步骤 11：漏斗计算（阈值固定） ============
function computeFunnel(notes) {
  const sum = f => notes.reduce((a, n) => a + (Number(n[f]) || 0), 0);
  const totalExp = sum('exposure'), totalViews = sum('views');
  const totalLikes = sum('likes'), totalComments = sum('comments'), totalCollects = sum('collects');
  const totalFans = sum('fans'), totalShares = sum('shares');
  const avgCtr = totalExp ? totalViews / totalExp : 0;
  const ctrVerdict = avgCtr > CTR_OK_MAX ? '优秀' : (avgCtr >= CTR_OK_MIN ? '合格' : '偏弱');
  // 留存按各自体裁的阈值判定（图文 5s / 视频 10s），不再一刀切 10s
  const retentionBadNotes = notes.filter(n => (Number(n.avg_watch_sec) || 0) < retentionFloor(n));
  const retentionBad = retentionBadNotes.length;
  const retentionVerdict = retentionBad === 0 ? '合格' : (retentionBad >= 2 ? '断档' : '偏弱');
  const interactRate = totalViews ? (totalLikes + totalComments + totalCollects) / totalViews : 0;
  const interactVerdict = interactRate >= INTERACT_HOT ? '爆款线以上' : (interactRate >= INTERACT_OK ? '合格' : (interactRate > 0 ? '偏弱' : '断档'));
  const fanRate = totalViews ? totalFans / totalViews : 0;
  const fanVerdict = fanRate < FAN_BREAK ? '断档' : '合格';
  const pct = (v, d = 1) => (v * 100).toFixed(d) + '%';
  const watchTimes = notes.map(n => Number(n.avg_watch_sec) || 0);
  // 日均曝光：按各自已发布天数归一化后再比较，避免"老笔记曝光高"被误读成内容更好
  const expPerDay = notes.map(n => perDay(n.exposure, n.publish_time));
  const typeCount = notes.reduce((a, n) => { const t = noteType(n); a[t] = (a[t] || 0) + 1; return a; }, {});
  const typeSummary = Object.entries(typeCount).map(([k, v]) => `${k} ${v} 条`).join(' / ');
  return {
    totalExp, totalViews, totalLikes, totalComments, totalCollects, totalFans, totalShares,
    avgCtr, ctrVerdict, retentionBad, retentionBadNotes, retentionVerdict, interactRate, interactVerdict,
    fanRate, fanVerdict, pct, typeCount, typeSummary,
    maxWatch: watchTimes.length ? Math.max(...watchTimes) : 0,
    minWatch: watchTimes.length ? Math.min(...watchTimes) : 0,
    maxExpPerDay: expPerDay.length ? Math.max(...expPerDay) : 0,
    minExpPerDay: expPerDay.length ? Math.min(...expPerDay) : 0,
  };
}

// ============ 步骤 13：HTML 报告渲染 + 预览 ============
function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}
const fmtCtr = c => (Number(c) * 100).toFixed(1) + '%';
function verdictClass(v) {
  if (v === '优秀' || v === '合格' || v === '爆款线以上') return 'ok';
  if (v === '偏弱') return 'weak';
  return 'broken';
}
function todayStr() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

function buildConclusion(f, notes) {
  const n = notes.length;
  const parts = [`封面点击率整体为 ${f.pct(f.avgCtr)}（${f.ctrVerdict}）`];
  if (f.retentionBad > 0) parts.push(`${f.retentionBad}/${n} 条人均观看低于同体裁断档线（图文 ${RETENTION_BREAK_S_IMAGE}s / 视频 ${RETENTION_BREAK_S_VIDEO}s，${f.retentionVerdict}）`);
  else parts.push(`人均观看均达同体裁断档线以上（${f.retentionVerdict}）`);
  parts.push(`互动率 ${f.pct(f.interactRate)}（${f.interactVerdict}）`);
  if (f.totalFans === 0) parts.push('涨粉为零（断档）');
  else parts.push(`涨粉率 ${f.pct(f.fanRate, 2)}（${f.fanVerdict}）`);
  const decay = f.retentionVerdict !== '合格' || f.interactVerdict === '偏弱' || f.interactVerdict === '断档' || f.fanVerdict !== '合格';
  return `诊断结论（本批 ${f.typeSummary || '体裁未识别'}）：` + parts.join('；') + '。' +
    (decay ? '「点击 → 留存 → 互动 → 涨粉」存在逐层衰减，优先修复「正文前 3 秒钩子」与「收藏/评论引导」。' : '「点击 → 留存 → 互动 → 涨粉」整体健康。');
}

function buildReportHtml(ctx, f, reportFull) {
  const date = todayStr();
  const nickname = ctx.accountNickname || '（未能识别账号昵称）';

  const rows = ctx.notes.map((n) => `
    <tr>
      <td class="t">${esc(n.title)}</td>
      <td>${esc(noteType(n))}</td>
      <td>${esc(n.publish_time)}</td>
      <td>${daysSince(n.publish_time)}天</td>
      <td>${n.exposure}</td>
      <td>${perDay(n.exposure, n.publish_time)}</td>
      <td>${n.views}</td>
      <td>${fmtCtr(n.ctr)}</td>
      <td>${n.likes}</td>
      <td>${n.comments}</td>
      <td>${n.collects}</td>
      <td>${n.fans}</td>
      <td>${n.shares}</td>
      <td>${n.avg_watch_sec}s</td>
    </tr>`).join('');

  const retTitles = (f.retentionBadNotes || []).map(n => `${n.title}（${noteType(n)} ${n.avg_watch_sec}s）`).join('、');

  const stages = `
    <div class="stage">
      <div class="name">① 点击率（曝光→观看）</div>
      <div class="value">${f.pct(f.avgCtr)}</div>
      <div><span class="badge ${verdictClass(f.ctrVerdict)}">${f.ctrVerdict}</span></div>
      <div class="detail">曝光 ${f.totalExp} → 观看 ${f.totalViews}；<br>合格区间 10%–20%${f.avgCtr > 0.20 ? '，本账号高于优秀线' : ''}。<br>日均曝光 ${f.maxExpPerDay} 最高 / ${f.minExpPerDay} 最低（已按发布天数归一化）。</div>
    </div>
    <div class="stage">
      <div class="name">② 内容留存（人均观看时长）</div>
      <div class="value">${f.maxWatch}s 最优 / ${f.minWatch}s 最差</div>
      <div><span class="badge ${verdictClass(f.retentionVerdict)}">${f.retentionVerdict}</span></div>
      <div class="detail">断档线按体裁分设：图文 &lt;${RETENTION_BREAK_S_IMAGE}s / 视频 &lt;${RETENTION_BREAK_S_VIDEO}s。<br>本批 ${f.retentionBad} 条低于断档线：${esc(retTitles || '（无）')}。</div>
    </div>
    <div class="stage">
      <div class="name">③ 互动率（赞+评+藏）/观看</div>
      <div class="value">${f.pct(f.interactRate)}</div>
      <div><span class="badge ${verdictClass(f.interactVerdict)}">${f.interactVerdict}</span></div>
      <div class="detail">互动 ${f.totalLikes + f.totalComments + f.totalCollects}（赞 ${f.totalLikes} / 评 ${f.totalComments} / 藏 ${f.totalCollects}）；爆款线 5%–10%</div>
    </div>
    <div class="stage">
      <div class="name">④ 涨粉（观看→关注）</div>
      <div class="value">${f.totalFans} 粉 / ${ctx.notes.length} 条</div>
      <div><span class="badge ${verdictClass(f.fanVerdict)}">${f.fanVerdict}</span></div>
      <div class="detail">涨粉率 ${f.pct(f.fanRate, 2)}；${f.totalShares} 次分享。互动与涨粉断层最严重。</div>
    </div>`;

  const noteBlocks = ctx.notes.map((n, i) => {
    const kws = (ctx.keywords[i] || []).join(' / ');
    const b = ctx.benchmarks[i] || { benchmarks: [], enough: false, actual_count: 0, reason: '' };
    const acts = ctx.actions[i] || [];
    const bmRows = b.benchmarks.map((x, j) =>
      `<tr><td>${j + 1}</td><td class="t">${esc(x.title)}</td><td>${esc(x.author)}</td><td>${esc(x.likes)}</td></tr>`).join('');
    const bmNote = !b.enough
      ? `<p class="warn">⚠ 达到爆款门槛（≥${b.likes_floor || BENCH_MIN_LIKES} 赞）且题材相似的对标不足 3 条（实际 ${b.actual_count} 条）：${esc(b.reason)}。宁缺毋滥，未用低赞笔记凑数。</p>` : '';
    const actItems = acts.length ? acts.map(a => `<li>${esc(a)}</li>`).join('')
      : '<li class="warn">改进动作生成失败（子会话未返回）。</li>';
    const interact = n.likes + n.comments + n.collects;
    return `
    <div class="note-card">
      <h3><span class="idx">${i + 1}</span>${esc(n.title)}</h3>
      <p class="meta">${esc(noteType(n))} ｜ 已发布 ${daysSince(n.publish_time)} 天 ｜ 关键词：<b>${esc(kws || '（无）')}</b> ｜ 曝光 ${n.exposure}（日均 ${perDay(n.exposure, n.publish_time)}） ｜ 观看 ${n.views} ｜ 点击率 ${fmtCtr(n.ctr)} ｜ 互动 ${interact} ｜ 涨粉 ${n.fans}</p>
      <h4>对标爆款表（点赞门槛 ≥${b.likes_floor || BENCH_MIN_LIKES}）</h4>
      <table><thead><tr><th>#</th><th>标题</th><th>作者</th><th>点赞数</th></tr></thead><tbody>${bmRows}</tbody></table>
      ${bmNote}
      <h4>3 条改进动作</h4>
      <ol class="actions">${actItems}</ol>
    </div>`;
  }).join('');

  const footerNote = reportFull
    ? '本次每条笔记均找到 ≥3 条达到点赞门槛的同题材对标爆款，报告完整（full）。'
    : `本次有 ${ctx.partials.length} 条笔记的合格对标不足 3 条（partial，宁缺毋滥不凑数）：${ctx.partials.map(p => `「${p.title}」实际 ${p.count} 条（${p.reason}）`).join('；')}。`;

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>小红书账号分析报告 ${date}</title>
<style>
  body { font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; background: #f7f7fa; color: #333; margin: 0; padding: 24px; }
  .wrap { max-width: 1080px; margin: 0 auto; }
  h1 { font-size: 24px; color: #ff2e4d; }
  h2 { font-size: 19px; border-left: 4px solid #ff2e4d; padding-left: 10px; margin-top: 36px; }
  h3 { font-size: 16px; }
  h4 { font-size: 14px; color: #666; margin: 16px 0 8px; }
  table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
  th, td { padding: 10px 12px; text-align: left; font-size: 13px; border-bottom: 1px solid #eee; }
  th { background: #fafafa; color: #888; font-weight: 500; white-space: nowrap; }
  td.t { color: #333; }
  .note-card { background: #fff; border-radius: 8px; padding: 20px; margin: 16px 0; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
  .note-card h3 .idx { display: inline-block; background: #ff2e4d; color: #fff; border-radius: 50%; width: 22px; height: 22px; line-height: 22px; text-align: center; font-size: 12px; margin-right: 6px; }
  .meta { color: #888; font-size: 12px; margin: 6px 0 0; }
  ol.actions li { margin: 8px 0; font-size: 13px; line-height: 1.7; }
  .warn { color: #ff9500; font-size: 13px; }
  .funnel { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 8px; }
  .funnel .stage { background: #fff; border-radius: 8px; padding: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
  .funnel .stage .name { font-size: 13px; color: #888; }
  .funnel .stage .value { font-size: 22px; font-weight: 700; margin: 6px 0; }
  .funnel .stage .detail { font-size: 12px; color: #999; line-height: 1.5; }
  .badge { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; color: #fff; }
  .ok { background: #34c759; }
  .weak { background: #ff9500; }
  .broken { background: #ff2e4d; }
  .footer { margin-top: 30px; color: #aaa; font-size: 12px; text-align: center; }
</style>
</head>
<body>
<div class="wrap">
  <h1>小红书账号分析报告</h1>
  <p style="color:#888;font-size:13px;">分析对象：账号「${esc(nickname)}」 ｜ 数据来源：创作者后台官方数据看板（导出 Excel）＋ 小红书公开搜索结果 ｜ 生成时间：${new Date().toLocaleString('zh-CN')}</p>

  <h2>① 数据总表（最近 ${ctx.notes.length} 条笔记，按首发时间倒序）</h2>
  <p style="color:#999;font-size:12px;margin:4px 0 10px;">曝光是随时间累积的存量，新旧笔记不可直接比大小，故额外给出「日均曝光 = 曝光 / 已发布天数」；留存断档线按体裁分设（图文 ${RETENTION_BREAK_S_IMAGE}s / 视频 ${RETENTION_BREAK_S_VIDEO}s）。</p>
  <table>
    <thead><tr><th>标题</th><th>类型</th><th>首发时间</th><th>已发布</th><th>曝光</th><th>日均曝光</th><th>观看量</th><th>封面点击率</th><th>点赞</th><th>评论</th><th>收藏</th><th>涨粉</th><th>分享</th><th>人均观看时长</th></tr></thead>
    <tbody>${rows}</tbody>
  </table>

  <h2>② 转化漏斗健康度诊断</h2>
  <div class="funnel">${stages}</div>
  <p style="font-size:13px;color:#666;line-height:1.7;">${esc(buildConclusion(f, ctx.notes))}</p>

  <h2>③ 逐条笔记：对标爆款 + 改进动作</h2>
  ${noteBlocks}

  <div class="footer">本报告由 xhs-account-analyst 自动生成。竞对数据仅使用搜索结果页公开可见的标题、作者与点赞数。${esc(footerNote)}</div>
</div>
</body>
</html>`;
}

// ============ 数据/摘要输出 ============
function buildMarkdown(ctx, f, reportFull) {
  const L = [];
  L.push('# 小红书账号分析数据（xhs-account-analyst）', '');
  L.push(`- 分析账号：${ctx.accountNickname || '（未能识别账号昵称）'}`);
  L.push('- 数据来源：创作者后台官方数据看板导出 Excel');
  L.push(`- 分析参数：notes_count=${ctx.notesCount}，keyword_per_note=${ctx.kwPerNote}`);
  L.push(`- 报告状态：${reportFull ? 'full（每条笔记均有 ≥3 条达到点赞门槛的同题材对标）' : 'partial（存在合格对标不足 3 条的笔记，宁缺毋滥不凑数）'}`);
  L.push(`- 报告文件：${ctx.reportPath}`);
  L.push('- 竞对数据仅使用搜索结果页公开可见的标题、作者与点赞数', '');

  L.push(`## ① 数据总表（最近 ${ctx.notes.length} 条笔记，按首发时间倒序）`, '');
  L.push('> 曝光是随时间累积的存量，新旧笔记不可直接比大小，故额外给出「日均曝光 = 曝光 / 已发布天数」。', '');
  L.push('| 标题 | 类型 | 首发时间 | 已发布 | 曝光 | 日均曝光 | 观看量 | 封面点击率 | 点赞 | 评论 | 收藏 | 涨粉 | 分享 | 人均观看时长 |');
  L.push('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|');
  for (const n of ctx.notes) {
    L.push(`| ${n.title} | ${noteType(n)} | ${n.publish_time} | ${daysSince(n.publish_time)}天 | ${n.exposure} | ${perDay(n.exposure, n.publish_time)} | ${n.views} | ${fmtCtr(n.ctr)} | ${n.likes} | ${n.comments} | ${n.collects} | ${n.fans} | ${n.shares} | ${n.avg_watch_sec}s |`);
  }
  L.push('', '## ② 转化漏斗健康度诊断', '');
  L.push('| 层级 | 指标 | 数值 | 判断 | 说明 |');
  L.push('|---|---|---|---|---|');
  L.push(`| ① 点击率（曝光→观看） | 观看量/曝光 | ${f.pct(f.avgCtr)}（${f.totalViews}/${f.totalExp}） | ${f.ctrVerdict} | 合格区间 10%-20%；日均曝光 ${f.maxExpPerDay} 最高 / ${f.minExpPerDay} 最低 |`);
  L.push(`| ② 内容留存（人均观看时长） | 人均观看时长 | 最优 ${f.maxWatch}s / 最差 ${f.minWatch}s | ${f.retentionVerdict} | 断档线按体裁分设：图文 <${RETENTION_BREAK_S_IMAGE}s / 视频 <${RETENTION_BREAK_S_VIDEO}s；本批 ${f.retentionBad} 条低于断档线 |`);
  L.push(`| ③ 互动率（(赞+评+藏)/观看） | 互动/观看 | ${f.pct(f.interactRate)}（${f.totalLikes + f.totalComments + f.totalCollects}/${f.totalViews}） | ${f.interactVerdict} | 爆款线 5%-10%；赞 ${f.totalLikes} / 评 ${f.totalComments} / 藏 ${f.totalCollects} |`);
  L.push(`| ④ 涨粉（观看→关注） | 涨粉数 | ${f.totalFans} 粉 / ${ctx.notes.length} 条（${f.pct(f.fanRate, 2)}） | ${f.fanVerdict} | ${f.totalShares} 次分享 |`);
  L.push('', buildConclusion(f, ctx.notes), '');

  L.push('## ③ 逐条笔记：对标爆款 + 改进动作', '');
  ctx.notes.forEach((n, i) => {
    const b = ctx.benchmarks[i] || { benchmarks: [], enough: false, actual_count: 0, reason: '' };
    L.push(`### 笔记 ${i + 1}：${n.title}（${noteType(n)}，已发布 ${daysSince(n.publish_time)} 天，关键词：${(ctx.keywords[i] || []).join(' / ') || '无'}）`, '');
    L.push(`对标爆款表（点赞门槛 ≥${b.likes_floor || BENCH_MIN_LIKES}）：`, '');
    L.push('| # | 标题 | 作者 | 点赞数 |');
    L.push('|---|---|---|---|');
    b.benchmarks.forEach((x, j) => L.push(`| ${j + 1} | ${x.title} | ${x.author} | ${x.likes} |`));
    if (!b.enough) L.push('', `> ⚠ 达到爆款门槛且题材相似的对标不足 3 条（实际 ${b.actual_count} 条）：${b.reason}。宁缺毋滥，未用低赞笔记凑数。`);
    L.push('', '3 条改进动作：', '');
    const acts = ctx.actions[i] || [];
    acts.forEach((a, j) => L.push(`${j + 1}. ${a}`));
    if (!acts.length) L.push('（改进动作生成失败）');
    L.push('');
  });

  L.push('## 执行过程记录', '');
  for (const log of ctx.logs) L.push('- ' + log);
  L.push('');
  return L.join('\n');
}

// ============ 主流程 ============
async function main() {
  mkdirSync(TMP, { recursive: true });

  let input = {};
  try {
    input = JSON.parse(readFileSync(join(process.cwd(), 'input.json'), 'utf-8'));
  } catch (e) {
    console.error('input.json 读取失败（使用默认值）:', e.message);
  }
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
  const notesCount = clamp(Number(input.notes_count) || 5, 1, 20);
  const kwPerNote = clamp(Number(input.keyword_per_note) || 1, 1, 3);
  const outputDir = input.output_dir || '/tmp/xhs-note-analyst-output';
  const outputFiles = input.output_files || {};
  const resultFile = join(outputDir, outputFiles.result || 'res.json');
  const dataFile = join(outputDir, outputFiles.data || 'data.md');
  const reportPath = input.report_path || join(outputDir, `小红书账号分析报告_${todayStr()}.html`);
  try { mkdirSync(outputDir, { recursive: true }); } catch (e) { /* 调用方已建好，忽略 */ }
  try { mkdirSync(dirname(reportPath), { recursive: true }); } catch (e) { /* 忽略 */ }

  const ctx = {
    notesCount, kwPerNote, outputDir, resultFile, dataFile, reportPath,
    notes: [], keywords: [], cardsByNote: [], benchmarks: [], actions: [],
    partials: [], logs: [], error: '', accountNickname: '', totalKeywords: 0,
  };

  try {
    await ensureRelay();
    // 建本任务 tab 组：并行跑多个 skill 时各自 tab 隔离，不混进共享的 wc3 默认组
    const { groupId } = await relayCall('group.create', { name: 'xhs-note-analyst' });
    GROUP_ID = groupId;
    console.error(`[run] notes_count=${notesCount}, keyword_per_note=${kwPerNote}, report=${reportPath}`);

    // 步骤 1-4：创作者后台导出 Excel + openpyxl 解析
    // existing_excel：传入已导出的 Excel 路径则跳过导出（运行环境读不了 ~/Downloads 时的兜底，
    // 配合 account_nickname 供对标搜索剔除自家笔记）
    const useExisting = input.existing_excel && existsSync(input.existing_excel);
    const { nickname, excelPath } = useExisting
      ? { nickname: input.account_nickname || '', excelPath: input.existing_excel }
      : await exportNotesFromCreator();
    if (useExisting) console.error(`[run] 使用已导出 Excel: ${excelPath}`);
    ctx.accountNickname = nickname;
    console.error(`[run] 账号昵称: ${nickname || '未识别'}，导出文件: ${excelPath}`);
    const allNotes = await parseNotesExcel(excelPath);
    if (!Array.isArray(allNotes) || !allNotes.length) throw new Error('Excel 中无笔记数据');
    allNotes.sort((a, b) => (a.publish_time < b.publish_time ? 1 : a.publish_time > b.publish_time ? -1 : 0));
    ctx.notes = allNotes.slice(0, notesCount);
    ctx.logs.push(`创作者后台导出 Excel（${excelPath}），共 ${allNotes.length} 条，按首发时间倒序取前 ${ctx.notes.length} 条`);
    console.error(`[run] 待分析笔记 ${ctx.notes.length} 条`);

    // 步骤 5：关键词提炼（子会话，每批最多 3 条，规则 9）
    for (let start = 0; start < ctx.notes.length; start += 3) {
      const batch = ctx.notes.slice(start, start + 3);
      try {
        const out = await runSubsession(buildKeywordPrompt(batch, kwPerNote), KEYWORD_SCHEMA, 'kw');
        const items = normalizeKeywords(out);
        for (const it of items) {
          let g = start + Number(it.index);
          if (isNaN(g) || g < start || g >= start + batch.length) {
            const byTitle = batch.findIndex(n => n.title === it.title);
            g = byTitle >= 0 ? start + byTitle : -1;
          }
          if (g >= 0 && g < ctx.notes.length) ctx.keywords[g] = it.keywords.slice(0, kwPerNote);
        }
      } catch (e) {
        console.error(`[kw] 关键词提炼批次 ${start} 失败:`, e.message);
        ctx.logs.push(`关键词提炼批次失败: ${e.message}`);
      }
    }
    ctx.keywords = ctx.notes.map((n, i) => ctx.keywords[i] || []);
    ctx.totalKeywords = ctx.keywords.reduce((a, k) => a + k.length, 0);
    console.error(`[run] 关键词: ${JSON.stringify(ctx.keywords)}`);

    // 步骤 6-9：逐关键词搜索（串行 + 词间节奏控制）
    for (let i = 0; i < ctx.notes.length; i++) {
      const kws = ctx.keywords[i] || [];
      const allCards = [];
      for (const kw of kws) {
        try {
          const cards = await searchKeywordWithRetry(kw);
          allCards.push(...cards);
          console.error(`[search] 「${kw}」取到 ${cards.length} 张卡片`);
        } catch (e) {
          console.error(`[search] 「${kw}」失败:`, e.message);
          ctx.logs.push(`搜索「${kw}」失败: ${e.message}`);
        }
        if (kws.length > 1) await sleep(BETWEEN_SEARCH_MS + Math.floor(Math.random() * 2000));
      }
      // 按 note-id 去重（同词不同词可能重复出现同一卡片）
      const seen = new Set();
      ctx.cardsByNote[i] = allCards.filter(c => { if (!c.id || seen.has(c.id)) return false; seen.add(c.id); return true; });
      await sleep(BETWEEN_SEARCH_MS + Math.floor(Math.random() * 2000));
    }

    // 步骤 10：对标爆款筛选（子会话，每笔记一条，并行限流 2）
    const benchRes = await pMap(ctx.notes, async (note, i) => {
      // 无关键词或无搜索结果卡片时无法筛选对标：跳过子会话直接记 partial，避免浪费 LLM 调用
      if (!(ctx.keywords[i] || []).length || !(ctx.cardsByNote[i] || []).length) {
        return { benchmarks: [], enough: false, actual_count: 0, reason: '无搜索结果卡片' };
      }
      return pickBenchmarks(i, note, ctx.keywords[i] || [], ctx.cardsByNote[i] || [], ctx.accountNickname);
    });
    ctx.benchmarks = ctx.notes.map((n, i) =>
      (benchRes[i] && benchRes[i].status === 'fulfilled') ? benchRes[i].value
        : { benchmarks: [], enough: false, actual_count: 0, reason: '对标筛选失败' });

    // 汇总 partial（不足 3 条 / 关键词缺失 / 搜索无结果）
    for (let i = 0; i < ctx.notes.length; i++) {
      const b = ctx.benchmarks[i];
      if (!b.enough) {
        let reason = b.reason || '达到点赞门槛的同题材对标不足 3 条';
        if (!(ctx.keywords[i] || []).length) reason = '关键词提炼失败，未执行搜索';
        else if (!(ctx.cardsByNote[i] || []).length) reason = '搜索未获取到结果卡片';
        ctx.partials.push({ title: ctx.notes[i].title, count: b.actual_count, reason });
      }
    }
    const benchOkCount = ctx.benchmarks.filter(b => b.enough).length;
    console.error(`[run] 对标爆款：${benchOkCount}/${ctx.notes.length} 条笔记达标`);

    // 步骤 12：改进动作生成（子会话，每笔记一条，并行限流 2）
    const actRes = await pMap(ctx.notes, async (note, i) =>
      generateActions(i, note, (ctx.benchmarks[i] && ctx.benchmarks[i].benchmarks) || []));
    ctx.actions = ctx.notes.map((n, i) =>
      (actRes[i] && actRes[i].status === 'fulfilled' && Array.isArray(actRes[i].value)) ? actRes[i].value : []);

    // 步骤 11+13：漏斗计算 + HTML 渲染 + 预览
    const funnel = computeFunnel(ctx.notes);
    const reportFull = ctx.partials.length === 0;
    const html = buildReportHtml(ctx, funnel, reportFull);
    writeFileSync(reportPath, html, 'utf-8');
    console.error(`[run] 报告已写入: ${reportPath}（${html.length} bytes）`);

    // 打开预览并验证（不 track，预览 tab 留给用户）
    try {
      const previewUrl = 'file://' + encodeURI(reportPath);
      const ptab = await relayCall('tab.create', { url: previewUrl, active: true, groupId: GROUP_ID });
      await sleep(3000);
      const st = await evalJson(ptab.id, 'JSON.stringify({url: location.href, title: document.title, hasH1: !!document.querySelector("h1")})');
      console.error(`[preview] ${JSON.stringify(st)}`);
      if (!st || !st.hasH1) ctx.logs.push('报告预览验证异常（hasH1=false）');
    } catch (e) {
      console.error('[preview] 预览打开失败:', e.message);
      ctx.logs.push('预览打开失败: ' + e.message);
    }
  } catch (e) {
    ctx.error = String(e && e.message || e);
    console.error('[run] 异常:', e);
  } finally {
    await closeAllTabs();
    // 整组关闭（含建组时的种子 tab），任务结束不残留、不影响并行中的其他任务
    if (GROUP_ID != null) { try { await relayCall('group.close', { groupId: GROUP_ID }); } catch (e) { console.error('group.close fail:', e.message); } }
  }

  // 状态与摘要
  let status, summary;
  if (ctx.error) {
    status = 'failed';
    summary = `运行失败: ${ctx.error}`;
  } else if (!ctx.notes.length) {
    status = 'failed';
    summary = '未获取到任何笔记数据（Excel 为空或解析失败）';
  } else if (ctx.partials.length === 0) {
    status = 'success';
    summary = `已分析最近 ${ctx.notes.length} 条笔记并生成报告：${reportPath}。关键词 ${ctx.totalKeywords} 个，每条笔记均找到 ≥3 条达到点赞门槛的同题材对标爆款（full）。`;
  } else {
    const parts = ctx.partials.map(p => `「${p.title}」实际 ${p.count} 条（${p.reason}）`);
    status = 'partial';
    summary = `已生成报告（partial）：${ctx.partials.length}/${ctx.notes.length} 条笔记的合格对标不足 3 条（宁缺毋滥，未用低赞笔记凑数）——${parts.join('；')}。报告：${reportPath}`;
  }

  const result = {
    status, summary,
    notes_count: ctx.notesCount,
    account_nickname: ctx.accountNickname,
    note_count_analyzed: ctx.notes.length,
    keywords: ctx.keywords,
    benchmark_shortages: ctx.partials,
    report_path: reportPath,
    output_dir: outputDir,
  };
  try { writeFileSync(resultFile, JSON.stringify(result, null, 2)); } catch (e) { console.error('res.json 写入失败:', e.message); }
  try {
    const md = ctx.notes.length
      ? buildMarkdown(ctx, computeFunnel(ctx.notes), ctx.partials.length === 0)
      : `# 小红书账号分析数据（xhs-account-analyst）\n\n- 状态：failed\n- 说明：${summary}\n`;
    writeFileSync(dataFile, md);
  } catch (e) { console.error('data.md 写入失败:', e.message); }

  // stdout 只输出一行 JSON 摘要（其余日志走 stderr）
  console.log(JSON.stringify({ status, summary, output_dir: outputDir }));
}

// ============ 子会话封装（供主流程调用的带兜底实现） ============
async function pickBenchmarks(noteIdx, note, keywords, cards, ownNickname) {
  const likesFloor = computeLikesFloor(cards);
  try {
    const out = await runSubsession(buildBenchmarkPrompt(note, keywords, cards, ownNickname, likesFloor), BENCH_SCHEMA, 'bench');
    return normalizeBenchmarks(out, likesFloor);
  } catch (e) {
    console.error(`[bench] 对标筛选失败（note ${noteIdx}）:`, e.message);
    return { benchmarks: [], enough: false, actual_count: 0, reason: '对标筛选子会话失败' };
  }
}
async function generateActions(noteIdx, note, benchmarks) {
  try {
    const out = await runSubsession(buildActionPrompt(note, benchmarks), ACTION_SCHEMA, 'act');
    return normalizeActions(out);
  } catch (e) {
    console.error(`[act] 改进动作生成失败（note ${noteIdx}）:`, e.message);
    return [];
  }
}

// ============ 点赞数换算（"1.2万"→12000；"赞"或非数字→0） ============
function parseLikes(s) {
  const str = String(s || '').trim();
  const m = str.match(/([\d.]+)\s*万/);
  if (m) return Math.round(parseFloat(m[1]) * 10000);
  const n = str.match(/^[\d,]+$/);
  if (n) return parseInt(str.replace(/,/g, ''), 10);
  return 0;
}

main().then(() => process.exit(0)).catch(e => {
  console.error('fatal:', e);
  console.log(JSON.stringify({ status: 'failed', error: String(e && e.message || e) }));
  process.exit(0);
});
