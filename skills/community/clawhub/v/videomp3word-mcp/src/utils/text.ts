import type { Entity } from "../schemas.js";

const STOP_WORDS = new Set([
  "the", "and", "for", "that", "with", "this", "from", "have", "will", "into", "your", "about", "they", "their",
  "there", "were", "what", "when", "where", "which", "would", "should", "could", "after", "before", "then", "than",
  "them", "been", "being", "also", "just", "more", "most", "only", "some", "such", "very", "through",
]);

export function normalizeWhitespace(value: string): string {
  return value.replace(/\r\n/g, "\n").replace(/[\t ]+/g, " ").replace(/\n{3,}/g, "\n\n").trim();
}

export function splitIntoSentences(text: string): string[] {
  return normalizeWhitespace(text)
    .split(/(?<=[.!?])\s+/)
    .map((sentence) => sentence.trim())
    .filter(Boolean);
}

export function chunkText(text: string, maxChars: number): string[] {
  const normalized = normalizeWhitespace(text);
  if (!normalized) return [];
  if (normalized.length <= maxChars) return [normalized];

  const paragraphs = normalized.split(/\n{2,}/);
  const chunks: string[] = [];
  let current = "";

  for (const paragraph of paragraphs) {
    if (!paragraph.trim()) continue;
    const candidate = current ? `${current}\n\n${paragraph}` : paragraph;
    if (candidate.length <= maxChars) {
      current = candidate;
      continue;
    }
    if (current) chunks.push(current.trim());
    if (paragraph.length <= maxChars) {
      current = paragraph;
      continue;
    }
    const sentences = splitIntoSentences(paragraph);
    let sentenceChunk = "";
    for (const sentence of sentences) {
      const sentenceCandidate = sentenceChunk ? `${sentenceChunk} ${sentence}` : sentence;
      if (sentenceCandidate.length <= maxChars) {
        sentenceChunk = sentenceCandidate;
      } else {
        if (sentenceChunk) chunks.push(sentenceChunk.trim());
        sentenceChunk = sentence;
      }
    }
    current = sentenceChunk;
  }

  if (current) chunks.push(current.trim());
  return chunks.filter(Boolean);
}

export function extractKeywords(text: string, limit: number): string[] {
  const words = normalizeWhitespace(text).toLowerCase().match(/[a-z][a-z0-9_-]{2,}/g) || [];
  const counts = new Map<string, number>();
  for (const word of words) {
    if (STOP_WORDS.has(word)) continue;
    counts.set(word, (counts.get(word) || 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, limit)
    .map(([word]) => word);
}

export function detectEntities(text: string, limit: number): Entity[] {
  const entityMap = new Map<string, Entity>();
  const titleCaseMatches = text.match(/\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b/g) || [];
  for (const match of titleCaseMatches) {
    const name = match.trim();
    if (name.length < 3 || entityMap.has(name)) continue;
    entityMap.set(name, { name, type: /Inc|Ltd|Corp|Company|University|OpenAI|Google/.test(name) ? "organization" : "person_or_concept" });
    if (entityMap.size >= limit) break;
  }
  const yearMatches = text.match(/\b(20\d{2}|19\d{2})\b/g) || [];
  for (const match of yearMatches) {
    if (entityMap.has(match)) continue;
    entityMap.set(match, { name: match, type: "date" });
    if (entityMap.size >= limit) break;
  }
  return [...entityMap.values()].slice(0, limit);
}

export function buildHashEmbedding(text: string, dimensions = 12): number[] {
  const vector = Array.from({ length: dimensions }, () => 0);
  const tokens = normalizeWhitespace(text).toLowerCase().match(/[a-z0-9_-]{2,}/g) || [];
  if (tokens.length === 0) return vector;
  for (const token of tokens) {
    let hash = 0;
    for (let index = 0; index < token.length; index += 1) {
      hash = ((hash << 5) - hash + token.charCodeAt(index)) | 0;
    }
    const position = Math.abs(hash) % dimensions;
    vector[position] += 1;
  }
  return vector.map((value) => Number((value / tokens.length).toFixed(6)));
}

export function extractActionItems(sentences: string[], limit: number): Array<{ task: string; owner: string; deadline: string }> {
  const outputs: Array<{ task: string; owner: string; deadline: string }> = [];
  const trigger = /\b(action item|todo|follow up|follow-up|need to|needs to|must|should|will|by\s+\w+)/i;
  for (const sentence of sentences) {
    if (!trigger.test(sentence)) continue;
    const ownerMatch = sentence.match(/^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:will|should|must|needs to)/);
    const deadlineMatch = sentence.match(/\b(by\s+[^,.]+|before\s+[^,.]+|on\s+[^,.]+|next\s+[^,.]+)\b/i);
    outputs.push({
      task: sentence.trim(),
      owner: ownerMatch?.[1] || "unassigned",
      deadline: deadlineMatch?.[1] || "unspecified",
    });
    if (outputs.length >= limit) break;
  }
  return outputs;
}

export function uniqueStrings(values: string[], limit?: number): string[] {
  const seen = new Set<string>();
  const output: string[] = [];
  for (const value of values) {
    const normalized = value.trim();
    if (!normalized) continue;
    const key = normalized.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    output.push(normalized);
    if (limit && output.length >= limit) break;
  }
  return output;
}

export function clipText(value: string, limit: number): string {
  const normalized = normalizeWhitespace(value);
  if (normalized.length <= limit) return normalized;
  return `${normalized.slice(0, limit - 3)}...`;
}

export function safeJsonParse<T>(value: string): T | null {
  try {
    return JSON.parse(value) as T;
  } catch {
    return null;
  }
}
