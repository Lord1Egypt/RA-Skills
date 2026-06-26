/**
 * OpenRouter HTTP Client
 *
 * A reusable HTTP client for making requests to the OpenRouter API.
 * Supports rate limiting, retries, and configurable timeouts.
 *
 * Environment variables are automatically loaded from .env file by Bun.
 * See: https://bun.sh/docs/runtime/env
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import * as fs from 'fs';
import * as path from 'path';

/** Configuration for OpenRouter client */
export interface OpenRouterConfig {
  apiKey: string;
  baseUrl: string;
  timeout: number;
  maxRetries: number;
  retryDelay: number;
  rateLimitRequestsPerMinute: number;
  referer?: string;
  title?: string;
}

/** Chat message structure */
export interface ChatMessage {
  role: 'system' | 'user' | 'assistant' | 'tool';
  content: string;
  name?: string;
  tool_call_id?: string;
}

/** Response format specification */
export interface ResponseFormat {
  type: 'json_object' | 'text';
}

/** Tool definition for function calling */
export interface Tool {
  type: 'function';
  function: {
    name: string;
    description?: string;
    parameters?: Record<string, unknown>;
  };
}

/** Tool call in response */
export interface ToolCall {
  id: string;
  type: 'function';
  function: {
    name: string;
    arguments: string;
  };
}

/** Chat completion response */
export interface ChatCompletionResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: Array<{
    index: number;
    message: {
      role: string;
      content: string;
      tool_calls?: ToolCall[];
    };
    finish_reason: string;
  }>;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

/** Simple token bucket rate limiter */
class RateLimiter {
  private interval: number;
  private lastRequestTime: number = 0;

  constructor(requestsPerMinute: number) {
    this.interval = 60.0 / requestsPerMinute;
  }

  /** Wait if necessary to comply with rate limit */
  async acquire(): Promise<void> {
    const currentTime = Date.now() / 1000;
    const timeSinceLast = currentTime - this.lastRequestTime;

    if (timeSinceLast < this.interval) {
      const sleepTime = (this.interval - timeSinceLast) * 1000;
      await new Promise(resolve => setTimeout(resolve, sleepTime));
    }

    this.lastRequestTime = Date.now() / 1000;
  }
}

/** OpenRouter API Client */
export class OpenRouterClient {
  private config: OpenRouterConfig;
  private rateLimiter: RateLimiter;
  private axiosInstance: AxiosInstance;

  constructor(config?: Partial<OpenRouterConfig>) {
    this.config = this.loadConfig(config);
    this.rateLimiter = new RateLimiter(this.config.rateLimitRequestsPerMinute);
    this.axiosInstance = this.createAxiosInstance();
  }

  /** Load configuration from environment variables and provided config */
  private loadConfig(providedConfig?: Partial<OpenRouterConfig>): OpenRouterConfig {
    const apiKey = providedConfig?.apiKey ??
      process.env.OPENROUTER_API_KEY ??
      process.env.GROK_API_KEY;

    if (!apiKey) {
      throw new Error(
        'API key not found. Set OPENROUTER_API_KEY or GROK_API_KEY environment variable.'
      );
    }

    return {
      apiKey,
      baseUrl: providedConfig?.baseUrl ??
        process.env.OPENROUTER_BASE_URL ??
        'https://openrouter.ai/api/v1',
      timeout: providedConfig?.timeout ??
        parseInt(process.env.OPENROUTER_TIMEOUT ?? '90', 10),
      maxRetries: providedConfig?.maxRetries ??
        parseInt(process.env.OPENROUTER_MAX_RETRIES ?? '3', 10),
      retryDelay: providedConfig?.retryDelay ??
        parseFloat(process.env.OPENROUTER_RETRY_DELAY ?? '2.0'),
      rateLimitRequestsPerMinute: providedConfig?.rateLimitRequestsPerMinute ??
        parseInt(process.env.OPENROUTER_RATE_LIMIT_RPM ?? '60', 10),
      referer: providedConfig?.referer ?? 'https://github.com/wei-stock-analysis',
      title: providedConfig?.title ?? 'AI Stock Analysis Agent',
    };
  }

  /** Create axios instance with default configuration */
  private createAxiosInstance(): AxiosInstance {
    const instance = axios.create({
      baseURL: this.config.baseUrl,
      timeout: this.config.timeout * 1000,
      headers: {
        'Authorization': `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': this.config.referer,
        'X-Title': this.config.title,
      },
    });

    return instance;
  }

  /**
   * Make a chat completion request to OpenRouter
   */
  async chatCompletion(
    model: string,
    messages: ChatMessage[],
    options: {
      temperature?: number;
      maxTokens?: number;
      responseFormat?: ResponseFormat;
      tools?: Tool[];
      toolChoice?: string;
      extraHeaders?: Record<string, string>;
    } = {}
  ): Promise<ChatCompletionResponse> {
    const url = '/chat/completions';

    const payload: Record<string, unknown> = {
      model,
      messages,
      temperature: options.temperature ?? 0.1,
    };

    if (options.maxTokens) {
      payload.max_tokens = options.maxTokens;
    }

    if (options.responseFormat) {
      payload.response_format = options.responseFormat;
    }

    if (options.tools) {
      payload.tools = options.tools;
    }

    if (options.toolChoice) {
      payload.tool_choice = options.toolChoice;
    }

    const headers = options.extraHeaders ?? {};
    const maxAttempts = this.config.maxRetries + 1;

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      await this.rateLimiter.acquire();
      const startTime = Date.now();

      try {
        console.debug(
          `Making request to ${url} with model ${model} (attempt ${attempt}/${maxAttempts})`
        );

        const response = await this.axiosInstance.post(url, payload, {
          headers: headers,
        });

        const elapsedMs = Date.now() - startTime;
        console.info(`Request completed in ${elapsedMs}ms - Model: ${model}`);

        return response.data as ChatCompletionResponse;

      } catch (error) {
        const elapsedMs = Date.now() - startTime;
        const axiosError = error as AxiosError;

        // Handle network errors (timeout, connection error)
        if (axiosError.code === 'ECONNABORTED' || axiosError.code === 'ENOTFOUND') {
          console.warn(
            `Network error on attempt ${attempt}/${maxAttempts} after ${elapsedMs}ms: ${axiosError.message}`
          );

          if (attempt < maxAttempts) {
            const sleepTime = this.config.retryDelay * Math.pow(2, attempt - 1);
            console.info(`Retrying in ${sleepTime.toFixed(1)} seconds...`);
            await new Promise(resolve => setTimeout(resolve, sleepTime * 1000));
            continue;
          }
        }

        // Handle HTTP errors
        if (axiosError.response) {
          const status = axiosError.response.status;
          console.error(
            `HTTP error after ${elapsedMs}ms: ${status} - ${JSON.stringify(axiosError.response.data)}`
          );

          // Retry on rate limit or server errors
          if ([429, 500, 502, 503, 504].includes(status) && attempt < maxAttempts) {
            const sleepTime = this.config.retryDelay * Math.pow(2, attempt - 1);
            console.info(`Retrying in ${sleepTime.toFixed(1)} seconds...`);
            await new Promise(resolve => setTimeout(resolve, sleepTime * 1000));
            continue;
          }

          throw new Error(
            `HTTP ${status}: ${JSON.stringify(axiosError.response.data)}`
          );
        }

        // Handle request errors
        console.warn(
          `Request error on attempt ${attempt}/${maxAttempts} after ${elapsedMs}ms: ${axiosError.message}`
        );

        if (attempt < maxAttempts) {
          const sleepTime = this.config.retryDelay * Math.pow(2, attempt - 1);
          console.info(`Retrying in ${sleepTime.toFixed(1)} seconds...`);
          await new Promise(resolve => setTimeout(resolve, sleepTime * 1000));
          continue;
        }

        throw error;
      }
    }

    throw new Error('All attempts failed');
  }

  /** Save debug response to file when JSON parsing fails */
  private saveDebugResponse(response: unknown, error: Error): void {
    const debugDir = path.join(process.cwd(), 'intermediate');
    if (!fs.existsSync(debugDir)) {
      fs.mkdirSync(debugDir, { recursive: true });
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const debugFile = path.join(debugDir, `openrouter_debug_${timestamp}.txt`);

    fs.writeFileSync(debugFile, JSON.stringify({
      timestamp: new Date().toISOString(),
      error: error.message,
      response,
    }, null, 2));

    console.error(`Debug response saved to: ${debugFile}`);
  }
}

/**
 * Factory function to create a client with optional API key
 */
export function createOpenRouterClient(apiKey?: string): OpenRouterClient {
  if (apiKey) {
    return new OpenRouterClient({ apiKey });
  }
  return new OpenRouterClient();
}

/** Common model names for reference (OpenRouter format) */
export const OPENROUTER_MODELS = {
  // xAI models
  GROK_4_1_FAST: 'x-ai/grok-4.1-fast:online',
  GROK_4_1: 'x-ai/grok-4.1',
  GROK_3_BETA: 'x-ai/grok-3-beta',

  // OpenAI models
  GPT_4O: 'openai/gpt-4o',
  GPT_4O_MINI: 'openai/gpt-4o-mini',
  GPT_4_TURBO: 'openai/gpt-4-turbo',

  // Anthropic models
  CLAUDE_3_5_SONNET: 'anthropic/claude-3.5-sonnet',
  CLAUDE_3_OPUS: 'anthropic/claude-3-opus',

  // Google models
  GEMINI_1_5_PRO: 'google/gemini-1.5-pro',
  GEMINI_1_5_FLASH: 'google/gemini-1.5-flash',

  // DeepSeek models
  DEEPSEEK_CHAT: 'deepseek/deepseek-chat',
  DEEPSEEK_CODER: 'deepseek/deepseek-coder',

  // Meta models
  LLAMA_3_1_70B: 'meta-llama/llama-3.1-70b-instruct',
  LLAMA_3_1_405B: 'meta-llama/llama-3.1-405b-instruct',

  // 智谱 GLM
  GLM_5: 'zhipu/glm-5',
  GLM_4_PLUS: 'zhipu/glm-4-plus',

  // 月之暗面 Kimi
  KIMI_K2_5: 'moonshotai/kimi-k2.5',

  // 阿里通义千问
  QWEN3_MAX: 'qwen/qwen3-max',

  // MiniMax
  MINIMAX_M2_5: 'minimax/minimax-m2.5',
};

// Export default
export default OpenRouterClient;
