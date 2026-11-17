#!/usr/bin/env node
// One TikTok slideshow, start to finish: your photos -> slides with the words on them -> a TikTok draft (or a post),
// optionally the same slides to Instagram, Facebook, LinkedIn, Bluesky... No npm install: Node 18+ and its fetch.
//
//   node slideshow.mjs --dir posts/2026-10-24-0900 [--publish --privacy public] [--also instagram,linkedin] [--brand <id>] [--dry]
//
// The folder holds the photos (1.jpg ... 6.jpg, or .png/.webp, sorted by name), slides.json and caption.txt:
//   slides.json  ["hook on slide 1", "slide 2 words", "", "...", "CTA on slide 5", ""]  (one entry per photo; "" = no words)
//   caption.txt  the TikTok caption (hook, short story, at most 5 hashtags)
// Writes result.json next to them (ids, links) and appends a line to ../log.jsonl for the daily review.
// Needs POSTWIRE_API_KEY (Dashboard -> API keys at https://postwire.io). The key is only sent to postwire.io.
import fs from "node:fs";
import path from "node:path";

const API = "https://postwire.io";
const args = process.argv.slice(2);
const flag = (n) => args.includes(`--${n}`);
const opt = (n, d = null) => { const i = args.indexOf(`--${n}`); return i >= 0 && args[i + 1] && !args[i + 1].startsWith("--") ? args[i + 1] : d; };

const dir = opt("dir");
const key = process.env.POSTWIRE_API_KEY;
if (!dir) { console.error("usage: node slideshow.mjs --dir <folder> [--publish --privacy public] [--also instagram,linkedin] [--brand <id>] [--dry]"); process.exit(2); }
if (!key) { console.error("POSTWIRE_API_KEY is not set. Create one at https://postwire.io (Dashboard -> API keys)."); process.exit(2); }

const H = { Authorization: `Bearer ${key}` };
async function call(method, url, body) {
  const r = await fetch(API + url, { method, headers: body ? { ...H, "Content-Type": "application/json" } : H, body: body ? JSON.stringify(body) : undefined });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`${method} ${url} -> ${r.status} ${j.code || ""} ${j.error || ""}`.trim());
  return j;
}
const TYPES = { ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp" };

const photos = fs.readdirSync(dir).filter((f) => TYPES[path.extname(f).toLowerCase()]).sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
const texts = JSON.parse(fs.readFileSync(path.join(dir, "slides.json"), "utf8"));
const caption = fs.readFileSync(path.join(dir, "caption.txt"), "utf8").trim();
if (!photos.length || photos.length > 35) throw new Error(`${photos.length} photos in ${dir}: TikTok takes 1 to 35 (6 is the format that works)`);
if (texts.length !== photos.length) throw new Error(`slides.json has ${texts.length} entries for ${photos.length} photos — one entry per photo ("" for no words)`);

const slides = [];
for (const [i, file] of photos.entries()) {
  const bytes = fs.readFileSync(path.join(dir, file));
  const type = TYPES[path.extname(file).toLowerCase()];
  // 1) upload the photo (the bytes go straight to storage), 2) put the words on it, 1080x1920
  const up = await call("POST", "/api/media/upload-url", { content_type: type, size_bytes: bytes.length });
  const put = await fetch(up.upload_url, { method: "PUT", headers: { "Content-Type": type }, body: bytes });
  if (!put.ok) throw new Error(`upload of ${file} failed: HTTP ${put.status}`);
  const fin = await call("GET", `/api/media/finalize?path=${encodeURIComponent(up.path)}`);
  const slide = await call("POST", "/api/media/card", { text: String(texts[i] || ""), background_url: fin.media_url });
  slides.push({ file, text: texts[i] || "", url: slide.media_url });
  console.log(`slide ${i + 1}/${photos.length} ready: ${file}`);
}
if (flag("dry")) {
  fs.writeFileSync(path.join(dir, "result.json"), JSON.stringify({ dry: true, slides }, null, 2));
  console.log("dry run: slides made, nothing sent. Open the links in result.json to check them.");
  process.exit(0);
}

const publish = flag("publish");
const also = (opt("also", "") || "").split(",").map((s) => s.trim()).filter(Boolean);
const body = {
  platforms: ["tiktok", ...also], text: caption, media: slides.map((s) => ({ url: s.url, type: "image" })),
  options: { tiktok: publish ? { auto_add_music: true } : { as_draft: true } },
  ...(publish ? { privacy: opt("privacy", "public") } : {}),
  ...(opt("brand") ? { brand_id: opt("brand") } : {}),
};
const res = await call("POST", "/api/post", body);
const out = { at: new Date().toISOString(), mode: publish ? "published" : "draft", hook: texts[0], cta: texts.find((t, i) => i > 0 && /\b(app|link|bio|download|try|free)\b/i.test(t || "")) || null,
  caption, slides, results: (res.results || []).map((r) => ({ platform: r.platform, ok: r.ok, id: r.id, url: r.url, error: r.error, notice: r.notice })) };
fs.writeFileSync(path.join(dir, "result.json"), JSON.stringify(out, null, 2));
fs.appendFileSync(path.join(dir, "..", "log.jsonl"), JSON.stringify({ dir: path.basename(dir), at: out.at, mode: out.mode, hook: out.hook, cta: out.cta, results: out.results }) + "\n");
for (const r of out.results) console.log(`${r.platform}: ${r.ok ? "ok" : "FAILED"} ${r.url || r.notice || r.error || ""}`);
if (!publish) console.log("\nNext: open TikTok -> Inbox -> the draft, pick a trending sound, post. Then tell your agent the video link.");
