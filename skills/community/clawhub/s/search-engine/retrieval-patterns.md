# Retrieval Patterns — Search Engine

Use this file to select retrieval logic that matches real user intent.

## Pattern 1: Lexical-First Retrieval

Best for exact terminology, short documents, and predictable vocabularies.

- candidate generation from token overlap
- field boosts for title and key metadata
- typo tolerance with conservative limits

## Pattern 2: Semantic-First Retrieval

Best for natural-language queries, long-form content, and paraphrased intent.

- candidate generation by vector similarity
- reranking to reduce semantic false positives
- strong metadata filtering to avoid topic bleed

## Pattern 3: Hybrid Retrieval

Best default for mixed workloads.

- retrieve lexical and semantic candidates in parallel
- deduplicate by stable document identity
- rerank with shared policy and business constraints

## Filtering and Faceting Rules

- filtering narrows candidate space before ranking
- faceting explains available dimensions to users
- avoid hard filters when user intent is exploratory

## Tie-Break and Diversification

- apply deterministic tie-break rules for stable outputs
- diversify near-duplicate results when intent is broad
- do not diversify when query is clearly transactional
