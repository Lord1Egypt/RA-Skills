#!/usr/bin/env node
'use strict'

const fs = require('node:fs')
const path = require('node:path')
const { fileHash } = require('./lib/production')
const transcript = require('./lib/transcript')

const OPTIONS = {
  normalize: ['input', 'time-unit', 'source-url', 'channel-id', 'media-file', 'out'],
  text: ['input', 'out'],
  subtitles: ['input', 'format', 'display', 'out'],
  words: ['input', 'out'],
  compare: ['input', 'script', 'out'],
  locate: ['input', 'query', 'out'],
  reuse: ['input', 'media-file', 'source-url', 'out'],
}

function parseArgs(argv) {
  const [command = 'help', ...args] = argv
  if (['help', '--help', '-h'].includes(command)) return { command: 'help', flags: {} }
  if (!Object.hasOwn(OPTIONS, command)) throw new Error('Unknown transcript command: ' + command)
  const flags = {}
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].slice(2)
    if (!args[i].startsWith('--') || !OPTIONS[command].includes(key)) throw new Error('Unknown option: ' + args[i])
    if (Object.hasOwn(flags, key) || !args[i + 1] || args[i + 1].startsWith('--')) throw new Error('Repeated or missing option value: ' + args[i])
    flags[key] = args[i + 1]
  }
  return { command, flags }
}

function main(argv) {
  const { command, flags: f } = parseArgs(argv)
  if (command === 'help') return { tool: 'Vibbit local transcript utilities', commands: {
    normalize: '--input completed-asr.json [--media-file audio] [--source-url URL] [--channel-id ID] [--time-unit seconds|milliseconds (video ASR only)] --out transcript.json',
    text: '--input transcript.json --out recognized.txt',
    subtitles: '--input transcript.json --format srt|vtt [--display display.json] --out captions.srt',
    words: '--input transcript.json --out words.json',
    compare: '--input transcript.json --script adopted.txt [--out check.json]',
    locate: '--input transcript.json --query WORDS [--out locations.json]',
    reuse: '--input transcript.json (--media-file audio | --source-url URL) [--out reuse.json]',
  }, behavior: 'Local data only. No API calls, media downloads, generation, cutting, acoustic checks, or installation. Outputs must be new; ASR milliseconds are converted to seconds.' }
  function need(...keys) { for (const key of keys) if (!f[key]) throw new Error('--' + key + ' is required') }
  need('input')
  if (['normalize', 'text', 'subtitles', 'words'].includes(command)) need('out')
  const input = transcript.readInput(f.input)
  let result
  if (command === 'normalize') result = transcript.normalizeTranscript(input.data, {
    timeUnit: f['time-unit'], sourceUrl: f['source-url'], channelId: f['channel-id'],
    mediaFile: f['media-file'], inputHash: input.sha256,
  })
  if (command === 'subtitles') result = transcript.exportSubtitles(input.data, {
    format: f.format, display: f.display ? transcript.readInput(f.display).data : undefined, transcriptHash: input.sha256,
  })
  if (command === 'text') result = transcript.validateTranscript(input.data).text + '\n'
  if (command === 'words') result = transcript.exportWords(input.data)
  if (command === 'compare') { need('script'); result = transcript.compareScript(input.data, transcript.readScript(f.script)) }
  if (command === 'locate') { need('query'); result = transcript.locateSpeech(input.data, f.query) }
  if (command === 'reuse') result = transcript.checkReuse(input.data, { mediaFile: f['media-file'], sourceUrl: f['source-url'] })
  if (!f.out) return result
  fs.writeFileSync(f.out, typeof result === 'string' ? result : JSON.stringify(result, null, 2) + '\n', { flag: 'wx', mode: 0o600 })
  return { ok: true, output: path.resolve(f.out), kind: typeof result === 'string' ? (command === 'text' ? 'text' : f.format || 'srt') : result.kind || command, ...fileHash(f.out) }
}

if (require.main === module) {
  try { process.stdout.write(JSON.stringify(main(process.argv.slice(2)), null, 2) + '\n') }
  catch (error) { process.stderr.write(JSON.stringify({ ok: false, error: error.message }) + '\n'); process.exitCode = 2 }
}

module.exports = { main, parseArgs }
