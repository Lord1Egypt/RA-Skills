#!/usr/bin/env node
// 网页内容批量提取

const args = process.argv.slice(2);
const urls = args.filter(a => !a.startsWith("-"));
if (urls.length === 0) { console.error("No URLs provided"); process.exit(1); }

const apiKey = (process.env.TAVILY_API_KEY ?? "").trim();
const resp = await fetch("https://api.tavily.com/extract", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ api_key: apiKey, urls: urls }),
});

const data = await resp.json();
(data.results ?? []).forEach(r => {
  console.log(`# ${r.url}\n\n${r.raw_content || "(no content)"}\n---\n`);
});