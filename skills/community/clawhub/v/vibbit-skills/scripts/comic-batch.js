#!/usr/bin/env node
'use strict'

const fs = require('node:fs/promises')
const path = require('node:path')
const crypto = require('node:crypto')
const { validate } = require('./lib/schemas')
const { stringifyJson } = require('./lib/json')
const tasks = require('./lib/tasks')
const imageSpec = require('./lib/registry').commands.gen_image
const { createClient, VibbitError, redactValue } = require('./lib/client')
const { resolveAccount, resolveCredential } = require('./lib/auth-store')

const digest = value => crypto.createHash('sha256').update(value).digest('hex')
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))
const terminal = status => ['COMPLETED', 'FAILED', 'INSUFFICIENT_POINTS', 'REJECTED'].includes(status)
const inputError = message => new VibbitError('input', message)
async function readJson(file) {
  const stat = await fs.stat(file)
  if (!stat.isFile() || stat.size > 1024 * 1024) throw inputError('Expected a regular JSON file of at most 1 MB')
  return JSON.parse(await fs.readFile(file, 'utf8'))
}
async function save(file, value, exclusive = false) {
  const temporary = file + '.' + crypto.randomUUID() + '.tmp'
  try {
    await fs.writeFile(exclusive ? file : temporary, JSON.stringify(value, null, 2) + '\n', { flag: 'wx', mode: 0o600 })
    if (!exclusive) await fs.rename(temporary, file)
  } finally { if (!exclusive) await fs.rm(temporary, { force: true }).catch(() => {}) }
}
function keys(value, allowed) {
  if (!value || typeof value !== 'object' || Array.isArray(value) || Object.keys(value).some(key => !allowed.includes(key))) {
    throw inputError('Unexpected comic batch fields')
  }
}
async function prepare(file) {
  const manifest = await readJson(file)
  keys(manifest, ['version', 'references_ready', 'pages'])
  if (manifest.version !== 1 || manifest.references_ready !== true) throw inputError('Use version 1 and references_ready=true only after reviewing the adopted shared references/page')
  if (!Array.isArray(manifest.pages) || !manifest.pages.length || manifest.pages.length > 1000) throw inputError('Provide 1..1000 explicitly authorized ready pages')
  const pages = [], ids = new Set()
  for (const page of manifest.pages) {
    keys(page, ['page_id', 'input_file', 'name'])
    if (typeof page.page_id !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9_-]{0,99}$/.test(page.page_id) || ids.has(page.page_id)) throw inputError('Page IDs must be distinct safe identifiers')
    if (typeof page.input_file !== 'string' || !page.input_file.trim()) throw inputError('Each ready page needs an actual input_file')
    if (page.name !== undefined && (typeof page.name !== 'string' || !page.name.trim() || page.name.length > 200)) throw inputError('Page names must be nonblank text of at most 200 characters')
    ids.add(page.page_id)
    const inputFile = path.resolve(path.dirname(file), page.input_file)
    const { input } = validate('gen_image', await readJson(inputFile))
    const hash = digest(stringifyJson(tasks.requestSpec(imageSpec, input).body))
    pages.push({ page_id: page.page_id, input_file: inputFile, name: page.name || page.page_id, input, input_sha256: hash })
  }
  const fingerprint = digest(JSON.stringify(pages.map(({ page_id, input_sha256, name }) => ({ page_id, input_sha256, name }))))
  return { fingerprint, pages }
}

async function bounded(items, limit, work) {
  let index = 0
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (index < items.length) await work(items[index++])
  }))
}

async function run(client, batch, { stateDir, concurrency = 3, maxNew = 6, timeoutMs = 50000,
  queryOnly = false, now = Date.now, delay = sleep, onProgress = () => {} } = {}) {
  if (!Number.isInteger(concurrency) || concurrency < 1 || concurrency > 8) throw inputError('Concurrency must be 1..8; this is a client policy, not a service quota')
  if (!Number.isInteger(maxNew) || maxNew < 1 || maxNew > 1000) throw inputError('max-new must be 1..1000 within the authorized total')
  if (!(timeoutMs > 0 && timeoutMs <= 60000)) throw inputError('Wait window must be at most 60 seconds')
  if (typeof stateDir !== 'string' || !path.isAbsolute(stateDir)) throw inputError('Use an absolute private persistent state-dir unique to this batch')
  await fs.mkdir(stateDir, { recursive: true, mode: 0o700 })
  const directory = await fs.lstat(stateDir)
  if (!directory.isDirectory() || directory.isSymbolicLink() || process.platform !== 'win32' &&
    ((directory.mode & 0o077) || directory.uid !== process.getuid?.())) throw inputError('Use a private owned state directory (0700 on POSIX)')
  const lock = path.join(stateDir, 'batch.lock')
  try { await save(lock, { pid: process.pid }, true) } catch (error) {
    if (error.code === 'EEXIST') throw new VibbitError('configuration', 'This batch is already locked. Do not run two schedulers or remove a live process lock.')
    throw error
  }
  const deadline = now() + timeoutMs
  let submitted = 0, stopReason
  try {
    const identityFile = path.join(stateDir, 'batch.json')
    const identity = { version: 1, kind: 'comic_batch', base_url: client.base, fingerprint: batch.fingerprint }
    try {
      const saved = await readJson(identityFile)
      if (JSON.stringify(saved) !== JSON.stringify(identity)) throw inputError('This state directory belongs to different pages, requests or API site; preserve it for recovery')
    } catch (error) {
      if (error.code !== 'ENOENT') throw error
      await save(identityFile, identity, true)
    }
    const pages = []
    // Preflight every journal before the first API call, including pages not yet admitted.
    for (const page of batch.pages) {
      const journal = path.join(stateDir, 'page-' + page.page_id + '.json')
      let record
      try { record = await tasks.loadState(journal, client.base) } catch (error) { if (error.code !== 'ENOENT') throw error }
      if (record && (record.command !== 'gen_image' || record.input_sha256 !== page.input_sha256)) throw inputError('A saved page belongs to a different request; do not replace its journal')
      const row = { ...page, journal, result_file: journal + '.result.json', status: record?.phase || 'UNSUBMITTED', task_id: record?.task_id,
        next_query: Number.isFinite(record?.comic_next_query_at) ? record.comic_next_query_at : 0 }
      if (record && !row.task_id && !['FAILED', 'INSUFFICIENT_POINTS', 'REJECTED'].includes(row.status)) { row.status = 'SUBMISSION_UNKNOWN'; stopReason = 'submission_unknown' }
      if (row.status === 'COMPLETED') {
        try {
          const cached = await readJson(row.result_file)
          if (cached.task_id !== row.task_id || cached.status !== 'COMPLETED') throw new Error('Unverified cached result')
          row.output = cached
        } catch { row.status = 'RESULT_PENDING' }
      }
      pages.push(row)
    }
    const snapshot = () => ({ total: pages.length, completed: pages.filter(row => row.status === 'COMPLETED').length,
      failed: pages.filter(row => ['FAILED', 'INSUFFICIENT_POINTS', 'REJECTED'].includes(row.status)).length,
      active: pages.filter(row => row.task_id && !terminal(row.status)).length,
      unsubmitted: pages.filter(row => row.status === 'UNSUBMITTED').length,
      unknown: pages.filter(row => row.status === 'SUBMISSION_UNKNOWN').length })
    let lastProgress
    const progress = () => {
      const value = { ...snapshot(), submitted_this_window: submitted, ...(stopReason ? { stop_reason: stopReason } : {}) }
      const text = JSON.stringify(value)
      if (text !== lastProgress) { onProgress(value); lastProgress = text }
    }
    const accept = async (row, output) => {
      row.status = output.status; row.task_id = output.task_id; row.next_query = now() + 5000
      if (output.status === 'COMPLETED') {
        row.output = { ok: output.ok, status: output.status, task_id: output.task_id,
          result: output.result, artifacts: output.artifacts, image_archive: output.image_archive }
        try { await save(row.result_file, row.output) } catch {
          stopReason = 'result_record_unavailable'; row.record_error = true
        }
      }
      try {
        const record = await tasks.loadState(row.journal, client.base)
        record.phase = row.status; record.comic_next_query_at = row.next_query
        await save(row.journal, record)
      } catch { throw new VibbitError('journal', 'The page result is retained but its journal could not be updated; do not submit again') }
    }
    const failed = async (row, error, write) => {
      row.error_kind = error.kind || 'local_error'
      if (write) {
        try {
          const record = await tasks.loadState(row.journal, client.base)
          row.task_id = record.task_id; row.status = record.phase
        } catch { row.status = 'SUBMISSION_UNKNOWN' }
        if (!row.task_id && !terminal(row.status)) row.status = 'SUBMISSION_UNKNOWN'
        if (row.status === 'SUBMISSION_UNKNOWN' || error.ambiguous !== false && !row.task_id) stopReason = 'submission_unknown'
      } else if (error.kind === 'task_failed') {
        row.status = error.status || 'FAILED'
        const record = await tasks.loadState(row.journal, client.base)
        record.phase = row.status
        await save(row.journal, record)
      }
      if (error.http_status === 429 || error.code === 1006) stopReason = 'rate_limited'
      if (error.kind === 'authentication' || error.kind === 'configuration' || error.kind === 'journal') stopReason = 'account_or_record_action_required'
      if (error.status === 'INSUFFICIENT_POINTS') stopReason = 'insufficient_points'
      row.next_query = now() + Math.max(5000, (error.retry_after_seconds || 0) * 1000)
      try {
        const record = await tasks.loadState(row.journal, client.base)
        record.comic_next_query_at = row.next_query
        await save(row.journal, record)
      } catch { stopReason = 'account_or_record_action_required' }
    }
    while (now() < deadline) {
      const due = pages.filter(row => row.task_id && !terminal(row.status) && row.next_query <= now())
      await bounded(due, concurrency, async row => {
        if (now() >= deadline) return
        try {
          const output = await tasks.status(client, row.task_id, imageSpec,
            Math.max(1, deadline - now()), row.journal + '.source.json')
          await accept(row, output)
        } catch (error) { await failed(row, error, false) }
      })
      // Reserve a remote-active slot until completion; rapid POSTs alone are not a concurrency limit.
      while (!queryOnly && !stopReason && submitted < maxNew && snapshot().active < concurrency && now() < deadline) {
        const row = pages.find(item => item.status === 'UNSUBMITTED')
        if (!row) break
        submitted++
        const timedClient = { base: client.base, request: (method, route, body, budget) => client.request(method, route, body,
          Math.max(1, Math.min(budget ?? 30000, deadline - now()))) }
        try {
          await accept(row, await tasks.submit(timedClient, 'gen_image', row.input,
            { stateFile: row.journal, imageArchiveRequest: { name: row.name } }))
        } catch (error) { await failed(row, error, true) }
        progress()
        if (!stopReason && now() < deadline) await delay(Math.min(500, deadline - now()))
      }
      const counts = snapshot()
      progress()
      if (!counts.active) break
      const next = Math.min(...pages.filter(row => row.task_id && !terminal(row.status)).map(row => row.next_query))
      await delay(Math.min(Math.max(1, next - now()), Math.max(0, deadline - now())))
    }
    const counts = snapshot()
    return { ok: !counts.failed && !counts.unknown, ...counts, submitted_this_window: submitted,
      ...(counts.active ? { wait_timed_out: true } : {}),
      concurrency, state_dir: stateDir, stop_reason: stopReason || (counts.active ? 'wait_window' : counts.unsubmitted ? queryOnly ? 'query_only' : 'review_checkpoint' : 'complete'),
      pages: pages.map(row => ({ page_id: row.page_id, status: row.status, ...(row.task_id ? { task_id: row.task_id } : {}),
        state_file: row.journal, ...(row.output ? { result_file: row.result_file, ...row.output } : {}),
        ...(row.error_kind ? { error_kind: row.error_kind } : {}), ...(row.record_error ? { record_saved: false } : {}) })) }
  } finally { await fs.rm(lock, { force: true }) }
}

async function main(argv) {
  const [command = 'help', ...args] = argv
  if (['help', '--help', '-h'].includes(command)) return { tool: 'Vibbit ready comic-page scheduling',
    plan: '--manifest FILE (offline validation; no writes)',
    run: '--manifest FILE --state-dir ABSOLUTE_PRIVATE_DIR [--concurrency 3] [--max-new 6] [--timeout-seconds 50] [--query-only]',
    behavior: 'Review the adopted shared references/page first. Only independent ready pages belong in the manifest. Reuse the same manifest and state directory. Bounded remote-active tasks, separate page journals and no ambiguous write retries. Service quotas and generation speed are not guaranteed.' }
  if (!['plan', 'run'].includes(command)) throw inputError('Choose plan or run')
  const flags = {}
  for (let i = 0; i < args.length; i++) {
    const key = args[i].replace(/^--/, '')
    if (!args[i].startsWith('--') || Object.hasOwn(flags, key) || !['manifest', 'state-dir', 'concurrency', 'max-new', 'timeout-seconds', 'query-only'].includes(key)) throw inputError('Unexpected or duplicate comic batch option')
    if (key === 'query-only') flags[key] = true
    else {
      const value = args[++i]
      if (!value || value.startsWith('--')) throw inputError('Missing comic batch option value')
      flags[key] = value
    }
  }
  if (!flags.manifest) throw inputError('A manifest file is required')
  const batch = await prepare(path.resolve(flags.manifest))
  if (command === 'plan') return { ok: true, submitted: false, total: batch.pages.length,
    pages: batch.pages.map(({ page_id, input_file, input_sha256 }) => ({ page_id, input_file, input_sha256 })) }
  const account = await resolveAccount(), credential = await resolveCredential({ account })
  if (!credential.key) throw new VibbitError('authentication_required', 'Configure the execution environment with the existing Vibbit account setup flow')
  const client = createClient(credential)
  const result = await run(client, batch, { stateDir: flags['state-dir'], concurrency: flags.concurrency === undefined ? 3 : Number(flags.concurrency),
    maxNew: flags['max-new'] === undefined ? 6 : Number(flags['max-new']),
    timeoutMs: flags['timeout-seconds'] === undefined ? 50000 : Number(flags['timeout-seconds']) * 1000,
    queryOnly: !!flags['query-only'], onProgress: value => process.stderr.write(JSON.stringify(value) + '\n') })
  return redactValue(result, credential.key)
}
if (require.main === module) main(process.argv.slice(2)).then(output => {
  process.stdout.write(JSON.stringify(output, null, 2) + '\n')
  if (output.unknown || output.failed) process.exitCode = 4
}).catch(error => {
  const key = process.env.VIBBIT_API_KEY || process.env.VIBBIT_OPENAPI_KEY || ''
  process.stdout.write(JSON.stringify(redactValue({ ok: false, error: { kind: error.kind || 'input', message: error.message } }, key)) + '\n')
  process.exitCode = 2
})
module.exports = { prepare, run, main }
