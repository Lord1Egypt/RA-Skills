/**
 * Model Clients Index
 *
 * Exports all model clients for the multi-model researcher.
 */

export { BailianClient, createBailianClient, BAILIAN_MODELS } from './bailian.js';
export { OpenRouterClient, createOpenRouterClient, OPENROUTER_MODELS } from './openrouter.js';
export {
  OpenAICompliantClient,
  createOpenAICompliantClient,
  createProviderClient,
  OPENAI_COMPLIANT_PROVIDERS,
} from './openai_compliant.js';

// Re-export types
export type { BailianConfig, ChatMessage as BailianChatMessage, ChatCompletionResponse as BailianChatCompletionResponse } from './bailian.js';
export type { OpenRouterConfig, ChatMessage as OpenRouterChatMessage, ChatCompletionResponse as OpenRouterChatCompletionResponse } from './openrouter.js';
export type {
  OpenAICompliantConfig,
  ChatMessage as OpenAIChatMessage,
  ChatCompletionResponse as OpenAIChatCompletionResponse,
  EmbeddingsResponse,
  Tool,
  ToolCall,
} from './openai_compliant.js';
