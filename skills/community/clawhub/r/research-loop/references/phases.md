# Research Loop Phases

All phases are small and inspectable. Python helper phases write deterministic artifacts; agent-native phases perform judgment and code generation.

| Phase | Owner | Output |
| --- | --- | --- |
| `source_intake` | Python + agent | source snapshot and inventory |
| `mempalace_context` | Python | current-head memory pack |
| `council_knowledge` | Python | expert council route |
| `expert_forum_coverage` | Python | coverage score and expansion queue |
| `literature_refresh` | OpenAlex + native web search | papers and web evidence |
| `knowledge_publish` | Python | cycle knowledge base |
| `advisor_design` | agent | advisor manifest, protocol hygiene findings, innovation-frontier reading, and action backlog |
| `execution_packet` | Python | one selected micro-step, preferring unresolved hygiene gates while preserving an exploration lane |
| `executor_run` | agent | runnable source changes, protocol hygiene notes, innovation-frontier notes, and executor manifest |
| `advisor_reflection` | Python | post-execution constraints and evidence-level demotions |
| `openspace_retrospective` | Python | loop improvement notes |
| `next_cycle_handoff` | Python | next-cycle handoff |
| `star_office_status` | Python | local dashboard status |
| `overwatcher_check` | Python | observe-only workflow health report |
| `github_publish` | Python | target repo delivery |

Do not rely on Ollama native web search. If fresh web evidence is needed inside an agent-native phase, use native web search and pass short, attributed snippets into the relevant helper stage.

Before choosing a new scientific claim or venue-packaging step, run the protocol hygiene rubric in [protocol hygiene](protocol-hygiene.md). Cleanup of positioning drift, deterministic artifact dirtiness, narrow CI gates, misleading result/input-quality names, and weak contamination checks takes priority over adding new claims.

Before choosing a new micro-step, also run the innovation frontier rubric in [innovation frontier](innovation-frontier.md). Current assets should bound supported claims, but they should not trap the research design or prevent bounded exploration probes.
