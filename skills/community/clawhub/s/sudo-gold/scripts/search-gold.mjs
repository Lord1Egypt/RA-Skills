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

const QUERY_BY_TYPE = {
  price: "黄金价格 美元/盎司 人民币/克 最新",
  news: "黄金 最新 新闻 央行购金 地缘政治",
  technical: "黄金 技术分析 RSI MACD 支撑位 阻力位",
  fundamental: "黄金 基本面 美联储 利率 美元 美债收益率",
};

// 综合分析
async function analyze() {
  console.log("🥇 黄金投资综合分析报告");
  console.log("📅 " + new Date().toLocaleString('zh-CN'));
  console.log("=".repeat(50));
  
  // 1. 价格概览
  console.log("\n1️⃣ 价格概览");
  console.log("-".repeat(40));
  try {
    const priceData = await searchTavily(QUERY_BY_TYPE.price, 2);
    if (priceData.answer) console.log(priceData.answer.slice(0, 300));
  } catch (e) {
    console.log("获取失败");
  }
  
  // 2. 技术面
  console.log("\n2️⃣ 技术面");
  console.log("-".repeat(40));
  try {
    const techData = await searchTavily(QUERY_BY_TYPE.technical, 2);
    if (techData.answer) console.log(techData.answer.slice(0, 300));
  } catch (e) {
    console.log("获取失败");
  }
  
  // 3. 基本面
  console.log("\n3️⃣ 基本面");
  console.log("-".repeat(40));
  try {
    const fundData = await searchTavily(QUERY_BY_TYPE.fundamental, 2);
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
const isAnalyzeArg = args.includes("--analyze");

if (isAnalyzeArg || args.length === 0) {
  analyze().catch(console.error);
} else {
  const typeIndex = args.indexOf("--type");
  const type = typeIndex >= 0 ? args[typeIndex + 1] : null;
  const allowedTypes = Object.keys(QUERY_BY_TYPE);

  if (!type || !allowedTypes.includes(type) || args.length > 2) {
    console.error("用法: node search-gold.mjs [--analyze] 或 node search-gold.mjs --type price|news|technical|fundamental");
    process.exit(2);
  }

  const query = QUERY_BY_TYPE[type];
  searchTavily(query, 3).then(data => {
    if (data.answer) console.log("## 分析\n" + data.answer + "\n");
    console.log("## 来源（标题）");
    for (const r of (data.results || []).slice(0, 3)) {
      console.log(`- ${r.title}`);
    }
  }).catch(console.error);
}
