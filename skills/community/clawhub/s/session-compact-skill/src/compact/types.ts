/**
 * Core type definitions for session management
 * Aligned with Claw Code's session/message architecture
 */

/**
 * Token usage tracking per message (matches Claw Code's TokenUsage)
 */
export interface TokenUsage {
  input_tokens: number;
  output_tokens: number;
  cache_creation_input_tokens: number;
  cache_read_input_tokens: number;
}

/**
 * Calculate total tokens from usage
 */
export function calculateTotalTokens(usage: TokenUsage): number {
  return (
    usage.input_tokens +
    usage.output_tokens +
    usage.cache_creation_input_tokens +
    usage.cache_read_input_tokens
  );
}

/**
 * Content block types (matches Claw Code's ContentBlock enum)
 */
export interface TextBlock {
  type: 'text';
  text: string;
}

export interface ToolUseBlock {
  type: 'tool_use';
  id: string;
  name: string;
  input: string;
}

export interface ToolResultBlock {
  type: 'tool_result';
  tool_use_id: string;
  tool_name: string;
  output: string;
  is_error: boolean;
}

export type ContentBlock = TextBlock | ToolUseBlock | ToolResultBlock;

/**
 * Message role types
 */
export type MessageRole = 'system' | 'user' | 'assistant' | 'tool';

/**
 * Conversation message with rich content blocks (matches Claw Code's ConversationMessage)
 */
export interface ConversationMessage {
  role: MessageRole;
  blocks: ContentBlock[];
  usage?: TokenUsage;
}

/**
 * Helper: Create a user text message
 */
export function createUserMessage(text: string): ConversationMessage {
  return {
    role: 'user',
    blocks: [{ type: 'text', text }],
    usage: undefined
  };
}

/**
 * Helper: Create an assistant message with blocks
 */
export function createAssistantMessage(
  blocks: ContentBlock[],
  usage?: TokenUsage
): ConversationMessage {
  return {
    role: 'assistant',
    blocks,
    usage
  };
}

/**
 * Helper: Create a tool result message
 */
export function createToolResultMessage(
  toolUseId: string,
  toolName: string,
  output: string,
  isError: boolean
): ConversationMessage {
  return {
    role: 'tool',
    blocks: [{
      type: 'tool_result',
      tool_use_id: toolUseId,
      tool_name: toolName,
      output,
      is_error: isError
    }],
    usage: undefined
  };
}

/**
 * Helper: Create a system message
 */
export function createSystemMessage(text: string): ConversationMessage {
  return {
    role: 'system',
    blocks: [{ type: 'text', text }],
    usage: undefined
  };
}

/**
 * Session structure (matches Claw Code's Session)
 */
export interface Session {
  version: number;
  messages: ConversationMessage[];
}

/**
 * Session metadata for tracking
 */
export interface SessionMetadata {
  session_id: string;
  created_at: string;
  updated_at: string;
  message_count: number;
  total_input_tokens: number;
  total_output_tokens: number;
  total_cache_tokens: number;
  compaction_count: number;
}

/**
 * Session error types
 */
export class SessionError extends Error {
  constructor(
    message: string,
    public code: 'IO_ERROR' | 'PARSE_ERROR' | 'NOT_FOUND' | 'INVALID_FORMAT'
  ) {
    super(message);
    this.name = 'SessionError';
  }
}

/**
 * Extract text content from a message (for backward compatibility)
 */
export function extractMessageText(message: ConversationMessage): string {
  return message.blocks
    .filter((block): block is TextBlock => block.type === 'text')
    .map(block => block.text)
    .join('\n');
}

/**
 * Convert legacy message format to new format
 */
export function convertLegacyMessage(
  legacy: { role: string; content?: string }
): ConversationMessage {
  return {
    role: legacy.role as MessageRole,
    blocks: [{ type: 'text', text: legacy.content || '' }],
    usage: undefined
  };
}

/**
 * Convert new message format to legacy format (for backward compatibility)
 */
export function convertToLegacyMessage(message: ConversationMessage): { role: string; content: string } {
  return {
    role: message.role,
    content: extractMessageText(message)
  };
}
