## Description:

SuperThink is a deep research and synthesis skill that scopes a topic, runs a multi-stage analysis pipeline, and produces deep-dive sections, a full synthesis document, and an executive brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inxan3](https://clawhub.ai/user/inxan3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use SuperThink for long-form research projects that need structured scoping, parallel deep dives, synthesis, and executive-ready summaries. It is best suited for runs where the user can provide an Anthropic API key, persistent storage, and acceptance of a long unattended workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can run unattended for 6-12 hours and incur Anthropic API costs.

Mitigation: Confirm scope, budget, API access, and acceptable unattended operation before starting a run.

Risk: The workflow writes persistent research outputs under /data/superthink/ and batch state under ./batch-jobs/.

Mitigation: Use storage locations with appropriate access controls and retention expectations for the research topic.

Risk: Completion may be delivered through configured notification channels.

Mitigation: Configure only approved webhook, Telegram, or log destinations, especially for sensitive topics.

Risk: DOCX generation depends on python-docx.

Mitigation: Pin python-docx before enabling DOCX output, or rely on the Markdown brief when DOCX output is not required.

## Reference(s):

- [SuperThink ClawHub Skill Page](https://clawhub.ai/inxan3/skills/superthink)
- [Publisher Profile: inxan3](https://clawhub.ai/user/inxan3)
- [Skill Definition](artifact/SKILL.md)
- [Batch Worker Implementation Spec](artifact/batch-worker-spec.md.md)
- [Markdown to DOCX Implementation Spec](artifact/md2docx-spec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON job and state files, shell commands, implementation guidance, and optional DOCX output generated from Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a master brief, 10-12 deep-dive section files, a 40000-60000 word synthesis document, an approximately 3000 word executive brief, and optional DOCX delivery.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
