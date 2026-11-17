#!/usr/bin/env node
/**
 * tb-opportunity-radar — 新品机会雷达：类目级竞品分析（淘宝/天猫 + 小红书）
 *
 * 输入 1 个淘宝/天猫商品链接 → 采集该商品(A) → 猜聚焦搜索词 → 淘宝搜索前 5 seeded 随机选 B/C（排除同店）
 * → 三品同管线采集（主图/详情长图/SKU/价格销量/评价）→ 图片文案 OCR + 七维打标 → 频次×销量加权
 * → 评价三层规则分层 → xhs 同词需求源采集 → 生成 HTML 报告。
 *
 * 浏览器操作只走 Extension Relay（HTTP 3459）；需要"理解"的判断交给 LLM 子会话（wc3-code → serve :3460）。
 * 本 skill 完全独立，不 import / 不读取 / 不引用任何其他 skill 的代码或文档。
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { spawn, execFileSync } from 'node:child_process';

// ---------------------------------------------------------------------------
// 常量与基础设施
// ---------------------------------------------------------------------------

const RELAY_URL = 'http://127.0.0.1:3459';
const CLI_DIR = import.meta.dirname;
const WC3_CODE = join(CLI_DIR, 'wc3-code.mjs');
const TMP = join(tmpdir(), 'tb-opportunity-radar-' + process.pid);

// 访问节奏：任何浏览器操作之间至少间隔 1.9s（要求 ≥1.8s）。sleep 本身也算间隔，所以只在不足时补。
const MIN_OP_INTERVAL_MS = 1900;
const CONCURRENCY = 2; // 子会话并发上限 2，避免限流

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let lastOpEnd = 0;
async function relayCall(op, params = {}, timeout = 45000) {
  const gap = MIN_OP_INTERVAL_MS - (Date.now() - lastOpEnd);
  if (gap > 0) await sleep(gap);
  const res = await fetch(`${RELAY_URL}/api/call`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ op, params, timeout }),
  });
  const data = await res.json();
  lastOpEnd = Date.now();
  if (data.error) throw new Error(`${op}: ${data.error}`);
  return data.result;
}

async function ensureRelay() {
  let status;
  try {
    status = await (await fetch(`${RELAY_URL}/api/status`)).json();
  } catch (e) {
    throw new Error(`浏览器中继不可用（${RELAY_URL}）：${e.message}`);
  }
  if (!status.extensionConnected) throw new Error('浏览器扩展未连接，请确认中继服务与扩展已启动');
}

let GROUP_ID = null;
function pageEval(tabId, code, timeout = 45000) {
  return relayCall('page.eval', { tabId, groupId: GROUP_ID, code }, timeout);
}
function openTab(url, active = false) {
  return relayCall('tab.create', { url, active, groupId: GROUP_ID });
}
async function closeTab(tabId) {
  try { await relayCall('tab.close', { tabId, groupId: GROUP_ID }); } catch { /* 关不掉不影响结果 */ }
}

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

// --- LLM 子会话（wc3-code → 本地 serve :3460 代跑）---

function callClaudeWithFile(promptContent, promptFile, outputFile, opts = {}) {
  writeFileSync(promptFile, promptContent, 'utf-8');
  return new Promise((resolve, reject) => {
    const args = ['--prompt-file', promptFile, '--output', outputFile];
    if (opts.timeout) args.push('--timeout', String(opts.timeout));
    if (opts.schema) args.push('--schema', opts.schema);
    if (opts.resume) args.push('--resume', opts.resume);
    const child = spawn('node', [WC3_CODE, ...args], { stdio: ['ignore', 'ignore', 'pipe'] });
    let stderr = '';
    child.stderr.on('data', (d) => { stderr += d; });
    child.on('close', (code) => {
      if (code !== 0) return reject(new Error(`wc3-code exit ${code}: ${stderr.slice(0, 300)}`));
      try { resolve(readFileSync(outputFile, 'utf-8')); } catch (e) { reject(e); }
    });
    child.on('error', reject);
  });
}

// 子会话返回结构不可靠，递归剥壳后再用（规则：先 parse → 解 {result} → 抠代码块 → 兜底匹配）
function extractJson(raw) {
  if (raw == null) return null;
  if (typeof raw === 'object') return raw;
  let v = String(raw).trim();
  for (let i = 0; i < 4; i++) {
    try { const p = JSON.parse(v); if (p && typeof p === 'object') return normalizeResult(p); } catch { /* 继续剥 */ }
    const m = v.match(/```(?:json)?\s*([\s\S]*?)```/);
    if (m) { v = m[1].trim(); continue; }
    const s = v.indexOf('{'), a = v.indexOf('[');
    const start = s >= 0 && (a < 0 || s < a) ? s : a;
    if (start < 0) return null;
    const endCh = v[start] === '{' ? '}' : ']';
    const end = v.lastIndexOf(endCh);
    if (end <= start) return null;
    v = v.slice(start, end + 1);
  }
  try { return JSON.parse(v); } catch { return null; }
}
function normalizeResult(p) {
  if (p && typeof p === 'object' && !Array.isArray(p) && typeof p.result !== 'undefined' && Object.keys(p).length <= 3) {
    if (typeof p.result === 'string' || typeof p.result === 'object') return normalizeResult(p.result);
  }
  return p;
}
async function llmJson(name, prompt, schema) {
  const out = await callClaudeWithFile(prompt, join(TMP, `prompt-${name}.md`), join(TMP, `out-${name}.json`), { schema });
  const parsed = extractJson(out);
  if (!parsed) throw new Error(`子会话 ${name} 返回无法解析`);
  return parsed;
}

// ---------------------------------------------------------------------------
// 页面内 JS（全部来自实测成功记录；用 String.raw 保证正则里的 \d 不被 JS 字符串吃掉）
// ---------------------------------------------------------------------------

const JS_PAGE_STATE = String.raw`(()=>{
  const t = document.body ? document.body.innerText : '';
  return JSON.stringify({
    title: document.title || '',
    url: location.href,
    bodyLen: t.length,
    blocked: /亲，请验证|滑动验证|Security Check|请完成安全验证/.test(t.slice(0, 3000)),
    loginWall: /login\.taobao\.com|login\.tmall\.com|passport\.alipay/.test(location.href)
  });
})()`;

const JS_META = String.raw`(()=>{
  const t = document.body ? document.body.innerText : '';
  const pick = (re) => { const m = t.match(re); return m ? m[1].trim() : null; };
  // 店铺名：必须用 shopName-- 选择器直取且过滤掉 Wrap 外层（shopNameWrap > span.shopName 结构），
  // 正文正则只作兜底——上一版只靠正则导致 shop 采空、同店排除失效
  let shop = '';
  const shopEls = Array.from(document.querySelectorAll('[class*="shopName--"]')).filter(function(e){ return !/Wrap/.test(String(e.className)); });
  for (let i = 0; i < shopEls.length; i++) {
    const s = (shopEls[i].textContent || '').trim();
    if (s) { shop = s; break; }
  }
  if (!shop) shop = pick(/([^\n]{2,24}(?:旗舰店|专营店|专卖店|官方店|企业店))/) || '';
  // shopId 主键：店铺链接 href（同店排除用 shopId 比对，不用店名文本）
  const shopLink = document.querySelector('a[href*="//shop"]');
  const shopLinkHref = shopLink ? shopLink.href : '';
  const shopIdM = shopLinkHref.match(/shop(\d+)\.(?:taobao|tmall)\.com/);
  const shopId = shopIdM ? shopIdM[1] : '';
  let sold = null, soldText = null;
  const sm = t.match(/已售\s*([\d.]+)\s*(万)?\s*\+/);           // 「已售 3万+」也要能吃下
  if (sm) { soldText = sm[0].trim(); sold = Math.round(parseFloat(sm[1]) * (sm[2] ? 10000 : 1)); }
  const rateCountText = pick(/用户评价·\s*([0-9]+(?:\+)?|[\d.]+万(?:\+)?)/);
  const gr = pick(/近3个月好评率高达([0-9.]+%)/);
  const goodRateText = gr ? ('近3个月好评率高达' + gr) : null;

  // 价格：页面里 ￥ 出现多次（优惠券金额常在前面），优先取「￥N 起」这一组
  const hits = [];
  const prx = /￥\s*\n?\s*([0-9]+(?:\.[0-9]+)?)/g;
  let pm;
  while ((pm = prx.exec(t)) !== null) {
    const after = t.slice(pm.index + pm[0].length, pm.index + pm[0].length + 10).replace(/\s+/g, '');
    const before = t.slice(Math.max(0, pm.index - 10), pm.index).replace(/\s+/g, '');
    hits.push({ v: parseFloat(pm[1]), after: after, before: before });
    if (hits.length > 40) break;
  }
  const hit = hits.find(function(p){ return p.after.indexOf('起') === 0 && !/券|减|满/.test(p.before); })
           || hits.find(function(p){ return p.after.indexOf('起') === 0; })
           || hits[0] || null;
  const priceText = hit ? ('￥' + hit.v + (hit.after.indexOf('起') === 0 ? ' 起' : '')) : null;

  let skus = [];
  const ci = t.indexOf('颜色分类');
  if (ci >= 0) {
    const lines = t.slice(ci + 4).split('\n').map(function(s){ return s.trim(); }).filter(Boolean);
    for (let i = 0; i < Math.min(3, lines.length); i++) {
      const parts = lines[i].split(/[\t ]+/).map(function(s){ return s.trim(); }).filter(function(s){ return s.length > 1; });
      if (parts.length > skus.length) skus = parts;
      if (skus.length >= 2) break;
    }
  }
  skus = skus.slice(0, 60);
  return JSON.stringify({
    title: document.title || '', shop: shop, shopId: shopId, shopLinkHref: shopLinkHref,
    sold: sold, soldText: soldText,
    rateCountText: rateCountText, goodRateText: goodRateText,
    price: hit ? hit.v : null, priceText: priceText,
    skus: skus, skuCount: skus.length
  });
})()`;

// 主图：只认 alicdn 且实际渲染宽度 ≥300，按 O1CN 串去重（同一张图有 _q50.jpg_.webp / _.webp 两种 src）
const JS_MAIN_IMAGES = String.raw`(()=>{
  const out = []; const seen = new Set();
  Array.from(document.querySelectorAll('img')).forEach(function(i){
    const s = i.src || '';
    if (!/alicdn|taobaocdn|tbcdn/.test(s)) return;
    if (!(i.naturalWidth >= 300)) return;
    const k = (s.match(/O1CN[A-Za-z0-9]+/) || [s])[0];
    if (seen.has(k)) return;
    seen.add(k); out.push(s);
  });
  return JSON.stringify(out.slice(0, 12));
})()`;

// 「图文详情」tab：不在 interactive ariaTree 里，必须 dispatch 完整指针/鼠标事件序列
const JS_CLICK_DETAIL_TAB = String.raw`(()=>{
  const cands = Array.from(document.querySelectorAll('div,span,li,a')).filter(function(e){
    const x = (e.textContent || '').trim();
    return x === '图文详情' || x === '宝贝详情' || x === '详情';
  });
  cands.sort(function(a,b){ return (a.textContent||'').length - (b.textContent||'').length; });
  const el = cands[0];
  if (!el) return JSON.stringify({ ok: false, err: 'tab not found' });
  el.scrollIntoView({ block: 'center' });
  const r = el.getBoundingClientRect();
  const x = r.left + r.width / 2, y = r.top + r.height / 2;
  const mk = function(ex){ return Object.assign({ bubbles: true, cancelable: true, composed: true, clientX: x, clientY: y, button: 0, buttons: 1, view: window, isPrimary: true, pointerId: 1, pointerType: 'mouse' }, ex || {}); };
  ['pointerover','pointerenter','pointerdown'].forEach(function(t){ el.dispatchEvent(new PointerEvent(t, mk())); });
  el.dispatchEvent(new MouseEvent('mousedown', mk()));
  el.dispatchEvent(new PointerEvent('pointerup', mk({ buttons: 0 })));
  el.dispatchEvent(new MouseEvent('mouseup', mk({ buttons: 0 })));
  el.dispatchEvent(new MouseEvent('click', mk({ buttons: 0 })));
  return JSON.stringify({ ok: true });
})()`;

// 详情长图在 [data-src] 上（img.src 是占位 //g.alicdn.com/s.gif），必须步进滚动触发懒加载
const JS_SCROLL_DETAIL = String.raw`(()=>{
  window.__ds = window.__ds || new Set();
  window.__dl = window.__dl || [];
  Array.from(document.querySelectorAll('[data-src]')).forEach(function(e){
    const s = e.getAttribute('data-src') || '';
    if (!/alicdn|taobaocdn|tbcdn/.test(s)) return;
    if (/\.mp4/i.test(s)) return;
    const k = s.replace(/^https?:/, '').replace(/[?&].*$/, '');
    if (!window.__ds.has(k)) { window.__ds.add(k); window.__dl.push(s); }
  });
  window.scrollBy(0, 1200);
  return JSON.stringify({ n: window.__dl.length, y: Math.round(window.scrollY) });
})()`;

const JS_GET_DETAIL = String.raw`(()=>{ return JSON.stringify((window.__dl || []).slice(0, 60)); })()`;

// 「查看全部评价」兜底定位：仅在 page.search 找不到按钮文案时使用（部分页面变体）。
// 主路径必须 page.search 取 ref + page.click 真实点击——合成事件被 isTrusted 检查无视（B=3/C=16 的根因之一）
const JS_OPEN_REVIEWS = String.raw`(()=>{
  let el = document.querySelector('[class*=ShowButton]');
  if (!el) {
    const cands = Array.from(document.querySelectorAll('div,span,a')).filter(function(e){
      return /查看全部评价|全部评价|累计评价/.test(e.textContent || '') && !/footer--/.test(String(e.className));
    });
    cands.sort(function(a,b){ return (a.textContent||'').length - (b.textContent||'').length; });
    el = cands[0];
  }
  if (!el) return JSON.stringify({ ok: false, err: 'button not found' });
  el.scrollIntoView({ block: 'center' });
  const r = el.getBoundingClientRect();
  const x = r.left + r.width / 2, y = r.top + r.height / 2;
  const mk = function(ex){ return Object.assign({ bubbles: true, cancelable: true, composed: true, clientX: x, clientY: y, button: 0, buttons: 1, view: window, isPrimary: true, pointerId: 1, pointerType: 'mouse' }, ex || {}); };
  ['pointerover','pointerenter','pointerdown'].forEach(function(t){ el.dispatchEvent(new PointerEvent(t, mk())); });
  el.dispatchEvent(new MouseEvent('mousedown', mk()));
  el.dispatchEvent(new PointerEvent('pointerup', mk({ buttons: 0 })));
  el.dispatchEvent(new MouseEvent('mouseup', mk({ buttons: 0 })));
  el.dispatchEvent(new MouseEvent('click', mk({ buttons: 0 })));
  return JSON.stringify({ ok: true });
})()`;

// 展开后内联在主布局里的评价卡片数（内联区块硬上限约 22）
const JS_COUNT_COMMENTS = String.raw`String(document.querySelectorAll('[class*="Comment--"]').length)`;

// 内联评价卡片收集器：边滚边采、window.__seenRv 去重（滚动只为让卡片进视口触发渲染，
// 加载本身靠点击展开——直接对容器 scrollTop 滚动不触发懒加载，上轮已证死路）。
// 正文优先 title 属性：textContent 被高亮 span 拆段；本版评价卡不展示 SKU，字段尽量解析、常为空
const JS_COLLECT_REVIEWS = String.raw`(()=>{
  if (!window.__rv) { window.__rv = []; window.__seenRv = new Set(); }
  const box = document.querySelector('[class*="comments--"]');
  if (box) {
    const r = box.getBoundingClientRect();
    window.scrollBy(0, Math.max(300, Math.min(r.bottom, 900)));
  }
  const cards = document.querySelectorAll('[class*="Comment--"]');
  let added = 0;
  cards.forEach(function(c){
    const user = ((c.querySelector('[class*="userName--"]') || {}).textContent || '').trim();
    const dateEl = c.querySelector('[class*="meta--"]');
    const dateRaw = dateEl ? (dateEl.textContent || '').trim() : '';
    const dm = dateRaw.match(/(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})/);
    const date = dm ? (dm[1] + '-' + ('0' + dm[2]).slice(-2) + '-' + ('0' + dm[3]).slice(-2)) : dateRaw.slice(0, 30);
    const contentEl = c.querySelector('[class*="content--"]');
    const content = ((contentEl && contentEl.getAttribute('title')) || (contentEl && contentEl.textContent) || '').trim();
    const imgs = c.querySelectorAll('[class*="album--"] img').length;
    const replyEls = c.querySelectorAll('[class*="reply--"], [class*="Reply--"]');
    const replyEl = replyEls.length ? replyEls[replyEls.length - 1] : null;
    const reply = replyEl ? (replyEl.textContent || '').trim().slice(0, 200) : '';
    const skuRaw = dateRaw.split('已购：')[1] || '';
    const sku = skuRaw.trim().slice(0, 60);
    const key = user + '|' + date + '|' + content.slice(0, 40);
    if (user && !window.__seenRv.has(key)) {
      window.__seenRv.add(key);
      window.__rv.push({ user: user, date: date, sku: sku, content: content, imgs: imgs, reply: reply });
      added++;
    }
  });
  return JSON.stringify({ total: window.__rv.length, added: added });
})()`;

// 一次性导出收集器，避免 shell 中转大 JSON
const JS_EXPORT_REVIEWS = String.raw`JSON.stringify(window.__rv || [])`;

// 搜索卡片：id 取 href 里全部 id= 匹配中最长的数字串（广告跳转链先命中 5~6 位假 id）且 ≥11 位
// （滤掉购物车链接的 10 位 pm_id）；店名必须取卡片容器内 [class*="shopNameText--"]——
// shopName-- 文本混「回头客1万/9年老店」前缀；无店铺字段的不是商品卡，直接跳过
const JS_SEARCH_CARDS = String.raw`(()=>{
  const anchors = Array.from(document.querySelectorAll('a[href*="id="]'));
  const seen = new Set(); const cards = [];
  for (let i = 0; i < anchors.length; i++) {
    const a = anchors[i];
    const ids = [];
    let m; const rx = /id=(\d+)/g;
    while ((m = rx.exec(a.href)) !== null) ids.push(m[1]);
    if (!ids.length) continue;
    ids.sort(function(x, y){ return y.length - x.length; });
    const id = ids[0];
    if (id.length < 11 || seen.has(id)) continue;
    let card = a, shop = '';
    for (let j = 0; j < 12 && card; j++) {
      const s = card.querySelector('[class*="shopNameText--"]');
      if (s) { shop = (s.textContent || '').trim(); break; }
      card = card.parentElement;
    }
    if (!card || !shop) continue;
    const tEl = card.querySelector('[class*="title--"] span, [class*="title--"]');
    const title = tEl ? (tEl.textContent || '').trim().slice(0, 80) : '';
    const sEl = card.querySelector('[class*="realSales--"], [class*="sold--"]');
    const sold = sEl ? (sEl.textContent || '').trim().slice(0, 20) : '';
    seen.add(id);
    cards.push({ rank: cards.length, id: id, shop: shop, title: title, sold: sold });
    if (cards.length >= 5) break;
  }
  return JSON.stringify({ count: cards.length, items: cards });
})()`;

const JS_XHS_CARDS = String.raw`(()=>{
  const cards = Array.from(document.querySelectorAll('section.note-item, .note-item'));
  const out = [];
  cards.forEach(function(c){
    const a = c.querySelector('a[href*=xsec_token]');
    if (!a) return;
    const href = a.getAttribute('href') || '';
    const idm = href.match(/\/(?:search_result|explore)\/([0-9a-f]+)/);
    const tok = href.match(/xsec_token=([^&]+)/);
    if (!idm || !tok) return;
    const t = (c.innerText || '').split('\n').map(function(s){ return s.trim(); }).filter(Boolean);
    out.push({ rank: out.length, id: idm[1], token: tok[1], title: t[0] || '', tail: t.slice(-3).join(' / ') });
  });
  return JSON.stringify(out.slice(0, 30));
})()`;

const JS_XHS_DETAIL = String.raw`(()=>{
  const g = function(s){ const e = document.querySelector(s); return e ? e.innerText.trim() : ''; };
  const title = g('#detail-title') || g('.title');
  const desc = g('.note-text') || g('#detail-desc') || g('.desc');
  const author = g('.author-container .username') || g('[class*=username]');
  const date = g('.bottom-container .date') || g('[class*=date]');
  const like = g('.like-wrapper .count');
  const collect = g('.collect-wrapper .count');
  const cmtCount = g('[class*=chat] .count');
  const comments = Array.from(document.querySelectorAll('.parent-comment')).map(function(c){
    const t = c.querySelector('.content') || c.querySelector('[class*=content]');
    const lk = c.querySelector('[class*=like] .count') || c.querySelector('.like .count');
    const au = c.querySelector('[class*=author]') || c.querySelector('.name');
    return { text: t ? t.innerText.trim() : '', likes: lk ? lk.innerText.trim() : '0', author: au ? au.innerText.trim() : '' };
  });
  return JSON.stringify({ title: title, author: author, date: date, like: like, collect: collect, cmtCount: cmtCount, desc: desc.slice(0, 2000), comments: comments.slice(0, 60) });
})()`;

const JS_XHS_SCROLL = String.raw`(()=>{
  const sels = ['.note-scroller', '.comments-container', '.interaction-container'];
  let sc = null;
  for (let i = 0; i < sels.length; i++) { sc = document.querySelector(sels[i]); if (sc) break; }
  if (sc) sc.scrollTop = sc.scrollHeight;
  window.scrollTo(0, document.body.scrollHeight);
  return JSON.stringify({ ok: !!sc, top: sc ? Math.round(sc.scrollTop) : 0, h: sc ? sc.scrollHeight : 0 });
})()`;

// ---------------------------------------------------------------------------
// 本地工具：图片下载 / 转换（文案提取走 LLM 子会话多模态读图，不用本地 OCR）
// ---------------------------------------------------------------------------

function origImageUrl(u) {
  let s = String(u || '');
  if (s.startsWith('//')) s = 'https:' + s;
  return s.replace(/_\.webp.*$/, '');
}

function downloadImage(url, outFile) {
  try {
    execFileSync('curl', ['-sSL', '--max-time', '30', '-A',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36',
      '-o', outFile, url], { stdio: 'ignore' });
    return existsSync(outFile) && statSize(outFile) > 1024;
  } catch { return false; }
}
function statSize(f) { try { return readFileSync(f).length; } catch { return 0; } }

// 大图直接喂给下游会拖慢转换/内嵌，统一压到 900px 的 jpeg
function toJpeg(inFile, outJpg) {
  try {
    execFileSync('sips', ['-s', 'format', 'jpeg', '-Z', '900', '--out', outJpg, inFile], { stdio: 'ignore' });
    return existsSync(outJpg);
  } catch { return false; }
}

function prepareImages(label, urls, maxN) {
  const dir = join(TMP, 'images', label);
  mkdirSync(dir, { recursive: true });
  const out = [];
  const list = (urls || []).filter((u) => u && !/\.mp4/i.test(u)).slice(0, maxN);
  for (let i = 0; i < list.length; i++) {
    const raw = join(dir, `raw-${i}`);
    const jpg = join(dir, `img-${i}.jpg`);
    if (!downloadImage(origImageUrl(list[i]), raw)) continue;
    if (!toJpeg(raw, jpg)) continue;
    out.push({ index: i, url: list[i], file: jpg, text: '' });
  }
  return out;
}

// ---------------------------------------------------------------------------
// 评价三层分层（规则化，输出真实数字）
// ---------------------------------------------------------------------------

// 归一化：去掉空白与标点，只留文字/数字，避免标点变体影响匹配
function norm(s) { return String(s || '').replace(/[^\p{L}\p{N}]/gu, ''); }

function classifyInvalid(text) {
  const n = norm(text);
  if (!n) return '空评价';
  // ① 系统默认好评（淘宝自动生成的那种）
  if (/该用户觉得商品非常好|此用户没有填写评价|系统默认好评|默认好评/.test(n) && n.length < 40) return '系统默认好评';
  // ① 未使用先评价
  if (/还没用|还未使用|没使用|还没开始用|未使用|还没拆|还没打开/.test(n) && n.length < 15) return '未使用先评价';
  // ① 印象标签拼接句：淘宝印象标签系统把多个 ≤12 字短句用句号拼起来，没有第一人称叙述。
  //    只按句号/分号切（按逗号切会把正常长句误判成标签串），且要命中「挺/不错/够/很」这类评价词。
  const segs = String(text).split(/[。！？!?.；;]/).map((s) => s.trim()).filter((s) => s.length > 0);
  if (segs.length >= 2 && segs.every((s) => norm(s).length <= 12) && segs.some((s) => /挺|不错|够|很/.test(s))
      && !/我|我们|买|收到|下单|用了|回购/.test(n)) return '印象标签拼接句';
  return null;
}

// 最长公共子串（截断到 200 字，避免 O(n²) 爆炸）
function lcsLen(a, b) {
  a = a.slice(0, 200); b = b.slice(0, 200);
  if (!a || !b) return 0;
  const prev = new Uint16Array(b.length + 1);
  const cur = new Uint16Array(b.length + 1);
  let best = 0;
  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      if (a[i - 1] === b[j - 1]) { cur[j] = prev[j - 1] + 1; if (cur[j] > best) best = cur[j]; }
      else cur[j] = 0;
    }
    prev.set(cur.subarray(0, b.length + 1));
    cur.fill(0);
  }
  return best;
}

function classifyReviews(items) {
  // items: [{label, shop, reviews:[{user,date,sku,text,imgCount,reply}]}]
  const flat = [];
  for (const it of items) {
    for (const r of it.reviews) {
      const invalid = classifyInvalid(r.text);
      flat.push({
        label: it.label, shop: it.shop, user: r.user, date: r.date, sku: r.sku, text: r.text,
        imgCount: r.imgCount, reply: r.reply, invalidReason: invalid, normalized: norm(r.text), layer: invalid ? 'invalid' : 'pending',
      });
    }
  }
  const invalidCount = flat.filter((r) => r.layer === 'invalid').length;

  // ② 跨用户归一化公共子串 ≥18 字 → 双方都判疑似刷单（模板复用）
  const cand = flat.filter((r) => r.layer === 'pending');
  const fakePairs = [];
  for (let i = 0; i < cand.length; i++) {
    for (let j = i + 1; j < cand.length; j++) {
      // 同一个买家自己写的两条不算模板复用
      if (cand[i].user && cand[i].user === cand[j].user) continue;
      const L = lcsLen(cand[i].normalized, cand[j].normalized);
      if (L >= 18) {
        cand[i].layer = 'fake'; cand[j].layer = 'fake';
        fakePairs.push({ a: i, b: j, len: L, aText: cand[i].text.slice(0, 60), bText: cand[j].text.slice(0, 60) });
      }
    }
  }
  // ③ 其余全部视为真实（兜住没被前两层命中的）
  for (const r of flat) if (r.layer === 'pending') r.layer = 'real';
  const perItem = {};
  for (const it of items) perItem[it.label] = { total: it.reviews.length, invalid: 0, fake: 0, real: 0 };
  for (const r of flat) if (perItem[r.label]) perItem[r.label][r.layer]++;
  const totals = { total: flat.length, invalid: invalidCount, fake: flat.filter((r) => r.layer === 'fake').length, real: flat.filter((r) => r.layer === 'real').length };
  return { perItem, totals, details: flat, fakePairs };
}

// ---------------------------------------------------------------------------
// 标签频次 × 销量加权
// ---------------------------------------------------------------------------

function weightTags(items) {
  // items: [{label, sold, tags:[{dim,tag,has}]}]
  const map = new Map();
  for (const it of items) {
    for (const t of (it.tags || [])) {
      if (Number(t.has) !== 1) continue;
      const dim = String(t.dim || '其他').trim();
      const tag = String(t.tag || '').trim();
      if (!tag) continue;
      const key = dim + '|' + tag;
      if (!map.has(key)) map.set(key, { dim, tag, cover: 0, weight: 0, by: {} });
      const row = map.get(key);
      row.cover += 1;
      row.weight += Number(it.sold) || 0;
      row.by[it.label] = 1;
    }
  }
  const rows = [...map.values()].sort((a, b) => (b.cover - a.cover) || (b.weight - a.weight));
  return { sold: Object.fromEntries(items.map((i) => [i.label, Number(i.sold) || 0])), rows };
}

// ---------------------------------------------------------------------------
// 采集：单品全管线
// ---------------------------------------------------------------------------

// 候选商品无效（已下架/错误页/缺关键字段）——调用方捕获后顺延到下一个候选，不算整跑失败
class InvalidItemError extends Error {
  constructor(msg) { super(msg); this.name = 'InvalidItemError'; }
}

async function assertNotBlocked(tabId, what) {
  const st = await pageEval(tabId, JS_PAGE_STATE);
  const s = JSON.parse(st);
  if (s.loginWall || s.blocked) {
    const e = new Error(`${what} 被登录墙或访问限制拦截（title="${s.title}"）。请在本机 Chrome 登录淘宝/天猫后重试。`);
    e.fatal = true; // 登录墙必须整个 skill 报错提示用户，不能静默顺延
    throw e;
  }
  return s;
}

// page.search 取「查看全部评价」按钮 refs：页面上常有 2 个文本完全相同的命中，
// 第一个可能是无效元素（validate_3 三品全栽在这里：点第一个 ref 没反应，卡片数停在 2）。
// 必须返回全部精确命中，由调用方逐个试点直到展开数达标（实测 ref_13 无效 / ref_14 才是真按钮）
async function findReviewButtonRefs(tabId) {
  const matches = await relayCall('page.search', { tabId, groupId: GROUP_ID, query: '查看全部评价', maxResults: 12 });
  const arr = Array.isArray(matches) ? matches : (matches.matches || matches.results || []);
  return arr.filter((m) => String(m.text || '').trim() === '查看全部评价').map((m) => m.ref);
}

async function collectItem(label, role, id, url) {
  const tab = await openTab(url, false);
  const tabId = tab.id || tab.tabId;
  try {
    await sleep(10000);
    const st = await assertNotBlocked(tabId, `商品 ${label} 页面`);
    // 候选有效性：已下架商品会跳转到 error.item.taobao.com/noitem（上一版 B 样本就是这种，采出 0 评价 0 标签还自称三品）
    if (/error\.|noitem|\/error\//.test(st.url)) throw new InvalidItemError('页面跳转到宝贝不存在错误页');
    if (/宝贝不存在|很抱歉，您查看的宝贝|页面走丢了|出错了/.test(st.title || '')) {
      throw new InvalidItemError('页面标题为错误提示：' + String(st.title).slice(0, 30));
    }
    const meta = JSON.parse(await pageEval(tabId, JS_META));
    // 缺价格且缺销量 = 不是有效的商品详情页（防错误页推荐位被当成商品 meta）
    if (meta.price == null && meta.sold == null) {
      throw new InvalidItemError('详情页未提取到价格与销量，判为无效商品页');
    }
    const mainImages = JSON.parse(await pageEval(tabId, JS_MAIN_IMAGES));
    await sleep(2000);

    // 详情长图：必须先点「图文详情」再滚，否则 DOM 里只有画廊图
    await pageEval(tabId, JS_CLICK_DETAIL_TAB);
    await sleep(3000);
    let n = 0, stall = 0;
    for (let i = 0; i < 16 && stall < 3; i++) {
      const r = JSON.parse(await pageEval(tabId, JS_SCROLL_DETAIL));
      if (r.n === n) stall++; else { stall = 0; n = r.n; }
      await sleep(2000);
    }
    const detailImages = JSON.parse(await pageEval(tabId, JS_GET_DETAIL));
    await sleep(2000);

    // 评价展开：page.search 取 refs + page.click 真实点击（合成事件被 isTrusted 检查无视）。
    // 关键：同名命中常有 2 个且第一个往往无效（validate_3 根因），必须逐个试点——
    // 每点一个等 4.5s 数卡片数，≥20 即停；一轮全点完仍不足则重取 refs 再来一轮（ref 点击后可能失效）
    await sleep(2000);
    let expanded = 0, reviewClicks = 0;
    for (let round = 0; round < 2 && expanded < 20; round++) {
      let refs = [];
      try { refs = await findReviewButtonRefs(tabId); } catch { refs = []; }
      if (refs.length) {
        for (const ref of refs) {
          if (expanded >= 20) break;
          try { await relayCall('page.click', { tabId, groupId: GROUP_ID, ref }); } catch { continue; }
          reviewClicks++;
          await sleep(4500);
          expanded = Number(await pageEval(tabId, JS_COUNT_COMMENTS)) || 0;
        }
      } else {
        // 兜底：按钮文案定位不到（页面变体）时退回 DOM 定位 + 指针事件序列
        await pageEval(tabId, JS_OPEN_REVIEWS);
        await sleep(4000);
        expanded = Number(await pageEval(tabId, JS_COUNT_COMMENTS)) || 0;
      }
    }
    // 边滚边采：每轮滚动+去重收集，连续 2 轮 added=0 即停（轮间 ≥2s）
    let stallR = 0;
    for (let i = 0; i < 12; i++) {
      const r = JSON.parse(await pageEval(tabId, JS_COLLECT_REVIEWS));
      if (Number(r.added) === 0) { stallR++; if (stallR >= 2) break; } else stallR = 0;
      await sleep(2200);
    }
    const revList = JSON.parse(await pageEval(tabId, JS_EXPORT_REVIEWS) || '[]');

    return {
      label, role, id, url,
      site: /tmall\.com/.test(url) ? '天猫' : '淘宝',
      shop: meta.shop || '', shopId: meta.shopId || '', shopLinkHref: meta.shopLinkHref || '',
      brand: (meta.shop || '').replace(/(旗舰店|专营店|专卖店|官方店|企业店|海外店)$/, '').trim(),
      title: (meta.title || st.title || '').replace(/\s*[-|]\s*(淘宝网|天猫)$/, '').trim(),
      priceText: meta.priceText, price: meta.price,
      soldText: meta.soldText, sold: meta.sold,
      rateCountText: meta.rateCountText, goodRateText: meta.goodRateText,
      skus: meta.skus || [], skuCount: meta.skuCount || 0,
      mainImages, detailImages,
      imageCount: { main: (mainImages || []).length, detail: (detailImages || []).length },
      reviews: (revList || []).map((r) => ({ user: r.user, date: r.date, sku: r.sku || '', text: r.content, imgCount: r.imgs, reply: r.reply, shop: meta.shop || '' })),
      reviewExpanded: expanded, reviewClicks,
    };
  } finally {
    await closeTab(tabId);
  }
}

// ---------------------------------------------------------------------------
// 选品：淘宝搜索 + seeded random
// ---------------------------------------------------------------------------

function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const normShop = (s) => String(s || '').replace(/[\s|·]/g, '');

async function searchTaobao(term) {
  const home = await openTab('https://www.taobao.com', false);
  await sleep(8000);
  const tabId = home.id || home.tabId;
  const searchUrl = 'https://s.taobao.com/search?q=' + encodeURIComponent(term);
  // 首页搜索框真身在 kissy iframe，直接 location.assign 保留 taobao.com referer 才不会丢 q
  await pageEval(tabId, `location.assign(${JSON.stringify(searchUrl)}); 'ok'`);
  await sleep(10000);
  const st = JSON.parse(await pageEval(tabId, JS_PAGE_STATE));
  const cards = JSON.parse(await pageEval(tabId, JS_SEARCH_CARDS));
  if ((cards.count || 0) === 0 || !/淘宝搜索/.test(st.title)) {
    await closeTab(tabId);
    throw new Error(`淘宝搜索「${term}」未拿到结果卡片（title="${st.title}"）。请在本机 Chrome 登录淘宝后重试。`);
  }
  return { tabId, searchUrl, cards: cards.items || [], title: st.title };
}

// 选品顺序：seeded random 落在哪个候选就从哪个开始，之后按下标循环顺延——
// 命中同店/失效/重复候选时跳到下一个并记录，而不是放弃
function pickOrder(top5, rnd) {
  const n = Math.min(5, top5.length);
  const r = rnd();
  const start = Math.floor(r * n);
  const order = [];
  for (let i = 0; i < n; i++) order.push((start + i) % n);
  return { randomValue: r, startIndex: start, order };
}

// ---------------------------------------------------------------------------
// xhs：搜索 → 选帖（子会话）→ 深挖（代码）
// ---------------------------------------------------------------------------

async function xhsSearch(keyword) {
  const t = await openTab('https://www.xiaohongshu.com/explore', false);
  await sleep(8000);
  const tabId = t.id || t.tabId;
  // 首页搜索框现在是 AI 版 textarea，直跳 search_result 才能拿到普通笔记列表
  await pageEval(tabId, `location.href = 'https://www.xiaohongshu.com/search_result?keyword=' + encodeURIComponent(${JSON.stringify(keyword)}) + '&source=web_explore_feed'; 'ok'`);
  await sleep(9000);
  const cardsRaw = await pageEval(tabId, JS_XHS_CARDS);
  return { tabId, keyword, cards: JSON.parse(cardsRaw || '[]') };
}

async function deepDiveNote(note) {
  const url = `https://www.xiaohongshu.com/explore/${note.id}?xsec_token=${encodeURIComponent(note.token)}&xsec_source=pc_search`;
  const t = await openTab(url, false);
  const tabId = t.id || t.tabId;
  try {
    await sleep(9000);
    let best = JSON.parse(await pageEval(tabId, JS_XHS_DETAIL));
    for (let i = 0; i < 3; i++) {
      await pageEval(tabId, JS_XHS_SCROLL);
      await sleep(3000);
      const cur = JSON.parse(await pageEval(tabId, JS_XHS_DETAIL));
      // 评论是懒加载的，保留拿到最多的那次
      if ((cur.comments || []).length >= (best.comments || []).length) best = cur;
    }
    return { ...note, url, ...best };
  } finally {
    await closeTab(tabId);
  }
}

// ---------------------------------------------------------------------------
// 报告
// ---------------------------------------------------------------------------

const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const yn = (v) => (v ? '有' : '—');

function renderReport(ctx) {
  const { items, selection, tagW, cls, xhs, demands, conclusions, focusTerm, seed, productUrl, boundaries } = ctx;
  const L = [];
  const P = (s = '') => L.push(s);
  const totalSold = Object.values(tagW.sold).reduce((a, b) => a + b, 0);

  P('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">');
  P('<title>竞品分析报告 · ' + esc(focusTerm) + '</title>');
  P(`<style>
  :root{--ink:#22303c;--mut:#6a7c8a;--line:#e3e9ed;--mint:#e8f5ee;--mint-d:#2f7d5d;--org:#fdf1e3;--org-d:#c2701f;}
  *{box-sizing:border-box}body{margin:0;font:15px/1.75 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif;color:var(--ink);background:#f7f9fa}
  .wrap{max-width:1100px;margin:0 auto;padding:0 20px 60px}
  header{background:linear-gradient(120deg,var(--mint) 0%,#f4fbf7 55%,var(--org) 100%);padding:34px 0 26px;border-bottom:1px solid var(--line)}
  header .wrap{padding-bottom:0}h1{margin:0 0 8px;font-size:24px}
  .sub{color:var(--mut);font-size:13px}.caliber{margin-top:14px;background:#fff;border-left:4px solid var(--mint-d);padding:10px 14px;border-radius:4px;font-size:14px}
  section{background:#fff;border:1px solid var(--line);border-radius:8px;padding:20px 22px;margin-top:18px}
  h2{margin:0 0 14px;font-size:18px;border-left:4px solid var(--org-d);padding-left:10px}
  h3{margin:18px 0 8px;font-size:15px;color:var(--mint-d)}
  table{width:100%;border-collapse:collapse;font-size:13.5px}
  th,td{border:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}
  th{background:#f2f6f4;white-space:nowrap}
  .muted{color:var(--mut);font-size:13px}
  .tag{display:inline-block;background:var(--mint);color:var(--mint-d);border-radius:3px;padding:1px 7px;margin:2px 3px 2px 0;font-size:12.5px}
  .quote{background:#fbfcfd;border-left:3px solid var(--line);padding:6px 10px;margin:5px 0;font-size:13.5px;color:#3c4c58}
  .kpi{display:flex;gap:12px;flex-wrap:wrap;margin:10px 0}
  .kpi div{background:#f4f8f6;border:1px solid var(--line);border-radius:6px;padding:8px 14px;font-size:13.5px}
  .kpi b{font-size:18px;color:var(--mint-d)}
  .imgs{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px}
  .imgs figure{margin:0;width:210px}
  .imgs img{width:100%;border:1px solid var(--line);border-radius:4px;display:block}
  .imgs figcaption{font-size:12px;color:var(--mut);margin-top:4px}
  ul{margin:6px 0;padding-left:20px}li{margin:3px 0}
  </style></head><body>`);

  P('<header><div class="wrap">');
  P('<h1>竞品分析报告 · ' + esc(focusTerm) + '</h1>');
  P('<div class="sub">起点商品：' + esc(productUrl) + ' ｜ 选品种子 seed=' + esc(seed) + ' ｜ 生成时间：' + esc(new Date().toISOString().slice(0, 10)) + ' ｜ 写给电商运营同学</div>');
  P('<div class="caliber"><b>判定口径（一句话）：</b>本报告只依据三品页面采集到的图片文案标签、真实评价原话与小红书评论原话做判断——供给重叠 = 三品中 3/3 打到的标签且销量加权高；待补内容 = 三品覆盖 ≤1/3、但在真实评价或小红书评论里有人明确提出的需求。</div>');
  P('</div></header><div class="wrap">');

  // 1 样本构成
  P('<section><h2>1. 样本构成（含种子）</h2>');
  P('<table><tr><th>样本</th><th>角色</th><th>商品ID</th><th>平台</th><th>店铺 / 品牌</th><th>到手价</th><th>销量口径</th><th>评价数</th><th>SKU数</th><th>主图/详情图</th></tr>');
  for (const k of ['A', 'B', 'C']) {
    const it = items[k];
    if (!it) {
      const perr = (selection.picks || []).find((p) => p.label === k && p.error);
      P(`<tr><td>${k}</td><td colspan="9">未采集到（${esc(perr ? perr.error : '原因见边界说明')}）</td></tr>`);
      continue;
    }
    P(`<tr><td><b>${k}</b></td><td>${esc(it.role)}</td><td>${esc(it.id)}</td><td>${esc(it.site)}</td><td>${esc(it.shop)} / ${esc(it.brand)}</td><td>${esc(it.priceText || '未提取')}</td><td>${esc(it.soldText || '未提取')}</td><td>${esc(it.rateCountText || '未提取')}</td><td>${esc(it.skuCount)}</td><td>${esc(it.imageCount.main)} / ${esc(it.imageCount.detail)}</td></tr>`);
  }
  P('</table>');
  P('<h3>1.1 选品记录</h3>');
  P('<ul>');
  P('<li>聚焦搜索词：<b>' + esc(focusTerm) + '</b>' + (selection.focusSource ? '（' + esc(selection.focusSource) + '）' : '') + '</li>');
  P('<li>随机种子 seed：<b>' + esc(seed) + '</b>（mulberry32，用于前 5 选 1，可复现）</li>');
  P('<li>搜索 URL：<span class="muted">' + esc(selection.searchUrl || '') + '</span></li>');
  P('</ul>');
  P('<table><tr><th>#</th><th>商品ID</th><th>卡片标题</th><th>店铺</th><th>卡片销量</th><th>选取情况</th></tr>');
  (selection.top5 || []).forEach((c, i) => {
    const hit = (selection.picks || []).find((p) => p.index === i && !p.error);
    const skipList = (selection.skips || []).filter((s) => s.index === i);
    const skipTxt = skipList.map((s) => `${s.label ? s.label + ':' : ''}顺延跳过（${s.reason}）`).join('；');
    let mark = '未选';
    if (hit && skipTxt) mark = skipTxt + '；后选为 ' + hit.label + '（随机数 ' + Number(hit.randomValue).toFixed(4) + '）';
    else if (hit) mark = '选为 ' + hit.label + '（随机数 ' + Number(hit.randomValue).toFixed(4) + '）';
    else if (skipTxt) mark = skipTxt;
    P(`<tr><td>${i + 1}</td><td>${esc(c.id)}</td><td>${esc(String(c.title || '').slice(0, 60))}</td><td>${esc(c.shopGuess || '未识别')}</td><td>${esc(c.soldText || '')}</td><td>${esc(mark)}</td></tr>`);
  });
  P('</table>');
  P('<p class="muted">选品规则：seeded random 定起点后顺延扫描；同店（先比卡片店名，再以详情页 shopId 为准核实）、失效商品（详情页核实为宝贝不存在或缺关键字段）、重复候选都跳过并记录；品牌 / 价格档 / 销量档不做事前配平，自然错开。</p>');
  P('</section>');

  // 2 频次 × 销量加权
  P('<section><h2>2. 图片文案标签：频次 × 销量加权</h2>');
  P('<p class="muted">标签来自三品主图与详情长图的文案（图片文案机器提取后打标）；权重 = 打到该标签的样本销量之和（销量取页面「已售 N+」），销量合计 ' + esc(totalSold.toLocaleString()) + '。</p>');
  P('<table><tr><th>维度</th><th>标签</th><th>A</th><th>B</th><th>C</th><th>覆盖</th><th>销量加权</th><th>占合计</th></tr>');
  for (const r of (tagW.rows || []).slice(0, 40)) {
    P(`<tr><td>${esc(r.dim)}</td><td>${esc(r.tag)}</td><td>${yn(r.by.A)}</td><td>${yn(r.by.B)}</td><td>${yn(r.by.C)}</td><td>${r.cover}/3</td><td>${esc(r.weight.toLocaleString())}</td><td>${totalSold ? ((r.weight / totalSold) * 100).toFixed(1) + '%' : '—'}</td></tr>`);
  }
  P('</table>');
  const overlap = (tagW.rows || []).filter((r) => r.cover === 3).slice(0, 12);
  P('<h3>供给重叠区（三品全都打到的标签）</h3>');
  P(overlap.length
    ? '<p>' + overlap.map((r) => '<span class="tag">' + esc(r.dim) + '·' + esc(r.tag) + '</span>').join('') + '</p>'
    : '<p class="muted">本次没有 3/3 全覆盖的标签。</p>');
  const thin = (tagW.rows || []).filter((r) => r.cover <= 1).slice(0, 12);
  P('<h3>覆盖稀薄区（≤1/3 打到）</h3>');
  P(thin.length
    ? '<p>' + thin.map((r) => '<span class="tag">' + esc(r.dim) + '·' + esc(r.tag) + '</span>').join('') + '</p>'
    : '<p class="muted">本次没有覆盖 ≤1/3 的标签。</p>');
  P('</section>');

  // 3 评价分层
  P('<section><h2>3. 评价分层结果（规则跑出来的真实数字）</h2>');
  P('<div class="kpi">');
  P(`<div>采集总条数 <b>${esc(cls.totals.total)}</b></div>`);
  P(`<div>① 无效忽略 <b>${esc(cls.totals.invalid)}</b></div>`);
  P(`<div>② 疑似刷单剔除 <b>${esc(cls.totals.fake)}</b></div>`);
  P(`<div>③ 视为真实 <b>${esc(cls.totals.real)}</b></div>`);
  P(`<div>真实占比 <b>${cls.totals.total ? ((cls.totals.real / cls.totals.total) * 100).toFixed(1) + '%' : '—'}</b></div>`);
  P('</div>');
  P('<table><tr><th>样本</th><th>店铺</th><th>采集</th><th>①无效（忽略，不计分母）</th><th>②疑似刷单（剔除）</th><th>③真实</th></tr>');
  for (const k of ['A', 'B', 'C']) {
    const p = cls.perItem[k];
    if (!p) { P(`<tr><td>${k}</td><td colspan="5">未采集</td></tr>`); continue; }
    const shop = items[k] ? items[k].shop : '';
    P(`<tr><td><b>${k}</b></td><td>${esc(shop)}</td><td>${esc(p.total)}</td><td>${esc(p.invalid)}</td><td>${esc(p.fake)}</td><td>${esc(p.real)}</td></tr>`);
  }
  P('</table>');
  P('<p class="muted">规则：① 系统默认好评 / 未使用先评价 / 印象标签拼接句 → 忽略，不计入分母；② 跨用户归一化后最长公共子串 ≥18 字 → 视为模板复用，双方剔除；③ 其余全部视为真实。</p>');
  const invSamples = cls.details.filter((d) => d.layer === 'invalid').slice(0, 6);
  if (invSamples.length) {
    P('<h3>被判无效的例子</h3>');
    invSamples.forEach((d) => P(`<div class="quote">[${esc(d.label)}·${esc(d.shop)}] ${esc(d.text.slice(0, 70))} <span class="muted">— ${esc(d.invalidReason)}</span></div>`));
  }
  if ((cls.fakePairs || []).length) {
    P('<h3>被判疑似刷单的配对（公共子串长度）</h3>');
    cls.fakePairs.slice(0, 6).forEach((p) => P(`<div class="quote">公共子串 ${esc(p.len)} 字：${esc(p.aText)} ｜ ${esc(p.bText)}</div>`));
  }
  P('</section>');

  // 4 满足度
  P('<section><h2>4. 真实评价满足度表</h2>');
  if (!demands || !demands.demands || !demands.demands.length) {
    P('<p class="muted">未拿到（原因：需求归纳子会话未返回结果）。原始评价与笔记评论已落盘在 data/ 下，可重跑该步。</p>');
  } else {
    P('<table><tr><th>需求点</th><th>证据（原话 / 店别 / 条数）</th><th>A</th><th>B</th><th>C</th><th>说明</th></tr>');
    for (const d of demands.demands) {
      const ev = (d.evidence || []).slice(0, 4).map((e) => `<div class="quote">${esc(e.text)} <span class="muted">— ${esc(e.src)}${e.where ? ' / ' + esc(e.where) : ''} / ${esc(e.n)} 条</span></div>`).join('');
      P(`<tr><td><b>${esc(d.q)}</b></td><td>${ev || '—'}</td><td>${yn(d.cover && d.cover.A)}</td><td>${yn(d.cover && d.cover.B)}</td><td>${yn(d.cover && d.cover.C)}</td><td>${esc(d.coverNote || '')}</td></tr>`);
    }
    P('</table>');
  }
  P('</section>');

  // 5 xhs
  P('<section><h2>5. 小红书同词需求原话</h2>');
  if (!xhs || !xhs.notes || !xhs.notes.length) {
    P('<p class="muted">未拿到（原因：小红书采集失败）。</p>');
  } else {
    P('<p class="muted">检索词：' + esc((xhs.keywords || []).join(' / ')) + ' ｜ 命中卡片 ' + esc(xhs.cardCount) + ' 张 ｜ 深挖 ' + esc(xhs.notes.length) + ' 篇</p>');
    for (const n of xhs.notes) {
      P('<h3>' + esc(n.title || '(无标题)') + ' <span class="muted">— ' + esc(n.author || '') + ' / 赞 ' + esc(n.like || '0') + ' / 评论 ' + esc(n.cmtCount || '0') + '</span></h3>');
      P('<div class="quote">笔记正文：' + esc(String(n.desc || '').slice(0, 300) || '（正文主要在图片里 / 只有话题标签）') + '</div>');
      (n.comments || []).slice(0, 8).forEach((c) => P(`<div class="quote">${esc(String(c.text).slice(0, 160))} <span class="muted">— 评论 @${esc(c.author || '匿名')}</span></div>`));
    }
    if ((xhs.rejected || []).length) {
      P('<h3>被剔除的笔记</h3><ul>');
      xhs.rejected.slice(0, 8).forEach((r) => P(`<li>${esc(r.title || r.id)} — ${esc(r.reason)}</li>`));
      P('</ul>');
    }
  }
  P('</section>');

  // 6 结论
  P('<section><h2>6. 结论表（证据 → 运营含义 → 可做的事）</h2>');
  if (!conclusions || !conclusions.rows || !conclusions.rows.length) {
    P('<p class="muted">未拿到（原因：结论归纳子会话未返回结果）。</p>');
  } else {
    P('<table><tr><th>证据</th><th>运营含义</th><th>可做的事</th></tr>');
    for (const r of conclusions.rows) P(`<tr><td>${esc(r.evidence)}</td><td>${esc(r.meaning)}</td><td>${esc(r.actions)}</td></tr>`);
    P('</table>');
  }
  P('</section>');

  // 7 关键图
  P('<section><h2>7. 三品关键图（各 2~4 张）</h2>');
  for (const k of ['A', 'B', 'C']) {
    const it = items[k];
    if (!it) continue;
    P('<h3>' + esc(k) + ' · ' + esc(it.shop) + ' · ' + esc(String(it.title).slice(0, 40)) + '</h3>');
    P('<div class="imgs">');
    (it.keyImages || []).forEach((im) => P(`<figure><img src="data:image/jpeg;base64,${im.b64}" alt=""><figcaption>${esc(im.kind)}</figcaption></figure>`));
    P('</div>');
  }
  P('</section>');

  // 8 边界
  P('<section><h2>8. 边界说明</h2><ul>');
  boundaries.forEach((b) => P('<li>' + esc(b) + '</li>'));
  P('</ul></section>');

  P('</div></body></html>');
  return L.join('\n');
}

// ---------------------------------------------------------------------------
// 主流程
// ---------------------------------------------------------------------------

async function loadInput() {
  const p = process.argv[2];
  if (p && existsSync(p)) return JSON.parse(readFileSync(p, 'utf-8'));
  if (process.env.WC3_INPUT_JSON) return JSON.parse(process.env.WC3_INPUT_JSON);
  if (!process.stdin.isTTY) {
    const chunks = [];
    for await (const c of process.stdin) chunks.push(c);
    const s = Buffer.concat(chunks).toString('utf-8').trim();
    if (s) return JSON.parse(s);
  }
  return {};
}

async function main() {
  mkdirSync(TMP, { recursive: true });
  const input = await loadInput();
  const productUrl = input.productUrl || input.product_url || input.url;
  if (!productUrl) throw new Error('缺少必填入参 productUrl');
  const searchTermInput = (input.searchTerm || input.search_term || '').trim();
  const today = new Date();
  const seed = Number(input.seed ?? Number(`${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, '0')}${String(today.getDate()).padStart(2, '0')}`));
  const outputDir = input.outputDir || input.output_dir || join(process.cwd(), '.workbuddy/output/tb-opportunity-radar-run');
  const dataDir = join(outputDir, 'data');
  mkdirSync(dataDir, { recursive: true });

  const failures = [];
  await ensureRelay();
  const g = await relayCall('group.create', { name: 'tb-opportunity-radar' });
  GROUP_ID = g.groupId;

  const idMatch = String(productUrl).match(/id=(\d{6,})/) || String(productUrl).match(/(\d{10,})/);
  const itemId = idMatch ? idMatch[1] : '';

  // --- 1~7：起点商品 A 全量采集 ---
  let A;
  try {
    A = await collectItem('A', '起点商品（入参）', itemId, productUrl);
  } catch (e) {
    throw new Error(`起点商品 A 采集失败（${e.message}）。请确认链接有效；若被登录墙拦截，请在 Chrome 登录淘宝后重试。`);
  }
  if (!A.title) throw new Error('商品 A 页面未取到标题，可能被登录墙拦截。请在本机 Chrome 登录淘宝/天猫后重试。');
  writeFileSync(join(dataDir, 'item-A.json'), JSON.stringify(A, null, 2));

  // --- 8：聚焦搜索词（子会话判断"聚焦不泛"）---
  let focusTerm = searchTermInput;
  let focusSource = searchTermInput ? '入参 searchTerm 指定' : '从商品标题/类目自动猜（子会话）';
  if (!focusTerm) {
    try {
      const r = await llmJson('term', `你是电商类目分析助手。下面是一个淘宝/天猫商品的标题与规格信息，请给出**一个聚焦搜索词**，用于在同一类目里找到最可比的竞品。

要求：
- 结构优先「品类词 + 关键规格」，例如品类是遮盖液、规格是防水型，就给「白斑遮盖液」这类词。
- 词要聚焦、不要太泛（不要用「护肤品」「神器」这种），否则搜出来的商品和它差距太大，比较失去意义。
- 只输出一个词，2~8 个汉字，不要标点、不要解释。

商品标题：${A.title}
店铺：${A.shop}
SKU 片段：${(A.skus || []).slice(0, 8).join(' / ')}

返回 JSON：{"term":"...","reason":"..."}`,
        JSON.stringify({ type: 'object', properties: { term: { type: 'string' }, reason: { type: 'string' } }, required: ['term'] }));
      focusTerm = String(r.term || '').trim();
      if (!focusTerm) throw new Error('子会话没给出搜索词');
    } catch (e) {
      // 聚焦词猜不出来就只能退回标题核心词，不能硬造
      focusTerm = String(A.title || '').replace(/[【】\[\]()（）]/g, ' ').split(/\s+/).filter(Boolean).slice(0, 1).join('') || '';
      focusSource = '子会话失败，退回标题首词（' + e.message.slice(0, 60) + '）';
      failures.push('guess-term: ' + e.message.slice(0, 80));
      if (!focusTerm) throw new Error('无法从商品标题推导聚焦搜索词，请在入参 searchTerm 指定');
    }
  }

  // --- 9~11：搜索 + seeded 随机选 B/C（失效/同店候选顺延并记录）---
  const search = await searchTaobao(focusTerm);
  await closeTab(search.tabId);
  // 搜索卡片已带结构化店名（shopNameText--）；shopId 要等详情页核实才有——同店排除两级比对
  const top5 = search.cards.slice(0, 5).map((c, i) => ({ index: i, id: c.id, shopGuess: c.shop, title: c.title, soldText: c.sold }));
  const rnd = mulberry32(Number(seed));
  const usedId = new Set([String(A.id || itemId)]);
  const usedShop = new Set([normShop(A.shop)].filter(Boolean));
  const usedShopIds = new Set([String(A.shopId || '')].filter(Boolean));
  const picks = [], skips = [];
  const items = { A };
  const host = /tmall\.com/.test(productUrl) ? 'https://detail.tmall.com/item.htm' : 'https://item.taobao.com/item.htm';

  for (const label of ['B', 'C']) {
    if (!top5.length) { picks.push({ label, error: '搜索结果无可选候选' }); continue; }
    const { randomValue, startIndex, order } = pickOrder(top5, rnd);
    let chosen = null;
    for (const idx of order) {
      const cand = top5[idx];
      const base = { label, index: idx, id: cand.id, shop: cand.shopGuess };
      if (usedId.has(String(cand.id))) { skips.push({ ...base, reason: '与已选商品重复' }); continue; }
      if (cand.shopGuess && usedShop.has(normShop(cand.shopGuess))) { skips.push({ ...base, reason: '与已选商品同店' }); continue; }
      try {
        // collectItem 内部做候选有效性核验（错误页/缺价格销量 → InvalidItemError），失败也顺延到下一个候选
        const it = await collectItem(label, label === 'B' ? '搜索随机命中（排除同店/失效后顺延）' : '搜索随机命中', cand.id, `${host}?id=${cand.id}`);
        // 详情页核实的 shopId（主键）/店名若与已选冲突，同样顺延并记录——上一版 shop 采空导致这步永不触发
        const sameShop = (it.shopId && usedShopIds.has(it.shopId)) || (it.shop && usedShop.has(normShop(it.shop)));
        if (sameShop) {
          skips.push({ ...base, shop: it.shop, shopId: it.shopId, reason: '与已选商品同店（详情页核实）' });
          continue;
        }
        chosen = { label, index: idx, id: cand.id, shopGuess: cand.shopGuess, title: cand.title, soldText: cand.soldText, randomValue, startIndex };
        usedId.add(String(cand.id));
        if (it.shopId) usedShopIds.add(it.shopId);
        if (it.shop) usedShop.add(normShop(it.shop));
        it.pickInfo = { index: idx, randomValue };
        items[label] = it;
        writeFileSync(join(dataDir, `item-${label}.json`), JSON.stringify(it, null, 2));
        break;
      } catch (e) {
        if (e.fatal) throw e; // 登录墙/访问限制：整跑报错提示用户，不静默顺延
        skips.push({
          ...base,
          reason: (e instanceof InvalidItemError ? '候选商品无效：' : '候选采集失败：') + String(e.message).slice(0, 60),
        });
        continue;
      }
    }
    if (!chosen) picks.push({ label, error: '前 5 候选均不可用（失效/同店/重复，明细见 skips）' });
    else picks.push(chosen);
  }

  const labels = ['A', 'B', 'C'].filter((k) => items[k]);
  const selection = {
    seed, focusTerm, focusSource, searchUrl: search.searchUrl, searchTitle: search.title,
    top5, picks, skips,
    rules: { filter: '前 5 候选中 seeded random（mulberry32）定起点后顺延扫描；跳过条件 = 同店、候选失效（错误页/缺关键字段，详情页核实）、重复，全部记录在 skips' },
  };
  writeFileSync(join(dataDir, 'selection.json'), JSON.stringify(selection, null, 2));

  // --- 13~14：图片下载（文案提取合并进第 15 步：LLM 子会话多模态读图，不用本地 OCR）---
  for (const k of labels) {
    const it = items[k];
    const mains = prepareImages(k + '-main', it.mainImages, 6);
    const details = prepareImages(k + '-detail', it.detailImages, 8);
    it.mainOcr = '';
    it.detailOcr = '';
    it.ocr = { main: '', detail: '' };
    // 报告内嵌关键图：主图前 3 张；不足则用详情图补齐（2~4 张）
    const keySrc = [...mains.slice(0, 3), ...details.slice(0, 4 - Math.min(3, mains.length))];
    it.keyImages = keySrc.slice(0, 4).map((m) => ({
      kind: m.file.includes('-main') ? '主图' : '详情图',
      b64: Buffer.from(readFileSync(m.file)).toString('base64'),
    }));
    writeFileSync(join(dataDir, `item-${k}.json`), JSON.stringify(it, null, 2));
  }

  // --- 15：七维打标（LLM 子会话多模态直接读图提取文案 + 判断标签归属；pipeline 后端模型已支持图片）---
  const DIM_HINT = '人群 / 环境 / 作用 / 形态 / 成分 / 保障 / 体验';
  const tagResults = await pMap(labels, async (k) => {
    const it = items[k];
    const mainFiles = [], detailFiles = [];
    try {
      const d = join(TMP, 'images', k + '-main'); if (existsSync(d)) mainFiles.push(...readdirSync(d).filter((f) => f.endsWith('.jpg')).slice(0, 6).map((f) => join(d, f)));
      const d2 = join(TMP, 'images', k + '-detail'); if (existsSync(d2)) detailFiles.push(...readdirSync(d2).filter((f) => f.endsWith('.jpg')).slice(0, 8).map((f) => join(d2, f)));
    } catch { /* 图片目录不存在就算了 */ }
    const imgFiles = [...mainFiles, ...detailFiles];
    const prompt = `你是电商商品卖点分析师。目标商品：淘宝/天猫「${it.title}」（店铺：${it.shop}）。

第一步——用 Read 工具逐张读取以下本地图片文件（多模态读图），提取每张图上的文案（主标题/卖点/参数/促销语，按出现顺序整理为一段通顺文字，看不清的字不要编造）：
${imgFiles.map((f, i) => `${i + 1}. ${f}`).join('\n') || '（无图片文件，直接凭下方文本判断）'}

第二步——基于你提取的文案，按七个维度打标：${DIM_HINT}。
- has=1 表示文案里明确表达了该标签；has=0 表示没出现。不要凭常识脑补，只认文案里有的。
- 标签名用 2~6 个汉字，同一维度下不同商品尽量用相同的标签名，方便横向比较（例如「防水」「遮盖力」「教程指导」）。
- evidence 填支持该判断的原文片段（≤30 字）。
- 每个维度可以打 0~3 个标签，全都没提到就留空。

返回 JSON：
{"tags":[{"dim":"人群","tag":"...","has":1,"evidence":"..."}],
 "imageCopy":[{"img":"文件路径","text":"该图提取的文案"}]}`;
    const r = await llmJson(`tag-${k}`, prompt, JSON.stringify({
      type: 'object',
      properties: {
        tags: { type: 'array', items: { type: 'object', properties: { dim: { type: 'string' }, tag: { type: 'string' }, has: { type: 'number' }, evidence: { type: 'string' } }, required: ['dim', 'tag', 'has'] } },
        imageCopy: { type: 'array', items: { type: 'object', properties: { img: { type: 'string' }, text: { type: 'string' } }, required: ['img', 'text'] } },
      },
      required: ['tags'],
    }));
    // 回填文案（字段名保留 mainOcr/detailOcr，下游 data.md 与报告无需改动；语义=LLM 读图提取的文案）
    const copyMap = new Map((r.imageCopy || []).map((c) => [String(c.img || ''), String(c.text || '')]));
    const lookup = (f) => copyMap.get(f) ?? [...copyMap.entries()].find(([p]) => p.endsWith('/' + f.split('/').pop()))?.[1] ?? '';
    const fmt = (files, tag) => files.map((f, i) => {
      const t = lookup(f);
      return t ? `[${tag}${i + 1}] ${t}` : '';
    }).filter(Boolean).join('\n').slice(0, 4000);
    it.mainOcr = fmt(mainFiles, '主图');
    it.detailOcr = fmt(detailFiles, '详情图');
    it.ocr = { main: it.mainOcr, detail: it.detailOcr };
    writeFileSync(join(dataDir, `item-${k}.json`), JSON.stringify(it, null, 2));
    return { label: k, tags: (r.tags || []).filter((t) => t && t.tag) };
  });
  for (const r of tagResults) {
    if (r.status === 'fulfilled') { items[r.value.label].tags = r.value.tags; }
    else {
      const k = labels[tagResults.indexOf(r)];
      items[k].tags = [];
      failures.push(`tag-${k}: ${String(r.reason).slice(0, 80)}`);
    }
  }
  const tagW = weightTags(labels.map((k) => ({ label: k, sold: items[k].sold, tags: items[k].tags || [] })));
  writeFileSync(join(dataDir, 'tag-matrix.json'), JSON.stringify({ sold: tagW.sold, rows: tagW.rows, items: Object.fromEntries(labels.map((k) => [k, items[k].tags || []])) }, null, 2));

  // --- 17：评价三层分层 ---
  const cls = classifyReviews(labels.map((k) => ({ label: k, shop: items[k].shop, reviews: items[k].reviews || [] })));
  writeFileSync(join(dataDir, 'review-classify.json'), JSON.stringify({
    rules: {
      invalid: '系统默认好评 / 未使用先评价 / 印象标签拼接句 → 忽略，不计入分母',
      fake: '跨用户归一化后最长公共子串 ≥18 字 → 视为模板复用，双方剔除',
      real: '其余全部视为真实',
    },
    totals: cls.totals, perItem: cls.perItem, fakePairs: cls.fakePairs, details: cls.details,
  }, null, 2));
  for (const k of labels) {
    const byLabel = cls.details.filter((d) => d.label === k);
    const md = [`# ${k} · ${items[k].shop} · 评价采集明细`, '',
      `- 商品：${items[k].title}`,
      `- 采集条数：${(items[k].reviews || []).length}（页面显示评价数：${items[k].rateCountText || '未提取'}）`,
      `- 分层结果：无效 ${cls.perItem[k].invalid} / 疑似刷单 ${cls.perItem[k].fake} / 真实 ${cls.perItem[k].real}`,
      '', '| # | 用户 | 日期 | SKU | 正文 | 图 | 商家回复 | 分层 |', '|---|---|---|---|---|---|---|---|'];
    (items[k].reviews || []).forEach((r, i) => {
      const d = byLabel[i] || {};
      md.push(`| ${i + 1} | ${r.user} | ${r.date} | ${r.sku} | ${String(r.text).replace(/\n/g, ' ').slice(0, 120)} | ${r.imgCount} | ${String(r.reply || '').replace(/\n/g, ' ').slice(0, 60)} | ${d.layer === 'invalid' ? '无效·' + d.invalidReason : (d.layer === 'fake' ? '疑似刷单' : '真实')} |`);
    });
    mkdirSync(join(dataDir, 'reviews', k), { recursive: true });
    writeFileSync(join(dataDir, 'reviews', k, 'reviews.md'), md.join('\n'));
  }

  // 验收底线自检：每品评价 ≥20 条；页面评价总数本身不足的算「到底」，不算缺
  const parseCount = (s) => { const m = String(s || '').replace(/,/g, '').match(/^([\d.]+)(万)?\+?\s*条?$/); return m ? Math.round(parseFloat(m[1]) * (m[2] ? 10000 : 1)) : null; };
  for (const k of labels) {
    const got = (items[k].reviews || []).length;
    const pageTotal = parseCount(items[k].rateCountText);
    if (got < 20 && !(pageTotal != null && pageTotal <= got)) {
      failures.push(`review-short-${k}: 仅 ${got} 条（页面显示 ${items[k].rateCountText || '?'}），未到底`);
    }
  }

  // --- 24：变体词（子会话从类目语义派生）---
  let variantTerm = '';
  try {
    const v = await llmJson('variant', `聚焦搜索词是「${focusTerm}」，起点商品标题是「${A.title}」。
请给出 1 个**同义/近义的变体搜索词**，用于在小红书找同一批用户的需求讨论（用户口语里常用的另一种说法，例如俗称、别名、场景词）。
只输出一个词，2~8 个汉字，不要标点。
返回 JSON：{"term":"...","reason":"..."}`,
      JSON.stringify({ type: 'object', properties: { term: { type: 'string' }, reason: { type: 'string' } }, required: ['term'] }));
    variantTerm = String(v.term || '').trim();
  } catch (e) { failures.push('variant-term: ' + String(e.message).slice(0, 80)); }
  const xhsKeywords = [focusTerm, variantTerm].filter(Boolean);

  // --- 18~20：xhs 搜索（每个词开新 tab）+ 选帖（子会话）+ 深挖（代码）---
  let xhs = { keywords: xhsKeywords, cardCount: 0, notes: [], rejected: [] };
  const siteHint = process.env.WC3_SITE_KNOWLEDGE ? join(process.env.WC3_SITE_KNOWLEDGE, 'xiaohongshu.md') : '';
  try {
    const allCards = [];
    for (const kw of xhsKeywords) {
      try {
        const s = await xhsSearch(kw);
        for (const c of s.cards) if (!allCards.find((x) => x.id === c.id)) allCards.push({ ...c, keyword: kw });
        await closeTab(s.tabId);
      } catch (e) { failures.push(`xhs-search-${kw}: ${String(e.message).slice(0, 80)}`); }
    }
    xhs.cardCount = allCards.length;
    if (allCards.length) {
      const pickPrompt = `${siteHint ? `开始前先 Read \`${siteHint}\` 获取小红书站点选择器与页面行为经验。\n\n` : ''}你是需求调研助手。检索词：${xhsKeywords.join(' / ')}（这是${focusTerm}品类的用户需求检索）。
下面是小红书搜索结果卡片（rank / id / 标题 / 作者与赞数尾部信息）。请挑出 **内容确实在讨论这个品类** 的普通图文笔记，用于深挖评论区获取需求原话。

挑选规则：
- 标题或作者信息里要能看出与「${focusTerm}」相关（词命中），再看评论数（评论密度）优先。
- 剔除「话题标签命中但内容无关」的误命中（例如同名词条是别的领域、泛美白/泛医疗科普、广告帖），并写明原因。
- 优先普通图文帖，避开合集/视频帖。
- 至少选 2 篇，最多 4 篇。

卡片列表：
${allCards.slice(0, 24).map((c) => `[${c.rank}] id=${c.id} 标题=${c.title} 尾部=${c.tail}`).join('\n')}

返回 JSON：{"picked":[0,2],"rejected":[{"idx":1,"title":"...","reason":"..."}]}`;
      const pick = await llmJson('xhs-pick', pickPrompt, JSON.stringify({
        type: 'object',
        properties: { picked: { type: 'array', items: { type: 'number' } }, rejected: { type: 'array', items: { type: 'object', properties: { idx: { type: 'number' }, title: { type: 'string' }, reason: { type: 'string' } } } } },
        required: ['picked'],
      }));
      const pickedIdx = (pick.picked || []).filter((i) => allCards[i]).slice(0, 4);
      const rejIdx = new Set(pickedIdx);
      xhs.rejected = (pick.rejected || []).map((r) => ({ title: r.title || (allCards[r.idx] ? allCards[r.idx].title : ''), reason: r.reason }));
      if (!rejIdx.size) xhs.rejected.push({ title: '', reason: '子会话未返回可深挖的笔记' });
      for (const i of pickedIdx) {
        try {
          const note = await deepDiveNote(allCards[i]);
          xhs.notes.push({ ...note, keyword: allCards[i].keyword });
        } catch (e) { failures.push(`xhs-note-${allCards[i].id}: ${String(e.message).slice(0, 80)}`); }
      }
    }
  } catch (e) { failures.push('xhs: ' + String(e.message).slice(0, 120)); }

  const jsonl = [];
  jsonl.push({ type: 'search', keywords: xhsKeywords, cardCount: xhs.cardCount, focusTerm });
  for (const n of xhs.notes) jsonl.push({ type: 'note', id: n.id, keyword: n.keyword, title: n.title, author: n.author, date: n.date, like: n.like, collect: n.collect, cmtCount: n.cmtCount, desc: n.desc, url: n.url });
  for (const n of xhs.notes) for (const c of (n.comments || [])) jsonl.push({ type: 'comment', noteId: n.id, noteTitle: n.title, author: c.author, likes: c.likes, text: c.text });
  for (const r of xhs.rejected) jsonl.push({ type: 'rejected', ...r });

  // --- 21：需求点 + 满足度（子会话）---
  let demands = null;
  try {
    const realByLabel = {};
    for (const k of labels) realByLabel[k] = cls.details.filter((d) => d.label === k && d.layer === 'real');
    const reviewBlock = labels.map((k) => `【${k}·${items[k].shop}】真实评价 ${realByLabel[k].length} 条：\n` +
      realByLabel[k].slice(0, 22).map((d, i) => `${i + 1}. (${d.date}${d.sku ? ' / ' + d.sku : ''}) ${String(d.text).slice(0, 220)}`).join('\n')).join('\n\n');
    const xhsBlock = (xhs.notes || []).map((n) => `【笔记】${n.title}（${n.author} / 赞${n.like} / 评论${n.cmtCount}）\n正文：${String(n.desc || '').slice(0, 500)}\n评论原话：\n` +
      (n.comments || []).slice(0, 20).map((c) => `- ${String(c.text).slice(0, 180)}`).join('\n')).join('\n\n');
    const tagBlock = labels.map((k) => `【${k}】` + (items[k].tags || []).filter((t) => Number(t.has) === 1).map((t) => `${t.dim}:${t.tag}`).join('、')).join('\n');
    demands = await llmJson('demand', `你是电商需求分析助手，面向运营同学。
品类聚焦词：${focusTerm}。三品是该类目里的三个样本（A/B/C，分属不同店铺）。

任务：从下面的【真实评价】（已经过规则分层，剔除了系统默认好评、未使用先评价、疑似刷单模板）和【小红书笔记与评论】里，归纳用户**明确提出的需求点**（想要什么、在意什么、卡在哪）。

要求：
- 每个需求点 q 写一句平实的话（≤20 字），不要写空泛的「品质好」。
- evidence：给出原话证据，src 填来源（填「评价」或「小红书评论」或「笔记正文」），where 填店别或笔记标题，text 填**原话原文**（不要改写），n 填支持该需求点的条数（按你引用的证据计数，≥1）。
- cover：判断 A/B/C 三品是否已经在页面文案/评价里满足了该需求（true/false）。
- coverNote：一句话说明判定依据（例如「A 详情图写了防水测试」）。
- 只归纳有原话支撑的需求点，最多 8 个；没有证据的不要写。

【真实评价】
${reviewBlock || '（无）'}

【小红书笔记与评论】
${xhsBlock || '（无）'}

【三品七维标签（供判断覆盖）】
${tagBlock || '（无）'}

返回 JSON：{"demands":[{"q":"...","evidence":[{"src":"评价","where":"A·xx店","text":"原话","n":2}],"cover":{"A":true,"B":false,"C":false},"coverNote":"..."}]}`,
      JSON.stringify({
        type: 'object',
        properties: {
          demands: {
            type: 'array', items: {
              type: 'object', properties: {
                q: { type: 'string' },
                evidence: { type: 'array', items: { type: 'object', properties: { src: { type: 'string' }, where: { type: 'string' }, text: { type: 'string' }, n: { type: 'number' } }, required: ['src', 'where', 'text', 'n'] } },
                cover: { type: 'object', properties: { A: { type: 'boolean' }, B: { type: 'boolean' }, C: { type: 'boolean' } } },
                coverNote: { type: 'string' },
              }, required: ['q', 'evidence', 'cover'],
            },
          },
        }, required: ['demands'],
      }));
  } catch (e) { failures.push('demand: ' + String(e.message).slice(0, 100)); }

  // --- 22：结论表（子会话，措辞把关）---
  let conclusions = null;
  try {
    conclusions = await llmJson('conclusion', `你是电商运营分析助手。下面是「${focusTerm}」品类的三品采集结果（供给侧标签加权 + 需求侧证据）。

请产出结论表，每行三列：
- evidence：证据（必须是上面出现过的事实/数字/原话，不要编）
- meaning：运营含义（这句话对这个品类的运营意味着什么，平实地说）
- actions：可做的事（具体到能动手的动作，如详情页补哪类说明、主图加什么信息、评价引导问什么）

措辞要求（硬性）：
- 面向运营同学，平实、具体、可执行。
- 禁止使用「红海」「蓝海」「入场券」「最大空位」「颠覆」「碾压」这类浮夸词。
- 每行都要有证据支撑，不要写没有依据的判断。
- 5~8 行。

【标签频次 × 销量加权（前 20）】
${(tagW.rows || []).slice(0, 20).map((r) => `${r.dim}·${r.tag}｜覆盖 ${r.cover}/3｜销量加权 ${r.weight}`).join('\n')}

【样本】
${labels.map((k) => `${k}：${items[k].shop} / ${items[k].priceText || '价格未提取'} / ${items[k].soldText || '销量未提取'} / 评价采集 ${(items[k].reviews || []).length} 条（真实 ${cls.perItem[k].real} 条）`).join('\n')}

【需求点与覆盖】
${(demands && demands.demands ? demands.demands : []).map((d) => `- ${d.q}（A:${d.cover && d.cover.A ? '有' : '无'} B:${d.cover && d.cover.B ? '有' : '无'} C:${d.cover && d.cover.C ? '有' : '无'}）证据：${(d.evidence || []).slice(0, 2).map((e) => e.text).join('；')}`).join('\n') || '（需求归纳未返回）'}

返回 JSON：{"rows":[{"evidence":"...","meaning":"...","actions":"..."}]}`,
      JSON.stringify({
        type: 'object',
        properties: { rows: { type: 'array', items: { type: 'object', properties: { evidence: { type: 'string' }, meaning: { type: 'string' }, actions: { type: 'string' } }, required: ['evidence', 'meaning', 'actions'] } } },
        required: ['rows'],
      }));
  } catch (e) { failures.push('conclusion: ' + String(e.message).slice(0, 100)); }

  for (const d of (demands && demands.demands ? demands.demands : [])) jsonl.push({ type: 'demand', ...d });
  writeFileSync(join(dataDir, 'xhs-demand.jsonl'), jsonl.map((x) => JSON.stringify(x)).join('\n') + '\n');

  // --- 23：报告 ---
  const boundaries = [
    `评价采集：每品点击「查看全部评价」内联展开后采集（展开区块上限约 22 条）：${labels.map((k) => `${k} 采到 ${(items[k].reviews || []).length} 条 / 页面显示 ${items[k].rateCountText || '未提取'}`).join('；')}；页面总数大于采集数时如实记「未到底」，不足 20 条且非「到底」的已在运行摘要中标注。`,
    `评价分层：① 无效 ${cls.totals.invalid} 条忽略不计分母；② 跨用户公共子串 ≥18 字 ${cls.totals.fake} 条剔除；③ 其余 ${cls.totals.real} 条视为真实——均为规则运行结果，非估计值。`,
    `销量口径统一取商品页「已售 N+」（${labels.map((k) => `${k}：${items[k].soldText || '未提取'}`).join('；')}）；「万」按 ×10000 折算。价格取页面「￥N 起」结构，页面未展示的优惠前价不做推断。`,
    `选品只做同店排除一个硬过滤，样本量仅 3 个，结论是这三个样本之间的比较，不代表整个类目。`,
    `图片文案由 LLM 子会话多模态直接读图提取，可能有个别错字；详情长图只取懒加载能滚出来的部分。`,
    `小红书：检索词 ${xhsKeywords.join(' / ') || '（未生成）'}，命中卡片 ${xhs.cardCount} 张，深挖 ${xhs.notes.length} 篇；部分笔记正文只在图片里（正文只有话题标签），这类笔记以标题和评论原话为证据。`,
    `全程操作间隔 ≥1.8s、串行采集，访问畅通；若商品页或搜索页被登录墙拦截，本 skill 会直接报错并提示在 Chrome 登录淘宝后重试。`,
  ];
  if (selection.skips.length) {
    boundaries.push(`选品顺延记录：${selection.skips.length} 个候选被跳过（${[...new Set(selection.skips.map((s) => s.reason.split('（')[0]))].join('、')}），逐条明细见样本构成表与 data/selection.json。`);
  }
  if (failures.length) boundaries.push('本次未完全跑通的环节：' + failures.join('；'));

  const html = renderReport({ items, selection, tagW, cls, xhs, demands, conclusions, focusTerm, seed, productUrl, boundaries });
  writeFileSync(join(outputDir, 'report.html'), html);

  const okCount = labels.length;
  // 三品是本 skill 的核心前置：不足三个有效样本（哪怕 failures 为空）也不能报 success
  const status = (okCount === 3 && failures.length === 0) ? 'success' : (okCount >= 2 ? 'partial' : 'failed');
  const summary = `三品采集 ${okCount}/3（${labels.join('/')}），聚焦词「${focusTerm}」，评价 ${cls.totals.total} 条（${labels.map((k) => `${k}:${(items[k].reviews || []).length}`).join('/')}）→真实 ${cls.totals.real} 条，标签 ${tagW.rows.length} 个，xhs 深挖 ${xhs.notes.length} 篇${failures.length ? `；未完全跑通：${failures.length} 项` : ''}`;
  console.log(JSON.stringify({ status, summary, output_dir: outputDir }));
}

main().catch((e) => {
  process.stderr.write('ERROR: ' + (e && e.stack ? e.stack : String(e)) + '\n');
  console.log(JSON.stringify({ status: 'failed', summary: String(e && e.message ? e.message : e).slice(0, 300) }));
  process.exit(0);
});
