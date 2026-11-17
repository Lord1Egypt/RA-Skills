// bg-live.js — 交互壁纸：流场粒子（鼠标搅动漩涡，随 light/dark 换色）
// 预览页通过 <script src> 加载；apply.mjs 把它内联进 inject.js
// 暴露 window.__wbsLiveBgStart(canvas) → { start, stop, isRunning }
window.__wbsLiveBgStart = function (canvas) {
  const ctx = canvas.getContext('2d');
  let w = 0, h = 0;
  const particles = [];
  const mouse = { x: -1e4, y: -1e4 };
  let running = false, raf = 0, t = 0, wasRunningBeforeHide = false;

  const isDark = () => document.body.classList.contains('dark');
  const palette = () => isDark()
    ? { bg: '8, 10, 24', fade: 0.06, lightness: 62, alpha: 0.5 }
    : { bg: '244, 246, 252', fade: 0.09, lightness: 46, alpha: 0.4 };
  const HUES = [190, 215, 260, 320, 165];

  function paintBase(full) {
    const p = palette();
    ctx.fillStyle = full ? `rgb(${p.bg})` : `rgba(${p.bg}, ${p.fade})`;
    ctx.fillRect(0, 0, w, h);
  }

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = canvas.clientWidth; h = canvas.clientHeight;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    paintBase(true);
  }

  // 伪噪声流场：几个正弦叠加，便宜又顺滑
  function field(x, y) {
    const s = 0.0022;
    return Math.sin(x * s * 1.7 + t * 0.35)
         + Math.cos(y * s * 1.3 - t * 0.28)
         + Math.sin((x + y) * s * 0.7 + t * 0.18);
  }

  class Particle {
    constructor() { this.reset(true); }
    reset(init) {
      this.x = Math.random() * w; this.y = Math.random() * h;
      this.px = this.x; this.py = this.y;
      this.vx = 0; this.vy = 0;
      this.life = init ? Math.random() * 200 : 0;
      this.maxLife = 220 + Math.random() * 320;
      this.hue = HUES[(Math.random() * HUES.length) | 0] + Math.random() * 20 - 10;
      this.speed = 0.6 + Math.random() * 1.1;
      this.size = Math.random() < 0.12 ? 1.8 : 1;
    }
    step() {
      const a = field(this.x, this.y) * Math.PI;
      this.vx += Math.cos(a) * 0.06 * this.speed;
      this.vy += Math.sin(a) * 0.06 * this.speed;
      // 鼠标漩涡：切向力为主 + 轻微外推
      const dx = this.x - mouse.x, dy = this.y - mouse.y;
      const d2 = dx * dx + dy * dy;
      if (d2 < 32400) {
        const d = Math.sqrt(d2) || 1;
        const f = (1 - d / 180) * 0.9;
        this.vx += (-dy / d) * f + (dx / d) * f * 0.25;
        this.vy += (dx / d) * f + (dy / d) * f * 0.25;
      }
      this.vx *= 0.96; this.vy *= 0.96;
      this.px = this.x; this.py = this.y;
      this.x += this.vx; this.y += this.vy;
      this.life++;
      if (this.life > this.maxLife || this.x < -20 || this.x > w + 20 || this.y < -20 || this.y > h + 20) this.reset(false);
    }
    draw() {
      const p = palette();
      ctx.strokeStyle = `hsla(${this.hue}, 85%, ${p.lightness}%, ${p.alpha})`;
      ctx.lineWidth = this.size;
      ctx.beginPath();
      ctx.moveTo(this.px, this.py);
      ctx.lineTo(this.x, this.y);
      ctx.stroke();
    }
  }

  function frame() {
    if (!running) return;
    t += 0.016;
    paintBase(false); // 低 alpha 覆盖 → 拖尾
    for (const p of particles) { p.step(); p.draw(); }
    raf = requestAnimationFrame(frame);
  }

  // ── 初始化 ──
  resize();
  const N = Math.min(420, Math.max(160, Math.floor((w * h) / 3800)));
  for (let i = 0; i < N; i++) particles.push(new Particle());
  window.addEventListener('resize', resize);
  window.addEventListener('pointermove', e => { mouse.x = e.clientX; mouse.y = e.clientY; });
  window.addEventListener('pointerleave', () => { mouse.x = -1e4; mouse.y = -1e4; });
  // 主题切换：立刻用新底色重铺，否则旧色拖尾残留
  new MutationObserver(() => paintBase(true)).observe(document.body, { attributes: true, attributeFilter: ['class'] });
  // 窗口隐藏时停帧省电
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) { wasRunningBeforeHide = running; api.stop(); }
    else if (wasRunningBeforeHide) api.start();
  });

  const api = {
    start() { if (!running) { running = true; frame(); } },
    stop() { running = false; cancelAnimationFrame(raf); },
    isRunning() { return running; },
  };
  api.start();
  return api;
};
