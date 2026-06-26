// scripts/06_tts_ws.js
// Sends sentence chunks to TTS provider and streams MP3 audio back.
// Supports: elevenlabs, cartesia
//
// Stress test: node scripts/06_tts_ws.js
// Should play audio through your speakers for a hardcoded test sentence.

require('dotenv').config()
const WebSocket = require('ws')
const { EventEmitter } = require('events')

const REQUIRED = ['TTS_PROVIDER', 'TTS_API_KEY', 'TTS_VOICE_ID']
const missing = REQUIRED.filter(k => !process.env[k])
if (missing.length) {
  console.error(`[voice-pipeline] Missing required env vars: ${missing.join(', ')}`)
  process.exit(1)
}

class TTSStream extends EventEmitter {
  constructor() {
    super()
    this.ws = null
    this.stopped = false
    this.reconnectAttempts = 0
    this.maxReconnects = 5
    this.queue = []
    this.connected = false
  }

  start() {
    this._connect()
  }

  send(text) {
    if (!text || !text.trim()) return
    if (this.connected) {
      this._send(text)
    } else {
      this.queue.push(text)
    }
  }

  _connect() {
    if (this.stopped) return

    const provider = process.env.TTS_PROVIDER.toLowerCase()

    if (provider === 'elevenlabs') {
      this._connectElevenLabs()
    } else if (provider === 'cartesia') {
      this._connectCartesia()
    } else {
      this.emit('error', new Error(`[tts] Unknown provider: ${provider}`))
    }
  }

  _connectElevenLabs() {
    const voiceId = process.env.TTS_VOICE_ID
    const url = `wss://api.elevenlabs.io/v1/text-to-speech/${voiceId}/stream-input?model_id=eleven_turbo_v2&output_format=mp3_44100_128`

    this.ws = new WebSocket(url, {
      headers: { 'xi-api-key': process.env.TTS_API_KEY }
    })

    this.ws.on('open', () => {
      this.connected = true
      this.reconnectAttempts = 0

      // ElevenLabs requires a BOS (beginning-of-stream) message first
      this.ws.send(JSON.stringify({
        text: ' ',
        voice_settings: { stability: 0.5, similarity_boost: 0.8 },
        generation_config: { chunk_length_schedule: [120, 160, 250, 290] }
      }))

      // Flush queued text
      while (this.queue.length) this._send(this.queue.shift())
    })

    this.ws.on('message', (data) => {
      try {
        const msg = JSON.parse(data.toString())
        if (msg.audio) {
          const audioChunk = Buffer.from(msg.audio, 'base64')
          this.emit('audio', audioChunk)
        }
      } catch (_) {}
    })

    this._attachReconnect()
  }

  _connectCartesia() {
    const url = `wss://api.cartesia.ai/tts/websocket?api_key=${process.env.TTS_API_KEY}&cartesia_version=2024-06-10`
    this.ws = new WebSocket(url)

    this.ws.on('open', () => {
      this.connected = true
      this.reconnectAttempts = 0
      while (this.queue.length) this._send(this.queue.shift())
    })

    this.ws.on('message', (data) => {
      try {
        const msg = JSON.parse(data.toString())
        if (msg.type === 'chunk' && msg.data) {
          const audioChunk = Buffer.from(msg.data, 'base64')
          this.emit('audio', audioChunk)
        }
      } catch (_) {}
    })

    this._attachReconnect()
  }

  _send(text) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      this.queue.push(text)
      return
    }

    const provider = process.env.TTS_PROVIDER.toLowerCase()

    if (provider === 'elevenlabs') {
      this.ws.send(JSON.stringify({ text }))
    } else if (provider === 'cartesia') {
      this.ws.send(JSON.stringify({
        transcript: text,
        voice: { mode: 'id', id: process.env.TTS_VOICE_ID },
        model_id: 'sonic-english',
        output_format: { container: 'raw', encoding: 'pcm_f32le', sample_rate: 44100 }
      }))
    }

    if (process.env.PIPELINE_DEBUG === 'true') console.error(`[tts] Sent: "${text}"`)
  }

  _attachReconnect() {
    this.ws.on('close', () => {
      this.connected = false
      if (!this.stopped) this._scheduleReconnect()
    })

    this.ws.on('error', (err) => {
      console.error('[tts] WebSocket error:', err.message)
      this.connected = false
      if (!this.stopped) this._scheduleReconnect()
    })
  }

  _scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnects) {
      this.emit('error', new Error('[tts] Max reconnect attempts reached'))
      return
    }
    this.reconnectAttempts++
    setTimeout(() => this._connect(), 1000 * this.reconnectAttempts)
  }

  flushAndStop() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      // ElevenLabs requires EOS message
      if (process.env.TTS_PROVIDER === 'elevenlabs') {
        this.ws.send(JSON.stringify({ text: '' }))
      }
    }
    this.stop()
  }

  stop() {
    this.stopped = true
    this.queue = []
    this.connected = false
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }
}

// Stress test
if (require.main === module) {
  const tts = new TTSStream()
  let audioReceived = false

  tts.on('audio', (chunk) => {
    if (!audioReceived) {
      console.error('[tts] Audio stream started. Received first chunk.')
      audioReceived = true
    }
    process.stdout.write(chunk)
  })

  tts.on('error', (e) => console.error(e.message))
  tts.start()

  setTimeout(() => {
    console.error('[tts] Sending test sentence...')
    tts.send('Hello! This is a test of the voice pipeline audio output.')
    setTimeout(() => { tts.flushAndStop(); process.exit(0) }, 5000)
  }, 1000)

  console.error('[tts] Connecting... redirect stdout to hear audio:')
  console.error('  node scripts/06_tts_ws.js | ffplay -f mp3 -i pipe:0')
}

module.exports = { TTSStream }