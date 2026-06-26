## Description: <br>
Reduces unnecessary token usage by guiding concise replies, trimmed logs and tool outputs, and current-state token accounting practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinoslug](https://clawhub.ai/user/sinoslug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and assistant operators use this skill to keep responses concise, trim logs and tool outputs before reasoning, and apply the current token accounting flow without adding speculative optimizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The token statistics command references a local token-show.py script that is not packaged in the reviewed artifact. <br>
Mitigation: Inspect the local token-show.py script in the deployment environment before relying on its statistics. <br>
Risk: Overly aggressive trimming of replies, logs, or tool outputs could remove context needed to preserve answer quality. <br>
Mitigation: Keep the skill's current-state guardrails: answer concisely, but retain necessary evidence and avoid unimplemented optimization tactics. <br>


## Reference(s): <br>
- [Current Token Optimization Spec](references/current-spec.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sinoslug/token-optimization-sinoslug) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with optional inline shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Current-state only; avoids speculative or not-yet-implemented tactics.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
