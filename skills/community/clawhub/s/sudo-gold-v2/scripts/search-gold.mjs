#!/usr/bin/env node

/**
 * Gold Analysis Script
 * 黄金投资分析工具
 */

const apiKey = (process.env.TAVILY_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing TAVILY_API_KEY");
  process.exit(1);
}

async function searchTavily(q, n = 3) {
  const resp = await fetch("https://api.tavily.com/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      api_key: apiKey,
      query: q,
      search_depth: "basic",
      max_results: n,
      include_answer: true,
    }),
  });
  return resp.json();
}

// 综合分析
async function analyze() {
  console.log("🥇 黄金投资综合分析报告");
  console.log("📅 " + new Date().toLocaleString('zh-CN'));
  console.log("=".repeat(50));
  
  // 1. 价格概览
  console.log("\n1️⃣ 价格概览");
  console.log("-".repeat(40));
  try {
    const priceData = await searchTavily("黄金价格 美元 盎司 2026年3月 最新", 2);
    if (priceData.answer) console.log(priceData.answer.slice(0, 300));
  } catch (e) {
    console.log("获取失败");
  }
  
  // 2. 技术面
  console.log("\n2️⃣ 技术面");
  console.log("-".repeat(40));
  try {
    const techData = await searchTavily("黄金技术分析 RSI MACD 金叉死叉 支撑位 阻力位", 2);
    if (techData.answer) console.log(techData.answer.slice(0, 300));
  } catch (e) {
    console.log("获取失败");
  }
  
  // 3. 基本面
  console.log("\n3️⃣ 基本面");
  console.log("-".repeat(40));
  try {
    const fundData = await searchTavily("黄金基本面 央行购金 地缘政治 美联储政策 2026", 2);
    if (fundData.answer) console.log(fundData.answer.slice(0, 300));
  } catch (e) {
    console.log("获取失败");
  }
  
  // 4. 风险提示
  console.log("\n4️⃣ 风险提示");
  console.log("-".repeat(40));
  console.log("• 金价波动较大，注意仓位控制");
  console.log("• 本分析仅供参考，不构成投资建议");
  console.log("• 投资有风险，入市需谨慎");
  console.log("• 建议根据自身风险承受能力制定策略");
  
  console.log("\n" + "=".repeat(50));
  console.log("📌 免责声明: 本报告仅供学习交流，不构成任何投资建议");
}

// 主入口
const args = process.argv.slice(2);

// 自动触发综合分析的关键字
const analyzeKeywords = ["黄金分析", "分析黄金", "黄金走势", "黄金投资", "黄金价格分析", "黄金能买吗", "黄金怎么样"];
const isAnalyzeArg = args.includes("--analyze");
const hasAnalyzeKeyword = args.length > 0 && args.some(a => analyzeKeywords.some(k => a.includes(k)));

if (isAnalyzeArg || hasAnalyzeKeyword || args.length === 0) {
  analyze().catch(console.error);
} else {
  const query = args[0];
  searchTavily(query, 5).then(data => {
    if (data.answer) console.log("## 分析\n" + data.answer + "\n");
    console.log("## 来源");
    for (const r of (data.results || []).slice(0, 5)) {
      console.log(`- ${r.title}`);
      console.log(`  ${r.url}`);
    }
  }).catch(console.error);
}
