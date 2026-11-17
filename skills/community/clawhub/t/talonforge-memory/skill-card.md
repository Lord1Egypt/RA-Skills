## Description:

Sets up a bilingual three-layer AI memory system with long-term MEMORY.md, daily notes, and nightly fact extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperzinou](https://clawhub.ai/user/casperzinou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to set up a local memory workflow that records durable user facts, daily events, decisions, and preferences across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A recurring unattended job may review conversations and write long-term notes beyond the user's intended scope.

Mitigation: Enable the cron job only after confirming the target files, timezone, review scope, and how to inspect or remove the job.

Risk: Durable memory files may retain sensitive, outdated, or incorrect facts without clear deletion or correction guidance.

Mitigation: Provide a regular review process for MEMORY.md and memory/ notes, including how to correct, supersede, or delete stored facts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/casperzinou/skills/talonforge-memory)
- [TalonForge Homepage](https://talonforge.xyz)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with file templates and an OpenClaw cron command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory file templates and configuration guidance for a recurring nightly extraction job.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
