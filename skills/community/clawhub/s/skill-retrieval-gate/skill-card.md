## Description: <br>
Decide whether to run `memory_search` before following another skill or workflow so the agent can reduce token usage without forcing retrieval on every task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otweihan](https://clawhub.ai/user/otweihan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide when local memory retrieval is warranted before another skill or workflow, build a compact `memory_search` query, limit retrieved context, and fall back when retrieval is weak or unnecessary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory may contain information that should not be reused in future tasks. <br>
Mitigation: Enable the skill only with memory sources whose contents are appropriate for relevant future reuse. <br>
Risk: Weak, stale, or noisy retrieval results can mislead the downstream workflow. <br>
Mitigation: Inspect only a few high-signal results, keep relevant facts, and fall back immediately when retrieval quality is low. <br>


## Reference(s): <br>
- [Decision Flow](references/decision-flow.md) <br>
- [Fallback Rules](references/fallback-rules.md) <br>
- [Query Construction](references/query-construction.md) <br>
- [Result Trimming](references/result-trimming.md) <br>
- [Skill Tiering](references/skill-tiering.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown guidance and decision criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bounded retrieval decision, compact query guidance, result trimming guidance, and fallback recommendation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
