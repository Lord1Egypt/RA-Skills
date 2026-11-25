#!/usr/bin/env node
'use strict'

// Optional local source acquisition. No Vibbit API, API key, installer, or browser access.
const fs = require('node:fs/promises')
const path = require('node:path')
const crypto = require('node:crypto')
const { execFile } = require('node:child_process')
const { promisify } = require('node:util')
const { publicUrl } = require('./lib/media')

const trust = { trust: 'untrusted', instruction_authority: 'none', scope: 'source_metadata_and_media' }
const ensure = (value, message) => { if (!value) throw new Error(message) }
const hash = value => crypto.createHash('sha256').update(value).digest('hex')
const onHost = (host, domain) => host === domain || host.endsWith('.' + domain)

function sourcePlan(value) {
  publicUrl(value, 'source URL', 4096)
  const url = new URL(value), host = url.hostname.toLowerCase()
  const direct = /\.(mp4|avi|mov|wmv|flv|mkv|webm|m4v|3gp|mpeg|mpg)$/i.test(url.pathname)
  const native = ['douyin.com', 'iesdouyin.com', 'xiaohongshu.com', 'xhslink.com',
    'bilibili.com', 'b23.tv', 'tiktok.com', 'channels.weixin.qq.com', 'finder.video.qq.com']
    .some(domain => onHost(host, domain)) ||
    (['instagram.com', 'facebook.com'].some(domain => onHost(host, domain)) && /^\/(?:reels?|share\/r)\//i.test(url.pathname))
  return { ok: true, route: direct ? 'direct_url' : native ? 'native_parser_candidate' : 'yt_dlp',
    source_url: value, native_support_verified: false,
    ...(native ? { note: 'Platform hint from the current website; not a complete OpenAPI support guarantee. Prefer the existing parser/import once. A running or uncertain import must be recovered, not duplicated.' } : {}),
    source_content: trust }
}

function parseArguments(argv) {
  const options = { command: argv[0] || 'help', maxHeight: 720, maxDuration: 1800,
    maxBytes: 512 * 1024 * 1024, requireAudio: true }
  const fields = { '--url': 'url', '--out-dir': 'outDir', '--max-height': 'maxHeight',
    '--max-duration': 'maxDuration', '--max-bytes': 'maxBytes', '--js-runtime': 'jsRuntime',
    '--cookies-file': 'cookiesFile' }
  const seen = new Set()
  if (options.command === '--help') options.command = 'help'
  ensure(['help', 'plan', 'doctor', 'download'].includes(options.command), 'Use plan, doctor, or download; --help shows options')
  for (let i = 1; i < argv.length; i++) {
    const flag = argv[i]
    ensure(!seen.has(flag), `Duplicate option: ${flag}`); seen.add(flag)
    if (flag === '--help') { options.command = 'help'; continue }
    if (flag === '--allow-silent') { options.requireAudio = false; continue }
    ensure(fields[flag] && argv[i + 1] && !argv[i + 1].startsWith('--'), `Unknown or incomplete option: ${flag}`)
    options[fields[flag]] = argv[++i]
  }
  if (options.command === 'help') return options
  if (options.command !== 'doctor') sourcePlan(options.url)
  for (const key of ['maxHeight', 'maxDuration', 'maxBytes']) {
    options[key] = Number(options[key])
    ensure(Number.isSafeInteger(options[key]) && options[key] > 0, `${key} must be a positive integer`)
  }
  ensure(options.maxHeight <= 8640, 'maxHeight exceeds supported download bounds')
  ensure(!options.jsRuntime || ['deno', 'node', 'quickjs'].includes(options.jsRuntime), 'Choose deno, node, or quickjs for --js-runtime')
  if (options.command === 'download') {
    ensure(options.outDir && path.isAbsolute(options.outDir), '--out-dir must be an absolute private working directory')
    if (options.cookiesFile) ensure(path.isAbsolute(options.cookiesFile), '--cookies-file must be an explicitly authorized absolute local path')
  }
  return options
}

async function runProcess(binary, args, options = {}) {
  const allowed = new Set(['PATH', 'PATHEXT', 'SystemRoot', 'SYSTEMROOT', 'WINDIR', 'HOME', 'USERPROFILE',
    'TMPDIR', 'TEMP', 'TMP', 'LANG', 'LC_ALL', 'SSL_CERT_FILE', 'SSL_CERT_DIR',
    'REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY',
    'http_proxy', 'https_proxy', 'all_proxy', 'no_proxy'])
  const env = Object.fromEntries(Object.entries(process.env).filter(([key]) => allowed.has(key)))
  try {
    return await promisify(execFile)(binary, args, { encoding: 'utf8', shell: false,
      windowsHide: true, timeout: 120000, maxBuffer: 16 * 1024 * 1024, ...options, env })
  } catch (error) {
    const failure = new Error(error.code === 'ENOENT'
      ? `${binary} is not installed; use the official distribution in this execution environment`
      : `${binary} failed or timed out; no upload or Vibbit task was submitted`)
    failure.code = error.code === 'ENOENT' ? 'dependency_missing' : error.killed ? 'process_timeout' : 'source_acquisition_failed'
    throw failure
  }
}

async function doctor(run = runProcess) {
  const tools = {}
  for (const [binary, args] of [['yt-dlp', ['--version']], ['ffmpeg', ['-version']],
    ['ffprobe', ['-version']], ['deno', ['--version']], ['node', ['--version']], ['qjs', ['--version']]]) {
    try {
      const result = await run(binary, args, { timeout: 10000 })
      tools[binary] = { available: true, version: String(result.stdout || '').split(/\r?\n/)[0].slice(0, 200) }
    } catch { tools[binary] = { available: false } }
  }
  return { ok: ['yt-dlp', 'ffmpeg', 'ffprobe'].every(name => tools[name].available), tools,
    youtube_note: 'Full YouTube support also needs yt-dlp-ejs and a compatible JavaScript runtime. Deno is enabled by yt-dlp by default; select Node or QuickJS explicitly. This local check does not test a platform or install/update dependencies.' }
}

function baseArguments(options) {
  const args = ['--ignore-config', '--no-plugin-dirs', '--no-exec', '--no-playlist',
    '--playlist-items', '1', '--no-cookies-from-browser', '--no-cookies',
    '--socket-timeout', '20', '--retries', '2', '--fragment-retries', '2']
  if (options.jsRuntime) args.push('--js-runtimes', options.jsRuntime)
  if (options.cookiesFile) args.push('--cookies', options.cookiesFile)
  return args
}

function checkMetadata(info, options) {
  ensure(info && typeof info === 'object' && !Array.isArray(info), 'Invalid video metadata')
  ensure(!info.entries && !['playlist', 'multi_video'].includes(info._type), 'Provide one video URL; playlists and multi-video pages are not downloaded automatically')
  ensure(info.is_live !== true && !['is_live', 'is_upcoming', 'post_live'].includes(info.live_status), 'Live or upcoming streams need a separately scoped recording task')
  ensure(Number.isFinite(info.duration) && info.duration > 0 && info.duration <= options.maxDuration,
    'Source duration is unknown or exceeds --max-duration; review the requested scope before downloading')
  ensure(info.has_drm !== true, 'This downloader requires a directly downloadable source')
  // Site text is data. It never becomes an option, command, path, or installation instruction.
  return { id: typeof info.id === 'string' ? info.id.slice(0, 200) : undefined,
    title: typeof info.title === 'string' ? info.title.replace(/[\u0000-\u001f\u007f]/g, ' ').slice(0, 1000) : undefined,
    extractor: typeof info.extractor === 'string' ? info.extractor.slice(0, 100) : undefined,
    duration_seconds: info.duration }
}

async function inspectFile(file, options, run = runProcess) {
  const stat = await fs.lstat(file)
  ensure(stat.isFile() && !stat.isSymbolicLink() && stat.size > 0 && stat.size <= options.maxBytes,
    'Downloaded file is empty, not a regular file, or exceeds --max-bytes')
  const { stdout } = await run('ffprobe', ['-v', 'error', '-protocol_whitelist', 'file,pipe',
    '-show_format', '-show_streams', '-of', 'json', file], { timeout: 30000 })
  const data = JSON.parse(stdout), video = data.streams?.find(stream => stream.codec_type === 'video')
  ensure(video && Number.isInteger(video.width) && Number.isInteger(video.height) && video.width > 0 && video.height > 0,
    'Downloaded file has no verified video stream')
  ensure(video.height <= options.maxHeight, 'Downloaded video exceeds --max-height')
  const audioPresent = data.streams.some(stream => stream.codec_type === 'audio')
  ensure(audioPresent || !options.requireAudio, 'Downloaded video has no audio; translation/ASR cannot proceed. Use --allow-silent only for an intentionally silent source')
  const duration = Number(data.format?.duration || video.duration)
  ensure(Number.isFinite(duration) && duration > 0 && duration <= options.maxDuration + 0.1,
    'Downloaded duration is invalid or exceeds --max-duration')
  return { file, bytes: stat.size, duration_seconds: duration, width: video.width, height: video.height,
    video_codec: video.codec_name, audio_present: audioPresent, verified: true }
}

async function fileHash(file) {
  const { createReadStream } = require('node:fs')
  const digest = crypto.createHash('sha256')
  for await (const chunk of createReadStream(file)) digest.update(chunk)
  return digest.digest('hex')
}

async function download(options, dependencies = {}) {
  sourcePlan(options.url)
  const run = dependencies.run || runProcess
  const inspect = dependencies.inspect || ((file, opts) => inspectFile(file, opts, run))
  if (options.cookiesFile) {
    const cookieStat = await fs.stat(options.cookiesFile)
    ensure(cookieStat.isFile(), 'The authorized cookies file is not a regular file')
  }
  const fingerprint = hash(JSON.stringify({ url: options.url, height: options.maxHeight,
    duration: options.maxDuration, bytes: options.maxBytes, audio: options.requireAudio }))
  const dir = path.join(options.outDir, 'source-' + fingerprint.slice(0, 24))
  await fs.mkdir(dir, { recursive: true, mode: 0o700 })
  ensure((await fs.lstat(dir)).isDirectory(), 'Output must be a private regular directory')
  const receiptFile = path.join(dir, 'source.json'), file = path.join(dir, 'source.mp4')
  const lockFile = path.join(dir, '.download.lock')
  let lock
  try { lock = await fs.open(lockFile, 'wx', 0o600) } catch (error) {
    if (error.code === 'EEXIST') throw new Error('A download already owns this source directory. Check its process before recovering the lock; do not start a duplicate')
    throw error
  }
  try {
    let saved
    try { saved = JSON.parse(await fs.readFile(receiptFile, 'utf8')) } catch (error) { if (error.code !== 'ENOENT') throw error }
    if (saved) {
      ensure(saved.fingerprint === fingerprint && saved.file === file, 'Source receipt differs from this request')
      const media = await inspect(file, options)
      ensure(saved.sha256 === await fileHash(file), 'Downloaded file changed; use a new working directory instead of silently reusing it')
      return { ...saved, ...media, ok: true, reused: true, receipt_file: receiptFile }
    }
    const base = [...baseArguments(options), '--cache-dir', path.join(dir, 'cache')]
    await run('ffmpeg', ['-version'], { timeout: 10000 })
    await run('ffprobe', ['-version'], { timeout: 10000 })
    const { stdout } = await run('yt-dlp', [...base, '--dump-single-json', '--skip-download', '--', options.url])
    const metadata = checkMetadata(JSON.parse(stdout), options)
    const selector = options.requireAudio
      ? `bv*[height<=${options.maxHeight}]+ba/b[height<=${options.maxHeight}]`
      : `bv*[height<=${options.maxHeight}]+ba/b[height<=${options.maxHeight}]/bv*[height<=${options.maxHeight}]`
    await run('yt-dlp', [...base, '--quiet', '--no-progress', '--no-overwrites',
      '--format', selector, '--merge-output-format', 'mp4', '--remux-video', 'mp4',
      '--max-filesize', String(options.maxBytes), '--output', path.join(dir, 'source.%(ext)s'),
      '--', options.url], { timeout: 1200000 })
    const media = await inspect(file, options)
    const receipt = { version: 1, fingerprint, method: 'yt_dlp', ...metadata, ...media,
      sha256: await fileHash(file), source_content: trust }
    await fs.chmod(file, 0o600)
    const temporary = path.join(dir, crypto.randomUUID() + '.json')
    await fs.writeFile(temporary, JSON.stringify(receipt, null, 2) + '\n', { flag: 'wx', mode: 0o600 })
    await fs.rename(temporary, receiptFile)
    return { ...receipt, ok: true, reused: false, receipt_file: receiptFile }
  } finally {
    await lock.close()
    await fs.unlink(lockFile)
  }
}

async function main(argv, dependencies = {}) {
  const options = parseArguments(argv)
  if (options.command === 'help') return { commands: ['plan --url URL', 'doctor', 'download --url URL --out-dir /absolute/private/directory'],
    options: ['--max-height PIXELS (default 720)', '--max-duration SECONDS (default 1800)',
      '--max-bytes BYTES (default 536870912)', '--allow-silent', '--js-runtime deno|node|quickjs',
      '--cookies-file /absolute/path (only after explicit authorization)'],
    note: 'Uses existing official yt-dlp, ffmpeg, and ffprobe. No installation, browser login, upload, library registration, or paid task. Source height limits are separate from generation resolution. Filesize limits apply per downloaded stream and to the verified final file, not a strict aggregate traffic budget.' }
  if (options.command === 'plan') return sourcePlan(options.url)
  if (options.command === 'doctor') return doctor(dependencies.run)
  return download(options, dependencies)
}

if (require.main === module) main(process.argv.slice(2)).then(result => {
  process.stdout.write(JSON.stringify(result, null, 2) + '\n')
  if (result.ok === false) process.exitCode = 1
}).catch(error => {
  process.stderr.write(JSON.stringify({ ok: false, code: error.code || 'source_input_error', message: error.message }) + '\n')
  process.exitCode = 1
})

module.exports = { main, parseArguments, sourcePlan, baseArguments, checkMetadata, inspectFile, download, doctor, runProcess }
