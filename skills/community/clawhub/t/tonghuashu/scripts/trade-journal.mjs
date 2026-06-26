#!/usr/bin/env node
/**
 * 交易日志工具（JSONL）
 *
 * 新增：
 * node trade-journal.mjs add --symbol 600519 --side buy --entry 1688 --stop 1650 --target 1760 --shares 100 --strategy short --note "回踩均线"
 *
 * 查看最近 N 条：
 * node trade-journal.mjs list --limit 20
 */

import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const logsDir = path.join(__dirname, 'logs')
const journalFile = path.join(logsDir, 'trade-journal.jsonl')

function parseArgs(argv) {
  const out = { _: [] }
  for (let i = 2; i < argv.length; i += 1) {
    const k = argv[i]
    const v = argv[i + 1]
    if (!k?.startsWith('--')) {
      out._.push(k)
      continue
    }
    out[k.slice(2)] = v && !v.startsWith('--') ? v : true
    if (v && !v.startsWith('--')) i += 1
  }
  return out
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true })
}

function now() {
  return new Date().toISOString()
}

function toNum(v, name) {
  if (v == null) return undefined
  const n = Number(v)
  if (!Number.isFinite(n)) throw new Error(`参数 ${name} 非法: ${v}`)
  return n
}

function addEntry(args) {
  ensureDir(logsDir)
  const entry = {
    ts: now(),
    symbol: String(args.symbol || '').trim(),
    side: String(args.side || '').toLowerCase(),
    entry: toNum(args.entry, 'entry'),
    stop: toNum(args.stop, 'stop'),
    target: toNum(args.target, 'target'),
    shares: toNum(args.shares, 'shares'),
    strategy: args.strategy ? String(args.strategy) : '',
    note: args.note ? String(args.note) : '',
    tag: args.tag ? String(args.tag) : '',
  }

  if (!/^\d{6}$/.test(entry.symbol)) throw new Error('symbol 必须是 6 位代码')
  if (!['buy', 'sell', 'long', 'short'].includes(entry.side)) throw new Error('side 必须是 buy/sell/long/short')

  fs.appendFileSync(journalFile, `${JSON.stringify(entry)}\n`, 'utf8')
  process.stdout.write(`${JSON.stringify({ ok: true, file: journalFile, entry }, null, 2)}\n`)
}

function listEntries(args) {
  if (!fs.existsSync(journalFile)) {
    process.stdout.write(`${JSON.stringify({ ok: true, file: journalFile, entries: [] }, null, 2)}\n`)
    return
  }
  const limit = Math.max(1, Number(args.limit || 20))
  const lines = fs.readFileSync(journalFile, 'utf8').split('\n').filter(Boolean)
  const last = lines.slice(-limit).map((l) => JSON.parse(l))
  process.stdout.write(`${JSON.stringify({ ok: true, file: journalFile, count: last.length, entries: last }, null, 2)}\n`)
}

try {
  const args = parseArgs(process.argv)
  const cmd = args._[0] || 'list'
  if (cmd === 'add') addEntry(args)
  else listEntries(args)
} catch (err) {
  process.stderr.write(`[trade-journal] ${(err && err.message) || String(err)}\n`)
  process.exit(1)
}
