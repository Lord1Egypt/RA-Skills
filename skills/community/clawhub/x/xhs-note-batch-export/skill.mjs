#!/usr/bin/env node
// xhs-note-batch-export：批量导出指定小红书博主主页「笔记」tab 的全部笔记为本地 Markdown。
// 所有浏览器操作通过 Extension Relay HTTP API（端口 3459）完成，不使用 CDP。
// 流程（全为确定性代码，无 LLM 子会话）：开主页 → 滚动收集卡片(去重) → 逐篇点开详情弹层提取 → 落盘 md + summary.json。
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const RELAY_URL = 'http://127.0.0.1:3459';

// ---- 时序常量（来自探索实测）----
const WAIT_DETAIL_LOAD = 4000; // 点卡片后等正文/媒体加载
const WAIT_CLOSE_OVERLAY = 2500; // history.back() 后等列表恢复
const SCROLL_STEP = 900; // 收集阶段每轮滚动距离
const WAIT_SCROLL = 1800; // 收集阶段滚动间隔
const MAX_STALL_ROUNDS = 3; // 连续无增长轮数 = 已到列表底部
const MAX_COLLECT_ROUNDS = 300; // 收集轮数上限（防死循环）
const WAIT_NOTES_TIMEOUT = 20000; // 等笔记列表渲染的超时
const POLL_INTERVAL = 2200; // 互动数轮询间隔
const POLL_MAX_MS = 18000; // 互动数轮询总上限
const LOCATE_STEP = 700; // 定位卡片时滚动步长
const LOCATE_WAIT = 1200; // 定位卡片时每轮等待
const LOCATE_MAX_ROUNDS = 80; // 定位上限（防死循环）
const PARALLEL_MAX = 3; // 详情抓取并发上限（>3 按 3 处理）
const PARALLEL_STAGGER_MS = 1500; // 并行 worker tab 创建间隔
const CONFIRM_OPEN_MS = 4000; // 点卡片后确认弹层已打开的轮询上限

let OUT_DIR = '';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ---- Extension Relay HTTP API 封装 ----
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

async function ensureRelay() {
  try {
    const status = await (await fetch(`${RELAY_URL}/api/status`)).json();
    if (!status.extensionConnected) throw new Error('Extension not connected');
  } catch (e) {
    throw new Error(`Relay not available at ${RELAY_URL}。需要先安装并启动 webclaw3（浏览器自动化主品，用你已登录的 Chrome 干活）：运行 webclaw3 doctor 检查环境，安装指引见 https://webclaw3.com（装 Chrome 扩展 + 领 Access Key）。原始错误：${e.message}`);
  }
}

// page.eval 封装：content script 未注入等瞬时错误加有限次重试
async function pageEval(tabId, code, groupId) {
  let lastErr;
  for (let i = 0; i < 3; i++) {
    try {
      return await relayCall('page.eval', { tabId, code, groupId }, 60000);
    } catch (e) {
      lastErr = e;
      await sleep(2000);
    }
  }
  throw lastErr;
}

// 解析 page.eval 返回的 JSON 字符串（IIFE 单表达式返回，避开多语句 eval 返回值不可靠的坑）
async function evalJson(tabId, code, groupId) {
  try {
    return JSON.parse(await pageEval(tabId, code, groupId));
  } catch {
    return null;
  }
}

// ---- pMap：带并发上限的批量执行（返回值格式同 Promise.allSettled）----
async function pMap(items, fn, { concurrency = 2 } = {}) {
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

// ---- 页面内提取脚本（选择器来自探索实测）----

// 详情提取函数：定义一次，每篇调用。图片去重、视频按 __t0 过滤防上一篇残留、互动数解析（1.2万→12000）
const EXTRACT_AND_STORE_JS = `(()=>{
  window.__collected = window.__collected || [];
  window.__extractAndStore = function(noteId){
    const num = t => {
      const s = (t || '').trim();
      if (!s) return null;
      if (/[0-9.]+\\s*万/.test(s)) return Math.round(parseFloat(s.replace(/[^0-9.]/g, '')) * 10000);
      return /^[0-9]+$/.test(s) ? parseInt(s, 10) : null;
    };
    const title = (document.querySelector('#detail-title') || {}).textContent ? document.querySelector('#detail-title').textContent.trim() : '';
    const desc  = (document.querySelector('#detail-desc') || {}).textContent ? document.querySelector('#detail-desc').textContent.trim() : '';
    const imgs  = [...new Set([...document.querySelectorAll('.swiper-slide img, .slide img')].map(i => i.getAttribute('src') || i.currentSrc).filter(Boolean))];
    const t0    = window.__t0 || 0;
    const vids  = [...new Set(performance.getEntriesByType('resource')
      .filter(r => r.startTime >= t0 && r.name.match(/\\/stream\\/.*\\.mp4/) && !r.name.startsWith('blob:'))
      .map(r => r.name))];
    const likeEl = document.querySelector('.engage-bar-container .left .like-wrapper .count');
    const colEl  = document.querySelector('.engage-bar-container .left .collect-wrapper .count');
    const chaEl  = document.querySelector('.engage-bar-container .left .chat-wrapper .count');
    const like = num(likeEl ? likeEl.textContent : '');
    const collect = num(colEl ? colEl.textContent : '');
    const comments = num(chaEl ? chaEl.textContent : '');
    const m = location.href.match(/\\/(?:explore|user\\/profile\\/[0-9a-f]+)\\/([0-9a-f]{24})/);
    const id = m ? m[1] : (noteId || '');
    const tok = (location.href.match(/xsec_token=([^&]+)/) || [])[1] || '';
    const rec = { note_id: id, title, desc, imgs, videos: vids,
      likes: like, collects: collect, comments,
      url: id ? ('https://www.xiaohongshu.com/explore/' + id + (tok ? '?xsec_token=' + tok : '')) : location.href };
    const idx = window.__collected.findIndex(r => r.note_id === id);
    if (idx >= 0) { window.__collected[idx] = rec; } else { window.__collected.push(rec); }
    return JSON.stringify({pushed:true, n:window.__collected.length, rec});
  };
  return JSON.stringify({ready:true});
})()`;

// 互动数轮询（不依赖 __extractAndStore，纯读取当前值）
const POLL_JS = `(()=>{
  const num = t => { const s=(t||'').trim(); if(!s) return null; if(/[0-9.]+\\s*万/.test(s)) return Math.round(parseFloat(s.replace(/[^0-9.]/g,''))*10000); return /^[0-9]+$/.test(s)?parseInt(s,10):null; };
  const likeEl=document.querySelector('.engage-bar-container .left .like-wrapper .count');
  const colEl=document.querySelector('.engage-bar-container .left .collect-wrapper .count');
  const chaEl=document.querySelector('.engage-bar-container .left .chat-wrapper .count');
  const likes=num(likeEl?likeEl.textContent:''), collects=num(colEl?colEl.textContent:''), comments=num(chaEl?chaEl.textContent:'');
  return JSON.stringify({likes, collects, comments});
})()`;

// 初始化去重集合 + 卡片列表 + 位置记录，并把首屏卡片全部入队（顺序 = 页面实际顺序 = 最新在前）
const INIT_COLLECT_JS = `(()=>{
  window.__seen = window.__seen || new Set();
  window.__cards = window.__cards || [];
  window.__cardPos = window.__cardPos || {};
  const pos = window.scrollY;
  let added = 0;
  [...document.querySelectorAll('section.note-item')].forEach(n => {
    const id = n.getAttribute('data-note-id');
    if (!id || window.__seen.has(id)) return;
    window.__seen.add(id); added++;
    window.__cardPos[id] = pos;
    const a = n.querySelector('a.title');
    const c = n.querySelector('a.cover');
    window.__cards.push({ id, title: a ? a.textContent.trim() : '', cover: c ? c.href : '' });
  });
  return JSON.stringify({ size: window.__seen.size, added });
})()`;

// 滚动收集一轮：滚动后把新出现的卡片追加进列表（虚拟列表只保留视口附近，必须边滚边收集）
const SCROLL_COLLECT_JS = `(()=>{
  window.scrollBy(0, ${SCROLL_STEP});
  const pos = window.scrollY;
  let added = 0;
  [...document.querySelectorAll('section.note-item')].forEach(n => {
    const id = n.getAttribute('data-note-id');
    if (!id || window.__seen.has(id)) return;
    window.__seen.add(id); added++;
    window.__cardPos[id] = pos;
    const a = n.querySelector('a.title');
    const c = n.querySelector('a.cover');
    window.__cards.push({ id, title: a ? a.textContent.trim() : '', cover: c ? c.href : '' });
  });
  return JSON.stringify({ size: window.__seen.size, added });
})()`;

// 后台 tab 激活焦点：分片并行时非当前 tab 都是后台 tab，操作前先派发鼠标事件 + window.focus()
// 否则滚动/点击在后台 tab 不生效（virtual list 懒加载不推进）
const ACTIVATE_FOCUS_JS = `(()=>{
  try { window.focus(); } catch(e) {}
  const b = document.body;
  if (b) {
    b.dispatchEvent(new MouseEvent('mousedown', {bubbles:true, cancelable:true}));
    b.dispatchEvent(new MouseEvent('mouseup', {bubbles:true, cancelable:true}));
    b.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true}));
  }
  return JSON.stringify({ok:true});
})()`;

// 关闭详情弹层：仅当已打开 explore 页才 history.back()，避免误退出博主主页
const BACK_JS = `(()=>{ if (location.href.indexOf('/explore/') >= 0) history.back(); return JSON.stringify({backed:true}); })()`;

// ---- 浏览器流程 ----

async function waitForNotes(tabId, groupId) {
  const deadline = Date.now() + WAIT_NOTES_TIMEOUT;
  while (Date.now() < deadline) {
    const r = await evalJson(
      tabId,
      `JSON.stringify({url: location.href, noteCount: document.querySelectorAll('section.note-item').length})`,
      groupId
    );
    if (r && r.noteCount > 0) return r;
    if (r && r.url.indexOf('website-login') >= 0) {
      throw new Error('检测到页面跳转至登录/验证页，已停止操作。请确认小红书账号登录状态后重试。');
    }
    await sleep(2500);
  }
  throw new Error('等待笔记列表渲染超时（博主主页可能不可访问或需登录）');
}

async function scrollCollect(tabId, groupId, targetSeen) {
  let stall = 0;
  for (let round = 0; round < MAX_COLLECT_ROUNDS; round++) {
    const r = await evalJson(tabId, SCROLL_COLLECT_JS, groupId);
    const size = r ? r.size : 0;
    const added = r ? r.added : 0;
    if (targetSeen !== Infinity && size >= targetSeen) return;
    if (added === 0) {
      stall++;
      if (stall >= MAX_STALL_ROUNDS) return; // 连续无增长 = 已到列表底部
    } else {
      stall = 0;
    }
    await sleep(WAIT_SCROLL);
  }
}

async function getCardPos(tabId, noteId, groupId) {
  // __cardPos 由主收集 tab 或并行 worker 注入的位置表提供；缺失时返回 null 走滚动兜底
  const r = await evalJson(
    tabId,
    `(()=>{ const p = window.__cardPos || {}; return JSON.stringify({ pos: p[${JSON.stringify(noteId)}] }); })()`,
    groupId
  );
  return r && r.pos != null ? r.pos : null;
}

async function cardInDom(tabId, noteId, groupId) {
  const r = await evalJson(
    tabId,
    `(()=>{ return JSON.stringify({ found: !!document.querySelector('section.note-item[data-note-id=${JSON.stringify(noteId)}]') }); })()`,
    groupId
  );
  return !!(r && r.found);
}

// 定位卡片：虚拟列表会回收视口外节点，不在 DOM 先滚动到附近再确认
async function locateCard(tabId, noteId, groupId) {
  // 优先跳到收集阶段记录的卡片位置（±500px 缓冲，确保在虚拟列表 buffer 内）
  const pos = await getCardPos(tabId, noteId, groupId);
  if (pos != null) {
    await pageEval(tabId, `(()=>{ window.scrollTo(0, Math.max(0, ${pos} - 500)); return JSON.stringify({ok:true}); })()`, groupId);
    await sleep(1200);
    if (await cardInDom(tabId, noteId, groupId)) return true;
  }
  for (let i = 0; i < LOCATE_MAX_ROUNDS; i++) {
    const r = await evalJson(
      tabId,
      `(()=>{
        if (document.querySelector('section.note-item[data-note-id=${JSON.stringify(noteId)}]')) return JSON.stringify({found:true});
        window.scrollBy(0, ${LOCATE_STEP});
        return JSON.stringify({found:false});
      })()`,
      groupId
    );
    if (r && r.found) return true;
    await sleep(LOCATE_WAIT);
  }
  return false;
}

// 定位卡片 + 快照 __t0（防上一篇视频 mp4 残留）+ 打开详情弹层
// 为什么先 dispatchEvent 合成点击：后台 worker tab 上 cover.click() 若 SPA 未拦截，a 的默认行为会整页导航
// 到 explore 页，注入的 __extractAndStore/__cardPos 随页面重建丢失；合成 MouseEvent 不会触发浏览器默认导航。
// 确认弹层未打开再退回 .click()（探索验证过的路径，active tab 下必然有效）。
async function clickAndOpen(tabId, noteId, groupId) {
  const clickScript = `(()=>{
    const card = document.querySelector('section.note-item[data-note-id=${JSON.stringify(noteId)}]');
    if (!card) return JSON.stringify({clicked:false, reason:'no-card'});
    card.scrollIntoView({block:'center'});
    window.__t0 = Math.max(0, ...performance.getEntriesByType('resource').map(r => r.startTime));
    const cover = card.querySelector('a.cover');
    if (!cover) return JSON.stringify({clicked:false, reason:'no-cover', t0:window.__t0});
    cover.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true, view:window}));
    return JSON.stringify({clicked:true, method:'dispatch', t0:window.__t0});
  })()`;
  const r = await evalJson(tabId, clickScript, groupId);
  if (!r || !r.clicked) return r || { clicked: false, reason: 'eval-error' };

  // 确认弹层已打开（URL 变为 explore 或详情标题出现），最多轮询 CONFIRM_OPEN_MS
  let opened = null;
  const deadline = Date.now() + CONFIRM_OPEN_MS;
  while (Date.now() < deadline) {
    opened = await evalJson(
      tabId,
      `JSON.stringify({explore: location.href.indexOf('/explore/') >= 0, hasTitle: !!document.querySelector('#detail-title')})`,
      groupId
    );
    if (opened && (opened.explore || opened.hasTitle)) return r;
    await sleep(1000);
  }

  const r2 = await evalJson(
    tabId,
    `(()=>{
      const card = document.querySelector('section.note-item[data-note-id=${JSON.stringify(noteId)}]');
      if (!card) return JSON.stringify({clicked:false, reason:'no-card'});
      card.scrollIntoView({block:'center'});
      window.__t0 = Math.max(0, ...performance.getEntriesByType('resource').map(r => r.startTime));
      const cover = card.querySelector('a.cover');
      if (!cover) return JSON.stringify({clicked:false, reason:'no-cover', t0:window.__t0});
      cover.click();
      return JSON.stringify({clicked:true, method:'click', t0:window.__t0});
    })()`,
    groupId
  );
  if (!r2 || !r2.clicked) return r2 || { clicked: false, reason: 'eval-error' };
  return r2;
}

// 后台 worker tab 点开详情若发生整页导航，注入的 __extractAndStore 会丢失：缺失则重新注入
async function ensureExtractFn(tabId, groupId) {
  const r = await evalJson(tabId, `JSON.stringify({has: typeof window.__extractAndStore === 'function'})`, groupId);
  if (!r || !r.has) await pageEval(tabId, EXTRACT_AND_STORE_JS, groupId).catch(() => {});
}

// 页面上下文完整性：整页导航后 __extractAndStore 与 __cardPos 位置表会一起丢失，需要重建
async function ctxIntact(tabId, groupId) {
  const r = await evalJson(
    tabId,
    `JSON.stringify({ok: !!(window.__extractAndStore && window.__cardPos && Object.keys(window.__cardPos).length > 0)})`,
    groupId
  );
  return !!(r && r.ok);
}

async function extractRecord(tabId, noteId, groupId) {
  await ensureExtractFn(tabId, groupId);
  const raw = await pageEval(tabId, `window.__extractAndStore(${JSON.stringify(noteId)})`, groupId);
  let res;
  try { res = JSON.parse(raw); } catch { return null; }
  if (!res || !res.rec) return null;
  // 空记录（弹层未打开/内容未加载）视为失败，不写入
  if (!res.rec.title && !res.rec.desc && (!res.rec.imgs || res.rec.imgs.length === 0)) return null;
  return res.rec;
}

async function pollInteractions(tabId, groupId) {
  const deadline = Date.now() + POLL_MAX_MS;
  while (Date.now() < deadline) {
    await sleep(POLL_INTERVAL);
    const r = await evalJson(tabId, POLL_JS, groupId);
    if (r && r.likes != null && r.collects != null && r.comments != null) return true;
  }
  return false;
}

async function activateFocus(tabId, groupId) {
  await pageEval(tabId, ACTIVATE_FOCUS_JS, groupId).catch(() => {});
}

// 单篇详情抓取：定位 → 点击弹层 → 提取 → 互动数轮询（缺则标 partial）→ 关闭弹层
async function extractOne(tabId, card, groupId) {
  await activateFocus(tabId, groupId);

  const found = await locateCard(tabId, card.id, groupId);
  if (!found) return { status: 'failed', reason: 'card-not-found' };

  const cj = await clickAndOpen(tabId, card.id, groupId);
  if (!cj.clicked) return { status: 'failed', reason: cj.reason || 'click-failed' };

  await sleep(WAIT_DETAIL_LOAD);

  const curUrl = await pageEval(tabId, 'location.href', groupId).catch(() => '');
  if (curUrl.indexOf('website-login') >= 0) return { status: 'failed', reason: 'login-redirect' };

  let rec = await extractRecord(tabId, card.id, groupId);
  if (!rec) {
    await sleep(2000);
    rec = await extractRecord(tabId, card.id, groupId);
  }
  if (!rec) {
    await pageEval(tabId, BACK_JS, groupId).catch(() => {});
    await sleep(WAIT_CLOSE_OVERLAY);
    return { status: 'failed', reason: 'extract-failed' };
  }

  if (rec.likes == null || rec.collects == null || rec.comments == null) {
    const got = await pollInteractions(tabId, groupId);
    if (got) rec = await extractRecord(tabId, card.id, groupId);
  }

  await pageEval(tabId, BACK_JS, groupId).catch(() => {});
  await sleep(WAIT_CLOSE_OVERLAY);

  return { status: 'ok', rec };
}

// 串行抓取（parallel=1）：主收集 tab 上逐篇处理；单篇抛错不中断整批
async function serialExtract(tabId, slice, groupId) {
  const slotResults = new Array(slice.length).fill(null);
  const failures = [];
  for (let i = 0; i < slice.length; i++) {
    try {
      const res = await extractOne(tabId, slice[i], groupId);
      if (res.status === 'ok') {
        slotResults[i] = res.rec;
      } else {
        failures.push({ note_id: slice[i].id, reason: res.reason });
      }
    } catch (e) {
      failures.push({ note_id: slice[i].id, reason: `note-error: ${String((e && e.message) || e).slice(0, 120)}` });
    }
  }
  return { slotResults, failures };
}

// 从位置表里挑选指定卡片的 {id: pos} 子集
function pickPos(posMap, cards) {
  const o = {};
  for (const c of cards) if (posMap[c.id] != null) o[c.id] = posMap[c.id];
  return o;
}

// 并行抓取（parallel=2~3）：把待抓列表按序分 N 段，开 N 个 tab（同一博主主页），每 tab 负责一段
// posMap：主收集 tab 的 __cardPos 快照，注入 worker 让虚拟列表直跳，避免后台 tab 从顶部慢滚
async function parallelExtract(profileUrl, slice, parallel, groupId, posMap) {
  const k = Math.min(parallel, slice.length);
  const perChunk = Math.ceil(slice.length / k);
  const chunks = [];
  for (let i = 0; i < k; i++) chunks.push(slice.slice(i * perChunk, (i + 1) * perChunk));

  const workerTabs = [];
  try {
    for (let i = 0; i < k; i++) {
      const t = await relayCall('tab.create', { url: profileUrl, active: i === 0, groupId });
      workerTabs.push(t.id);
      await sleep(PARALLEL_STAGGER_MS); // 错峰创建 tab
    }

    const chunkResults = await pMap(workerTabs, async (tabId, ci) => {
      const chunk = chunks[ci];
      const out = new Array(chunk.length).fill(null);
      const chunkPos = pickPos(posMap, chunk);
      try {
        await waitForNotes(tabId, groupId);
        await activateFocus(tabId, groupId);
        await pageEval(tabId, EXTRACT_AND_STORE_JS, groupId);
        await pageEval(tabId, INIT_COLLECT_JS, groupId).catch(() => {});
        await pageEval(
          tabId,
          `(()=>{ window.__cardPos = Object.assign(window.__cardPos || {}, ${JSON.stringify(chunkPos)}); return JSON.stringify({ok:Object.keys(window.__cardPos).length}); })()`,
          groupId
        );
      } catch (e) {
        for (let j = 0; j < chunk.length; j++) out[j] = { ok: false, reason: `worker-error: ${String((e && e.message) || e).slice(0, 120)}` };
        return out;
      }
      for (let j = 0; j < chunk.length; j++) {
        try {
          // 后台 tab 点开详情可能整页导航重建页面上下文（__extractAndStore/__cardPos 丢失）：
          // 检测到后从顶部重建注入，并重新下发剩余卡片的位置表
          const intact = await ctxIntact(tabId, groupId);
          if (!intact) {
            await pageEval(tabId, `(()=>{ window.scrollTo(0,0); return JSON.stringify({ok:true}); })()`, groupId).catch(() => {});
            await pageEval(tabId, EXTRACT_AND_STORE_JS, groupId).catch(() => {});
            const remPos = pickPos(posMap, chunk.slice(j));
            await pageEval(tabId, `(()=>{ window.__cardPos = ${JSON.stringify(remPos)}; return JSON.stringify({ok:Object.keys(window.__cardPos).length}); })()`, groupId).catch(() => {});
          }
          const res = await extractOne(tabId, chunk[j], groupId);
          if (res.status === 'ok') {
            out[j] = { ok: true, rec: res.rec };
          } else {
            out[j] = { ok: false, reason: res.reason };
          }
        } catch (e) {
          out[j] = { ok: false, reason: `note-error: ${String((e && e.message) || e).slice(0, 120)}` };
        }
      }
      return out;
    }, { concurrency: workerTabs.length });

    // pMap 返回 allSettled 格式（每项 {status, value}），必须解包 cr.value 取 worker 的返回数组——
    // 上一版在 !Array.isArray(cr) 处从不解包，导致每个分片都被判 worker-failed、parallel>1 必然 0 导出
    const slotResults = new Array(slice.length).fill(null);
    const failures = [];
    chunkResults.forEach((cr, ci) => {
      const chunk = chunks[ci];
      if (!cr || cr.status === 'rejected' || !Array.isArray(cr.value)) {
        for (let j = 0; j < chunk.length; j++) failures.push({ note_id: chunk[j].id, reason: 'worker-failed' });
        return;
      }
      const items = cr.value;
      items.forEach((item, j) => {
        const slot = ci * perChunk + j;
        if (item && item.ok) slotResults[slot] = item.rec;
        else failures.push({ note_id: chunk[j].id, reason: (item && item.reason) || 'failed' });
      });
    });
    return { slotResults, failures };
  } finally {
    for (const tabId of workerTabs) await relayCall('tab.close', { tabId, groupId }).catch(() => {});
  }
}

// 失败笔记重试：一律用主收集 tab 串行重试（parallel 隐式降级为 1）。
// 为什么重试而不是直接认失败：瞬时错误（content script 未注入、后台 tab 导航）在串行路径上通常能成功，
// 把 partial 导出尽量补齐；重试仍失败的如实记入 failures。
async function retryFailedNotes(tabId, slice, slotResults, failures, groupId) {
  if (failures.length === 0) return { slotResults, failures };
  const slotOf = new Map(slice.map((c, i) => [c.id, i]));
  const failedCards = failures.filter((f) => slotOf.has(f.note_id)).map((f) => ({ id: f.note_id }));
  if (failedCards.length === 0) return { slotResults, failures }; // 无可重试卡片（如 offset 越界）

  const { slotResults: r2, failures: f2 } = await serialExtract(tabId, failedCards, groupId);

  const newSlotResults = slotResults.slice();
  const keptFailures = [];
  r2.forEach((rec, i) => {
    const slot = slotOf.get(failedCards[i].id);
    if (rec) {
      newSlotResults[slot] = rec;
    } else {
      keptFailures.push({ note_id: failedCards[i].id, reason: (f2[i] && f2[i].reason) || 'retry-failed' });
    }
  });
  // 保留无法重试的原始失败（offset-beyond 等无卡片条目）
  const retriedIds = new Set(failedCards.map((c) => c.id));
  for (const f of failures) if (!retriedIds.has(f.note_id)) keptFailures.push(f);
  return { slotResults: newSlotResults, failures: keptFailures };
}

// ---- 落盘 ----

function sanitizeFileName(title) {
  const cleaned = title.replace(/[\\/:*?"<>|\x00-\x1f]/g, '').replace(/\s+/g, ' ').trim();
  return cleaned.slice(0, 50) || 'untitled';
}

function writeOutputs({ outDir, slice, slotResults, failures, offset, count, parallel, available, outputFiles }) {
  const partialIds = [];
  const written = [];
  for (let i = 0; i < slice.length; i++) {
    const rec = slotResults[i];
    if (!rec) continue;
    const title = rec.title || slice[i].title || 'untitled';
    const seq = offset + i + 1; // 序号按笔记在博主主页的位置延续递增，失败跳过时后续序号不位移
    const hasBody = !!(rec.desc && rec.desc.trim());
    const hasMedia = (rec.imgs && rec.imgs.length > 0) || (rec.videos && rec.videos.length > 0);
    const hasInteract = rec.likes != null && rec.collects != null && rec.comments != null;
    // 正文/图片全缺 或 互动数未读到 → 标 partial
    const partial = !(hasBody || hasMedia) || !hasInteract;
    if (partial) partialIds.push(rec.note_id);

    const lines = [
      `# ${title}`,
      `原文链接: ${rec.url || ''}`,
      `互动: 赞${rec.likes ?? '?'} 藏${rec.collects ?? '?'} 评${rec.comments ?? '?'}${partial ? ' (partial)' : ''}`,
      '---',
      rec.desc || '',
      '---',
    ];
    if (rec.imgs && rec.imgs.length > 0) lines.push(`图片: ${rec.imgs.join(' ')}`);
    if (rec.videos && rec.videos.length > 0) lines.push(`视频: ${rec.videos.join(' ')}`);
    lines.push('');

    const fname = `${String(seq).padStart(3, '0')}_${sanitizeFileName(title)}.md`;
    writeFileSync(join(outDir, fname), lines.join('\n'), 'utf8');
    written.push(fname);
  }

  const exportedCount = written.length;
  const summary = {
    total_exported: exportedCount,
    offset,
    count,
    parallel,
    total_available: available,
    skipped_partial: partialIds,
    failures,
  };
  writeFileSync(join(outDir, 'summary.json'), JSON.stringify(summary, null, 2), 'utf8');

  // pipeline 约定：res.json 只放元信息，完整数据放 data.md
  const status = exportedCount === 0 ? 'failed' : (failures.length > 0 || partialIds.length > 0) ? 'partial' : 'success';
  writeFileSync(
    join(outDir, outputFiles.result || 'res.json'),
    JSON.stringify({ status, summary, output_dir: outDir }, null, 2),
    'utf8'
  );
  writeFileSync(join(outDir, outputFiles.data || 'data.md'), buildDataMd(slice, slotResults, offset), 'utf8');

  return { summary, exportedCount, partialIds };
}

function buildDataMd(slice, slotResults, offset) {
  const parts = ['# xhs-note-batch-export 结果', ''];
  for (let i = 0; i < slice.length; i++) {
    const rec = slotResults[i];
    const seq = offset + i + 1;
    if (!rec) {
      parts.push(`## [${seq}] 未导出`);
      parts.push('');
      continue;
    }
    parts.push(`## [${seq}] ${rec.title || slice[i].title || 'untitled'}`);
    parts.push(`- 原文链接: ${rec.url || ''}`);
    parts.push(`- 互动: 赞${rec.likes ?? '?'} 藏${rec.collects ?? '?'} 评${rec.comments ?? '?'}`);
    parts.push(`- 图片: ${(rec.imgs || []).length} 张`);
    parts.push(`- 视频: ${(rec.videos || []).length} 个`);
    if (rec.desc) { parts.push(''); parts.push(rec.desc); }
    if (rec.imgs && rec.imgs.length) { parts.push(''); parts.push(`图片: ${rec.imgs.join(' ')}`); }
    if (rec.videos && rec.videos.length) { parts.push(''); parts.push(`视频: ${rec.videos.join(' ')}`); }
    parts.push('');
  }
  return parts.join('\n');
}

// ---- 入口 ----

function loadInput() {
  const p = process.argv[2];
  if (p) return JSON.parse(readFileSync(p, 'utf-8'));
  const raw = readFileSync(0, 'utf-8').trim();
  if (raw) return JSON.parse(raw);
  return {};
}

async function main() {
  const input = loadInput();
  const profileUrl = input.profileUrl;
  if (!profileUrl) throw new Error('input.profileUrl 必填');
  const count = input.count ?? 10;
  const offset = input.offset ?? 0;
  const parallel = Math.min(PARALLEL_MAX, Math.max(1, input.parallel ?? 1));
  const outputFiles = input.output_files || {};
  OUT_DIR = input.output_dir || input.outputDir || '/tmp/xhs-note-batch-export-output';
  mkdirSync(OUT_DIR, { recursive: true });

  await ensureRelay();
  const { groupId } = await relayCall('group.create', { name: 'xhs-note-batch-export' });

  try {
    await relayCall('group.setStatus', { groupId, status: 'running' }).catch(() => {});

    // Phase 1: 打开博主主页，确认笔记列表渲染
    const tab = await relayCall('tab.create', { url: profileUrl, active: true, groupId });
    await waitForNotes(tab.id, groupId);

    // Phase 2: 初始化去重集合/卡片列表/位置记录 + 注入详情提取函数
    await pageEval(tab.id, INIT_COLLECT_JS, groupId);
    await pageEval(tab.id, EXTRACT_AND_STORE_JS, groupId);

    // Phase 3: 滚动收集全部卡片（按首次出现顺序 = 页面顺序 = 最新在前）
    const requested = (count === -1 || count === 0) ? Infinity : count;
    const targetSeen = requested === Infinity ? Infinity : offset + requested;
    await scrollCollect(tab.id, groupId, targetSeen);

    const allCards = JSON.parse(await pageEval(tab.id, 'JSON.stringify(window.__cards)', groupId));
    const posMap = JSON.parse(await pageEval(tab.id, 'JSON.stringify(window.__cardPos || {})', groupId));
    const available = allCards.length;
    const endIdx = requested === Infinity ? available : Math.min(offset + requested, available);
    const slice = allCards.slice(offset, endIdx);

    let slotResults = new Array(slice.length).fill(null);
    let failures = [];
    if (slice.length === 0) {
      failures.push({ note_id: null, reason: 'offset-beyond-available', detail: `total_available=${available}, offset=${offset}` });
    } else if (parallel > 1 && slice.length > 1) {
      ({ slotResults, failures } = await parallelExtract(profileUrl, slice, parallel, groupId, posMap));
    } else {
      ({ slotResults, failures } = await serialExtract(tab.id, slice, groupId));
    }

    // 失败笔记用主 tab 串行重试一遍，尽量补齐 partial 缺口
    if (failures.length > 0 && slice.length > 0) {
      ({ slotResults, failures } = await retryFailedNotes(tab.id, slice, slotResults, failures, groupId));
    }

    // Phase 4: 落盘 md + summary.json + res.json + data.md
    const { summary, exportedCount, partialIds } = writeOutputs({
      outDir: OUT_DIR, slice, slotResults, failures, offset, count, parallel, available, outputFiles,
    });
    const status = exportedCount === 0 ? 'failed' : (failures.length > 0 || partialIds.length > 0) ? 'partial' : 'success';
    return {
      status,
      summary,
      output_dir: OUT_DIR,
      summaryText: `导出 ${exportedCount} 篇（total_available=${available}, 失败 ${failures.length}, partial ${partialIds.length}）`,
    };
  } finally {
    await relayCall('group.close', { groupId }).catch(() => {});
  }
}

main()
  .then((r) => {
    console.log(JSON.stringify({ status: r.status, summary: r.summaryText, output_dir: r.output_dir }));
  })
  .catch((err) => {
    console.log(JSON.stringify({ status: 'failed', error: String((err && err.message) || err), output_dir: OUT_DIR }));
    process.exit(0);
  });
