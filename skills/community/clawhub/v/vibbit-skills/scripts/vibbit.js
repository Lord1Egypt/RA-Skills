#!/usr/bin/env node
'use strict'

const fs = require('node:fs/promises')
const { commands, models } = require('./lib/registry')
const { validate } = require('./lib/schemas')
const { createClient, redact, redactValue, VibbitError } = require('./lib/client')
const tasks = require('./lib/tasks')
const { probeLocal } = require('./lib/media')
const { parseJson, stringifyJson } = require('./lib/json')
const { displayBody } = require('./lib/translation')
const { previewUrl } = require('./lib/preview')
const { uploadLocalFile } = require('./lib/upload')
const { resolveAccount, resolveCredential, saveSelection, clearCredential } = require('./lib/auth-store')
const { startSetup, openBrowser } = require('./lib/auth-setup')
const { accountLinks, recoveryAction } = require('./lib/account-actions')

const booleanFlags = new Set(['dry-run', 'wait', 'all', 'all-items', 'allow-legacy', 'allow-known-issue', 'help', 'open', 'check'])
const valueFlags = new Set(['input', 'state', 'submission-id', 'task-id', 'command', 'timeout-seconds', 'poll-seconds', 'file',
  'prompt', 'model', 'size', 'ref-url', 'url', 'video-url', 'sub-tasks', 'region', 'site', 'lang'])

function parseArgs(argv) {
  const [command = 'help', ...tokens] = argv
  const flags = {}
  for (let i = 0; i < tokens.length; i++) {
    const name = tokens[i].replace(/^--/, '')
    if (!tokens[i].startsWith('--') || (!booleanFlags.has(name) && !valueFlags.has(name))) throw new VibbitError('input', `Unknown option: ${tokens[i]}`)
    if (Object.hasOwn(flags, name)) throw new VibbitError('input', `Duplicate option: --${name}`)
    if (booleanFlags.has(name)) flags[name] = true
    else {
      if (tokens[i + 1] === undefined || tokens[i + 1] === '' || tokens[i + 1].startsWith('--')) throw new VibbitError('input', `--${name} needs a nonempty value`)
      flags[name] = tokens[++i]
    }
  }
  return { command, flags }
}

async function readInput(file) {
  let raw
  if (file === '-') {
    const chunks = []
    let length = 0
    for await (const chunk of process.stdin) {
      length += chunk.length
      if (length > 1024 * 1024) throw new VibbitError('input', 'Input JSON exceeds 1 MB')
      chunks.push(chunk)
    }
    raw = Buffer.concat(chunks).toString('utf8')
  } else {
    const stat = await fs.stat(file)
    if (!stat.isFile() || stat.size > 1024 * 1024) throw new VibbitError('input', 'Input must be a regular JSON file of at most 1 MB')
    raw = await fs.readFile(file, 'utf8')
  }
  try { return parseJson(raw) } catch { throw new VibbitError('input', 'Input is not valid JSON') }
}

function inlineInput(command, flags) {
  const result = {}
  const map = {
    gen_image: { prompt: 'prompt', model: 'model', size: 'size', 'ref-url': 'reference_image_urls' },
    parse_url: { url: 'url' },
    transcribe_audio: { url: 'url' },
    breakdown: { 'video-url': 'video_url', 'sub-tasks': 'sub_tasks' },
    remove_subtitles: { 'video-url': 'video_url' },
  }[command] || {}
  const inlineNames = ['prompt', 'model', 'size', 'ref-url', 'url', 'video-url', 'sub-tasks']
  for (const key of inlineNames) {
    if (flags[key] === undefined) continue
    if (!map[key]) throw new VibbitError('input', `--${key} does not apply to ${command}; use --input with the documented fields`)
    result[map[key]] = key === 'sub-tasks'
      ? flags[key].split(',').map(x => x.trim()).filter(Boolean)
      : key === 'ref-url' ? [flags[key]] : flags[key]
  }
  return result
}

function seconds(value, fallback, minimum, maximum) {
  if (value === undefined) return fallback * 1000
  const number = Number(value)
  if (!Number.isFinite(number) || number < minimum || number > maximum) throw new VibbitError('input', `Time option must be ${minimum}..${maximum} seconds`)
  return number * 1000
}

const help = {
  usage: 'node scripts/vibbit.js COMMAND --input payload.json [--dry-run | --wait] [--state journal.json | --submission-id STABLE_LOCAL_ID]; upload_info --file LOCAL_PATH [--input payload.json]',
  commands: Object.keys(commands),
  utilities: {
    capabilities: '[--all] (offline registry; no account-level discovery)',
    describe: '--command NAME (input fields, examples and execution requirements)',
    health: 'authenticated GET /health',
    auth_status: '[--check] (credential source and region; --check performs one authenticated health request)',
    auth_setup: '[--open] [--region cn|global | --site OFFICIAL_WEB_URL] [--lang en|zh-CN] [--timeout-seconds 600] (local browser form; verifies the selected site before saving; no key argument)',
    account_select: '--region cn|global (verifies the saved key for that site, then remembers it as the active account)',
    auth_clear: '[--region cn|global] (removes only the selected site private credential file; does not revoke the server key or change environment variables)',
    account_links: '(offline key, avatar creation/list, pricing/credit packs, and billing management links for the selected regional API)',
    status: '--task-id ID', wait: '--task-id ID [--timeout-seconds 50] [--poll-seconds 5]',
    resume: '(--state FILE | --submission-id ID) [--timeout-seconds 50] (local journal lookup, then GET only; never resubmits)',
    probe: '--file LOCAL_PATH (optional ffprobe dependency; no upload)',
    preview_url: '--url IMAGE_URL (offline preview address mapping; preserves the original URL)',
    upload_info: '--file LOCAL_PATH [--input request.json] (gets MATERIAL_UPLOAD credentials and uploads the file)',
  },
  env: ['VIBBIT_API_KEY (or VIBBIT_OPENAPI_KEY), takes precedence over the selected site private credential file', 'VIBBIT_REGION (cn or global; independent of conversation language)', 'VIBBIT_BASE_URL (explicit host API override; must match an explicit region)', 'VIBBIT_CONFIG_DIR (optional absolute private credential directory; outside the project and Skill)', 'VIBBIT_STATE_DIR (default .vibbit/tasks in current working directory)'],
  account_selection: 'Explicit --region / VIBBIT_REGION or host base, then saved site (including one legacy regional key), then --site website hint, then global. Both sites have independent accounts, keys, credits, products and assets. Never retry a key at another site.',
  compatibility: 'gen_image defaults to gpt-image-2.5-sunburst. --allow-known-issue applies only to commands marked known_issue. Dry-run does not submit a task.',
  submission_recovery: 'Keep one submission-id per operation and the same VIBBIT_STATE_DIR. Repeating it reuses the local journal and only queries an existing task ID. It is not sent as a server idempotency key; a lost response without a recorded task ID still needs acceptance verification.',
  exit_codes: { 0: 'success or accepted task', 1: 'API, task, transport or protocol error', 2: 'input or configuration error', 3: 'wait deadline reached; task may continue', 4: 'submission uncertainty / cannot resume without ID', 5: 'partial result failure' },
}

// Export only the fields needed to form requests and interpret the command.
function describeCommand(spec) {
  const keys = ['task_type', 'documentation_url', 'operation', 'method', 'suffix', 'mode', 'wire', 'status',
    'fields', 'required', 'example', 'result_kind', 'min_poll_ms', 'defaults', 'models', 'requires_opt_in', 'note']
  return Object.fromEntries(keys.filter(key => Object.hasOwn(spec, key)).map(key => [key, spec[key]]))
}

async function execute(argv, context) {
  const { command, flags } = parseArgs(argv)
  if (['help', '-h', '--help'].includes(command) || flags.help) return help
  const utilityFlags = {
    capabilities: ['all'], describe: ['command'], probe: ['file'], preview_url: ['url'], health: [],
    status: ['task-id'], wait: ['task-id', 'timeout-seconds', 'poll-seconds'],
    resume: ['state', 'submission-id', 'timeout-seconds', 'poll-seconds'],
    auth_status: ['check'], auth_setup: ['open', 'timeout-seconds', 'lang'], auth_clear: [], account_links: [], account_select: [],
  }[command]
  if (utilityFlags) for (const key of Object.keys(flags)) {
    if (!utilityFlags.includes(key) && !['region', 'site'].includes(key)) throw new VibbitError('input', `--${key} does not apply to ${command}`)
  }
  if (command === 'capabilities') return {
    account_verified: false,
    commands: Object.entries(commands).filter(([, s]) => flags.all || s.status === 'documented' || (s.status === 'legacy' && s.requires_opt_in === false)).map(([name, s]) => ({ name, task_type: s.task_type, ...(s.operation ? { operation: s.operation } : {}), status: s.status, mode: s.mode, requires_opt_in: s.status === 'known_issue' || (s.status === 'legacy' && s.requires_opt_in !== false) })),
  }
  if (command === 'describe') {
    if (!commands[flags.command]) throw new VibbitError('input', 'describe requires --command with a registered command name')
    return { command: flags.command, ...describeCommand(commands[flags.command]), ...(flags.command === 'seedance' ? { models } : {}) }
  }
  if (command === 'probe') {
    if (!flags.file) throw new VibbitError('input', 'probe requires --file')
    return probeLocal(flags.file)
  }
  if (command === 'preview_url') {
    let url
    try { url = new URL(flags.url) } catch { throw new VibbitError('input', 'preview_url requires --url with an HTTP(S) image URL') }
    if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password) throw new VibbitError('input', 'preview_url requires an HTTP(S) URL without embedded credentials')
    const preview = previewUrl(flags.url)
    return { ok: true, url: flags.url, preview_url: preview, converted: preview !== flags.url }
  }
  if (flags.file && command !== 'upload_info') throw new VibbitError('input', '--file applies only to upload_info or probe')
  if (flags.lang && command !== 'auth_setup') throw new VibbitError('input', '--lang applies only to auth_setup')
  const account = await resolveAccount({ region: flags.region, site: flags.site })
  const base = account.base
  context.base = base
  const credential = async () => {
    const resolved = await resolveCredential({ account })
    context.key = resolved.key
    return resolved
  }
  const clientFor = async () => {
    const resolved = await credential()
    if (!resolved.key) throw new VibbitError('authentication_required', 'No credential is available in this execution environment. Use host credential settings, or auth_setup --open on an accessible local computer.')
    return createClient(resolved)
  }
  if (command === 'account_links') return { ok: true, base, selection_source: account.selection_source, ...accountLinks(base) }
  if (command === 'auth_clear') return clearCredential({ account })
  if (command === 'account_select') {
    if (!flags.region) throw new VibbitError('input', 'account_select requires --region cn or --region global')
    if (process.env.VIBBIT_REGION && process.env.VIBBIT_REGION !== account.region) throw new VibbitError('configuration', 'Update the host VIBBIT_REGION before saving a different active site')
    await (await clientFor()).request('GET', '/health')
    await saveSelection(account.region)
    return { ok: true, verified: true, base, ...accountLinks(base), selected: true }
  }
  if (command === 'auth_status') {
    const resolved = await credential()
    const output = { ok: true, configured: !!resolved.key, source: resolved.source, selection_source: account.selection_source, base, ...accountLinks(base), verified: false, local_setup_supported: process.platform !== 'win32' && !accountLinks(base).account_environment_check_required }
    if (!resolved.key) output.account_action = recoveryAction({ kind: 'authentication_required' }, base)
    if (flags.check && resolved.key) {
      await createClient(resolved).request('GET', '/health')
      output.verified = true
    }
    return output
  }
  if (command === 'auth_setup') {
    const setup = await startSetup({ account, lang: flags.lang, timeoutMs: seconds(flags['timeout-seconds'], 600, 30, 1800) })
    const stop = () => setup.close()
    process.once('SIGINT', stop); process.once('SIGTERM', stop)
    try {
      process.stderr.write(JSON.stringify({ phase: 'AWAITING_USER_KEY', setup_url: setup.url, local_browser_required: true, region: accountLinks(base).region }) + '\n')
      if (flags.open) process.stderr.write(JSON.stringify({ browser_opened: await openBrowser(setup.url) }) + '\n')
      return await setup.done
    } finally { process.removeListener('SIGINT', stop); process.removeListener('SIGTERM', stop) }
  }
  if (flags.open || flags.check) throw new VibbitError('input', '--open applies to auth_setup; --check applies to auth_status')
  const onProgress = info => process.stderr.write(JSON.stringify(info) + '\n')
  const waitOptions = {
    timeoutMs: seconds(flags['timeout-seconds'], 50, 1, 3600),
    intervalMs: seconds(flags['poll-seconds'], 5, 5, 3600), onProgress,
  }
  if (command === 'health') return { ok: true, result: await (await clientFor()).request('GET', '/health') }
  if (command === 'status') return tasks.status(await clientFor(), flags['task-id'])
  if (command === 'wait') return tasks.wait(await clientFor(), flags['task-id'], waitOptions)
  if (command === 'resume') {
    if (!!flags.state === !!flags['submission-id']) throw new VibbitError('input', 'resume requires either --state or --submission-id')
    const file = flags.state || tasks.submissionFile(flags['submission-id'])
    return tasks.resume(await clientFor(), file, waitOptions)
  }
  if (!commands[command]) throw new VibbitError('input', 'Unknown command; run help or capabilities --all')
  if (flags['all-items'] && command !== 'confirm_translation') throw new VibbitError('input', '--all-items applies only to confirm_translation')
  if (flags['task-id'] && !commands[command].operation) throw new VibbitError('input', '--task-id applies to actions or task queries, not new submissions')
  const inline = inlineInput(command, flags)
  if (flags.input && Object.keys(inline).length) throw new VibbitError('input', 'Use either --input or inline fields; mixing could override user input')
  let input = flags.input
    ? await readInput(flags.input)
    : command === 'upload_info' && flags.file ? { is_temporary: false } : inline
  let checked
  try { checked = validate(command, input) } catch (error) { throw new VibbitError('input', error.message) }
  const { spec, warnings } = checked
  input = checked.input
  if (command === 'confirm_translation') {
    if (input.sub_task_id === undefined && !flags['all-items']) throw new VibbitError('input', 'Choose a sub_task_id or explicitly use --all-items to confirm the entire batch')
    if (input.sub_task_id !== undefined && flags['all-items']) throw new VibbitError('input', 'Use a sub_task_id or --all-items, never both')
  }
  const request = tasks.requestSpec(spec, input, flags['task-id'])
  if (flags.state && flags['submission-id']) throw new VibbitError('input', 'Choose --state or --submission-id, not both')
  if (flags['submission-id']) tasks.submissionFile(flags['submission-id'])
  if (flags['dry-run']) return { ok: true, dry_run: true, command, status: spec.status, method: request.method, endpoint: `${base}${request.route}`, body: displayBody(request.body), ...(flags['submission-id'] ? { submission_id: flags['submission-id'] } : {}), ...(spec.result_kind === 'translation' ? { body_json: stringifyJson(request.body) } : {}), warnings }
  if (spec.status === 'legacy' && spec.requires_opt_in !== false && !flags['allow-legacy']) throw new VibbitError('configuration', 'Legacy contract is disabled by default. Read the capability reference and use --allow-legacy only for an account known to support it.')
  if (spec.status === 'known_issue' && !flags['allow-known-issue']) throw new VibbitError('configuration', 'This API has a recorded support issue. Read the resource reference before using --allow-known-issue for a deliberate verification.')
  const client = await clientFor()
  const submitted = await tasks.submit(client, command, input, { stateFile: flags.state, submissionId: flags['submission-id'], taskId: flags['task-id'], onProgress })
  if (command === 'upload_info' && flags.file) {
    if (!submitted.result || typeof submitted.result !== 'object' || Array.isArray(submitted.result)) {
      throw new VibbitError('protocol', 'MATERIAL_UPLOAD did not return upload instructions')
    }
    const uploaded = await uploadLocalFile(flags.file, submitted.result)
    return { ...uploaded, command, submission_id: submitted.submission_id, state_file: submitted.state_file, request_id: submitted.request_id, warnings: [...(submitted.warnings || []), ...warnings] }
  }
  if (flags.wait && !submitted.review_context_required && !['COMPLETED', 'FAILED', 'INSUFFICIENT_POINTS'].includes(submitted.status)) {
    const waited = await tasks.wait(client, submitted.task_id, { ...waitOptions, stateFile: submitted.state_file, spec })
    return { ...waited, warnings: [...(waited.warnings || []), ...warnings] }
  }
  return { ...submitted, warnings: [...(submitted.warnings || []), ...warnings] }
}

async function main(argv) {
  const context = {}
  try {
    const output = await execute(argv, context)
    const action = recoveryAction(output, context.base)
    return redactValue({ ...output, ...(action ? { account_action: action } : {}) }, context.key)
  } catch (error) {
    error.message = redact(error.message, context.key)
    error.account_action = recoveryAction(error, context.base)
    throw error
  }
}

async function run() {
  const key = process.env.VIBBIT_API_KEY || process.env.VIBBIT_OPENAPI_KEY || ''
  try {
    const output = await main(process.argv.slice(2))
    process.stdout.write(redact(JSON.stringify(output, null, 2), key) + '\n')
    process.exitCode = output.wait_timed_out ? 3 : output.partial_failure ? 5 : output.ok === false ? 1 : 0
  } catch (error) {
    const kind = error.kind || (['ENOENT', 'EEXIST', 'EACCES'].includes(error.code) ? 'configuration' : 'input')
    const output = { ok: false, error: { kind, message: error.message,
      ...Object.fromEntries(['code', 'http_status', 'submission_id', 'request_id', 'task_id', 'status', 'state_file', 'phase', 'ambiguous', 'account_action'].filter(k => error[k] !== undefined).map(k => [k, error[k]])),
    } }
    process.stdout.write(redact(JSON.stringify(output, null, 2), key) + '\n')
    process.exitCode = error.ambiguous || kind === 'cannot_resume' ? 4 : ['input', 'configuration', 'authentication_required'].includes(kind) ? 2 : 1
  }
}

if (require.main === module) run()
module.exports = { main, parseArgs }
