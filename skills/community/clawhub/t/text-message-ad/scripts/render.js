// Renders a text-message-ad HTML file to PNG frames using Playwright.
// Usage: node render.js config.json
// Config format: see SKILL.md ("Timeline config").
const { chromium } = require('playwright');
const fs = require('fs');

const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const FPS = cfg.fps || 30;

(async () => {
  const browser = await chromium.launch();
  fs.mkdirSync(cfg.framesDir, { recursive: true });
  const page = await browser.newPage({
    viewport: { width: 444, height: 790 },
    deviceScaleFactor: 2.4324, // stage 444x789.3 -> ~1080x1920
  });
  await page.goto('file://' + cfg.html);
  await page.waitForLoadState('networkidle');

  await page.addStyleTag({ content: `
    body{padding:0 !important;background:#000}
    .stage{width:444px !important;height:789.3px !important;aspect-ratio:auto !important;border-radius:0 !important;box-shadow:none !important}
    .chat{scroll-behavior:auto !important}
    .endcard{transition:none !important}
    .replay{display:none !important}
  `});

  await page.evaluate((cfg) => {
    // kill autoplay timers
    const highest = setTimeout(() => {}, 0);
    for (let i = 0; i <= highest; i++) clearTimeout(i);

    const chat = document.getElementById('chat');
    const rows = [...chat.querySelectorAll('.row')];
    const ts = document.getElementById('ts');
    const endcard = document.getElementById('endcard');

    ts.classList.remove('show');
    endcard.classList.remove('show');
    rows.forEach(r => { r.classList.remove('visible'); r.querySelectorAll('.show').forEach(e => e.classList.remove('show')); });

    window.__seek = (t) => {
      if (t >= cfg.ts) {
        ts.classList.add('show');
        ts.style.animation = 'fadein .5s ease forwards';
        ts.style.animationDelay = `-${Math.min(t - cfg.ts, 500)}ms`;
        ts.style.animationPlayState = 'paused';
      } else { ts.classList.remove('show'); ts.style.animation = ''; }

      rows.forEach((row, i) => {
        const t0 = cfg.shows[i];
        const tHide = cfg.hides[i];
        const gone = tHide !== undefined && t >= tHide;
        if (t >= t0 && !gone) {
          row.classList.add('visible');
          const el = row.querySelector('.bubble, .linkcard, .typing');
          el.classList.add('show');
          const dt = t - t0;
          if (el.classList.contains('typing')) {
            el.style.animation = 'pop .3s cubic-bezier(.34,1.45,.6,1) forwards';
            el.style.animationDelay = `-${Math.min(dt, 300)}ms`;
            el.style.animationPlayState = 'paused';
            [...el.children].forEach((dot, j) => {
              dot.style.animation = 'blink 1.2s infinite ease-in-out';
              dot.style.animationDelay = `-${dt - j * 180}ms`;
              dot.style.animationPlayState = 'paused';
            });
          } else {
            el.style.animation = 'pop .38s cubic-bezier(.34,1.45,.6,1) forwards';
            el.style.animationDelay = `-${Math.min(dt, 380)}ms`;
            el.style.animationPlayState = 'paused';
          }
        } else {
          row.classList.remove('visible');
          const el = row.querySelector('.bubble, .linkcard, .typing');
          el.classList.remove('show');
          el.style.animation = '';
        }
      });
      if (t >= cfg.endcard) {
        endcard.classList.add('show');
        endcard.style.opacity = Math.min((t - cfg.endcard) / 600, 1);
      } else { endcard.classList.remove('show'); endcard.style.opacity = 0; }
      chat.scrollTop = chat.scrollHeight;
    };
  }, cfg);

  const stage = page.locator('.stage');
  const nFrames = Math.round(cfg.durationMs / 1000 * FPS);
  for (let f = 0; f < nFrames; f++) {
    await page.evaluate((t) => window.__seek(t), f * 1000 / FPS);
    await stage.screenshot({ path: `${cfg.framesDir}/${String(f).padStart(4, '0')}.png` });
    if (f % 90 === 0) console.log(f, '/', nFrames);
  }
  console.log('done', nFrames, 'frames ->', cfg.framesDir);
  await browser.close();
})();
