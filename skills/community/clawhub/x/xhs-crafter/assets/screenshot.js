const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

// ── Config ──
const PROJECT = path.resolve(process.argv[2] || '.');
const OUT = path.join(PROJECT, 'output');
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

const HTML_FILE = path.join(PROJECT, 'index.html');
if (!fs.existsSync(HTML_FILE)) {
  console.error(`index.html not found in ${PROJECT}`);
  process.exit(1);
}

const html = fs.readFileSync(HTML_FILE, 'utf-8');
const pageIds = [...html.matchAll(/id="(xhs-\d+)"/g)].map(m => m[1]);
if (pageIds.length === 0) {
  console.error('No xhs-* IDs found in HTML');
  process.exit(1);
}

const TARGETS = pageIds.map((id, i) => {
  const num = String(i + 1).padStart(1, '0');
  return [`#${id}`, `p${num}.png`];
});

const EXPECTED_TITLE = (html.match(/<title>([^<]+)<\/title>/) || [])[1] || '';

// Find Chrome
const CHROME_PATHS = [
  process.env.CHROME_PATH,
  process.env.LOCALAPPDATA && path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'chromium-1208', 'chrome-win64', 'chrome.exe'),
  process.env.PROGRAMFILES && path.join(process.env.PROGRAMFILES, 'Google', 'Chrome', 'Application', 'chrome.exe'),
].filter(Boolean);

if (process.env.LOCALAPPDATA) {
  try {
    const pwDir = path.join(process.env.LOCALAPPDATA, 'ms-playwright');
    if (fs.existsSync(pwDir)) {
      const dirs = fs.readdirSync(pwDir).filter(d => d.startsWith('chromium-'));
      for (const d of dirs) {
        CHROME_PATHS.push(path.join(pwDir, d, 'chrome-win64', 'chrome.exe'));
      }
    }
  } catch {}
}

const chromePath = CHROME_PATHS.find(p => {
  try { fs.accessSync(p); return true; } catch { return false; }
});

if (!chromePath) {
  console.error('Chrome not found. Set CHROME_PATH env var.');
  process.exit(1);
}
console.log(`Chrome: ${chromePath}`);

const SIZE_WARN_COVER = 500;
const SIZE_WARN_TEXT  = 200;

// ── Find a free port ──
function findFreePort() {
  return new Promise((resolve, reject) => {
    const net = require('net');
    const server = net.createServer();
    server.listen(0, '127.0.0.1', () => {
      const port = server.address().port;
      server.close(() => resolve(port));
    });
    server.on('error', reject);
  });
}

// ── Start local http.server in project directory ──
function startServer(projectDir, port) {
  return new Promise((resolve, reject) => {
    const proc = spawn('python', ['-m', 'http.server', String(port)], {
      cwd: projectDir,
      stdio: ['pipe', 'pipe', 'pipe'],
    });

    let resolved = false;

    const onReady = () => {
      if (!resolved) {
        resolved = true;
        console.log(`http.server started on port ${port} (cwd: ${projectDir})`);
        resolve({ proc, port });
      }
    };

    proc.stdout.on('data', onReady);
    proc.stderr.on('data', onReady);

    setTimeout(() => {
      if (!resolved) {
        onReady();
      }
    }, 1500);

    proc.on('error', (err) => {
      if (!resolved) reject(err);
    });
  });
}

// ── Main ──
(async () => {
  let server = null;
  try {
    server = await startServer(PROJECT, await findFreePort());
    const { proc: serverProc, port } = server;

    const browser = await puppeteer.launch({
      executablePath: chromePath,
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-cache',
        '--disable-application-cache',
        '--disable-offline-load-stale-cache',
      ],
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1080, height: 1440, deviceScaleFactor: 2 });

    await page.setCacheEnabled(false);

    const cacheBust = Date.now();
    const url = `http://localhost:${port}/index.html?t=${cacheBust}`;
    console.log(`Loading ${url} ...`);
    await page.goto(url, { waitUntil: 'networkidle0' });
    await page.evaluate(() => document.fonts.ready);

    // Verify page title matches
    const actualTitle = await page.title();
    if (EXPECTED_TITLE && actualTitle !== EXPECTED_TITLE) {
      console.error(`\n🚨 TITLE MISMATCH!`);
      console.error(`  Expected: ${EXPECTED_TITLE}`);
      console.error(`  Got:      ${actualTitle}`);
      console.error(`  The http.server may be serving the wrong project!`);
      console.error(`  Aborting screenshots.`);
      await browser.close();
      serverProc.kill();
      process.exit(1);
    }
    console.log(`Title verified: "${actualTitle}"`);

    console.log('Waiting 6s for images...');
    await new Promise(r => setTimeout(r, 6000));

    // Verify elements exist
    const found = await page.evaluate((ids) => {
      return ids.map(id => `${id}: ${!!document.getElementById(id)}`).join(', ');
    }, pageIds);
    console.log('Elements:', found);

    // Verify cover/finale images are loaded (not broken)
    const imgCheck = await page.evaluate(() => {
      const imgs = document.querySelectorAll('.hero-bleed img');
      return Array.from(imgs).map((img, i) => ({
        index: i,
        src: img.src,
        naturalWidth: img.naturalWidth,
        naturalHeight: img.naturalHeight,
        complete: img.complete,
      }));
    });
    if (imgCheck.length > 0) {
      for (const ic of imgCheck) {
        if (ic.naturalWidth === 0) {
          console.error(`🚨 Hero image ${ic.index + 1} FAILED to load: ${ic.src}`);
        } else {
          console.log(`Hero image ${ic.index + 1}: ${ic.naturalWidth}x${ic.naturalHeight} (${ic.src})`);
        }
      }
    }

    const warnings = [];

    for (let i = 0; i < TARGETS.length; i++) {
      const [sel, fname] = TARGETS[i];
      const el = await page.$(sel);
      if (!el) { console.error(`NOT FOUND: ${sel}`); continue; }
      const fp = path.join(OUT, fname);
      await el.screenshot({ path: fp, type: 'png' });
      const kb = Math.round(fs.statSync(fp).size / 1024);
      const isCoverOrFinale = (i === 0 || i === TARGETS.length - 1);
      const threshold = isCoverOrFinale ? SIZE_WARN_COVER : SIZE_WARN_TEXT;

      let status = 'OK';
      if (kb < threshold) {
        status = 'WARN';
        const reason = isCoverOrFinale
          ? `Cover/finale only ${kb}KB — background image may not have rendered`
          : `Page only ${kb}KB — content may be missing`;
        warnings.push(`${fname}: ${reason}`);
      }
      console.log(`${status}: ${fname} (${kb}KB)`);
    }

    if (warnings.length > 0) {
      console.log('\n⚠️  SIZE WARNINGS:');
      warnings.forEach(w => console.log(`  - ${w}`));
      console.log('  → Check that background images are valid and different from each other');
    }

    await browser.close();
    serverProc.kill();
    console.log(`\nDone! ${TARGETS.length} screenshots in ${OUT}`);
  } catch (err) {
    console.error('Screenshot failed:', err.message);
    if (server) server.proc.kill();
    process.exit(1);
  }
})();
