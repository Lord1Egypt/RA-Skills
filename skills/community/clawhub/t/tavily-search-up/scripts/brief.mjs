#!/usr/bin/env node

const url = process.argv[2];
if (!url) {
  console.error("请提供一个 URL。");
  process.exit(1);
}

const apiKey = (process.env.TAVILY_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing TAVILY_API_KEY");
  process.exit(1);
}

const resp = await fetch("https://api.tavily.com/extract", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ api_key: apiKey, urls: [url] }),
});

const data = await resp.json();
const content = data.results?.[0]?.raw_content || "";

if (!content) {
  console.log("未提取到有效情报。");
  process.exit(0);
}

console.log(`\n--- 🕵️ 绝密情报简报 ---`);
console.log(`📍 来源: ${url}`);
console.log(`📅 提取时间: ${new Date().toLocaleString()}`);
console.log(`\n### 📝 原始内容摘要 (前 500 字)`);
console.log(content.slice(0, 500) + "...");
console.log(`\n--- ⚠️ 代理提示 ---`);
console.log(`该内容已由 Tavily 优化提取。请根据上述数据执行后续推理任务。`);