// Screencast recording entry point.
// Outputs: raw.webm (cursorless playwright recording) + events.json (subtitles/moves/clicks).
// postprocess.js then reads both to produce final.mp4 with overlaid cursor + ripple + burned subtitles.
//
// HOW TO AUTHOR YOUR DEMO:
//   1. Set BASE / VIEWPORT below (or use env vars: SCREENCAST_BASE, SCREENCAST_VIEWPORT_W/H)
//   2. Replace the body inside the `try { ... }` block (search for "STAGE FLOW") with your
//      own stage sequence using the helpers (sub / click / scroll / hold / tryStep).
//   3. Run `npm run ship` — the rest of the pipeline (postprocess + deploy + review + clean)
//      is wired together for you.
//
// HELPERS available inside your flow:
//   sub(label)               — subtitle event + auto-hold (CJK-aware)
//   click(locator, label)    — cursor moves, dwells, clicks, dwells (full ceremony)
//   scroll(deltaY, ticks=1)  — wheel scroll on main content area
//   hold(ms=400)             — explicit pause
//   tryStep(name, fn)        — non-fatal stage; if fn throws, log and continue
//   page                     — the underlying Playwright Page (escape hatch)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// ===== CONFIG (replace per project) =====
const BASE = process.env.SCREENCAST_BASE || 'http://localhost:3000';
const VIEWPORT = {
  width: parseInt(process.env.SCREENCAST_VIEWPORT_W || '1440', 10),
  height: parseInt(process.env.SCREENCAST_VIEWPORT_H || '900', 10),
};
const STORAGE_STATE = path.join(__dirname, 'storageState.json');

// Persistent mask regions — blurred for the entire video.
// Use `selector` for elements you can target (resolved once after first navigation),
// or `box` for fixed coordinates (e.g. footer version, sidebar corners).
// IMPORTANT: selector-based masks assume the element is `position: fixed` or `sticky`.
// If the element scrolls with the page, the mask stays put and may drift off the target —
// use a `box` covering the worst-case viewport position instead.
const PERSISTENT_MASKS = [
  // { selector: '.user-badge',  label: 'username' },
  // { selector: 'header .logo', label: 'logo' },
  // { box: { x: 0, y: 820, w: 220, h: 80 }, label: 'sidebar-bottom' },
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const videoDir = path.join(__dirname, 'videos');
  if (!fs.existsSync(videoDir)) fs.mkdirSync(videoDir);
  fs.readdirSync(videoDir).forEach((f) => fs.unlinkSync(path.join(videoDir, f)));

  const contextOpts = {
    viewport: VIEWPORT,
    recordVideo: { dir: videoDir, size: VIEWPORT },
    ignoreHTTPSErrors: true,
  };
  if (fs.existsSync(STORAGE_STATE)) contextOpts.storageState = STORAGE_STATE;
  const context = await browser.newContext(contextOpts);

  const events = [];
  const tStart = Date.now();
  const t = () => +((Date.now() - tStart) / 1000).toFixed(2);
  const log = (msg) => console.log(`[${t().toFixed(2)}s] ${msg}`);

  const page = await context.newPage();

  // ---- helpers ----
  // Subtitle hold time scales with character count. CJK chars get more time per char.
  const subtitleHoldMs = (label) => {
    let ms = 700;
    for (const c of [...label]) {
      if (/[一-鿿㐀-䶿]/.test(c)) ms += 130; // CJK Unified
      else if (/\s/.test(c)) ms += 30;
      else ms += 55;
    }
    return Math.min(3500, Math.max(1100, ms));
  };
  const sub = async (label) => {
    events.push({ t: t(), kind: 'subtitle', label });
    log(`SUB (${subtitleHoldMs(label)}ms): ${label}`);
    await page.waitForTimeout(subtitleHoldMs(label));
  };
  const hold = (ms = 400) => page.waitForTimeout(ms);

  // Wheel scroll. Mouse parks in main content area first so the wheel scrolls main, not sidebar.
  const scroll = async (deltaY, ticks = 1) => {
    await page.mouse.move(Math.round(VIEWPORT.width / 2), Math.round(VIEWPORT.height / 2));
    for (let i = 0; i < ticks; i++) {
      await page.mouse.wheel(0, deltaY);
      await page.waitForTimeout(280);
    }
  };

  // boundingBox center, AFTER scrolling target into view (so cursor + ripple stay inside frame).
  const clickBox = async (locator, label) => {
    await locator.scrollIntoViewIfNeeded();
    await page.waitForTimeout(150); // let scroll settle
    const box = await locator.boundingBox();
    if (!box) throw new Error(`bounding box missing: ${label}`);
    return { x: Math.round(box.x + box.width / 2), y: Math.round(box.y + box.height / 2) };
  };

  // Click ceremony: push move → dwell → push click → click → dwell.
  // Dwell times are tuned so the synthetic cursor visibly arrives, the ripple flashes,
  // and the UI reaction is on-screen before the next action.
  const PAUSE_BEFORE_CLICK = 700;
  const PAUSE_AFTER_CLICK = 500;
  const click = async (locator, label) => {
    const c = await clickBox(locator, label);
    events.push({ t: t(), kind: 'move', x: c.x, y: c.y });
    log(`MOVE  (${c.x},${c.y}) — settling`);
    await page.waitForTimeout(PAUSE_BEFORE_CLICK);
    events.push({ t: t(), kind: 'click', x: c.x, y: c.y, label });
    log(`CLICK (${c.x},${c.y}) — ${label}`);
    await locator.click();
    await page.waitForTimeout(PAUSE_AFTER_CLICK);
  };

  // Non-fatal stage wrapper. If fn throws, log and continue — useful for optional UI surfaces
  // that may not exist on every account / permission tier.
  const tryStep = async (name, fn) => {
    try { await fn(); log(`✓ ${name}`); }
    catch (e) { log(`✗ ${name} — skipped: ${e.message.slice(0, 120)}`); }
  };

  // Resolve PERSISTENT_MASKS into mask_persistent events. Called automatically right after
  // first navigation (below). Selector-based masks query boundingBox() once; box-based masks
  // are written through as-is. Each mask becomes one event consumed by postprocess.js.
  const resolveMasks = async () => {
    for (const m of PERSISTENT_MASKS) {
      let box = m.box;
      if (m.selector) {
        const loc = page.locator(m.selector).first();
        try {
          await loc.waitFor({ state: 'visible', timeout: 5000 });
          const bb = await loc.boundingBox();
          if (!bb) { log(`MASK ⚠ "${m.label}" — selector matched but no bbox; skipping`); continue; }
          const pos = await loc.evaluate((el) => getComputedStyle(el).position).catch(() => 'unknown');
          if (pos !== 'fixed' && pos !== 'sticky') {
            log(`MASK ⚠ "${m.label}" — position=${pos}; may drift on scroll. Use { box } to lock coordinates.`);
          }
          box = { x: Math.round(bb.x), y: Math.round(bb.y), w: Math.round(bb.width), h: Math.round(bb.height) };
        } catch (e) {
          log(`MASK ✗ "${m.label}" — selector "${m.selector}" not resolvable: ${e.message.slice(0, 80)}`);
          continue;
        }
      }
      if (!box || box.w <= 0 || box.h <= 0) {
        log(`MASK ✗ "${m.label}" — invalid box`);
        continue;
      }
      events.push({ t: 0, kind: 'mask_persistent', label: m.label, x: box.x, y: box.y, w: box.w, h: box.h });
      log(`MASK ✓ "${m.label}" ${box.x},${box.y} ${box.w}x${box.h}`);
    }
  };

  try {
    // First navigation + mask resolution. record.js handles this for you so PERSISTENT_MASKS
    // can resolve their selectors against a logged-in DOM. After this block, the page is on
    // BASE and ready — your STAGE FLOW does NOT need to call page.goto(BASE) again.
    await page.goto(`${BASE}/`, { waitUntil: 'domcontentloaded' });
    await page.locator('body').waitFor({ state: 'visible', timeout: 10000 });
    await page.waitForTimeout(800); // let SPA settle before resolving mask selectors
    await resolveMasks();

    // ============================================================
    // ===== STAGE FLOW — replace this block with your demo =======
    // ============================================================
    // Page is already on BASE (record.js did the first navigation above) — start clicking.
    //
    // Example skeleton (delete and replace):
    //
    //   await page.locator('h1').first().waitFor({ timeout: 8000 });
    //   await sub('Welcome — what this demo shows');
    //
    //   const startBtn = page.locator('button').filter({ hasText: /Get started/ }).first();
    //   await click(startBtn, '点击「Get started」');
    //
    //   await sub('Now we navigate the main feature');
    //   await scroll(400, 2);
    //   await sub('Bottom of the page reveals X');
    //
    //   await tryStep('Optional: open settings', async () => {
    //     const settings = page.locator('button').filter({ hasText: /Settings/ }).first();
    //     await click(settings, '打开设置');
    //     await sub('设置页 — basic info');
    //     await hold(1500);
    //   });
    //
    //   await sub('Demo end');
    //
    // See examples/walkthrough-flow.md for a fuller pattern guide.
    throw new Error('No stage flow defined yet — replace the block in record.js (search "STAGE FLOW")');

  } finally {
    await context.close();
    await browser.close();
  }

  const videos = fs.readdirSync(videoDir).filter((f) => f.endsWith('.webm'));
  if (videos.length) {
    const src = path.join(videoDir, videos[0]);
    const dst = path.join(__dirname, 'raw.webm');
    fs.copyFileSync(src, dst);
    console.log('VIDEO:', dst, fs.statSync(dst).size, 'bytes');
  }
  fs.writeFileSync(path.join(__dirname, 'events.json'), JSON.stringify(events, null, 2));
  console.log('EVENTS:', events.length);
  console.log('DONE');
})();
