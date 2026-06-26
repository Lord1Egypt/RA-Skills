import { readFile, readdir } from 'fs/promises';
import { join } from 'path';

/**
 * session:start hook
 * Loads memory context + last raw interactions into the new session.
 *
 * Strategy:
 * 1. Load the most recent daily memory file (AI summaries)
 * 2. Also load today's file if different from most recent (catches intraday)
 * 3. Extract and inject the last N raw interactions verbatim so the AI can
 *    resume mid-conversation without loss of exact phrasing/decisions.
 */

const MAX_SUMMARY_CHARS = 6000;   // cap on AI summary context
const MAX_RECENT_MESSAGES = 10;   // last N user/assistant turns to preserve verbatim
const RECENT_MESSAGES_MARKER = '<!-- recent_messages_block -->';

export default async function ({ context, log }) {
  const workspace = context.workspace || process.cwd();
  const memoryDir = join(workspace, 'memory');

  try {
    const allFiles = await readdir(memoryDir)
      .then(files => files.filter(f => /^\d{4}-\d{2}-\d{2}\.md$/.test(f)))
      .catch(() => []);

    if (allFiles.length === 0) {
      log.debug('No memory files found to load');
      return;
    }

    // Sort descending — most recent first
    allFiles.sort((a, b) => b.localeCompare(a));

    const today = new Date().toISOString().split('T')[0] + '.md';
    const filesToLoad = allFiles[0] === today
      ? [allFiles[0], allFiles[1]].filter(Boolean)  // today + yesterday
      : [allFiles[0]];                               // just most recent

    // Combine summaries from loaded files
    let summaryBlocks = [];
    let recentMessagesBlock = null;

    for (const file of filesToLoad) {
      const content = await readFile(join(memoryDir, file), 'utf8').catch(() => null);
      if (!content) continue;

      // Extract the recent_messages block from the first (most recent) file only
      if (!recentMessagesBlock && content.includes(RECENT_MESSAGES_MARKER)) {
        const markerIdx = content.indexOf(RECENT_MESSAGES_MARKER);
        const blockStart = content.indexOf('\n', markerIdx) + 1;
        recentMessagesBlock = content.substring(blockStart).trim();

        // Summary is everything before the marker
        const summaryPart = content.substring(0, markerIdx).trim();
        if (summaryPart) summaryBlocks.push(`[${file}]\n${summaryPart}`);
      } else {
        summaryBlocks.push(`[${file}]\n${content.trim()}`);
      }
    }

    const combinedSummary = summaryBlocks.join('\n\n---\n\n').substring(0, MAX_SUMMARY_CHARS);

    if (!context.sessionEntry || !Array.isArray(context.sessionEntry.messages)) return;

    const msgs = context.sessionEntry.messages;

    // Inject AI summary context
    if (combinedSummary) {
      msgs.unshift({
        role: 'system',
        content: `[Memory context — AI summaries]\n\n${combinedSummary}`,
        metadata: { source: 'memory-loader', timestamp: new Date().toISOString() }
      });
      log.info(`Loaded memory summary (${combinedSummary.length} chars)`);
    }

    // Inject recent raw interactions if we have them
    if (recentMessagesBlock) {
      // Parse the stored JSON interactions back into system message
      try {
        const parsed = JSON.parse(recentMessagesBlock);
        if (Array.isArray(parsed) && parsed.length > 0) {
          const recentText = parsed
            .map(m => `**${m.role === 'user' ? 'Thomas' : 'AniBot'}:** ${m.content}`)
            .join('\n\n');
          msgs.unshift({
            role: 'system',
            content: `[Last ${parsed.length} messages verbatim — resume from here]\n\n${recentText}`,
            metadata: { source: 'recent-messages-loader', timestamp: new Date().toISOString() }
          });
          log.info(`Loaded ${parsed.length} recent raw messages for continuity`);
        }
      } catch {
        // Not JSON — inject as-is (legacy plain text block)
        msgs.unshift({
          role: 'system',
          content: `[Recent conversation]\n\n${recentMessagesBlock}`,
          metadata: { source: 'recent-messages-loader', timestamp: new Date().toISOString() }
        });
      }
    }
  } catch (error) {
    log.error('Failed to load memory:', error);
  }
}
