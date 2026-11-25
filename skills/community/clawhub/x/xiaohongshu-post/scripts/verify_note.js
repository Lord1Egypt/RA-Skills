#!/usr/bin/env node
/**
 * verify_note.js — 取刚发布笔记的 id / xsec_token / 短链，并用**无痕上下文**验证公开可见
 *
 * 为什么要无痕上下文：小红书笔记页是客户端渲染，SSR HTML 里没有笔记内容，
 * curl 永远验不出公开可见性。必须开一个全新（未登录）context 打开链接，
 * 断言 document.title 含笔记标题、正文文本命中。
 *
 * 用法:
 *   node verify_note.js [--port 9222] [--expect "标题前几个字"] [--json]
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

function loadPlaywright() {
  for (const m of ["playwright", "playwright-core"]) {
    try { return require(m); } catch (_) {}
  }
  const root = execSync("npm root -g", { encoding: "utf8" }).trim();
  return require(path.join(root, "@playwright", "cli", "node_modules", "playwright-core"));
}

const args = { port: 9222 };
for (let i = 2; i < process.argv.length; i++) {
  if (process.argv[i] === "--port") { args.port = parseInt(process.argv[++i], 10); }
  else if (process.argv[i] === "--expect") { args.expect = process.argv[++i]; }
  else if (process.argv[i] === "--json") { args.json = true; }
}

(async () => {
  const { chromium } = loadPlaywright();
  const browser = await chromium.connectOverCDP("http://127.0.0.1:" + args.port);
  const ctx = browser.contexts()[0];
  const page = ctx.pages()[0] || (await ctx.newPage());

  // 1) 笔记元数据
  //    ⚠️ 该接口带签名头（x-s / x-t / x-s-common），**自己 fetch 会 406**。
  //    正确做法：拦截页面自己发出的请求，读取它的响应体。
  if (!/note-manager/.test(page.url())) {
    await page.goto("https://creator.rednote.com/new/note-manager",
      { waitUntil: "domcontentloaded", timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(2500);
  }
  let noteBody = null;
  const onResp = async (r) => {
    if (!/note\/user\/posted/.test(r.url())) return;
    try { noteBody = await r.text(); } catch (_) {}
  };
  page.on("response", onResp);
  await page.reload({ waitUntil: "domcontentloaded", timeout: 30000 }).catch(() => {});
  for (let i = 0; i < 20 && !noteBody; i++) await page.waitForTimeout(500);
  page.off("response", onResp);

  const note = noteBody ? (() => {
    const j = JSON.parse(noteBody);
    const n = (j.data && j.data.notes && j.data.notes[0]) || null;
    if (!n) return null;
    return {
      id: n.id, title: n.display_title, tab_status: n.tab_status,
      xsec_token: n.xsec_token, xsec_source: n.xsec_source,
      visible_time: n.visible_time, images: (n.images_list || []).length
    };
  })() : null;
  if (!note) { console.error("未取到笔记数据（是否已登录创作中心？）"); process.exit(2); }

  note.publicUrl = "https://www.xiaohongshu.com/explore/" + note.id +
    "?xsec_token=" + encodeURIComponent(note.xsec_token) +
    "&xsec_source=" + (note.xsec_source || "pc_creatormng");
  note.statusText = { 0: "已发布", 1: "审核中", 2: "未通过" }[note.tab_status] || ("tab_status=" + note.tab_status);

  // 2) 短链（需 www 域有登录态；note_id 必须用 API 给的 id，不能从当前 URL 猜）
  try {
    const key = await page.evaluate(async (nid) => {
      const r = await fetch("https://edith.xiaohongshu.com/api/sns/web/share/code", {
        method: "POST", credentials: "include",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ note_id: nid })
      });
      const j = await r.json();
      return j && j.data ? j.data : null;
    }, note.id);
    if (key) note.shortUrl = "https://xhslink.com/" + key;
  } catch (_) { note.shortUrl = null; }

  // 3) 无痕上下文验证公开可见
  const anon = await browser.newContext();
  try {
    const p2 = await anon.newPage();
    await p2.goto(note.publicUrl, { waitUntil: "domcontentloaded", timeout: 30000 });
    await p2.waitForTimeout(4000);
    note.public = await p2.evaluate(() => ({
      finalUrl: location.href, title: document.title,
      bodyHit: document.body.innerText.slice(0, 4000)
    }));
    note.publicVisible = !/\/404/.test(note.public.finalUrl) &&
      (!args.expect || note.public.bodyHit.includes(args.expect));
  } finally {
    await anon.close();
  }

  if (args.json) { console.log(JSON.stringify(note, null, 2)); }
  else {
    console.log("标题      :", note.title);
    console.log("状态      :", note.statusText);
    console.log("图片数    :", note.images);
    console.log("笔记 ID   :", note.id);
    console.log("公开链接  :", note.publicUrl);
    if (note.shortUrl) console.log("短链      :", note.shortUrl);
    console.log("公开可见  :", note.publicVisible ? "✅ 是" : "❌ 否");
    if (!note.publicVisible) console.log("  实际标题:", note.public.title, "| 落地:", note.public.finalUrl);
  }
  await browser.close().catch(() => {});
  process.exit(note.publicVisible ? 0 : 3);
})().catch(e => { console.error("失败:", e && e.stack || e); process.exit(1); });
