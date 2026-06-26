(function () {
  'use strict';

  if (window.__redlineInjected) return;
  window.__redlineInjected = true;

  const STORAGE_KEY = '__redline_state__';
  const UI_ATTR = 'data-rl-ui';

  const config = window.__RL_CONFIG__ || {};
  const SERVER_URL = config.port
    ? `http://127.0.0.1:${config.port}/feedback`
    : null;
  const INBOX_PATH = config.inbox || '';
  const FILE_NAME =
    config.file ||
    location.pathname
      .split('/')
      .pop()
      .replace(/\.annotated\.html$/, '.html');

  const state = {
    mode: 'idle',
    annotations: [],
    nextId: 1,
    finder: null,
    hoverEl: null,
    activePopover: null,
    submitting: false,
  };

  // ---------- persistence ----------
  function persist() {
    try {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({ annotations: state.annotations, nextId: state.nextId })
      );
    } catch (e) {}
  }

  function restore() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      const parsed = JSON.parse(raw);
      state.annotations = parsed.annotations || [];
      state.nextId = parsed.nextId || state.annotations.length + 1;
    } catch (e) {}
  }

  // ---------- selector generation ----------
  function loadFinder() {
    return new Promise((resolve) => {
      if (window.finder) {
        state.finder = window.finder;
        return resolve();
      }
      const s = document.createElement('script');
      s.src = 'https://unpkg.com/@medv/finder@3.1.0/finder.js';
      s.setAttribute(UI_ATTR, '1');
      s.onload = () => {
        state.finder = window.finder || null;
        resolve();
      };
      s.onerror = () => resolve();
      document.head.appendChild(s);
    });
  }

  function fallbackSelector(el) {
    const parts = [];
    let cur = el;
    while (cur && cur.nodeType === 1 && cur !== document.documentElement) {
      let part = cur.tagName.toLowerCase();
      if (cur.id) {
        parts.unshift(part + '#' + CSS.escape(cur.id));
        break;
      }
      const parent = cur.parentNode;
      if (parent) {
        const sibs = Array.from(parent.children).filter(
          (c) => c.tagName === cur.tagName
        );
        if (sibs.length > 1) {
          part += `:nth-of-type(${sibs.indexOf(cur) + 1})`;
        }
      }
      parts.unshift(part);
      cur = cur.parentNode;
    }
    return parts.join(' > ');
  }

  function getSelector(el) {
    if (state.finder) {
      try {
        return state.finder(el, { className: () => true, tagName: () => true });
      } catch (e) {}
    }
    return fallbackSelector(el);
  }

  // ---------- DOM helpers ----------
  function isOurUI(el) {
    while (el && el.nodeType === 1) {
      if (el.hasAttribute && el.hasAttribute(UI_ATTR)) return true;
      el = el.parentNode;
    }
    return false;
  }

  function el(tag, props = {}, children = []) {
    const node = document.createElement(tag);
    node.setAttribute(UI_ATTR, '1');
    for (const k in props) {
      if (k === 'style') Object.assign(node.style, props[k]);
      else if (k === 'onclick') node.addEventListener('click', props[k]);
      else if (k === 'oninput') node.addEventListener('input', props[k]);
      else node[k] = props[k];
    }
    children.forEach((c) =>
      node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c)
    );
    return node;
  }

  // ---------- toolbar ----------
  let modeBtn, sidebarBox, hoverBox;

  let submitBtn;
  function buildToolbar() {
    const bar = el('div', { className: 'rl-toolbar' }, [
      (modeBtn = el('button', {
        className: 'rl-btn rl-btn-primary',
        onclick: toggleMode,
      }, ['✏️ 标注模式'])),
      (submitBtn = el('button', {
        className: 'rl-btn',
        onclick: submitFeedback,
      }, ['📤 提交反馈'])),
      el('button', { className: 'rl-btn', onclick: clearAll }, ['🗑 清空']),
      el('span', { className: 'rl-count', id: 'rl-count' }, ['0']),
    ]);
    document.body.appendChild(bar);

    hoverBox = el('div', { className: 'rl-hover' });
    document.body.appendChild(hoverBox);

    sidebarBox = el('div', { className: 'rl-sidebar' });
    document.body.appendChild(sidebarBox);
  }

  function toggleMode() {
    state.mode = state.mode === 'idle' ? 'annotate' : 'idle';
    document.body.classList.toggle('rl-active', state.mode === 'annotate');
    modeBtn.textContent =
      state.mode === 'annotate' ? '✋ 退出标注' : '✏️ 标注模式';
    modeBtn.classList.toggle('rl-btn-active', state.mode === 'annotate');
    if (state.mode === 'idle') hideHover();
  }

  // ---------- hover highlight ----------
  function moveHoverTo(target) {
    if (!target) return hideHover();
    const r = target.getBoundingClientRect();
    Object.assign(hoverBox.style, {
      display: 'block',
      left: r.left + window.scrollX + 'px',
      top: r.top + window.scrollY + 'px',
      width: r.width + 'px',
      height: r.height + 'px',
    });
  }
  function hideHover() {
    hoverBox.style.display = 'none';
  }

  // ---------- popover ----------
  function showPopover(target, existing) {
    closePopover();
    const r = target.getBoundingClientRect();
    const ta = el('textarea', {
      className: 'rl-textarea',
      placeholder: '写下针对这个元素的修改意见…',
    });
    ta.value = existing ? existing.comment : '';

    const pop = el('div', { className: 'rl-popover' }, [
      el('div', { className: 'rl-popover-title' }, [
        existing ? `编辑标注 #${existing.id}` : '新增标注',
      ]),
      ta,
      el('div', { className: 'rl-popover-actions' }, [
        el('button', {
          className: 'rl-btn rl-btn-primary',
          onclick: () => {
            const text = ta.value.trim();
            if (!text) return;
            if (existing) {
              existing.comment = text;
            } else {
              addAnnotation(target, text);
            }
            persist();
            renderAll();
            closePopover();
          },
        }, ['保存']),
        el('button', { className: 'rl-btn', onclick: closePopover }, ['取消']),
        existing
          ? el('button', {
              className: 'rl-btn rl-btn-danger',
              onclick: () => {
                state.annotations = state.annotations.filter(
                  (a) => a.id !== existing.id
                );
                persist();
                renderAll();
                closePopover();
              },
            }, ['删除'])
          : el('span', {}),
      ]),
    ]);

    document.body.appendChild(pop);
    state.activePopover = pop;

    const popH = 200;
    const top =
      r.bottom + popH + 12 < window.innerHeight
        ? r.bottom + window.scrollY + 8
        : r.top + window.scrollY - popH - 8;
    Object.assign(pop.style, {
      left: Math.max(8, r.left + window.scrollX) + 'px',
      top: Math.max(8, top) + 'px',
    });
    setTimeout(() => ta.focus(), 0);
  }

  function closePopover() {
    if (state.activePopover) {
      state.activePopover.remove();
      state.activePopover = null;
    }
  }

  // ---------- annotations ----------
  function addAnnotation(target, comment) {
    const r = target.getBoundingClientRect();
    state.annotations.push({
      id: state.nextId++,
      selector: getSelector(target),
      elementHTML: (target.outerHTML || '').slice(0, 1000),
      elementText: (target.textContent || '').trim().slice(0, 100),
      boundingBox: {
        x: Math.round(r.left + window.scrollX),
        y: Math.round(r.top + window.scrollY),
        w: Math.round(r.width),
        h: Math.round(r.height),
      },
      comment,
    });
  }

  function findElementBySelector(sel) {
    try {
      return document.querySelector(sel);
    } catch (e) {
      return null;
    }
  }

  // ---------- rendering ----------
  function renderBadges() {
    document.querySelectorAll('.rl-badge').forEach((n) => n.remove());
    state.annotations.forEach((a) => {
      const target = findElementBySelector(a.selector);
      if (!target) return;
      const r = target.getBoundingClientRect();
      const badge = el('div', {
        className: 'rl-badge',
        title: a.comment,
        onclick: (e) => {
          e.stopPropagation();
          e.preventDefault();
          showPopover(target, a);
        },
      }, [String(a.id)]);
      Object.assign(badge.style, {
        left: r.left + window.scrollX - 12 + 'px',
        top: r.top + window.scrollY - 12 + 'px',
      });
      document.body.appendChild(badge);
    });
  }

  function renderSidebar() {
    sidebarBox.innerHTML = '';
    sidebarBox.appendChild(
      el('div', { className: 'rl-sidebar-title' }, [
        `标注 (${state.annotations.length})`,
      ])
    );
    if (state.annotations.length === 0) {
      sidebarBox.appendChild(
        el('div', { className: 'rl-sidebar-empty' }, [
          '点"标注模式"后，点页面元素开始批注',
        ])
      );
      return;
    }
    state.annotations.forEach((a) => {
      const item = el('div', {
        className: 'rl-sidebar-item',
        onclick: () => {
          const t = findElementBySelector(a.selector);
          if (t) {
            t.scrollIntoView({ behavior: 'smooth', block: 'center' });
            setTimeout(() => showPopover(t, a), 350);
          }
        },
      }, [
        el('div', { className: 'rl-sidebar-id' }, ['#' + a.id]),
        el('div', { className: 'rl-sidebar-text' }, [a.elementText || a.selector]),
        el('div', { className: 'rl-sidebar-comment' }, [a.comment]),
      ]);
      sidebarBox.appendChild(item);
    });
  }

  function renderCount() {
    const c = document.getElementById('rl-count');
    if (c) c.textContent = String(state.annotations.length);
  }

  function renderAll() {
    renderBadges();
    renderSidebar();
    renderCount();
  }

  // ---------- submit / clipboard fallback ----------
  function buildPayload() {
    return {
      file: FILE_NAME,
      timestamp: new Date().toISOString(),
      annotations: state.annotations,
    };
  }

  async function copyToClipboardFallback(text) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (e) {}
    try {
      const ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      const ok = document.execCommand('copy');
      ta.remove();
      return ok;
    } catch (e) {
      return false;
    }
  }

  async function submitFeedback() {
    if (state.annotations.length === 0) {
      toast('还没有任何标注');
      return;
    }
    if (state.submitting) return;

    const payload = buildPayload();

    if (!SERVER_URL || !INBOX_PATH) {
      const copied = await copyToClipboardFallback(
        JSON.stringify(payload, null, 2)
      );
      toast(
        copied
          ? '⚠ 未配置 server，已 fallback 到剪贴板'
          : '⚠ 未配置 server 且剪贴板不可用'
      );
      return;
    }

    state.submitting = true;
    submitBtn.classList.add('rl-btn-loading');
    submitBtn.textContent = '提交中…';

    try {
      const res = await fetch(SERVER_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ inbox: INBOX_PATH, payload }),
      });
      const data = await res.json().catch(() => ({}));
      if (res.ok && data.ok) {
        submitBtn.textContent = '✓ 已提交';
        submitBtn.classList.remove('rl-btn-loading');
        submitBtn.classList.add('rl-btn-success');
        toast(`已提交 ${state.annotations.length} 条到 Claude Code，回去说一句话即可`);
        setTimeout(() => {
          submitBtn.textContent = '📤 提交反馈';
          submitBtn.classList.remove('rl-btn-success');
        }, 3000);
      } else {
        throw new Error(data.error || `HTTP ${res.status}`);
      }
    } catch (e) {
      const copied = await copyToClipboardFallback(
        JSON.stringify(payload, null, 2)
      );
      toast(
        copied
          ? `提交失败 (${e.message})，已 fallback 到剪贴板`
          : `提交失败: ${e.message}`
      );
      submitBtn.textContent = '📤 提交反馈';
      submitBtn.classList.remove('rl-btn-loading');
    } finally {
      state.submitting = false;
    }
  }

  function clearAll() {
    if (state.annotations.length === 0) return;
    if (!confirm('清空所有标注？此操作不可撤销。')) return;
    state.annotations = [];
    state.nextId = 1;
    persist();
    renderAll();
  }

  // ---------- toast ----------
  let toastTimer = null;
  function toast(msg) {
    let box = document.querySelector('.rl-toast');
    if (!box) {
      box = el('div', { className: 'rl-toast' });
      document.body.appendChild(box);
    }
    box.textContent = msg;
    box.classList.add('rl-toast-show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => box.classList.remove('rl-toast-show'), 2400);
  }

  // ---------- event handlers ----------
  function onMouseOver(e) {
    if (state.mode !== 'annotate') return;
    if (isOurUI(e.target)) return hideHover();
    state.hoverEl = e.target;
    moveHoverTo(e.target);
  }

  function onClick(e) {
    if (state.mode !== 'annotate') return;
    if (isOurUI(e.target)) return;
    e.preventDefault();
    e.stopPropagation();
    showPopover(e.target);
  }

  function onResize() {
    renderBadges();
    if (state.hoverEl && state.mode === 'annotate') moveHoverTo(state.hoverEl);
  }

  // ---------- init ----------
  function init() {
    restore();
    buildToolbar();
    renderAll();
    document.addEventListener('mouseover', onMouseOver, true);
    document.addEventListener('click', onClick, true);
    window.addEventListener('scroll', renderBadges, { passive: true });
    window.addEventListener('resize', onResize);
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        if (state.activePopover) closePopover();
        else if (state.mode === 'annotate') toggleMode();
      }
    });
  }

  loadFinder().then(() => {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
    } else {
      init();
    }
  });
})();
