#!/usr/bin/env node
/**
 * 同花顺快捷动作（Node 文本版）
 * 说明：通过 PowerShell COM SendKeys 执行 GUI 自动化，不依赖 .ahk/.ps1 文件。
 */

import fs from 'node:fs'
import path from 'node:path'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

function parseArgs(argv) {
  const out = { action: '', arg: '' }
  for (let i = 2; i < argv.length; i += 1) {
    const t = argv[i]
    const n = argv[i + 1]
    const k = t.toLowerCase()
    if ((k === '-action' || k === '--action') && n) {
      out.action = n
      i += 1
      continue
    }
    if ((k === '-arg' || k === '--arg') && n) {
      out.arg = n
      i += 1
      continue
    }
    if (!out.action) out.action = t
    else if (!out.arg) out.arg = t
  }
  return out
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true })
}

function nowDate() {
  const d = new Date()
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

function nowDateTime() {
  const d = new Date()
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hh = String(d.getHours()).padStart(2, '0')
  const mm = String(d.getMinutes()).padStart(2, '0')
  const ss = String(d.getSeconds()).padStart(2, '0')
  return `${y}-${m}-${day} ${hh}:${mm}:${ss}`
}

const logsDir = path.join(__dirname, 'logs')
ensureDir(logsDir)
const logFile = path.join(logsDir, `trading-${nowDate()}.log`)

function writeLog(status, action, arg = '-', detail = '') {
  const line = `${nowDateTime()} | ${status} | action=${action} | arg=${arg || '-'}${detail ? ` | ${detail}` : ''}\n`
  fs.appendFileSync(logFile, line, 'utf8')
}

function findPowerShell() {
  const candidates = [
    process.env.POWERSHELL_EXE,
    process.env.PWSH_PATH,
    'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe',
    'C:\\Program Files\\PowerShell\\7\\pwsh.exe',
    'powershell.exe',
  ].filter(Boolean)
  return candidates[0]
}

function psEscape(s) {
  return String(s).replace(/'/g, "''")
}

function runPs(command) {
  const exe = findPowerShell()
  const r = spawnSync(exe, ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', command], {
    encoding: 'utf8',
    windowsHide: true,
  })
  return { ok: r.status === 0, code: r.status ?? -1, stdout: r.stdout || '', stderr: r.stderr || '' }
}

function sleepMs(ms) {
  const script = `Start-Sleep -Milliseconds ${Math.max(1, Math.floor(ms))}`
  return runPs(script).ok
}

function activateThs() {
  const cmd = [
    'Add-Type -AssemblyName Microsoft.VisualBasic',
    "try {[Microsoft.VisualBasic.Interaction]::AppActivate('同花顺')|Out-Null; Start-Sleep -Milliseconds 250; exit 0} catch {}",
    "try {[Microsoft.VisualBasic.Interaction]::AppActivate('同花顺炒股')|Out-Null; Start-Sleep -Milliseconds 250; exit 0} catch {}",
    'exit 1',
  ].join('; ')
  return runPs(cmd).ok
}

function sendKeys(keys) {
  const cmd = `$ws=New-Object -ComObject WScript.Shell; $ws.SendKeys('${psEscape(keys)}')`
  return runPs(cmd).ok && sleepMs(300)
}

function sendStep(step) {
  switch (step) {
    case 'activate': return sleepMs(200)
    case 'refresh': return sendKeys('{F5}')
    case 'watchlist': return sendKeys('{F6}')
    case 'limitup': return sendKeys('^z')
    case 'gainrank': return sendKeys('60{ENTER}')
    case 'market_sh': return sendKeys('{F3}')
    case 'market_sz': return sendKeys('{F4}')
    case 'entrust': return sendKeys('{F12}')
    default: return false
  }
}

function runSequence(steps) {
  for (const s of steps) if (!sendStep(s)) return false
  return true
}

function normalizeSymbol(s) {
  const t = String(s || '').trim()
  return /^\d{6}$/.test(t) ? t : ''
}

function jumpToSymbol(code) {
  const s = normalizeSymbol(code)
  if (!s) return false
  return sendKeys(s) && sendKeys('{ENTER}')
}

function parseCsv(csv) {
  return String(csv || '')
    .split(',')
    .map((x) => normalizeSymbol(x))
    .filter(Boolean)
}

function loadSymbolsFromFile(filePath) {
  const p = filePath ? path.resolve(filePath) : path.join(__dirname, 'watchlist.txt')
  if (!fs.existsSync(p)) return []
  const out = []
  const seen = new Set()
  for (const line of fs.readFileSync(p, 'utf8').split(/\r?\n/)) {
    const t = line.trim()
    if (!t || t.startsWith('#') || t.startsWith(';')) continue
    const m = t.match(/\d{6}/g) || []
    for (const c of m) if (!seen.has(c)) { seen.add(c); out.push(c) }
  }
  return out
}

function batchReview(symbols, mode) {
  if (!symbols.length) return false
  for (const s of symbols) {
    if (!jumpToSymbol(s)) return false
    if (mode === 'kline' && !sendKeys('{F5}')) return false
    if (mode === 'f10' && !(sendKeys('{F10}') && sendKeys('{ESC}'))) return false
  }
  return true
}

function main() {
  if (process.platform !== 'win32') throw new Error('ths-hotkeys.mjs 仅支持 Windows')
  const { action, arg } = parseArgs(process.argv)
  const act = String(action || '').toLowerCase()
  if (!act) throw new Error('缺少 action 参数')
  if (!activateThs()) {
    writeLog('ERROR', act, arg, '未找到同花顺窗口')
    throw new Error('未找到同花顺窗口，请先打开客户端')
  }

  let ok = false
  let needSymbol = false
  const symbol = normalizeSymbol(arg)

  switch (act) {
    case 'activate': ok = sendStep('activate'); break
    case 'refresh': ok = sendStep('refresh'); break
    case 'watchlist': ok = sendStep('watchlist'); break
    case 'limitup': ok = sendStep('limitup'); break
    case 'gainrank': ok = sendStep('gainrank'); break
    case 'market_sh': ok = sendStep('market_sh'); break
    case 'market_sz': ok = sendStep('market_sz'); break
    case 'entrust': ok = sendStep('entrust'); break
    case 'morning_check': ok = runSequence(['market_sh', 'market_sz', 'limitup', 'gainrank', 'watchlist']); break
    case 'intraday_scan': ok = runSequence(['refresh', 'limitup', 'gainrank', 'watchlist']); break
    case 'after_close_review': ok = runSequence(['limitup', 'gainrank', 'watchlist']); break
    case 'prep_buy':
    case 'prep_sell':
      ok = sendStep('watchlist')
      if (ok && symbol) ok = jumpToSymbol(symbol)
      if (ok) ok = sendStep('entrust')
      break
    case 'focus': needSymbol = true; ok = jumpToSymbol(symbol); break
    case 'quote': needSymbol = true; ok = jumpToSymbol(symbol); break
    case 'kline': needSymbol = true; ok = jumpToSymbol(symbol) && sendStep('refresh'); break
    case 'detail': needSymbol = true; ok = jumpToSymbol(symbol) && sendKeys('{F1}'); break
    case 'fundamentals': needSymbol = true; ok = jumpToSymbol(symbol) && sendKeys('{F10}'); break
    case 'plan_short': ok = runSequence(['market_sh', 'market_sz', 'limitup', 'gainrank', 'watchlist', 'refresh', 'limitup']); break
    case 'plan_swing': ok = runSequence(['market_sh', 'market_sz', 'watchlist']) && sendKeys('80{ENTER}') && sendKeys('{F5}'); break
    case 'plan_scalp': ok = runSequence(['limitup', 'gainrank', 'refresh', 'limitup', 'gainrank']); break
    case 'batch_quote': ok = batchReview(parseCsv(arg), 'quote'); break
    case 'batch_kline': ok = batchReview(parseCsv(arg), 'kline'); break
    case 'batch_f10': ok = batchReview(parseCsv(arg), 'f10'); break
    case 'batch_quote_file': ok = batchReview(loadSymbolsFromFile(arg), 'quote'); break
    case 'batch_kline_file': ok = batchReview(loadSymbolsFromFile(arg), 'kline'); break
    case 'batch_f10_file': ok = batchReview(loadSymbolsFromFile(arg), 'f10'); break
    default: ok = false
  }

  if (!ok) {
    if (needSymbol && !symbol) {
      writeLog('ERROR', act, arg, '缺少或非法股票代码')
      throw new Error(`动作 ${act} 需要 6 位股票代码`)
    }
    writeLog('ERROR', act, arg, '未知动作或参数错误')
    throw new Error(`未知动作或参数错误: ${act}`)
  }

  writeLog('OK', act, arg, '执行成功')
}

try {
  main()
} catch (err) {
  process.stderr.write(`[ths-hotkeys] ${err?.message || String(err)}\n`)
  process.exit(1)
}
