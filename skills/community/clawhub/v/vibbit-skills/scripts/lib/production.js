'use strict'

const fs = require('node:fs')
const path = require('node:path')
const crypto = require('node:crypto')

const assert = (value, message) => { if (!value) throw new Error(message) }
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value)
const nonempty = value => typeof value === 'string' && value.trim().length > 0
const own = (value, key) => Object.hasOwn(value, key)
const digest = value => crypto.createHash('sha256').update(value).digest('hex')
function normalize(value) {
  const chars = [...value.normalize('NFKC').toLocaleLowerCase('en-US')]
  return chars.filter((ch, i) => /[\p{L}\p{N}]/u.test(ch)
    || (/[.,:/]/.test(ch) && /\p{N}/u.test(chars[i - 1] || '') && /\p{N}/u.test(chars[i + 1] || ''))
    || (/[+-]/.test(ch) && /\p{N}/u.test(chars[i + 1] || ''))).join('')
}

function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical)
  if (object(value)) return Object.fromEntries(Object.keys(value).sort().map(key => [key, canonical(value[key])]))
  return value
}

function readJson(file) {
  const stat = fs.statSync(file)
  assert(stat.isFile() && stat.size <= 16 * 1024 * 1024, 'JSON input must be a regular file of at most 16 MB')
  return JSON.parse(fs.readFileSync(file, 'utf8'))
}

function fileHash(file) {
  const stat = fs.statSync(file)
  assert(stat.isFile() && stat.size > 0, 'Media/input file must be a non-empty regular file: ' + file)
  // Stream synchronously in bounded chunks; videos need not fit into memory.
  const hash = crypto.createHash('sha256')
  const buffer = Buffer.alloc(1024 * 1024)
  const fd = fs.openSync(file, 'r')
  try {
    let length
    while ((length = fs.readSync(fd, buffer, 0, buffer.length, null)) > 0) hash.update(buffer.subarray(0, length))
  } finally { fs.closeSync(fd) }
  return { sha256: hash.digest('hex'), bytes: stat.size }
}

function writeJson(file, data) {
  // An explicit new file preserves earlier receipts and timing evidence.
  fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n', { flag: 'wx', mode: 0o600 })
}

function readPath(root, reference) {
  assert(nonempty(reference), 'Expected a local file path')
  assert(!/^[a-z][a-z0-9+.-]*:\/\//i.test(reference), 'Local production records require local files, not URLs')
  return path.resolve(root, reference)
}

function loadRun(runFile) {
  const runPath = path.resolve(runFile)
  const run = readJson(runPath)
  assert(object(run) && run.version === 1, 'Run version must be 1')
  const projectPath = readPath(path.dirname(runPath), run.project)
  const project = readJson(projectPath)
  assert(object(project) && project.version === 1 && nonempty(project.id), 'Project needs version 1 and a stable id')
  assert(object(project.outputs) && Object.keys(project.outputs).length > 0, 'Project outputs must be a non-empty object')
  assert(Array.isArray(run.targets) && run.targets.length > 0 && new Set(run.targets).size === run.targets.length, 'Run needs unique targets')
  assert(run.selections === undefined || object(run.selections), 'Run selections must be an object')
  for (const id of [...run.targets, ...Object.keys(run.selections || {})]) assert(own(project.outputs, id), 'Unknown output: ' + id)
  return { runPath, projectPath, runRoot: path.dirname(runPath), projectRoot: path.dirname(projectPath), run, project }
}

function selectedValue(project, reference) {
  assert(nonempty(reference), 'Output uses entries must be non-empty field paths')
  const keys = reference.split('.')
  assert(['script', 'direction', 'events'].includes(keys[0]), 'uses must reference script, direction, or events')
  let value = project
  for (const key of keys) {
    assert(object(value) || Array.isArray(value), 'Invalid content reference: ' + reference)
    assert(own(value, key), 'Missing content reference: ' + reference)
    value = value[key]
  }
  return value
}

function changedInputs(previous, current) {
  if (!object(previous) || previous.version !== 1) return [{ kind: 'unknown', reason: 'Receipt predates input manifests; compare the original project and files.' }]
  const changes = []
  if (previous.spec !== current.spec) changes.push({ kind: 'definition' })
  for (const [group, kind] of [['fields', 'field'], ['files', 'file'], ['dependencies', 'dependency']]) {
    const before = previous[group] || {}, after = current[group]
    for (const key of new Set([...Object.keys(before), ...Object.keys(after)])) {
      if (JSON.stringify(canonical(before[key])) !== JSON.stringify(canonical(after[key]))) changes.push({ kind, path: key })
    }
  }
  return changes.length ? changes : [{ kind: 'unknown', reason: 'Fingerprint changed outside the recorded input summary.' }]
}

function planner(context, ignoredSelection, diagnostic = false) {
  const { project, run, projectRoot, runRoot } = context
  const visiting = new Set()
  const memo = new Map()
  function resolve(id) {
    if (memo.has(id)) return memo.get(id)
    assert(!visiting.has(id), 'Output dependency cycle at ' + id)
    assert(own(project.outputs, id), 'Unknown dependency: ' + id)
    visiting.add(id)
    const spec = project.outputs[id]
    assert(object(spec) && ['video', 'audio', 'image', 'data'].includes(spec.kind), 'Invalid output kind: ' + id)
    assert(object(spec.recipe) && ['vibbit', 'local'].includes(spec.recipe.tool), 'Output recipe needs tool vibbit or local: ' + id)
    if (spec.recipe.tool === 'vibbit') {
      const { commands } = require('./registry')
      assert(own(commands, spec.recipe.command), 'Unknown Vibbit command in recipe: ' + id)
    } else assert(nonempty(spec.recipe.instruction), 'Local recipe needs an execution instruction: ' + id)
    const deps = spec.depends_on || []
    const uses = spec.uses || []
    const files = spec.files || []
    for (const [name, values] of Object.entries({ depends_on: deps, uses, files })) {
      assert(Array.isArray(values) && values.every(nonempty) && new Set(values).size === values.length, `${id}.${name} needs unique strings`)
    }
    const dependencies = deps.map(resolve)
    const issues = []
    const inputs = Object.fromEntries(uses.map(ref => [ref, selectedValue(project, ref)]))
    const fileInputs = Object.fromEntries(files.map(file => {
      try { return [file, fileHash(readPath(projectRoot, file)).sha256] }
      catch (error) {
        if (!diagnostic) throw error
        issues.push({ code: 'input_file_unavailable', path: file, message: error.message })
        return [file, null]
      }
    }))
    const manifest = {
      version: 1, spec: digest(JSON.stringify(canonical(spec))),
      fields: Object.fromEntries(Object.entries(inputs).map(([key, value]) => [key, digest(JSON.stringify(canonical(value)))])),
      files: fileInputs,
      dependencies: Object.fromEntries(dependencies.map(dep => [dep.id, { fingerprint: dep.fingerprint, artifact: dep.selection?.artifact.sha256 || null }])),
    }
    const fingerprint = digest(JSON.stringify(canonical({
      project: project.id, output: id, spec, inputs, files: fileInputs,
      dependencies: dependencies.map(dep => ({ id: dep.id, fingerprint: dep.fingerprint, artifact: dep.selection?.artifact.sha256 || null })),
    })))
    let selection, selectedReceipt
    if (id !== ignoredSelection && own(run.selections || {}, id)) {
      const receiptPath = readPath(runRoot, run.selections[id])
      selectedReceipt = receiptPath
      try {
        const receipt = readJson(receiptPath)
        assert(receipt.version === 1 && receipt.project_id === project.id && receipt.output_id === id, 'Receipt belongs to another project/output: ' + id)
        if (receipt.fingerprint !== fingerprint) {
          const changes = changedInputs(receipt.input_manifest, manifest)
          const error = new Error('Stale selection for ' + id + '; changed: ' + changes.map(change => change.path || change.kind).join(', ') + '; review and explicitly replace/remove this selection')
          error.details = { code: 'stale_selection', output: id, changes }
          throw error
        }
        assert(object(receipt.artifact) && receipt.artifact.kind === spec.kind, 'Selected artifact kind differs: ' + id)
        const localPath = readPath(path.dirname(receiptPath), receipt.artifact.path)
        const checked = fileHash(localPath)
        assert(checked.sha256 === receipt.artifact.sha256 && checked.bytes === receipt.artifact.bytes, 'Selected file changed: ' + id)
        selection = { receipt: receiptPath, artifact: { ...receipt.artifact, path: localPath }, source: receipt.source }
      } catch (error) {
        if (!diagnostic) throw error
        issues.push({ ...(error.details || { code: 'selection_unavailable' }), message: error.message })
      }
    }
    const blockedDependencies = dependencies.filter(dep => dep.issues.length).map(dep => dep.id)
    if (blockedDependencies.length) issues.push({ code: 'dependency_blocked', outputs: blockedDependencies })
    if (issues.length) selection = undefined
    const result = { id, kind: spec.kind, fingerprint, dependencies, selection, selectedReceipt, issues, manifest, recipe: spec.recipe, files: fileInputs }
    memo.set(id, result)
    visiting.delete(id)
    return result
  }
  return resolve
}

function planRun(runFile, diagnostic = false) {
  const context = loadRun(runFile)
  const resolve = planner(context, undefined, diagnostic)
  const steps = []
  const emitted = new Set()
  function visit(node) {
    if (emitted.has(node.id)) return
    emitted.add(node.id)
    if (!node.selection) node.dependencies.forEach(visit)
    steps.push({ output: node.id, kind: node.kind, action: node.issues.length ? 'blocked' : node.selection ? 'reuse' : 'execute', fingerprint: node.fingerprint,
      ...(diagnostic ? { reason: node.issues.length ? 'review_required' : node.selection ? 'selected_file_and_declared_inputs_match' : 'no_selected_receipt',
        issues: node.issues, ...(node.selectedReceipt ? { selected_receipt: node.selectedReceipt } : {}) } : {}),
      ...(node.selection ? { artifact: node.selection.artifact, receipt: node.selection.receipt }
        : { recipe: node.recipe, depends_on: node.dependencies.map(dep => dep.id), file_hashes: node.files }),
    })
  }
  context.run.targets.map(resolve).forEach(visit)
  return { version: 1, mode: diagnostic ? 'read_only_diagnosis' : 'read_only_plan', project_id: context.project.id, project: context.projectPath,
    ...(diagnostic ? { ready_for_host_review: !steps.some(step => step.action === 'blocked') } : {}),
    targets: context.run.targets, steps, submitted: false,
    limitations: ['Only declared dependencies are checked.', 'Reuse verifies file identity and declared inputs, not creative quality.', 'The host executes the remaining steps using existing tools; this command submits nothing.'] }
}

function recordOutput(runFile, output, media, source = {}) {
  const context = loadRun(runFile)
  const node = planner(context, output)(output)
  assert(node.dependencies.every(dep => dep.selection), 'Record dependencies first and explicitly select them before recording ' + output)
  const localPath = path.resolve(media)
  return { version: 1, project_id: context.project.id, output_id: output, fingerprint: node.fingerprint, input_manifest: node.manifest,
    artifact: { kind: node.kind, path: localPath, ...fileHash(localPath) }, source,
    quality: 'not_checked_by_this_tool', created_at: new Date().toISOString() }
}

function importTiming(media, transcript, language) {
  assert(nonempty(language), 'An explicit language is required')
  const raw = readJson(transcript)
  assert(raw.version === 1 && raw.time_unit === 'seconds', 'Normalized timing input needs version 1 and time_unit seconds')
  const rows = raw.words
  assert(Array.isArray(rows) && rows.length > 0, 'No word-level timing found; segment timestamps are not word timing')
  let lastStart = -1
  let lastEnd = -1
  const words = []
  for (const [index, row] of rows.entries()) {
    assert(object(row), 'Invalid word at ' + index)
    const text = row.text
    assert(nonempty(text), 'Missing word text at ' + index)
    if (!normalize(text)) continue
    assert(Number.isFinite(row.start) && Number.isFinite(row.end) && row.start >= 0 && row.end > row.start, 'Missing/invalid word time at ' + index + '; do not interpolate unaligned words')
    assert(row.start >= lastStart && row.end >= lastEnd, 'Word timing must be in spoken order')
    lastStart = row.start; lastEnd = row.end
    words.push({ text, start: row.start, end: row.end, ...(Number.isFinite(row.score) ? { score: row.score } : {}) })
  }
  assert(words.length > 0, 'No timed speech words')
  const localPath = path.resolve(media)
  const mediaHash = fileHash(localPath)
  if (raw.media_sha256 !== undefined) assert(raw.media_sha256 === mediaHash.sha256, 'Transcript declares a different media hash')
  return { version: 1, kind: 'word_timing', time_unit: 'seconds', language,
    media: { path: localPath, ...mediaHash }, words,
    provenance: { format: 'normalized_words_v1', transcript_path: path.resolve(transcript), transcript_sha256: fileHash(transcript).sha256,
      media_association: raw.media_sha256 ? 'source_declared_hash_matched' : 'operator_declared',
      acoustic_verification: 'not_performed_by_importer' } }
}

function locatePhrase(words, speech, quote, occurrence) {
  assert(nonempty(speech) && nonempty(quote), 'Speech and event quote must be non-empty')
  const normalized = words.map(word => normalize(word.text))
  const heard = normalized.join('')
  assert(heard === normalize(speech), 'Adopted speech differs from timed words; inspect the media/transcript instead of guessing alignment')
  const needle = normalize(quote)
  assert(needle.length > 0, 'Event quote contains no spoken characters')
  let cursor = 0
  const starts = new Map(), ends = new Map()
  normalized.forEach((word, i) => { starts.set(cursor, i); cursor += word.length; ends.set(cursor, i) })
  const matches = []
  for (let at = heard.indexOf(needle); at !== -1; at = heard.indexOf(needle, at + 1)) {
    if (starts.has(at) && ends.has(at + needle.length)) matches.push([starts.get(at), ends.get(at + needle.length)])
  }
  assert(matches.length > 0, 'Event quote was not found on measured word boundaries: ' + quote)
  if (occurrence === undefined) assert(matches.length === 1, 'Repeated event quote requires an explicit occurrence: ' + quote)
  const selected = occurrence === undefined ? 1 : occurrence
  assert(Number.isSafeInteger(selected) && selected >= 1 && selected <= matches.length, 'Event occurrence is outside the matching range')
  const [first, last] = matches[selected - 1]
  return { start: words[first].start, end: words[last].end, word_range: [first, last], occurrence: selected }
}

function bindEvents(runFile) {
  const context = loadRun(runFile)
  const { project, run, runRoot } = context
  assert(object(project.script) && Array.isArray(project.events), 'Project needs script and events')
  assert(object(run.timing), 'Run needs timing placements')
  assert(Number.isFinite(project.frame_rate) && project.frame_rate > 0 && project.frame_rate <= 240, 'Project needs frame_rate in (0, 240]')
  const resolve = planner(context)
  const segments = new Map()
  const ids = new Set()
  const events = project.events.map(event => {
    assert(object(event) && nonempty(event.id) && !ids.has(event.id), 'Events need unique ids')
    ids.add(event.id)
    assert(own(project.script, event.segment), 'Unknown Script segment: ' + event.segment)
    if (!segments.has(event.segment)) {
      assert(own(run.timing, event.segment), 'Missing timing placement for ' + event.segment)
      const placement = run.timing[event.segment]
      assert(object(placement) && Number.isFinite(placement.at_seconds) && placement.at_seconds >= 0, 'Timing placement needs a non-negative at_seconds')
      const output = resolve(placement.output)
      assert(output.selection && ['video', 'audio'].includes(output.kind), 'Timing needs explicitly selected audio/video: ' + placement.output)
      const evidencePath = readPath(runRoot, placement.evidence)
      const evidence = readJson(evidencePath)
      assert(evidence.version === 1 && evidence.kind === 'word_timing' && evidence.time_unit === 'seconds', 'Invalid timing evidence')
      assert(evidence.media?.sha256 === output.selection.artifact.sha256, 'Timing belongs to different media: ' + event.segment)
      assert(Array.isArray(evidence.words) && evidence.words.length > 0, 'Empty word timing evidence')
      // Validate imported records again; a hand-edited evidence file must not bypass checks.
      let previous = { start: -1, end: -1 }
      for (const word of evidence.words) {
        assert(nonempty(word.text) && normalize(word.text) && Number.isFinite(word.start) && Number.isFinite(word.end)
          && word.start >= 0 && word.end > word.start && word.start >= previous.start && word.end >= previous.end, 'Invalid imported word timing')
        previous = word
      }
      if (evidence.media.duration_seconds !== undefined) assert(Number.isFinite(evidence.media.duration_seconds)
        && evidence.media.duration_seconds > 0 && previous.end <= evidence.media.duration_seconds + 0.001, 'Word timing exceeds media duration')
      segments.set(event.segment, { placement, evidence, evidencePath, hash: fileHash(evidencePath).sha256 })
    }
    const { placement, evidence } = segments.get(event.segment)
    const located = locatePhrase(evidence.words, project.script[event.segment].speech, event.quote, event.occurrence)
    assert(['range', 'moment'].includes(event.type), 'Event type must be range or moment')
    const offset = event.offset_seconds ?? 0
    assert(Number.isFinite(offset), 'Event offset_seconds must be finite')
    const start = placement.at_seconds + located.start + offset
    const end = placement.at_seconds + located.end + offset
    assert(start >= 0, 'Event begins before the program')
    const base = { id: event.id, segment: event.segment, quote: event.quote, occurrence: located.occurrence,
      type: event.type, media_sha256: evidence.media.sha256, evidence_sha256: segments.get(event.segment).hash }
    if (event.type === 'moment') {
      const edge = event.edge || 'start'
      assert(['start', 'end'].includes(edge), 'Moment edge must be start or end')
      const seconds = edge === 'start' ? start : end
      return { ...base, seconds, frame: Math.round(seconds * project.frame_rate) }
    }
    assert(event.edge === undefined, 'Range events do not have an edge')
    return { ...base, start_seconds: start, end_seconds: end, start_frame: Math.floor(start * project.frame_rate + 1e-7),
      end_frame_exclusive: Math.ceil(end * project.frame_rate - 1e-7) }
  })
  return { version: 1, kind: 'bound_events', project_id: project.id, frame_rate: project.frame_rate,
    project_sha256: fileHash(context.projectPath).sha256, run_sha256: fileHash(context.runPath).sha256,
    events, limitations: ['Word times are supplied evidence, not independently verified acoustic alignment.',
      'Ranges round outwards to frames; moments round to the nearest frame.', 'Placement assumes the selected media is not trimmed or retimed after alignment.'] }
}

module.exports = { readJson, fileHash, writeJson, planRun, recordOutput, importTiming, locatePhrase, bindEvents }
