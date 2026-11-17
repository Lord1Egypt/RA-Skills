## Description:

Skill Security Scanner helps agents scan ClawHub, GitHub, and local skills for security risks in JavaScript, TypeScript, Python, and Shell files, then report scored findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torchesfrms](https://clawhub.ai/user/torchesfrms)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan skill packages or directories, inspect scored findings, and decide whether additional semantic review is needed before installation or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted scan targets may exploit unsafe command argument handling or archive extraction behavior.

Mitigation: Run scans in an isolated workspace or container and avoid passing untrusted URLs or paths through the Node wrapper.

Risk: Whitelist trust logic and generated semantic-analysis prompts can make pass/fail results unreliable.

Mitigation: Treat scanner results as advisory, review findings manually, and avoid high-stakes decisions until the documented scanner issues are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/torchesfrms/skills/skill-sec-scan)
- [Detection Rules Reference](references/rules.md)
- [Dangerous Commands Reference](references/dangerous-commands.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown security reports with optional JSON scan output and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores findings from 0-100 and may include follow-up semantic analysis prompts after user confirmation.]

## Skill Version(s):

4.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
