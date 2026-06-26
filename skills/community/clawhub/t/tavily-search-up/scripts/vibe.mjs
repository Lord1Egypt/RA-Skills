#!/usr/bin/env node

const query = process.argv.slice(2).join(" ");
if (!query) {
  console.error("请输入要进行情绪分析的话题。");
  process.exit(1);
}

const apiKey = (process.env.TAVILY_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing TAVILY_API_KEY");
  process.exit(1);
}

const resp = await fetch("https://api.tavily.com/search", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    api_key: apiKey,
    query: query,
    search_depth: "basic",
    include_answer: true,
    max_results: 10
  }),
});

const data = await resp.json();
const textToAnalyze = (data.answer + " " + (data.results || []).map(r => r.content).join(" ")).toLowerCase();

const positiveWords = ["breakthrough", "excellent", "growth", "love", "amazing", "success", "future", "positive", "good"];
const negativeWords = ["failed", "controversy", "scam", "expensive", "disaster", "risk", "hate", "negative", "bad"];

let posScore = 0;
let negScore = 0;

positiveWords.forEach(w => { if(textToAnalyze.includes(w)) posScore++ });
negativeWords.forEach(w => { if(textToAnalyze.includes(w)) negScore++ });

let vibe = "😐 中立 (Neutral)";
let emoji = "🌊";

if (posScore > negScore) { vibe = "🔥 极度乐观 (Bullish)"; emoji = "🚀"; }
else if (negScore > posScore) { vibe = "❄️ 充满质疑 (Bearish)"; emoji = "📉"; }

console.log(`## 话题: ${query}`);
console.log(`### 互联网情绪指数: ${vibe} ${emoji}`);
console.log(`> 基于 ${data.results?.length || 0} 条实时搜索结果分析得出。`);
console.log(`\n**AI 的简要总结:**\n${data.answer || "暂无总结"}`);