#!/usr/bin/env node
/**
 * 同花顺交易风控计算器
 * 用法：
 *   node risk-calc.mjs --capital 200000 --riskPct 1 --entry 25.8 --stop 24.9 --target 28
 */

function parseArgs(argv) {
  const out = {}
  for (let i = 2; i < argv.length; i += 1) {
    const k = argv[i]
    const v = argv[i + 1]
    if (!k?.startsWith('--')) continue
    out[k.slice(2)] = v
    i += 1
  }
  return out
}

function toNum(v, name) {
  const n = Number(v)
  if (!Number.isFinite(n)) throw new Error(`参数 ${name} 非法: ${v}`)
  return n
}

function round2(n) {
  return Math.round(n * 100) / 100
}

function main() {
  const args = parseArgs(process.argv)
  const capital = toNum(args.capital, 'capital')
  const riskPct = toNum(args.riskPct, 'riskPct')
  const entry = toNum(args.entry, 'entry')
  const stop = toNum(args.stop, 'stop')
  const target = args.target != null ? toNum(args.target, 'target') : null
  const side = (args.side || 'long').toLowerCase()

  if (capital <= 0) throw new Error('capital 必须 > 0')
  if (riskPct <= 0 || riskPct > 100) throw new Error('riskPct 必须在 (0,100] 区间')
  if (entry <= 0 || stop <= 0) throw new Error('entry/stop 必须 > 0')
  if (!['long', 'short'].includes(side)) throw new Error('side 仅支持 long/short')

  const riskAmount = capital * (riskPct / 100)
  const perShareRisk = side === 'long' ? entry - stop : stop - entry
  if (perShareRisk <= 0) {
    throw new Error(`方向 ${side} 下 stop 必须在有效风控区间，当前单股风险 <= 0`)
  }

  const rawShares = Math.floor(riskAmount / perShareRisk)
  const boardLot = args.boardLot != null ? Math.max(1, Math.floor(toNum(args.boardLot, 'boardLot'))) : 100
  const shares = Math.floor(rawShares / boardLot) * boardLot
  const positionCost = shares * entry
  const actualRisk = shares * perShareRisk
  const positionPct = (positionCost / capital) * 100

  const output = {
    inputs: { capital, riskPct, entry, stop, target, side, boardLot },
    result: {
      maxRiskAmount: round2(riskAmount),
      perShareRisk: round2(perShareRisk),
      suggestedShares: shares,
      positionCost: round2(positionCost),
      positionPct: round2(positionPct),
      actualRisk: round2(actualRisk),
    },
  }

  if (target != null) {
    const rewardPerShare = side === 'long' ? target - entry : entry - target
    const rr = rewardPerShare > 0 ? rewardPerShare / perShareRisk : 0
    output.result.rewardPerShare = round2(rewardPerShare)
    output.result.rr = round2(rr)
  }

  process.stdout.write(`${JSON.stringify(output, null, 2)}\n`)
}

try {
  main()
} catch (err) {
  process.stderr.write(`[risk-calc] ${(err && err.message) || String(err)}\n`)
  process.exit(1)
}
