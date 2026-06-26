/**
 * Soul Memory Plugin for OpenClaw
 * 
 * Automatically injects Soul Memory search results before each response
 * using the before_prompt_build Hook. v3.6.1 adds typed memory focus injection, distilled summaries, and audit logging.
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// Soul Memory configuration
interface SoulMemoryConfig {
  enabled: boolean;
  topK: number;
  minScore: number;
}

// Search result from Soul Memory
interface MemoryResult {
  path: string;
  content: string;
  score: number;
  priority?: string;
}

interface SearchProfile {
  topK: number;
  minScore: number;
}

/**
 * Search Soul Memory using Python backend
 */
async function searchMemories(query: string, config: SoulMemoryConfig): Promise<MemoryResult[]> {
  try {
    const effective = resolveSearchProfile(query, config);
    const escapedQuery = query.replace(/"/g, '\\"');
    const { stdout } = await execAsync(
      `python3 /root/.openclaw/workspace/soul-memory/cli.py search "${escapedQuery}" --top_k ${effective.topK} --min_score ${effective.minScore}`,
      {
        timeout: 5000,
        cwd: '/root/.openclaw/workspace/soul-memory'
      }
    );

    const trimmed = (stdout || '').trim();
    if (!trimmed) return [];

    try {
      const results = JSON.parse(trimmed);
      return Array.isArray(results) ? results : [];
    } catch {
      const match = trimmed.match(/(\[[\s\S]*\]|\{[\s\S]*\})/);
      if (match) {
        const recovered = JSON.parse(match[1]);
        return Array.isArray(recovered) ? recovered : [];
      }
      throw new Error(`Non-JSON search output: ${trimmed.substring(0, 200)}`);
    }
  } catch (error) {
    console.error('[Soul Memory] Search failed:', error instanceof Error ? error.message : String(error));
    return [];
  }
}



type MemoryBucket = 'User' | 'QST' | 'Config' | 'Recent' | 'Project' | 'General';

function classifyQuery(query: string): MemoryBucket {
  const q = (query || '').toLowerCase();
  if (/(記住|偏好|喜歡|身份|user|preference|like|favorite|timezone|name)/.test(q)) return 'User';
  if (/(qst|phi|varphi|fsca|dark matter|dark energy|physics|理論|物理|計算|公式|audit|審計)/.test(q)) return 'QST';
  if (/(config|設定|配置|token|api|gateway|port|model|provider|telegram|github|pwd|password)/.test(q)) return 'Config';
  if (/(上次|之前|剛才|recent|latest|last|今日|昨天|today|yesterday|剛剛)/.test(q)) return 'Recent';
  if (/(project|專案|repo|repository|deploy|issue|pr|pull request|workspace|build)/.test(q)) return 'Project';
  return 'General';
}

function resolveSearchProfile(query: string, config: SoulMemoryConfig): SearchProfile {
  const bucket = classifyQuery(query);
  if (bucket === 'User') return { topK: Math.min(config.topK, 3), minScore: 2.0 };
  if (bucket === 'Recent') return { topK: Math.min(config.topK, 3), minScore: 1.8 };
  if (bucket === 'QST') return { topK: Math.max(Math.min(config.topK, 5), 4), minScore: 2.5 };
  if (bucket === 'Config') return { topK: Math.min(Math.max(config.topK, 4), 6), minScore: 2.2 };
  if (bucket === 'Project') return { topK: Math.min(Math.max(config.topK, 4), 5), minScore: 2.0 };
  return { topK: Math.min(config.topK, 2), minScore: 3.0 };
}

function cleanMemorySnippet(text: string): string {
  let cleaned = text || '';
  cleaned = cleaned.replace(/\[[CIN]\]\s*\d{1,2}:\d{2}\s*Heartbeat 自動提取\s*\|\s*來源\s*：?\s*Session 對話回顧\s*\|\s*時區\s*：?\s*[^|]+\|?/gi, '');
  cleaned = cleaned.replace(/Conversation info \(untrusted metadata\):[\s\S]*$/gi, '');
  cleaned = cleaned.replace(/Sender \(untrusted metadata\):[\s\S]*$/gi, '');
  cleaned = cleaned.replace(/Successfully replaced text in\s+[^|]+\.?/gi, '');
  cleaned = cleaned.replace(/===\s*[^|]+\s*===/g, '');
  cleaned = cleaned.replace(/\b(total\s+\d+|drwxr[-\w\s]+|command exited with code \d+)\b/gi, '');
  cleaned = cleaned.replace(/```[\s\S]*?```/g, '');
  cleaned = cleaned.replace(/\|\s*\|+/g, '|');
  return cleaned;
}

function normalizeText(text: string): string {
  return cleanMemorySnippet(text)
    .replace(/[`*_#>-]/g, ' ')
    .replace(/\s*\|\s*/g, ' · ')
    .replace(/\s+/g, ' ')
    .trim();
}

function summarizeText(text: string, maxLen: number = 160): string {
  const normalized = normalizeText(text);
  if (normalized.length <= maxLen) return normalized;
  return normalized.slice(0, maxLen - 1).trimEnd() + '…';
}

function isNoisyMemory(result: MemoryResult): boolean {
  const hay = `${result.path || ''} ${result.content || ''}`.toLowerCase();
  return /(heartbeat 自動提取|conversation info \(untrusted metadata\)|sender \(untrusted metadata\)|successfully replaced text in|plugin registered|hook registered|loaded index with|=== |drwxr|command exited with code|exec completed)/.test(hay);
}

function classifyMemory(result: MemoryResult): MemoryBucket {
  const hay = `${result.path || ''} ${cleanMemorySnippet(result.content || '')}`.toLowerCase();

  if (isNoisyMemory(result)) {
    return 'General';
  }
  if (/(user\.md|identity|preferred name|what to call|timezone|秦王|陛下|偏好|喜歡|user)/.test(hay)) {
    return 'User';
  }
  if (/(qst|varphi|\bphi\b|fractal|spectral|dirac|fsca|torsion|dark matter|e8|theorem|appendix|cosmology)/.test(hay)) {
    return 'QST';
  }
  if (/(config|token|api key|credential|password|gateway|telegram|bot|provider|model|port|dashboard|gmail|openclaw)/.test(hay)) {
    return 'Config';
  }
  if (/(memory\/20\d\d-\d\d-\d\d\.md|today|yesterday|recent|剛才|今天|昨日|latest|last)/.test(hay)) {
    return 'Recent';
  }
  if (/(project|repo|repository|deploy|deployment|issue|pr |pull request|archive|workspace|build)/.test(hay)) {
    return 'Project';
  }
  return 'General';
}

function groupMemories(results: MemoryResult[]): Record<MemoryBucket, MemoryResult[]> {
  const grouped: Record<MemoryBucket, MemoryResult[]> = {
    User: [], QST: [], Config: [], Recent: [], Project: [], General: []
  };

  for (const result of results.filter(r => !isNoisyMemory(r))) {
    grouped[classifyMemory(result)].push(result);
  }

  return grouped;
}

function formatSource(path?: string): string {
  if (!path) return '';
  const short = path.split('/').slice(-2).join('/');
  return short || path;
}

function buildMemoryContext(results: MemoryResult[], query: string): string {
  const filteredResults = results.filter(r => !isNoisyMemory(r));
  if (filteredResults.length === 0) {
    return '';
  }

  const grouped = groupMemories(filteredResults);
  const bucketOrder: MemoryBucket[] = ['User', 'QST', 'Config', 'Recent', 'Project', 'General'];
  const focus = classifyQuery(query);
  const maxChars = focus === 'General' ? 420 : 720;
  const maxPerBucket = focus === 'General' ? 1 : 2;
  let context = '## Memory Focus\n';
  let usedChars = context.length;

  for (const bucket of bucketOrder) {
    const items = grouped[bucket];
    if (!items || items.length === 0) continue;

    context += `- ${bucket}:\n`;
    usedChars += (`- ${bucket}:\n`).length;

    const ranked = [...items]
      .sort((a, b) => (b.score || 0) - (a.score || 0))
      .slice(0, maxPerBucket);

    for (const item of ranked) {
      const summary = summarizeText(item.content, focus === 'General' ? 110 : 150);
      const source = formatSource(item.path);
      const sourcePart = source ? ` (${source})` : '';
      const line = `  • ${summary}${sourcePart}\n`;
      if (usedChars + line.length > maxChars) {
        return context.trimEnd() + '\n';
      }
      context += line;
      usedChars += line.length;
    }
  }

  return context.trimEnd() + '\n';
}

function buildAuditSummary(results: MemoryResult[]): string {
  const grouped = groupMemories(results);
  const parts: string[] = [];
  for (const [bucket, items] of Object.entries(grouped)) {
    if (items.length > 0) parts.push(`${bucket}:${items.length}`);
  }
  const topSources = results
    .slice(0, 3)
    .map(r => formatSource(r.path))
    .filter(Boolean)
    .join(', ');
  return `buckets=[${parts.join(' | ')}] topSources=[${topSources}]`;
}

/**
 * Get the last user message from the conversation
 */
function getLastUserMessage(messages: any[]): string {
  if (!messages || messages.length === 0) {
    return '';
  }

  // Find the last message from user role
  for (let i = messages.length - 1; i >= 0; i--) {
    const msg = messages[i];
    if (msg.role === 'user' && msg.content) {
      // Handle different content formats
      if (Array.isArray(msg.content)) {
        return msg.content
          .filter((item: any) => item.type === 'text')
          .map((item: any) => item.text)
          .join(' ');
      } else if (typeof msg.content === 'string') {
        return msg.content;
      }
    }
  }

  return '';
}

/**
 * Extract query from user message, removing metadata blocks and old memory markers
 */
function extractQuery(rawMessage: string): string {
  if (!rawMessage) return '';

  let cleaned = rawMessage.trim();

  // CRITICAL 1: Remove old memory marked with SoulM delimiters
  // Pattern: SoulM"...content..."
  cleaned = cleaned.replace(/SoulM".*?"/gs, '');

  // CRITICAL 2: Remove legacy memory context explicitly
  // Pattern: ## 🧠 Memory Context... (all content until next major section)
  cleaned = cleaned.replace(/## 🧠 Memory Context[\s\S]*?(?=\n\n\s*\n|$|## |---)/gm, '');
  cleaned = cleaned.replace(/🧠 Memory Context[\s\S]*?(?=\n\n\s*\n|$|## |---)/gm, '');

  // CRITICAL 3: Remove numbered memory entries (e.g., "1. 🔥 [🔴 Critical]...")
  cleaned = cleaned.replace(/^\s*\d+\.\s+🔥.*$/gm, '');
  cleaned = cleaned.replace(/^\s*\d+\.\s+⭐.*$/gm, '');

  // Remove "Conversation info" metadata blocks
  cleaned = cleaned.replace(/Conversation info \(untrusted metadata\):[\s\S]*?\n\n/g, '');
  cleaned = cleaned.replace(/Sender \(untrusted metadata\):[\s\S]*?\n\n/g, '');

  // Remove "System:" messages
  cleaned = cleaned.replace(/^System: \[[\s\S]*?\]$/gm, '');

  // Remove Markdown code blocks (```json ... ```, ``` ... ```)
  cleaned = cleaned.replace(/```[\s\S]*?```/g, '');

  // Remove HTML/XML-like blocks
  cleaned = cleaned.replace(/<[\s\S]*?>/g, '');

  // Remove empty lines and clean up
  cleaned = cleaned.replace(/\n\s*\n/g, '\n').trim();

  // If after cleaning we have nothing, use a longer prefix of the original message
  if (cleaned.length < 5 && rawMessage.length > 10) {
    // Try to extract the first meaningful sentence
    const firstSentenceMatch = rawMessage.match(/^[^。!！?？\n]+[。!！?？]?/);
    if (firstSentenceMatch) {
      cleaned = firstSentenceMatch[0].trim();
    } else {
      // Fallback to first 200 characters
      cleaned = rawMessage.substring(0, 200).trim();
    }
  }

  // Limit to 200 characters
  return cleaned.substring(0, 200);
}

/**
 * Check if query should skip memory search (greetings, simple commands, etc.)
 * v3.3.4 optimization: Reduce noise from irrelevant memory injections
 */
function shouldSkipQuery(query: string): boolean {
  if (!query || query.trim().length === 0) return true;
  
  const normalized = query.toLowerCase().trim();
  
  // Greetings (Chinese & English)
  const greetings = [
    '早', '早上好', '早安', '早啊', 'good morning',
    '好', '你好', '您好', 'hello', 'hi', 'hey',
    '再见', '拜拜', 'bye', 'goodbye', 'see you',
    '谢谢', '感谢', 'thank', 'thanks', 'thx',
    '好的', '好滴', 'ok', 'okay', '收到', '嗯', '嗯嗯'
  ];
  
  // Simple commands (1-2 characters, no context needed)
  const simpleCommands = [
    '？', '？', '?', '！', '!',
    '查', '看', '停', '重启', '重启服务',
    '检查', '测试', '运行', '执行',
    '继续', '继续做', '好的', '没问题'
  ];
  
  // Check for exact matches
  if (greetings.includes(normalized) || simpleCommands.includes(normalized)) {
    return true;
  }
  
  // Check for very short queries (< 3 characters) without technical keywords
  if (normalized.length < 3 && !/[0-9a-zA-Z\u4e00-\u9fa5]{3,}/.test(normalized)) {
    return true;
  }
  
  // Check for emoji-only messages
  if (/^[\p{Emoji}]+$/u.test(normalized)) {
    return true;
  }
  
  return false;
}

/**
 * Clean old memory markers from messages array
 * This prevents accumulation of memory context in conversation history
 */
function cleanOldMemoryFromMessages(messages: any[]): any[] {
  if (!messages || messages.length === 0) {
    return messages;
  }

  let cleanedMessages = [];
  let hadOldMemory = false;

  messages.forEach(msg => {
    let cleanedMsg = { ...msg };

    // Clean user messages
    if (msg.role === 'user') {
      let content = '';

      if (typeof msg.content === 'string') {
        content = msg.content;
      } else if (Array.isArray(msg.content)) {
        content = msg.content
          .filter((item: any) => item.type === 'text')
          .map((item: any) => item.text)
          .join(' ');
      }

      // Remove old memory markers
      const originalContent = content;
      content = content.replace(/SoulM".*?"/gs, '');

      // Check if we removed anything
      if (originalContent !== content) {
        hadOldMemory = true;

        // Update message content
        if (typeof msg.content === 'string') {
          cleanedMsg.content = content;
        } else if (Array.isArray(msg.content)) {
          cleanedMsg.content = msg.content.map((item: any) => {
            if (item.type === 'text') {
              return { type: 'text', text: content };
            }
            return item;
          });
        }
      }
    }

    // Clean assistant messages (remove SoulM markers)
    if (msg.role === 'assistant' && typeof msg.content === 'string') {
      const originalContent = msg.content;
      const cleanedContent = msg.content.replace(/SoulM".*?"/gs, '');

      if (originalContent !== cleanedContent) {
        hadOldMemory = true;
        cleanedMsg.content = cleanedContent;
      }
    }

    cleanedMessages.push(cleanedMsg);
  });

  if (hadOldMemory) {
    console.log('[Soul Memory] ✓ Cleaned old memory markers from messages');
  }

  return cleanedMessages;
}

/**
 * Plugin entry point
 */
export default function register(api: any) {
  const logger = api.logger || console;

  logger.info('[Soul Memory] Plugin registered via api.register()');

  // Register before_prompt_build Hook using api.on() (Plugin Hook API)
  api.on('before_prompt_build', async (event: any, ctx: any) => {
    const config: SoulMemoryConfig = {
      enabled: true,
      topK: 5,
      minScore: 3.0,  // v3.3.4: Increased from 0.0 to reduce noise
      ...api.config.plugins?.entries?.['soul-memory']?.config
    };

    // IMPORTANT: Log that hook was called
    logger.info('[Soul Memory] ✓ BEFORE_PROMPT_BUILD HOOK CALLED via api.on()');
    logger.debug(`[Soul Memory] Config: enabled=${config.enabled}, topK=${config.topK}, minScore=${config.minScore}`);
    logger.debug(`[Soul Memory] Event: prompt=${event.prompt?.substring(0, 50)}..., messages=${event.messages?.length || 0}`);
    logger.debug(`[Soul Memory] Context: agentId=${ctx.agentId}, sessionKey=${ctx.sessionKey}`);

    // Check if enabled
    if (!config.enabled) {
      logger.info('[Soul Memory] Plugin disabled, skipping');
      return {};
    }

    // v3.6.0: Prefer the actual last user message from messages.
    // Prompt text may end with system / metadata lines and is less reliable.
    const messages = event.messages || [];
    const cleanedMessages = cleanOldMemoryFromMessages(messages);
    let lastUserMessage = getLastUserMessage(cleanedMessages);
    let querySource = 'messages';

    // Fallback: derive from prompt only when user message is unavailable
    if (!lastUserMessage || lastUserMessage.length === 0) {
      querySource = 'prompt_fallback';
      logger.debug('[Soul Memory] No user message found, falling back to prompt');
      const prompt = event.prompt || '';
      let userQuery = prompt.trim();
      const lastNewlineIndex = userQuery.lastIndexOf('\n');
      if (lastNewlineIndex >= 0) {
        userQuery = userQuery.substring(lastNewlineIndex + 1).trim();
      }
      lastUserMessage = userQuery;
    }

    logger.info(`[Soul Memory] Query source: ${querySource}`);

    // v3.6.0 optimization: Skip search for greetings and simple commands
    if (shouldSkipQuery(lastUserMessage)) {
      logger.debug(`[Soul Memory] Skipping search for simple query: "${lastUserMessage.substring(0, 50)}"`);
      return {};
    }

    logger.debug(`[Soul Memory] User query length: ${lastUserMessage.length}`);

    // Skip if no user query
    if (!lastUserMessage || lastUserMessage.trim().length === 0) {
      logger.debug('[Soul Memory] No user query found, skipping');
      return {};
    }

    // Extract query with metadata removal
    const query = extractQuery(lastUserMessage);

    // Skip if query is too short
    if (query.length < 5) {
      logger.debug(`[Soul Memory] Query too short (${query.length} chars): "${query}", skipping`);
      return {};
    }

    logger.info(`[Soul Memory] Searching for: "${query}"`);

    // Search memories
    const results = await searchMemories(query, config);

    logger.info(`[Soul Memory] Found ${results.length} results`);

    if (results.length === 0) {
      logger.info('[Soul Memory] No memories found');
      return {};
    }

    const auditSummary = buildAuditSummary(results);
    logger.info(`[Soul Memory] Audit: ${auditSummary}`);

    const memoryContext = buildMemoryContext(results, lastUserMessage);
    logger.info(`[Soul Memory] ✓ Injected ${results.length} distilled memories into prependContext (${memoryContext.length} chars)`);

    return {
      prependContext: memoryContext
    };
  });

  logger.info('[Soul Memory] Hook registered via api.on(): before_prompt_build');
}
