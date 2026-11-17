#!/usr/bin/env node
'use strict'

const { writeJson, planRun, recordOutput, importTiming, bindEvents } = require('./lib/production')

const OPTIONS = {
  plan: ['run', 'out'],
  explain: ['run', 'out'],
  record: ['run', 'output-id', 'file', 'task-id', 'result-id', 'out'],
  'import-timing': ['file', 'transcript', 'language', 'out'],
  bind: ['run', 'out'],
}

function parseArgs(argv) {
  const [command = 'help', ...rest] = argv
  if (['help', '--help', '-h'].includes(command)) return { command: 'help', flags: {} }
  if (!Object.hasOwn(OPTIONS, command)) throw new Error('Unknown production command: ' + command)
  const flags = {}
  for (let i = 0; i < rest.length; i += 2) {
    const name = rest[i].slice(2)
    if (!rest[i].startsWith('--') || !OPTIONS[command].includes(name)) throw new Error('Unknown option: ' + rest[i])
    if (Object.hasOwn(flags, name)) throw new Error('Repeated option: ' + rest[i])
    if (!rest[i + 1] || rest[i + 1].startsWith('--')) throw new Error('Missing value: ' + rest[i])
    flags[name] = rest[i + 1]
  }
  return { command, flags }
}

async function main(argv) {
  const { command, flags: f } = parseArgs(argv)
  if (command === 'help') return { tool: 'Vibbit local production records', commands: {
    plan: '--run run.json [--out new-plan.json]',
    explain: '--run run.json [--out new-diagnosis.json] (read-only; blocked selections stay selected)',
    record: '--run run.json --output-id ID --file media [--task-id ID] [--result-id ID] --out new-receipt.json',
    'import-timing': '--file media --transcript words.json --language zh --out new-timing.json',
    bind: '--run run.json [--out new-events.json]',
  }, behavior: 'Local files only. No API submission, install, media generation, transcription, or rendering. Output paths must be new.' }
  function need(...keys) { for (const key of keys) if (!f[key]) throw new Error('--' + key + ' is required') }
  let result
  if (command === 'plan') { need('run'); result = planRun(f.run) }
  if (command === 'explain') { need('run'); result = planRun(f.run, true) }
  if (command === 'record') {
    need('run', 'output-id', 'file', 'out')
    result = recordOutput(f.run, f['output-id'], f.file, {
      ...(f['task-id'] ? { task_id: f['task-id'] } : {}), ...(f['result-id'] ? { result_id: f['result-id'] } : {}),
      attribution: 'operator_provided',
    })
  }
  if (command === 'import-timing') {
    need('file', 'transcript', 'language', 'out')
    result = importTiming(f.file, f.transcript, f.language)
    const info = await require('./lib/media').probeLocal(f.file)
    const duration = Number(info.format?.duration)
    if (!info.streams?.some(stream => stream.codec_type === 'audio') || !Number.isFinite(duration) || duration <= 0) throw new Error('Word timing requires media with a measured duration and audio stream')
    if (result.words.some(word => word.end > duration + 0.001)) throw new Error('Word timing extends beyond the actual media duration')
    result.media.duration_seconds = duration
    result.provenance.media_probe = 'ffprobe'
  }
  if (command === 'bind') { need('run'); result = bindEvents(f.run) }
  if (f.out) { writeJson(f.out, result); return { ok: true, output: require('node:path').resolve(f.out), kind: result.kind || command } }
  return result
}

if (require.main === module) {
  main(process.argv.slice(2)).then(result => process.stdout.write(JSON.stringify(result, null, 2) + '\n'))
    .catch(error => { process.stderr.write(JSON.stringify({ ok: false, error: error.message, ...(error.details ? { details: error.details } : {}) }) + '\n'); process.exitCode = 2 })
}

module.exports = { main, parseArgs }
