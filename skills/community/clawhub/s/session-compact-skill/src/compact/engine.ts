import { loadConfig, type CompactConfig } from './config.js';
import {
  ConversationMessage,
  ContentBlock,
  TextBlock,
  ToolUseBlock,
  ToolResultBlock,
  TokenUsage,
  extractMessageText,
  convertLegacyMessage
} from './types.js';
import { execSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

interface LLMResponse {
  content: string;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
  };
}

/**
 * 读取 OpenClaw 配置获取当前模型
 */
export function getCurrentModel(): string {
  const configPath = join(homedir(), '.openclaw', 'openclaw.json');
  try {
    const config = JSON.parse(readFileSync(configPath, 'utf-8'));
    return config.models?.defaults?.default || config.default_model || config.model || 'qwen/qwen3.5-122b-a10b';
  } catch (error) {
    console.warn('[LLM] Failed to read config, using default:', error);
    return 'qwen/qwen3.5-122b-a10b';
  }
}

/**
 * 调用 OpenClaw 的 LLM 服务（通过 CLI 命令）
 */
async function callLLM(options: { 
  model: string; 
  messages: Array<{ role: string; content: string }>; 
  max_tokens: number; 
  temperature?: number; 
}): Promise<LLMResponse> {
  const prompt = options.messages[0].content;
  let modelToUse = options.model || getCurrentModel();
  if (!modelToUse || modelToUse.trim() === '') {
    modelToUse = getCurrentModel();
    console.log(`[LLM] Using global default model: ${modelToUse}`);
  }

  const escapedPrompt = prompt
    .replace(/\\/g, '\\\\')
    .replace(/"/g, '\\"')
    .replace(/\n/g, '\\n')
    .replace(/\r/g, '\\r');

  try {
    const sessionId = `compact-${Date.now()}`;
    const command = `openclaw agent --session-id "${sessionId}" --message "${escapedPrompt}" --json --timeout 60`;
    const output = execSync(command, {
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe'],
      timeout: 65000
    });

    try {
      const result = JSON.parse(output);
      if (result.result && result.result.payloads && result.result.payloads.length > 0) {
        return {
          content: result.result.payloads[0].text,
          usage: result.result.meta?.agentMeta?.lastCallUsage || undefined
        };
      }
      return {
        content: result.result?.payloads?.[0]?.text || result.summary || output,
        usage: undefined
      };
    } catch (parseError) {
      console.error('[LLM] JSON parse failed:', parseError);
      return { content: output.trim(), usage: undefined };
    }
  } catch (error: any) {
    console.error('[LLM] Call failed:', error.message);
    if (error.message.includes('command not found')) {
      throw new Error('OpenClaw CLI not found. Please ensure it is installed and in PATH.');
    }
    if (error.message.includes('Gateway agent failed')) {
      throw new Error('Gateway connection failed. Please run `openclaw gateway start` or check your configuration.');
    }
    throw new Error(`LLM call failed: ${error.message}`);
  }
}

export interface CompactionResult {
  summary: string;
  formattedSummary: string;
  removedCount: number;
  savedTokens: number;
  originalTokens: number;
  compactedTokens: number;
}

/**
 * 估算消息的 Token 数量 (支持新旧两种消息格式)
 */
export function estimateTokenCount(
  messages: Array<{ content?: string } | ConversationMessage>
): number {
  return messages.reduce((sum, msg) => {
    // Check if it's the new ConversationMessage format
    if ('blocks' in msg) {
      const conversationMsg = msg as ConversationMessage;
      return sum + estimateMessageTokens(conversationMsg);
    }
    // Legacy format
    const text = msg.content || '';
    return sum + Math.ceil(text.length / 4);
  }, 0);
}

/**
 * 估算单个 ConversationMessage 的 Token 数量
 */
function estimateMessageTokens(message: ConversationMessage): number {
  return message.blocks.reduce((sum, block) => {
    switch (block.type) {
      case 'text':
        return sum + Math.ceil(block.text.length / 4) + 1;
      case 'tool_use':
        return sum + Math.ceil((block.name.length + block.input.length) / 4) + 1;
      case 'tool_result':
        return sum + Math.ceil((block.tool_name.length + block.output.length) / 4) + 1;
      default:
        return sum;
    }
  }, 0);
}

/**
 * 计算会话中的实际 Token 使用量 (从 usage 元数据)
 */
export function calculateActualTokenUsage(messages: ConversationMessage[]): TokenUsage {
  const total: TokenUsage = {
    input_tokens: 0,
    output_tokens: 0,
    cache_creation_input_tokens: 0,
    cache_read_input_tokens: 0
  };

  for (const msg of messages) {
    if (msg.usage) {
      total.input_tokens += msg.usage.input_tokens;
      total.output_tokens += msg.usage.output_tokens;
      total.cache_creation_input_tokens += msg.usage.cache_creation_input_tokens;
      total.cache_read_input_tokens += msg.usage.cache_read_input_tokens;
    }
  }

  return total;
}

/**
 * 从消息中自动提取时间线（Claw Code 风格：不依赖 LLM）
 */
export function extractTimelineFromMessages(
  messages: Array<{ role: string; content?: string } | ConversationMessage>
): string {
  const recentMessages = messages.slice(-10);

  const timeline = recentMessages
    .filter(m => {
      const text = 'blocks' in m
        ? extractMessageText(m as ConversationMessage)
        : (m as any).content || '';
      return text.trim().length > 5;
    })
    .map(m => {
      const text = 'blocks' in m
        ? extractMessageText(m as ConversationMessage)
        : (m as any).content || '';
      const content = text.trim().substring(0, 60);
      const role = m.role;
      return `  - ${role}: ${content}${text.length > 60 ? '...' : ''}`;
    });

  return timeline.join('\n');
}

/**
 * 从 LLM 响应中提取摘要内容
 */
function extractSummaryContent(response: string): string {
  const match = response.match(/<summary>([\s\S]*?)<\/summary>/);
  if (match) {
    return match[1].trim();
  }
  return response.trim();
}

/**
 * 验证摘要是否包含关键结构
 */
export function validateSummary(summary: string): boolean {
  const requiredFields = ['Scope:', 'Pending work:', 'Key files:'];
  return requiredFields.every(field => summary.includes(field));
}

/**
 * 提取摘要中的关键点（用于合并）
 */
export function extractSummaryHighlights(summary: string): string[] {
  const match = summary.match(/<summary>([\s\S]*?)<\/summary>/);
  const content = match ? match[1] : summary;
  const lines = content.split('\n')
    .map(l => l.trim())
    .filter(l => l && !l.startsWith('- Scope:') && !l.startsWith('- Key timeline:') && !l.startsWith('<summary>') && !l.startsWith('</summary>'));
  return lines.slice(0, 5);
}

/**
 * 提取时间线（用于合并）
 */
export function extractTimeline(summary: string): string[] {
  const match = summary.match(/- Key timeline:\s*([\s\S]*?)(?:\n\n|$)/);
  if (!match) return [];
  return match[1]
    .split('\n')
    .map(l => l.trim())
    .filter(l => l && l.startsWith('-'))
    .slice(0, 5);
}

/**
 * 合并旧摘要和新摘要（防止递归压缩退化）
 */
export function mergeCompactedSummaries(existingSummary: string | undefined, newSummary: string): string {
  if (!existingSummary) return newSummary;

  const oldHighlights = extractSummaryHighlights(existingSummary);
  const newHighlights = extractSummaryHighlights(newSummary);
  const oldTimeline = extractTimeline(existingSummary);
  const newTimeline = extractTimeline(newSummary);
  const mergedTimeline = [...oldTimeline, ...newTimeline].slice(-10);

  return `<summary>
- Previously compacted context:
${oldHighlights.map(h => `  - ${h}`).join('\n')}
- Newly compacted context:
${newHighlights.map(h => `  - ${h}`).join('\n')}
- Key timeline:
${mergedTimeline.map(t => `  - ${t.replace(/^- /, '')}`).join('\n')}
</summary>`;
}

/**
 * 生成会话摘要（Claw Code 风格：代码提取 + LLM 整理）
 */
export async function generateSummary(
  messages: Array<{ role: string; content?: string } | ConversationMessage>,
  config: CompactConfig
): Promise<string> {
  // Convert legacy messages if needed
  const normalizedMessages = messages.map(m =>
    'blocks' in m ? m as ConversationMessage : convertLegacyMessage(m as any)
  );

  const userCount = normalizedMessages.filter(m => m.role === 'user').length;
  const assistantCount = normalizedMessages.filter(m => m.role === 'assistant').length;
  const toolCount = normalizedMessages.filter(m => m.role === 'tool').length;

  // 1. 代码先提取时间线（Claw Code 核心逻辑：不依赖 LLM）
  const autoTimeline = extractTimelineFromMessages(messages);

  // 2. 检查是否有旧摘要
  let existingSummary: string | undefined;
  if (normalizedMessages.length > 0 && normalizedMessages[0].role === 'system') {
    const systemContent = extractMessageText(normalizedMessages[0]);
    const match = systemContent.match(/Summary:\n([\s\S]*?)(?:\n\nRecent messages|Continue the conversation)/);
    if (match) {
      existingSummary = match[1].trim();
    }
  }

  // 3. 提取工具使用信息
  const toolNames = new Set<string>();
  const fileCandidates = new Set<string>();

  for (const msg of normalizedMessages) {
    for (const block of msg.blocks) {
      if (block.type === 'tool_use') {
        toolNames.add(block.name);
        // Extract file paths from tool input
        const fileMatches = block.input.match(/[\/\w]+\.\w{2,4}/g);
        if (fileMatches) fileMatches.forEach(f => fileCandidates.add(f));
      }
      if (block.type === 'tool_result') {
        toolNames.add(block.tool_name);
      }
      if (block.type === 'text') {
        // Extract file paths from text
        const fileMatches = block.text.match(/[\/\w]+\.\w{2,4}/g);
        if (fileMatches) fileMatches.forEach(f => fileCandidates.add(f));
      }
    }
  }

  // 3. 构建提示词：将提取好的时间线直接填入
  const prompt = `
请严格总结以下对话历史的关键信息。必须包含以下所有字段。

消息统计：
- 总消息数：${normalizedMessages.length}
- 用户消息：${userCount}
- 助手消息：${assistantCount}
- 工具消息：${toolCount}

**已提取的时间线（直接使用，不要修改）**:
${autoTimeline}

**工具使用**:
${toolNames.size > 0 ? Array.from(toolNames).join(', ') : '无'}

**文件引用**:
${fileCandidates.size > 0 ? Array.from(fileCandidates).slice(0, 8).join(', ') : '无'}

输出格式（必须严格遵循）：
<summary>
- Scope: ${normalizedMessages.length} earlier messages compacted (user=${userCount}, assistant=${assistantCount}, tool=${toolCount}).
- Recent requests:
  - [根据最近消息推断的最近 3 个用户请求]
- Pending work:
  - [根据最近消息推断的待办事项]
- Key files:
  - [根据工具使用推断的文件路径]
- Tools used:
  - [使用的工具名称]
- Key timeline:
${autoTimeline}
</summary>
`.trim();

  const response = await callLLM({
    model: config.model,
    messages: [{ role: 'user', content: prompt }],
    max_tokens: 500,
    temperature: 0.1
  });

  const rawSummary = extractSummaryContent(response.content);

  // 4. 验证摘要结构
  if (!validateSummary(rawSummary)) {
    console.warn('[LLM] Generated summary missing required fields, using fallback with auto-timeline.');
    return `<summary>
- Scope: ${normalizedMessages.length} messages compacted.
- Recent requests: [Inferred]
- Pending work: [Continue current task]
- Key files: ${fileCandidates.size > 0 ? Array.from(fileCandidates).slice(0, 5).join(', ') : '[See tool usage]'}
- Tools used: ${toolNames.size > 0 ? Array.from(toolNames).join(', ') : '[See tool usage]'}
- Key timeline:
${autoTimeline}
</summary>`;
  }

  // 5. 强制确保时间线存在（双重保险）
  const finalSummary = rawSummary.replace(
    /- Key timeline:([\s\S]*?)(?:\n\n|$)/,
    `- Key timeline:\n${autoTimeline}`
  );

  // 6. 如果存在旧摘要，合并
  if (existingSummary) {
    return mergeCompactedSummaries(existingSummary, finalSummary);
  }

  return finalSummary;
}

/**
 * 生成续写指令
 */
export function getContinuationPrompt(summary: string, preserveRecent: boolean): string {
  let prompt = 'This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion.\n\n';
  prompt += `Summary:\n${summary}\n\n`;
  if (preserveRecent) {
    prompt += 'Recent messages are preserved verbatim.\n\n';
  }
  prompt += 'Continue the conversation from where it left off without asking further questions. Resume directly — do not acknowledge the summary, do not recap, and do not preface with continuation text.';
  return prompt;
}

/**
 * 检查是否需要压缩
 */
export function shouldCompact(messages: Array<{ content?: string }>, config: CompactConfig): boolean {
  const totalTokens = estimateTokenCount(messages);
  return totalTokens > (config.max_tokens * 0.9);
}

/**
 * 压缩会话
 */
export async function compactSession(
  messages: Array<{ role: string; content?: string } | ConversationMessage>,
  config: CompactConfig
): Promise<CompactionResult> {
  const totalTokens = estimateTokenCount(messages);

  if (totalTokens <= config.max_tokens * 0.9) {
    return {
      summary: '',
      formattedSummary: '',
      removedCount: 0,
      savedTokens: 0,
      originalTokens: totalTokens,
      compactedTokens: totalTokens
    };
  }

  try {
    const keepCount = config.preserve_recent;
    const oldMessages = messages.slice(0, -keepCount);
    const recentMessages = messages.slice(-keepCount);

    const summary = await generateSummary(oldMessages, config);
    const formattedSummary = `Summary:\n${summary}`;

    const oldTokens = estimateTokenCount(oldMessages);
    const summaryTokens = Math.ceil(summary.length / 4);
    const savedTokens = oldTokens - summaryTokens;

    // Calculate compacted session tokens
    const compactedTokens = summaryTokens + estimateTokenCount(recentMessages);

    return {
      summary,
      formattedSummary,
      removedCount: oldMessages.length,
      savedTokens,
      originalTokens: totalTokens,
      compactedTokens
    };
  } catch (error) {
    console.error('[Compact] Compression failed, returning original session:', error);
    return {
      summary: '',
      formattedSummary: '',
      removedCount: 0,
      savedTokens: 0,
      originalTokens: totalTokens,
      compactedTokens: totalTokens
    };
  }
}
