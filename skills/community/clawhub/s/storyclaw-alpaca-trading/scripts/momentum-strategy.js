#!/usr/bin/env node

/**
 * 动量轮动策略 - Momentum Rotation Strategy
 *
 * 逻辑：
 * 1. 扫描选股池，计算动量分数（RSI + 均线 + 近期涨幅）
 * 2. 持有排名前 2-3 名的股票
 * 3. 每周/双周轮动一次
 * 4. 单只止损 -8%
 *
 * 适合账户：$1000-5000
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

// 加载配置
const CONFIG_PATH = path.join(__dirname, "..", "config.json");
if (!fs.existsSync(CONFIG_PATH)) {
  console.error("❌ config.json not found");
  process.exit(1);
}
const config = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf8"));

const API_KEY = config.apiKey;
const API_SECRET = config.apiSecret;
const BASE_URL = config.baseUrl || "https://paper-api.alpaca.markets";
const DATA_URL = config.dataUrl || "https://data.alpaca.markets";

// HTTP 请求辅助函数
function request(method, url, data = null) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      port: urlObj.port || 443,
      path: urlObj.pathname + urlObj.search,
      method,
      headers: {
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": API_SECRET,
        "Content-Type": "application/json",
      },
    };

    const req = https.request(options, (res) => {
      let body = "";
      res.on("data", (chunk) => (body += chunk));
      res.on("end", () => {
        try {
          const json = JSON.parse(body);
          if (res.statusCode >= 400) {
            reject(new Error(`API Error [${res.statusCode}]: ${json.message || body}`));
          } else {
            resolve(json);
          }
        } catch (e) {
          resolve(body);
        }
      });
    });

    req.on("error", reject);
    if (data) req.write(JSON.stringify(data));
    req.end();
  });
}

// 延迟函数（避免 API 限流）
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// 选股池 - L 的自选股（2026-02-07）
const STOCK_UNIVERSE = [
  "GOOGL", // 谷歌
  "TSLA", // 特斯拉
  "PLTR", // Palantir
  "AMZN", // 亚马逊
  "AVGO", // 博通
  "FCX", // 麦克莫兰铜金
  "FBTC", // Fidelity Bitcoin ETF
];

// 策略参数（L的自选股优化）
const MAX_POSITIONS = 2; // 最多持仓数（持有前2名）
const POSITION_SIZE = 0.45; // 单只仓位比例（45%，保留10%现金）
const STOP_LOSS = 0.08; // 止损比例（8%）
const MIN_STOCK_PRICE = 50; // 最低股价限制
const MAX_STOCK_PRICE = 400; // 最高股价限制（调高以容纳 AVGO/GOOGL/AMZN）
const RSI_PERIOD = 14;
const MOMENTUM_DAYS = 5; // 动量计算周期

// 计算 RSI
function calculateRSI(bars, period = 14) {
  if (bars.length < period + 1) return 50;

  let gains = 0;
  let losses = 0;

  for (let i = bars.length - period; i < bars.length; i++) {
    const change = bars[i].c - bars[i - 1].c;
    if (change > 0) gains += change;
    else losses -= change;
  }

  const avgGain = gains / period;
  const avgLoss = losses / period;

  if (avgLoss === 0) return 100;
  const rs = avgGain / avgLoss;
  return 100 - 100 / (1 + rs);
}

// 计算均线
function calculateSMA(bars, period) {
  if (bars.length < period) return null;
  const slice = bars.slice(-period);
  const sum = slice.reduce((acc, bar) => acc + bar.c, 0);
  return sum / period;
}

// 获取股票历史数据
async function getBars(symbol, days = 60) {
  const end = new Date();
  const start = new Date(end - days * 24 * 60 * 60 * 1000);

  const url = `${DATA_URL}/v2/stocks/${symbol}/bars?start=${start.toISOString().split("T")[0]}&end=${end.toISOString().split("T")[0]}&timeframe=1Day&feed=iex`;

  try {
    const data = await request("GET", url);
    return data.bars || [];
  } catch (error) {
    console.error(`   ⚠️ ${symbol} 数据获取失败: ${error.message}`);
    return [];
  }
}

// 计算动量分数
async function calculateMomentumScore(symbol) {
  const bars = await getBars(symbol, 60);

  if (bars.length < 30) return null;

  // 计算指标
  const rsi = calculateRSI(bars, RSI_PERIOD);
  const sma20 = calculateSMA(bars, 20);
  const sma50 = calculateSMA(bars, 50);
  const currentPrice = bars[bars.length - 1].c;

  // 计算近期涨幅
  const priceNDaysAgo = bars[bars.length - MOMENTUM_DAYS - 1].c;
  const momentum = ((currentPrice - priceNDaysAgo) / priceNDaysAgo) * 100;

  // 综合评分
  let score = 0;

  // RSI 权重 30%
  if (rsi > 50) score += (rsi - 50) * 0.6;

  // 均线权重 30%
  if (sma20 && sma50 && sma20 > sma50) score += 15;
  if (currentPrice > sma20) score += 15;

  // 动量权重 40%
  score += momentum * 2;

  return {
    symbol,
    score,
    rsi,
    sma20,
    sma50,
    currentPrice,
    momentum,
  };
}

// 扫描所有股票
async function scanStocks() {
  console.log("🔍 开始扫描选股池...\n");

  const results = [];

  for (const symbol of STOCK_UNIVERSE) {
    const score = await calculateMomentumScore(symbol);
    if (score) results.push(score);
    await sleep(300); // 避免 API 限流
  }

  // 排序
  results.sort((a, b) => b.score - a.score);

  console.log("📊 动量排名：");
  console.log("━".repeat(80));
  results.forEach((stock, index) => {
    const emoji = index < MAX_POSITIONS ? "🟢" : "⚪️";
    console.log(
      `${emoji} ${(index + 1).toString().padStart(2)}. ${stock.symbol.padEnd(6)} | 分数: ${stock.score.toFixed(2).padStart(7)} | RSI: ${stock.rsi.toFixed(1).padStart(5)} | 动量: ${stock.momentum.toFixed(2)}%`,
    );
  });
  console.log("━".repeat(80) + "\n");

  return results;
}

// 获取当前持仓
async function getCurrentPositions() {
  const positions = await request("GET", `${BASE_URL}/v2/positions`);
  return positions.map((p) => ({
    symbol: p.symbol,
    qty: parseInt(p.qty),
    entryPrice: parseFloat(p.avg_entry_price),
    currentPrice: parseFloat(p.current_price),
    marketValue: parseFloat(p.market_value),
    unrealizedPL: parseFloat(p.unrealized_pl),
    unrealizedPLPercent: parseFloat(p.unrealized_plpc) * 100,
  }));
}

// 检查止损
async function checkStopLoss(positions) {
  console.log("🛡️ 检查止损...\n");

  for (const position of positions) {
    const lossPercent = position.unrealizedPLPercent;

    if (lossPercent <= -STOP_LOSS * 100) {
      console.log(`🚨 ${position.symbol} 触发止损！亏损 ${lossPercent.toFixed(2)}%`);
      console.log(`   卖出 ${position.qty} 股，止损价 $${position.currentPrice.toFixed(2)}\n`);

      // 执行止损
      await request("POST", `${BASE_URL}/v2/orders`, {
        symbol: position.symbol,
        qty: position.qty,
        side: "sell",
        type: "market",
        time_in_force: "day",
      });

      console.log(`✅ ${position.symbol} 止损订单已提交\n`);
    }
  }
}

// 执行交易
async function executeTrades(rankedStocks, currentPositions) {
  const account = await request("GET", `${BASE_URL}/v2/account`);
  const buyingPower = parseFloat(account.buying_power);
  const equity = parseFloat(account.equity);

  console.log(`💰 账户状态：现金 $${buyingPower.toFixed(2)} | 总资产 $${equity.toFixed(2)}\n`);

  // 找出应该持有的股票（前 N 名）
  const targetStocks = rankedStocks.slice(0, MAX_POSITIONS).map((s) => s.symbol);
  const currentSymbols = currentPositions.map((p) => p.symbol);

  // 卖出不在目标列表中的股票
  for (const position of currentPositions) {
    if (!targetStocks.includes(position.symbol)) {
      console.log(`📤 ${position.symbol} 已不在目标持仓，卖出 ${position.qty} 股`);

      await request("POST", `${BASE_URL}/v2/orders`, {
        symbol: position.symbol,
        qty: position.qty,
        side: "sell",
        type: "market",
        time_in_force: "day",
      });

      console.log(`✅ ${position.symbol} 卖出订单已提交\n`);
      await sleep(1000);
    }
  }

  // 等待卖出订单完成
  await sleep(3000);

  // 重新获取账户信息
  const updatedAccount = await request("GET", `${BASE_URL}/v2/account`);
  const availableCash = parseFloat(updatedAccount.buying_power);

  // 买入目标股票
  for (const stock of rankedStocks.slice(0, MAX_POSITIONS)) {
    if (currentSymbols.includes(stock.symbol)) {
      console.log(`✓ ${stock.symbol} 已持有，跳过\n`);
      continue;
    }

    // 股价过滤（小账户专用）
    if (stock.currentPrice < MIN_STOCK_PRICE || stock.currentPrice > MAX_STOCK_PRICE) {
      console.log(
        `⚠️ ${stock.symbol} 股价 $${stock.currentPrice.toFixed(2)} 不在范围内（$${MIN_STOCK_PRICE}-$${MAX_STOCK_PRICE}），跳过\n`,
      );
      continue;
    }

    // 计算应买入金额
    const targetAmount = equity * POSITION_SIZE;
    const maxBuyAmount = Math.min(
      targetAmount,
      availableCash / (MAX_POSITIONS - currentSymbols.length),
    );

    if (maxBuyAmount < 100) {
      console.log(`⚠️ ${stock.symbol} 可用资金不足（需要 $${targetAmount.toFixed(2)}），跳过\n`);
      continue;
    }

    // 计算股数
    const qty = Math.floor(maxBuyAmount / stock.currentPrice);

    if (qty === 0) {
      console.log(
        `⚠️ ${stock.symbol} 股价太高（$${stock.currentPrice.toFixed(2)}），无法购买，跳过\n`,
      );
      continue;
    }

    console.log(
      `📥 买入 ${stock.symbol}: ${qty} 股 @ $${stock.currentPrice.toFixed(2)} (约 $${(qty * stock.currentPrice).toFixed(2)})`,
    );

    await request("POST", `${BASE_URL}/v2/orders`, {
      symbol: stock.symbol,
      qty: qty,
      side: "buy",
      type: "market",
      time_in_force: "day",
    });

    console.log(`✅ ${stock.symbol} 买入订单已提交\n`);
    await sleep(1000);
  }
}

// 生成每日报告
async function generateReport() {
  const account = await request("GET", `${BASE_URL}/v2/account`);
  const positions = await getCurrentPositions();

  console.log("\n" + "=".repeat(80));
  console.log("📈 每日策略报告");
  console.log("=".repeat(80));

  console.log(`\n💰 账户总览：`);
  console.log(`   总资产：$${parseFloat(account.equity).toFixed(2)}`);
  console.log(`   现金：$${parseFloat(account.cash).toFixed(2)}`);
  console.log(`   持仓市值：$${parseFloat(account.portfolio_value).toFixed(2)}`);

  if (positions.length > 0) {
    console.log(`\n📦 当前持仓：`);
    positions.forEach((p) => {
      const plEmoji = p.unrealizedPL >= 0 ? "📈" : "📉";
      console.log(
        `   ${plEmoji} ${p.symbol}: ${p.qty} 股 | 成本 $${p.entryPrice.toFixed(2)} | 现价 $${p.currentPrice.toFixed(2)} | P&L ${p.unrealizedPLPercent.toFixed(2)}%`,
      );
    });
  } else {
    console.log(`\n📦 当前无持仓`);
  }

  console.log("\n" + "=".repeat(80) + "\n");
}

// 主函数
async function main() {
  try {
    console.log("\n🚀 动量轮动策略启动！\n");
    console.log(`⏰ 时间：${new Date().toLocaleString()}\n`);

    // 1. 扫描股票
    const rankedStocks = await scanStocks();

    // 2. 获取当前持仓
    const currentPositions = await getCurrentPositions();

    // 3. 检查止损
    await checkStopLoss(currentPositions);

    // 4. 执行交易
    await executeTrades(rankedStocks, currentPositions);

    // 5. 生成报告
    await generateReport();

    console.log("✅ 策略执行完成！\n");
  } catch (error) {
    console.error("❌ 策略执行出错：", error);
    process.exit(1);
  }
}

// 运行
main();
