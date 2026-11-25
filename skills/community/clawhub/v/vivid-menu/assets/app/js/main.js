/* ============================================================
 * main.js — 界面编排
 * 只做三件事：把状态画到屏幕上、把用户动作翻译成工具调用、
 * 在两条驱动路径之间做切换。
 * ============================================================ */

import { blankMenu, blankDish, updateDish, removeDish, THEMES, THEME_LIST, stats, themeOf } from './model.js';
import { renderMenu } from './render.js';
import { inspectMenu } from './inspect.js';
import { createToolset, BRIEF } from './protocol.js';
import { runLocal, autoFix, autoPickSignature, redrawAll, mountWebMCP } from './driver.js';
import { readImageFile, cropRegion, fileFromPaste } from './photo.js';
import { downloadSvg, downloadPng, copyPng } from './export.js';
import { store, PRESETS } from './store.js';
import { parseTextMenu } from './parse.js';
import { inferKind } from './art/index.js';

/* ---------------- DOM ---------------- */

const $ = (id) => document.getElementById(id);
const dom = {
  stage: $('stage'),
  leftPane: $('leftPane'),
  sourceView: $('sourceView'),
  paperHolder: $('paperHolder'),
  cmdInput: $('cmdInput'),
  btnRun: $('btnRun'),
  dishCount: $('dishCount'),
  engineStatus: $('engineStatus'),
  engineText: $('engineText'),
  themeSwatch: $('themeSwatch'),
  intro: $('intro'),
  progress: $('progress'),
  toast: $('toast'),
  fileInput: $('fileInput'),
  sheetMask: $('sheetMask'),
  drawerMask: $('drawerMask'),
  drawerBody: $('drawerBody'),
  briefMask: $('briefMask'),
  briefBody: $('briefBody'),
  mcpHint: $('mcpHint'),
};

/* ---------------- 状态 ---------------- */

const state = {
  menu: blankMenu({ name: '' }),
  source: { dataUrl: '', width: 0, height: 0, text: '', zoom: null },
  editingId: null,
  busy: false,
  focus: false,
  events: [],
  dirty: false,
};

let rafId = 0;
const scheduleRender = () => {
  if (rafId) return;
  rafId = requestAnimationFrame(() => {
    rafId = 0;
    paintPaper();
    paintMeta();
  });
};

/* ---------------- 轻提示 ---------------- */

let toastTimer = null;
function toast(msg, isErr = false) {
  dom.toast.textContent = msg;
  dom.toast.classList.toggle('err', isErr);
  dom.toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => dom.toast.classList.remove('show'), 2600);
}

/* ---------------- 会话上下文（供工具调用） ---------------- */

const ctx = {
  getMenu: () => state.menu,
  setMenu: (m) => {
    state.menu = { ...m, sourceImage: state.source.dataUrl || '' };
    store.save(state.menu);
    scheduleRender();
  },
  getSource: () => state.source,
  pushEvent: (type, payload) => state.events.push({ type, payload }),
  takeEvent: () => state.events.shift() || null,
  cropSource: (box) => cropRegion(state.source, box),
};

const toolset = createToolset(ctx);

/* ---------------- 绘制屏幕 ---------------- */

function paintPaper() {
  const { svg } = renderMenu(state.menu);
  dom.paperHolder.innerHTML = svg;
  dom.paperHolder.style.background = themeOf(state.menu).paper;
}

function paintMeta() {
  const s = stats(state.menu);
  dom.dishCount.textContent = `${s.count} 道菜${s.signatureCount ? ` · ${s.signatureCount} 招牌` : ''}`;
  dom.themeSwatch.style.background = themeOf(state.menu).paper;
  dom.btnRun.disabled = state.busy;
}

function paintSource() {
  const box = dom.sourceView;
  const s = state.source;

  if (s.dataUrl) {
    box.innerHTML = `
      <div class="photo-box">
        <img src="${s.dataUrl}" alt="原始菜单">
        ${state.busy ? '<div class="scan"></div>' : ''}
      </div>
      ${s.zoom ? `
        <div class="zoom-box">
          <div class="zb-head"><span>局部放大</span><span>${Math.round(s.zoom.w * 100)}% 区域</span></div>
          <img src="${s.zoom.dataUrl}" alt="放大区域">
        </div>` : ''}
      <div class="source-empty">
        <b>照片只在本机，不上传</b>
        浏览器本地读不出图上的字。把菜名和价格粘到下面的框里，就能开始画。
      </div>`;
    return;
  }

  if (s.text.trim()) {
    const st = stats(state.menu);
    box.innerHTML = `<div class="text-box">${escapeHtml(s.text)}</div>` + (st.count ? miniStat(st) : '');
    return;
  }

  if (state.menu.dishes.length) {
    const st = stats(state.menu);
    box.innerHTML = `
      <div class="source-empty">
        <b>这张已经画好了</b>
        右边是成品。点任意一道菜可以改名字、价格和说明；<br>也可以把文字粘到下面的框里，重新生成一张。
      </div>` + miniStat(st);
    return;
  }

  box.innerHTML = `<div class="source-empty">
      <b>还没有素材</b>
      上传一张菜单照片，或把你的菜单文字粘进来。<br>一行一道菜就行。
    </div>`;
}

function miniStat(st) {
  return `<div class="mini-stat">
    <div><span>菜品</span><b>${st.count}</b></div>
    <div><span>分节</span><b>${st.sections.length}</b></div>
    <div><span>招牌</span><b>${st.signatureCount}</b></div>
  </div>`;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

/* ---------------- 进度 ---------------- */

function showProgress(ratio, label) {
  dom.progress.hidden = false;
  dom.progress.querySelector('.bar i').style.width = `${Math.round(ratio * 100)}%`;
  dom.progress.querySelector('.label').textContent = label;
}
function hideProgress() {
  dom.progress.hidden = true;
  dom.progress.querySelector('.bar i').style.width = '0%';
}

/* ---------------- 开场 ---------------- */

function hideIntro() {
  dom.intro.classList.add('hidden');
}
function showIntro() {
  dom.intro.classList.remove('hidden');
}

/* ---------------- 生成 ---------------- */

async function generate() {
  if (state.busy) return;

  const text = (dom.cmdInput.value || '').trim() || state.source.text;
  if (!text.trim()) {
    if (state.source.dataUrl) {
      toast('照片里有字，但浏览器认不出来。请把菜名粘到下面的框里。', true);
      dom.cmdInput.focus();
    } else {
      toast('先粘一段菜单文字，或上传一张照片', true);
    }
    return;
  }

  state.source.text = text;
  state.busy = true;
  dom.btnRun.textContent = '绘制中…';
  dom.btnRun.disabled = true;
  paintSource();
  showProgress(0.04, '铺纸…');
  hideIntro();

  try {
    const res = await runLocal(ctx, toolset, {
      pace: 58,
      onStep: (s) => showProgress(0.08 + (s.done / s.total) * 0.9, s.label),
    });

    if (!res.ok) {
      toast(res.error + (res.hint ? '：' + res.hint : ''), true);
      return;
    }

    store.save(state.menu, { immediate: true });
    // 文字已经落到素材区，输入框腾出来当指令区
    dom.cmdInput.value = '';
    dom.cmdInput.placeholder = '继续说要改什么，例如：把招牌换成酸辣粉 / 价格都加个 ¥';
    paintSource();
    scheduleRender();

    const rep = res.report;
    const parts = [`画好了 ${res.parsed.dishes} 道菜`];
    if (rep.errors) parts.push(`${rep.errors} 处要修`);
    else if (rep.warns) parts.push(`${rep.warns} 处可优化`);
    else parts.push('质检通过');
    if (res.fixed.length) parts.push(`自动修了 ${res.fixed.length} 项`);
    showProgress(1, parts.join('，'));
    toast(parts.join('，'));
  } catch (e) {
    console.error(e);
    toast('绘制出错：' + e.message, true);
  } finally {
    state.busy = false;
    dom.btnRun.textContent = '开始绘制';
    dom.btnRun.disabled = false;
    paintMeta();
    paintSource();
    setTimeout(hideProgress, 1000);
  }
}

/* ---------------- 素材输入 ---------------- */

async function loadPhoto(file) {
  if (!file) return;
  try {
    const img = await readImageFile(file);
    state.source = { ...state.source, dataUrl: img.dataUrl, width: img.width, height: img.height, zoom: null };
    state.menu = { ...state.menu, sourceImage: img.dataUrl };
    store.save(state.menu);
    hideIntro();
    paintSource();
    toast('照片已就位。把菜名粘到下面的框里，就能开始画。');
  } catch (e) {
    toast(e.message, true);
  }
}

function loadText(text) {
  state.source.text = text;
  dom.cmdInput.value = text;
  hideIntro();
  paintSource();
  dom.cmdInput.focus();
}

/* ---------------- 打开菜单 ---------------- */

function openMenu(menu) {
  state.menu = { ...menu };
  state.source = {
    dataUrl: menu.sourceImage || '',
    width: 0, height: 0,
    text: '',
    zoom: null,
  };
  hideIntro();
  paintSource();
  scheduleRender();
  paintMeta();
}

/* ---------------- 菜品编辑 ---------------- */

function bindPaperClicks() {
  dom.paperHolder.addEventListener('click', (e) => {
    const hit = e.target.closest('.vm-hit');
    if (!hit) return;
    const id = hit.getAttribute('data-dish');
    if (id) openSheet(id);
  });
}

function openSheet(dishId) {
  const d = state.menu.dishes.find((x) => x.id === dishId);
  if (!d) return;
  state.editingId = dishId;

  $('fName').value = d.name || '';
  $('fPrice').value = d.price || '';
  $('fSection').value = d.section || '';
  $('fBlurb').value = d.blurb || '';
  $('fTags').value = (d.tags || []).join(',');
  $('fSig').checked = !!d.signature;
  $('fSigNote').value = d.signature_note || '';
  $('sigNoteWrap').hidden = !d.signature;
  $('artKind').textContent = d.kind || inferKind(d.name, d.tags) || '—';

  dom.sheetMask.hidden = false;
  $('fName').focus();
}

function closeSheet() {
  dom.sheetMask.hidden = true;
  state.editingId = null;
}

function saveSheet() {
  const id = state.editingId;
  if (!id) return;
  const patch = {
    name: $('fName').value.trim(),
    price: $('fPrice').value.trim(),
    section: $('fSection').value.trim(),
    blurb: $('fBlurb').value.trim(),
    tags: $('fTags').value.split(/[,，、]/).map((s) => s.trim()).filter(Boolean).slice(0, 3),
    signature: $('fSig').checked,
    signature_note: $('fSigNote').value.trim(),
  };
  if (!patch.name) { toast('菜名不能为空', true); return; }
  ctx.setMenu(updateDish(state.menu, id, patch));
  store.save(state.menu, { immediate: true });
  closeSheet();
  scheduleRender();
}

/* ---------------- 合集 ---------------- */

function openDrawer() {
  const saved = store.list();
  const items = [
    ...saved.map((m) => ({ menu: m, saved: true })),
    ...PRESETS.map((m) => ({ menu: m, saved: false })),
  ];

  if (!items.length) {
    dom.drawerBody.innerHTML = '<div class="gal-empty">还没有存过菜单。<br>画完一张就会自动出现在这里。</div>';
  } else {
    dom.drawerBody.innerHTML = items.map(({ menu, saved }, i) => {
      const { svg } = renderMenu(menu, { hitAreas: false });
      const s = stats(menu);
      return `<div class="gal-item" data-idx="${i}">
        <div class="thumb">${svg}</div>
        <div class="meta">
          <b>${escapeHtml(menu.name || '未命名')}</b>
          <span>${s.count} 道菜 · ${saved ? '我存的' : '示例'}</span>
        </div>
        ${saved ? '<button class="del" data-del="' + menu.id + '" title="删除">×</button>' : ''}
      </div>`;
    }).join('');

    dom.drawerBody.querySelectorAll('.gal-item').forEach((node) => {
      node.addEventListener('click', (e) => {
        if (e.target.closest('.del')) return;
        const idx = Number(node.getAttribute('data-idx'));
        openMenu(items[idx].menu);
        dom.drawerMask.hidden = true;
        toast('已打开「' + (items[idx].menu.name || '未命名') + '」');
      });
    });

    dom.drawerBody.querySelectorAll('.del').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        store.remove(btn.getAttribute('data-del'));
        openDrawer();
      });
    });
  }
  dom.drawerMask.hidden = false;
}

/* ---------------- 主题面板 ---------------- */

let themePanel = null;
function toggleThemePanel() {
  if (themePanel) { closeThemePanel(); return; }

  themePanel = document.createElement('div');
  themePanel.className = 'theme-panel';
  themePanel.innerHTML = THEME_LIST.map((t) => `
    <button data-theme="${t.id}" class="${state.menu.theme === t.id ? 'on' : ''}">
      <span class="chip" style="background:${t.paper};border-color:${t.edge}">
        <i style="background:${t.ink}"></i><i style="background:${t.accent}"></i>
      </span>
      <span class="tn">${t.label}</span>
    </button>`).join('');

  document.body.appendChild(themePanel);
  const r = $('btnTheme').getBoundingClientRect();
  themePanel.style.top = `${r.bottom + 8}px`;
  themePanel.style.left = `${Math.max(12, Math.min(r.left - 60, window.innerWidth - 230))}px`;

  themePanel.querySelectorAll('button').forEach((b) => {
    b.addEventListener('click', () => {
      ctx.setMenu({ ...state.menu, theme: b.getAttribute('data-theme') });
      store.save(state.menu, { immediate: true });
      closeThemePanel();
      toast('换成「' + THEMES[b.getAttribute('data-theme')].label + '」');
    });
  });

  setTimeout(() => document.addEventListener('click', outsideTheme), 0);
}

function outsideTheme(e) {
  if (themePanel && !themePanel.contains(e.target) && e.target.id !== 'btnTheme') closeThemePanel();
}

function closeThemePanel() {
  if (themePanel) { themePanel.remove(); themePanel = null; }
  document.removeEventListener('click', outsideTheme);
}

/* ---------------- 绑定 ---------------- */

function bind() {
  // 开场三个入口
  dom.intro.querySelectorAll('.choice').forEach((b) => {
    b.addEventListener('click', () => {
      const act = b.getAttribute('data-act');
      if (act === 'photo') dom.fileInput.click();
      if (act === 'text') { hideIntro(); dom.cmdInput.focus(); }
      if (act === 'demo') { openMenu(PRESETS[0]); toast('已打开示例菜单，可以直接改'); }
    });
  });

  $('btnPick').addEventListener('click', () => dom.fileInput.click());
  $('btnText').addEventListener('click', () => { hideIntro(); dom.cmdInput.focus(); dom.cmdInput.select(); });
  $('btnReset').addEventListener('click', () => {
    if (state.menu.dishes.length && !confirm('清空当前菜单，重新开始？')) return;
    state.menu = blankMenu({ theme: state.menu.theme });
    state.source = { dataUrl: '', width: 0, height: 0, text: '', zoom: null };
    dom.cmdInput.value = '';
    store.save(state.menu, { immediate: true });
    paintSource();
    scheduleRender();
    paintMeta();
    showIntro();
  });

  dom.fileInput.addEventListener('change', (e) => {
    const f = e.target.files?.[0];
    dom.fileInput.value = '';
    loadPhoto(f);
  });

  dom.btnRun.addEventListener('click', generate);

  // 粘贴：图片优先进素材，纯文字进输入框
  document.addEventListener('paste', (e) => {
    const f = fileFromPaste(e);
    if (f) {
      e.preventDefault();
      loadPhoto(f);
      return;
    }
    const t = e.clipboardData?.getData('text/plain') || '';
    if (t && /[\u4e00-\u9fa5]/.test(t) && /\d/.test(t) && document.activeElement !== dom.cmdInput) {
      e.preventDefault();
      loadText(t);
      toast('文字已接住，点「开始绘制」试试');
    }
  });

  // 拖入
  let dragDepth = 0;
  window.addEventListener('dragenter', (e) => {
    if (!e.dataTransfer?.types?.includes('Files')) return;
    dragDepth += 1;
    document.body.classList.add('drag-over');
  });
  window.addEventListener('dragleave', () => {
    dragDepth = Math.max(0, dragDepth - 1);
    if (!dragDepth) document.body.classList.remove('drag-over');
  });
  window.addEventListener('dragover', (e) => e.preventDefault());
  window.addEventListener('drop', (e) => {
    e.preventDefault();
    dragDepth = 0;
    document.body.classList.remove('drag-over');
    const f = e.dataTransfer?.files?.[0];
    if (f && f.type.startsWith('image/')) loadPhoto(f);
  });

  // 顶栏
  $('btnTheme').addEventListener('click', toggleThemePanel);
  $('btnGallery').addEventListener('click', openDrawer);
  $('btnBrief').addEventListener('click', () => {
    dom.briefBody.textContent = BRIEF;
    dom.briefMask.hidden = false;
  });
  $('briefClose').addEventListener('click', () => { dom.briefMask.hidden = true; });
  dom.briefMask.addEventListener('click', (e) => { if (e.target === dom.briefMask) dom.briefMask.hidden = true; });

  // 底部工具
  $('btnFocus').addEventListener('click', () => {
    state.focus = !state.focus;
    dom.stage.classList.toggle('focus', state.focus);
    $('btnFocus').classList.toggle('on', state.focus);
  });
  $('btnSvg').addEventListener('click', () => {
    if (!state.menu.dishes.length) return toast('还没有菜可导出', true);
    downloadSvg(state.menu);
    toast('SVG 已下载');
  });
  $('btnPng').addEventListener('click', async () => {
    if (!state.menu.dishes.length) return toast('还没有菜可导出', true);
    const r = await copyPng(state.menu, 2);
    toast(r === 'copied' ? '图片已复制，去微信里粘贴' : r === 'downloaded' ? '已下载 PNG' : '导出失败', r === 'failed');
  });

  // 编辑浮层
  $('sheetClose').addEventListener('click', closeSheet);
  dom.sheetMask.addEventListener('click', (e) => { if (e.target === dom.sheetMask) closeSheet(); });
  $('btnSaveDish').addEventListener('click', saveSheet);
  $('btnDel').addEventListener('click', () => {
    const id = state.editingId;
    if (!id) return;
    ctx.setMenu(removeDish(state.menu, id));
    store.save(state.menu, { immediate: true });
    closeSheet();
    scheduleRender();
    toast('已删除');
  });
  $('fSig').addEventListener('change', (e) => { $('sigNoteWrap').hidden = !e.target.checked; });
  $('btnRedraw').addEventListener('click', () => {
    const id = state.editingId;
    if (!id) return;
    const d = state.menu.dishes.find((x) => x.id === id);
    if (!d) return;
    // 用一个新种子重画：换掉 art 并微调 id 参与哈希
    const next = updateDish(state.menu, id, { art: '', kind: d.kind || inferKind(d.name, d.tags) });
    next.dishes = next.dishes.map((x) =>
      x.id === id ? { ...x, _seed: Math.random().toString(36).slice(2) } : x,
    );
    ctx.setMenu(next);
    scheduleRender();
    toast('换了一幅');
  });

  // 抽屉
  $('drawerClose').addEventListener('click', () => { dom.drawerMask.hidden = true; });
  dom.drawerMask.addEventListener('click', (e) => { if (e.target === dom.drawerMask) dom.drawerMask.hidden = true; });

  // 快捷键
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeSheet();
      dom.drawerMask.hidden = true;
      dom.briefMask.hidden = true;
      closeThemePanel();
    }
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') generate();
    if ((e.metaKey || e.ctrlKey) && e.key === 's') {
      e.preventDefault();
      store.save(state.menu, { immediate: true });
      toast('已保存到合集');
    }
  });

  window.addEventListener('beforeunload', () => store.flush());
  bindPaperClicks();
}

/* ---------------- 引擎状态 ---------------- */

function initEngineBadge() {
  const mcp = mountWebMCP(toolset, {
    name: 'vivid-menu',
    description: '生动菜单：逐道菜绘制餐厅菜单',
  });
  if (mcp.supported) {
    dom.engineStatus.setAttribute('data-state', 'mcp');
    dom.engineText.textContent = `Agent 已接入 · ${mcp.count} 个工具`;
    dom.mcpHint.innerHTML = `<span style="color:#4a6b46">WebMCP 已就绪，${mcp.count} 个工具可供外部 Agent 调用</span>`;
  } else {
    dom.engineStatus.setAttribute('data-state', 'local');
    dom.engineText.textContent = '内置引擎';
    dom.mcpHint.textContent = '当前浏览器无 WebMCP，使用内置引擎（不影响使用）';
  }
}

/* ---------------- 启动 ---------------- */

function boot() {
  bind();
  initEngineBadge();
  paintSource();
  paintMeta();

  // 恢复上次的菜单
  const activeId = store.activeId();
  const saved = activeId ? store.get(activeId) : null;
  if (saved && saved.dishes?.length) {
    openMenu(saved);
  } else {
    paintPaper();
  }

  // 提示当前能力边界
  console.info('%c生动菜单', 'color:#b4472f;font-weight:600', '就绪。9 个工具已挂到 window.vividMenu');
  window.vividMenu = { state, ctx, toolset, renderMenu, inspectMenu, parseTextMenu };

  // 分享/演示入口：?demo=0|1|2 直接打开内置示例
  const q = new URLSearchParams(location.search);
  if (q.has('demo')) {
    const i = Math.max(0, Math.min(PRESETS.length - 1, Number(q.get('demo')) || 0));
    openMenu(PRESETS[i]);
  }
  if (q.has('text')) {
    const t = q.get('text');
    dom.cmdInput.value = t;
    loadText(t);
    // ?text=...&run=1 可做一键演示链接
    if (q.has('run')) setTimeout(generate, 260);
  }
  // 调试用：?sheet=1 打开第一道菜的编辑浮层
  if (q.has('sheet') && state.menu.dishes[0]) {
    setTimeout(() => openSheet(state.menu.dishes[0].id), 500);
  }
}

boot();
