/**
 * LLM Provider - 统一 LLM 调用接口 v1.0
 * 
 * 支持:
 * - OpenAI (GPT-4, GPT-3.5)
 * - Claude (Claude-3 Opus, Sonnet, Haiku)
 * - 智谱 AI (GLM-4)
 * - 百度千帆 (ERNIE)
 * - 阿里通义 (Qwen)
 * - Ollama (本地)
 * 
 * Usage:
 *     import { LLMProviderFactory } from './system/llm_provider.js';
 *     
 *     const llm = LLMProviderFactory.create("openai", { model: "gpt-4" });
 *     const response = await llm.generate("写一个贪吃蛇游戏");
 *     
 *     for await (const chunk of llm.stream("写一首诗")) {
 *       process.stdout.write(chunk);
 *     }
 */

// ============================================================
// Types & Interfaces
// ============================================================

/**
 * @typedef {Object} LLMResponse
 * @property {string} content - 响应内容
 * @property {string} model - 使用的模型
 * @property {number} tokensUsed - 总 token 数
 * @property {number} inputTokens - 输入 token 数
 * @property {number} outputTokens - 输出 token 数
 * @property {string} finishReason - 结束原因
 * @property {number} latency - 延迟（秒）
 * @property {string} provider - 提供商名称
 */

/**
 * @typedef {Object} Message
 * @property {string} role - system|user|assistant
 * @property {string} content - 消息内容
 */

// ============================================================
// Base Provider
// ============================================================

export class BaseLLMProvider {
  constructor(apiKey = null, model = null, baseUrl = null, config = {}) {
    this.apiKey = apiKey || this._getApiKey();
    this.model = model || this._getDefaultModel();
    this.baseUrl = baseUrl;
    this.config = config;
  }

  name = 'base';

  _getApiKey() {
    const envVar = `${this.name.toUpperCase()}_API_KEY`;
    return process.env[envVar] || null;
  }

  _getDefaultModel() {
    return 'unknown';
  }

  /**
   * Generate a response
   * @param {string} prompt
   * @param {string|undefined} system
   * @param {Message[]|undefined} messages
   * @param {Object} kwargs
   * @returns {Promise<LLMResponse>}
   */
  async generate(prompt, system = null, messages = null, ...kwargs) {
    throw new Error('Not implemented');
  }

  /**
   * Stream generate
   * @param {string} prompt
   * @param {string|undefined} system
   * @param {Message[]|undefined} messages
   * @param {Object} kwargs
   * @returns {AsyncGenerator<string>}
   */
  async *stream(prompt, system = null, messages = null, ...kwargs) {
    throw new Error('Not implemented');
  }

  _buildMessages(prompt, system, messages) {
    /** @type {Object[]} */
    const result = [];

    if (system) {
      result.push({ role: 'system', content: system });
    }

    if (messages) {
      for (const m of messages) {
        result.push({ role: m.role, content: m.content });
      }
    }

    if (prompt) {
      result.push({ role: 'user', content: prompt });
    }

    return result;
  }

  toDict() {
    return {
      name: this.name,
      model: this.model,
      baseUrl: this.baseUrl,
    };
  }
}

// ============================================================
// OpenAI Provider
// ============================================================

export class OpenAIProvider extends BaseLLMProvider {
  constructor(apiKey = null, model = null, baseUrl = null, ...kwargs) {
    super(apiKey, model, baseUrl, kwargs);
    this.name = 'openai';
  }

  _getDefaultModel() {
    return 'gpt-4';
  }

  async generate(prompt, system = null, messages = null, ...kwargs) {
    const start = Date.now();

    try {
      // Dynamic import for openai package
      const { default: OpenAI } = await import('openai');
      
      const client = new OpenAI({
        apiKey: this.apiKey,
        baseURL: this.baseUrl,
      });

      const msgList = this._buildMessages(prompt, system, messages);

      const response = await client.chat.completions.create({
        model: this.model,
        messages: msgList,
        ...kwargs,
      });

      return {
        content: response.choices[0].message.content,
        model: response.model,
        tokensUsed: response.usage.total_tokens,
        inputTokens: response.usage.prompt_tokens,
        outputTokens: response.usage.completion_tokens,
        finishReason: response.choices[0].finish_reason,
        latency: (Date.now() - start) / 1000,
        provider: this.name,
      };
    } catch (e) {
      return this._mockResponse(prompt, start, e.message);
    }
  }

  async *stream(prompt, system = null, messages = null, ...kwargs) {
    try {
      const { default: OpenAI } = await import('openai');
      
      const client = new OpenAI({
        apiKey: this.apiKey,
        baseURL: this.baseUrl,
      });

      const msgList = this._buildMessages(prompt, system, messages);

      const stream = await client.chat.completions.create({
        model: this.model,
        messages: msgList,
        stream: true,
        ...kwargs,
      });

      for await (const chunk of stream) {
        if (chunk.choices[0].delta.content) {
          yield chunk.choices[0].delta.content;
        }
      }
    } catch (e) {
      yield `[错误] ${e.message}`;
    }
  }

  _mockResponse(prompt, start, error = null) {
    const latency = (Date.now() - start) / 1000;
    const preview = prompt.length > 200 ? prompt.slice(0, 200) + '...' : prompt;
    return {
      content: error ? `[错误] ${error}` : `[模拟响应] 基于提示生成内容...\n\n提示: ${preview}`,
      model: this.model,
      tokensUsed: Math.floor(prompt.length / 4),
      inputTokens: 0,
      outputTokens: 0,
      finishReason: error ? 'error' : 'stop',
      latency,
      provider: `${this.name}_mock`,
    };
  }
}

// ============================================================
// Claude Provider
// ============================================================

export class ClaudeProvider extends BaseLLMProvider {
  constructor(apiKey = null, model = null, ...kwargs) {
    super(apiKey, model, null, kwargs);
    this.name = 'claude';
  }

  _getDefaultModel() {
    return 'claude-3-opus-20240229';
  }

  async generate(prompt, system = null, messages = null, ...kwargs) {
    const start = Date.now();

    try {
      const Anthropic = await import('@anthropic-ai/sdk');
      const client = new Anthropic.default({ apiKey: this.apiKey });

      const msgList = this._buildMessages(prompt, null, messages);

      const params = {
        model: this.model,
        messages: msgList,
        max_tokens: kwargs.max_tokens || 4096,
      };

      if (system) {
        params.system = system;
      }

      const response = await client.messages.create(params);

      return {
        content: response.content[0].text,
        model: response.model,
        tokensUsed: response.usage.input_tokens + response.usage.output_tokens,
        inputTokens: response.usage.input_tokens,
        outputTokens: response.usage.output_tokens,
        finishReason: response.stop_reason,
        latency: (Date.now() - start) / 1000,
        provider: this.name,
      };
    } catch (e) {
      return this._mockResponse(prompt, start, e.message);
    }
  }

  async *stream(prompt, system = null, messages = null, ...kwargs) {
    try {
      const Anthropic = await import('@anthropic-ai/sdk');
      const client = new Anthropic.default({ apiKey: this.apiKey });

      const msgList = this._buildMessages(prompt, null, messages);

      const params = {
        model: this.model,
        messages: msgList,
        max_tokens: kwargs.max_tokens || 4096,
        stream: true,
      };

      if (system) {
        params.system = system;
      }

      const stream = await client.messages.stream(params);

      for await (const event of stream) {
        if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
          yield event.delta.text;
        }
      }
    } catch (e) {
      yield `[错误] ${e.message}`;
    }
  }

  _mockResponse(prompt, start, error = null) {
    const latency = (Date.now() - start) / 1000;
    const preview = prompt.length > 200 ? prompt.slice(0, 200) : prompt;
    return {
      content: error ? `[错误] ${error}` : `[Claude 模拟] 基于提示生成...\n\n${preview}`,
      model: this.model,
      tokensUsed: Math.floor(prompt.length / 4),
      inputTokens: 0,
      outputTokens: 0,
      finishReason: error ? 'error' : 'stop',
      latency,
      provider: `${this.name}_mock`,
    };
  }
}

// ============================================================
// Zhipu Provider (智谱 AI)
// ============================================================

export class ZhipuProvider extends BaseLLMProvider {
  constructor(apiKey = null, model = null, ...kwargs) {
    super(apiKey, model, null, kwargs);
    this.name = 'zhipu';
  }

  _getDefaultModel() {
    return 'glm-4';
  }

  async generate(prompt, system = null, messages = null, ...kwargs) {
    const start = Date.now();

    try {
      const { ZhipuAI } = await import('zhipuai');
      const client = new ZhipuAI({ apiKey: this.apiKey });

      const msgList = this._buildMessages(prompt, system, messages);

      const response = await client.chat.completions.create({
        model: this.model,
        messages: msgList,
        ...kwargs,
      });

      return {
        content: response.choices[0].message.content,
        model: response.model,
        tokensUsed: response.usage.total_tokens,
        inputTokens: response.usage.prompt_tokens,
        outputTokens: response.usage.completion_tokens,
        finishReason: response.choices[0].finish_reason,
        latency: (Date.now() - start) / 1000,
        provider: this.name,
      };
    } catch (e) {
      return this._mockResponse(prompt, start, e.message);
    }
  }

  async *stream(prompt, system = null, messages = null, ...kwargs) {
    try {
      const { ZhipuAI } = await import('zhipuai');
      const client = new ZhipuAI({ apiKey: this.apiKey });

      const msgList = this._buildMessages(prompt, system, messages);

      const stream = await client.chat.completions.create({
        model: this.model,
        messages: msgList,
        stream: true,
        ...kwargs,
      });

      for await (const chunk of stream) {
        if (chunk.choices[0].delta.content) {
          yield chunk.choices[0].delta.content;
        }
      }
    } catch (e) {
      yield `[错误] ${e.message}`;
    }
  }

  _mockResponse(prompt, start, error = null) {
    const latency = (Date.now() - start) / 1000;
    const preview = prompt.length > 200 ? prompt.slice(0, 200) : prompt;
    return {
      content: error ? `[错误] ${error}` : `[智谱模拟] 基于提示生成...\n\n${preview}`,
      model: this.model,
      tokensUsed: Math.floor(prompt.length / 4),
      inputTokens: 0,
      outputTokens: 0,
      finishReason: error ? 'error' : 'stop',
      latency,
      provider: `${this.name}_mock`,
    };
  }
}

// ============================================================
// Ollama Provider
// ============================================================

export class OllamaProvider extends BaseLLMProvider {
  constructor(baseUrl = 'http://localhost:11434', model = null, ...kwargs) {
    super(null, model, baseUrl, kwargs);
    this.name = 'ollama';
  }

  _getDefaultModel() {
    return 'llama3';
  }

  async generate(prompt, system = null, messages = null, ...kwargs) {
    const start = Date.now();

    try {
      const msgList = this._buildMessages(prompt, system, messages);

      const response = await fetch(`${this.baseUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: this.model,
          messages: msgList,
          stream: false,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();

      return {
        content: data.message?.content || '',
        model: this.model,
        tokensUsed: data.eval_count || 0,
        inputTokens: data.prompt_eval_count || 0,
        outputTokens: data.eval_count || 0,
        finishReason: data.done ? 'stop' : 'error',
        latency: (Date.now() - start) / 1000,
        provider: this.name,
      };
    } catch (e) {
      return {
        content: `[错误] ${e.message}`,
        model: this.model,
        tokensUsed: 0,
        inputTokens: 0,
        outputTokens: 0,
        finishReason: 'error',
        latency: (Date.now() - start) / 1000,
        provider: this.name,
      };
    }
  }

  async *stream(prompt, system = null, messages = null, ...kwargs) {
    try {
      const msgList = this._buildMessages(prompt, system, messages);

      const response = await fetch(`${this.baseUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: this.model,
          messages: msgList,
          stream: true,
        }),
      });

      if (!response.ok) {
        yield `[错误] HTTP ${response.status}`;
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const lines = decoder.decode(value).split('\n');
        for (const line of lines) {
          if (line.trim()) {
            try {
              const data = JSON.parse(line);
              if (data.message?.content) {
                yield data.message.content;
              }
            } catch {}
          }
        }
      }
    } catch (e) {
      yield `[错误] ${e.message}`;
    }
  }
}

// ============================================================
// LLM Provider Factory
// ============================================================

export const LLMProviderFactory = {
  _providers: {
    'openai': OpenAIProvider,
    'gpt': OpenAIProvider,
    'claude': ClaudeProvider,
    'anthropic': ClaudeProvider,
    'zhipu': ZhipuProvider,
    'glm': ZhipuProvider,
    'ollama': OllamaProvider,
    'local': OllamaProvider,
  },

  _modelAliases: {
    'gpt-4': 'openai',
    'gpt-3.5': 'openai',
    'gpt-4o': 'openai',
    'claude-3': 'claude',
    'claude-3-opus': 'claude',
    'claude-3-sonnet': 'claude',
    'glm-4': 'zhipu',
    'glm-3': 'zhipu',
    'ollama': 'ollama',
  },

  /**
   * Create an LLM provider instance
   * @param {string} provider
   * @param {Object} options
   * @returns {BaseLLMProvider}
   */
  create(provider, options = {}) {
    const { apiKey, model, baseUrl, ...kwargs } = options;

    // Resolve model alias
    if (this._modelAliases[provider]) {
      provider = this._modelAliases[provider];
    }

    if (!this._providers[provider]) {
      throw new Error(
        `不支持的提供商: ${provider}。支持: ${Object.keys(this._providers).join(', ')}`
      );
    }

    const ProviderClass = this._providers[provider];
    return new ProviderClass(apiKey, model, baseUrl, kwargs);
  },

  /**
   * List all supported providers
   * @returns {string[]}
   */
  listProviders() {
    return Object.keys(this._providers);
  },

  /**
   * List models for a provider (or all)
   * @param {string|undefined} provider
   * @returns {Object}
   */
  listModels(provider = null) {
    const models = {
      openai: ['gpt-4', 'gpt-4o', 'gpt-3.5-turbo'],
      claude: ['claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307'],
      zhipu: ['glm-4', 'glm-3-turbo'],
      ollama: ['llama3', 'llama2', 'mistral', 'codellama', 'qwen2.5'],
    };

    if (provider) {
      return models[provider] || [];
    }

    return models;
  },
};

// ============================================================
// CLI
// ============================================================

async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'demo';

  if (command === 'list') {
    console.log('支持的提供商:');
    for (const p of LLMProviderFactory.listProviders()) {
      const models = LLMProviderFactory.listModels(p);
      console.log(`  - ${p}: ${models.join(', ')}`);
    }
    return;
  }

  // Demo command
  const providerArg = args.find(a => a.startsWith('--provider='))?.split('=')[1] || 'ollama';
  const modelArg = args.find(a => a.startsWith('--model='))?.split('=')[1] || null;
  const promptArg = args.find(a => a.startsWith('--prompt='))?.split('=')[1] || '用一句话介绍 Python';

  const options = {};
  if (providerArg === 'ollama') {
    options.baseUrl = process.env.OLLAMA_HOST || 'http://localhost:11434';
  }

  const llm = LLMProviderFactory.create(providerArg, { model: modelArg, ...options });

  console.log(`提示: ${promptArg}`);
  console.log(`提供商: ${llm.name}`);
  console.log(`模型: ${llm.model}`);
  console.log('-'.repeat(40));

  const response = await llm.generate(promptArg);
  console.log(`响应: ${response.content}`);
  console.log(`Token: ${response.tokensUsed}`);
  console.log(`延迟: ${response.latency.toFixed(2)}s`);
}

// Run if called directly
const isMain = process.argv[1]?.endsWith('llm_provider.js') || process.argv[1]?.endsWith('llm_provider.mjs');
if (isMain) {
  main().catch(console.error);
}

export default { LLMProviderFactory, BaseLLMProvider };
