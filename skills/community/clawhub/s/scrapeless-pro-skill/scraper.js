#!/usr/bin/env node
/**
 * Scrapeless Pro — Professional Web Scraping for OpenClaw
 * Stealth browser automation with Playwright + anti-detection
 */

const { program } = require('commander');
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// ─── License Validation ───────────────────────────────────────────
const LICENSE_KEY = process.env.SCRAPELESS_LICENSE_KEY;

function validateLicense(key) {
    if (!key) {
        console.error('❌ SCRAPELESS_LICENSE_KEY not set.');
        console.error('   Purchase at https://scrapeless-pro.com');
        console.error('   export SCRAPELESS_LICENSE_KEY="SCRAPELESS-XXXX-XXXX-XXXX-XXXX"');
        return false;
    }
    const regex = /^SCRAPELESS\-[A-Z0-9]{4}\-[A-Z0-9]{4}\-[A-Z0-9]{4}\-[A-Z0-9]{4}$/;
    if (!regex.test(key)) {
        console.error('❌ Invalid license format. Expected: SCRAPELESS-XXXX-XXXX-XXXX-XXXX');
        return false;
    }
    return true;
}

// ─── User Agent Pool ──────────────────────────────────────────────
const USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15',
];

function randomUserAgent() {
    return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function randomViewport() {
    const widths = [1920, 1366, 1440, 1536, 1280];
    const heights = [1080, 768, 900, 864, 720];
    const i = Math.floor(Math.random() * widths.length);
    return { width: widths[i], height: heights[i] };
}

function randomDelay(min = 500, max = 2000) {
    return new Promise(r => setTimeout(r, min + Math.random() * (max - min)));
}

// ─── Stealth Context Builder ──────────────────────────────────────
async function createStealthContext(browser) {
    const viewport = randomViewport();
    const ua = randomUserAgent();

    const context = await browser.newContext({
        userAgent: ua,
        viewport,
        locale: 'en-US',
        timezoneId: 'America/New_York',
        permissions: ['geolocation'],
        geolocation: { latitude: 40.7128, longitude: -74.0060 },
        colorScheme: 'light',
        deviceScaleFactor: 1 + Math.random(),
        hasTouch: false,
        isMobile: false,
        javaScriptEnabled: true,
        ignoreHTTPSErrors: true,
    });

    // Inject stealth scripts before any page loads
    await context.addInitScript(() => {
        // Override webdriver detection
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        // Override plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        // Override languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
        });
        // Override permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) =>
            parameters.name === 'notifications'
                ? Promise.resolve({ state: Notification.permission })
                : originalQuery(parameters);
        // Hide Chrome runtime
        window.chrome = { runtime: {} };
        // Override toString for stealth
        const nativeToStringFunctionString = Error.toString().replace(/Error/g, 'toString');
        const origProto = Function.prototype.toString;
        const myToString = function () {
            if (this === myToString) return nativeToStringFunctionString;
            return origProto.call(this);
        };
        Function.prototype.toString = myToString;
    });

    return context;
}

// ─── Data Extraction ──────────────────────────────────────────────
async function extractData(page, selectors) {
    return await page.evaluate((sels) => {
        const data = { title: document.title, url: window.location.href, timestamp: new Date().toISOString() };

        if (sels && Object.keys(sels).length > 0) {
            // Extract based on provided selectors
            for (const [key, selector] of Object.entries(sels)) {
                const elements = document.querySelectorAll(selector);
                data[key] = Array.from(elements).map(el => el.textContent.trim()).filter(Boolean);
                if (data[key].length === 1) data[key] = data[key][0];
            }
        } else {
            // Auto-detect: extract common data patterns
            data.headings = Array.from(document.querySelectorAll('h1, h2, h3')).map(h => ({
                level: h.tagName,
                text: h.textContent.trim()
            })).filter(h => h.text);

            data.links = Array.from(document.querySelectorAll('a[href]')).slice(0, 50).map(a => ({
                text: a.textContent.trim(),
                href: a.href
            })).filter(l => l.text);

            data.images = Array.from(document.querySelectorAll('img[src]')).slice(0, 20).map(img => ({
                alt: img.alt,
                src: img.src
            }));

            data.paragraphs = Array.from(document.querySelectorAll('p')).map(p => p.textContent.trim()).filter(Boolean).slice(0, 20);

            data.meta = {};
            document.querySelectorAll('meta[name], meta[property]').forEach(m => {
                const key = m.getAttribute('name') || m.getAttribute('property');
                data.meta[key] = m.getAttribute('content');
            });
        }

        return data;
    }, selectors);
}

// ─── Output Formatters ────────────────────────────────────────────
function toJSON(data) {
    return JSON.stringify(data, null, 2);
}

function toCSV(data) {
    if (!data || typeof data !== 'object') return '';
    const flat = {};
    for (const [key, value] of Object.entries(data)) {
        if (Array.isArray(value)) {
            flat[key] = value.map(v => typeof v === 'object' ? JSON.stringify(v) : v).join('; ');
        } else if (typeof value === 'object' && value !== null) {
            flat[key] = JSON.stringify(value);
        } else {
            flat[key] = value;
        }
    }
    const headers = Object.keys(flat);
    const values = headers.map(h => `"${String(flat[h] || '').replace(/"/g, '""')}"`);
    return [headers.join(','), values.join(',')].join('\n');
}

function toMarkdown(data) {
    let md = `# ${data.title || 'Scraped Page'}\n\n`;
    md += `**URL:** ${data.url}\n`;
    md += `**Scraped:** ${data.timestamp}\n\n`;
    if (data.headings) {
        md += `## Headings\n`;
        data.headings.forEach(h => md += `- ${h.level}: ${h.text}\n`);
        md += '\n';
    }
    if (data.paragraphs) {
        md += `## Content\n`;
        data.paragraphs.forEach(p => md += `${p}\n\n`);
    }
    return md;
}

// ─── Main Scrape Function ─────────────────────────────────────────
async function scrape(url, options = {}) {
    const { format = 'json', selectors = null, timeout = 30000, output = null, headless = true, delay: delayMs = 1000 } = options;

    console.log(`🕷️ Scrapeless Pro — Starting scrape`);
    console.log(`   URL: ${url}`);
    console.log(`   Format: ${format}`);
    console.log(`   Stealth: enabled`);

    const browser = await chromium.launch({
        headless,
        args: [
            '--disable-blink-features=AutomationControlled',
            '--disable-infobars',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--disable-gpu',
        ],
    });

    try {
        const context = await createStealthContext(browser);
        const page = await context.newPage();

        // Random delay before navigation
        await randomDelay(300, delayMs);

        console.log(`   Navigating...`);
        const response = await page.goto(url, {
            waitUntil: 'networkidle',
            timeout,
        });

        console.log(`   Status: ${response.status()}`);

        // Human-like behavior: scroll randomly
        await page.evaluate(() => {
            window.scrollBy(0, Math.random() * 500);
        });
        await randomDelay(500, 1500);

        // Extract data
        console.log(`   Extracting data...`);
        const parsedSelectors = selectors ? JSON.parse(selectors) : null;
        const data = await extractData(page, parsedSelectors);

        // Format output
        let formatted;
        switch (format) {
            case 'csv':
                formatted = toCSV(data);
                break;
            case 'markdown':
            case 'md':
                formatted = toMarkdown(data);
                break;
            default:
                formatted = toJSON(data);
        }

        // Output
        if (output) {
            fs.writeFileSync(output, formatted);
            console.log(`   ✅ Saved to ${output}`);
        } else {
            console.log(formatted);
        }

        await context.close();
        console.log(`\n✅ Scrape complete`);

        return data;

    } catch (err) {
        console.error(`❌ Scrape failed: ${err.message}`);
        throw err;
    } finally {
        await browser.close();
    }
}

// ─── CLI Setup ────────────────────────────────────────────────────
program
    .name('scrapeless')
    .description('Professional web scraping for OpenClaw')
    .version('1.0.3');

program
    .command('scrape <url>')
    .description('Scrape a URL with stealth browser automation')
    .option('-f, --format <format>', 'Output format: json, csv, markdown', 'json')
    .option('-s, --selectors <json>', 'CSS selectors as JSON: {"name":"selector"}')
    .option('-o, --output <file>', 'Save output to file')
    .option('-t, --timeout <ms>', 'Navigation timeout in ms', '30000')
    .option('--no-headless', 'Run in headed mode (visible browser)')
    .option('-d, --delay <ms>', 'Random delay before navigation', '1000')
    .action(async (url, opts) => {
        if (!validateLicense(LICENSE_KEY)) process.exit(1);
        try {
            await scrape(url, {
                format: opts.format,
                selectors: opts.selectors,
                output: opts.output,
                timeout: parseInt(opts.timeout),
                headless: opts.headless,
                delay: parseInt(opts.delay),
            });
        } catch (err) {
            process.exit(1);
        }
    });

program
    .command('validate')
    .description('Validate your license key')
    .action(() => {
        if (validateLicense(LICENSE_KEY)) {
            console.log(`✅ License valid: ${LICENSE_KEY}`);
        } else {
            process.exit(1);
        }
    });

program.parse();

module.exports = { scrape, validateLicense, extractData };