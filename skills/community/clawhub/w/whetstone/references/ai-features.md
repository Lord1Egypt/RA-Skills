# AI boundaries

Use when a feature sends data to a model, retrieves private content or lets model output influence actions. A local prototype with synthetic data needs less process than an agent with customer data and write credentials.

## Constrain authority outside the model

Map what the model can read, which input is untrusted and which effects its tools can cause. Retrieved text, email, tool results and model-generated arguments do not grant permission. Prompt wording or an injection detector alone is not an access-control boundary.

Enforce identity, allowed operations, destinations and parameter validation in application code. Scope credentials narrowly. For consequential actions, use the product's approved human confirmation or deterministic limits tied to the exact action; a model cannot approve its own refund or data export. Apply budgets, deadlines and bounded tool steps. An ambiguous write result needs outcome checking before a retry. Record every tool call the agent proposes or makes, with its inputs, the approval or limit that allowed or blocked it, and the outcome, so actions can be investigated and reversed. Redact that record and bound its retention.

Treat generated output as untrusted: validate schemas and business constraints, encode rendered content, and do not execute generated SQL, shell code or tool names directly. A structurally valid response can still be unauthorized or wrong. Constrain external image/link fetching in rendered output: a generated URL can leak data without an explicit tool call. Keep provenance and trust labels when persisting memories; retrieved instructions must not become trusted policy in a later session.

For MCP, verify server identity, intended scopes and token audience. Reject token passthrough; a session/state handle does not replace authentication and authorization. Server metadata cannot authorize a new destination. A local MCP server executes code with its process privileges: review its origin, launch arguments and access. Confirm current protocol requirements for the actual deployment.

## Keep retrieval within the caller's access

Enforce document permissions at query time, before content reaches the model: pass the caller's current user and group identities into the search filter on every request, and apply the same scope to snippets, caches and citations. Filtering only the final answer is too late, and a prompt instruction is not access control. Preserve document identity, version and provenance; propagate deletion and permission changes to indexes and caches.

Test two users with different access. Check retrieval separately from answer quality: the correct document may not be found, or the answer may misrepresent it. Define what to do when evidence is absent, stale or contradictory. A citation must support the claim, not merely name a related page.

## Preserve retrieval meaning

Keep headings, identifiers and source/version metadata with chunks so retrieved excerpts remain interpretable. Evaluate exact names and codes; semantic similarity alone may miss them. Add keyword/hybrid retrieval or reranking only when measured retrieval failures justify it.

Query and indexed embeddings must share a compatible model and dimensions. Treat embedding, chunking or schema changes as index migrations: build and evaluate an incompatible replacement before switching traffic, and retain the recovery route.

## Verify the feature, not the prompt's appearance

Build a small evaluation set from the real task, with expected outcomes and cases for unavailable evidence, denied access, malicious retrieved instructions and failed tools. Use the models/configurations actually deployed. Include the permission and index-transition cases above when those boundaries change, preserve a holdout where feasible, and add each production failure to the set.

For agents that act over several steps, evaluate the whole task, including interrupted or failed tool calls. Check resulting state and unintended effects, not just the final reply or a prescribed tool sequence.

Measure retrieval against labeled relevant documents, separately from answer grounding and unsupported claims; a fluent answer does not prove that retrieval found the right evidence. Name the metrics and thresholds before tuning. For retrieval-backed answers:

| Metric | Question it answers |
|---|---|
| Recall at k | Is a labeled relevant document among the top k results? |
| Groundedness | Is every claim in the answer supported by the retrieved text? |
| Answer relevance | Does the answer address the question that was asked? |
| Correct refusal rate | Does it decline when evidence is missing or the caller lacks access? |
| Restricted-content leaks | Did any answer, snippet or citation expose a document the caller cannot read? The target is zero. |

Prefer code-based checks such as exact match, schema validation and citation presence. Calibrate automated graders against human-reviewed cases before trusting them, and inspect disagreements.

Rerun the set whenever the prompt, model or model version, retrieval settings, chunking or tools change, and compare the results with the current behavior on the same cases and starting state. A drop below a threshold is a failing check. Record agent, model/configuration, dataset and grader/rubric versions. Report results by relevant scenario or user group alongside the aggregate; measure cost/latency where relevant. Repeat trials when variability could change the decision, distinguishing agent failures from grader or environment variation. Passing a few cases is a smoke check, not proof of reliability across users or models. The optional [AI evaluation plan](../templates/ai-eval-plan.md) records the set, metrics, thresholds, versions and triggers.

## Data sent to model providers

Check provider retention and processing location against the project's requirements before sending private data. Avoid raw prompts/documents in telemetry by default.

## Sources

- [Anthropic: evaluating AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)
- [OWASP LLM Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [MCP security best practices](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices)
- [Microsoft: vector index compatibility](https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-create-index)
- [Microsoft: hybrid retrieval](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview)
- [Microsoft: document-level access in search](https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview)
- [OWASP Top 10 for LLM applications: vector and embedding weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/)
- [Introduction to Information Retrieval: evaluating ranked results](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html)
- [TruLens: the RAG triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/)
