import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { autoSolveCaptcha } from './primitives/captcha.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = path.join(__dirname, '..', 'data');
const SESSIONS_DIR = path.join(DATA_DIR, 'sessions');
const SCREENSHOTS_DIR = path.join(DATA_DIR, 'screenshots');

fs.mkdirSync(SESSIONS_DIR, { recursive: true });
fs.mkdirSync(SCREENSHOTS_DIR, { recursive: true });

const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

class BrowserPool {
  constructor() {
    this.browser = null;
    this.contexts = new Map(); // domain -> context
  }

  async getBrowser() {
    if (!this.browser) {
      this.browser = await chromium.launch({
        headless: true,
        args: [
          '--disable-blink-features=AutomationControlled',
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-accelerated-2d-canvas',
          '--disable-gpu',
          '--window-size=1920,1080',
        ],
      });
      console.log('[BrowserPool] Browser launched');
    }
    return this.browser;
  }

  async getContext(domain) {
    if (this.contexts.has(domain)) {
      return this.contexts.get(domain);
    }

    const browser = await this.getBrowser();
    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: USER_AGENT,
      locale: 'en-US',
      timezoneId: 'America/New_York',
    });

    // Anti-detection
    await context.addInitScript(() => {
      Object.defineProperty(navigator, 'webdriver', { get: () => false });
      delete navigator.__proto__.webdriver;
    });

    // Load saved cookies if they exist
    const cookiePath = path.join(SESSIONS_DIR, `cookies-${domain}.json`);
    if (fs.existsSync(cookiePath)) {
      try {
        const cookies = JSON.parse(fs.readFileSync(cookiePath, 'utf-8'));
        await context.addCookies(cookies);
        console.log(`[BrowserPool] Loaded ${cookies.length} cookies for ${domain}`);
      } catch (e) {
        console.log(`[BrowserPool] Failed to load cookies for ${domain}: ${e.message}`);
      }
    }

    this.contexts.set(domain, context);
    return context;
  }

  async getPage(domain) {
    const context = await this.getContext(domain);
    const page = await context.newPage();

    // Register CAPTCHA auto-detection on page load
    page.on('load', async () => {
      try {
        // Short delay to let challenge render
        await page.waitForTimeout(1000).catch(() => {});
        await autoSolveCaptcha(page);
      } catch {
        // Non-blocking — don't let CAPTCHA detection crash page loads
      }
    });

    return page;
  }

  async saveCookies(domain) {
    const context = this.contexts.get(domain);
    if (!context) return;
    const cookies = await context.cookies();
    const cookiePath = path.join(SESSIONS_DIR, `cookies-${domain}.json`);
    fs.writeFileSync(cookiePath, JSON.stringify(cookies, null, 2));
    console.log(`[BrowserPool] Saved ${cookies.length} cookies for ${domain}`);
  }

  async screenshot(page, name) {
    const filepath = path.join(SCREENSHOTS_DIR, `${name}-${Date.now()}.png`);
    await page.screenshot({ path: filepath, fullPage: false });
    console.log(`[BrowserPool] Screenshot: ${filepath}`);
    return filepath;
  }

  getDomain(url) {
    try {
      return new URL(url).hostname;
    } catch {
      return url;
    }
  }

  async close() {
    // Save all cookies before closing
    for (const [domain] of this.contexts) {
      await this.saveCookies(domain);
    }
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
      this.contexts.clear();
      console.log('[BrowserPool] Browser closed');
    }
  }
}

// Singleton
const pool = new BrowserPool();
export default pool;
export { BrowserPool, SESSIONS_DIR, SCREENSHOTS_DIR, DATA_DIR };
