import axios from "axios";
import * as cheerio from "cheerio";
import crypto from "crypto";

export class TelegramWebScraper {
  constructor(config, logger) {
    this.config = config;
    this.logger = logger;
    this.client = axios.create({
      timeout: 15000,
      headers: {
        "User-Agent": config.user_agent || "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
      },
      validateStatus: status => status < 500 // Handle 4xx as errors, not exceptions
    });
  }

  /**
   * Fetch and parse messages from a public Telegram channel webpage
   * @param {string} channelIdentifier - username, @username, or full URL
   * @param {number} limit - max messages to extract
   * @returns {Promise<{messages: Array, error?: string}>}
   */
  async fetchChannelMessages(channelIdentifier, limit = 20) {
    const username = this._normalizeChannel(channelIdentifier);
    if (!username) {
      return { error: `Invalid channel identifier: ${channelIdentifier}`, messages: [] };
    }
    
    const url = `https://t.me/s/${username}`;

    try {
      this.logger.debug(`Fetching ${url}`);
      const { data: html, status } = await this.client.get(url);
      
      if (status === 404) {
        return { 
          error: `Channel not found or private: @${username}. Verify it's public at ${url}`, 
          messages: [] 
        };
      }
      if (status >= 400) {
        return { 
          error: `HTTP ${status} from ${url}. Telegram may be rate-limiting requests.`, 
          messages: [] 
        };
      }

      return { messages: this._parseMessages(html, username, limit), error: null };
    } catch (err) {
      return { 
        error: `Network error fetching ${username}: ${err.message}`, 
        messages: [] 
      };
    }
  }

  /**
   * Normalize various channel identifier formats to plain username
   * Supports: "durov", "@durov", "https://t.me/s/durov", "https://t.me/durov"
   */
  _normalizeChannel(identifier) {
    if (!identifier || typeof identifier !== "string") return null;
    
    // Extract username from URL or raw identifier
    const urlMatch = identifier.match(/t\.me\/(?:s\/)?@?([^/?#]+)/i);
    const rawMatch = identifier.match(/^@?([^/?#]+)$/);
    
    const username = (urlMatch || rawMatch)?.[1]?.toLowerCase();
    
    // Basic validation: alphanumeric + underscores, 3-32 chars
    if (username && /^[a-z0-9_]{3,32}$/.test(username)) {
      return username;
    }
    return null;
  }

  /**
   * Parse HTML from t.me/s/* page and extract message objects
   * Resilient to minor Telegram HTML structure changes
   */
  _parseMessages(html, channel, limit) {
    const $ = cheerio.load(html);
    const messages = [];

    // Primary selector: Telegram's standard message text container
    // Fallback: if structure changes, we'd need to update this
    $('.tgme_widget_message_text').each((i, el) => {
      if (i >= limit) return false; // Respect limit
      
      // Extract and clean text content
      let text = $(el).text()
        .replace(/\s+/g, ' ')           // Normalize whitespace
        .replace(/[\u200B-\u200D\uFEFF]/g, '') // Remove zero-width chars
        .replace(/\n{3,}/g, '\n\n')     // Limit consecutive newlines
        .trim();
      
      // Filter out noise: empty, too short, or boilerplate
      if (text && text.length > 15 && !this._isBoilerplate(text)) {
        const hash = this._hashMessage(text);
        const timestamp = this._extractTimestamp($(el)) || Date.now();
        
        messages.push({
          id: hash,      // Unique identifier for deduplication
          text,          // Cleaned message content
          timestamp,     // Approximate message time (ms since epoch)
          channel        // Source channel username
        });
      }
    });

    // Return in chronological order (oldest → newest) for coherent summarization
    return messages.reverse();
  }

  /**
   * Attempt to extract message timestamp from HTML
   * Returns milliseconds since epoch, or null if unavailable
   */
  _extractTimestamp($el) {
    // Try <time datetime="..."> first (most reliable)
    const timeEl = $el.closest('.tgme_widget_message').find('time[datetime]');
    if (timeEl.length) {
      const dt = new Date(timeEl.attr('datetime'));
      if (!isNaN(dt.getTime())) return dt.getTime();
    }
    
    // Fallback: data-post attribute contains channel/message_id
    // We can't get exact time, but can use as secondary dedup key
    const postAttr = $el.closest('.tgme_widget_message').attr('data-post');
    if (postAttr) {
      // Format: "channel/12345" — we already have channel, so just log
      this.logger.debug(`Found data-post: ${postAttr} (using fallback timestamp)`);
    }
    
    return null;
  }

  /**
   * Filter out common boilerplate text that isn't user content
   */
  _isBoilerplate(text) {
    const patterns = [
      /forwarded from/i,
      /edited\b/i,
      /pinned message/i,
      /this channel is/i,
      /join chat/i
    ];
    return patterns.some(re => re.test(text));
  }

  /**
   * Generate deterministic hash for message deduplication
   * Uses SHA256 of normalized text (case-insensitive, trimmed)
   */
  _hashMessage(text) {
    const normalized = text.trim().toLowerCase();
    return crypto
      .createHash('sha256')
      .update(normalized)
      .digest('hex')
      .slice(0, 16); // 16-char hex = 64 bits, sufficient for dedup
  }

  /**
   * Simple delay utility for rate limiting
   */
  async delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}