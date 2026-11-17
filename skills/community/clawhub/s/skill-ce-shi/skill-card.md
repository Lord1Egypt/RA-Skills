## Description:

Evaluates Agent Skill documentation with the SkillsBench methodology, including trigger accuracy, documentation quality, structural completeness, and resource organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gloreasu](https://clawhub.ai/user/gloreasu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this agent skill to review OpenClaw Skill documentation, score quality dimensions, and generate improvement guidance before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled reference material describes dynamic command execution even though the skill presents itself as a static, read-only documentation evaluator.

Mitigation: Use it only for read-only documentation evaluation; do not run dynamic tests, copied commands, network access, API tokens, or file modifications unless explicitly requested in a sandboxed environment.

## Reference(s):

- [SkillsBench Website](https://www.skillsbench.ai/)
- [SkillsBench Paper](https://arxiv.org/abs/2602.12670)
- [SkillsBench GitHub](https://github.com/benchflow-ai/skillsbench)
- [Evaluation Guidelines](references/evaluation-guidelines.md)
- [Dynamic Testing Guide](references/dynamic-testing-guide.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown skill quality report with scores, findings, and improvement recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static documentation analysis; no code execution is required for the claimed primary workflow.]

## Skill Version(s):

3.0.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
