# Source References

## Primary Repository
**xai-org/x-algorithm**: https://github.com/xai-org/grok-1 (original Grok architecture)
Exposed at: https://github.com/xai-org/x-algorithm (For You feed algorithm documentation)

## Key Files Analyzed

### System Overview
- `/README.md` - High-level architecture overview, pipeline stages, scoring mechanics

### Phoenix Components (ML Models)
- `/phoenix/README.md` - Detailed Phoenix architecture, two-tower retrieval, ranking with candidate isolation
- `/phoenix/recsys_model.py` - Ranking model implementation (Grok transformer, hash embeddings, candidate isolation mask)
- `/phoenix/recsys_retrieval_model.py` - Retrieval model (two-tower, user+candidate encoders)
- `/phoenix/grok.py` - Transformer implementation (attention, RoPE, RMSNorm, candidate isolation masking)

### Home Mixer (Pipeline)
- `/home-mixer/lib.rs` - Pipeline framework definition
- `/home-mixer/candidate_pipeline/candidate_pipeline.rs` - Stage orchestration, parallel execution
- `/home-mixer/scorers/phoenix_scorer.rs` - ML prediction integration
- `/home-mixer/scorers/weighted_scorer.rs` - Score combination, VQV eligibility, offset calculation
- `/home-mixer/scorers/author_diversity_scorer.rs` - Diversity decay algorithm
- `/home-mixer/filters/mod.rs` - Filter catalog (pre and post-selection)

### Thunder (In-Network Source)
- `/thunder/thunder_service.rs` - In-memory post store, real-time ingestion
- `/thunder/posts/post_store.rs` - Per-user post indexing

### Candidate Pipeline Framework
- `/candidate-pipeline/candidate_pipeline.rs` - Async pipeline trait definitions
- `/candidate-pipeline/scorer.rs` - Scorer trait
- `/candidate-pipeline/filter.rs` - Filter trait
- `/candidate-pipeline/hydrator.rs` - Hydrator trait
- `/candidate-pipeline/source.rs` - Source trait

## Engagement Actions Modeled
From `recsys_model.py` and `phoenix_scorer.rs`:

### Discrete Actions (Probabilities)
- `favorite` (like)
- `reply`
- `retweet`
- `quote`
- `click`
- `profile_click`
- `photo_expand`
- `share`
- `dwell`
- `follow_author`
- `not_interested` (negative)
- `block_author` (negative)
- `mute_author` (negative)
- `report` (negative)
- `share_via_dm`
- `share_via_copy_link`
- `quoted_click`

### Continuous Actions
- `dwell_time` (in milliseconds)

## Scoring Flow

```text
User + History (S positions)
      │
      ▼
┌─────────────────────┐
│  Transformer (Grok) │  ← Candidate isolation mask applied
└─────────────────────┘
      │
      ▼
Extract candidate outputs (C positions)
      │
      ▼
Unembedding → logits [B, C, num_actions]
      │
      ▼
Softmax per action → probabilities
      │
      ▼
Weighted sum → combined_score
      │
      ▼
Author diversity adjustment → final_score
```

## Candidate Isolation Mask Logic (from `grok.py`)

```
Full sequence: [user] + [history] + [candidates]
Attn mask:
- User/History: can attend to all User/History (causal bidirectional)
- Candidates: can attend to User/History AND self (diagonal)
- Candidates: CANNOT attend to other candidates (only self)

Result: Each candidate's context = user + history + itself. Independent scoring.
```

## Important Notes

1. **Exact weight values are not public**: The `params` module is excluded from open source. All weight constants (FAVORITE_WEIGHT, REPLY_WEIGHT, etc.) are proprietary.
2. **Thresholds are not specified**: Age filter duration, VQV minimum video duration, diversity decay factor, floor, negative score offset, these are tuned internally.
3. **Model hyperparameters**: embedding_size, num_layers, num_heads, key_size not documented in the repo.
4. **Online features**: The repo shows batch features only. Real-time features like "number of times shown today" might exist but not shown.
5. **Training data regime**: Not described.

## Inference: What This Means for Content Strategy

Since exact weights are unknown, we infer relative importance from:
- Which actions are explicitly modeled (multiple candidate interactions → likely higher value)
- Which actions are negative (these definitely hurt)
- Which actions indicate deep engagement (dwell time, video view, photo expand, replies)
- Which actions are shallow (likes)

The presence of rich interaction types (quote, share, dwell_time) suggests the model goes beyond clickbait and rewards sustained engagement.

## Conversion to Social Media Advice

Technical property → Content implication:

| ML Feature | Content Implication |
|------------|---------------------|
| Multi-action prediction | Don't just chase likes; design for the action that matters to you |
| Candidate isolation | Your content's score is absolute, not relative. Quality always wins. |
| No hand-engineered features | The model understands context; write naturally for your audience |
| Negative weights | Avoid spammy/baiting tactics that trigger blocks/mutes/reports |
| Author diversity | Space out posts; quantity ≠ reach |
| Video view weight | Native video with strong hook matters |
| Dwell time | Medium-length substantial content rewards reading time |
| History-based relevance | Consistency in niche builds better user embeddings over time |
| Hash embeddings | Semantic meaning matters; keywords help but don't over-optimize |
| Freshness filter | Timeliness, trend-jacking, newsjacking effective |
| Pre-scoring filters | Quality gate: must be fresh, unique, non-self, complete data |

## Further Reading (External)
- Grok-1 paper/announcement: https://x.ai/blog/grok-1
- Transformer architecture: "Attention Is All You Need" (Vaswani et al.)
- Two-tower models: Classic retrieval architecture
- Recommendation systems: Coursera, Stanford CS246 references
