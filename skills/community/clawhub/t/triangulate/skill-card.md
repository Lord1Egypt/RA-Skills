## Description:

Triangulate orchestrates explicit three-perspective consensus analysis with task decomposition, parallel agent execution, review, and Markdown report rendering for complex decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xincen0725](https://clawhub.ai/user/xincen0725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced agent users use Triangulate when they explicitly request three-perspective analysis for architecture choices, diagnostics, research, planning, or other complex decisions that benefit from independent review and consensus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can spawn child agents for analysis, which may expand scope, cost, or operational impact if used on high-risk requests.

Mitigation: Install only where child-agent execution is expected, and require separate authorization for high-risk operational tasks.

Risk: Checkpoint and report files may contain sensitive task context and can be affected by weak file-path controls.

Mitigation: Use trusted checkpoint names, keep checkpoint storage local and access-controlled, and avoid passing sensitive data unless retention is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xincen0725/skills/triangulate)
- [Publisher profile](https://clawhub.ai/user/xincen0725)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON decision records, and agent task instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include consensus conclusions, disagreement notes, uncertainty statements, execution statistics, and checkpoint-backed workflow state.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
