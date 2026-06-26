/**
 * 阿里云百炼 (Bailian/DashScope) HTTP Client
 *
 * A reusable HTTP client for making requests to the Alibaba Cloud Bailian API.
 * Supports rate limiting, retries, and configurable timeouts.
 *
 * Environment variables are automatically loaded from .env file by Bun.
 * See: https://bun.sh/docs/runtime/env
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import * as fs from 'fs';
import * as path from 'path';

/** Configuration for Bailian client */
export interface BailianConfig {
  apiKey: string;
  baseUrl: string;
  timeout: number;
  maxRetries: number;
  retryDelay: number;
  rateLimitRequestsPerMinute: number;
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

/** Search options for web search */
export interface SearchOptions {
  search_strategy?: 'standard' | 'pro';
  max_results?: number;
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
      tool_calls?: Array<{
        id: string;
        type: string;
        function: {
          name: string;
          arguments: string;
        };
      }>;
    };
    finish_reason: string;
  }>;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

/** Embeddings response */
export interface EmbeddingsResponse {
  object: string;
  data: Array<{
    object: string;
    embedding: number[];
    index: number;
  }>;
  model: string;
  usage: {
    prompt_tokens: number;
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

/** Bailian API Client */
export class BailianClient {
  private config: BailianConfig;
  private rateLimiter: RateLimiter;
  private axiosInstance: AxiosInstance;

  constructor(config?: Partial<BailianConfig>) {
    this.config = this.loadConfig(config);
    this.rateLimiter = new RateLimiter(this.config.rateLimitRequestsPerMinute);
    this.axiosInstance = this.createAxiosInstance();
  }

  /** Load configuration from environment variables and provided config */
  private loadConfig(providedConfig?: Partial<BailianConfig>): BailianConfig {
    const apiKey = providedConfig?.apiKey ??
      process.env.BAILIAN_API_KEY ??
      process.env.DASHSCOPE_API_KEY;

    if (!apiKey) {
      throw new Error(
        'API key not found. Set BAILIAN_API_KEY or DASHSCOPE_API_KEY environment variable.'
      );
    }

    return {
      apiKey,
      baseUrl: providedConfig?.baseUrl ??
        process.env.BAILIAN_BASE_URL ??
        'https://dashscope.aliyuncs.com/compatible-mode/v1',
      timeout: providedConfig?.timeout ??
        parseInt(process.env.BAILIAN_TIMEOUT ?? '90', 10),
      maxRetries: providedConfig?.maxRetries ??
        parseInt(process.env.BAILIAN_MAX_RETRIES ?? '3', 10),
      retryDelay: providedConfig?.retryDelay ??
        parseFloat(process.env.BAILIAN_RETRY_DELAY ?? '2.0'),
      rateLimitRequestsPerMinute: providedConfig?.rateLimitRequestsPerMinute ??
        parseInt(process.env.BAILIAN_RATE_LIMIT_RPM ?? '60', 10),
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
      },
    });

    return instance;
  }

  /**
   * Make a chat completion request to Bailian API
   *
   * Model naming convention (like OpenRouter):
   * - If model ends with `:online`, the `:online` suffix is stripped and web search is enabled
   *   e.g., "qwen-max:latest:online" -> model="qwen-max:latest", enable_search=true
   */
  async chatCompletion(
    model: string,
    messages: ChatMessage[],
    options: {
      temperature?: number;
      maxTokens?: number;
      topP?: number;
      responseFormat?: ResponseFormat;
      tools?: Tool[];
      toolChoice?: string;
      extraHeaders?: Record<string, string>;
      enableSearch?: boolean;
      searchOptions?: SearchOptions;
    } = {}
  ): Promise<ChatCompletionResponse> {
    const url = '/chat/completions';

    // Handle :online suffix (like OpenRouter convention)
    // If model ends with :online, strip it and enable web search
    let actualModel = model;
    let enableSearch = options.enableSearch;
    if (model.endsWith(':online')) {
      actualModel = model.slice(0, -7); // Remove ':online' suffix
      enableSearch = true; // Auto-enable web search
      console.info(`[BailianClient] Detected :online suffix, using model "${actualModel}" with web search enabled`);
    }

    const payload: Record<string, unknown> = {
      model: actualModel,
      messages,
      temperature: options.temperature ?? 0.7,
    };

    if (options.maxTokens) {
      payload.max_tokens = options.maxTokens;
    }

    if (options.topP !== undefined) {
      payload.top_p = options.topP;
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

    // Bailian-specific parameters for web search
    if (enableSearch !== undefined) {
      payload.enable_search = enableSearch;
    }

    if (options.searchOptions) {
      payload.search_options = options.searchOptions;
    }

    const headers = options.extraHeaders ?? {};
    const maxAttempts = this.config.maxRetries + 1;

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      await this.rateLimiter.acquire();
      const startTime = Date.now();

      try {
        console.debug(
          `Making request to ${url} with model ${actualModel} (attempt ${attempt}/${maxAttempts})`
        );

        const response = await this.axiosInstance.post(url, payload, {
          headers: headers,
        });

        const elapsedMs = Date.now() - startTime;
        console.info(`Request completed in ${elapsedMs}ms - Model: ${actualModel}`);

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

  /**
   * Create embeddings for text using Bailian embedding models
   */
  async embeddings(
    model: string,
    inputText: string | string[],
    options: {
      dimensions?: number;
      encodingFormat?: 'float' | 'base64';
    } = {}
  ): Promise<EmbeddingsResponse> {
    const url = '/embeddings';

    const payload: Record<string, unknown> = {
      model,
      input: inputText,
      encoding_format: options.encodingFormat ?? 'float',
    };

    if (options.dimensions) {
      payload.dimensions = options.dimensions;
    }

    await this.rateLimiter.acquire();
    const startTime = Date.now();

    try {
      console.debug(`Making embedding request with model ${model}`);

      const response = await this.axiosInstance.post(url, payload);

      const elapsedMs = Date.now() - startTime;
      console.info(`Embedding request completed in ${elapsedMs}ms - Model: ${model}`);

      return response.data as EmbeddingsResponse;

    } catch (error) {
      const axiosError = error as AxiosError;
      console.error(`Embedding request failed: ${axiosError.message}`);
      throw error;
    }
  }

  /** Save debug response to file when JSON parsing fails */
  private saveDebugResponse(response: unknown, error: Error): void {
    const debugDir = path.join(process.cwd(), 'intermediate');
    if (!fs.existsSync(debugDir)) {
      fs.mkdirSync(debugDir, { recursive: true });
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const debugFile = path.join(debugDir, `bailian_debug_${timestamp}.txt`);

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
export function createBailianClient(apiKey?: string): BailianClient {
  if (apiKey) {
    return new BailianClient({ apiKey });
  }
  return new BailianClient();
}

/** Common model names for reference */
export const BAILIAN_MODELS = {
  // Qwen series (通义千问)
  QWEN_MAX: 'qwen-max',
  QWEN_MAX_LATEST: 'qwen-max-latest',
  QWEN_PLUS: 'qwen-plus',
  QWEN_PLUS_LATEST: 'qwen-plus-latest',
  QWEN_TURBO: 'qwen-turbo',
  QWEN_TURBO_LATEST: 'qwen-turbo-latest',

  // DeepSeek series
  DEEPSEEK_R1: 'deepseek-r1',
  DEEPSEEK_V3: 'deepseek-v3',
  DEEPSEEK_R1_DISTILL_QWEN: 'deepseek-r1-distill-qwen',

  // Embedding models
  TEXT_EMBEDDING_V3: 'text-embedding-v3',
  TEXT_EMBEDDING_V2: 'text-embedding-v2',
};

// Export default
export default BailianClient;
