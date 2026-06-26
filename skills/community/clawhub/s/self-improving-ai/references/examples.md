# Entry Examples

Concrete examples of well-formatted AI/LLM entries with all fields.

## Learning: Model Selection (Code Generation)

```markdown
## [LRN-20250415-001] model_selection

**Logged**: 2025-04-15T10:30:00Z
**Priority**: high
**Status**: resolved
**Area**: model_config

### Summary
Switched from GPT-4o to Claude Sonnet for code generation; 23% improvement on HumanEval, 40% cost reduction

### Details
Evaluated Claude 4 Sonnet against GPT-4o on our internal code generation benchmark (500 multi-file
edit tasks). Sonnet scored 89.2% vs GPT-4o's 72.5% on correct first-attempt edits. Sonnet is
significantly better at following complex multi-file edit instructions where changes span 3+ files
with interdependencies. GPT-4o tended to miss downstream type changes in dependent files.

Cost comparison at 1M tokens/day: GPT-4o ~$45/day vs Sonnet ~$27/day (40% reduction).

### Impact
- **Quality**: 23% improvement on HumanEval pass@1 (72.5% → 89.2%)
- **Cost**: 40% reduction in daily API spend
- **Latency**: Comparable (Sonnet P50: 1.2s, GPT-4o P50: 1.1s)

### Suggested Action
Update model selection matrix: use Claude Sonnet as default for code generation tasks.
Keep GPT-4o as fallback and for tasks requiring function calling with complex schemas.

### Metadata
- Source: benchmark_evaluation
- Model: claude-4-sonnet vs gpt-4o
- Provider: anthropic vs openai
- Modality: text
- Temperature: 0.1
- Token Usage: avg 2,400 input / 1,800 output per task
- Latency: Sonnet P50 1,200ms / GPT-4o P50 1,100ms
- Cost: Sonnet $0.027/task vs GPT-4o $0.045/task
- Tags: model-selection, code-generation, benchmark, cost-optimization
- Pattern-Key: model_selection.code_generation

---
```

## Learning: Prompt Optimization (Chain-of-Thought)

```markdown
## [LRN-20250416-001] prompt_optimization

**Logged**: 2025-04-16T14:00:00Z
**Priority**: medium
**Status**: resolved
**Area**: prompt_engineering

### Summary
Adding "Think step by step before writing code" to system prompt reduced bug rate by 35% on internal eval

### Details
Tested chain-of-thought prompting on our internal eval suite (200 coding tasks with known correct
solutions). Adding "Think step by step before writing code. Identify edge cases before
implementing." to the system prompt reduced incorrect outputs from 31% to 20% (35% relative
improvement).

Effect varies by model:
- Claude 4 Sonnet: 28% → 16% error rate (43% improvement)
- GPT-4o: 34% → 24% error rate (29% improvement)
- Llama 3.1 70B: 45% → 42% error rate (7% improvement — minimal effect)
- Mistral Large: 38% → 30% error rate (21% improvement)

The improvement is most pronounced on tasks requiring multi-step reasoning. Smaller models
(<30B parameters) show minimal benefit, likely because they lack the capacity to execute
chain-of-thought effectively.

### Suggested Action
Add chain-of-thought instruction to system prompt for all code generation tasks using
models >30B parameters. Do not apply to small/fast models as it wastes tokens without benefit.

### Metadata
- Source: a_b_test
- Model: claude-4-sonnet, gpt-4o, llama-3.1-70b, mistral-large
- Provider: anthropic, openai, meta, mistral
- Modality: text
- Temperature: 0.1
- Token Usage: +150 tokens average overhead from CoT reasoning
- Tags: prompt-engineering, chain-of-thought, eval, code-generation
- Pattern-Key: prompt_optimization.chain_of_thought

---
```

## Learning: Context Management (Lost-in-the-Middle)

```markdown
## [LRN-20250417-001] context_management

**Logged**: 2025-04-17T09:15:00Z
**Priority**: high
**Status**: promoted
**Promoted**: RAG architecture doc
**Area**: rag_pipeline

### Summary
RAG context placed at beginning of prompt was ignored; moving chunks to just before user query improved relevance from 67% to 89%

### Details
Our RAG pipeline placed retrieved chunks at the top of the context window, followed by system
instructions, then the user query. Evaluation showed the model frequently ignored retrieved
context, especially when total context exceeded 8K tokens.

This is the "lost-in-the-middle" effect documented in Liu et al. (2023): LLMs attend most strongly
to the beginning and end of context, with a U-shaped attention curve. Information in the middle
of long contexts gets effectively ignored.

Restructured prompt layout:
1. System instructions (brief, ~200 tokens)
2. User query
3. Retrieved context chunks (placed right before the query, within the attention "end" zone)

Result: answer relevance jumped from 67% to 89% on our 500-question eval set.

### Suggested Action
Always place RAG-retrieved context immediately before the user's question, not at the
beginning of the prompt. Keep system instructions minimal and at the very start.

### Metadata
- Source: evaluation
- Model: claude-4-sonnet
- Provider: anthropic
- Modality: text
- Token Usage: same total tokens, different ordering
- Tags: rag, context-management, lost-in-the-middle, prompt-structure
- Pattern-Key: context_management.lost_in_the_middle

---
```

## Learning: Cost Efficiency (Embedding Dimensionality Reduction)

```markdown
## [LRN-20250418-001] cost_efficiency

**Logged**: 2025-04-18T11:00:00Z
**Priority**: medium
**Status**: resolved
**Area**: embeddings

### Summary
Switching from ada-002 (1536d) to a 512d model with Matryoshka dimensionality reduction saved 60% on vector storage with only 2% recall drop

### Details
Our vector store held 2.3M documents embedded with text-embedding-ada-002 at 1536 dimensions.
Storage cost was $840/month on Pinecone. Evaluated switching to text-embedding-3-small with
Matryoshka dimensionality reduction to 512 dimensions.

Benchmark results on our domain-specific retrieval eval (1,000 queries):
- ada-002 (1536d): Recall@10 = 94.2%, MRR = 0.87
- text-embedding-3-small (512d): Recall@10 = 92.1%, MRR = 0.85
- text-embedding-3-small (256d): Recall@10 = 86.4%, MRR = 0.79 (too much degradation)

512d was the sweet spot: 2.1% recall drop, 2.3% MRR drop, but 66% reduction in vector
dimensions → 60% storage cost reduction ($840 → $336/month).

### Suggested Action
Use text-embedding-3-small with 512 dimensions for general-purpose retrieval.
Reserve 1536d for high-precision retrieval tasks (legal, medical).
Never go below 512d without evaluating domain-specific recall.

### Metadata
- Source: benchmark_evaluation
- Model: text-embedding-ada-002 vs text-embedding-3-small
- Provider: openai
- Modality: text
- Cost: $840/month → $336/month (60% reduction)
- Tags: embeddings, dimensionality-reduction, cost, matryoshka, vector-store
- Pattern-Key: cost_efficiency.embedding_reduction

---
```

## Model Issue: Fine-Tune Regression (Catastrophic Forgetting)

```markdown
## [MDL-20250420-001] fine_tune_regression

**Logged**: 2025-04-20T16:00:00Z
**Priority**: critical
**Status**: resolved
**Area**: fine_tuning

### Summary
Fine-tuned Llama 3.1 70B on customer support data; improved tone but catastrophic forgetting on code tasks

### Details
Fine-tuned Llama 3.1 70B with QLoRA (rank 16, alpha 32) on 12K customer support conversation
pairs. Goal: improve empathetic tone and company-specific knowledge.

Results on eval suites:
- Customer support tone: 72% → 91% (target achieved)
- Company FAQ accuracy: 65% → 88% (target achieved)
- HumanEval (coding): 68% → 37% (catastrophic regression)
- MMLU (general knowledge): 79% → 71% (significant regression)

The fine-tuning data was 100% customer support with zero coding or general knowledge examples.
The model over-specialized, losing capabilities in unrelated domains.

### Root Cause
Pure domain-specific fine-tuning without replay data from general capabilities.
QLoRA rank 16 was high enough to significantly modify model weights.

### Fix
1. Mixed training data: 70% customer support + 20% general instruction + 10% coding
2. Reduced QLoRA rank from 16 to 8
3. Added eval gates: abort training if any benchmark drops >5% from baseline

Post-fix results:
- Customer support tone: 72% → 87% (slightly lower but acceptable)
- HumanEval: 68% → 65% (within 5% threshold)
- MMLU: 79% → 77% (within 5% threshold)

### Metadata
- Model: llama-3.1-70b (fine-tuned)
- Provider: meta (self-hosted)
- Modality: text
- Temperature: 0.3
- Training: QLoRA rank 16 → rank 8, 3 epochs, lr 2e-4
- Eval: HumanEval, MMLU, custom tone scorer, custom FAQ accuracy
- Tags: fine-tuning, catastrophic-forgetting, qlora, regression, eval
- Pattern-Key: fine_tune_regression.catastrophic_forgetting

### Resolution
- **Resolved**: 2025-04-22T10:00:00Z
- **Notes**: Mixed training data prevents catastrophic forgetting. Always include replay data.

---
```

## Model Issue: Multimodal Gap (Scanned PDF with Rotation)

```markdown
## [MDL-20250421-001] modality_gap

**Logged**: 2025-04-21T13:30:00Z
**Priority**: high
**Status**: resolved
**Area**: multimodal

### Summary
Claude vision fails to read handwritten text in scanned PDFs with >15 degree rotation

### Details
Document processing pipeline sends scanned PDFs to Claude 4 Opus vision for OCR and extraction.
Quality was high for clean scans but dropped severely for documents with rotation, skew, or
handwritten annotations.

Failure modes:
- Rotation >15°: model returns "I can't read the text clearly" or hallucinates content
- Handwritten annotations overlapping printed text: annotation ignored or misattributed
- Low-contrast scans (<100 DPI effective): complete extraction failure

Testing across 200 scanned documents:
- Clean scans (0° rotation, typed text): 96% accuracy
- Minor rotation (<15°): 89% accuracy
- Significant rotation (>15°): 42% accuracy
- Handwritten + rotation: 23% accuracy

### Fix
Added preprocessing pipeline before model ingestion:
1. Deskew with OpenCV `cv2.minAreaRect` + affine transform
2. Contrast normalization (CLAHE)
3. Upscale low-DPI images to minimum 300 DPI
4. Separate handwritten region detection with dedicated model

Post-fix: accuracy on rotated documents improved from 42% to 91%.

### Metadata
- Model: claude-4-opus
- Provider: anthropic
- Modality: multimodal (image/PDF)
- Token Usage: ~1,200 input tokens per page (image)
- Latency: 3,200ms per page
- Cost: $0.048 per page
- Tags: multimodal, vision, pdf, ocr, rotation, preprocessing
- Pattern-Key: modality_gap.rotated_pdf

### Resolution
- **Resolved**: 2025-04-22T15:00:00Z
- **Notes**: Always preprocess scanned documents before sending to vision models.

---
```

## Feature Request: Automated Model A/B Testing

```markdown
## [FEAT-20250419-001] model_ab_testing_framework

**Logged**: 2025-04-19T10:00:00Z
**Priority**: high
**Status**: pending
**Area**: evaluation

### Requested Capability
Automated model A/B testing framework that routes N% of requests to a candidate model
and compares outputs via LLM-as-judge evaluation.

### User Context
Currently comparing models requires manual benchmark runs on static eval sets.
We need to evaluate models on live production traffic to catch real-world differences
that synthetic benchmarks miss. Manual A/B testing is error-prone and takes 2-3 days
per comparison.

### Complexity Estimate
complex

### Suggested Implementation
1. Traffic router: split N% of requests to candidate model (configurable per endpoint)
2. Dual inference: both models process the same input, only primary response is served
3. LLM-as-judge: third model evaluates both outputs on quality, relevance, safety
4. Metrics dashboard: win rate, quality score distribution, latency comparison, cost delta
5. Auto-promote: if candidate wins by >5% over 1,000 samples, flag for promotion
6. Guardrails: abort test if candidate error rate exceeds 2x baseline

Architecture:
```
Request → Router → [Primary Model] → Response to user
                 → [Candidate Model] → Shadow response
                                     → LLM Judge → Metrics DB → Dashboard
```

### Metadata
- Frequency: recurring (every model evaluation cycle)
- Related Features: model selection matrix, eval pipeline, provider routing

---
```

## Learning: Promoted to Skill (RAG Chunk Sizing)

```markdown
## [LRN-20250412-001] context_management

**Logged**: 2025-04-12T15:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/rag-chunk-sizing
**Area**: rag_pipeline

### Summary
Optimal RAG chunk sizes vary significantly by content type; one-size-fits-all chunking degrades retrieval quality

### Details
After 3 months of RAG pipeline tuning across 4 projects, established optimal chunk sizes
by content type based on retrieval recall@10 benchmarks:

| Content Type | Optimal Chunk Size | Overlap | Boundary Strategy |
|--------------|-------------------|---------|-------------------|
| Source code | 100-200 lines | 20 lines | Function/class boundaries |
| Documentation (prose) | 500-800 tokens | 50 tokens | Semantic paragraph boundaries |
| Tables / structured data | Full table as single chunk | None | Preserve table integrity |
| API references | One endpoint per chunk | None | Endpoint boundary |
| Chat transcripts | One conversation turn | 1 turn | Speaker change |
| Legal documents | 300-500 tokens | 100 tokens | Section/clause boundaries |

Key findings:
- Code chunks that split mid-function lose 34% retrieval accuracy
- Tables split across chunks are effectively useless (retrieval recall drops to 12%)
- Prose chunked at arbitrary token boundaries vs semantic boundaries: 15% recall difference
- Overlap is critical for prose but harmful for structured data (causes duplicate retrieval)

### Suggested Action
Implement content-type-aware chunking in the RAG pipeline. Detect content type before
chunking and apply the appropriate strategy. Never use a single chunk size for all content.

### Metadata
- Source: benchmark_evaluation
- Model: text-embedding-3-small (512d)
- Provider: openai (embeddings)
- Tags: rag, chunking, retrieval, content-type, benchmark
- See Also: LRN-20250320-003, LRN-20250401-007, MDL-20250405-002
- Pattern-Key: context_management.chunk_sizing
- Recurrence-Count: 4
- First-Seen: 2025-01-20
- Last-Seen: 2025-04-12

---
```
