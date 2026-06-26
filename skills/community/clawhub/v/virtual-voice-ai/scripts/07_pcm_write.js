// scripts/07_pcm_write.js
// Decodes MP3 audio from TTS provider and writes raw PCM to VB-Cable.
// VB-Cable expects raw PCM input. TTS providers output MP3.
// This script bridges that gap using ffmpeg as a decoder.

require('dotenv').config()
const { spawn } = require('child_process')
const os = require('os')

const REQUIRED = ['VIRTUAL_CABLE_NAME']
const missing = REQUIRED.filter(k => !process.env[k])
if (missing.length) {
  console.error(`[voice-pipeline] Missing required env vars: ${missing.join(', ')}`)
  console.error('Run node scripts/01_list_devices.js to find the correct device name.')
  process.exit(1)
}

function buildOutputArgs(deviceName) {
  const platform = os.platform()

  if (platform === 'win32') {
    return [
      '-f', 's16le',
      '-ar', '44100',
      '-ac', '2',
      '-f', 'dshow',
      `audio=${deviceName}`
    ]
  } else if (platform === 'darwin') {
    return [
      '-f', 's16le',
      '-ar', '44100',
      '-ac', '2',
      '-f', 'avfoundation',
      `:${deviceName}`
    ]
  } else {
    return [
      '-f', 's16le',
      '-ar', '44100',
      '-ac', '2',
      '-f', 'alsa',
      deviceName
    ]
  }
}

class PCMWriter {
  constructor() {
    this.ffmpegDecode = null
    this.ffmpegWrite = null
    this.stopped = false
    this._setup()
  }

  _setup() {
    const deviceName = process.env.VIRTUAL_CABLE_NAME

    // Stage 1: Decode incoming MP3 to raw PCM (44.1kHz stereo s16le)
    this.ffmpegDecode = spawn('ffmpeg', [
      '-f', 'mp3',
      '-i', 'pipe:0',
      '-ar', '44100',
      '-ac', '2',
      '-f', 's16le',
      'pipe:1'
    ], { stdio: ['pipe', 'pipe', 'ignore'] })

    // Stage 2: Write PCM to VB-Cable virtual device
    const outputArgs = buildOutputArgs(deviceName)
    this.ffmpegWrite = spawn('ffmpeg', [
      '-f', 's16le',
      '-ar', '44100',
      '-ac', '2',
      '-i', 'pipe:0',
      ...outputArgs
    ], { stdio: ['pipe', 'ignore', 'ignore'] })

    // Pipe decode output to write input
    this.ffmpegDecode.stdout.pipe(this.ffmpegWrite.stdin)

    this.ffmpegDecode.on('error', (e) => {
      if (!this.stopped) console.error('[pcm-writer] Decode error:', e.message)
    })

    this.ffmpegWrite.on('error', (e) => {
      if (!this.stopped) console.error('[pcm-writer] Write error:', e.message)
      if (e.message.includes('No such') || e.message.includes('Invalid')) {
        console.error(`[pcm-writer] Device "${deviceName}" not found.`)
        console.error('[pcm-writer] Run node scripts/01_list_devices.js and update VIRTUAL_CABLE_NAME in .env')
      }
    })

    if (process.env.PIPELINE_DEBUG === 'true') {
      console.error(`[pcm-writer] Writing to: ${deviceName}`)
    }
  }

  // Write an MP3 audio chunk from TTS
  write(mp3Chunk) {
    if (this.stopped || !this.ffmpegDecode) return
    if (this.ffmpegDecode.stdin.writable) {
      this.ffmpegDecode.stdin.write(mp3Chunk)
    }
  }

  // Instantly silence output (for kill switch)
  flush() {
    if (this.ffmpegDecode) {
      this.ffmpegDecode.kill('SIGKILL')
      this.ffmpegDecode = null
    }
    if (this.ffmpegWrite) {
      this.ffmpegWrite.kill('SIGKILL')
      this.ffmpegWrite = null
    }
    // Restart for next utterance
    if (!this.stopped) this._setup()
  }

  stop() {
    this.stopped = true
    if (this.ffmpegDecode) { this.ffmpegDecode.kill('SIGKILL'); this.ffmpegDecode = null }
    if (this.ffmpegWrite) { this.ffmpegWrite.kill('SIGKILL'); this.ffmpegWrite = null }
  }
}

module.exports = { PCMWriter }