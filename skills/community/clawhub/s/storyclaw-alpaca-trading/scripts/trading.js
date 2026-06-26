#!/usr/bin/env node
/**
 * Alpaca Trading Bot
 * US stock & crypto trading via Alpaca API
 *
 * Commands:
 *   quote <symbol>              - Get real-time quote (stock or crypto)
 *   buy <symbol> <qty>          - Buy by quantity (shares or coins)
 *   buy-amount <symbol> <$>     - Buy by dollar amount
 *   sell <symbol> <qty>         - Sell by quantity
 *   sell-all <symbol>           - Sell entire position
 *   positions                   - Show current positions
 *   account                     - Show account info
 *   history                     - Show order history
 *   bars <symbol> [days]        - Get price history (OHLCV)
 *   rsi <symbol> [period]       - Calculate RSI
 *   strategy-rsi <symbol>       - Run RSI mean reversion strategy
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

// Load user-specific config
const { loadUserConfig } = require("./config-loader");
const { config } = loadUserConfig();

const API_KEY = config.apiKey;
const API_SECRET = config.apiSecret;
const BASE_URL = config.baseUrl || "https://paper-api.alpaca.markets";
const DATA_URL = config.dataUrl || "https://data.alpaca.markets";

// Crypto symbols use '/' format for Alpaca API
function isCrypto(symbol) {
  const cryptos = [
    "BTC",
    "ETH",
    "SOL",
    "DOGE",
    "AVAX",
    "LINK",
    "DOT",
    "MATIC",
    "ADA",
    "XRP",
    "LTC",
    "UNI",
    "AAVE",
    "SHIB",
    "PEPE",
  ];
  const base = symbol.replace("/USD", "").replace("USD", "").toUpperCase();
  return cryptos.includes(base);
}

function normalizeSymbol(symbol) {
  symbol = symbol.toUpperCase();
  if (isCrypto(symbol) && !symbol.includes("/")) {
    return symbol.replace("USD", "") + "/USD";
  }
  return symbol;
}

function displaySymbol(symbol) {
  return symbol.replace("/", "");
}

// HTTP request helper
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

// Commands
const commands = {
  // Check if configured
  check() {
    console.log("✅ Alpaca配置检查:");
    console.log(`  API Key: ${API_KEY ? "已配置" : "❌ 未配置"}`);
    console.log(`  API Secret: ${API_SECRET ? "已配置" : "❌ 未配置"}`);
    console.log(`  Base URL: ${BASE_URL}`);
    console.log(`  User: ${config.userId || "unknown"}`);
    if (!API_KEY || !API_SECRET) {
      console.log("\n⚠️ 请先配置 Alpaca API keys:");
      console.log(
        `   cp config.example.json credentials/${process.env.USER_ID || "YOUR_USER_ID"}.json`,
      );
    }
    return { configured: !!API_KEY && !!API_SECRET };
  },

  // Get account info
  async account() {
    const acc = await request("GET", `${BASE_URL}/v2/account`);
    console.log("💰 Account Summary:");
    console.log(`  Cash: $${parseFloat(acc.cash).toFixed(2)}`);
    console.log(`  Portfolio Value: $${parseFloat(acc.portfolio_value).toFixed(2)}`);
    console.log(`  Buying Power: $${parseFloat(acc.buying_power).toFixed(2)}`);
    console.log(`  Equity: $${parseFloat(acc.equity).toFixed(2)}`);
    return acc;
  },

  // Get real-time quote (stock or crypto)
  async quote(symbol) {
    symbol = normalizeSymbol(symbol);
    const crypto = isCrypto(symbol);

    if (crypto) {
      const base = symbol.split("/")[0];
      const quote = await request(
        "GET",
        `${DATA_URL}/v1beta3/crypto/us/latest/quotes?symbols=${symbol}`,
      );
      const q = quote.quotes[symbol];
      console.log(`📊 ${symbol} Quote (Crypto):`);
      console.log(`  Bid: $${q.bp}`);
      console.log(`  Ask: $${q.ap}`);
      console.log(`  Mid: $${((q.ap + q.bp) / 2).toFixed(2)}`);
      console.log(`  Time: ${new Date(q.t).toLocaleString()}`);
      return q;
    } else {
      const quote = await request("GET", `${DATA_URL}/v2/stocks/${symbol}/quotes/latest?feed=iex`);
      const q = quote.quote;
      console.log(`📊 ${symbol} Quote:`);
      console.log(`  Bid: $${q.bp} x ${q.bs}`);
      console.log(`  Ask: $${q.ap} x ${q.as}`);
      console.log(`  Mid: $${((q.ap + q.bp) / 2).toFixed(2)}`);
      console.log(`  Time: ${new Date(q.t).toLocaleString()}`);
      return q;
    }
  },

  // Buy by quantity
  async buy(symbol, qty) {
    symbol = normalizeSymbol(symbol);
    const crypto = isCrypto(symbol);
    qty = crypto ? parseFloat(qty) : parseInt(qty);

    console.log(`🛒 Buying ${qty} ${crypto ? "units" : "shares"} of ${symbol}...`);

    const order = await request("POST", `${BASE_URL}/v2/orders`, {
      symbol,
      qty: String(qty),
      side: "buy",
      type: "market",
      time_in_force: crypto ? "gtc" : "day",
    });

    console.log(`✅ Order submitted: ${order.id}`);
    console.log(`   Status: ${order.status}`);
    return order;
  },

  // Buy by dollar amount
  async "buy-amount"(symbol, amount) {
    symbol = normalizeSymbol(symbol);
    const crypto = isCrypto(symbol);
    amount = parseFloat(amount);

    console.log(`🛒 Buying $${amount.toFixed(2)} of ${symbol}...`);

    const order = await request("POST", `${BASE_URL}/v2/orders`, {
      symbol,
      notional: String(amount),
      side: "buy",
      type: "market",
      time_in_force: crypto ? "gtc" : "day",
    });

    console.log(`✅ Order submitted: ${order.id}`);
    console.log(`   Status: ${order.status}`);
    return order;
  },

  // Sell by quantity
  async sell(symbol, qty) {
    symbol = normalizeSymbol(symbol);
    const crypto = isCrypto(symbol);
    qty = crypto ? parseFloat(qty) : parseInt(qty);

    console.log(`💸 Selling ${qty} ${crypto ? "units" : "shares"} of ${symbol}...`);

    const order = await request("POST", `${BASE_URL}/v2/orders`, {
      symbol,
      qty: String(qty),
      side: "sell",
      type: "market",
      time_in_force: crypto ? "gtc" : "day",
    });

    console.log(`✅ Order submitted: ${order.id}`);
    console.log(`   Status: ${order.status}`);
    return order;
  },

  // Sell entire position
  async "sell-all"(symbol) {
    symbol = normalizeSymbol(symbol);
    const displaySym = symbol.replace("/", "");

    // Find position
    const positions = await request("GET", `${BASE_URL}/v2/positions`);
    const pos = positions.find((p) => p.symbol === displaySym || p.symbol === symbol);

    if (!pos) {
      console.log(`❌ No position in ${symbol}`);
      return null;
    }

    console.log(
      `💸 Selling all ${pos.qty} of ${symbol} (Value: $${parseFloat(pos.market_value).toFixed(2)})...`,
    );

    const order = await request("POST", `${BASE_URL}/v2/orders`, {
      symbol,
      qty: pos.qty,
      side: "sell",
      type: "market",
      time_in_force: isCrypto(symbol) ? "gtc" : "day",
    });

    console.log(`✅ Order submitted: ${order.id}`);
    console.log(`   Status: ${order.status}`);
    return order;
  },

  // Show positions
  async positions() {
    const positions = await request("GET", `${BASE_URL}/v2/positions`);

    if (positions.length === 0) {
      console.log("📦 No positions");
      return [];
    }

    console.log("📦 Current Positions:");
    let totalValue = 0;
    for (const pos of positions) {
      const value = parseFloat(pos.market_value);
      const pnl = parseFloat(pos.unrealized_pl);
      const pnlPct = parseFloat(pos.unrealized_plpc) * 100;
      totalValue += value;

      const isCryptoPos = pos.asset_class === "crypto";
      const qtyDisplay = isCryptoPos ? parseFloat(pos.qty).toFixed(6) : pos.qty;
      const label = isCryptoPos ? "units" : "shares";

      console.log(`  ${pos.symbol}: ${qtyDisplay} ${label}`);
      console.log(`    Value: $${value.toFixed(2)}`);
      console.log(`    P&L: $${pnl.toFixed(2)} (${pnlPct.toFixed(2)}%)`);
    }
    console.log(`  Total Value: $${totalValue.toFixed(2)}`);
    return positions;
  },

  // Order history
  async history() {
    const orders = await request("GET", `${BASE_URL}/v2/orders?status=all&limit=10`);

    console.log("📜 Recent Orders:");
    for (const order of orders) {
      const qty = order.qty || `$${order.notional}`;
      console.log(
        `  [${order.created_at.split("T")[0]}] ${order.side.toUpperCase()} ${qty} ${order.symbol}`,
      );
      console.log(`    Status: ${order.status}, Type: ${order.type}`);
      if (order.filled_avg_price) {
        console.log(`    Filled: $${parseFloat(order.filled_avg_price).toFixed(2)}`);
      }
    }
    return orders;
  },

  // Get price bars (OHLCV)
  async bars(symbol, days = 30) {
    symbol = normalizeSymbol(symbol);
    const crypto = isCrypto(symbol);
    const end = new Date();
    const start = new Date(end - days * 24 * 60 * 60 * 1000);

    let url;
    if (crypto) {
      url = `${DATA_URL}/v1beta3/crypto/us/bars?symbols=${symbol}&start=${start.toISOString().split("T")[0]}&end=${end.toISOString().split("T")[0]}&timeframe=1Day`;
    } else {
      url = `${DATA_URL}/v2/stocks/${symbol}/bars?start=${start.toISOString().split("T")[0]}&end=${end.toISOString().split("T")[0]}&timeframe=1Day&feed=iex`;
    }

    const data = await request("GET", url);
    const bars = crypto ? data.bars[symbol] || [] : data.bars || [];

    console.log(`📈 ${symbol} - Last ${Math.min(days, bars.length)} days:`);
    bars.slice(-10).forEach((bar) => {
      console.log(
        `  ${bar.t.split("T")[0]}: O:${bar.o} H:${bar.h} L:${bar.l} C:${bar.c} V:${bar.v}`,
      );
    });

    return bars;
  },

  // Calculate RSI
  async rsi(symbol, period = 14) {
    const bars = await this.bars(symbol, period * 2);
    const closes = bars.map((b) => b.c);

    let gains = 0,
      losses = 0;
    for (let i = 1; i <= period; i++) {
      const change = closes[i] - closes[i - 1];
      if (change > 0) gains += change;
      else losses += Math.abs(change);
    }

    const avgGain = gains / period;
    const avgLoss = losses / period;
    const rs = avgGain / avgLoss;
    const rsi = 100 - 100 / (1 + rs);

    console.log(`📊 ${symbol} RSI(${period}): ${rsi.toFixed(2)}`);
    if (rsi < 30) console.log("   🟢 OVERSOLD - Potential BUY");
    else if (rsi > 70) console.log("   🔴 OVERBOUGHT - Potential SELL");
    else console.log("   ⚪ NEUTRAL");

    return rsi;
  },

  // Portfolio equity history
  async "portfolio-history"(period = "1W", timeframe = "1D") {
    const validPeriods = ["1D", "1W", "1M", "3M", "1A"];
    const validTimeframes = { "1D": "1H", "1W": "1D", "1M": "1D", "3M": "1D", "1A": "1D" };
    period = period.toUpperCase();
    if (!validPeriods.includes(period)) period = "1W";
    timeframe = validTimeframes[period];

    const data = await request(
      "GET",
      `${BASE_URL}/v2/account/portfolio/history?period=${period}&timeframe=${timeframe}`,
    );
    const ts = data.timestamp || [];
    const equity = data.equity || [];
    const pl = data.profit_loss || [];
    const plp = data.profit_loss_pct || [];

    // Filter out zero-equity points (days before account had value)
    const points = ts
      .map((t, i) => ({ t, equity: equity[i], pl: pl[i], plp: plp[i] }))
      .filter((p) => p.equity > 0);

    if (points.length === 0) {
      console.log("📊 No portfolio history available");
      return data;
    }

    const first = points[0].equity;
    const last = points[points.length - 1].equity;
    const totalPL = last - first;
    const totalPLPct = (totalPL / first) * 100;

    const totalSign = totalPL >= 0 ? "+" : "";
    const totalArrow = totalPL >= 0 ? "📈" : "📉";

    console.log(
      `\n${totalArrow} Portfolio History (${period})  ${totalSign}$${totalPL.toFixed(0)}  (${totalSign}${totalPLPct.toFixed(2)}%)`,
    );
    console.log(`   Now: $${last.toLocaleString("en-US", { maximumFractionDigits: 2 })}`);
    console.log();

    const dateFormat =
      period === "1D"
        ? (t) => new Date(t * 1000).toISOString().slice(11, 16)
        : (t) => new Date(t * 1000).toISOString().slice(5, 10);
    points.forEach((p) => {
      const arrow = p.pl >= 0 ? "▲" : "▼";
      const sign = p.pl >= 0 ? "+" : "-";
      const eq = `$${p.equity.toLocaleString("en-US", { maximumFractionDigits: 0 })}`;
      const change = `${sign}$${Math.abs(p.pl).toFixed(0)}`;
      const pctSign = p.plp >= 0 ? "+" : "";
      console.log(
        `  ${dateFormat(p.t)}  ${eq.padStart(10)}  ${arrow} ${change.padStart(8)}  (${pctSign}${(p.plp * 100).toFixed(2)}%)`,
      );
    });

    return data;
  },

  // RSI mean reversion strategy
  async "strategy-rsi"(symbol, qty = 1) {
    symbol = normalizeSymbol(symbol);
    console.log(`🤖 Running RSI Strategy for ${symbol}...`);

    const rsi = await this.rsi(symbol);
    const positions = await request("GET", `${BASE_URL}/v2/positions`);
    const displaySym = symbol.replace("/", "");
    const hasPosition = positions.some((p) => p.symbol === displaySym || p.symbol === symbol);

    if (rsi < 30 && !hasPosition) {
      console.log("✅ RSI < 30 and no position → BUY signal");
      return await this.buy(symbol, qty);
    } else if (rsi > 70 && hasPosition) {
      console.log("✅ RSI > 70 and has position → SELL signal");
      return await this["sell-all"](symbol);
    } else {
      console.log("⏸  No action: RSI in neutral zone or position mismatch");
      return null;
    }
  },
};

// Main
(async () => {
  const [cmd, ...args] = process.argv.slice(2);

  if (!cmd || !commands[cmd]) {
    console.log("Usage: node trading.js <command> [args]");
    console.log("\nCommands:");
    console.log("  check                       - Check configuration");
    console.log("  buy <symbol> <qty>          - Buy by quantity");
    console.log("  buy-amount <symbol> <$>     - Buy by dollar amount");
    console.log("  sell <symbol> <qty>         - Sell by quantity");
    console.log("  sell-all <symbol>           - Sell entire position");
    console.log("  positions                   - Show positions");
    console.log("  account                     - Show account");
    console.log("  history                     - Order history");
    console.log("  portfolio-history [period]  - Account equity curve (1D/1W/1M/3M/1A)");
    console.log("  bars <symbol> [days]        - Price history");
    console.log("  rsi <symbol> [period]       - Calculate RSI");
    console.log("  strategy-rsi <symbol>       - Run RSI strategy");
    console.log("\nCrypto symbols: BTC, ETH, SOL, DOGE, etc.");
    console.log("  e.g., node trading.js quote BTC");
    console.log("  e.g., node trading.js buy-amount BTC 1000");
    process.exit(1);
  }

  try {
    await commands[cmd](...args);
  } catch (err) {
    console.error("❌ Error:", err.message);
    process.exit(1);
  }
})();
