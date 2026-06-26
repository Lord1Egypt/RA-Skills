# Evaluation Metrics — Search Engine

Use this file before shipping relevance or indexing changes.

## Offline Quality Signals

| Metric | What It Measures | Common Failure |
|--------|------------------|----------------|
| Precision@k | Useful results in top-k | Overly broad retrieval |
| Recall@k | Coverage of relevant items | Missing candidates |
| MRR | How soon first good hit appears | Weak top ranking |
| NDCG@k | Ordering quality by graded relevance | Inconsistent reranking |

## Reliability Signals

- p50/p95/p99 latency by query path
- timeout and error rate by endpoint
- stale index percentage and refresh lag

## Query Set Design

Include at least:
- head queries with high traffic
- long-tail diagnostic queries
- multilingual or domain-specific queries
- negative queries that should return sparse results

## Release Gate Template

1. Baseline comparison complete with no critical regressions.
2. Latency within agreed SLO limits.
3. Incident rollback steps validated.
4. Monitoring alerts configured for first rollout window.

If any gate fails, keep current production policy and iterate.
