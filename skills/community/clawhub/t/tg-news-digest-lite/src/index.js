import fs from "fs-extra";
import yaml from "yaml";
import { TelegramWebScraper } from "./scraper.js";
import { StateManager } from "./storage.js";
import { Summarizer } from "./summarizer.js";

// Minimal logger for skill runtime
const logger = {
  info: (...a) => console.log("[INFO]", ...a),
  warn: (...a) => console.warn("[WARN]", ...a),
  error: (...a) => console.error("[ERROR]", ...a),
  debug: (...a) => process.env.DEBUG && console.debug("[DEBUG]", ...a)
};

export const tools = {
  /**
   * Main tool: execute the full news digest pipeline
   * 
   * Flow:
   * 1. Load configuration (config.yaml or args)
   * 2. For each channel:
   *    a. Fetch public webpage via TelegramWebScraper
   *    b. Parse messages, generate SHA256 hashes
   *    c. Filter out already-seen messages using StateManager
   *    d. If new messages exist and meet threshold, send to Summarizer
   *    e. Update seen-messages cache
   * 3. Format all summaries into a single digest
   * 4. Deliver via ctx.send to configured notify_channel
   * 
   * @param {Object} params
   * @param {Object} params.context - OpenClaw runtime context (model, send, etc.)
   * @param {Object} params.args - Tool arguments from user/cli
   * @returns {Promise<Object>} Execution result with status and metrics
   */
  async run_digest_cycle({ context, args }) {
    const config = await this._loadConfig();
    const scraper = new TelegramWebScraper(config.monitoring, logger);
    const storage = new StateManager();
    const llm = new Summarizer(
      process.env.OPENCLAW_GATEWAY_URL || "http://127.0.0.1:18789",
      context.model?.primary
    );

    // Resolve channel list: args override config
    const rawChannels = args.channels?.length 
      ? args.channels 
      : config.monitoring.channels;
    
    const channels = rawChannels
      .map(c => scraper._normalizeChannel(c))
      .filter(Boolean); // Remove invalid entries

    if (!channels.length) {
      return { 
        status: "error", 
        message: "No valid channels provided. Use --args '{\"channels\":[\"durov\"]}' or update config.yaml" 
      };
    }

    let digest = [];
    let totalTokens = 0;
    let errors = [];

    // Process each channel sequentially (with rate limiting)
    for (const channel of channels) {
      try {
        // Respect rate limit to avoid IP throttling
        await scraper.delay(config.monitoring.rate_limit_ms);

        // Fetch and parse messages from public webpage
        const result = await scraper.fetchChannelMessages(
          channel, 
          config.monitoring.fetch_window
        );
        
        if (result.error) {
          errors.push(`${channel}: ${result.error}`);
          continue; // Continue with other channels
        }

        // Load previously seen message hashes for deduplication
        const seen = await storage.getSeenHashes(channel);
        
        // Filter to only new messages (by hash)
        const newMessages = result.messages.filter(m => !seen.has(m.id));

        // Skip if no new content (and not forced)
        if (!newMessages.length && !args.force) {
          logger.debug(`No new messages in @${channel}`);
          continue;
        }

        // Generate AI summary if enough new messages
        if (newMessages.length >= (config.digest.min_messages_for_summary || 1)) {
          const summary = await llm.generate(newMessages, config.digest);
          digest.push({
            channel,
            count: newMessages.length,
            ...summary
          });
          totalTokens += summary.token_count;
        }

        // Update cache with ALL fetched messages (not just new ones)
        // This ensures we don't re-process the same messages next time
        const allHashes = result.messages.map(m => m.id);
        await storage.updateSeenHashes(channel, allHashes);

      } catch (err) {
        errors.push(`${channel}: ${err.message}`);
        logger.error(`Pipeline error for ${channel}:`, err);
        // Continue processing other channels (fault isolation)
      }
    }

    // Deliver digest if we have content to report
    if (digest.length > 0) {
      const formatted = this._formatDigest(digest, config.digest);
      await this._notify(formatted, config.digest.notify_channel, context);
    }

    // Return structured result for logging/auditing
    return {
      status: digest.length ? "success" : "no_new_content",
      channels_checked: channels.length,
      channels_with_updates: digest.length,
      consumed_tokens: totalTokens,
      errors: errors.length ? errors : undefined,
      timestamp: new Date().toISOString()
    };
  },

  /**
   * Dynamically manage the list of monitored channels
   * Updates config.yaml and clears cache for removed channels
   */
  async configure_channels({ args }) {
    const configPath = "./config.yaml";
    const config = yaml.parse(await fs.readFile(configPath, "utf8"));
    const current = new Set(config.monitoring.channels);

    // Add new channels (normalize format)
    if (args.add?.length) {
      args.add.forEach(c => {
        const normalized = c.match(/t\.me\/(?:s\/)?@?([^/?#]+)/i)?.[1] || c.replace(/^@/, "");
        if (normalized) current.add(normalized);
      });
    }
    
    // Remove channels and clear their cache
    if (args.remove?.length) {
      args.remove.forEach(c => {
        const normalized = c.match(/t\.me\/(?:s\/)?@?([^/?#]+)/i)?.[1] || c.replace(/^@/, "");
        if (normalized) {
          current.delete(normalized);
          // Clear cache for removed channel
          const storage = new StateManager();
          await storage.clearChannel(normalized);
        }
      });
    }

    // Persist updated config
    config.monitoring.channels = Array.from(current);
    await fs.writeFile(configPath, yaml.stringify(config), "utf8");

    return { 
      status: "updated", 
      channels: Array.from(current),
      message: `Now monitoring ${current.size} channel(s)` 
    };
  },

  /**
   * Return operational status for monitoring/health checks
   */
  async get_status() {
    const config = await this._loadConfig();
    const storage = new StateManager();
    const state = await storage.init();
    
    return {
      tracked_channels: config.monitoring.channels.length,
      channels: config.monitoring.channels,
      cache_entries: Object.keys(state.channels).reduce(
        (sum, ch) => sum + (state.channels[ch]?.length || 0), 0
      ),
      rate_limit_ms: config.monitoring.rate_limit_ms,
      last_check: state.meta?.last_run || "never"
    };
  },

  // ===== Internal helpers =====

  async _loadConfig() {
    try {
      return yaml.parse(await fs.readFile("./config.yaml", "utf8"));
    } catch (err) {
      logger.warn("Config not found, using defaults");
      return {
        monitoring: { 
          channels: [], 
          fetch_window: 20, 
          rate_limit_ms: 2000,
          user_agent: "Mozilla/5.0 (X11; Linux x86_64)"
        },
        digest: { 
          language: "en", 
          max_tokens_per_channel: 300, 
          format: "markdown", 
          notify_channel: "default",
          min_messages_for_summary: 2
        }
      };
    }
  },

  _formatDigest(items, cfg) {
    const header = `📰 **Telegram News Digest**\n🕒 ${new Date().toLocaleString('en-US', { timeZone: 'UTC' })} UTC\n\n`;
    
    let body = "";
    const sorted = cfg.group_by === "time" 
      ? items.sort((a, b) => b.channel.localeCompare(a.channel)) // placeholder: real time sort would need timestamps
      : items;

    for (const item of sorted) {
      body += `🔹 **@${item.channel}** (${item.count} new message${item.count > 1 ? 's' : ''})\n`;
      body += `${item.summary}\n`;
      if (item.tags?.length) body += `🏷 ${item.tags.join(", ")}\n`;
      body += `\n`;
    }
    
    const footer = cfg.format === "markdown" 
      ? `\n*Generated by tg-news-digest-lite • [Report issues](https://github.com/your-org/tg-news-digest-lite)*`
      : "";

    return header + body + footer;
  },

  async _notify(text, channel, ctx) {
    // Preferred: use OpenClaw's session.send for integrated delivery
    if (typeof ctx?.send === "function") {
      await ctx.send({ channel, content: text });
      logger.info(`Digest sent to channel: ${channel}`);
    } else {
      // Fallback: log to stdout (for cron/heartbeat mode)
      console.log(`\n[NOTIFY → ${channel}]\n${text}\n`);
      logger.info(`Digest printed to stdout (configure notify_channel for integrated delivery)`);
    }
  }
};

export default { tools };