# Figure Taxonomy Routing

> **v1.10 fallback boundary:** This is a generic fallback scaffold. It does not count as the class-specific taxonomy or pattern library required for a locked generated specialized skill. Use it for initial routing, bootstrapping, or explicit fast-track only.


Use this routing reference to convert vague needs into specific figure types. Start from the reader question, not from style.

## Routing order

1. Reader question
2. Logical gap type
3. Narrative role / figure function
4. Evidence type
5. Paper slot
6. Visual rhetoric
7. Visual grammar / layout
8. Editing lever
9. Style family

## Reader question axis

| Reader question | Use when | Likely figure types |
|---|---|---|
| why_is_this_problem_real | reader does not buy the problem | motivation contrast board, failure-mode figure |
| can_i_see_the_core_case | one example carries the intuition | toy case storyboard, case walkthrough |
| how_does_the_idea_become_a_model | idea-to-formal jump is abrupt | idea-to-model bridge, mechanism figure |
| what_are_the_parts_and_data_flow | components or system map are unclear | method overview, architecture, pipeline, system figure |
| what_happens_over_time | process or loop matters | process loop, timeline, training/inference figure |
| what_evidence_should_i_believe | claim needs evidence support | evidence comparison, ablation, result summary |
| what_is_the_proof_intuition | theorem needs visual interpretation | theory/proof intuition figure |
| what_is_the_main_message | paper needs a memorable overview | graphical abstract, intro hero, overview map |
| how_is_the_dataset_or_benchmark_made | data/task/protocol is a contribution | dataset/benchmark/protocol figure |
| what_design_space_are_we_mapping | categories/tradeoffs/taxonomy matter | taxonomy, design-space, matrix figure |
| what_should_reviewers_stop_worrying_about | rebuttal or risk mitigation is needed | reviewer evidence board, limitation/failure analysis |

## Logical gap axis

- `phenomenon_to_problem`: observed phenomenon -> defined problem.
- `problem_to_hypothesis`: problem -> core hypothesis.
- `hypothesis_to_mechanism`: intuition -> mechanism.
- `mechanism_to_objective`: mechanism -> variables/loss/constraints.
- `objective_to_algorithm`: objective -> procedure.
- `algorithm_to_system`: local step -> whole system/workflow.
- `system_to_evidence`: method -> believable results.
- `evidence_to_claim`: metrics/cases -> conclusion.
- `theory_to_intuition`: theorem/bound -> visual intuition.
- `taxonomy_to_choice`: design space -> recommended method/configuration.

## Narrative role axis

- motivation/problem-gap
- overview/graphical abstract
- inspiration-source/real-world-to-model bridge
- toy example/case evidence
- method overview/architecture
- idea-to-model/mechanism bridge
- training/inference/process loop
- data/benchmark construction
- taxonomy/design-space map
- result/ablation/evidence panel
- theory/proof intuition
- limitation/failure analysis
- rebuttal evidence board
- slide summary

## Visual rhetoric axis

- contrast before/after
- progressive stage reveal
- causal chain
- decompose then recompose
- zoom in / zoom out
- mapping alignment
- feedback loop or cycle
- search space / design space
- storyboard walkthrough
- evidence compression
- direct exposition

## Visual grammar axis

- block-arrow pipeline
- input-output triptych
- graph/network schematic
- sequence/timeline
- image grid / qualitative panel
- matrix / heatmap / chart hybrid
- equation-diagram hybrid
- trajectory/environment scene
- wide multi-panel landscape
- vertical stack
- tile/card/mosaic board
- central-core-with-callouts
- minimal line-art / theory schematic

## Paper slot guidance

| Slot | Best figure roles | Avoid |
|---|---|---|
| intro / first chapter | motivation, hero overview, inspiration bridge, case teaser | dense architecture, too many metrics |
| method | framework, architecture, mechanism, algorithm/process, idea-to-model bridge | broad decoration without technical anchors |
| results | evidence comparison, ablation, qualitative examples, mechanism probes | full method re-explanation |
| analysis/discussion | limitation, failure analysis, taxonomy, interpretation, future directions | polished hero without evidence |
| appendix | dense implementation, extended walkthrough, full taxonomy, protocol detail | oversized simplified hero |
| rebuttal | one-risk evidence board, compact mechanism proof | new broad claims or confusing visuals |
| slides | simplified story version, fewer panels, stronger labels | appendix-density labels |

## Routing output template

```markdown
### 图类型路由
| Axis | Decision | Rationale |
|---|---|---|
| Reader question | ... | ... |
| Logical gap | ... | ... |
| Narrative role | ... | ... |
| Paper slot | ... | ... |
| Visual rhetoric | ... | ... |
| Visual grammar | ... | ... |
| Evidence type | ... | ... |
| Density/layout | ... | ... |
| Editing lever | ... | ... |

**默认推荐图类型：**...
```

## v1.7 routing rule

In the two-layer workflow, taxonomy routing has two meanings:

1. **Builder-layer routing:** use literature-derived taxonomy to define what the specialized figure-making skill should cover.
2. **Production-layer routing:** use the generated specialized skill to route a concrete target-paper need to a specific figure subtype, layout family, and prompt strategy.

When working on B1-B9, do not jump to concrete figure rendering. When working on P1-P9, cite or reference the active specialized skill in the state footer.
