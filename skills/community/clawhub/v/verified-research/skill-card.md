## Description:

Provides a multi-source research workflow that breaks down complex questions, prioritizes high-trust sources, cross-checks claims, and produces structured research reports with a three-day cache.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashanzzz](https://clawhub.ai/user/ashanzzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users can use this skill to run deeper web research, preserve intermediate evidence cards, and produce a structured report for fact-heavy, comparative, exploratory, or verification tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research summaries and learning logs may persist sensitive topics or conclusions outside the immediate report workflow.

Mitigation: Use the skill only for non-sensitive research unless MEMORY.md archival and learning-log writes are removed or made explicit opt-in.

Risk: Cleanup behavior deletes cached research directories and relies on path handling around /tmp/deep-research-cache.

Mitigation: Run cleanup only in a sandbox or least-privileged account, and validate cache paths before enabling scheduled cleanup.

Risk: The artifact describes possible self-modification of SKILL.md when methodology issues are found.

Mitigation: Require human review before accepting any skill-file changes, or disable self-modification for managed deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ashanzzz/skills/verified-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown research reports with evidence-card files, manifest JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates temporary research caches under /tmp/deep-research-cache and may archive summaries to MEMORY.md after three days.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
