/**
 * MMR (Maximum Marginal Relevance) Diversity Selection
 * Balances relevance vs diversity to avoid homogeneous results
 * mmrSelect: keyword-based (text overlap)
 * mmrSelectWithEmbedding: embedding-based (cosine distance)
 */
import { similarity as jaccardSimilarity } from './dedup.js';

/**
 * Keyword-based MMR selection
 * @param {Array} documents - documents with {text, score} or {memory: {text}, score}
 * @param {number} topK - final number to select
 * @param {number} lambda - diversity weight (0=greedy by score, 1=max diversity)
 * @returns {Array}
 */
export function mmrSelect(documents, topK = 5, lambda = 0.5) {
  if (!documents || documents.length <= topK) return documents;
  const docs = documents.map(d => ({
    text: d.memory?.text || d.text || '',
    score: d.score || d.finalScore || d.bm25Score || 0,
    _orig: d,
  }));
  const selected = [];
  const remaining = [...docs];

  // Pick highest score as seed
  docs.sort((a, b) => b.score - a.score);
  selected.push(docs[0]);
  remaining.splice(0, 1);

  while (selected.length < topK && remaining.length > 0) {
    let bestIdx = -1;
    let bestMMR = -Infinity;

    for (let i = 0; i < remaining.length; i++) {
      const doc = remaining[i];
      // Relevance: normalized score
      const relevance = doc.score / (docs[0].score || 1);
      // Diversity: min Jaccard distance to selected
      let minSimilarity = 1;
      for (const s of selected) {
        const sim = jaccardSimilarity(doc.text, s.text);
        if (sim < minSimilarity) minSimilarity = sim;
      }
      const diversity = 1 - minSimilarity;
      // MMR formula
      const mmr = lambda * relevance + (1 - lambda) * diversity;

      if (mmr > bestMMR) {
        bestMMR = mmr;
        bestIdx = i;
      }
    }

    if (bestIdx === -1) break;
    selected.push(remaining[bestIdx]);
    remaining.splice(bestIdx, 1);
  }

  return selected.map(s => s._orig);
}

/**
 * Embedding-based MMR (cosine distance)
 * @param {Array} documents - documents with {embedding, score}
 * @param {number} topK
 * @param {number} lambda
 * @param {Function} embedFn - optional custom embedding fn
 */
export async function mmrSelectWithEmbedding(documents, topK = 5, lambda = 0.5, embedFn = null) {
  if (!documents || documents.length <= topK) return documents;
  if (!embedFn) return mmrSelect(documents, topK, lambda);

  const docs = documents.map((d, i) => ({
    embedding: d.embedding || d.memory?.embedding,
    score: d.score || d.finalScore || 0,
    _orig: d,
    _idx: i,
  })).filter(d => d.embedding);

  if (docs.length <= topK) return documents;

  // Seed with highest score
  docs.sort((a, b) => b.score - a.score);
  const selected = [docs[0]];
  const remaining = docs.slice(1);

  while (selected.length < topK && remaining.length > 0) {
    let bestIdx = -1;
    let bestMMR = -Infinity;

    for (let i = 0; i < remaining.length; i++) {
      const doc = remaining[i];
      const relevance = doc.score / (docs[0].score || 1);

      let minCosine = 1;
      for (const s of selected) {
        const cos = cosineSimilarity(doc.embedding, s.embedding);
        if (cos < minCosine) minCosine = cos;
      }
      const diversity = 1 - minCosine;
      const mmr = lambda * relevance + (1 - lambda) * diversity;

      if (mmr > bestMMR) {
        bestMMR = mmr;
        bestIdx = i;
      }
    }

    if (bestIdx === -1) break;
    selected.push(remaining[bestIdx]);
    remaining.splice(bestIdx, 1);
  }

  return selected.map(s => s._orig);
}

function cosineSimilarity(a, b) {
  if (!a || !b || a.length !== b.length) return 0;
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB) + 1e-10);
}

export default { mmrSelect, mmrSelectWithEmbedding };
