/**
 * Token Compressor — Reduces API costs by compressing conversation context
 * 
 * Three layers:
 * 1. Message Compressor: Strips filler from user input before sending to paid API
 * 2. History Compressor: Summarizes old conversation turns into compact summaries
 * 3. Response Cache: Serves cached answers for similar questions
 * 
 * Uses local Ollama (free) for all compression work.
 * Paid API only sees dense, efficient tokens.
 */

const http = require('http');

class TokenCompressor {
  constructor(config = {}) {
    this.enabled = config.enabled !== false;
    this.ollamaHost = config.ollamaHost || 'localhost';
    this.ollamaPort = config.ollamaPort || 11434;
    this.compressionModel = config.compressionModel || 'llama3.1:8b';
    
    // History compression settings
    this.maxUncompressedTurns = config.maxUncompressedTurns || 10; // Keep last N turns verbatim
    this.summaryMaxTokens = config.summaryMaxTokens || 300; // Max tokens for summary block
    
    // Cache settings
    this.cache = new Map();
    this.cacheMaxSize = config.cacheMaxSize || 100;
    this.cacheTTL = config.cacheTTL || 3600000; // 1 hour
    
    // Stats
    this.stats = {
      messagesCompressed: 0,
      historySummaries: 0,
      cacheHits: 0,
      estimatedTokensSaved: 0
    };

    // Compressed history summary (rolling)
    this.historySummary = null;
    this.compressedTurnCount = 0;
  }

  /**
   * Layer 1: Compress a user message — strip filler, extract intent
   * Returns original if compression fails or isn't worth it
   */
  async compressMessage(message) {
    if (!this.enabled) return { compressed: message, original: message, saved: false };
    
    // Skip short messages — not worth compressing
    const wordCount = message.split(/\s+/).length;
    if (wordCount < 15) {
      return { compressed: message, original: message, saved: false };
    }

    try {
      const prompt = `Compress this message to its core meaning. Keep all specific details, names, numbers, and technical terms. Remove filler words, hedging, repetition, and social padding. Output ONLY the compressed version, nothing else.

Original: "${message}"

Compressed:`;

      const result = await this._queryOllama(prompt);
      
      if (result && result.length < message.length * 0.85) {
        // Only use compression if we actually saved significant tokens
        const saved = message.length - result.length;
        this.stats.messagesCompressed++;
        this.stats.estimatedTokensSaved += Math.floor(saved / 4); // ~4 chars per token
        return { compressed: result, original: message, saved: true, charsSaved: saved };
      }
      
      return { compressed: message, original: message, saved: false };
    } catch (err) {
      // Ollama down or error — pass through original
      return { compressed: message, original: message, saved: false, error: err.message };
    }
  }

  /**
   * Layer 2: Compress conversation history
   * Keeps last N turns verbatim, summarizes everything before that
   * Returns compressed history array ready for API
   */
  async compressHistory(history, systemPrompt = '') {
    if (!this.enabled) return history;
    if (history.length <= this.maxUncompressedTurns * 2) return history;

    // Split: old turns to summarize, recent turns to keep
    const cutoff = history.length - (this.maxUncompressedTurns * 2);
    const oldTurns = history.slice(0, cutoff);
    const recentTurns = history.slice(cutoff);

    // Only re-summarize if we have new old turns
    if (oldTurns.length > this.compressedTurnCount) {
      try {
        const turnText = oldTurns.map(t => `${t.role}: ${t.content}`).join('\n');
        
        const prompt = `Summarize this conversation into a brief context paragraph. Include key topics discussed, decisions made, important details mentioned, and any unresolved questions. Be dense and factual. Max 200 words.

${this.historySummary ? `Previous summary: ${this.historySummary}\n\nNew turns to incorporate:\n` : ''}${turnText}

Summary:`;

        const summary = await this._queryOllama(prompt);
        if (summary) {
          this.historySummary = summary;
          this.compressedTurnCount = oldTurns.length;
          this.stats.historySummaries++;
          
          const oldTokens = turnText.length / 4;
          const newTokens = summary.length / 4;
          this.stats.estimatedTokensSaved += Math.floor(oldTokens - newTokens);
        }
      } catch (err) {
        // Failed — just return uncompressed
        return history;
      }
    }

    // Build compressed history: summary as first message + recent turns
    if (this.historySummary) {
      return [
        { role: 'user', content: `[Previous conversation summary: ${this.historySummary}]` },
        { role: 'assistant', content: 'Understood, I have the context from our previous conversation.' },
        ...recentTurns
      ];
    }

    return history;
  }

  /**
   * Layer 3: Check cache for similar questions
   * Uses simple keyword matching (no AI needed)
   */
  checkCache(message) {
    if (!this.enabled) return null;
    
    const key = this._cacheKey(message);
    const cached = this.cache.get(key);
    
    if (cached && (Date.now() - cached.timestamp) < this.cacheTTL) {
      this.stats.cacheHits++;
      return cached.response;
    }
    
    // Clean expired entries
    if (cached) this.cache.delete(key);
    return null;
  }

  /**
   * Store a response in cache
   */
  cacheResponse(message, response) {
    if (!this.enabled) return;
    
    const key = this._cacheKey(message);
    
    // Evict oldest if full
    if (this.cache.size >= this.cacheMaxSize) {
      const oldest = this.cache.keys().next().value;
      this.cache.delete(oldest);
    }
    
    this.cache.set(key, {
      response,
      timestamp: Date.now()
    });
  }

  /**
   * Get compression stats
   */
  getStats() {
    return {
      ...this.stats,
      cacheSize: this.cache.size,
      historySummaryLength: this.historySummary ? this.historySummary.length : 0,
      compressedTurns: this.compressedTurnCount
    };
  }

  /**
   * Reset state (on new conversation)
   */
  reset() {
    this.historySummary = null;
    this.compressedTurnCount = 0;
    this.cache.clear();
  }

  // --- Internal ---

  _cacheKey(message) {
    // Normalize: lowercase, strip punctuation, sort words
    const words = message.toLowerCase()
      .replace(/[^\w\s]/g, '')
      .split(/\s+/)
      .filter(w => w.length > 3)
      .sort()
      .join(' ');
    return words;
  }

  _queryOllama(prompt) {
    return new Promise((resolve, reject) => {
      const body = JSON.stringify({
        model: this.compressionModel,
        messages: [
          { role: 'system', content: 'You are a text compression tool. Output only what is asked, nothing else. No explanations, no preamble.' },
          { role: 'user', content: prompt }
        ],
        stream: false,
        options: {
          temperature: 0.1,  // Low creativity — we want faithful compression
          num_predict: 512    // Cap output length
        }
      });

      const req = http.request({
        hostname: this.ollamaHost,
        port: this.ollamaPort,
        path: '/api/chat',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body)
        },
        timeout: 15000 // 15s max — if Ollama is slow, skip compression
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            resolve(parsed.message?.content?.trim() || null);
          } catch {
            reject(new Error('Invalid Ollama response'));
          }
        });
      });

      req.on('error', reject);
      req.on('timeout', () => { req.destroy(); reject(new Error('Ollama timeout')); });
      req.write(body);
      req.end();
    });
  }
}

module.exports = TokenCompressor;

