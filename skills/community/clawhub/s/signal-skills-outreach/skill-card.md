## Description:

Turn a signal-scout prospect report into the right next action per prospect type — outreach sequences for Individuals, content/GTM briefs for Segments, BD pitch one-pagers for Companies. Use after signal-scout produces its report, or when you already have a qualified prospect list. Never sends anything automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orensegal](https://clawhub.ai/user/orensegal)

### License/Terms of Use:

MIT-0

## Use Case:

Founders, marketers, and business development teams use this skill to turn qualified prospect data into individualized outreach sequences, segment content briefs, and company pitches. It produces drafts for human review and does not send messages automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personalized drafts may rely on public prospect details that are stale or misrepresented.

Mitigation: Check each detail against its public source and review every draft before use; only reference information the prospect posted publicly and intentionally.

Risk: The skill reads prospect input and writes output files, while scan guidance says the host runtime's file permissions are not established.

Mitigation: Use only intended input and output paths, and check that the host runtime's file access fits the task.

## Reference(s):

- [Outreach Framework](references/outreach-framework.md)
- [Project homepage (metadata/clawdis)](https://github.com/OrenSegal/signal-skills)
- [ClawHub release page](https://clawhub.ai/orensegal/skills/signal-skills-outreach)

## Skill Output:

**Output Type(s):** [Text, JSON, HTML]

**Output Format:** [JSON package and optional HTML report with outreach drafts, content/GTM briefs, or BD pitches]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts require human review; messages are never sent automatically.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
