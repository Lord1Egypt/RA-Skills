#!/usr/bin/env node
/**
 * publish_note.js — 在已登录的小红书创作中心发布图文笔记
 *
 * 通过 CDP 连到已启动的 Chrome（见 bootstrap_browser.sh），完成：
 *   切「上传图文」→ 传图 → 填标题 → 填正文 → 插入真话题标签 → 截图
 * 默认**不点发布**（--publish 才点），符合"发布前给用户看草稿"的纪律。
 *
 * 用法:
 *   node publish_note.js --title "标题" --body-file body.txt \
 *        --images cover.png,a.png,b.png --topics "WorkBuddy,1024程序员节" \
 *        [--publish] [--out draft.png] [--port 9222]
 *
 * 依赖: playwright / playwright-core（会自动找全局 @playwright/cli 自带的 playwright-core）
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

function loadPlaywright() {
  const tries = ["playwright", "playwright-core"];
  for (const m of tries) {
    try { return require(m); } catch (_) {}
  }
  try {
    const root = execSync("npm root -g", { encoding: "utf8" }).trim();
    const p = path.join(root, "@playwright", "cli", "node_modules", "playwright-core");
    return require(p);
  } catch (_) {}
  throw new Error(
    "找不到 playwright/playwright-core。\n" +
    "修复: npm install -g @playwright/cli@latest  （或 npm install -g playwright）"
  );
}

function parseArgs(argv) {
  const a = { port: 9222, topics: [], images: [] };
  for (let i = 2; i < argv.length; i++) {
    const k = argv[i];
    const v = argv[i + 1];
    if (k === "--title") { a.title = v; i++; }
    else if (k === "--body-file") { a.bodyFile = v; i++; }
    else if (k === "--body") { a.body = v; i++; }
    else if (k === "--images") { a.images = v.split(",").map(s => s.trim()).filter(Boolean); i++; }
    else if (k === "--topics") { a.topics = v.split(",").map(s => s.trim()).filter(Boolean); i++; }
    else if (k === "--out") { a.out = v; i++; }
    else if (k === "--port") { a.port = parseInt(v, 10); i++; }
    else if (k === "--publish") { a.publish = true; }
  }
  return a;
}

const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/** 在编辑器内插入真话题标签：输入 #关键词 → 等 tippy 建议框 → 点精确匹配项 */
async function insertTopic(page, keyword) {
  const ed = page.locator("div[contenteditable=true]").first();
  await ed.click();
  await page.keyboard.press("Control+End");
  await page.keyboard.type("#" + keyword, { delay: 120 });
  await page.waitForTimeout(3000);

  const exact = page.locator(".tippy-box *")
    .filter({ hasText: new RegExp("^#" + esc(keyword) + "$") }).first();
  if (await exact.count()) {
    await exact.click({ timeout: 8000 });
  } else {
    // 兜底：点第一条以 #关键词 开头的建议
    const loose = page.locator(".tippy-box *")
      .filter({ hasText: new RegExp("^#" + esc(keyword)) }).first();
    if (!(await loose.count())) throw new Error("话题建议未弹出: " + keyword);
    await loose.click({ timeout: 8000 });
  }
  await page.waitForTimeout(800);
  // 校验：必须是 data-topic 节点（纯文本 #xxx 不算）
  const name = await page.evaluate(() => {
    const ed = document.querySelector("div[contenteditable=true]");
    const chips = Array.from(ed.querySelectorAll("a.tiptap-topic"));
    return chips.length ? JSON.parse(chips[chips.length - 1].getAttribute("data-topic")).name : null;
  });
  if (!name) throw new Error("话题未转成真标签: " + keyword);
  return name;
}

(async () => {
  const args = parseArgs(process.argv);
  if (!args.title) { console.error("缺少 --title"); process.exit(2); }
  if (!args.images.length) { console.error("缺少 --images"); process.exit(2); }

  const bodyText = args.bodyFile
    ? fs.readFileSync(args.bodyFile, "utf8")
    : (args.body || "");
  const images = args.images.map(p => path.resolve(p));
  for (const p of images) if (!fs.existsSync(p)) { console.error("图片不存在: " + p); process.exit(2); }

  const { chromium } = loadPlaywright();
  const browser = await chromium.connectOverCDP("http://127.0.0.1:" + args.port);
  const ctx = browser.contexts()[0];
  const page = ctx.pages()[0] || (await ctx.newPage());

  console.log("当前页面:", page.url());
  // ⛔ 必须在发布页；笔记管理页（/new/note-manager）没有 file input
  if (!/\/publish\/publish/.test(page.url())) {
    await page.goto("https://creator.rednote.com/publish/publish",
      { waitUntil: "domcontentloaded", timeout: 30000 });
    await page.waitForTimeout(3000);
  }
  // 切「上传图文」
  // ⚠️ DOM 里有**两份**同名 tab：一份 aria-hidden="true" 的无障碍镜像（尺寸相同、盖在真标签上面）
  //    → 普通 click 的命中检测永远被镜像挡住（Playwright 报 "intercepts pointer events"）。
  //    对非 aria-hidden 的真元素直接派发 click 才稳。
  const switched = await page.evaluate(() => {
    const tabs = Array.from(document.querySelectorAll("div.creator-tab"));
    const real = tabs.filter(e =>
      (e.textContent || "").trim() === "上传图文" && e.getAttribute("aria-hidden") === null);
    if (!real.length) return false;
    real[real.length - 1].click();
    return true;
  });
  if (!switched) throw new Error("找不到「上传图文」标签");
  await page.waitForTimeout(2500);

  // 传图（第一张为封面）
  await page.locator("input[type=file]").first().setInputFiles(images);
  await page.waitForTimeout(4000);

  // 标题
  const titleInput = page.locator('input[placeholder*="标题"]').first();
  await titleInput.scrollIntoViewIfNeeded();
  await titleInput.fill(args.title);
  await page.waitForTimeout(500);

  // 正文
  const ed = page.locator("div[contenteditable=true]").first();
  await ed.click();
  await page.keyboard.insertText(bodyText);
  await page.waitForTimeout(1200);

  // 话题
  const inserted = [];
  for (const t of args.topics) inserted.push(await insertTopic(page, t));

  // 草稿快照（顶部 + 正文两张）
  await page.screenshot({ path: args.out || "draft_top.png" });
  await ed.scrollIntoViewIfNeeded();
  await page.waitForTimeout(500);
  await page.screenshot({ path: (args.out || "draft_top.png").replace(/\.png$/, "_body.png") });

  const state = await page.evaluate(() => {
    const ed = document.querySelector("div[contenteditable=true]");
    const title = document.querySelector('input[placeholder*="标题"]');
    // 缩略图尺寸约 200×267，据此数已上传图片（不是数 file input 数量）
    const thumbs = Array.from(document.querySelectorAll("img")).filter(i => {
      const r = i.getBoundingClientRect();
      return r.width > 150 && r.width < 260 && r.height > 180 && r.height < 320;
    }).length;
    return {
      title: title ? title.value : null,
      titleLen: title ? title.value.length : 0,
      bodyLen: ed ? ed.innerText.length : 0,
      topics: ed ? Array.from(ed.querySelectorAll("a.tiptap-topic"))
        .map(c => JSON.parse(c.getAttribute("data-topic")).name) : [],
      imageThumbs: thumbs
    };
  });

  console.log("草稿状态:", JSON.stringify(state));
  console.log("话题已插入:", inserted.join(", "));

  if (args.publish) {
    const btn = page.getByText("发布", { exact: true }).last();
    await btn.click();
    await page.waitForTimeout(5000);
    const url = page.url();
    console.log("发布后 URL:", url);
    if (!/published=true/.test(url)) {
      console.error("⚠️ 未检测到 published=true，请人工确认是否发布成功");
      process.exit(3);
    }
    console.log("✅ 已发布");
  } else {
    console.log("⏸ 未发布（加 --publish 才点发布按钮）");
  }
  await browser.close().catch(() => {});
})().catch(e => { console.error("失败:", e && e.stack || e); process.exit(1); });
