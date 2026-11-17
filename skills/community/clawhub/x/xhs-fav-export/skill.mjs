#!/usr/bin/env node
/**
 * xhs-fav-export — 把小红书 Web 端当前登录用户「收藏」tab 的收藏笔记批量导出为本地 Markdown。
 *
 * 架构：全程确定性代码（Extension Relay HTTP API，端口 3459），不使用 CDP、不调用 LLM 子会话。
 * SUMMARY §2 分工表中 8 个步骤全部为【代码】步骤（页面操作 / 数据提取 / 文件生成都是规则化逻辑）。
 *
 * 流程（与 SUMMARY §3 一一对应）：
 *   1. group.create 任务分组
 *   2. 打开小红书首页，自动探测当前登录用户主页 uid（收藏 tab 必须是自己主页；
 *      不能硬编码 explore 测试用的 profile URL，requirement 要求对任意输入通用）
 *   3. tab.create 打开 <profile>?tab=collection（active:true，懒加载只在前台 tab 触发）
 *   4. 校验收藏视图；卡片不足 offset+count 时才分步 scrollBy(0,800) 触发懒加载
 *      （陷阱 1：body.click() 激活不了后台 tab 焦点，卡住不值得，仅当卡片数不足才滚动）
 *   5. 缓存卡片列表到 window.__cards（data-note-id / a.title / a.cover href，xsec_token 完整保留）
 *   6. 串行逐篇：确保列表页 → 快照 __t0 → 点击 a.cover 打开弹层 → 提取详情 → 立即落盘 → history.back()
 *      （串行是硬约束：多 tab 并行触发站点访问限制；逐篇落盘让失败代价控制在单篇——陷阱 5）
 *   7. 写 summary.json（{ total_exported, offset, count, skipped_partial }）
 */

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

/* ------------------------- 常量 ------------------------- */

const RELAY_URL = 'http://127.0.0.1:3459';
const HOMEPAGE = 'https://www.xiaohongshu.com/';

// 时序常量（SUMMARY §3c）—— tab.create 后 7s 等 SPA、点击弹层后 5s、history.back 后 2s
const SLEEP_AFTER_TAB_CREATE = 7000;
const SLEEP_AFTER_COVER_CLICK = 5000;
const SLEEP_AFTER_BACK = 2000;
const SLEEP_AFTER_ENSURE_CLEAN = 2000;
const SCROLL_STEP = 800;             // 陷阱 1：增量滚动触发懒加载，不要一次性 scrollTo(0, scrollHeight)
const CARD_LOAD_DEADLINE_MS = 20000; // 懒加载轮询总时限
const SCROLL_ROUND_MS = 2000;        // 每轮滚动后等待
const MAX_GROWTH_IDLE_ROUNDS = 2;    // 连续 2 轮无增长即停
const MAX_TITLE_LEN = 50;            // 文件名标题截断长度

const GROUP_NAME = 'xhs-fav-export';

/* --------------------- page.eval 脚本 ---------------------
 * 注意：脚本里禁止出现 '\n' 字面量（JSON body 传输会炸）；一律返回 JSON.stringify(...)
 * 字符串，调用端 JSON.parse。脚本全部来自 SUMMARY §3b 验证过的选择器，直接采用。
 */

// 探测当前登录用户 uid：优先导航「我」链接（自己主页），其次取页面中第一个
// profile 链接（header 里的头像链接在 DOM 中先于 feed 卡片出现）。失败时由调用端报错提示。
const DETECT_PROFILE_JS = `(function(){var links=Array.from(document.querySelectorAll('a[href*="/user/profile/"]'));var pick='';for(var i=0;i<links.length;i++){if((links[i].textContent||'').trim()==='我'){pick=links[i].getAttribute('href');break}}if(!pick&&links.length){pick=links[0].getAttribute('href')}if(!pick)return JSON.stringify({uid:''});var m=pick.match(/\\/user\\/profile\\/([0-9a-f]{24})/i);return JSON.stringify({uid:m?m[1]:''})})()`;

const COUNT_NOTE_JS = `JSON.stringify({n:document.querySelectorAll('section.note-item').length})`;

// 显式点击「收藏」tab（精确匹配文本"收藏"）——2026-08-18 修复：URL ?tab=collection 参数无效，
// 页面默认停在第一个「笔记」tab（自己发布的笔记），必须点击「收藏」tab 才进入收藏视图。
// 返回：{clicked:true, active:<激活tab文本>, n:<点击后卡片数>}
const CLICK_COLLECTION_TAB_JS = `(function(){
  var tabs=Array.from(document.querySelectorAll('.reds-tab-item'));
  var fav=tabs.find(function(el){return (el.textContent||'').trim()==='收藏'});
  if(!fav)return JSON.stringify({clicked:false,active:''});
  fav.click();
  var active='';
  var cur=tabs.find(function(el){return (el.className||'').indexOf('active')>=0});
  if(cur)active=(cur.textContent||'').trim();
  return JSON.stringify({clicked:true,active:active,n:document.querySelectorAll('section.note-item').length});
})()`;

// 增量滚动触发懒加载（陷阱 1：后台/隐藏 tab 时懒加载可能被节流；仅当卡片数不足才调用）
function buildScrollJs() {
  return `(function(){window.scrollBy(0,${SCROLL_STEP});return 'scrolled'})()`;
}

// 缓存卡片列表：DOM 出现顺序 = 收藏时间倒序（最新在前），offset/count 直接切片。
// 2026-08-18 修复：点击「收藏」tab 后 Vue 不清空「笔记」tab 的 DOM，section.note-item 是
// 「笔记残留 + 收藏新增」混合列表。必须先用 __noteCardIds（笔记 tab 原卡片 id 集合）过滤，
// 只保留收藏新增的卡片（收藏时间倒序，最新收藏在最前）。
const CACHE_CARDS_JS = `(()=>{
  var cards=Array.from(document.querySelectorAll('section.note-item'));
  var noteIds=window.__noteCardIds||null;
  var filtered=cards;
  if(noteIds&&noteIds.size){filtered=cards.filter(function(c){return !noteIds.has(c.getAttribute('data-note-id'))});}
  window.__cards=filtered.map(function(c,i){var t=c.querySelector('a.title'),cv=c.querySelector('a.cover');return {idx:i,id:c.getAttribute('data-note-id'),title:t?t.textContent.trim():'',coverHref:cv?cv.getAttribute('href'):''}});
  return JSON.stringify({n:window.__cards.length,totalDom:cards.length,filtered:filtered.length});
})()`;

// 记录当前（笔记 tab）已渲染的卡片 id 集合到 window.__noteCardIds —— 点击「收藏」前调用，
// 供 CACHE_CARDS_JS 过滤掉笔记残留，只留收藏新增卡片
const SNAPSHOT_NOTE_CARD_IDS_JS = `(function(){
  var ids=new Set(Array.from(document.querySelectorAll('section.note-item')).map(function(c){return c.getAttribute('data-note-id')}));
  window.__noteCardIds=ids;
  return JSON.stringify({n:ids.size});
})()`;

// 激活页面焦点 —— 2026-08-18 修复：后台/隐藏 tab（visibilityState=hidden）时 Vue 懒加载被
// 浏览器节流，点击「收藏」后不会加载新卡片。派发真实鼠标事件序列（mousedown+mouseup+click）
// 到 body 中心，浏览器视为真实用户交互，document.hasFocus() 变 true，懒加载恢复。
const ACTIVATE_FOCUS_JS = `(function(){
  var el=document.body;
  var r=el.getBoundingClientRect();
  var x=Math.max(10,Math.min(r.width/2,r.width-10));
  var y=Math.max(10,Math.min(r.height/2,r.height-10));
  ['mousedown','mouseup','click'].forEach(function(type){
    el.dispatchEvent(new MouseEvent(type,{bubbles:true,cancelable:true,view:window,clientX:x,clientY:y}));
  });
  try{window.focus();}catch(e){}
  return JSON.stringify({focus:document.hasFocus(),vis:document.visibilityState});
})()`;

// 确保回到列表页（残留弹层则 history.back）
const ENSURE_CLEAN_JS = `(function(){if(document.querySelector('#detail-title')){history.back();return 'backed'};return 'clean'})()`;

// 快照当前最大资源 startTime —— 陷阱 2：视频提取必须按时间过滤，否则上一篇的视频 URL 残留到下一篇
const SNAPSHOT_T0_JS = `(function(){var e=performance.getEntriesByType('resource');window.__t0=e.length?e[e.length-1].startTime:0;return JSON.stringify({t0:window.__t0})})()`;

const BACK_JS = `(function(){history.back();return 'back'})()`;

// 点击第 absIndex 张卡片的 a.cover（弹层模式；不要 tab.create 直开 explore 页）。
// absIndex 是绝对序号 = offset + i（SUMMARY Step 5 的 i 取 offset .. offset+count-1）。
// 2026-08-18 修复：DOM 里 section.note-item 是「笔记残留+收藏」混合列表，必须按过滤后的
// window.__cards[absIndex].id 在 DOM 中定位对应卡片点击（不能用混合列表的数组下标）。
function buildClickCoverJs(absIndex) {
  return `(function(){
    var card=(window.__cards&&window.__cards[${absIndex}])?window.__cards[${absIndex}]:null;
    if(!card||!card.id)return 'no-card';
    var cards=Array.from(document.querySelectorAll('section.note-item'));
    var target=null;
    for(var i=0;i<cards.length;i++){if(cards[i].getAttribute('data-note-id')===card.id){target=cards[i];break}}
    if(!target)return 'no-cover-match';
    var cv=target.querySelector('a.cover');
    if(!cv)return 'no-cover';
    cv.click();
    return 'clicked';
  })()`;
}

// 提取详情：标题回退到卡片标题（部分详情无 #detail-title，陷阱 3）、图片去重、视频按 __t0 时间过滤
function buildExtractDetailJs(absIndex) {
  return `(function(){var t=document.querySelector('#detail-title');var d=document.querySelector('#detail-desc');var card=(window.__cards&&window.__cards[${absIndex}])?window.__cards[${absIndex}]:null;var title=(t&&t.textContent.trim())?t.textContent.trim():(card?card.title:'');var imgs=Array.from(new Set(Array.from(document.querySelectorAll('.swiper-slide img, .slide img')).map(function(im){return im.src})));var t0=window.__t0||0;var vids=Array.from(new Set(Array.from(performance.getEntriesByType('resource')).filter(function(e){return e.startTime>=t0}).map(function(e){return e.name}).filter(function(u){return u.indexOf('/stream/')>=0&&u.indexOf('.mp4')>=0})));var data={id:card?card.id:'',title:title,desc:d?d.textContent.trim():'',imgs:imgs,video:vids,url:location.href};return JSON.stringify(data)})()`;
}

/* ------------------------- 工具 ------------------------- */

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function log(msg) {
  // 进度日志走 stderr，stdout 只允许最后一行 JSON
  console.error('[xhs-fav-export] ' + msg);
}

function relayCall(op, params = {}, timeout = 30000) {
  return fetch(`${RELAY_URL}/api/call`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ op, params, timeout }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) throw new Error(data.error);
      return data.result;
    });
}

async function ensureRelay() {
  try {
    const status = await (await fetch(`${RELAY_URL}/api/status`)).json();
    if (!status.extensionConnected) throw new Error('Extension not connected');
  } catch (e) {
    throw new Error(`Relay not available at ${RELAY_URL}. Is start-relay.mjs running? ${e.message}`);
  }
}

async function pageEval(tabId, code, groupId) {
  return relayCall('page.eval', { tabId, code, groupId });
}

async function countNoteItems(tabId, groupId) {
  const raw = await pageEval(tabId, COUNT_NOTE_JS, groupId);
  return JSON.parse(raw).n;
}

// 轮询 + 增量滚动，确保卡片数量 >= minCount（懒加载依赖真实滚动，陷阱 1）
async function ensureCardsLoaded(tabId, groupId, minCount) {
  let n = await countNoteItems(tabId, groupId);
  if (n >= minCount) return n;
  log(`当前卡片 ${n} 篇，目标 ${minCount} 篇，开始增量滚动触发懒加载`);
  const deadline = Date.now() + CARD_LOAD_DEADLINE_MS;
  let lastN = n;
  let idleRounds = 0;
  while (Date.now() < deadline && n < minCount) {
    try {
      await pageEval(tabId, buildScrollJs(), groupId);
    } catch (e) {
      log(`滚动失败：${e.message}`);
    }
    await sleep(SCROLL_ROUND_MS);
    n = await countNoteItems(tabId, groupId);
    if (n > lastN) {
      lastN = n;
      idleRounds = 0;
    } else if (++idleRounds >= MAX_GROWTH_IDLE_ROUNDS) {
      break;
    }
  }
  log(`滚动结束，卡片 ${n} 篇`);
  return n;
}

// 打开收藏 tab 并等待 SPA 加载（返回的 url/title 为空是正常现象，必须 sleep 再校验）
// 2026-08-18 修复：?tab=collection URL 参数无效（页面停在「笔记」tab），必须点击「收藏」tab；
// 且点击后 Vue 不清空笔记 tab 的 DOM，需先快照笔记卡片 id，缓存收藏时过滤残留
async function openCollectionTab(groupId, profileUrl) {
  const t = await relayCall('tab.create', { url: `${profileUrl}?tab=collection`, active: true, groupId });
  await sleep(SLEEP_AFTER_TAB_CREATE);
  // 快照前先等「笔记」tab 卡片稳定（懒加载可能还在跑，快照早了会漏掉部分笔记 id，
  // 导致它们被误判成"收藏"）——最多等 20s，2 轮数量不变即稳定
  const stabDeadline = Date.now() + 20000;
  let lastCount = -1;
  let stableRounds = 0;
  while (Date.now() < stabDeadline && stableRounds < 2) {
    try {
      const raw = await pageEval(t.id, COUNT_NOTE_JS, groupId);
      const n = JSON.parse(raw).n;
      if (n === lastCount) stableRounds++; else { stableRounds = 0; lastCount = n; }
      if (stableRounds < 2) await sleep(1500);
    } catch (e) { await sleep(1500); }
  }
  log(`笔记 tab 卡片稳定于 ${lastCount} 篇，开始快照`);
  // 快照当前（笔记 tab）已渲染卡片 id —— 供后续过滤收藏残留
  try {
    await pageEval(t.id, SNAPSHOT_NOTE_CARD_IDS_JS, groupId);
  } catch (e) {}
  // 显式点击「收藏」tab（必须，否则导出的是自己发布的「笔记」tab）
  const clickRaw = await pageEval(t.id, CLICK_COLLECTION_TAB_JS, groupId);
  let clickState = { clicked: false };
  try { clickState = JSON.parse(clickRaw); } catch (e) {}
  log(`点击收藏 tab: ${JSON.stringify(clickState)}`);
  await sleep(2500); // active class 更新有延迟，多等一会
  // 激活页面焦点（后台 tab 懒加载被节流，需真实交互信号唤醒）
  try {
    const focusRaw = await pageEval(t.id, ACTIVATE_FOCUS_JS, groupId);
    log(`激活焦点: ${focusRaw}`);
  } catch (e) {}
  await sleep(1000);
  // 再读一次激活 tab 确认切到收藏（首次读取可能滞后）
  try {
    const confirmRaw = await pageEval(t.id, `(function(){var cur=Array.from(document.querySelectorAll('.reds-tab-item')).find(function(el){return (el.className||'').indexOf('active')>=0});return JSON.stringify({active:cur?(cur.textContent||'').trim():''})})()`, groupId);
    const confirmState = JSON.parse(confirmRaw);
    log(`确认激活 tab: ${confirmState.active}`);
  } catch (e) {}
  return { tabId: t.id, clickState };
}

// 文件名净化：去掉 \/:*?"<>| 与控制字符、strip 首尾点与空白、截断 50 字符、空则 'untitled'
function sanitizeTitle(title) {
  let s = String(title || '')
    .replace(/[\\/:*?"<>|\u0000-\u001f\u007f]/g, '')
    .replace(/^[\s.]+|[\s.]+$/g, '')
    .slice(0, MAX_TITLE_LEN);
  return s || 'untitled';
}

// 单篇导出（串行）。absIndex 是绝对序号（offset+i），seq 用于文件名与「收藏于」。
async function exportOneNote(tabId, groupId, absIndex, seq) {
  // 5a. 确保在列表页（残留弹层则 history.back 兜底）
  await pageEval(tabId, ENSURE_CLEAN_JS, groupId);
  await sleep(SLEEP_AFTER_ENSURE_CLEAN);
  // 5b. 快照 __t0（视频时间过滤）
  await pageEval(tabId, SNAPSHOT_T0_JS, groupId);
  // 5c. 点击 a.cover 打开弹层
  const clickRes = await pageEval(tabId, buildClickCoverJs(absIndex), groupId);
  if (clickRes !== 'clicked') throw new Error('click cover 失败: ' + clickRes);
  await sleep(SLEEP_AFTER_COVER_CLICK);
  // 6. 提取详情
  const raw = await pageEval(tabId, buildExtractDetailJs(absIndex), groupId);
  const data = JSON.parse(raw);
  const noteId = data.id || ((data.url || '').match(/\/explore\/([0-9a-f]{24})/i) || [])[1] || '';
  if (!data.title) throw new Error('标题为空（详情与卡片回退均无标题）');
  if (!data.url || data.url.indexOf('/explore/') < 0) {
    throw new Error(`原文链接不含 /explore/（弹层未正确打开?）: ${data.url}`);
  }
  const imgs = Array.isArray(data.imgs) ? data.imgs.filter(Boolean) : [];
  const vids = Array.isArray(data.video) ? data.video.filter(Boolean) : [];
  const isPartial = !String(data.desc || '').trim() && imgs.length === 0 && vids.length === 0;
  // 7. 关闭弹层
  try {
    await pageEval(tabId, BACK_JS, groupId);
  } catch (_) {
    // 关闭失败不致命，下一轮 5a 会兜底
  }
  await sleep(SLEEP_AFTER_BACK);
  return { data, noteId, isPartial };
}

// 带恢复的单篇导出：非断连瞬时错误重试 1 次；扩展连接中断则重建 tab（陷阱 5 的恢复路径，
// 旧 tab 页面内存全部丢失，逐篇落盘把损失控在单篇），重建后重新加载卡片再重试。
async function exportNoteSafely(tabState, groupId, absIndex, seq, profileUrl) {
  try {
    return await exportOneNote(tabState.tabId, groupId, absIndex, seq);
  } catch (e) {
    const msg = String(e && e.message ? e.message : e);
    if (msg.indexOf('disconnected') >= 0 || msg.indexOf('Extension not connected') >= 0) {
      log(`扩展连接中断（${msg}），重建 tab 恢复...`);
      await relayCall('tab.close', { tabId: tabState.tabId }).catch(() => {});
      const opened = await openCollectionTab(groupId, profileUrl);
      tabState.tabId = opened.tabId;
      const n = await countNoteItems(tabState.tabId, groupId);
      if (n === 0) throw new Error('重建 tab 后收藏视图无卡片（未登录?）');
      await ensureCardsLoaded(tabState.tabId, groupId, offset + count);
      await pageEval(tabState.tabId, CACHE_CARDS_JS, groupId);
      return await exportOneNote(tabState.tabId, groupId, absIndex, seq);
    }
    // 非断连瞬时错误：尽量关掉残留弹层，重试 1 次
    try {
      await pageEval(tabState.tabId, BACK_JS, groupId);
      await sleep(SLEEP_AFTER_BACK);
    } catch (_) {}
    return await exportOneNote(tabState.tabId, groupId, absIndex, seq);
  }
}

function writeNoteFile(outputDir, seq, data, isPartial) {
  const baseName = `${seq}_${sanitizeTitle(data.title)}`;
  const fileName = baseName + (isPartial ? ' (partial)' : '') + '.md';
  const imgs = Array.isArray(data.imgs) ? data.imgs.filter(Boolean) : [];
  const vids = Array.isArray(data.video) ? data.video.filter(Boolean) : [];
  const lines = [
    `# ${data.title}`,
    `原文链接: ${data.url}`,
    `收藏于: ${seq}`,
    '---',
    String(data.desc || ''),
    '---',
  ];
  if (imgs.length) lines.push(`图片: ${imgs.join(' ')}`);
  if (vids.length) lines.push(`视频: ${vids.join(' ')}`);
  writeFileSync(join(outputDir, fileName), lines.join('\n') + '\n', 'utf-8');
  return fileName;
}

/* ------------------------- 入口 ------------------------- */

async function main() {
  // --- 读入参（requirement 定义：offset / count / outputDir） ---
  let input = {};
  const inputPath = process.argv[2];
  if (inputPath) {
    input = JSON.parse(readFileSync(inputPath, 'utf-8'));
  } else {
    try {
      input = JSON.parse(readFileSync('input.json', 'utf-8'));
    } catch (_) {
      // 没有 input.json 时用默认值
    }
  }
  const offset = Number(input.offset ?? 0);
  const count = Number(input.count ?? 10);
  const outputDir = input.outputDir || input.output_dir || '/tmp/xhs-fav-export-output';
  if (!Number.isInteger(offset) || offset < 0) throw new Error(`offset 非法（须为非负整数）: ${offset}`);
  if (!Number.isInteger(count) || count < 1) throw new Error(`count 非法（须为正整数）: ${count}`);
  mkdirSync(outputDir, { recursive: true });

  await ensureRelay();
  let groupId = null;
  let tabState = null;
  const failures = [];
  const partialNoteIds = [];
  const notes = [];
  let available = 0;

  try {
    // Step 1 — 任务分组（多任务隔离）
    const g = await relayCall('group.create', { name: GROUP_NAME });
    groupId = g.groupId;
    await relayCall('group.setStatus', { groupId, status: 'running' }).catch(() => {});

    // Step 2 — 探测当前登录用户 profile URL（收藏 tab 必须是自己主页）
    let profileUrl = String(input.profileUrl || '').trim();
    if (!profileUrl) {
      let homeTab = null;
      try {
        homeTab = await relayCall('tab.create', { url: HOMEPAGE, active: true, groupId });
        await sleep(SLEEP_AFTER_TAB_CREATE);
        const det = JSON.parse(await pageEval(homeTab.id, DETECT_PROFILE_JS, groupId));
        if (!det.uid) {
          throw new Error('未检测到当前登录用户主页：首页找不到个人主页链接。请确认已在 Chrome 中登录小红书，或在 input.json 提供 profileUrl。');
        }
        profileUrl = `https://www.xiaohongshu.com/user/profile/${det.uid}`;
        log(`已探测到登录用户 profile: ${profileUrl}`);
      } finally {
        if (homeTab) {
          try {
            await relayCall('tab.close', { tabId: homeTab.id });
          } catch (_) {}
        }
      }
    } else {
      profileUrl = profileUrl.split('?')[0].split('#')[0];
    }

    // Step 3 — 打开收藏 tab（active:true；SPA 加载中 url/title 返回为空是正常现象）
    // 2026-08-18 修复：openCollectionTab 内部已显式点击「收藏」tab（URL 参数无效）
    const opened = await openCollectionTab(groupId, profileUrl);
    tabState = { tabId: opened.tabId, clickState: opened.clickState };
    if (!opened.clickState || !opened.clickState.clicked) {
      log('警告：未找到「收藏」tab（页面结构可能变化），继续尝试读取当前视图卡片');
    }

    // Step 4 — 校验收藏视图（首屏渲染慢时轮询等待，确认不是"未登录/空视图"才继续）
    let n = 0;
    const zeroDeadline = Date.now() + CARD_LOAD_DEADLINE_MS;
    while (Date.now() < zeroDeadline && n === 0) {
      n = await countNoteItems(tabState.tabId, groupId);
      if (n === 0) await sleep(1500);
    }
    if (n === 0) {
      throw new Error('收藏 tab 无任何卡片（未登录 / 探测到的主页不是自己 / 页面结构变化）。若已登录仍失败，请在 input.json 提供 profileUrl。');
    }
    const minCount = offset + count;
    await ensureCardsLoaded(tabState.tabId, groupId, minCount);

    // Step 5 — 缓存卡片列表到 window.__cards
    const cacheRaw = await pageEval(tabState.tabId, CACHE_CARDS_JS, groupId);
    available = JSON.parse(cacheRaw).n;
    if (available <= offset) {
      throw new Error(`收藏列表仅加载 ${available} 篇（offset=${offset} 处无更多卡片）：本环境懒加载可能受限，请用更小的 offset 分批导出。`);
    }
    const target = Math.min(count, available - offset);
    log(`共加载 ${available} 篇收藏，本次导出 ${target} 篇（offset=${offset}）`);

    // Step 6 — 串行逐篇：提取 → 立即落盘（陷阱 5：逐篇落盘，debugger 挂掉只丢单篇）
    for (let i = 0; i < target; i++) {
      const absIndex = offset + i; // SUMMARY Step 5：i 取 offset .. offset+count-1
      try {
        const { data, noteId, isPartial } = await exportNoteSafely(tabState, groupId, absIndex, absIndex, profileUrl);
        const fileName = writeNoteFile(outputDir, absIndex, data, isPartial);
        notes.push({ seq: absIndex, id: noteId, title: data.title, partial: isPartial, file: fileName });
        if (isPartial) partialNoteIds.push(noteId);
        log(`已导出 #${absIndex} ${data.title}${isPartial ? ' (partial)' : ''}`);
      } catch (e) {
        failures.push({ index: absIndex, seq: absIndex, error: String(e && e.message ? e.message : e) });
        log(`第 #${absIndex} 篇导出失败（已跳过）：${e.message}`);
      }
    }

    // 收尾：关掉可能残留的弹层
    try {
      await pageEval(tabState.tabId, BACK_JS, groupId);
    } catch (_) {}
  } finally {
    if (tabState) {
      try {
        await relayCall('tab.close', { tabId: tabState.tabId });
      } catch (_) {}
    }
    if (groupId) {
      try {
        await relayCall('group.close', { groupId });
      } catch (_) {}
    }
  }

  // Step 7 — summary.json（Accept 规定格式）
  const expected = Math.min(count, Math.max(0, available - offset));
  const summary = {
    total_exported: notes.length,
    offset,
    count,
    skipped_partial: partialNoteIds,
  };
  if (failures.length) summary.failures = failures;
  if (notes.length < expected) {
    summary.note =
      '实际导出数少于目标' +
      (failures.length ? `（${failures.length} 篇提取失败）` : '') +
      (available - offset < count ? '（收藏列表在 offset 后不足 count 篇）' : '');
  }
  writeFileSync(join(outputDir, 'summary.json'), JSON.stringify(summary, null, 2), 'utf-8');

  // output_files（若调用方指定）：res.json 只放元信息，data.md 放导出文件清单
  const outFiles = input.output_files || {};
  if (outFiles.result) {
    writeFileSync(
      join(outputDir, outFiles.result),
      JSON.stringify(
        {
          status: notes.length === 0 ? 'failed' : failures.length ? 'partial' : 'success',
          total_exported: notes.length,
          offset,
          count,
          expected,
          skipped_partial: partialNoteIds,
          failures,
          exported_files: notes.map((n) => n.file),
        },
        null,
        2
      ),
      'utf-8'
    );
  }
  if (outFiles.data) {
    const manifest = notes.length
      ? notes.map((n) => `- \`${n.file}\` — ${n.title}${n.partial ? ' (partial)' : ''}`).join('\n')
      : '(no files exported)';
    writeFileSync(join(outputDir, outFiles.data), manifest + '\n', 'utf-8');
  }

  const status = notes.length === 0 ? 'failed' : failures.length || partialNoteIds.length ? 'partial' : 'success';
  const summaryText =
    `已导出 ${notes.length} 篇收藏笔记到 ${outputDir}` +
    (partialNoteIds.length ? `（${partialNoteIds.length} 篇仅标题+链接标记 partial）` : '') +
    (failures.length ? `（${failures.length} 篇失败）` : '');
  console.log(JSON.stringify({ status, summary: summaryText, output_dir: outputDir }));
}

main().catch((e) => {
  console.error('[xhs-fav-export] fatal: ' + (e && e.stack ? e.stack : e));
  console.log(JSON.stringify({ status: 'failed', error: String(e && e.message ? e.message : e) }));
  process.exit(0);
});
