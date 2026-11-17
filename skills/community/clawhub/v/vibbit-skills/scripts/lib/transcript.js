'use strict'

const fs = require('node:fs')
const path = require('node:path')
const crypto = require('node:crypto')
const { parseJson } = require('./json')
const { publicUrl } = require('./media')
const { fileHash } = require('./production')

const object = value => value !== null && typeof value === 'object' && !Array.isArray(value)
const assert = (value, message) => { if (!value) throw new Error(message) }
const nonempty = value => typeof value === 'string' && value.trim().length > 0
const digest = text => crypto.createHash('sha256').update(text).digest('hex')
const decode = value => typeof value === 'string' ? parseJson(value) : value

function readInput(file) {
  const stat = fs.statSync(file)
  assert(stat.isFile() && stat.size <= 16 * 1024 * 1024, 'Transcript input must be a regular file of at most 16 MB')
  const text = fs.readFileSync(file, 'utf8')
  return { data: parseJson(text), sha256: digest(text) }
}

function readScript(file) {
  const stat = fs.statSync(file)
  assert(stat.isFile() && stat.size <= 256 * 1024, 'Script must be a UTF-8 file of at most 256 KB')
  return fs.readFileSync(file, 'utf8')
}

function normalizeTranscript(input, { timeUnit, sourceUrl, channelId, mediaFile, inputHash } = {}) {
  assert(object(input), 'Expected an ASR result object')
  assert(input.ok !== false && (input.code === undefined || input.code === 200), 'A failed API response is not transcription evidence')
  const envelope = object(input.data) ? input.data : input
  assert(envelope.status === undefined || envelope.status === 'COMPLETED', 'Use the completed ASR result, not a pending or failed task')
  let result = envelope.task_result ? decode(envelope.task_result.result)
    : Object.hasOwn(envelope, 'result') ? decode(envelope.result) : envelope
  assert(object(result), 'Missing structured transcription result')
  let rows, text, channel, format
  if (Array.isArray(result.transcripts)) {
    assert(result.transcripts.length > 0, 'No transcription tracks returned; inspect the task before concluding silence')
    const tracks = channelId === undefined ? result.transcripts
      : result.transcripts.filter(track => String(track.channel_id) === String(channelId))
    assert(tracks.length === 1, 'Select one actual --channel-id when multiple transcription tracks exist')
    const track = tracks[0]
    assert(object(track) && Array.isArray(track.sentences), 'Missing ASR sentences')
    rows = track.sentences
    text = track.text
    channel = track.channel_id
    format = 'vibbit_audio_asr'
    assert(timeUnit === undefined || timeUnit === 'milliseconds', 'Audio ASR begin_time/end_time are milliseconds')
    timeUnit = 'milliseconds'
  } else {
    assert(channelId === undefined, '--channel-id applies only to audio ASR tracks')
    if (Array.isArray(result.sub_results)) {
      const matches = result.sub_results.filter(row => row.task_type === 'asr')
      assert(matches.length === 1 && ['GENERATED', 'COMPLETED', 'SUCCESS'].includes(matches[0].status), 'Use a successful video ASR sub-result')
      result = decode(matches[0].result)
    }
    assert(object(result) && Array.isArray(result.items), 'Expected audio transcripts or video ASR items')
    assert(['seconds', 'milliseconds'].includes(timeUnit), 'Video ASR requires its confirmed --time-unit seconds or milliseconds')
    rows = result.items
    format = 'vibbit_video_asr'
  }
  const reportedUrl = format === 'vibbit_audio_asr' ? result.file_url : undefined
  if (reportedUrl && sourceUrl) assert(reportedUrl === sourceUrl, 'Requested source URL differs from the ASR source URL')
  sourceUrl = sourceUrl || reportedUrl
  assert(nonempty(sourceUrl), 'A source URL is required to associate the transcript with its media')
  publicUrl(sourceUrl, 'source URL')
  const issues = []
  const factor = timeUnit === 'milliseconds' ? 1000 : 1
  function interval(begin, end, location, word = false) {
    const original = { begin_time: begin, end_time: end }
    if (!Number.isFinite(begin) || !Number.isFinite(end) || begin < 0 || end < begin) {
      issues.push({ code: 'missing_or_invalid_time', ...location })
      return { original }
    }
    if (begin === end) issues.push({ code: word ? 'zero_duration_word' : 'zero_duration_sentence', ...location })
    return { original, start: begin / factor, end: end / factor }
  }
  const ids = new Set()
  const sentences = rows.map((row, index) => {
    assert(object(row) && typeof (row.text ?? row.content) === 'string', 'Sentence text is missing at ' + index)
    const id = String(row.sentence_id ?? `segment-${index}`)
    assert(!ids.has(id), 'Duplicate sentence ID: ' + id)
    ids.add(id)
    const timing = interval(row.begin_time ?? row.from, row.end_time ?? row.to, { sentence_id: id })
    assert(row.words === undefined || Array.isArray(row.words), 'Sentence words must be an array')
    const words = (row.words || []).map((word, wordIndex) => {
      assert(object(word) && typeof word.text === 'string', 'Invalid word text')
      assert(word.punctuation === undefined || typeof word.punctuation === 'string', 'Invalid word punctuation')
      return { text: word.text, punctuation: word.punctuation || '',
        ...interval(word.begin_time, word.end_time, { sentence_id: id, word_index: wordIndex }, true) }
    })
    return { id, text: row.text ?? row.content, ...timing, words,
      ...(row.language ? { language: row.language } : {}),
      ...(row.emotion ? { emotion: row.emotion } : {}) }
  })
  return {
    version: 1, kind: 'speech_transcript', time_unit: 'seconds', source_time_unit: timeUnit,
    source: { url: sourceUrl,
      ...(typeof envelope.task_id === 'string' && envelope.task_id.startsWith('task-') ? { task_id: envelope.task_id } : {}),
      ...(mediaFile ? { media: { path: path.resolve(mediaFile), ...fileHash(mediaFile) } } : {}) },
    ...(channel !== undefined ? { channel_id: channel } : {}),
    text: typeof text === 'string' ? text : sentences.map(row => row.text).join('\n'),
    sentences, issues, raw_result: result,
    provenance: { format, ...(inputHash ? { input_sha256: inputHash } : {}),
      media_association: mediaFile ? 'operator_associated_file_hash' : 'source_url_only',
      acoustic_verification: 'not_performed' },
  }
}

function validateTranscript(record) {
  assert(object(record) && record.version === 1 && record.kind === 'speech_transcript'
    && record.time_unit === 'seconds' && object(record.source) && nonempty(record.source.url)
    && typeof record.text === 'string' && Array.isArray(record.sentences), 'Expected a normalized speech_transcript in seconds')
  publicUrl(record.source.url, 'source URL')
  const ids = new Set()
  for (const row of record.sentences) {
    assert(object(row) && nonempty(row.id) && typeof row.text === 'string' && Array.isArray(row.words), 'Invalid normalized sentence')
    assert(!ids.has(row.id), 'Duplicate normalized sentence ID')
    ids.add(row.id)
  }
  return record
}

const positiveTime = row => Number.isFinite(row.start) && Number.isFinite(row.end) && row.start >= 0 && row.end > row.start
function timestamp(seconds, separator) {
  const total = Math.round(seconds * 1000)
  assert(Number.isSafeInteger(total) && total >= 0, 'Invalid subtitle timestamp')
  const pad = (value, length) => String(value).padStart(length, '0')
  return pad(Math.floor(total / 3600000), 2) + ':' + pad(Math.floor(total / 60000) % 60, 2)
    + ':' + pad(Math.floor(total / 1000) % 60, 2) + separator + pad(total % 1000, 3)
}

function captionText(text) {
  assert(nonempty(text) && !/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/.test(text), 'Invalid or empty caption text')
  return text.replace(/\r\n?/g, '\n').split('\n').map(line => line.trim()).filter(Boolean).join('\n')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

function exportSubtitles(record, { format = 'srt', display, transcriptHash } = {}) {
  validateTranscript(record)
  assert(['srt', 'vtt'].includes(format), 'Subtitle format must be srt or vtt')
  assert(record.sentences.length > 0, 'No sentences available for subtitle export')
  const replacements = new Map()
  if (display) {
    assert(object(display) && display.version === 1 && Array.isArray(display.cues)
      && nonempty(transcriptHash) && display.transcript_sha256 === transcriptHash, 'Display captions belong to a different transcript file')
    const ids = new Set(record.sentences.map(row => row.id))
    for (const cue of display.cues) {
      assert(object(cue) && ids.has(cue.id) && !replacements.has(cue.id), 'Unknown or repeated display sentence ID')
      assert(nonempty(cue.text) && (cue.translation === undefined || nonempty(cue.translation)), 'Display text must be nonempty')
      replacements.set(cue.id, cue)
    }
  }
  let previousEnd = 0
  const cues = record.sentences.map((row, index) => {
    assert(positiveTime(row) && row.start >= previousEnd, 'Subtitle sentences need positive, ordered, non-overlapping times; inspect sentence ' + row.id)
    assert(Math.round(row.end * 1000) > Math.round(row.start * 1000), 'Subtitle duration rounds to zero at ' + row.id)
    previousEnd = row.end
    const correction = replacements.get(row.id)
    const text = correction ? correction.text + (correction.translation ? '\n' + correction.translation : '') : row.text
    const separator = format === 'srt' ? ',' : '.'
    return `${index + 1}\n${timestamp(row.start, separator)} --> ${timestamp(row.end, separator)}\n${captionText(text)}`
  })
  return (format === 'vtt' ? 'WEBVTT\n\n' : '') + cues.join('\n\n') + '\n'
}

function exportWords(record) {
  validateTranscript(record)
  const words = []
  let previousStart = -1, previousEnd = -1
  for (const row of record.sentences) {
    const sentenceTokens = tokens(row.text).items.map(token => token.value)
    const wordText = []
    for (const word of row.words) {
      assert(object(word) && nonempty(word.text) && positiveTime(word), 'Word timing is missing or zero-duration; inspect the audio instead of interpolating')
      assert(word.punctuation === undefined || typeof word.punctuation === 'string', 'Invalid word punctuation')
      assert(word.start >= previousStart && word.end >= previousEnd, 'Word timing is not in spoken order')
      if (Number.isFinite(row.start) && Number.isFinite(row.end)) {
        assert(word.start >= row.start && word.end <= row.end, 'Word timing falls outside its sentence')
      }
      previousStart = word.start; previousEnd = word.end
      const text = word.text + (word.punctuation || '')
      wordText.push(text)
      words.push({ text, start: word.start, end: word.end, punctuation: word.punctuation || '' })
    }
    const wordTokens = wordText.flatMap(text => tokens(text).items.map(token => token.value))
    assert(sentenceTokens.join('') === wordTokens.join(''),
      'Word text does not cover the sentence; inspect missing words instead of exporting partial timing')
  }
  assert(words.length > 0, 'No real word timing available; sentence timing cannot be distributed into words')
  return { version: 1, time_unit: 'seconds', words,
    ...(record.source.media ? { media_sha256: record.source.media.sha256 } : {}),
    provenance: { transcript_source: record.source, acoustic_verification: 'not_performed' } }
}

function tokens(text) {
  const normalized = text.normalize('NFKC').toLocaleLowerCase('en-US')
  const regex = /[+-]?\p{N}+(?:[.,:/]\p{N}+)*|[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}]|\p{Script=Latin}[\p{Script=Latin}\p{M}\p{N}]*|[\p{L}\p{M}]+/gu
  const items = [...normalized.matchAll(regex)].map(match => ({ value: match[0], start: match.index, end: match.index + match[0].length }))
  return { text: normalized, items }
}

function compareScript(record, script) {
  validateTranscript(record)
  assert(nonempty(script), 'Adopted script must be nonempty')
  const expected = tokens(script), actual = tokens(record.text)
  const a = expected.items, b = actual.items
  assert(a.length > 0, 'Adopted script must contain spoken text')
  assert((a.length + 1) * (b.length + 1) <= 4000000, 'Compare long recordings by adopted passage; token comparison exceeds its bounded local limit')
  const width = b.length + 1
  const lcs = new Uint32Array((a.length + 1) * width)
  for (let i = a.length - 1; i >= 0; i--) for (let j = b.length - 1; j >= 0; j--) {
    lcs[i * width + j] = a[i].value === b[j].value ? 1 + lcs[(i + 1) * width + j + 1]
      : Math.max(lcs[(i + 1) * width + j], lcs[i * width + j + 1])
  }
  const mapped = record.sentences.flatMap(row => tokens(row.text).items.map(() => row))
  const mapValues = record.sentences.flatMap(row => tokens(row.text).items.map(token => token.value))
  const canLocate = mapValues.length === b.length && mapValues.every((value, index) => value === b[index].value)
  const differences = []
  const slice = (data, from, to) => from === to ? '' : data.text.slice(data.items[from].start, data.items[to - 1].end)
  let i = 0, j = 0
  while (i < a.length || j < b.length) {
    if (i < a.length && j < b.length && a[i].value === b[j].value) { i++; j++; continue }
    const fromA = i, fromB = j
    while (i < a.length || j < b.length) {
      if (i < a.length && j < b.length && a[i].value === b[j].value) break
      if (j >= b.length || (i < a.length && lcs[(i + 1) * width + j] >= lcs[i * width + j + 1])) i++
      else j++
    }
    const contextRows = canLocate ? [...new Set(j > fromB ? mapped.slice(fromB, j)
      : mapped.slice(Math.max(0, fromB - 1), Math.min(mapped.length, fromB + 1)))] : []
    differences.push({ kind: fromA === i ? 'extra_recognized_text' : fromB === j ? 'missing_from_recognition' : 'different_recognized_text',
      expected: slice(expected, fromA, i), recognized: slice(actual, fromB, j),
      locations: contextRows.map(row => ({ sentence_id: row.id, text: row.text,
        ...(positiveTime(row) ? { start: row.start, end: row.end } : {}) })), location_precision: 'sentence_context' })
  }
  return { version: 1, kind: 'speech_check', source: record.source, time_unit: 'seconds',
    status: differences.length ? 'review_needed' : 'matches_recognized_text',
    differences, script_sha256: digest(script), acoustic_verification: 'not_performed',
    automatic_regeneration: false,
    note: 'Text differences are listening leads, not proof of spoken errors. Numbers pronounced as words and phonetic variants may differ.' }
}

function locateSpeech(record, query) {
  validateTranscript(record)
  assert(nonempty(query) && query.length <= 256, 'Query must contain 1..256 characters')
  const needle = query.normalize('NFKC').toLocaleLowerCase('en-US')
  return { version: 1, kind: 'speech_locations', source: record.source, time_unit: 'seconds', match_mode: 'literal_substring',
    items: record.sentences.filter(row => row.text.normalize('NFKC').toLocaleLowerCase('en-US').includes(needle))
      .map(row => ({ sentence_id: row.id, text: row.text, ...(positiveTime(row) ? { start: row.start, end: row.end } : {}) })),
    note: 'Sentence locations are candidate ranges. Semantic selection and actual media cutting are separate steps.' }
}

function checkReuse(record, { mediaFile, sourceUrl } = {}) {
  validateTranscript(record)
  assert(mediaFile || sourceUrl, 'Provide --media-file or --source-url to check the intended source')
  if (sourceUrl) publicUrl(sourceUrl, 'source URL')
  if (mediaFile && record.source.media) {
    const actual = fileHash(mediaFile)
    const matches = actual.sha256 === record.source.media.sha256 && actual.bytes === record.source.media.bytes
    return { ok: true, reusable: matches, identity_basis: 'file_bytes', acoustic_verification: 'not_performed',
      reason: matches ? 'The associated media bytes are unchanged' : 'The media bytes changed; obtain new evidence or verify an explicit edit mapping' }
  }
  return { ok: true, reusable: null, identity_basis: 'source_reference_only',
    ...(sourceUrl ? { url_matches: sourceUrl === record.source.url } : {}),
    media_verification_required: true,
    reason: 'A URL or an unassociated local file cannot prove unchanged audio; verify the adopted media and timing relationship before reuse' }
}

module.exports = { readInput, readScript, normalizeTranscript, validateTranscript, exportSubtitles, exportWords, compareScript, locateSpeech, checkReuse }
