## Description:

Ingest Tencent Meeting recordings, minutes, and transcripts into the Research KB by delegating platform fetching to tencent-meeting-skill, then letting OpenClaw generate structured meeting wiki pages and related KB updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research operations teams use this skill to ingest Tencent Meeting recordings, minutes, and transcripts into a Research KB. It helps an agent prepare meeting source context, create Markdown drafts and compact manifests, validate them, and apply the resulting wiki pages and KB updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task payloads can redirect Gitea uploads carrying the bot token and meeting content.

Mitigation: Install only where backend task payloads are trusted or validated, and require the Gitea endpoint to come from administrator-controlled configuration or an allowlist.

Risk: A broad Gitea bot token could expose or modify repositories beyond the intended KB.

Mitigation: Use a bot token limited to the intended Team KB repository and the minimum permissions needed for KB updates.

Risk: Full meeting minutes and transcripts may be archived into the repository or shared work area.

Mitigation: Keep the shared work directory private, confirm repository access controls, and make users aware that meeting content can be persisted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myd2002/skills/tencent-meeting-ingest)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown drafts, compact JSON manifests, and backend result JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task-scoped draft and manifest paths; meeting source material may be archived as files.]

## Skill Version(s):

1.0.14 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
