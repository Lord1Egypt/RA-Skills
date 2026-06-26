#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const path = require("node:path");

function parseArgs(argv) {
  const args = {
    url: "",
    output: "xhs_note_browser.json",
    cookieFile: "",
    timeout: 45000,
    waitMs: 2500,
    headed: false,
    screenshot: "",
    htmlOut: "",
  };
  for (let i = 2; i < argv.length; i += 1) {
    const k = argv[i];
    const v = argv[i + 1];
    if (k === "--url") args.url = v || "";
    else if (k === "--output") args.output = v || args.output;
    else if (k === "--cookie-file") args.cookieFile = v || "";
    else if (k === "--timeout") args.timeout = Number(v || args.timeout);
    else if (k === "--wait-ms") args.waitMs = Number(v || args.waitMs);
    else if (k === "--screenshot") args.screenshot = v || "";
    else if (k === "--html-out") args.htmlOut = v || "";
    else if (k === "--headed") args.headed = true;
    else if (k === "--help" || k === "-h") {
      printHelp();
      process.exit(0);
    }
  }
  return args;
}

function printHelp() {
  console.log(`Usage:
  node fetch_xiaohongshu_note_playwright.js --url <note_url> [options]

Options:
  --url <url>            Xiaohongshu note URL
  --output <file>        Output JSON file (default: xhs_note_browser.json)
  --cookie-file <file>   Raw Cookie header value saved in a text file
  --timeout <ms>         Navigation timeout in ms (default: 45000)
  --wait-ms <ms>         Extra wait after load (default: 2500)
  --headed               Run non-headless for debugging
  --screenshot <file>    Optional screenshot output path
  --html-out <file>      Optional rendered HTML output path
  --help                 Show help`);
}

function parseCookieHeader(raw) {
  const out = [];
  const text = (raw || "").trim();
  if (!text) return out;
  for (const part of text.split(";")) {
    const p = part.trim();
    if (!p) continue;
    const idx = p.indexOf("=");
    if (idx <= 0) continue;
    const name = p.slice(0, idx).trim();
    const value = p.slice(idx + 1).trim();
    if (!name) continue;
    out.push({ name, value, domain: ".xiaohongshu.com", path: "/" });
  }
  return out;
}

function pick(v, fallback = null) {
  return v === undefined || v === null || v === "" ? fallback : v;
}

function toIntMaybe(v) {
  if (v === undefined || v === null) return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

function extractNoteId(url) {
  const m = String(url || "").match(/\/explore\/([0-9a-zA-Z]+)/);
  return m ? m[1] : null;
}

function deepFind(obj, keys) {
  if (!obj || typeof obj !== "object") return [];
  const res = [];
  const stack = [obj];
  while (stack.length) {
    const cur = stack.pop();
    if (!cur || typeof cur !== "object") continue;
    for (const [k, v] of Object.entries(cur)) {
      if (keys.includes(k)) res.push(v);
      if (v && typeof v === "object") stack.push(v);
    }
  }
  return res;
}

async function run() {
  const args = parseArgs(process.argv);
  if (!args.url) {
    printHelp();
    process.exit(2);
  }

  let playwright;
  try {
    playwright = require("playwright");
  } catch (e) {
    console.error("playwright_not_installed");
    console.error("Install: npm i playwright && npx playwright install chromium");
    process.exit(3);
  }

  const payload = {
    ok: false,
    url: args.url,
    final_url: args.url,
    note_id: extractNoteId(args.url),
    title: null,
    description: null,
    author: null,
    published_at: null,
    tags: [],
    images: [],
    interaction: {
      like_count: null,
      comment_count: null,
      share_count: null,
      collect_count: null,
    },
    login_popup_detected: false,
    login_popup_closed: false,
    fetched_at_utc: new Date().toISOString(),
    source_status: "error",
    error: "",
  };

  const browser = await playwright.chromium.launch({ headless: !args.headed });
  const context = await browser.newContext({
    userAgent:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " +
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    locale: "zh-CN",
    viewport: { width: 1440, height: 2000 },
  });

  try {
    if (args.cookieFile) {
      const cookieText = fs.readFileSync(args.cookieFile, "utf-8");
      const cookies = parseCookieHeader(cookieText);
      if (cookies.length > 0) await context.addCookies(cookies);
    }

    const page = await context.newPage();
    await page.goto(args.url, { waitUntil: "domcontentloaded", timeout: args.timeout });
    await page.waitForTimeout(args.waitMs);
    payload.final_url = page.url();

    const isLoginRedirect = payload.final_url.includes("/login");
    if (isLoginRedirect) {
      payload.ok = false;
      payload.source_status = "login_required";
      payload.error = "redirected_to_login; provide cookie-file from logged-in browser";
      const htmlEarly = await page.content();
      if (args.htmlOut) fs.writeFileSync(args.htmlOut, htmlEarly, "utf-8");
      if (args.screenshot) await page.screenshot({ path: args.screenshot, fullPage: true });
    }
    const popupResult = await page.evaluate(() => {
      const hasLoginText = /登录查看更多内容|登录后查看更多内容/.test(document.body.innerText || "");
      const closeSelectors = [
        'button[aria-label*="关闭"]',
        'button[class*="close"]',
        'div[class*="close"]',
        'i[class*="close"]',
        '.login-container button',
        '.login-guide button',
      ];
      let clicked = false;
      for (const sel of closeSelectors) {
        const nodes = Array.from(document.querySelectorAll(sel));
        for (const n of nodes) {
          const txt = (n.textContent || "").trim();
          const cls = n.className ? String(n.className) : "";
          if (/关闭|close|icon-close|cancel/i.test(txt + " " + cls)) {
            try {
              n.click();
              clicked = true;
            } catch (_) {}
          }
        }
      }
      // Remove common overlay layers if present.
      const overlaySelectors = [
        '.mask',
        '.modal-mask',
        '.overlay',
        '.login-container',
        '.login-guide',
        '[class*="login-panel"]',
      ];
      for (const sel of overlaySelectors) {
        const nodes = document.querySelectorAll(sel);
        nodes.forEach((el) => {
          const c = el.className ? String(el.className) : "";
          if (/login|modal|mask|overlay/i.test(c)) {
            try {
              el.remove();
            } catch (_) {}
          }
        });
      }
      return { hasLoginText, clicked };
    });
    payload.login_popup_detected = !!(popupResult && popupResult.hasLoginText);
    payload.login_popup_closed = !!(popupResult && popupResult.clicked);
    if (payload.login_popup_detected) {
      await page.waitForTimeout(1200);
    }
    if (!isLoginRedirect) {
      const html = await page.content();
      if (args.htmlOut) {
        fs.writeFileSync(args.htmlOut, html, "utf-8");
      }
      if (args.screenshot) {
        await page.screenshot({ path: args.screenshot, fullPage: true });
      }

      const extracted = await page.evaluate(() => {
        const readMeta = (name) => {
          const p = document.querySelector(`meta[property="${name}"]`);
          if (p && p.content) return p.content;
          const n = document.querySelector(`meta[name="${name}"]`);
          if (n && n.content) return n.content;
          return null;
        };

        const getJsonLd = () => {
          const blocks = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
          const out = [];
          for (const b of blocks) {
            try {
              const v = JSON.parse(b.textContent || "");
              out.push(v);
            } catch (_) {}
          }
          return out;
        };

        return {
          title: readMeta("og:title") || document.title || null,
          description: readMeta("og:description") || null,
          ogImage: readMeta("og:image") || null,
          jsonLd: getJsonLd(),
        };
      });

      payload.title = pick(extracted.title);
      payload.description = pick(extracted.description);
      if (extracted.ogImage) payload.images.push(extracted.ogImage);

      const ldList = Array.isArray(extracted.jsonLd) ? extracted.jsonLd : [];
      const merged = {};
      for (const item of ldList) {
        if (item && typeof item === "object") Object.assign(merged, item);
      }

      if (merged.author && typeof merged.author === "object") {
        payload.author = pick(merged.author.name);
      }
      payload.published_at = pick(merged.datePublished);

      const keywords = pick(merged.keywords, "");
      if (typeof keywords === "string" && keywords.trim()) {
        payload.tags = keywords
          .split(/[，,]/)
          .map((s) => s.trim())
          .filter(Boolean);
      }

      const ldImage = merged.image;
      if (typeof ldImage === "string") payload.images.push(ldImage);
      if (Array.isArray(ldImage)) {
        for (const i of ldImage) {
          if (typeof i === "string") payload.images.push(i);
        }
      }
      payload.images = Array.from(new Set(payload.images.filter(Boolean)));

      // Regex fallback on rendered HTML for note description/author.
      const descPatterns = [/"desc":"([^"]{1,5000})"/, /"description":"([^"]{1,5000})"/];
      for (const p of descPatterns) {
        const m = html.match(p);
        if (m && m[1]) {
          const cand = m[1].replace(/\\n/g, "\n").replace(/\\"/g, '"').trim();
          if (cand && !/3 亿人的生活经验，都在小红书/.test(cand)) {
            payload.description = cand;
            break;
          }
        }
      }
      if (!payload.author) {
        const m = html.match(/"nickname":"([^"]{1,200})"/);
        if (m && m[1]) payload.author = m[1].replace(/\\"/g, '"');
      }

      const stats = Array.isArray(merged.interactionStatistic) ? merged.interactionStatistic : [];
      for (const s of stats) {
        if (!s || typeof s !== "object") continue;
        const t = String(s.interactionType || "").toLowerCase();
        const c = toIntMaybe(s.userInteractionCount);
        if (t.includes("like")) payload.interaction.like_count = c;
        else if (t.includes("comment")) payload.interaction.comment_count = c;
        else if (t.includes("share")) payload.interaction.share_count = c;
      }

      // Fallback: extract lightweight fields from visible DOM only.
      const domFallback = await page.evaluate(() => {
        const pickText = (selectors) => {
          for (const s of selectors) {
            const el = document.querySelector(s);
            const text = el && el.textContent ? el.textContent.trim() : "";
            if (text) return text;
          }
          return null;
        };
        return {
          title: pickText(["h1", ".note-content .title", ".content .title"]),
          author: pickText([".author .name", ".author-name", ".username", ".user-name", ".author"]),
          description: pickText([".note-content .desc", ".content .desc", ".note-desc", ".desc"]),
        };
      });
      if (!payload.title && domFallback && domFallback.title) payload.title = domFallback.title;
      if (!payload.author && domFallback && domFallback.author) payload.author = domFallback.author;
      if (!payload.description && domFallback && domFallback.description) payload.description = domFallback.description;
      if (payload.description && /3 亿人的生活经验，都在小红书/.test(payload.description)) {
        payload.description = null;
      }

      payload.ok = true;
      payload.source_status = "ok";
      if (!/\/explore\/[0-9a-zA-Z]+/.test(payload.final_url)) {
        payload.source_status = "redirected";
        payload.error = "redirected_to_non_note_page; try valid note URL and cookie-file";
        payload.ok = false;
      }
    }
  } catch (e) {
    payload.error = String(e && e.message ? e.message : e);
    payload.source_status = "error";
  } finally {
    await context.close();
    await browser.close();
  }

  fs.writeFileSync(args.output, `${JSON.stringify(payload, null, 2)}\n`, "utf-8");
  console.log(`Saved: ${path.resolve(args.output)}`);
  if (!payload.ok) process.exit(1);
}

run().catch((e) => {
  console.error(String(e));
  process.exit(1);
});
