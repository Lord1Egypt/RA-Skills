## Description:

Skillsmith-JOJO helps developers create, test, review, optimize, package, and publish AI agent skills using templates, validation scripts, security checks, and token analysis guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skillforge-jojo](https://clawhub.ai/user/skillforge-jojo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to scaffold new ClawHub/OpenClaw skills, improve existing SKILL.md files, run structure and syntax checks, perform advisory security review, analyze token footprint, and prepare releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised safety and validation checks may not enforce every safeguard.

Mitigation: Treat validation and security-check results as advisory, and manually review generated skills, scripts, and release artifacts before deployment.

Risk: Git automation can stage and commit broad changes when broad staging is requested.

Mitigation: Inspect repository status and diffs before running the Git helper, and avoid broad staging unless it is intentional.

Risk: Setup examples can lead to unpinned or broad dependency installation.

Mitigation: Use isolated environments and pinned dependencies when following setup examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skillforge-jojo/skills/skillsmith-jojo)
- [Publisher profile](https://clawhub.ai/user/skillforge-jojo)
- [Skill design best practices](references/best-practices.md)
- [ClawHub publishing guide](references/publishing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and shell command snippets; helper scripts may emit terminal text or JSON reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 for the bundled validation and analysis scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
