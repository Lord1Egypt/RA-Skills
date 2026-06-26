#!/usr/bin/env node
'use strict';

/**
 * Stream Assembler — Merges validated fragments into a coherent answer
 *
 * ClawHub Security: NO network access. NO file system writes.
 * Pure synchronous computation on caller-provided data.
 *
 * Input  JSON: { fragments: [...], query: string, lang?: "zh"|"en" }
 * Output JSON: { answer, coherenceScore, tokensEstimate, fragmentCount, warnings }
 */

// ---------------------------------------------------------------------------
// Token estimator (rough: 1 token ≈ 4 chars for English, 2 chars for Chinese)
// ---------------------------------------------------------------------------
function estimateTokens(text) {
  const chineseChars = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const otherChars   = text.length - chineseChars;
  return Math.ceil(chineseChars / 2 + otherChars / 4);
}

// ---------------------------------------------------------------------------
// Deduplication: remove fragments with > 80% overlapping content
// ---------------------------------------------------------------------------
function jaccard(a, b) {
  const setA = new Set(a.toLowerCase().split(/\s+/));
  const setB = new Set(b.toLowerCase().split(/\s+/));
  const intersection = [...setA].filter(x => setB.has(x)).length;
  const union = new Set([...setA, ...setB]).size;
  return union === 0 ? 0 : intersection / union;
}

function deduplicateFragments(fragments) {
  const kept = [];
  for (const frag of fragments) {
    const content = frag.content || frag.snippet || '';
    const isDuplicate = kept.some(k => {
      const kContent = k.content || k.snippet || '';
      return jaccard(content, kContent) > 0.8;
    });
    if (!isDuplicate) kept.push(frag);
  }
  return kept;
}

// ---------------------------------------------------------------------------
// Coherence scorer: measures semantic relatedness between consecutive fragments
// ---------------------------------------------------------------------------
function simpleTokenSet(text) {
  return new Set(
    text.toLowerCase()
      .replace(/[^\w\u4e00-\u9fff\s]/g, ' ')
      .split(/\s+/)
      .filter(t => t.length > 1)
  );
}

function overlapScore(textA, textB) {
  const setA = simpleTokenSet(textA);
  const setB = simpleTokenSet(textB);
  const inter = [...setA].filter(t => setB.has(t)).length;
  const min   = Math.min(setA.size, setB.size);
  return min === 0 ? 0 : inter / min;
}

function computeCoherence(fragments, query) {
  if (fragments.length === 0) return 0;
  if (fragments.length === 1) return 0.9;  // single fragment is always coherent

  let totalSim = 0;
  // Compare each fragment to the query + previous fragment
  for (let i = 0; i < fragments.length; i++) {
    const content = fragments[i].content || fragments[i].snippet || '';
    const queryScore = overlapScore(content, query);
    const prevScore  = i > 0
      ? overlapScore(content, fragments[i - 1].content || fragments[i - 1].snippet || '')
      : 1.0;
    totalSim += (queryScore * 0.6 + prevScore * 0.4);
  }

  return +(totalSim / fragments.length).toFixed(3);
}

// ---------------------------------------------------------------------------
// Format header for each fragment
// ---------------------------------------------------------------------------
function formatFragmentHeader(frag, idx, lang) {
  if (frag.file) {
    const lineInfo = frag.line ? `:${frag.line}` : '';
    return lang === 'zh'
      ? `**[${idx + 1}] 来源：${frag.file}${lineInfo}**`
      : `**[${idx + 1}] Source: ${frag.file}${lineInfo}**`;
  }
  if (frag.url || frag.domain) {
    return lang === 'zh'
      ? `**[${idx + 1}] 来源：${frag.domain || frag.url}**`
      : `**[${idx + 1}] Source: ${frag.domain || frag.url}**`;
  }
  return `**[${idx + 1}]**`;
}

// ---------------------------------------------------------------------------
// Main assembler
// ---------------------------------------------------------------------------
function assemble(input) {
  const { fragments = [], query = '', lang = 'en' } = input;

  if (fragments.length === 0) {
    return { answer: '', coherenceScore: 0, tokensEstimate: 0, fragmentCount: 0, warnings: ['no_fragments'] };
  }

  // Deduplicate
  const unique = deduplicateFragments(fragments);
  const warnings = [];
  if (unique.length < fragments.length) {
    warnings.push(`deduped_${fragments.length - unique.length}_fragments`);
  }

  // Score coherence before assembly
  const coherenceScore = computeCoherence(unique, query);
  if (coherenceScore < 0.3) warnings.push('low_coherence_consider_requery');

  // Build answer string (streaming-ready: each section is a complete block)
  const sections = unique.map((frag, i) => {
    const header  = formatFragmentHeader(frag, i, lang);
    const content = (frag.content || frag.snippet || '').trim().slice(0, 2000);
    return `${header}\n\n${content}`;
  });

  const answer = sections.join('\n\n---\n\n');
  const tokensEstimate = estimateTokens(answer);

  if (tokensEstimate > 3000) warnings.push('answer_may_be_too_long');

  return {
    answer,
    coherenceScore,
    tokensEstimate,
    fragmentCount: unique.length,
    lang,
    warnings
  };
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
function main() {
  const arg = process.argv[2];

  if (!arg) {
    console.error('Usage: node scripts/stream-assembler.js \'{"fragments":[...],"query":"..."}\'');
    process.exit(1);
  }

  try {
    const input = JSON.parse(arg);
    console.log(JSON.stringify(assemble(input)));
  } catch (e) {
    console.log(JSON.stringify({ error: e.message }));
    process.exit(1);
  }
}

main();
