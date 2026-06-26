import type { ServerConfig } from "../config.js";
import { clipText, safeJsonParse } from "../utils/text.js";

type ChatMessage = {
  role: "system" | "user";
  content: string;
};

function extractMessageContent(payload: Record<string, unknown>): string {
  const choice = Array.isArray(payload.choices) ? payload.choices[0] : null;
  const message = choice && typeof choice === "object" ? (choice as { message?: { content?: unknown } }).message : undefined;
  const content = message?.content;
  if (typeof content === "string") return content.trim();
  if (Array.isArray(content)) {
    return content
      .map((item) => {
        if (typeof item === "string") return item;
        if (item && typeof item === "object" && "text" in item) {
          const text = (item as { text?: unknown }).text;
          return typeof text === "string" ? text : "";
        }
        return "";
      })
      .join("")
      .trim();
  }
  return "";
}

function extractJsonObject(raw: string): string {
  const trimmed = raw.trim();
  if (trimmed.startsWith("{") && trimmed.endsWith("}")) return trimmed;
  const start = trimmed.indexOf("{");
  const end = trimmed.lastIndexOf("}");
  if (start >= 0 && end > start) return trimmed.slice(start, end + 1);
  return trimmed;
}

export class ModelClient {
  constructor(private readonly config: ServerConfig) {}

  isEnabled(): boolean {
    return Boolean(this.config.knowledgeModelApiKey);
  }

  async generateJson<T>(messages: ChatMessage[], modelName: string): Promise<T | null> {
    if (!this.config.knowledgeModelApiKey) return null;

    const response = await fetch(`${this.config.knowledgeModelApiBase}/chat/completions`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        authorization: `Bearer ${this.config.knowledgeModelApiKey}`,
      },
      body: JSON.stringify({
        model: modelName,
        temperature: 0.1,
        messages,
      }),
    });

    const payload = (await response.json().catch(() => ({}))) as Record<string, unknown>;
    if (!response.ok) {
      const message = typeof payload.message === "string" ? payload.message : `Knowledge model request failed with status ${response.status}`;
      throw new Error(message);
    }

    const content = extractMessageContent(payload);
    const extracted = extractJsonObject(content);
    const parsed = safeJsonParse<T>(extracted);
    if (!parsed) {
      throw new Error(`Knowledge model returned non-JSON output: ${clipText(content, 320)}`);
    }
    return parsed;
  }
}
