#!/usr/bin/env node
/**
 * 同花顺全流程编排器（Windows + Node 文本脚本）
 *
 * 示例：
 * node run-all.mjs --mode short --batch kline
 * node run-all.mjs --mode swing --watchlist ./watchlist.txt
 * node run-all.mjs --mode short --symbols 600519,300750 --batch f10
 * node run-all.mjs --mode short --capital 200000 --riskPct 1 --entry 25.8 --stop 24.9 --target 28
 * node run-all.mjs --plan-file ./trading-plan.sample.json
 */

import fs from 'node:fs'
import path from 'node:path'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

function parseArgs(argv) {
  const out = {}
  for (let i = 2; i < argv.length; i += 1) {
    const key = argv[i]
    if (!key?.startsWith('--')) continue
    const k = key.slice(2)
    const v = argv[i + 1]
    if (!v || v.startsWith('--')) {
      out[k] = true
    } else {
      out[k] = v
      i += 1
    }
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

function formatDate(ts = Date.now()) {
  const d = new Date(ts)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

function formatDateTime(ts = Date.now()) {
  const d = new Date(ts)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hh = String(d.getHours()).padStart(2, '0')
  const mm = String(d.getMinutes()).padStart(2, '0')
  const ss = String(d.getSeconds()).padStart(2, '0')
  return `${y}-${m}-${day} ${hh}:${mm}:${ss}`
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true })
}

function findNodeExe(customPath) {
  if (customPath && fs.existsSync(customPath)) return customPath
  const envPath = process.env.NODE_EXE || process.env.NODE_PATH
  if (envPath && fs.existsSync(envPath)) return envPath
  return process.execPath || null
}

function parseSymbolsCsv(csv = '') {
  return csv
    .split(',')
    .map((s) => s.trim())
    .filter((s) => /^\d{6}$/.test(s))
}

function computeRisk(args) {
  if (!(args.capital && args.riskPct && args.entry && args.stop)) return null
  const capital = toNum(args.capital, 'capital')
  const riskPct = toNum(args.riskPct, 'riskPct')
  const entry = toNum(args.entry, 'entry')
  const stop = toNum(args.stop, 'stop')
  const target = args.target != null ? toNum(args.target, 'target') : null
  const side = (args.side || 'long').toLowerCase()
  const boardLot = args.boardLot != null ? Math.max(1, Math.floor(toNum(args.boardLot, 'boardLot'))) : 100

  if (capital <= 0) throw new Error('capital 必须 > 0')
  if (riskPct <= 0 || riskPct > 100) throw new Error('riskPct 必须在 (0,100] 区间')
  if (!['long', 'short'].includes(side)) throw new Error('side 仅支持 long/short')

  const riskAmount = capital * (riskPct / 100)
  const perShareRisk = side === 'long' ? entry - stop : stop - entry
  if (perShareRisk <= 0) throw new Error('stop 位置不合法，导致单股风险 <= 0')

  const rawShares = Math.floor(riskAmount / perShareRisk)
  const shares = Math.floor(rawShares / boardLot) * boardLot
  const positionCost = shares * entry
  const actualRisk = shares * perShareRisk
  const positionPct = (positionCost / capital) * 100

  const out = {
    maxRiskAmount: round2(riskAmount),
    perShareRisk: round2(perShareRisk),
    suggestedShares: shares,
    positionCost: round2(positionCost),
    positionPct: round2(positionPct),
    actualRisk: round2(actualRisk),
    side,
    boardLot,
  }

  if (target != null) {
    const rewardPerShare = side === 'long' ? target - entry : entry - target
    out.rewardPerShare = round2(rewardPerShare)
    out.rr = round2(rewardPerShare > 0 ? rewardPerShare / perShareRisk : 0)
  }
  return out
}

function buildPlan(args) {
  const mode = String(args.mode || 'short').toLowerCase()
  const batch = args.batch ? String(args.batch).toLowerCase() : null
  const symbolsCsv = args.symbols ? String(args.symbols) : ''
  const symbols = parseSymbolsCsv(symbolsCsv)
  const watchlist = args.watchlist ? String(args.watchlist) : path.join(__dirname, 'watchlist.txt')

  let actions
  if (mode === 'swing') {
    actions = ['morning_check', 'plan_swing']
  } else if (mode === 'scalp') {
    actions = ['plan_scalp']
  } else {
    actions = ['morning_check', 'plan_short']
  }

  if (args.intraday) actions.push('intraday_scan')
  if (args.afterClose) actions.push('after_close_review')

  if (batch) {
    if (symbols.length > 0) {
      const csv = symbols.join(',')
      if (batch === 'quote') actions.push(`batch_quote:${csv}`)
      if (batch === 'kline') actions.push(`batch_kline:${csv}`)
      if (batch === 'f10') actions.push(`batch_f10:${csv}`)
    } else {
      if (batch === 'quote') actions.push(`batch_quote_file:${watchlist}`)
      if (batch === 'kline') actions.push(`batch_kline_file:${watchlist}`)
      if (batch === 'f10') actions.push(`batch_f10_file:${watchlist}`)
    }
  }

  return {
    mode,
    watchlist,
    symbols,
    actions,
  }
}

function loadPlanFile(planFilePath) {
  const abs = path.isAbsolute(planFilePath) ? planFilePath : path.resolve(process.cwd(), planFilePath)
  const raw = fs.readFileSync(abs, 'utf8')
  const plan = JSON.parse(raw)
  if (!Array.isArray(plan.actions) || plan.actions.length === 0) {
    throw new Error(`plan-file 缺少 actions: ${abs}`)
  }
  return { ...plan, planFile: abs, planDir: path.dirname(abs) }
}

function normalizeActionStep(step, baseDir) {
  if (typeof step !== 'string') return step
  const [action, arg = ''] = step.split(':')
  if (!/_file$/.test(action)) return step
  if (!arg) return step
  const resolved = path.isAbsolute(arg) ? arg : path.resolve(baseDir, arg)
  return `${action}:${resolved}`
}

function normalizePlanActions(plan, baseDir) {
  if (!Array.isArray(plan.actions)) return plan
  return {
    ...plan,
    actions: plan.actions.map((s) => normalizeActionStep(s, baseDir)),
  }
}

function runHotkeysStep(exePath, scriptPath, step, dryRun) {
  const [action, arg = ''] = step.split(':')
  const command = `"${exePath}" "${scriptPath}" --action "${action}"${arg ? ` --arg "${arg}"` : ''}`
  if (dryRun) {
    return { ok: true, code: 0, command, stdout: '[dry-run]', stderr: '' }
  }
  const result = spawnSync(exePath, [scriptPath, '--action', action, ...(arg ? ['--arg', arg] : [])], {
    encoding: 'utf8',
    windowsHide: true,
  })
  return {
    ok: result.status === 0,
    code: result.status ?? -1,
    command,
    stdout: result.stdout || '',
    stderr: result.stderr || '',
  }
}

function main() {
  const args = parseArgs(process.argv)
  const dryRun = Boolean(args.dryRun)
  const isWin = process.platform === 'win32'
  const logsDir = path.join(__dirname, 'logs')
  ensureDir(logsDir)

  const scriptPath = path.join(__dirname, 'ths-hotkeys.mjs')
  const startAt = Date.now()
  const startedAt = formatDateTime(startAt)

  let plan
  if (args.planFile) {
    const rawPlan = loadPlanFile(String(args.planFile))
    plan = normalizePlanActions(rawPlan, rawPlan.planDir || process.cwd())
  } else {
    plan = normalizePlanActions(buildPlan(args), process.cwd())
  }

  const risk = computeRisk(args)

  const summary = {
    startedAt,
    platform: process.platform,
    dryRun,
    plan,
    risk,
    steps: [],
    ok: false,
  }

  if (!isWin && !dryRun) {
    summary.ok = false
    summary.error = 'run-all.mjs 当前仅支持 Windows（可用 --dryRun 预演）。'
  } else {
    const exe = findNodeExe(args.nodePath ? String(args.nodePath) : '')
    if (!exe && !dryRun) {
      summary.ok = false
      summary.error = '未找到 Node 可执行文件，请设置 --nodePath 或环境变量 NODE_EXE。'
    } else {
      const effectiveExe = exe || 'node'
      for (const step of plan.actions) {
        const res = runHotkeysStep(effectiveExe, scriptPath, step, dryRun)
        summary.steps.push({
          step,
          ok: res.ok,
          code: res.code,
          command: res.command,
          stdout: res.stdout.trim(),
          stderr: res.stderr.trim(),
        })
        if (!res.ok) break
      }
      summary.ok = summary.steps.every((s) => s.ok)
    }
  }

  summary.finishedAt = formatDateTime()
  summary.durationMs = Date.now() - startAt

  const fileName = `run-all-${formatDate(startAt)}-${String(startAt).slice(-6)}.json`
  const outFile = path.join(logsDir, fileName)
  fs.writeFileSync(outFile, `${JSON.stringify(summary, null, 2)}\n`, 'utf8')

  process.stdout.write(`${JSON.stringify({ ok: summary.ok, logFile: outFile, summary }, null, 2)}\n`)
  if (!summary.ok) process.exit(1)
}

try {
  main()
} catch (err) {
  process.stderr.write(`[run-all] ${(err && err.message) || String(err)}\n`)
  process.exit(1)
}
