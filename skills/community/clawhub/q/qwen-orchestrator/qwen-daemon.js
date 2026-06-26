const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const PROFILE_DIR = path.join(__dirname, '.profile');
const SESSIONS_DIR = path.join(__dirname, '.sessions');
const SESSION_FILE = path.join(SESSIONS_DIR, 'daemon.json');
const DAEMON_ENDPOINT_FILE = path.join(__dirname, '.daemon-ws-endpoint');
const QWEN_URL = 'https://chat.qwen.ai/';

let browser = null;
let page = null;
let endpoint = '';
let sessionPayload = '';
let healing = false;

function unlinkIfMatches(filePath, expectedContent) {
  try {
    if (!fs.existsSync(filePath)) return;
    const current = fs.readFileSync(filePath, 'utf8');
    if (current === expectedContent) {
      fs.unlinkSync(filePath);
    }
  } catch (e) {}
}

function writeEndpointFiles() {
  if (!browser) return;
  endpoint = browser.wsEndpoint();
  sessionPayload = JSON.stringify({
    browserWSEndpoint: endpoint,
    pid: process.pid,
    created: new Date().toISOString(),
  });
  fs.writeFileSync(DAEMON_ENDPOINT_FILE, endpoint);
  fs.writeFileSync(SESSION_FILE, sessionPayload);
}

function cleanupEndpointFiles() {
  try {
    unlinkIfMatches(DAEMON_ENDPOINT_FILE, endpoint);
    unlinkIfMatches(SESSION_FILE, sessionPayload);
  } catch (e) {}
}

async function navigateWithRetry(targetPage, label = 'Qwen Chat') {
  const MAX_NAV_RETRIES = 3;
  for (let attempt = 1; attempt <= MAX_NAV_RETRIES; attempt++) {
    try {
      console.log(`📍 Навигация на ${label} (попытка ${attempt}/${MAX_NAV_RETRIES})...`);
      await targetPage.goto(QWEN_URL, { timeout: 60000, waitUntil: 'domcontentloaded' });
      console.log(`✅ ${label} loaded`);
      return;
    } catch (navErr) {
      console.log(`⚠️ Навигация не удалась (попытка ${attempt}): ${navErr.message}`);
      if (attempt < MAX_NAV_RETRIES) {
        const waitMs = Math.min(attempt * 5000, 15000);
        console.log(`⏳ Ожидание ${waitMs / 1000}s перед повторной попыткой...`);
        await new Promise((r) => setTimeout(r, waitMs));
        try { await targetPage.reload({ waitUntil: 'domcontentloaded', timeout: 30000 }); } catch {}
      } else {
        console.error(`❌ Не удалось загрузить ${label} после ${MAX_NAV_RETRIES} попыток`);
      }
    }
  }
}

async function ensureDaemonPage(reason = 'health-check') {
  if (healing) return page;
  healing = true;
  try {
    if (!browser || !browser.isConnected()) {
      throw new Error('browser disconnected');
    }

    if (page) {
      try {
        if (!page.isClosed()) {
          await page.title().catch(() => {});
          return page;
        }
      } catch {}
    }

    const pages = await browser.pages().catch(() => []);
    const livePages = pages.filter((p) => {
      try { return p && !p.isClosed(); } catch { return false; }
    });

    page = livePages.find((p) => {
      try {
        const url = p.url();
        return url.includes('qwen') || url === 'about:blank';
      } catch {
        return false;
      }
    }) || livePages[0] || await browser.newPage();

    console.log(`🔧 Восстанавливаю daemon page (${reason})...`);
    try {
      const url = page.url();
      if (!url || url === 'about:blank' || url.includes('chrome-error')) {
        await navigateWithRetry(page, 'Qwen Chat');
      }
    } catch {
      await navigateWithRetry(page, 'Qwen Chat');
    }

    page.on('error', async (err) => {
      console.error('⚠️ Страница упала, пробую восстановить...', err.message);
      try {
        await ensureDaemonPage('page-error');
        if (page && !page.isClosed()) {
          await navigateWithRetry(page, 'Qwen Chat');
          console.log('✅ Страница восстановлена после ошибки');
        }
      } catch (e) {
        console.error('❌ Не удалось восстановить страницу:', e.message);
      }
    });

    page.on('close', async () => {
      console.log('⚠️ Текущая страница daemon была закрыта, создаю новую...');
      try {
        page = null;
        await ensureDaemonPage('page-closed');
      } catch (e) {
        console.error('❌ Не удалось пересоздать страницу:', e.message);
      }
    });

    return page;
  } finally {
    healing = false;
  }
}

(async () => {
  console.log('🚀 Запуск Qwen Daemon...');

  fs.mkdirSync(PROFILE_DIR, { recursive: true });
  fs.mkdirSync(SESSIONS_DIR, { recursive: true });

  browser = await puppeteer.launch({
    headless: 'new',
    userDataDir: PROFILE_DIR,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--no-first-run',
      '--no-default-browser-check',
      '--disable-gpu',
      '--window-size=1280,800',
    ],
  });

  browser.on('disconnected', () => {
    console.error('❌ Браузер daemon отключился; очищаю endpoint и выхожу');
    cleanupEndpointFiles();
    process.exit(1);
  });

  writeEndpointFiles();
  console.log(`✅ Endpoint готов: ${endpoint}`);

  page = (await browser.pages())[0] || await browser.newPage();
  await navigateWithRetry(page, 'Qwen Chat');
  await ensureDaemonPage('startup');

  setInterval(async () => {
    try {
      if (!browser || !browser.isConnected()) {
        throw new Error('browser disconnected');
      }
      await ensureDaemonPage('periodic-health');
      const url = page.url();
      if (url.includes('chrome-error://') || url.includes('chrome-error')) {
        console.log('⚠️ Страница на error page, перезагружаем...');
        await navigateWithRetry(page, 'Qwen Chat');
        console.log('✅ Страница восстановлена: ' + page.url());
      }
    } catch (e) {
      console.error('⚠️ Health-check daemon не удался:', e.message);
      cleanupEndpointFiles();
      process.exit(1);
    }
  }, 30000);

  const shutdown = async (signal) => {
    console.log(`\n(System) Получен ${signal}, останавливаю демон...`);
    try {
      if (browser) await browser.close();
    } catch (e) {}
    cleanupEndpointFiles();
    console.log('✅ Демон остановлен');
    process.exit(0);
  };

  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('SIGINT', () => shutdown('SIGINT'));
  process.on('SIGHUP', () => shutdown('SIGHUP'));

  console.log(`🆔 PID: ${process.pid}`);
  console.log('💡 Для остановки: kill ' + process.pid);
})();
