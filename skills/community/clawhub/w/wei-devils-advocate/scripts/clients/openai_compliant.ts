/**
 * OpenAI Compliant HTTP Client
 *
 * A generic HTTP client for any OpenAI-compatible API endpoint.
 * Works with any provider that follows the OpenAI API format:
 * - Local models (Ollama, llama.cpp, etc.)
 * - Third-party APIs (Together, Fireworks, Anyscale, etc.)
 * - Self-hosted endpoints
 *
 * Environment variables are automatically loaded from .env file by Bun.
 * See: https://bun.sh/docs/runtime/env
 */

import axios, { AxiosInstance, AxiosError } from 'axios';

/** Configuration for OpenAI compliant client */
export interface OpenAICompliantConfig {
  /** API key for authentication */
  apiKey: string;
  /** Base URL for the API (e.g., http://localhost:11434/v1) */
  baseUrl: string;
  /** Request timeout in seconds (default: 90) */
  timeout: number;
  /** Maximum number of retries (default: 3) */
  maxRetries: number;
  /** Delay between retries in seconds (default: 2.0) */
  retryDelay: number;
  /** Rate limit: requests per minute (default: 60) */
  rateLimitRequestsPerMinute: number;
  /** Optional organization ID */
  organization?: string;
  /** Optional project ID */
  project?: string;
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

/**
 * Generic OpenAI Compliant API Client
 *
 * Works with any API that follows OpenAI's REST API format.
 */
export class OpenAICompliantClient {
  private config: OpenAICompliantConfig;
  private rateLimiter: RateLimiter;
  private axiosInstance: AxiosInstance;

  /**
   * Create a new OpenAI compliant client
   *
   * @example
   * ```typescript
   * // For Ollama local model
   * const client = new OpenAICompliantClient({
   *   apiKey: 'ollama',  // Ollama doesn't require a real key
   *   baseUrl: 'http://localhost:11434/v1',
   * });
   *
   * // For Together AI
   * const client = new OpenAICompliantClient({
   *   apiKey: process.env.TOGETHER_API_KEY!,
   *   baseUrl: 'https://api.together.xyz/v1',
   * });
   * ```
   */
  constructor(config: Partial<OpenAICompliantConfig> & { apiKey: string; baseUrl: string }) {
    this.config = this.loadConfig(config);
    this.rateLimiter = new RateLimiter(this.config.rateLimitRequestsPerMinute);
    this.axiosInstance = this.createAxiosInstance();
  }

  /**
   * Create client from environment variables
   *
   * Expects:
   * - `{PREFIX}_API_KEY` - API key
   * - `{PREFIX}_BASE_URL` - Base URL (required)
   *
   * Optional:
   * - `{PREFIX}_TIMEOUT` - Timeout in seconds
   * - `{PREFIX}_MAX_RETRIES` - Max retries
   * - `{PREFIX}_RETRY_DELAY` - Retry delay in seconds
   * - `{PREFIX}_RATE_LIMIT_RPM` - Rate limit (requests per minute)
   */
  static fromEnv(prefix: string): OpenAICompliantClient {
    const apiKey = process.env[`${prefix}_API_KEY`] ?? process.env[`${prefix}_API_KEY`];
    const baseUrl = process.env[`${prefix}_BASE_URL`];

    if (!apiKey) {
      throw new Error(
        `API key not found. Set ${prefix}_API_KEY environment variable.`
      );
    }

    if (!baseUrl) {
      throw new Error(
        `Base URL not found. Set ${prefix}_BASE_URL environment variable.`
      );
    }

    return new OpenAICompliantClient({
      apiKey,
      baseUrl,
      timeout: parseInt(process.env[`${prefix}_TIMEOUT`] ?? '90', 10),
      maxRetries: parseInt(process.env[`${prefix}_MAX_RETRIES`] ?? '3', 10),
      retryDelay: parseFloat(process.env[`${prefix}_RETRY_DELAY`] ?? '2.0'),
      rateLimitRequestsPerMinute: parseInt(
        process.env[`${prefix}_RATE_LIMIT_RPM`] ?? '60',
        10
      ),
      organization: process.env[`${prefix}_ORGANIZATION`],
      project: process.env[`${prefix}_PROJECT`],
    });
  }

  /** Load configuration from environment variables and provided config */
  private loadConfig(
    providedConfig: Partial<OpenAICompliantConfig> & { apiKey: string; baseUrl: string }
  ): OpenAICompliantConfig {
    return {
      apiKey: providedConfig.apiKey,
      baseUrl: providedConfig.baseUrl,
      timeout: providedConfig.timeout ?? 90,
      maxRetries: providedConfig.maxRetries ?? 3,
      retryDelay: providedConfig.retryDelay ?? 2.0,
      rateLimitRequestsPerMinute: providedConfig.rateLimitRequestsPerMinute ?? 60,
      organization: providedConfig.organization,
      project: providedConfig.project,
    };
  }

  /** Create axios instance with default configuration */
  private createAxiosInstance(): AxiosInstance {
    const headers: Record<string, string> = {
      Authorization: `Bearer ${this.config.apiKey}`,
      'Content-Type': 'application/json',
    };

    if (this.config.organization) {
      headers['OpenAI-Organization'] = this.config.organization;
    }

    if (this.config.project) {
      headers['OpenAI-Project'] = this.config.project;
    }

    const instance = axios.create({
      baseURL: this.config.baseUrl,
      timeout: this.config.timeout * 1000,
      headers,
    });

    return instance;
  }

  /**
   * Make a chat completion request
   *
   * @example
   * ```typescript
   * const response = await client.chatCompletion(
   *   'llama3.2',
   *   [{ role: 'user', content: 'Hello!' }]
   * );
   * console.log(response.choices[0].message.content);
   * ```
   */
  async chatCompletion(
    model: string,
    messages: ChatMessage[],
    options: {
      temperature?: number;
      maxTokens?: number;
      topP?: number;
      topK?: number;
      frequencyPenalty?: number;
      presencePenalty?: number;
      responseFormat?: ResponseFormat;
      tools?: Tool[];
      toolChoice?: string;
      extraHeaders?: Record<string, string>;
      seed?: number;
      stop?: string | string[];
    } = {}
  ): Promise<ChatCompletionResponse> {
    const url = '/chat/completions';

    const payload: Record<string, unknown> = {
      model,
      messages,
      temperature: options.temperature ?? 0.7,
    };

    if (options.maxTokens) {
      payload.max_tokens = options.maxTokens;
    }

    if (options.topP !== undefined) {
      payload.top_p = options.topP;
    }

    if (options.topK !== undefined) {
      payload.top_k = options.topK;
    }

    if (options.frequencyPenalty !== undefined) {
      payload.frequency_penalty = options.frequencyPenalty;
    }

    if (options.presencePenalty !== undefined) {
      payload.presence_penalty = options.presencePenalty;
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

    if (options.seed !== undefined) {
      payload.seed = options.seed;
    }

    if (options.stop) {
      payload.stop = options.stop;
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
          headers,
        });

        const elapsedMs = Date.now() - startTime;
        console.info(`Request completed in ${elapsedMs}ms - Model: ${model}`);

        return response.data as ChatCompletionResponse;
      } catch (error) {
        const elapsedMs = Date.now() - startTime;
        const axiosError = error as AxiosError;

        // Handle network errors (timeout, connection error)
        if (
          axiosError.code === 'ECONNABORTED' ||
          axiosError.code === 'ENOTFOUND' ||
          axiosError.code === 'ECONNREFUSED'
        ) {
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

          throw new Error(`HTTP ${status}: ${JSON.stringify(axiosError.response.data)}`);
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
   * Create embeddings for text
   *
   * @example
   * ```typescript
   * const response = await client.embeddings(
   *   'text-embedding-3-small',
   *   'Hello world'
   * );
   * console.log(response.data[0].embedding);
   * ```
   */
  async embeddings(
    model: string,
    inputText: string | string[],
    options: {
      dimensions?: number;
      encodingFormat?: 'float' | 'base64';
      user?: string;
    } = {}
  ): Promise<EmbeddingsResponse> {
    const url = '/embeddings';

    const payload: Record<string, unknown> = {
      model,
      input: inputText,
    };

    if (options.dimensions) {
      payload.dimensions = options.dimensions;
    }

    if (options.encodingFormat) {
      payload.encoding_format = options.encodingFormat;
    }

    if (options.user) {
      payload.user = options.user;
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

  /**
   * List available models
   *
   * Note: Not all OpenAI-compliant APIs support this endpoint.
   */
  async listModels(): Promise<
    Array<{
      id: string;
      object: string;
      created: number;
      owned_by: string;
    }>
  > {
    try {
      const response = await this.axiosInstance.get('/models');
      return response.data.data;
    } catch (error) {
      const axiosError = error as AxiosError;
      console.warn(`Failed to list models: ${axiosError.message}`);
      return [];
    }
  }
}

/**
 * Factory function to create an OpenAI compliant client
 *
 * @example
 * ```typescript
 * const client = createOpenAICompliantClient({
 *   apiKey: 'your-api-key',
 *   baseUrl: 'https://api.your-provider.com/v1',
 * });
 * ```
 */
export function createOpenAICompliantClient(
  apiKey: string,
  baseUrl: string,
  options?: Partial<Omit<OpenAICompliantConfig, 'apiKey' | 'baseUrl'>>
): OpenAICompliantClient {
  return new OpenAICompliantClient({
    apiKey,
    baseUrl,
    ...options,
  });
}

/** Common OpenAI-compliant providers */
export const OPENAI_COMPLIANT_PROVIDERS = {
  /** OpenAI official */
  OPENAI: {
    baseUrl: 'https://api.openai.com/v1',
    envKey: 'OPENAI_API_KEY',
  },
  /** Azure OpenAI */
  AZURE: {
    baseUrl: 'https://{resource}.openai.azure.com/openai/deployments/{deployment}',
    envKey: 'AZURE_OPENAI_API_KEY',
  },
  /** Together AI */
  TOGETHER: {
    baseUrl: 'https://api.together.xyz/v1',
    envKey: 'TOGETHER_API_KEY',
  },
  /** Fireworks AI */
  FIREWORKS: {
    baseUrl: 'https://api.fireworks.ai/inference/v1',
    envKey: 'FIREWORKS_API_KEY',
  },
  /** Anyscale */
  ANYSCALE: {
    baseUrl: 'https://api.endpoints.anyscale.com/v1',
    envKey: 'ANYSCALE_API_KEY',
  },
  /** Ollama (local) */
  OLLAMA: {
    baseUrl: 'http://localhost:11434/v1',
    envKey: 'OLLAMA_API_KEY', // Usually not required, can be any string
  },
  /** LocalAI */
  LOCALAI: {
    baseUrl: 'http://localhost:8080/v1',
    envKey: 'LOCALAI_API_KEY',
  },
  /** llama.cpp server */
  LLAMA_CPP: {
    baseUrl: 'http://localhost:8080/v1',
    envKey: 'LLAMA_CPP_API_KEY',
  },
  /** Perplexity */
  PERPLEXITY: {
    baseUrl: 'https://api.perplexity.ai',
    envKey: 'PERPLEXITY_API_KEY',
  },
  /** Groq */
  GROQ: {
    baseUrl: 'https://api.groq.com/openai/v1',
    envKey: 'GROQ_API_KEY',
  },
  /** Cerebras */
  CEREBRAS: {
    baseUrl: 'https://api.cerebras.ai/v1',
    envKey: 'CEREBRAS_API_KEY',
  },
  /** AI21 */
  AI21: {
    baseUrl: 'https://api.ai21.com/studio/v1',
    envKey: 'AI21_API_KEY',
  },
  /** Mistral */
  MISTRAL: {
    baseUrl: 'https://api.mistral.ai/v1',
    envKey: 'MISTRAL_API_KEY',
  },
};

/** Create client for a specific provider */
export function createProviderClient(
  provider: keyof typeof OPENAI_COMPLIANT_PROVIDERS,
  apiKey?: string
): OpenAICompliantClient {
  const config = OPENAI_COMPLIANT_PROVIDERS[provider];
  const key = apiKey ?? process.env[config.envKey];

  if (!key) {
    throw new Error(
      `API key not found for ${provider}. Set ${config.envKey} environment variable.`
    );
  }

  return new OpenAICompliantClient({
    apiKey: key,
    baseUrl: config.baseUrl,
  });
}

// Export default
export default OpenAICompliantClient;
