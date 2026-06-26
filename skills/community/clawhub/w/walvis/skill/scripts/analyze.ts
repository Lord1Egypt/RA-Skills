#!/usr/bin/env node
/**
 * WALVIS analyze script
 * Analyzes content (URL/text/image) using an OpenAI-compatible LLM API
 * Usage: node analyze.js <content> [--type link|text|image]
 *
 * Reads config from ~/.walvis/manifest.json
 * Outputs JSON: { title, summary, tags, type, content_snippet }
 */

import { readManifest } from './storage.js';
import type { AnalysisResult, ItemType } from './types.js';

const SYSTEM_PROMPT = `You are WALVIS, an AI bookmark assistant. Analyze the given content and return a JSON object with exactly these fields:
{
  "title": "concise title (max 80 chars)",
  "summary": "2-3 sentence summary of the content",
  "tags": ["tag1", "tag2", "tag3"],
  "type": "link" | "text" | "image" | "note",
  "content_snippet": "most important excerpt (max 200 chars)"
}

Rules:
- tags should be lowercase, 1-3 words each, max 5 tags
- type should reflect the primary content type
- summary should be informative and concise
- Respond ONLY with the JSON object, no markdown fences`;

async function fetchUrlContent(url: string): Promise<string> {
  try {
    const res = await fetch(url, {
      headers: { 'User-Agent': 'Mozilla/5.0 (compatible; WALVIS/0.1)' },
      signal: AbortSignal.timeout(10000),
    });
    const html = await res.text();
    // Extract text content from HTML (naive but effective)
    const text = html
      .replace(/<script[\s\S]*?<\/script>/gi, '')
      .replace(/<style[\s\S]*?<\/style>/gi, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/\s+/g, ' ')
      .trim()
      .slice(0, 3000);
    // Try to get title
    const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
    const title = titleMatch ? titleMatch[1].trim() : '';
    return title ? `Title: ${title}\n\n${text}` : text;
  } catch {
    return `URL: ${url} (could not fetch content)`;
  }
}

function detectType(input: string): ItemType {
  const urlRegex = /^https?:\/\//i;
  const imageRegex = /\.(jpg|jpeg|png|gif|webp|svg)(\?.*)?$/i;
  if (urlRegex.test(input)) {
    if (imageRegex.test(input)) return 'image';
    return 'link';
  }
  return 'text';
}

export async function analyzeContent(input: string): Promise<AnalysisResult> {
  const manifest = readManifest();
  const detectedType = detectType(input);

  let contentToAnalyze = input;
  if (detectedType === 'link') {
    const fetched = await fetchUrlContent(input);
    contentToAnalyze = `URL: ${input}\n\n${fetched}`;
  }

  const response = await fetch(`${manifest.llmEndpoint}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${process.env.WALVIS_LLM_API_KEY ?? ''}`,
    },
    body: JSON.stringify({
      model: manifest.llmModel,
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: `Analyze this content:\n\n${contentToAnalyze}` },
      ],
      temperature: 0.3,
      max_tokens: 500,
    }),
  });

  if (!response.ok) {
    throw new Error(`LLM API error: ${response.status} ${await response.text()}`);
  }

  const data = await response.json() as { choices: Array<{ message: { content: string } }> };
  const raw = data.choices[0].message.content.trim();

  try {
    const result = JSON.parse(raw) as AnalysisResult;
    // Ensure type matches detected type if not set
    if (!result.type) result.type = detectedType;
    return result;
  } catch {
    // Fallback if JSON parse fails
    return {
      title: input.slice(0, 80),
      summary: 'Content saved. (Analysis failed to parse.)',
      tags: ['uncategorized'],
      type: detectedType,
      content_snippet: input.slice(0, 200),
    };
  }
}

// CLI entry point
if (process.argv[1].endsWith('analyze.js') || process.argv[1].endsWith('analyze.ts')) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Usage: analyze <content>');
    process.exit(1);
  }
  try {
    const result = await analyzeContent(input);
    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error('Error:', (err as Error).message);
    process.exit(1);
  }
}
