#!/usr/bin/env node
// 高级搜索工具

function usage() {
  console.error(`Usage: search.mjs "query" [-n 5] [--deep] [--topic general|news] [--days 7]`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const query = args[0];
let n = 5;
let searchDepth = "basic";
let topic = "general";
let days = null;

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === "-n") { n = Number.parseInt(args[i + 1] ?? "5", 10); i++; continue; }
  if (a === "--deep") { searchDepth = "advanced"; continue; }
  if (a === "--topic") { topic = args[i + 1] ?? "general"; i++; continue; }
  if (a === "--days") { days = Number.parseInt(args[i + 1] ?? "7", 10); i++; continue; }
}

const apiKey = (process.env.TAVILY_API_KEY ?? "").trim();
if (!apiKey) { console.error("Missing TAVILY_API_KEY"); process.exit(1); }

console.log(`\n🔍 **正在检索关于 "${query}" 的深度数据...**\n`);

const resp = await fetch("https://api.tavily.com/search", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    api_key: apiKey,
    query: query,
    search_depth: searchDepth,
    topic: topic,
    max_results: Math.max(1, Math.min(n, 20)),
    include_answer: true,
  }),
});

const data = await resp.json();
if (data.answer) console.log(`> ✨ **AI 洞察**: ${data.answer}\n---\n`);

(data.results ?? []).forEach(r => {
  console.log(`- **${r.title}** (匹配度: ${(r.score * 100).toFixed(0)}%)`);
  console.log(`  ${r.url}\n  ${r.content.slice(0, 300)}...\n`);
});