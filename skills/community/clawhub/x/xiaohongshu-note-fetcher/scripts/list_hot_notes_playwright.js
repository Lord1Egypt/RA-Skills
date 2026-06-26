#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");

function parseArgs(argv) {
  const args = {
    keyword: "",
    cookieFile: "",
    maxItems: 50,
    minLikes: 1000,
    output: "xhs_hot_notes.json",
    mdOutput: "xhs_hot_notes.md",
    timeout: 45000,
    scrollRounds: 10,
    waitMs: 1800,
    headed: false,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const k = argv[i];
    const v = argv[i + 1];
    if (k === "--keyword") args.keyword = v || "";
    else if (k === "--cookie-file") args.cookieFile = v || "";
    else if (k === "--max-items") args.maxItems = Number(v || args.maxItems);
    else if (k === "--min-likes") args.minLikes = Number(v || args.minLikes);
    else if (k === "--output") args.output = v || args.output;
    else if (k === "--md-output") args.mdOutput = v || args.mdOutput;
    else if (k === "--timeout") args.timeout = Number(v || args.timeout);
    else if (k === "--scroll-rounds") args.scrollRounds = Number(v || args.scrollRounds);
    else if (k === "--wait-ms") args.waitMs = Number(v || args.waitMs);
    else if (k === "--headed") args.headed = true;
    else if (k === "--help" || k === "-h") {
      console.log(`Usage:
  node list_hot_notes_playwright.js --keyword <关键词> --cookie-file <cookie.txt> [options]

Options:
  --max-items <n>       Max notes to collect (default: 50)
  --min-likes <n>       Filter threshold (default: 1000)
  --output <file>       JSON output path
  --md-output <file>    Markdown output path
  --scroll-rounds <n>   Scroll rounds (default: 10)
  --wait-ms <ms>        Wait between rounds (default: 1800)
  --headed              Run non-headless for debug
`);
      process.exit(0);
    }
  }
  return args;
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

function parseLikes(raw) {
  const s = String(raw || "").trim().toLowerCase();
  if (!s) return null;
  const clean = s.replace(/,/g, "");
  const wan = clean.match(/^(\d+(?:\.\d+)?)\s*万$/);
  if (wan) return Math.round(Number(wan[1]) * 10000);
  const qian = clean.match(/^(\d+(?:\.\d+)?)\s*k$/);
  if (qian) return Math.round(Number(qian[1]) * 1000);
  const num = clean.match(/^\d+(?:\.\d+)?$/);
  if (num) return Math.round(Number(clean));
  return null;
}

function toMarkdown(data) {
  const lines = [];
  lines.push(`# 小红书高赞文章列表（点赞 > ${data.min_likes}）`);
  lines.push("");
  lines.push(`- 关键词: ${data.keyword}`);
  lines.push(`- 抓取时间: ${data.fetched_at_utc}`);
  lines.push(`- 总抓取: ${data.total_collected}`);
  lines.push(`- 高赞数量: ${data.hot_notes.length}`);
  lines.push("");
  if (data.hot_notes.length === 0) {
    lines.push("暂无符合条件的笔记。");
    return `${lines.join("\n")}\n`;
  }
  for (let i = 0; i < data.hot_notes.length; i += 1) {
    const n = data.hot_notes[i];
    lines.push(`${i + 1}. ${n.title || "Untitled"}`);
    lines.push(`   - 点赞: ${n.likes ?? "N/A"}`);
    lines.push(`   - 作者: ${n.author || "N/A"}`);
    lines.push(`   - 链接: ${n.url}`);
  }
  return `${lines.join("\n")}\n`;
}

async function main() {
  const args = parseArgs(process.argv);
  if (!args.keyword) throw new Error("missing --keyword");
  if (!args.cookieFile) throw new Error("missing --cookie-file");

  const browser = await chromium.launch({ headless: !args.headed });
  const context = await browser.newContext({
    userAgent:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " +
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    locale: "zh-CN",
    viewport: { width: 1400, height: 2200 },
  });

  try {
    const cookieText = fs.readFileSync(args.cookieFile, "utf-8");
    const cookies = parseCookieHeader(cookieText);
    if (cookies.length > 0) await context.addCookies(cookies);

    const page = await context.newPage();
    const url = `https://www.xiaohongshu.com/search_result?keyword=${encodeURIComponent(args.keyword)}&source=web_explore_feed`;
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: args.timeout });
    await page.waitForTimeout(args.waitMs);

    const loginState = await page.evaluate(() => {
      try {
        const st = window.__INITIAL_STATE__;
        if (st && st.user && typeof st.user.loggedIn === "boolean") {
          return { known: true, loggedIn: st.user.loggedIn };
        }
      } catch (_) {}
      return { known: false, loggedIn: null };
    });
    if (loginState.known && !loginState.loggedIn) {
      throw new Error("cookie_not_logged_in: refresh cookie from logged-in browser request");
    }

    // Try closing login overlays.
    await page.evaluate(() => {
      const sels = ['button[aria-label*="关闭"]', 'button[class*="close"]', '.close'];
      for (const s of sels) {
        for (const el of document.querySelectorAll(s)) {
          try {
            el.click();
          } catch (_) {}
        }
      }
    });

    for (let i = 0; i < args.scrollRounds; i += 1) {
      await page.mouse.wheel(0, 2600);
      await page.waitForTimeout(args.waitMs);
    }

    const cards = await page.evaluate(() => {
      const toAbs = (href) => {
        if (!href) return null;
        if (href.startsWith("http")) return href;
        if (href.startsWith("/")) return `https://www.xiaohongshu.com${href}`;
        return null;
      };
      const out = [];
      const anchors = Array.from(document.querySelectorAll('a[href*="/explore/"], a[href*="/discovery/item/"]'));
      for (const a of anchors) {
        const href = toAbs(a.getAttribute("href"));
        if (!href) continue;
        const card = a.closest("section, article, div") || a.parentElement;
        const text = (card && card.innerText) || a.innerText || "";
        const lines = text.split("\n").map((x) => x.trim()).filter(Boolean);
        const title = lines[0] || "";
        let author = "";
        let likesText = "";
        for (const line of lines) {
          if (!likesText && /^(\d+(\.\d+)?万?|\d+(\.\d+)?k)$/i.test(line)) likesText = line;
          if (!author && /@|作者|发布/.test(line) === false && line.length <= 24 && line !== title) author = line;
        }
        out.push({ url: href, title, author, likes_text: likesText });
      }
      return out;
    });

    const dedup = [];
    const seen = new Set();
    for (const c of cards) {
      if (!c.url || seen.has(c.url)) continue;
      seen.add(c.url);
      dedup.push(c);
      if (dedup.length >= args.maxItems) break;
    }

    const notes = dedup.map((n) => ({
      ...n,
      likes: parseLikes(n.likes_text),
    }));
    const hot = notes.filter((n) => (n.likes || 0) > args.minLikes);

    const result = {
      ok: true,
      keyword: args.keyword,
      min_likes: args.minLikes,
      total_collected: notes.length,
      fetched_at_utc: new Date().toISOString(),
      notes,
      hot_notes: hot,
    };

    fs.writeFileSync(args.output, `${JSON.stringify(result, null, 2)}\n`, "utf-8");
    fs.writeFileSync(args.mdOutput, toMarkdown(result), "utf-8");
    console.log(`Saved JSON: ${path.resolve(args.output)}`);
    console.log(`Saved MD:   ${path.resolve(args.mdOutput)}`);
    console.log(`Collected: ${notes.length}, Hot(>${args.minLikes}): ${hot.length}`);
  } finally {
    await context.close();
    await browser.close();
  }
}

main().catch((e) => {
  console.error(String(e && e.message ? e.message : e));
  process.exit(1);
});
