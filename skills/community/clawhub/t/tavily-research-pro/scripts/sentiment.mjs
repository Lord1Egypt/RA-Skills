#!/usr/bin/env node
// 舆情分析工具 - 透明化处理

const query = process.argv.slice(2).join(" ");
if (!query) { console.error("请输入分析话题。"); process.exit(1); }

const apiKey = (process.env.TAVILY_API_KEY ?? "").trim();
const resp = await fetch("https://api.tavily.com/search", {
  method: "POST",
  headers: { 
    "Content-Type": "application/json",
    "User-Agent": "ClawHub-TavilyResearchPro/1.1.1" 
  },
  body: JSON.stringify({ api_key: apiKey, query: query, include_answer: true, max_results: 10 }),
});

const data = await resp.json();
const text = (data.answer + " " + (data.results || []).map(r => r.content).join(" ")).toLowerCase();

const pos = ["breakthrough", "excellent", "growth", "success", "future", "positive", "good"];
const neg = ["failed", "controversy", "scam", "risk", "decline", "negative", "bad"];

let score = 0;
pos.forEach(w => { if(text.includes(w)) score++ });
neg.forEach(w => { if(text.includes(w)) score-- });

let label = "😐 中立 (Neutral)";
if (score > 0) label = "📈 积极/看好 (Bullish)";
else if (score < 0) label = "📉 审慎/看空 (Bearish)";

console.log(`## 话题调研: ${query}`);
console.log(`### 舆情指数: ${label}`);
console.log(`\n**分析总结 (基于公开信息):**\n${data.answer || "暂无数据"}`);