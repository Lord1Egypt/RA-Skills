/**
 * Token Counter - Estimate token counts
 */

import { encoding_for_model } from 'tiktoken';

let encoder = null;

async function getEncoder() {
  if (!encoder) {
    try {
      encoder = await encoding_for_model('gpt-4');
    } catch {
      // Fallback to cl100k_base
      encoder = await import('tiktoken').then(m => m.get_encoding('cl100k_base'));
    }
  }
  return encoder;
}

export async function tokenCount(text) {
  try {
    const enc = await getEncoder();
    return enc.encode(text).length;
  } catch {
    // Fallback: rough estimate
    return Math.ceil(text.length / 4);
  }
}

export async function truncateToTokens(text, maxTokens) {
  try {
    const enc = await getEncoder();
    const tokens = enc.encode(text);
    if (tokens.length <= maxTokens) return text;
    
    return enc.decode(tokens.slice(0, maxTokens));
  } catch {
    // Fallback
    return text.slice(0, maxTokens * 4);
  }
}