// scripts/03_deepgram_ws.js
// Opens a Deepgram streaming WebSocket and pipes PCM audio chunks.
// Emits 'transcript' events with final text.
//
// Stress test: node scripts/03_deepgram_ws.js
// Speak into your mic. Transcripts should appear within ~1 second.

require('dotenv').config()
const WebSocket = require('ws')
const { EventEmitter } = require('events')
const { startCapture, SAMPLE_RATE, CHANNELS } = require('./02_capture_resample')

const REQUIRED = ['DEEPGRAM_API_KEY']
const missing = REQUIRED.filter(k => !process.env[k])
if (missing.length) {
  console.error(`[voice-pipeline] Missing required env vars: ${missing.join(', ')}`)
  process.exit(1)
}

const DEEPGRAM_URL = [
  'wss://api.deepgram.com/v1/listen',
  `?encoding=linear16`,
  `&sample_rate=${SAMPLE_RATE}`,
  `&channels=${CHANNELS}`,
  `&model=nova-2`,
  `&language=en-US`,
  `&interim_results=false`,
  `&endpointing=${process.env.DEEPGRAM_ENDPOINTING_MS || 300}`
].join('')

class DeepgramSTT extends EventEmitter {
  constructor() {
    super()
    this.ws = null
    this.ffmpeg = null
    this.reconnectAttempts = 0
    this.maxReconnects = 5
    this.stopped = false
  }

  start() {
    this._connect()
  }

  _connect() {
    if (this.stopped) return

    this.ws = new WebSocket(DEEPGRAM_URL, {
      headers: { Authorization: `Token ${process.env.DEEPGRAM_API_KEY}` }
    })

    this.ws.on('open', () => {
      if (process.env.PIPELINE_DEBUG === 'true') console.error('[deepgram] WebSocket open')
      this.reconnectAttempts = 0

      // Start or resume audio capture
      if (!this.ffmpeg) {
        this.ffmpeg = startCapture((chunk) => {
          if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(chunk)
          }
        })
      }
    })

    this.ws.on('message', (data) => {
      try {
        const msg = JSON.parse(data.toString())
        const transcript = msg?.channel?.alternatives?.[0]?.transcript
        if (transcript && msg.is_final) {
          if (process.env.PIPELINE_DEBUG === 'true') console.error(`[deepgram] Final: "${transcript}"`)
          this.emit('transcript', transcript)
        }
      } catch (e) {
        // malformed JSON from Deepgram, ignore
      }
    })

    this.ws.on('close', (code) => {
      if (this.stopped) return
      if (process.env.PIPELINE_DEBUG === 'true') console.error(`[deepgram] WebSocket closed (${code}), reconnecting...`)
      this._scheduleReconnect()
    })

    this.ws.on('error', (err) => {
      console.error('[deepgram] WebSocket error:', err.message)
      this._scheduleReconnect()
    })
  }

  _scheduleReconnect() {
    if (this.stopped || this.reconnectAttempts >= this.maxReconnects) {
      this.emit('error', new Error(`[deepgram] Max reconnect attempts reached (${this.maxReconnects})`))
      return
    }
    this.reconnectAttempts++
    setTimeout(() => this._connect(), 1000 * this.reconnectAttempts)
  }

  stop() {
    this.stopped = true
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    if (this.ffmpeg) {
      this.ffmpeg.kill('SIGKILL')
      this.ffmpeg = null
    }
  }
}

// When run directly (stress test mode)
if (require.main === module) {
  const stt = new DeepgramSTT()
  stt.on('transcript', (text) => console.log(`[transcript] ${text}`))
  stt.on('error', (err) => console.error(err.message))
  stt.start()
  console.error('[voice-pipeline] Listening... speak into your mic (Ctrl+C to stop)')
  process.on('SIGINT', () => { stt.stop(); process.exit(0) })
}

module.exports = { DeepgramSTT }