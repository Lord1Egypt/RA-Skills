# Research basis, checked 2026-09-26

Design influences only: no reproduced implementations, dependencies or transferable benchmark scores. Preserve the GPT four-layer design without vector services/background daemons.

| Primary source | Bounded adaptation |
| --- | --- |
| [SimpleMem v3, 2026-01-29](https://arxiv.org/abs/2601.02553v3) | Compact evidence units and query-aware retrieval. The revised paper describes online synthesis; do not import the earlier asynchronous design or gains. |
| [LeanMem v1, 2026-08-04](https://arxiv.org/abs/2608.03463v1) | Separate stable descriptions, changing events and source-grounded records; allocate retrieval by evidence needs. Preprint, not proof of plugin performance. |
| [LongMemEval v2, 2025-03-04](https://arxiv.org/abs/2410.10813v2) | Test extraction, multi-session reasoning, time, updates and abstention. Local synthetic cases are not the benchmark. |
| [Anthropic context engineering, 2025-09-29](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Small relevant context, lightweight pointers, on-demand reading and careful handoffs. Do not assume Claude platform features exist in ChatGPT. |
| [Anatomy of Agentic Memory v2, 2026-05-20](https://arxiv.org/html/2602.19320v2) | Assess correctness alongside retrieval/maintenance cost and model sensitivity. One benchmark or LLM judge is not universal evidence. |

Engineering additions: version-bound checks, supported optimistic concurrency, inspect-before-retry and dependency invalidation. These workflow reliability rules are not claimed paper findings or score gains.

Do not add paid APIs, external accounts, telemetry, embeddings or graph databases because a paper uses them. Recheck primary sources before future “latest” claims. Ground capability claims in tools actually available that session.
