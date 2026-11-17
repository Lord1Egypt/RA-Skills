## Description:

Sweeping Monk is a research and academic methodology advisor that helps with study design, critical reasoning, root-cause diagnosis, academic writing structure, and communication around stalled research problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, students, and developers use this skill to diagnose research design problems, select suitable methods, critique arguments, structure academic writing, and decide when to hand off literature search or citation checking to specialized skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write local telemetry files and maintain a persistent anonymous ID.

Mitigation: Review the telemetry behavior before installation and disable local recording if it is not acceptable for the deployment environment.

Risk: Usage-derived method labels may be uploaded to Tencent Cloud endpoints when cloud upload is enabled.

Mitigation: Review the configured endpoints and disable cloud upload in environments that prohibit outbound telemetry.

Risk: The skill can read profile or memory context to tailor research advice.

Mitigation: Avoid storing sensitive or unnecessary personal data in profile and memory context used with this skill.

Risk: A creator workflow can apply remotely supplied proposal text to local skill files.

Mitigation: Keep creator tokens outside the release package and manually review proposed changes before approving or applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j-levee/skills/sweeping-monk)
- [SKILL.md](SKILL.md)
- [Research Playbook](references/research-playbook.md)
- [Method Matrix](references/method-matrix.md)
- [Methodology Library Index](references/methodology-library/INDEX.md)
- [Signals Specification](references/signals.md)
- [Security Audit](references/security-audit.md)
- [Source Reference Cards](references/sources/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with optional lists, code blocks, shell commands, and configuration snippets when the user asks for implementation help]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory-first output; literature search and citation verification are delegated to recommended specialized skills.]

## Skill Version(s):

1.12.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
