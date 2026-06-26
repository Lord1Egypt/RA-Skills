#!/usr/bin/env node
/**
 * TikTok Stream URL Extractor v2.4
 * 
 * Strategie:
 * 1. Playwright: Navigiere zu /live, schließe Popups, fange FLV-URLs via page.on('response')
 * 2. Streamlink: Fallback (zuverlässigste CLI-Methode)
 * 3. yt-dlp: Letzter Fallback
 * 
 * Fix: Verwendet page.on('response') statt nicht-existierender waitForResponses()
 */

const { chromium } = require('playwright');
const path = require('path');
const util = require('util');
const execPromise = util.promisify(require('child_process').exec);

function humanDelay(min = 2000, max = 4000) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// DSGVO + Login-Popups schließen
async function handlePopups(page) {
    let closed = false;

    // DSGVO
    const dsgvoSelectors = [
        'button:has-text("Verstanden")', '[data-e2e="cookie-banner-accept"]',
        'button:has-text("Accept")', 'button:has-text("Akzeptieren")',
        'button:has-text("Alle akzeptieren")', 'button:has-text("Allow all")',
        'button:has-text("Accept all")', '[data-testid="cookie-policy-banner-accept"]'
    ];
    for (const sel of dsgvoSelectors) {
        try {
            const btn = await page.waitForSelector(sel, { state: 'visible', timeout: 3000 });
            if (btn) { await btn.click(); await page.waitForTimeout(humanDelay(1000, 2000)); closed = true; break; }
        } catch (e) { /* weiter */ }
    }

    // Login Pop-up 1: "Bei TikTok anmelden" → X-Button
    try {
        const loginText = await page.$('text="Bei TikTok anmelden"');
        if (loginText) {
            const closeBtn = await page.$('div[role="dialog"] [aria-label="Close"], div[role="dialog"] button[aria-label="Schließen"], div[role="dialog"] svg');
            if (closeBtn) { await closeBtn.click(); await page.waitForTimeout(humanDelay(1000, 2000)); closed = true; }
        }
    } catch (e) { /* nicht da */ }

    // Login Pop-up 2: "Jetzt nicht" Button
    try {
        const skipBtn = await page.$('button:has-text("Jetzt nicht"), button:has-text("Not now")');
        if (skipBtn) { await skipBtn.click(); await page.waitForTimeout(humanDelay(1000, 2000)); closed = true; }
    } catch (e) { /* nicht da */ }

    return closed;
}

// Prüfe ob Stream eingeschränkt ist (nach Popup-Handling)
async function checkRestrictions(page) {
    const restrictionTexts = [
        'text="Bei TikTok anmelden"',
        'text=/Dieses LIVE enthält Themen/',
        'text="Melde dich an für das vollständige Erlebnis"',
        'text=/Melde dich an für das volle/',
        'text="Log in to TikTok"',
        'text=/mature content/',
        'text=/age-restricted/'
    ];
    for (const sel of restrictionTexts) {
        try {
            const el = await page.$(sel);
            if (el && await el.isVisible()) {
                return { restricted: true, reason: sel.replace('text=', '').replace(/[/"]/g, '') };
            }
        } catch (e) { /* weiter */ }
    }
    return { restricted: false, reason: null };
}

// Playwright-basierte FLV-Extraktion
async function extractWithPlaywright(username, qualityPreference) {
    let browser;
    try {
        browser = await chromium.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
        });
        const context = await browser.newContext({
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport: { width: 1920, height: 1080 }
        });
        const page = await context.newPage();

        // FLV-URLs sammeln via Event-Listener BEVOR wir navigieren
        const collectedUrls = [];
        page.on('response', response => {
            const url = response.url();
            if (url.includes('.flv') && (url.includes('tiktokcdn') || url.includes('pull-flv'))) {
                collectedUrls.push({
                    url: url,
                    status: response.status(),
                    timestamp: new Date().toISOString()
                });
            }
        });

        // Navigiere direkt zu /live
        await page.goto(`https://www.tiktok.com/@${username}/live`, {
            waitUntil: 'domcontentloaded',
            timeout: 30000
        });

        // Popups schließen
        await handlePopups(page);

        // Warte auf Seitenaufbau
        await page.waitForTimeout(humanDelay(3000, 5000));
        try { await page.waitForLoadState('networkidle', { timeout: 10000 }); } catch (e) { /* ok */ }

        // Prüfe auf Einschränkungen
        const restrictions = await checkRestrictions(page);
        if (restrictions.restricted) {
            console.log(`Playwright: Stream restricted - ${restrictions.reason}`);
            return { success: false, method: 'playwright', restricted: true, reason: restrictions.reason };
        }

        // Versuche Video abzuspielen falls nötig
        try {
            const video = await page.$('video');
            if (video) { await video.evaluate(v => v.play()).catch(() => {}); }
        } catch (e) { /* ok */ }

        // Warte auf FLV-URLs (Stream muss laden)
        await page.waitForTimeout(humanDelay(8000, 12000));

        // Zweiter Versuch Popups zu schließen (können nach Delay erscheinen)
        await handlePopups(page);
        await page.waitForTimeout(humanDelay(3000, 5000));

        // Nochmal Restrictions prüfen
        const restrictions2 = await checkRestrictions(page);
        if (restrictions2.restricted) {
            console.log(`Playwright: Stream became restricted after wait - ${restrictions2.reason}`);
            return { success: false, method: 'playwright', restricted: true, reason: restrictions2.reason };
        }

        // URLs auswerten
        if (collectedUrls.length === 0) {
            console.log('Playwright: No FLV URLs captured via network monitoring.');
            return { success: false, method: 'playwright', restricted: false, reason: 'No FLV URLs found' };
        }

        // Deduplizieren und nach Qualität sortieren
        const uniqueUrls = [...new Map(collectedUrls.map(item => [item.url.split('?')[0], item])).values()];

        // Qualitäts-Präferenz anwenden
        const qualityOrder = qualityPreference === 'auto'
            ? ['_hd.flv', '_sd.flv', '_ld.flv', '.flv']
            : [`_${qualityPreference}.flv`, '.flv'];

        let bestUrl = null;
        for (const suffix of qualityOrder) {
            bestUrl = uniqueUrls.find(u => u.url.includes(suffix));
            if (bestUrl) break;
        }
        if (!bestUrl) bestUrl = uniqueUrls[0];

        return {
            success: true,
            method: 'playwright',
            username,
            url: bestUrl.url,
            quality: qualityPreference,
            allUrls: uniqueUrls.length,
            timestamp: new Date().toISOString()
        };

    } catch (error) {
        console.error(`Playwright error: ${error.message}`);
        return { success: false, method: 'playwright', error: error.message };
    } finally {
        if (browser) await browser.close();
    }
}

// Streamlink Fallback
async function tryStreamlink(username, quality) {
    const scriptPath = path.join(__dirname, 'extraction-methods', 'extract-tiktok-streamlink.sh');
    try {
        const { stdout } = await execPromise(`bash "${scriptPath}" ${username} ${quality} --json`);
        return JSON.parse(stdout);
    } catch (error) {
        if (error.stdout) {
            try { return JSON.parse(error.stdout); } catch (e) { /* kein JSON */ }
        }
        return { success: false, method: 'streamlink', username, message: error.message, timestamp: new Date().toISOString() };
    }
}

// yt-dlp Fallback
async function tryYtDlp(username, quality) {
    const scriptPath = path.join(__dirname, 'extraction-methods', 'extract-tiktok-yt-dlp.sh');
    const ytFormat = quality === 'ld' ? 'worst' : (quality === 'auto' ? 'best' : quality);
    try {
        const { stdout } = await execPromise(`bash "${scriptPath}" ${username} ${ytFormat} --json`);
        return JSON.parse(stdout);
    } catch (error) {
        if (error.stdout) {
            try { return JSON.parse(error.stdout); } catch (e) { /* kein JSON */ }
        }
        return { success: false, method: 'yt-dlp', username, message: error.message, timestamp: new Date().toISOString() };
    }
}

// Hauptfunktion mit Fallback-Kette
async function getStreamUrl(username, qualityPreference = 'ld') {
    const timestamp = new Date().toISOString();

    // --- 1. Playwright ---
    console.log(`[1/3] Trying Playwright for @${username}...`);
    const pwResult = await extractWithPlaywright(username, qualityPreference);
    if (pwResult.success) {
        pwResult.timestamp = timestamp;
        return pwResult;
    }
    console.log(`Playwright result: ${pwResult.reason || pwResult.error || 'failed'}`);

    // --- 2. Streamlink (zuverlässigster Fallback) ---
    console.log(`[2/3] Trying streamlink for @${username} (quality: ${qualityPreference})...`);
    const slResult = await tryStreamlink(username, qualityPreference);
    if (slResult.success) {
        return slResult;
    }
    console.log(`Streamlink result: ${slResult.message || slResult.error || 'failed'}`);

    // --- 3. yt-dlp (letzter Versuch) ---
    console.log(`[3/3] Trying yt-dlp for @${username}...`);
    const ytResult = await tryYtDlp(username, qualityPreference);
    if (ytResult.success) {
        return ytResult;
    }
    console.log(`yt-dlp result: ${ytResult.message || ytResult.error || 'failed'}`);

    // --- Alle fehlgeschlagen ---
    return {
        success: false,
        username,
        message: 'All extraction methods failed (Playwright, streamlink, yt-dlp).',
        playwrightReason: pwResult.reason || pwResult.error,
        streamlinkReason: slResult.message || slResult.error,
        ytdlpReason: ytResult.message || ytResult.error,
        timestamp
    };
}

// --- CLI ---
if (process.argv.length < 3) {
    console.error('Usage: node tiktok-get-stream.js <username> [quality: ld|sd|hd|origin|auto] [--json]');
    process.exit(1);
}

const cliUsername = process.argv[2];
const cliQuality = process.argv[3] || 'ld';
const cliJson = process.argv.includes('--json');

getStreamUrl(cliUsername, cliQuality).then(result => {
    if (cliJson) {
        console.log(JSON.stringify(result, null, 2));
    } else {
        if (result.success) {
            console.log(result.url);
        } else {
            console.error(result.message);
        }
    }
    process.exit(result.success ? 0 : 1);
}).catch(err => {
    console.error('Unhandled error:', err.message);
    process.exit(1);
});
