import { BaseImportAdapter } from './base-adapter.js';
import fs from 'node:fs';
import os from 'node:os';
/** Maximum messages per conversation chunk for LLM extraction. */
const CHUNK_SIZE = 20;
/** Gap (in minutes) between entries that starts a new pseudo-session. */
const SESSION_GAP_MINUTES = 30;
// ── Timestamp Parsing ────────────────────────────────────────────────────────
const MONTHS = {
    Jan: 0, Feb: 1, Mar: 2, Apr: 3, May: 4, Jun: 5,
    Jul: 6, Aug: 7, Sep: 8, Oct: 9, Nov: 10, Dec: 11,
};
/**
 * Parse Gemini timestamp: "1 Apr 2026, 18:39:35 WEST" → ISO 8601.
 * Timezone is treated as UTC (all entries use the same TZ, preserving order).
 */
function parseTimestamp(raw) {
    const m = raw.match(/^(\d{1,2})\s+(\w{3})\s+(\d{4}),\s+(\d{2}):(\d{2}):(\d{2})\s+/);
    if (!m || MONTHS[m[2]] === undefined)
        return undefined;
    const d = new Date(Date.UTC(+m[3], MONTHS[m[2]], +m[1], +m[4], +m[5], +m[6]));
    return d.toISOString();
}
// ── HTML Helpers ─────────────────────────────────────────────────────────────
function decodeEntities(t) {
    return t.replace(/&#39;/g, "'").replace(/&quot;/g, '"').replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ');
}
function stripHTML(html) {
    return html.replace(/<br\s*\/?>/gi, '\n').replace(/<\/p>/gi, '\n')
        .replace(/<\/li>/gi, '\n').replace(/<\/h[1-6]>/gi, '\n')
        .replace(/<hr\s*\/?>/gi, '\n---\n').replace(/<[^>]+>/g, '')
        .replace(/\n{3,}/g, '\n\n').trim();
}
// ── Gemini Adapter ───────────────────────────────────────────────────────────
export class GeminiAdapter extends BaseImportAdapter {
    source = 'gemini';
    displayName = 'Google Gemini';
    async parse(input, onProgress) {
        const warnings = [];
        const errors = [];
        let content;
        if (input.content) {
            content = input.content;
        }
        else if (input.file_path) {
            try {
                const resolved = input.file_path.replace(/^~/, os.homedir());
                const fileStat = fs.statSync(resolved);
                const fileSizeMB = fileStat.size / (1024 * 1024);
                if (fileSizeMB > 500) {
                    errors.push(`File is too large to import: ${fileSizeMB.toFixed(1)}MB exceeds the 500MB cap. ` +
                        'Split the file into smaller chunks and import each separately.');
                    return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
                }
                const freeMem = os.freemem();
                if (freeMem < fileStat.size * 2) {
                    errors.push(`Not enough free memory: ${(freeMem / (1024 * 1024)).toFixed(0)}MB available, ` +
                        `~${Math.ceil(fileStat.size * 2 / (1024 * 1024))}MB needed (2× file size). ` +
                        'Close other applications or split the file.');
                    return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
                }
                content = fs.readFileSync(resolved, 'utf-8');
            }
            catch (e) {
                errors.push(`Failed to read file: ${e instanceof Error ? e.message : 'Unknown error'}`);
                return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
            }
        }
        else {
            errors.push('Gemini import requires either content or file_path. ' +
                'Export from Google Takeout: takeout.google.com → select Gemini Apps → export. ' +
                'Provide the "My Activity.html" file path.');
            return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
        }
        if (onProgress) {
            onProgress({ current: 0, total: 0, phase: 'parsing', message: 'Parsing Gemini HTML...' });
        }
        // Parse HTML into entries
        const entries = this.parseHTML(content);
        if (entries.length === 0) {
            warnings.push('No conversation entries found in the HTML file.');
            return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
        }
        // Group into pseudo-sessions by temporal proximity
        const sessions = this.groupSessions(entries);
        if (onProgress) {
            onProgress({
                current: 0,
                total: sessions.length,
                phase: 'parsing',
                message: `Parsed ${entries.length} entries into ${sessions.length} sessions`,
            });
        }
        // Build conversation chunks from sessions
        const chunks = [];
        let totalMessages = 0;
        for (const session of sessions) {
            const messages = [];
            for (const entry of session) {
                if (entry.userPrompt)
                    messages.push({ role: 'user', text: entry.userPrompt });
                if (entry.aiResponse)
                    messages.push({ role: 'assistant', text: entry.aiResponse });
            }
            if (messages.length === 0)
                continue;
            totalMessages += messages.length;
            const timestamp = session[0].timestampISO;
            // Sub-chunk large sessions
            for (let i = 0; i < messages.length; i += CHUNK_SIZE) {
                const batch = messages.slice(i, i + CHUNK_SIZE);
                const chunkIdx = Math.floor(i / CHUNK_SIZE) + 1;
                const totalChunks = Math.ceil(messages.length / CHUNK_SIZE);
                const title = totalChunks > 1
                    ? `Gemini session (part ${chunkIdx}/${totalChunks})`
                    : 'Gemini session';
                chunks.push({ title, messages: batch, timestamp });
            }
        }
        return {
            facts: [],
            chunks,
            totalMessages,
            warnings,
            errors,
            source_metadata: {
                format: 'gemini-takeout-html',
                total_entries: entries.length,
                sessions_count: sessions.length,
                chunks_count: chunks.length,
                total_messages: totalMessages,
                date_range: {
                    earliest: entries[0]?.timestampISO,
                    latest: entries[entries.length - 1]?.timestampISO,
                },
            },
        };
    }
    /**
     * Parse Gemini Takeout HTML into structured entries.
     *
     * Each outer-cell div contains: "Prompted USER_TEXT<br>TIMESTAMP<br>RESPONSE_HTML"
     * all within one content-cell.
     */
    parseHTML(html) {
        const entries = [];
        const cellPattern = /<div class="outer-cell[^"]*">([\s\S]*?)(?=<div class="outer-cell|$)/g;
        let match;
        while ((match = cellPattern.exec(html)) !== null) {
            const cell = match[1];
            // Only process "Prompted" entries (skip canvas, feedback)
            const promptedIdx = cell.indexOf('Prompted\u00a0');
            if (promptedIdx === -1)
                continue;
            // Extract timestamp
            const tsMatch = cell.match(/(\d{1,2}\s+\w{3}\s+\d{4},\s+\d{2}:\d{2}:\d{2}\s+\w+)/);
            if (!tsMatch)
                continue;
            const timestampISO = parseTimestamp(tsMatch[1]);
            if (!timestampISO)
                continue;
            // Split on timestamp to separate user prompt from AI response
            const afterPrompted = cell.substring(promptedIdx + 'Prompted\u00a0'.length);
            const tsPattern = /(\d{1,2}\s+\w{3}\s+\d{4},\s+\d{2}:\d{2}:\d{2}\s+\w+)/;
            const tsIdx = afterPrompted.search(tsPattern);
            let userPrompt = '';
            let aiResponse = '';
            if (tsIdx > 0) {
                userPrompt = stripHTML(decodeEntities(afterPrompted.substring(0, tsIdx))).trim();
                const tsInner = afterPrompted.match(tsPattern);
                if (tsInner) {
                    const afterTs = afterPrompted.substring(tsIdx + tsInner[0].length)
                        .replace(/^\s*<br\s*\/?>\s*/i, '');
                    const endDiv = afterTs.search(/<\/div>\s*<div class="content-cell/);
                    const rawResp = endDiv !== -1 ? afterTs.substring(0, endDiv) : afterTs;
                    aiResponse = stripHTML(decodeEntities(rawResp)).trim();
                }
            }
            if (userPrompt.length < 3 && aiResponse.length < 3)
                continue;
            entries.push({
                userPrompt,
                aiResponse,
                timestampISO,
                timestampUnix: Math.floor(new Date(timestampISO).getTime() / 1000),
            });
        }
        // Sort chronologically (HTML is newest-first)
        entries.sort((a, b) => a.timestampUnix - b.timestampUnix);
        return entries;
    }
    /**
     * Group entries into pseudo-sessions by temporal proximity.
     */
    groupSessions(entries) {
        if (entries.length === 0)
            return [];
        const sessions = [];
        let current = [entries[0]];
        for (let i = 1; i < entries.length; i++) {
            const gap = entries[i].timestampUnix - entries[i - 1].timestampUnix;
            if (gap > SESSION_GAP_MINUTES * 60) {
                sessions.push(current);
                current = [entries[i]];
            }
            else {
                current.push(entries[i]);
            }
        }
        if (current.length > 0)
            sessions.push(current);
        return sessions;
    }
}
