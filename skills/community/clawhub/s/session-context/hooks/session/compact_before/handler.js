import { readFile, mkdir, writeFile } from 'fs/promises';
import { join } from 'path';

const RECENT_MESSAGES_MARKER = '<!-- recent_messages_block -->';
const MAX_RECENT_MESSAGES = 10;  // raw turns to preserve verbatim
const MAX_CONTENT_PER_MSG = 1500; // truncate very long messages when storing

/**
 * Determines whether this conversation should be summarized.
 */
function shouldSummarize(context) {
  const msgCount = context.messages?.length || 0;
  const tokenCount = context.session?.tokenCount || 0;
  const maxTokens = context.config?.maxTokens || 128000;

  return (
    msgCount >= 20 ||
    tokenCount > maxTokens * 0.6
  );
}

/**
 * Generates a concise summary of the conversation using the agent's LLM.
 */
async function summarizeConversation(messages, log) {
  try {
    const agent = global.__OPENCLAW_AGENT__;
    if (!agent || typeof agent.generateSummary !== 'function') {
      log?.warn?.('Agent.generateSummary not available, using fallback');
      const text = messages
        .map(m => `${m.role === 'user' ? 'User' : 'Assistant'}: ${String(m.content || '').substring(0, 500)}`)
        .join('\n');
      return `**Quick Summary** (${messages.length} messages, auto-fallback):\n\n${text.substring(0, 1200)}...`;
    }
    const summary = await agent.generateSummary(messages);
    return summary || '**Summary generated but empty**';
  } catch (error) {
    log?.error?.('Error generating summary:', error);
    return `**Summary failed** — ${error.message}`;
  }
}

/**
 * Extracts the last N user/assistant message turns, truncating very long content.
 */
function extractRecentMessages(messages, n) {
  const conversational = messages.filter(m => m.role === 'user' || m.role === 'assistant');
  const recent = conversational.slice(-n);
  return recent.map(m => ({
    role: m.role,
    content: typeof m.content === 'string'
      ? m.content.substring(0, MAX_CONTENT_PER_MSG)
      : String(m.content || '').substring(0, MAX_CONTENT_PER_MSG)
  }));
}

/**
 * Writes the summary + recent messages to today's daily memory file.
 *
 * File structure:
 * ─────────────────────────────────
 * ## HH:MM:SS  ← timestamp
 * <AI summary>
 *
 * ---
 *
 * ## Earlier entry...
 *
 * <!-- recent_messages_block -->
 * [JSON array of last N messages]
 * ─────────────────────────────────
 *
 * The recent_messages_block is always at the END of the file so it's easy
 * to find and replace. On next compact it gets updated in-place.
 */
async function writeMemoryFile(summary, recentMessages, workspace) {
  const memoryDir = join(workspace, 'memory');
  await mkdir(memoryDir, { recursive: true });

  const today = new Date().toISOString().split('T')[0];
  const filePath = join(memoryDir, `${today}.md`);

  let existing = '';
  try {
    existing = await readFile(filePath, 'utf8');
  } catch {
    // new file
  }

  // Strip old recent_messages block if present
  const markerIdx = existing.indexOf(RECENT_MESSAGES_MARKER);
  const summaryPart = markerIdx >= 0 ? existing.substring(0, markerIdx).trimEnd() : existing.trimEnd();

  const timestamp = new Date().toLocaleTimeString();
  const newEntry = `## ${timestamp}\n${summary}`;
  const separator = summaryPart ? '\n\n---\n\n' : '';
  const recentBlock = `\n\n${RECENT_MESSAGES_MARKER}\n${JSON.stringify(recentMessages, null, 2)}`;

  const content = newEntry + separator + summaryPart + recentBlock;
  await writeFile(filePath, content, 'utf8');
  return filePath;
}

/**
 * Main hook entry point
 */
export default async function (context) {
  const log = context.log || console;
  const workspace = context.workspace || process.cwd();

  try {
    if (!shouldSummarize(context)) {
      log.debug('session:compact:before - skipping (threshold not met)');
      return;
    }

    const messages = context.messages || [];
    log.info('session:compact:before - generating summary...');

    const [summary, recentMessages] = await Promise.all([
      summarizeConversation(messages, log),
      Promise.resolve(extractRecentMessages(messages, MAX_RECENT_MESSAGES))
    ]);

    const filePath = await writeMemoryFile(summary, recentMessages, workspace);
    log.info(`session:compact:before - summary + ${recentMessages.length} recent msgs written to ${filePath}`);
  } catch (error) {
    log.error('session:compact:before hook failed:', error);
  }
}
