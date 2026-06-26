#!/usr/bin/env node
// ═══════════════════════════════════════════════════════════════════
// Rhetra TaxGuard — Trade Compliance Check
// Called by the SKILL.md before every trade execution
// ═══════════════════════════════════════════════════════════════════

const http = require("http")

function parseArgs(args) {
  const parsed = {}
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--")) {
      const key = args[i].slice(2)
      const val = args[i + 1]
      if (val && !val.startsWith("--")) {
        try { parsed[key] = JSON.parse(val) } catch { parsed[key] = val }
        i++
      } else {
        parsed[key] = true
      }
    }
  }
  return parsed
}

const args = parseArgs(process.argv.slice(2))

if (!args.key || !args.action) {
  console.log("Rhetra TaxGuard — Trade Compliance Check")
  console.log("")
  console.log("Usage: node check-trade.js --key API_KEY --action \"BUY 50 NVDA\" --ticker NVDA [options]")
  console.log("")
  console.log("Required:")
  console.log("  --key              Rhetra API key")
  console.log("  --action           Trade description (e.g. \"BUY 50 NVDA at market\")")
  console.log("")
  console.log("Recommended:")
  console.log("  --ticker           Symbol being traded")
  console.log("  --equity           Current account equity")
  console.log("  --day-trades       Day trades this week")
  console.log("  --exchange         Platform (alpaca, crypto.com, bitget, polymarket)")
  console.log("  --recent-sales     JSON array of recent sales [{ticker,date,type,gainLoss}]")
  console.log("  --positions        JSON array of positions [{ticker,acquiredDate,quantity,costBasis,currentValue}]")
  console.log("")
  console.log("Tax context (improves accuracy):")
  console.log("  --annual-gains     Total realized gains this year")
  console.log("  --annual-losses    Total realized losses this year")
  console.log("  --harvested-losses Total harvested losses this year")
  console.log("  --total-trades     Total trades this year")
  console.log("  --magi             Estimated modified adjusted gross income")
  console.log("  --filing-status    single, married_joint, married_separate, head_of_household")
  console.log("  --cost-basis       Cost basis method (FIFO, LIFO, SPECIFIC_LOT, AVG_COST)")
  console.log("")
  console.log("Guardian mode (opt-in trade blocking):")
  console.log("  --block-wash-sales    Block trades that trigger wash sales")
  console.log("  --block-pdt           Block trades that trigger PDT designation")
  console.log("  --block-short-term    Block short-term sells when long-term is close")
  process.exit(1)
}

const payload = JSON.stringify({
  actorId: args.actor || "trader-agent",
  actorType: "AGENT",
  action: args.action,
  domains: ["SECURITIES_TRADING", "TAX"],
  jurisdiction: "US",
  context: {
    ticker: args.ticker,
    accountEquity: args.equity,
    dayTradesThisWeek: args["day-trades"],
    exchange: args.exchange,
    recentSales: args["recent-sales"],
    currentPositions: args.positions,
    recentPurchases: args["recent-purchases"],
    annualRealizedGains: args["annual-gains"],
    annualRealizedLosses: args["annual-losses"],
    annualHarvestedLosses: args["harvested-losses"],
    totalTradesThisYear: args["total-trades"],
    estimatedMAGI: args.magi,
    filingStatus: args["filing-status"],
    costBasisMethod: args["cost-basis"],
    guardianMode: {
      blockWashSales: args["block-wash-sales"] || false,
      blockPDT: args["block-pdt"] || false,
      blockShortTermSells: args["block-short-term"] || false,
    },
  },
})

const apiHost = args.host || "api.rhetra.io"
const apiPort = args.port || (apiHost === "localhost" ? 3001 : 443)
const protocol = apiHost === "localhost" ? http : require("https")

const options = {
  hostname: apiHost,
  port: apiPort,
  path: "/api/resolve",
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + args.key,
    "Content-Length": Buffer.byteLength(payload),
  },
}

const req = protocol.request(options, (res) => {
  let data = ""
  res.on("data", (chunk) => data += chunk)
  res.on("end", () => {
    try {
      const j = JSON.parse(data)

      console.log("═══ TAXGUARD ═══")
      console.log("")

      if (j.outcome === "BLOCKED") {
        console.log("⛔ TRADE BLOCKED (Guardian Mode)")
        console.log("")
        ;(j.modifications || []).forEach(m => console.log(m))
      } else {
        console.log("✅ TRADE OK — Review disclosures below:")
        console.log("")
        const mods = j.modifications || []
        if (mods.length === 0) {
          console.log("No tax concerns detected for this trade.")
        } else {
          // Separate HIGH priority (deterministic) from corpus-backed
          mods.forEach(m => console.log(m))
        }
      }

      console.log("")
      console.log("Decision ID:", j.decisionId || "N/A")
      console.log("═══════════════")

      // Exit code: 0 = allowed, 1 = blocked, 2 = error
      process.exit(j.outcome === "BLOCKED" ? 1 : 0)
    } catch (err) {
      console.error("TaxGuard error: could not parse response")
      console.error(data.slice(0, 200))
      process.exit(2)
    }
  })
})

req.on("error", (err) => {
  console.log("═══ TAXGUARD ═══")
  console.log("")
  console.log("⚠️  TaxGuard is offline. Trade proceeding without compliance check.")
  console.log("Error:", err.message)
  console.log("═══════════════")
  process.exit(0) // Don't block trades if we're unreachable
})

req.write(payload)
req.end()
