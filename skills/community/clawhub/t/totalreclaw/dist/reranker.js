/**
 * TotalReclaw Plugin - Client-Side Re-Ranker
 *
 * Replaces the naive `textScore` word-overlap scorer with a proper ranking
 * pipeline:
 *   1. Okapi BM25 — term frequency / inverse document frequency
 *   2. Cosine similarity — between query and fact embeddings (WASM-backed)
 *   3. Importance — normalized importance score (0-1)
 *   4. Recency — time-decay with 1-week half-life
 *   5. Weighted RRF (Reciprocal Rank Fusion) — combines all ranking lists
 *   6. MMR (Maximal Marginal Relevance) — promotes diversity in results
 *
 * Cosine similarity delegates to the Rust WASM core for performance.
 * All other functions are pure TypeScript. This module runs CLIENT-SIDE
 * after decrypting candidates from the server.
 */
// ---------------------------------------------------------------------------
// Cosine Similarity
// ---------------------------------------------------------------------------
/**
 * Compute cosine similarity between two vectors.
 *
 * Returns dot(a, b) / (||a|| * ||b||).
 * Returns 0 if either vector has zero magnitude (avoids division by zero).
 */
export function cosineSimilarity(a, b) {
    if (a.length === 0 || b.length === 0)
        return 0;
    const len = Math.min(a.length, b.length);
    let dot = 0;
    let normA = 0;
    let normB = 0;
    for (let i = 0; i < len; i++) {
        dot += a[i] * b[i];
        normA += a[i] * a[i];
        normB += b[i] * b[i];
    }
    const denom = Math.sqrt(normA) * Math.sqrt(normB);
    if (denom === 0)
        return 0;
    return dot / denom;
}
// ---------------------------------------------------------------------------
// Tokenization
// ---------------------------------------------------------------------------
/**
 * Tokenize a text string for BM25 scoring.
 *
 * Matches the tokenization rules used for blind indices in crypto.ts:
 *   1. Lowercase
 *   2. Remove punctuation (keep Unicode letters, numbers, whitespace)
 *   3. Split on whitespace
 *   4. Filter tokens shorter than 2 characters
 *
 * Removes common English stop words to improve BM25 signal — stop words
 * have low IDF and add noise.
 */
const STOP_WORDS = new Set([
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'do', 'for',
    'from', 'had', 'has', 'have', 'he', 'her', 'him', 'his', 'how', 'if',
    'in', 'into', 'is', 'it', 'its', 'me', 'my', 'no', 'not', 'of', 'on',
    'or', 'our', 'out', 'she', 'so', 'than', 'that', 'the', 'their', 'them',
    'then', 'there', 'these', 'they', 'this', 'to', 'up', 'us', 'was', 'we',
    'were', 'what', 'when', 'where', 'which', 'who', 'whom', 'why', 'will',
    'with', 'you', 'your',
]);
export function tokenize(text, removeStopWords = true) {
    let tokens = text
        .toLowerCase()
        .replace(/[^\p{L}\p{N}\s]/gu, ' ')
        .split(/\s+/)
        .filter((t) => t.length >= 2);
    if (removeStopWords) {
        tokens = tokens.filter((t) => !STOP_WORDS.has(t));
    }
    return tokens;
}
// ---------------------------------------------------------------------------
// BM25 Scoring (Okapi BM25)
// ---------------------------------------------------------------------------
/**
 * Compute the Okapi BM25 score for a single document against a query.
 *
 * @param queryTerms  - Tokenized query terms
 * @param docTerms    - Tokenized document terms
 * @param avgDocLen   - Average document length (in tokens) across the candidate corpus
 * @param docCount    - Total number of documents in the candidate corpus
 * @param termDocFreqs - Map from term to number of documents containing that term
 * @param k1          - BM25 k1 parameter (default 1.2)
 * @param b           - BM25 b parameter (default 0.75)
 */
export function bm25Score(queryTerms, docTerms, avgDocLen, docCount, termDocFreqs, k1 = 1.2, b = 0.75) {
    if (docTerms.length === 0 || avgDocLen === 0 || docCount === 0)
        return 0;
    // Count term frequencies in this document.
    const docTf = new Map();
    for (const term of docTerms) {
        docTf.set(term, (docTf.get(term) ?? 0) + 1);
    }
    const docLen = docTerms.length;
    let score = 0;
    for (const qi of queryTerms) {
        const freq = docTf.get(qi) ?? 0;
        if (freq === 0)
            continue;
        const nqi = termDocFreqs.get(qi) ?? 0;
        // IDF with Robertson-Walker floor: ln((N - n + 0.5) / (n + 0.5) + 1)
        const idf = Math.log((docCount - nqi + 0.5) / (nqi + 0.5) + 1);
        // TF saturation with length normalization.
        const tfNorm = (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * docLen / avgDocLen));
        score += idf * tfNorm;
    }
    return score;
}
/**
 * Fuse multiple ranking lists using Reciprocal Rank Fusion.
 */
export function rrfFuse(rankings, k = 60) {
    const fusedScores = new Map();
    for (const ranking of rankings) {
        for (let rank = 0; rank < ranking.length; rank++) {
            const item = ranking[rank];
            const contribution = 1 / (k + rank + 1);
            fusedScores.set(item.id, (fusedScores.get(item.id) ?? 0) + contribution);
        }
    }
    const fused = [];
    for (const [id, score] of fusedScores) {
        fused.push({ id, score });
    }
    fused.sort((a, b) => b.score - a.score);
    return fused;
}
// ---------------------------------------------------------------------------
// Weighted Reciprocal Rank Fusion
// ---------------------------------------------------------------------------
/**
 * Fuse multiple ranking lists using Weighted Reciprocal Rank Fusion.
 */
export function weightedRrfFuse(rankings, weights, k = 60) {
    const fusedScores = new Map();
    for (let r = 0; r < rankings.length; r++) {
        const w = weights[r] ?? 1;
        for (let rank = 0; rank < rankings[r].length; rank++) {
            const item = rankings[r][rank];
            const contribution = w * (1 / (k + rank + 1));
            fusedScores.set(item.id, (fusedScores.get(item.id) ?? 0) + contribution);
        }
    }
    const fused = [];
    for (const [id, score] of fusedScores) {
        fused.push({ id, score });
    }
    fused.sort((a, b) => b.score - a.score);
    return fused;
}
export const DEFAULT_WEIGHTS = {
    bm25: 0.25,
    cosine: 0.25,
    importance: 0.25,
    recency: 0.25,
};
const TEMPORAL_KEYWORDS = /\b(yesterday|today|last\s+week|last\s+month|recently|recent|latest|ago|when|this\s+week|this\s+month|earlier|before|after|since|during|tonight|morning|afternoon)\b/i;
const FACTUAL_PATTERNS = /^(what|who|where|which|how\s+many|how\s+much|is\s+|are\s+|does\s+|do\s+|did\s+|was\s+|were\s+)\b/i;
/** Ranking weights tuned for each query intent. */
export const INTENT_WEIGHTS = {
    factual: { bm25: 0.40, cosine: 0.20, importance: 0.25, recency: 0.15 },
    temporal: { bm25: 0.15, cosine: 0.20, importance: 0.20, recency: 0.45 },
    semantic: { bm25: 0.20, cosine: 0.35, importance: 0.25, recency: 0.20 },
};
/**
 * Classify a query into one of three intent types using lightweight heuristics.
 * Temporal is checked first so "What did we discuss yesterday?" -> temporal.
 */
export function detectQueryIntent(query) {
    if (TEMPORAL_KEYWORDS.test(query))
        return 'temporal';
    if (FACTUAL_PATTERNS.test(query) && query.length < 80)
        return 'factual';
    return 'semantic';
}
// ---------------------------------------------------------------------------
// Source-weight lookup (Retrieval v2 Tier 1)
//
// Mirrors the table in `rust/totalreclaw-core/src/reranker.rs` exactly so
// the TypeScript reranker produces the same ordering as core rerankWithConfig
// when `applySourceWeights: true` is passed.
//
// NOTE: this is duplicated here (vs calling core via WASM) because the
// plugin's local reranker handles RRF + MMR on the client side with rich
// candidate metadata. The core `rerankWithConfig` is the canonical source
// of truth and will be used directly by MCP/Python adapters.
// ---------------------------------------------------------------------------
// v2-lenient (core 2.4.0+, default). Bench-validated across 3+ corpora per
// docs/plans/2026-04-28-v2-lenient-promotion-proposal.md. Mirrors
// `SOURCE_WEIGHTS` in rust/totalreclaw-core/src/reranker.rs — values MUST
// stay in lockstep or the cross-runtime parity test fails.
const SOURCE_WEIGHTS = {
    'user': 1.0,
    'user-inferred': 0.95,
    'derived': 0.85,
    'external': 0.85,
    'assistant': 0.85,
};
const LEGACY_FALLBACK_WEIGHT = 0.85;
export function getSourceWeight(source) {
    if (!source)
        return LEGACY_FALLBACK_WEIGHT;
    const w = SOURCE_WEIGHTS[source.toLowerCase()];
    return w ?? 0.85; // unknown source → moderate penalty
}
// ---------------------------------------------------------------------------
// Recency Scoring
// ---------------------------------------------------------------------------
/**
 * Compute a recency score with a 1-week half-life.
 */
function recencyScore(createdAt) {
    const nowSeconds = Date.now() / 1000;
    const hoursSince = (nowSeconds - createdAt) / 3600;
    return 1 / (1 + hoursSince / 168);
}
// ---------------------------------------------------------------------------
// MMR (Maximal Marginal Relevance)
// ---------------------------------------------------------------------------
/**
 * Apply Maximal Marginal Relevance to promote diversity in results.
 */
export function applyMMR(candidates, lambda = 0.7, topK = 8) {
    if (candidates.length === 0)
        return [];
    if (candidates.length <= 1)
        return candidates.slice(0, topK);
    const remaining = candidates.map((c, i) => ({ candidate: c, index: i }));
    const selected = [];
    const n = candidates.length;
    while (selected.length < topK && remaining.length > 0) {
        let bestIdx = -1;
        let bestMMR = -Infinity;
        for (let i = 0; i < remaining.length; i++) {
            const { candidate, index } = remaining[i];
            // Relevance: linear decay from 1.0 (first) to near 0 (last)
            const relevance = 1.0 - index / n;
            // Max similarity to any already-selected candidate
            let maxSim = 0;
            if (candidate.embedding && candidate.embedding.length > 0) {
                for (const sel of selected) {
                    if (sel.embedding && sel.embedding.length > 0) {
                        const sim = cosineSimilarity(candidate.embedding, sel.embedding);
                        if (sim > maxSim)
                            maxSim = sim;
                    }
                }
            }
            const mmr = lambda * relevance - (1 - lambda) * maxSim;
            if (mmr > bestMMR) {
                bestMMR = mmr;
                bestIdx = i;
            }
        }
        if (bestIdx >= 0) {
            selected.push(remaining[bestIdx].candidate);
            remaining.splice(bestIdx, 1);
        }
        else {
            break;
        }
    }
    return selected;
}
// ---------------------------------------------------------------------------
// Combined Re-Ranker
// ---------------------------------------------------------------------------
/**
 * Re-rank decrypted candidates using BM25 + Cosine + Importance + Recency
 * with Weighted RRF fusion and MMR diversity.
 *
 * When `applySourceWeights` is true, the final RRF score for each candidate
 * is multiplied by a Retrieval v2 Tier 1 source weight based on the
 * candidate's `source` field. v2-lenient (core 2.4.0+, default):
 * user=1.0, user-inferred=0.95, derived/external/assistant=0.85.
 * Candidates without a `source` field use the legacy fallback weight (0.85).
 * This is the flag equivalent of core
 * `rerankWithConfig(.., apply_source_weights=true)`.
 */
export function rerank(query, queryEmbedding, candidates, topK = 8, weights, applySourceWeights = false) {
    if (candidates.length === 0)
        return [];
    // Merge caller weights with defaults
    const w = { ...DEFAULT_WEIGHTS, ...weights };
    // --- Step 1: Tokenize ---
    const queryTerms = tokenize(query);
    const candidateTerms = candidates.map((c) => tokenize(c.text));
    // --- Step 2: Corpus statistics ---
    const docCount = candidates.length;
    let totalDocLen = 0;
    const termDocFreqs = new Map();
    for (const terms of candidateTerms) {
        totalDocLen += terms.length;
        const uniqueTerms = new Set(terms);
        for (const term of uniqueTerms) {
            termDocFreqs.set(term, (termDocFreqs.get(term) ?? 0) + 1);
        }
    }
    const avgDocLen = docCount > 0 ? totalDocLen / docCount : 0;
    // --- Step 3: BM25 scores ---
    const bm25Ranking = [];
    for (let i = 0; i < candidates.length; i++) {
        const score = bm25Score(queryTerms, candidateTerms[i], avgDocLen, docCount, termDocFreqs);
        bm25Ranking.push({ id: candidates[i].id, score });
    }
    bm25Ranking.sort((a, b) => b.score - a.score);
    // --- Step 4: Cosine similarity scores ---
    const cosineScores = new Map();
    const cosineRanking = [];
    for (const candidate of candidates) {
        if (candidate.embedding && candidate.embedding.length > 0) {
            const score = cosineSimilarity(queryEmbedding, candidate.embedding);
            cosineScores.set(candidate.id, score);
            cosineRanking.push({ id: candidate.id, score });
        }
    }
    cosineRanking.sort((a, b) => b.score - a.score);
    // --- Step 5: Importance ranking ---
    const importanceRanking = candidates.map((c) => ({
        id: c.id,
        score: c.importance ?? 0.5,
    }));
    importanceRanking.sort((a, b) => b.score - a.score);
    // --- Step 6: Recency ranking ---
    const recencyRanking = candidates.map((c) => ({
        id: c.id,
        score: c.createdAt != null ? recencyScore(c.createdAt) : 0.5,
    }));
    recencyRanking.sort((a, b) => b.score - a.score);
    // --- Step 7: Weighted RRF fusion ---
    const rankings = [bm25Ranking];
    const rankWeights = [w.bm25];
    if (cosineRanking.length > 0) {
        rankings.push(cosineRanking);
        rankWeights.push(w.cosine);
    }
    rankings.push(importanceRanking);
    rankWeights.push(w.importance);
    rankings.push(recencyRanking);
    rankWeights.push(w.recency);
    const fused = weightedRrfFuse(rankings, rankWeights);
    // --- Step 8: Build result objects with scores ---
    const candidateMap = new Map();
    for (const c of candidates) {
        candidateMap.set(c.id, c);
    }
    const rrfResults = [];
    for (const item of fused) {
        const candidate = candidateMap.get(item.id);
        if (candidate) {
            const sourceWeight = applySourceWeights
                ? getSourceWeight(candidate.source)
                : 1.0;
            rrfResults.push({
                ...candidate,
                rrfScore: item.score * sourceWeight,
                cosineSimilarity: cosineScores.get(item.id),
                sourceWeight: applySourceWeights ? sourceWeight : undefined,
            });
        }
    }
    // When source weights are applied the RRF-scaled scores may no longer be in
    // descending order (weighted=0.85 assistant could slip below a weighted=1.0
    // user fact that was originally ranked lower). Re-sort so the top-K picked
    // by MMR is meaningful.
    if (applySourceWeights) {
        rrfResults.sort((a, b) => b.rrfScore - a.rrfScore);
    }
    // --- Step 9: Apply MMR for diversity, then return top-k ---
    const mmrResults = applyMMR(rrfResults, 0.7, topK);
    // Preserve rrfScore and cosineSimilarity through MMR
    return mmrResults;
}
// ---------------------------------------------------------------------------
// Relevance gate
// ---------------------------------------------------------------------------
/**
 * Decide whether reranked results clear the relevance gate for surfacing to
 * the user (recall tool) or auto-injecting into agent context (hooks).
 *
 * Plain cosine cut-off: at least one reranked result has cosine similarity
 * with the query embedding >= `cosineThreshold`.
 *
 * History (rc.18 → rc.22):
 *   rc.18 issue #116 surfaced as a recall miss for short queries against
 *   the local Harrier-OSS-270m model — cosine alone produced false-negatives
 *   even when every query token literally appeared in the candidate. rc.18
 *   shipped a defensive "lexical-override" fallback (every meaningful query
 *   token had to appear as a 4-char-prefix substring in the top result).
 *   The override was always intended as a band-aid until the
 *   source-weighted reranker hoisted from `totalreclaw-core` produced
 *   honest cosine signals for short queries. rc.22 hoists that reranker
 *   and drops the band-aid: the gate is now back to a single-signal cosine
 *   cut-off, matching Hermes (Python client) and the canonical reranker
 *   spec.
 *
 * @param query - the user's search query (raw string) — accepted for ABI
 *   stability, no longer consulted post rc.22.
 * @param reranked - reranked results (top first)
 * @param cosineThreshold - the configured cosine cutoff (typically 0.15)
 * @returns true if results should be surfaced; false to suppress
 */
export function passesRelevanceGate(_query, reranked, cosineThreshold) {
    if (reranked.length === 0)
        return false;
    const maxCosine = Math.max(...reranked.map((r) => r.cosineSimilarity ?? 0));
    return maxCosine >= cosineThreshold;
}
