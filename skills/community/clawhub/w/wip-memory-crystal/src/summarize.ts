// memory-crystal/summarize.ts — MD session summary generation.
// Two modes: LLM (calls gpt-4o-mini or configured provider) and simple (no API call).
// Controlled by CRYSTAL_SUMMARY_MODE env var.

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join, basename } from 'node:path';
import https from 'node:https';
import http from 'node:http';

// ── Types ──

export interface SessionSummary {
  title: string;
  slug: string;
  summary: string;
  topics: string[];
  messageCount: number;
  date: string;
}

export interface SummaryMessage {
  role: string;
  text: string;
  timestamp: string;
  sessionId: string;
}

// ── Config ──

const SUMMARY_MODE = process.env.CRYSTAL_SUMMARY_MODE || 'simple';
const SUMMARY_PROVIDER = process.env.CRYSTAL_SUMMARY_PROVIDER || 'openai';
const SUMMARY_MODEL = process.env.CRYSTAL_SUMMARY_MODEL || 'gpt-4o-mini';

// ── Simple mode: no API call ──

function generateSimpleSummary(messages: SummaryMessage[]): SessionSummary {
  const firstUser = messages.find(m => m.role === 'user');
  const title = firstUser
    ? firstUser.text.slice(0, 80).replace(/\n/g, ' ').trim()
    : 'Untitled Session';

  const slug = title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 50);

  // Build preview from first 10 messages
  const preview = messages.slice(0, 10).map(m => {
    const roleLabel = m.role === 'user' ? 'User' : 'Assistant';
    const snippet = m.text.slice(0, 200).replace(/\n/g, ' ').trim();
    return `**${roleLabel}:** ${snippet}${m.text.length > 200 ? '...' : ''}`;
  }).join('\n\n');

  const date = messages[0]?.timestamp?.slice(0, 10) || new Date().toISOString().slice(0, 10);

  return {
    title,
    slug,
    summary: preview,
    topics: [],
    messageCount: messages.length,
    date,
  };
}

// ── LLM mode: call API for summary ──

async function generateLlmSummary(messages: SummaryMessage[]): Promise<SessionSummary> {
  // Condense transcript for the LLM (keep it under ~4000 tokens)
  const condensed = messages.slice(0, 30).map(m => {
    const roleLabel = m.role === 'user' ? 'User' : 'Assistant';
    const text = m.text.slice(0, 500);
    return `${roleLabel}: ${text}`;
  }).join('\n\n');

  const prompt = `Summarize this conversation. Return JSON only, no markdown fences.

Format:
{"title": "short title", "slug": "url-safe-slug", "summary": "2-4 sentences", "topics": ["topic1", "topic2"]}

Conversation:
${condensed}`;

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    // Fall back to simple mode if no API key
    return generateSimpleSummary(messages);
  }

  try {
    const body = JSON.stringify({
      model: SUMMARY_MODEL,
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3,
      max_tokens: 300,
    });

    const result = await httpPost('https://api.openai.com/v1/chat/completions', body, {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    });

    const parsed = JSON.parse(result);
    const content = parsed.choices?.[0]?.message?.content || '';

    // Parse JSON from response (strip markdown fences if present)
    const jsonStr = content.replace(/```json?\n?/g, '').replace(/```/g, '').trim();
    const data = JSON.parse(jsonStr);

    const date = messages[0]?.timestamp?.slice(0, 10) || new Date().toISOString().slice(0, 10);

    return {
      title: data.title || 'Untitled',
      slug: (data.slug || 'untitled').slice(0, 50),
      summary: data.summary || '',
      topics: data.topics || [],
      messageCount: messages.length,
      date,
    };
  } catch {
    // LLM failed, fall back to simple
    return generateSimpleSummary(messages);
  }
}

// ── HTTP helper ──

function httpPost(url: string, body: string, headers: Record<string, string>): Promise<string> {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const client = parsed.protocol === 'https:' ? https : http;

    const req = client.request({
      hostname: parsed.hostname,
      port: parsed.port,
      path: parsed.pathname + parsed.search,
      method: 'POST',
      headers: { ...headers, 'Content-Length': Buffer.byteLength(body) },
      timeout: 30000,
    }, (res) => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode && res.statusCode >= 200 && res.statusCode < 300) {
          resolve(data);
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data.slice(0, 200)}`));
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
    req.write(body);
    req.end();
  });
}

// ── Public API ──

export async function generateSessionSummary(messages: SummaryMessage[]): Promise<SessionSummary> {
  if (SUMMARY_MODE === 'llm') {
    return generateLlmSummary(messages);
  }
  return generateSimpleSummary(messages);
}

export function formatSummaryMarkdown(summary: SessionSummary, sessionId: string): string {
  const lines: string[] = [];
  lines.push(`# ${summary.title}`);
  lines.push('');
  lines.push(`**Session:** ${sessionId}  **Date:** ${summary.date}  **Messages:** ${summary.messageCount}`);
  lines.push('');
  lines.push('## Summary');
  lines.push('');
  lines.push(summary.summary);

  if (summary.topics.length > 0) {
    lines.push('');
    lines.push('## Key Topics');
    lines.push('');
    for (const topic of summary.topics) {
      lines.push(`- ${topic}`);
    }
  }

  lines.push('');
  return lines.join('\n');
}

export function writeSummaryFile(
  sessionsDir: string,
  summary: SessionSummary,
  agentId: string,
  sessionId: string,
): string {
  if (!existsSync(sessionsDir)) mkdirSync(sessionsDir, { recursive: true });

  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10);
  const timeStr = now.toISOString().slice(11, 19).replace(/:/g, '-');
  const filename = `${dateStr}--${timeStr}--${agentId}--${summary.slug}.md`;
  const filepath = join(sessionsDir, filename);

  const content = formatSummaryMarkdown(summary, sessionId);
  writeFileSync(filepath, content);

  return filepath;
}
