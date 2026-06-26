import { createOpenAI } from "openai";

export class Summarizer {
  constructor(gatewayUrl, defaultModel) {
    this.client = createOpenAI({
      baseURL: `${gatewayUrl}/v1`,
      apiKey: process.env.OPENCLAW_GATEWAY_TOKEN || "openclaw",
      timeout: 30000
    });
    this.model = defaultModel || "qwen/qwen3.5-35b";
  }

  /**
   * Generate structured summary from message list using LLM
   * @param {Array} messages - Array of {text, timestamp, channel}
   * @param {Object} config - Digest configuration (language, tokens, etc.)
   * @returns {Promise<Object>} {summary, tags, sentiment, token_count, status}
   */
  async generate(messages, config) {
    if (!messages?.length) {
      return { summary: "", token_count: 0, status: "empty", tags: [], sentiment: "neutral" };
    }

    const prompt = this._buildPrompt(messages, config);
    
    try {
      const res = await this.client.chat.completions.create({
        model: this.model,
        messages: [{ role: "user", content: prompt }],
        temperature: 0.3, // Low temperature for factual summaries
        max_tokens: config.max_tokens_per_channel || 300,
        response_format: { type: "json_object" } // Enforce JSON output
      });

      const raw = res.choices[0]?.message?.content || "{}";
      const parsed = JSON.parse(raw);
      
      return {
        summary: parsed.summary || "No significant updates detected.",
        tags: Array.isArray(parsed.tags) ? parsed.tags : [],
        sentiment: ["positive", "neutral", "negative"].includes(parsed.sentiment) 
          ? parsed.sentiment 
          : "neutral",
        token_count: res.usage?.completion_tokens || 0,
        status: "success"
      };
    } catch (err) {
      // Graceful fallback: return raw messages if LLM fails
      const fallbackText = messages
        .slice(-3) // Last 3 messages as representative sample
        .map(m => `• ${m.text}`)
        .join("\n");
      
      return {
        summary: `[LLM unavailable] Latest messages:\n${fallbackText}`,
        tags: [],
        sentiment: "unknown",
        token_count: 0,
        status: "fallback"
      };
    }
  }

  /**
   * Construct prompt that guides LLM to produce structured, concise output
   */
  _buildPrompt(messages, config) {
    const messageList = messages
      .map(m => `• ${m.text}`)
      .join("\n");
    
    return `You are a professional news analyst. Review these Telegram messages and return ONLY valid JSON:

{
  "summary": "Concise summary in ${config.language} (max ${config.max_tokens_per_channel} tokens). Focus on factual updates, ignore spam/repeats/ads.",
  "tags": ["topic1", "topic2"],
  "sentiment": "positive|neutral|negative"
}

Messages from channel:
${messageList}

Rules:
- Output MUST be valid JSON, no markdown, no explanations
- Summary should be 2-4 bullet points worth of information
- Tags should be 2-4 relevant keywords
- If no meaningful content, set summary to "No significant updates.`;
  }
}