export interface ModelInvoker {
  (prompt: string): Promise<string>;
}

export interface InvokeModelOptions {
  apiKey?: string;
  baseUrl?: string;
  model?: string;
  systemPrompt?: string;
  temperature?: number;
  maxTokens?: number;
  timeoutMs?: number;
  headers?: Record<string, string>;
}

interface ChatCompletionResponse {
  choices?: Array<{
    message?: {
      content?: string | Array<{ type?: string; text?: string }>;
    };
    text?: string;
  }>;
}

const DEFAULT_BASE_URL = "https://api.openai.com/v1/chat/completions";
const DEFAULT_MODEL = "gpt-4.1-mini";

function readEnv(name: string): string | undefined {
  const value = process.env[name];
  return value && value.trim() ? value.trim() : undefined;
}

function resolveApiKey(options: InvokeModelOptions): string {
  const apiKey = options.apiKey ?? readEnv("MODEL_API_KEY") ?? readEnv("OPENAI_API_KEY");
  if (!apiKey) {
    throw new Error("Missing API key. Set MODEL_API_KEY or OPENAI_API_KEY.");
  }
  return apiKey;
}

function resolveBaseUrl(options: InvokeModelOptions): string {
  return options.baseUrl ?? readEnv("MODEL_BASE_URL") ?? readEnv("OPENAI_BASE_URL") ?? DEFAULT_BASE_URL;
}

function extractTextContent(content: string | Array<{ type?: string; text?: string }> | undefined): string {
  if (typeof content === "string") return content;
  if (Array.isArray(content)) {
    return content
      .filter((item) => item?.type === "text" && typeof item.text === "string")
      .map((item) => item.text?.trim() ?? "")
      .filter(Boolean)
      .join("\n");
  }
  return "";
}

function parseResponse(data: ChatCompletionResponse): string {
  const firstChoice = data.choices?.[0];
  const content = extractTextContent(firstChoice?.message?.content);
  if (content) return content;
  if (typeof firstChoice?.text === "string" && firstChoice.text.trim()) return firstChoice.text.trim();
  throw new Error("Model response did not contain any text output.");
}

export async function invokeModel(prompt: string, options: InvokeModelOptions = {}): Promise<string> {
  const mockResponse = readEnv("MODEL_MOCK_RESPONSE");
  if (mockResponse) {
    return mockResponse;
  }

  const controller = new AbortController();
  const timeoutMs = options.timeoutMs ?? 45_000;
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(resolveBaseUrl(options), {
      method: "POST",
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${resolveApiKey(options)}`,
        ...(options.headers ?? {}),
      },
      body: JSON.stringify({
        model: options.model ?? readEnv("MODEL_NAME") ?? DEFAULT_MODEL,
        temperature: options.temperature ?? 0.7,
        max_tokens: options.maxTokens ?? 1600,
        messages: [
          {
            role: "system",
            content: options.systemPrompt ?? "You are a helpful assistant that must return structured Chinese content.",
          },
          {
            role: "user",
            content: prompt,
          },
        ],
      }),
    });

    if (!response.ok) {
      const errorBody = await response.text();
      throw new Error(`Model request failed with ${response.status}: ${errorBody}`);
    }

    const data = (await response.json()) as ChatCompletionResponse;
    return parseResponse(data);
  } finally {
    clearTimeout(timeout);
  }
}

export function createModelInvoker(options: InvokeModelOptions = {}): ModelInvoker {
  return (prompt: string) => invokeModel(prompt, options);
}
