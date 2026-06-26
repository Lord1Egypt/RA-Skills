// index.js
// Main pipeline orchestrator. This is what the host app imports.
//
// Usage:
//   const pipeline = require('./voice-pipeline')
//   pipeline.start()
//   pipeline.stop()  // kill switch

require('dotenv').config()
const { EventEmitter } = require('events')
const { DeepgramSTT } = require('./scripts/03_deepgram_ws')
const { LLMStream } = require('./scripts/04_llm_stream')
const { SentenceChunker } = require('./scripts/05_sentence_chunker')
const { TTSStream } = require('./scripts/06_tts_ws')
const { PCMWriter } = require('./scripts/07_pcm_write')

// Validate all required env vars up front
const REQUIRED = [
  'DEEPGRAM_API_KEY',
  'LLM_PROVIDER', 'LLM_API_KEY', 'LLM_MODEL',
  'TTS_PROVIDER', 'TTS_API_KEY', 'TTS_VOICE_ID',
  'VIRTUAL_CABLE_NAME'
]

class VoicePipeline extends EventEmitter {
  constructor() {
    super()
    this.stt = null
    this.llm = null
    this.chunker = null
    this.tts = null
    this.pcm = null
    this.running = false
  }

  start() {
    const missing = REQUIRED.filter(k => !process.env[k])
    if (missing.length) {
      throw new Error(`[voice-pipeline] Missing required env vars: ${missing.join(', ')}\nAdd them to your .env and restart.`)
    }

    if (this.running) {
      console.warn('[voice-pipeline] Already running. Call stop() first.')
      return
    }

    this.running = true

    // Initialize all stages
    this.stt = new DeepgramSTT()
    this.llm = new LLMStream()
    this.chunker = new SentenceChunker()
    this.tts = new TTSStream()
    this.pcm = new PCMWriter()

    // Wire: STT → LLM
    this.stt.on('transcript', (text) => {
      this.emit('transcript', text)
      this.llm.send(text)
    })

    // Wire: LLM → Chunker
    this.llm.on('token', (token) => {
      this.chunker.push(token)
    })
    this.llm.on('done', () => {
      this.chunker.flush()
    })

    // Wire: Chunker → TTS
    this.chunker.on('chunk', (sentence) => {
      this.emit('speaking', sentence)
      this.tts.send(sentence)
    })

    // Wire: TTS → PCM Writer
    this.tts.on('audio', (mp3Chunk) => {
      this.pcm.write(mp3Chunk)
    })

    // Error propagation
    ;[this.stt, this.llm, this.tts].forEach(stage => {
      stage.on('error', (err) => {
        console.error('[voice-pipeline] Stage error:', err.message)
        this.emit('error', err)
      })
    })

    // Start the pipeline
    this.tts.start()
    this.stt.start()

    console.log('[voice-pipeline] Started. Listening...')
    this.emit('started')
  }

  // Kill switch — call this from hotkey, IPC, SIGINT, or wherever
  stop() {
    if (!this.running) return
    this.running = false

    console.log('[voice-pipeline] Stopping...')

    // Order matters: silence audio first, then clean up upstream
    if (this.pcm) { this.pcm.stop(); this.pcm = null }
    if (this.tts) { this.tts.stop(); this.tts = null }
    if (this.llm) { this.llm.abort(); this.llm = null }
    if (this.chunker) { this.chunker.reset(); this.chunker = null }
    if (this.stt) { this.stt.stop(); this.stt = null }

    this.emit('stopped')
    console.log('[voice-pipeline] Stopped.')
  }

  // Interrupt current speech mid-sentence without stopping the pipeline
  interrupt() {
    if (this.pcm) this.pcm.flush()
    if (this.tts) { this.tts.stop(); this.tts = new TTSStream(); this.tts.start() }
    if (this.llm) this.llm.abort()
    if (this.chunker) this.chunker.reset()
    this.emit('interrupted')
  }
}

const pipeline = new VoicePipeline()

// Graceful shutdown
process.on('SIGINT', () => { pipeline.stop(); process.exit(0) })
process.on('SIGTERM', () => { pipeline.stop(); process.exit(0) })

module.exports = pipeline

// Run directly
if (require.main === module) {
  pipeline.on('transcript', t => console.log(`[you] ${t}`))
  pipeline.on('speaking', s => console.log(`[jarvis] ${s}`))
  pipeline.on('error', e => console.error('[error]', e.message))
  pipeline.start()
}