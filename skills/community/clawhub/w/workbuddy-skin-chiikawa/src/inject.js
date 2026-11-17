// inject.js — 注入 payload：挂载样式 + 顶部日历条
// 由 apply.mjs 把 CSS 内联到占位符后 evaluate
(() => {
  if (window.__wbsMounted) return 'already mounted';
  window.__wbsMounted = true;

  // ── 1. 样式 ──
  const style = document.createElement('style');
  style.id = 'wbs-style';
  style.textContent = /*__CSS__*/'';/*__END__*/
  document.head.appendChild(style);

  // ── 2. 外观跟随 App 设置（不强制翻转；CSS 里 light/dark 两套变量自动适配） ──

  // ── 2.5 背景模式：video 时挂 <video> 层垫在 #root 下（静态图仍留 body 背景做垫底/海报） ──
  const BG_MODE = /*__MODE__*/"static";/*__END__*/
  if (BG_MODE === 'video') {
    const v = document.createElement('video');
    v.id = 'wbs-bg-video';
    v.src = /*__VIDEO_URL__*/'';/*__END__*/
    v.autoplay = v.muted = v.loop = true;
    v.playsInline = true;
    v.setAttribute('disablepictureinpicture', '');
    Object.assign(v.style, {
      position: 'fixed', inset: '0', width: '100%', height: '100%',
      objectFit: 'cover', zIndex: '0', pointerEvents: 'none',
    });
    document.body.prepend(v);
    document.body.classList.add('wbs-video');
    v.play().catch(() => {});
    // 专注模式：上次选择暂停则保持暂停
    if (localStorage.getItem('wbs-video-paused') === '1') v.pause();
  }

  // ── 3. 顶部日历条（今天居中，滚动窗） ──
  const DOW = ['日', '一', '二', '三', '四', '五', '六'];
  let focusOffset = 0; // 焦点日相对今天的偏移，默认今天居中
  let highlightOffset = null; // 任务高亮的日期偏移，null = 不高亮

  function sameDay(a, b) {
    return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
  }

  // 从任务条目文本解析日期（“N分钟/小时/天/周前”“昨天”“M月D日”）
  function itemDate(item) {
    const t = item.textContent;
    const now = new Date(); now.setHours(0, 0, 0, 0);
    let m;
    if (/刚刚|分钟前/.test(t)) return now;
    if ((m = t.match(/(\d+)\s*小时前/))) {
      const d = new Date(); d.setHours(d.getHours() - Number(m[1]), 0, 0, 0);
      d.setHours(0, 0, 0, 0);
      return d;
    }
    if (/昨天/.test(t)) { const d = new Date(now); d.setDate(d.getDate() - 1); return d; }
    if ((m = t.match(/(\d+)\s*天前/))) { const d = new Date(now); d.setDate(d.getDate() - Number(m[1])); return d; }
    if ((m = t.match(/(\d+)\s*周前/))) { const d = new Date(now); d.setDate(d.getDate() - Number(m[1]) * 7); return d; }
    if ((m = t.match(/(\d{1,2})月(\d{1,2})日/))) {
      const d = new Date(now); d.setMonth(Number(m[1]) - 1, Number(m[2])); return d;
    }
    return null;
  }

  function applyTaskHighlight() {
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const target = highlightOffset === null ? null
      : new Date(today.getTime() + highlightOffset * 86400000);
    for (const it of document.querySelectorAll('.conversation-list-content .conversation-item')) {
      const d = itemDate(it);
      const hit = target && d && sameDay(d, target);
      it.classList.toggle('wbs-dayhit', !!hit);
      it.classList.toggle('wbs-daydim', !!(target && !hit));
    }
  }

  function render(bar) {
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const focus = new Date(today); focus.setDate(today.getDate() + focusOffset);
    const days = [];
    for (let i = -3; i <= 3; i++) {
      const d = new Date(focus); d.setDate(focus.getDate() + i);
      days.push(d);
    }
    bar.innerHTML = `
      <button class="wbs-cal-nav" data-nav="-1">‹</button>
      <span class="wbs-cal-month" title="回到今天">${focus.getMonth() + 1}月</span>
      <div class="wbs-cal-days">
        ${days.map((d, i) => {
          const isToday = d.getTime() === today.getTime();
          const isFocus = d.getTime() === focus.getTime();
          return `<div class="wbs-cal-day${isToday ? ' today' : ''}${isFocus && !isToday ? ' focus' : ''}" data-offset="${focusOffset + i - 3}">
            <span class="dow">${DOW[d.getDay()]}</span>
            <span class="dnum">${d.getDate()}</span>
          </div>`;
        }).join('')}
      </div>
      <button class="wbs-cal-nav" data-nav="1">›</button>
      ${BG_MODE === 'video' ? `<button class="wbs-cal-nav wbs-video-toggle" title="专注模式：暂停/播放背景动画">${(document.getElementById('wbs-bg-video') || {}).paused ? '▶' : '⏸'}</button>` : ''}`;
    bar.querySelectorAll('[data-nav]').forEach(b =>
      b.addEventListener('click', () => { focusOffset += Number(b.dataset.nav); render(bar); }));
    const vt = bar.querySelector('.wbs-video-toggle');
    if (vt) vt.addEventListener('click', () => {
      const v = document.getElementById('wbs-bg-video');
      if (!v) return;
      if (v.paused) v.play().catch(() => {}); else v.pause();
      localStorage.setItem('wbs-video-paused', v.paused ? '1' : '0');
      vt.textContent = v.paused ? '▶' : '⏸';
    });
    bar.querySelectorAll('.wbs-cal-day').forEach(d =>
      d.addEventListener('click', () => {
        focusOffset = Number(d.dataset.offset);
        // 再点同一天取消高亮，否则高亮当天任务
        highlightOffset = highlightOffset === focusOffset ? null : focusOffset;
        render(bar);
        applyTaskHighlight();
      }));
    bar.querySelector('.wbs-cal-month').addEventListener('click', () => {
      focusOffset = 0;
      highlightOffset = null;
      render(bar);
      applyTaskHighlight();
    });
  }

  // ── 4. 磁贴纯图标化：文字藏起后，把名称写到 title 做悬停提示 ──
  function iconifyTiles() {
    for (const btn of document.querySelectorAll('.conversation-list-tab-button')) {
      if (!btn.title) {
        const label = [...btn.querySelectorAll('span')].map(s => s.textContent.trim()).filter(Boolean).join(' · ');
        if (label) btn.title = label;
      }
    }
    const row = document.querySelector('.conversation-list-tab-row');
    if (!row) return;
    const btn = row.querySelector('.conversation-list-tab-button');
    const actions = row.querySelector('.conversation-list-tab-actions');
    if (btn && actions && actions.parentElement !== btn) btn.appendChild(actions);
  }

  // ── 5. 敲木鱼：钉在输入框右边，对话视图自动跟随 ──
  let muyuCount = Number(localStorage.getItem('wbs-muyu-count') || 0);

  // 真实木鱼采样（用户版，apply 时内联 base64 WAV）
  // 页面 CSP 禁止 <audio> 加载 data: URL，改走 WebAudio decodeAudioData
  const MUYU_B64 = /*__MUYU_AUDIO__*/"";/*__END__*/
  let muyuBuf = null; // null=未解码 false=解码失败 AudioBuffer=就绪

  function audioCtx() {
    const Ctx = window.AudioContext || window.webkitAudioContext;
    return audioCtx.ctx || (audioCtx.ctx = new Ctx());
  }
  async function ensureMuyu() {
    if (muyuBuf !== null) return muyuBuf;
    try {
      const bin = atob(MUYU_B64);
      const arr = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
      muyuBuf = await audioCtx().decodeAudioData(arr.buffer);
    } catch { muyuBuf = false; }
    return muyuBuf;
  }
  ensureMuyu(); // 提前解码，第一次敲击就能用

  function knockSound() {
    const ctx = audioCtx();
    if (ctx.state === 'suspended') ctx.resume();
    ensureMuyu().then(buf => {
      if (!buf) return synthKnock();
      const src = ctx.createBufferSource();
      src.buffer = buf;
      src.connect(ctx.destination);
      src.start();
    });
  }
  function synthKnock() {
    try {
      const ctx = audioCtx();
      const t = ctx.currentTime;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(720, t);
      osc.frequency.exponentialRampToValueAtTime(180, t + 0.07);
      gain.gain.setValueAtTime(0.5, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.12);
      osc.connect(gain).connect(ctx.destination);
      osc.start(t); osc.stop(t + 0.13);
    } catch {}
  }

  function knock(w) {
    muyuCount++;
    localStorage.setItem('wbs-muyu-count', muyuCount);
    w.querySelector('.wbs-muyu-count').textContent = muyuCount;
    w.classList.remove('knocked');
    void w.offsetWidth; // 重触动画
    w.classList.add('knocked');
    setTimeout(knockSound, 110); // 槌子落下瞬间才出声
    const f = document.createElement('div');
    f.className = 'wbs-muyu-float';
    f.textContent = '功德 +1';
    w.appendChild(f);
    setTimeout(() => f.remove(), 900);
  }

  function mountMuyu() {
    let w = document.getElementById('wbs-muyu');
    if (!w) {
      w = document.createElement('div');
      w.id = 'wbs-muyu';
      w.innerHTML = `
        <div class="wbs-muyu-fish">
          <div class="wbs-muyu-ripple"></div>
          <svg viewBox="0 0 64 48" width="40" height="30">
            <ellipse cx="32" cy="26" rx="28" ry="19" fill="#8a5a2b"/>
            <ellipse cx="32" cy="22" rx="28" ry="17" fill="#a8713a"/>
            <path d="M14 24 Q32 34 50 24" stroke="#5d3a17" stroke-width="2.5" fill="none"/>
            <circle cx="50" cy="16" r="3.5" fill="#5d3a17"/>
          </svg>
          <div class="wbs-muyu-mallet">
            <svg viewBox="0 0 24 44" width="18" height="33">
              <rect x="10.5" y="12" width="3" height="26" rx="1.5" fill="#7a4e22"/>
              <circle cx="12" cy="9" r="8" fill="#a8713a"/>
              <circle cx="12" cy="9" r="8" fill="url(#wbs-mg)" opacity="0.35"/>
              <defs><radialGradient id="wbs-mg" cx="0.35" cy="0.3"><stop offset="0%" stop-color="#fff"/><stop offset="100%" stop-color="transparent"/></radialGradient></defs>
            </svg>
          </div>
        </div>
        <div class="wbs-muyu-count">${muyuCount}</div>`;
      w.title = '敲木鱼 · 功德+1';
      w.addEventListener('click', () => knock(w));
      document.body.appendChild(w);
    }
    // 跟随输入框：取可见 editable，向上找最外层 composer 容器，钉在其右侧
    const eds = [...document.querySelectorAll('[class*="_editable"]')]
      .filter(e => {
        const r = e.getBoundingClientRect();
        return r.width > 100 && r.height > 0 && e.offsetParent !== null;
      });
    const ed = eds[eds.length - 1];
    if (ed) {
      // 取最内层匹内容器（= 玻璃罩本身），中心才和视觉一致
      let anchor = ed, el = ed;
      while (el) {
        if (el.className && /composer|input-area-container|_container/.test(el.className.toString())) { anchor = el; break; }
        el = el.parentElement;
      }
      const r = anchor.getBoundingClientRect();
      const FISH_W = 52, MARGIN = 8;
      // 右侧边栏（detail/inspiration 等 *-panel）打开时隐藏
      const panelOpen = [...document.querySelectorAll('[data-view-id$="-panel"]')]
        .some(p => p.getBoundingClientRect().width > 0);
      const gap = window.innerWidth - r.right; // 输入框右缘到窗口右缘的间隙
      if (!panelOpen && gap >= FISH_W + MARGIN * 2) {
        // 纵轴：输入框垂直居中；横轴：间隙内居中
        w.style.display = 'flex';
        w.style.left = (r.right + (gap - FISH_W) / 2) + 'px';
        w.style.top = (r.top + r.height / 2 - FISH_W / 2) + 'px'; // 鱼身中心对准输入框中心
      } else {
        w.style.display = 'none'; // 间隙不够就消失
      }
    } else {
      w.style.display = 'none';
    }
  }

  function mount() {
    iconifyTiles();
    mountMuyu();
    applyTaskHighlight(); // DOM 变化后重挂高亮
    // 侧栏收起检测：顶栏给红绿灯让位
    const sb = document.querySelector('[data-view-id=sidebar]');
    const collapsed = !sb || sb.getBoundingClientRect().width < 40;
    const topbar = document.getElementById('wbs-topbar');
    if (topbar) topbar.classList.toggle('wbs-pad-left', collapsed);
    const host = document.querySelector('.teams-content-wrapper');
    if (!host || document.getElementById('wbs-topbar')) return;
    host.style.display = 'flex';
    host.style.flexDirection = 'column';
    const bar = document.createElement('div');
    bar.id = 'wbs-topbar';
    render(bar);
    host.prepend(bar);
    // 主内容区占满剩余高度
    const main = host.querySelector('.teams-main-content');
    if (main) { main.style.flex = '1'; main.style.minHeight = '0'; }
  }

  mount();
  new MutationObserver(mount).observe(document.getElementById('root'), {
    childList: true, subtree: true, attributes: true, attributeFilter: ['class', 'style'],
  });
  return 'wbs mounted (follows app theme)';
})();
