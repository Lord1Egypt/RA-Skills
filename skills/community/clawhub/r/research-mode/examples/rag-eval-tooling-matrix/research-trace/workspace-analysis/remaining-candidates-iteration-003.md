# Iteration 003: Remaining Candidate Evidence

Focused search pass covering the five remaining official-source candidates named in the work order.

| Candidate | Suggested matrix treatment | Evidence summary | Practical scoring notes | Source |
|---|---|---|---|---|
| Evidently | Primary row | Official RAG evaluation tutorial demonstrates a local open-source workflow for retrieval and generation quality, viewing results as a pandas dataframe and visual report, with optional platform upload. | Strong for notebook/report-driven quality checks and teams that want ML/LLM quality monitoring patterns; verify platform/self-host posture separately before governance scoring. | https://docs.evidentlyai.com/examples/LLM_rag_evals |
| W&B Weave | Primary row | Official RAG guide tracks retrieval steps, evaluates responses with an LLM judge, measures context precision, and uses Evaluation objects with datasets and scorers. | Strong for teams already using W&B or wanting managed tracing, datasets, model/version tracking, and eval UI; score deployment/governance separately from eval capability. | https://docs.wandb.ai/weave/tutorial-rag |
| LlamaIndex evaluators | Framework-fit caveat row | Official docs separate response evaluation and retrieval evaluation, including faithfulness, context relevancy, answer relevancy, semantic similarity, guideline adherence, synthetic question generation, and ranking metrics. | Best treated as primary only when the application is built on LlamaIndex; otherwise list as framework-native capability or integration note. | https://developers.llamaindex.ai/python/framework/module_guides/evaluating/ |
| Haystack evaluation | Framework-fit caveat row | Official docs cover pipeline/component evaluation, end-to-end vs component evaluation, model-based RAG evaluation, statistical retriever metrics, and Ragas/DeepEval evaluator integrations. | Best treated as primary only for Haystack projects; otherwise list as framework-native evaluation support with limited standalone observability. | https://docs.haystack.deepset.ai/docs/model-based-evaluation |
| OpenAI Evals / Evals API | Caveat or legacy row | Official OpenAI docs describe evals for testing model outputs and app behavior, but also state the Evals platform is being deprecated: read-only for existing users on 2026-10-31 and shutdown on 2026-11-30. | Do not score as a long-term primary RAG evaluation stack. Include as OpenAI-specific/legacy caveat and point teams toward current OpenAI evaluation surfaces only if the stack is already OpenAI-centric. | https://developers.openai.com/api/docs/guides/evals |

Open questions reduced:

- Framework-native tools: LlamaIndex and Haystack should be caveat/framework-fit rows unless the target production stack already uses them.
- OpenAI Evals: treat as caveat or legacy option because the official platform deprecation materially changes long-term suitability.
- Governance scoring still needs a separate verification pass for license, self-host/SaaS posture, RBAC, retention, and enterprise controls across primary candidates. Avoid inferring those fields from eval capability docs.
