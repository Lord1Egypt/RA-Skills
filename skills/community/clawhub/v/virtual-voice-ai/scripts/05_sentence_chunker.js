// scripts/05_sentence_chunker.js
// Buffers LLM token stream and flushes complete sentences to TTS.
// TTS providers need at least 15-30 words with punctuation to produce
// natural-sounding audio. Sending individual tokens = robotic choppy output.
//
// Flush triggers:
//   1. Sentence-ending punctuation (. ? ! followed by space or end)
//   2. Word count exceeds CHUNK_MAX_WORDS (safety valve)
//   3. Flush timeout after LLM 'done' event

const { EventEmitter } = require('events')

const MAX_WORDS = parseInt(process.env.CHUNK_MAX_WORDS || '25')
const FLUSH_TIMEOUT_MS = parseInt(process.env.CHUNK_FLUSH_TIMEOUT_MS || '800')

class SentenceChunker extends EventEmitter {
  constructor() {
    super()
    this.buffer = ''
    this.flushTimer = null
  }

  push(token) {
    this.buffer += token

    // Cancel pending timeout flush since we got new tokens
    if (this.flushTimer) {
      clearTimeout(this.flushTimer)
      this.flushTimer = null
    }

    this._tryFlush()
  }

  // Called when LLM stream ends — flush whatever remains
  flush() {
    if (this.flushTimer) {
      clearTimeout(this.flushTimer)
      this.flushTimer = null
    }
    this._emit()
  }

  _tryFlush() {
    const text = this.buffer

    // Check for sentence-ending punctuation followed by space or end of string
    const sentenceEnd = /[.?!][)\]"']?\s/.exec(text) || /[.?!][)\]"']?$/.exec(text)

    const wordCount = text.trim().split(/\s+/).filter(Boolean).length

    if (sentenceEnd || wordCount >= MAX_WORDS) {
      if (sentenceEnd) {
        // Flush up to and including the sentence end
        const cutAt = sentenceEnd.index + sentenceEnd[0].length
        const chunk = text.slice(0, cutAt).trim()
        this.buffer = text.slice(cutAt)
        if (chunk) this.emit('chunk', chunk)

        // Check if remainder also has a sentence
        if (this.buffer.trim()) this._tryFlush()
      } else {
        // Word limit hit — flush all
        this._emit()
      }
    } else {
      // Nothing to flush yet — set a timeout in case LLM pauses
      this.flushTimer = setTimeout(() => {
        if (this.buffer.trim()) this._emit()
      }, FLUSH_TIMEOUT_MS)
    }
  }

  _emit() {
    const chunk = this.buffer.trim()
    this.buffer = ''
    if (chunk) {
      if (process.env.PIPELINE_DEBUG === 'true') console.error(`[chunker] Flushing: "${chunk}"`)
      this.emit('chunk', chunk)
    }
  }

  reset() {
    if (this.flushTimer) clearTimeout(this.flushTimer)
    this.buffer = ''
    this.flushTimer = null
  }
}

// Stress test
if (require.main === module) {
  const chunker = new SentenceChunker()
  chunker.on('chunk', (c) => console.log(`\n[CHUNK] "${c}"`))

  const mockTokens = 'Hello there! My name is JARVIS. I am an AI assistant. How can I help you today?'.split(' ')
  console.log('Feeding tokens one by one:\n')
  mockTokens.forEach((t, i) => {
    setTimeout(() => {
      process.stdout.write(t + ' ')
      chunker.push(t + ' ')
      if (i === mockTokens.length - 1) setTimeout(() => chunker.flush(), 100)
    }, i * 80)
  })
}

module.exports = { SentenceChunker }