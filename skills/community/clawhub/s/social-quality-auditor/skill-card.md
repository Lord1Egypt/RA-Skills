## Description:

Audits a social asset batch before publishing or assesses a channel program's maturity using ECHO checks for channel truth, claims, disclosures, engagement manipulation, UGC rights, and measurement denominators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Social, marketing, and governance teams use this skill to review one pre-publish asset package or one channel portfolio/window. It reports audit status, verdict, scoring state, unknown inputs, verified controls, and concrete fixes without publishing content or changing registries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires social assets, governance records, permissions evidence, and analytics exports to complete an audit.

Mitigation: Provide only the specific evidence needed for the selected asset gate or program-maturity profile, and treat missing private evidence as Unknown rather than failure.

Risk: An audit result could be mistaken for permission to publish or mutate channel records.

Mitigation: Require separate explicit approval before publishing, unpausing queues, writing audit artifacts, or changing canonical registries.

## Reference(s):

- [Standalone auditor runtime](artifact/references/auditor-runtime.md)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/social-quality-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report with structured status, verdict, score state, unknowns, findings, and fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a permissioned audit artifact only after explicit user authorization; otherwise it returns the audit result in conversation.]

## Skill Version(s):

19.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
