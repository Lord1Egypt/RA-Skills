# RAG and LLM Application Evaluation Tooling Matrix

## Executive summary

The strongest production choices depend less on a single universal "best" evaluator and more on the team's operating model:

- **Managed experiment and governance workflow:** LangSmith is the clearest fit for LangChain-heavy teams that want datasets, experiment runs, traces, and enterprise deployment options in one platform.
- **Open-source trace-first quality loop:** Langfuse and Phoenix are strong when self-hosting, data control, and trace-level evaluation matter.
- **Lifecycle platform fit:** MLflow GenAI is attractive for teams already standardizing on MLflow and wanting evaluation, feedback, tracing, and self-hosted governance in one lifecycle layer.
- **CI/regression gate:** DeepEval / Confident AI and Promptfoo are strong options for repeatable test suites, with Promptfoo being lighter and more config-oriented.
- **RAG-specific metric layer:** Ragas and TruLens are useful evaluator layers, but they usually need to be paired with experiment tracking, trace collection, or governance tooling.

## Shortlist table

| Tool family | Tier | Eval fit | Operational fit | Best use | Main caveat |
| --- | --- | --- | --- | --- | --- |
| LangSmith | Adopt/shortlist | 91 | 92 | Best default shortlist item for LangChain-heavy teams that need datasets, experiment runs, traces, enterprise deployment options, and governance controls. | Strongest fit when the application stack already uses LangChain or the team accepts a managed/commercial control plane. |
| Langfuse | Adopt/shortlist | 81 | 100 | Strong for trace-first RAG quality loops, production scoring, and teams that want self-hosting with documented RBAC and retention controls. | Separate OSS/core features from edition-specific enterprise controls before procurement. |
| W&B Weave | Adopt/shortlist | 85 | 84 | Strong for teams already using W&B and wanting traced RAG steps, datasets, scorers, and evaluation UI in the same ecosystem. | Self-managed Weave requires an enterprise W&B Platform deployment, Kubernetes, ClickHouse, S3-compatible storage, and a Weave-enabled license. |
| Phoenix | Strong candidate | 81 | 92 | Strong for teams that want self-hosted tracing, RAG evaluation, datasets, and privacy controls around evaluation data. | Managed enterprise controls should be verified separately from self-hosted Phoenix OSS capabilities. |
| MLflow GenAI | Strong candidate | 80 | 92 | Strong when the organization already standardizes on MLflow and wants GenAI evals, human feedback, tracing, and self-hosted lifecycle governance. | RAG-specific ergonomics may be less focused than dedicated RAG eval libraries or observability platforms. |
| Opik | Strong candidate | 88 | 72 | Good for teams that want tracing, datasets, experiments, online evaluation, and CI hooks in one evaluation family. | Public research here verified broad capabilities from the official repository; deeper enterprise controls need vendor-doc confirmation. |
| DeepEval / Confident AI | Strong candidate | 76 | 80 | Strong for CI/regression tests and unit-test-style LLM app evaluation, with team reporting and governance on the Confident AI platform side. | Do not treat enterprise SSO/RBAC/audit/retention as features of the local OSS runner; they are platform-side controls. |
| Ragas | Strong candidate | 79 | 60 | Best when the team needs RAG-specific metrics, test set generation, and framework integrations, and can pair the library with separate experiment tracking. | Excellent evaluator library, not a complete production governance or observability platform by itself. |
| Giskard OSS / Giskard Hub | Strong candidate | 70 | 80 | Good for test-suite-driven RAG validation, out-of-scope handling, multi-turn checks, and organizations that also need AI risk/security workflows. | Enterprise controls are Hub-side; verify the OSS workflow against the team's desired CI and observability shape. |
| Promptfoo | Situational | 64 | 72 | Strong for lightweight local/private evals, prompt/provider comparisons, and CI checks where the team owns the evaluation configuration. | The OSS runner is not a sandbox for untrusted eval configs or code-executing fields; isolate execution for adversarial packs. |
| TruLens | Situational | 68 | 56 | Useful when the team wants explicit RAG Triad-style scoring around context relevance, groundedness, and answer relevance. | Treat as a strong evaluator/concept layer unless the broader platform requirements are already solved elsewhere. |
| LlamaIndex evaluators | Situational | 68 | 48 | Use as a primary option only when the production RAG app is built on LlamaIndex; otherwise treat as framework-native support or a metric source. | Not a standalone evaluation platform for teams outside the LlamaIndex ecosystem. |
| Haystack evaluation | Situational | 64 | 48 | Use as a primary option only for Haystack-based RAG pipelines; otherwise treat as framework-native evaluation support. | Strongest inside Haystack pipelines; not a standalone observability or governance platform. |
| Evidently OSS / Platform | Situational | 57 | 52 | Good for notebook/report-driven RAG quality checks and teams that want dataframe outputs, visual reports, and ML quality monitoring patterns. | Managed SaaS availability has conflicting official documentation; require vendor confirmation before scoring it as available. |
| OpenAI Evals / Evals API | Avoid/legacy | 46 | 36 | Do not choose as a long-term primary RAG evaluation stack; keep only as a legacy/OpenAI-specific caveat where already in use. | Official docs state Evals platform read-only for existing users on 2026-10-31 and shutdown on 2026-11-30. |

## Scoring model

The workbook uses two visible scoring layers:

- **Evaluation Fit Score:** RAG-specific metrics, CI/regression support, datasets/testsets, observability/tracing, integration fit, and public evidence maturity.
- **Operational Fit Score:** deployment/data-control posture, access control/retention/audit/governance, and public evidence maturity.

The default weighted criteria are:

| Criterion | Weight | Layer | Notes |
| --- | --- | --- | --- |
| RAG-specific metrics and evaluators | 20 | Evaluation | Does the tool directly evaluate retrieval quality, groundedness, answer quality, and related RAG failure modes? |
| Repeatable regression and CI workflow | 15 | Evaluation | How directly can teams run repeatable eval suites in CI or automated regression gates? |
| Dataset/testset and experiment workflow | 15 | Evaluation | How well does the tool support datasets, generated test sets, experiments, examples, or runs? |
| Observability/tracing and production feedback loop | 15 | Evaluation | Can scores be attached to traces/spans or production feedback loops? |
| Integration fit with common RAG stacks | 10 | Evaluation | How cleanly does it integrate with common RAG frameworks and app stacks? |
| Deployment/data-control posture | 10 | Operational | Is the tool local, self-hostable, hybrid, or otherwise usable under data-control constraints? |
| Access control, retention, audit, and enterprise governance | 10 | Operational | Are RBAC, retention, audit, SSO, or equivalent controls publicly documented? |
| Public evidence maturity | 5 | Both | How strong and specific is the public evidence used for this row? |

## Important caveats

| Topic | Caveat | Decision impact |
| --- | --- | --- |
| Evidently managed SaaS | Current official docs conflict: some pages say Cloud is no longer available as SaaS, while Cloud v2 docs describe SaaS onboarding. Treat as vendor-confirmation required. | Blocking for teams that require managed SaaS. |
| OpenAI Evals | Official OpenAI docs mark the Evals platform as deprecated, with read-only status on 2026-10-31 and shutdown on 2026-11-30. | Do not select as a long-term primary stack. |
| Framework-native rows | LlamaIndex and Haystack evaluators are valuable when the app already uses those frameworks, but they are not standalone observability/governance platforms. | Use as framework support, not a default cross-stack choice. |
| Commercial governance claims | Some enterprise controls are documented on vendor pages rather than deep implementation docs. | Use evidence confidence and procurement/security review before adoption. |
| Promptfoo execution model | Promptfoo OSS is a local eval runner, not a sandbox for untrusted configs or code-executing eval fields. | Run untrusted eval packs in isolated CI/runtime environments. |
| Scores are fit scores, not benchmark results | The matrix scores publicly documented capabilities and production fit; it does not benchmark model quality or runtime performance. | Run a project-specific proof of concept before final tool selection. |

## Recommended adoption path

1. Pick one trace/observability-backed option and one CI/regression option for a two-tool proof of concept.
2. Run both against the same representative RAG failures: irrelevant retrieval, unsupported answer, stale source, out-of-scope user query, and multi-turn context drift.
3. Require evidence capture: prompt, retrieved context, answer, expected behavior, scores, source links, and reviewer notes.
4. Before procurement, validate retention, RBAC, SSO, audit logging, data residency, and self-hosting/SaaS status directly with current vendor documentation or security review.

## Evidence policy

This package uses public official documentation, GitHub repositories, release/vendor documentation, and vendor docs. It does not include confidential identifiers, credentials, or contact data.
