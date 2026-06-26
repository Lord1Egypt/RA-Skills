import { execFileSync } from 'node:child_process'
import path from 'node:path'
import {
  ensureDirForFile,
  getRuntimeConfig,
  getStringArg,
  loadSkillConfig,
  parseArgs,
  probeMediaFile,
  resolveFfmpegBinary,
  resolveFfprobeBinary,
  validateMixedMedia,
  writeJsonMaybe,
} from './_shared'

type MixResult = {
  rawVideo: string
  subtitledVideo: string
  subtitleTtsVideo: string
  finalVideo: string
  status: 'partial' | 'final'
  formal: boolean
  ffmpeg: string
  ffprobe: string
  probe?: {
    input: ReturnType<typeof probeMediaFile>
    output: ReturnType<typeof probeMediaFile>
    validation: ReturnType<typeof validateMixedMedia>
  }
}

function runFfmpeg(ffmpeg: string, args: string[]) {
  execFileSync(ffmpeg, args, { stdio: 'inherit' })
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2))
  const configPath = getStringArg(args, 'config') || undefined
  const config = loadSkillConfig(configPath)
  const runtime = getRuntimeConfig(config)
  const video = getStringArg(args, 'video')
  const tts = getStringArg(args, 'tts')
  const ambience = getStringArg(args, 'ambience')
  const out = getStringArg(args, 'out')
  const resultJsonPath = getStringArg(args, 'result-json') || undefined
  const ffmpeg = resolveFfmpegBinary(getStringArg(args, 'ffmpeg'), runtime?.ffmpeg)
  const ffprobe = resolveFfprobeBinary(getStringArg(args, 'ffprobe'), runtime?.ffprobe)
  if (!video || !out) {
    throw new Error('用法: tsx mix-final-video.ts --video <mp4> [--tts <mp3>] [--ambience <mp3>] --out <mp4> [--result-json <json>] [--config <json>] [--ffmpeg <路径>] [--ffprobe <路径>]')
  }

  ensureDirForFile(out)

  const inputs = ['-y', '-i', path.resolve(video)]
  let filter = ''
  let mapAudio = '0:a?'

  if (tts && ambience) {
    inputs.push('-i', path.resolve(tts), '-i', path.resolve(ambience))
    filter = '[1:a]apad,aresample=44100,pan=stereo|c0=c0|c1=c0,volume=1.0[a1];[2:a]atrim=0:999,aresample=44100,volume=0.18[a2];[a1][a2]amix=inputs=2:weights=1 0.35:duration=first:dropout_transition=0[aout]'
    mapAudio = '[aout]'
  } else if (tts) {
    inputs.push('-i', path.resolve(tts))
    filter = '[1:a]apad,aresample=44100,pan=stereo|c0=c0|c1=c0,volume=1.0[aout]'
    mapAudio = '[aout]'
  } else if (ambience) {
    inputs.push('-i', path.resolve(ambience))
    filter = '[1:a]atrim=0:999,aresample=44100,volume=0.18[aout]'
    mapAudio = '[aout]'
  }

  const ffmpegArgs = [...inputs]
  if (filter) {
    ffmpegArgs.push('-filter_complex', filter, '-map', '0:v', '-map', mapAudio)
  } else {
    ffmpegArgs.push('-map', '0:v', '-map', mapAudio)
  }
  ffmpegArgs.push('-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', path.resolve(out))
  runFfmpeg(ffmpeg, ffmpegArgs)

  const inputProbe = probeMediaFile(video, ffprobe)
  const outputProbe = probeMediaFile(out, ffprobe)
  const validation = validateMixedMedia(inputProbe, outputProbe, Boolean(tts || ambience))
  if (!validation.ok) {
    throw new Error(`混音结果校验失败: ${validation.errors.join('；')}`)
  }

  const result: MixResult = {
    rawVideo: path.resolve(video),
    subtitledVideo: '',
    subtitleTtsVideo: tts ? path.resolve(out) : '',
    finalVideo: path.resolve(out),
    status: tts || ambience ? 'final' : 'partial',
    formal: true,
    ffmpeg,
    ffprobe,
    probe: {
      input: inputProbe,
      output: outputProbe,
      validation,
    },
  }
  writeJsonMaybe(result, resultJsonPath)
}
