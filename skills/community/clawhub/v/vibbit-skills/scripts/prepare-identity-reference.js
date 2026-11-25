#!/usr/bin/env node
'use strict'

// Local motion-reference preparation only. No API, credentials, model, or face detector.
const fs = require('node:fs')
const path = require('node:path')
const crypto = require('node:crypto')
const { spawn, execFileSync } = require('node:child_process')

function ensure(condition, message) {
  if (!condition) throw new Error(message)
}

function parseArguments(argv) {
  const args = { dryRun: false }
  for (let i = 0; i < argv.length; i++) {
    const flag = argv[i]
    if (flag === '--help') args.help = true
    else if (flag === '--dry-run') args.dryRun = true
    else if (flag === '--plan' || flag === '--out') {
      ensure(argv[i + 1] && !argv[i + 1].startsWith('--'), `${flag} needs a path`)
      const key = flag === '--plan' ? 'plan' : 'out'
      ensure(!args[key], `Duplicate ${flag}`)
      args[key] = path.resolve(argv[++i])
    } else throw new Error(`Unknown option: ${flag}`)
  }
  if (!args.help) ensure(args.plan && args.out, 'Use --plan PLAN.json --out REFERENCE.mp4')
  return args
}

function probeLocal(file) {
  ensure(fs.statSync(file).isFile(), 'Source must be a local regular file')
  const data = JSON.parse(execFileSync('ffprobe', [
    '-v', 'error', '-protocol_whitelist', 'file,pipe',
    '-show_entries', 'stream=codec_type,width,height,duration,codec_name,avg_frame_rate,nb_frames:stream_side_data=rotation:format=duration,size',
    '-of', 'json', file,
  ], { encoding: 'utf8', maxBuffer: 1024 * 1024 }))
  const video = data.streams?.find(stream => stream.codec_type === 'video')
  ensure(video, 'Source has no video stream')
  ensure(!(video.side_data_list || []).some(item => Number(item.rotation || 0) % 360),
    'Normalize source rotation before measuring head regions')
  const duration = Number(video.duration || data.format?.duration)
  ensure(Number.isFinite(duration) && duration > 0, 'Source duration is unavailable')
  ensure(Number.isInteger(video.width) && video.width >= 2 && video.width % 2 === 0 &&
    Number.isInteger(video.height) && video.height >= 2 && video.height % 2 === 0,
  'Normalize source to even pixel dimensions before tracking')
  return { width: video.width, height: video.height, duration_seconds: duration,
    video_codec: video.codec_name, source_audio_present: data.streams.some(s => s.codec_type === 'audio') }
}

function validatePlan(plan, media) {
  ensure(plan && typeof plan === 'object' && !Array.isArray(plan), 'Plan must be an object')
  ensure(Object.keys(plan).every(key => ['source_file', 'fps', 'tracks'].includes(key)), 'Unknown plan field')
  ensure(typeof plan.source_file === 'string' && path.isAbsolute(plan.source_file), 'source_file must be an absolute local path')
  const fps = plan.fps ?? 30
  ensure(Number.isInteger(fps) && fps >= 24 && fps <= 60, 'fps must be an integer from 24 to 60')
  ensure(Array.isArray(plan.tracks) && plan.tracks.length > 0, 'Provide measured head-region tracks')
  const ids = new Set()
  for (const track of plan.tracks) {
    ensure(track && typeof track === 'object' && !Array.isArray(track), 'Invalid track')
    ensure(Object.keys(track).every(key => ['id', 'from_seconds', 'to_seconds', 'keyframes'].includes(key)), 'Unknown track field')
    ensure(typeof track.id === 'string' && track.id.trim() && !ids.has(track.id), 'Each track needs a unique id')
    ids.add(track.id)
    ensure(Number.isFinite(track.from_seconds) && Number.isFinite(track.to_seconds) &&
      track.from_seconds >= 0 && track.to_seconds > track.from_seconds &&
      track.to_seconds <= media.duration_seconds + 1e-6, 'Track interval must be within the source clip')
    ensure(Array.isArray(track.keyframes) && track.keyframes.length >= 2, 'Track needs at least two keyframes')
    let previous = -Infinity
    for (const keyframe of track.keyframes) {
      ensure(keyframe && Object.keys(keyframe).every(key => ['at_seconds', 'box'].includes(key)), 'Invalid keyframe fields')
      ensure(Number.isFinite(keyframe.at_seconds) && keyframe.at_seconds > previous &&
        keyframe.at_seconds >= track.from_seconds && keyframe.at_seconds <= track.to_seconds,
      'Keyframe times must increase within their track interval')
      ensure(Array.isArray(keyframe.box) && keyframe.box.length === 4 &&
        keyframe.box.every(Number.isFinite) && keyframe.box[2] > 0 && keyframe.box[3] > 0,
      'box must be finite [x, y, width, height] with positive size')
      previous = keyframe.at_seconds
    }
    ensure(Math.abs(track.keyframes[0].at_seconds - track.from_seconds) < 1e-6 &&
      Math.abs(track.keyframes.at(-1).at_seconds - track.to_seconds) < 1e-6,
    'Keyframes must cover both ends of each track interval')
  }
  return { ...plan, fps }
}

function boxAtTime(track, seconds) {
  if (seconds < track.from_seconds || seconds >= track.to_seconds) return null
  const keys = track.keyframes
  let right = 1
  while (right < keys.length - 1 && keys[right].at_seconds < seconds) right++
  const a = keys[right - 1], b = keys[right]
  const fraction = (seconds - a.at_seconds) / (b.at_seconds - a.at_seconds)
  return a.box.map((value, i) => value + (b.box[i] - value) * fraction)
}

function maskFrame(frame, width, height, tracks, seconds) {
  ensure(frame.length === width * height * 3, 'Incomplete RGB frame')
  let covered = false
  for (const track of tracks) {
    const box = boxAtTime(track, seconds)
    if (!box) continue
    const left = Math.max(0, Math.min(width, Math.floor(box[0])))
    const top = Math.max(0, Math.min(height, Math.floor(box[1])))
    const right = Math.max(0, Math.min(width, Math.ceil(box[0] + box[2])))
    const bottom = Math.max(0, Math.min(height, Math.ceil(box[1] + box[3])))
    if (right <= left || bottom <= top) continue
    for (let y = top; y < bottom; y++) frame.fill(124, (y * width + left) * 3, (y * width + right) * 3)
    covered = true
  }
  return covered
}

function completion(child, label) {
  let details = ''
  child.stderr.on('data', data => { details = (details + data.toString()).slice(-8192) })
  const done = new Promise((resolve, reject) => {
    child.once('error', error => reject(new Error(`${label}: ${error.message}`)))
    child.once('close', code => code === 0 ? resolve() : reject(new Error(`${label} failed: ${details.trim() || code}`)))
  })
  // Attach rejection handling while the frame pipeline is still running.
  done.catch(() => {})
  return done
}

async function hashFile(file) {
  const hash = crypto.createHash('sha256')
  for await (const chunk of fs.createReadStream(file)) hash.update(chunk)
  return hash.digest('hex')
}

async function prepareReference(plan, media, out) {
  ensure(!fs.existsSync(out), 'Output already exists; choose a new revision path')
  ensure(path.extname(out).toLowerCase() === '.mp4', 'Output must be an MP4 path')
  ensure(fs.statSync(path.dirname(out)).isDirectory(), 'Output parent must exist')
  const temp = fs.mkdtempSync(path.join(path.dirname(out), '.identity-reference-'))
  const partial = path.join(temp, 'reference.mp4')
  let decoder, encoder, decoded, encoded
  try {
    decoder = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-xerror',
      '-protocol_whitelist', 'file,pipe', '-i', plan.source_file, '-map', '0:v:0',
      '-vf', `setpts=PTS-STARTPTS,fps=${plan.fps}`, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
    { stdio: ['ignore', 'pipe', 'pipe'] })
    decoded = completion(decoder, 'Video decode')
    encoder = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-xerror',
      '-f', 'rawvideo', '-pixel_format', 'rgb24', '-video_size', `${media.width}x${media.height}`,
      '-framerate', String(plan.fps), '-i', '-', '-an', '-c:v', 'libx264', '-preset', 'medium',
      '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-n', partial],
    { stdio: ['pipe', 'ignore', 'pipe'] })
    encoder.stdin.on('error', () => {})
    encoded = completion(encoder, 'Video encode')
    const frame = Buffer.allocUnsafe(media.width * media.height * 3)
    let filled = 0, frames = 0, maskedFrames = 0
    for await (const chunk of decoder.stdout) {
      let offset = 0
      while (offset < chunk.length) {
        const length = Math.min(chunk.length - offset, frame.length - filled)
        chunk.copy(frame, filled, offset, offset + length)
        filled += length
        offset += length
        if (filled === frame.length) {
          if (maskFrame(frame, media.width, media.height, plan.tracks, frames / plan.fps)) maskedFrames++
          // Wait until this buffer has been consumed before reusing it.
          await new Promise((resolve, reject) => encoder.stdin.write(frame, error => error ? reject(error) : resolve()))
          filled = 0
          frames++
        }
      }
    }
    await decoded
    ensure(filled === 0 && frames > 0, 'Source produced incomplete or empty frames')
    encoder.stdin.end()
    await encoded
    const result = probeLocal(partial)
    ensure(!result.source_audio_present, 'Prepared reference unexpectedly contains audio')
    ensure(Math.abs(result.duration_seconds - media.duration_seconds) <= 1 / plan.fps + 0.002,
      'Prepared reference duration drifted by more than one output frame')
    ensure(maskedFrames > 0, 'No measured head region intersected the video')
    const report = {
      ok: true, purpose: 'head-obscured motion reference; not a finished face-replacement video',
      source_file: plan.source_file, source_sha256: await hashFile(plan.source_file),
      output_file: out, output_sha256: await hashFile(partial),
      width: result.width, height: result.height, fps: plan.fps,
      duration_seconds: result.duration_seconds, frames, frames_with_mask: maskedFrames,
      bytes: fs.statSync(partial).size, audio_present: false,
      track_ids: plan.tracks.map(track => track.id),
      face_detection_performed: false, visual_coverage_verified: false,
    }
    fs.copyFileSync(partial, out, fs.constants.COPYFILE_EXCL)
    fs.chmodSync(out, 0o600)
    return report
  } catch (error) {
    decoder?.kill()
    encoder?.kill()
    await Promise.allSettled([decoded, encoded].filter(Boolean))
    throw error
  } finally {
    fs.rmSync(temp, { recursive: true, force: true })
  }
}

async function main(argv) {
  const args = parseArguments(argv)
  if (args.help) return {
    usage: 'node prepare-identity-reference.js --plan /absolute/tracking.json --out /absolute/new-reference.mp4 [--dry-run]',
    requirements: 'Node.js 18+, existing ffmpeg and ffprobe; no installs, network, or API key',
    plan: 'source_file, optional fps (30), tracks with id/from_seconds/to_seconds and keyframes at_seconds/box [x,y,width,height]',
    timing: 'Clip-local seconds from the first source video frame; boxes use source pixels. Normalize rotation and trim before measuring.',
    output: 'Silent H.264 motion reference with measured head/hair regions obscured. Inspect coverage before generation.',
  }
  const raw = JSON.parse(fs.readFileSync(args.plan, 'utf8'))
  ensure(typeof raw?.source_file === 'string' && path.isAbsolute(raw.source_file), 'source_file must be an absolute local path')
  ensure(path.resolve(raw.source_file) !== args.out && args.plan !== args.out, 'Output cannot replace the source or plan')
  ensure(!fs.existsSync(args.out), 'Output already exists; choose a new revision path')
  const media = probeLocal(raw.source_file)
  const plan = validatePlan(raw, media)
  if (args.dryRun) return { ok: true, dry_run: true, source_file: plan.source_file, output_file: args.out,
    ...media, fps: plan.fps, tracks: plan.tracks.length, network_used: false, submitted: false }
  return prepareReference(plan, media, args.out)
}

if (require.main === module) main(process.argv.slice(2)).then(
  result => process.stdout.write(JSON.stringify(result, null, 2) + '\n'),
  error => { process.stderr.write(`Identity reference preparation failed: ${error.message}\n`); process.exitCode = 1 },
)

module.exports = { main, parseArguments, probeLocal, validatePlan, boxAtTime, maskFrame, prepareReference }
