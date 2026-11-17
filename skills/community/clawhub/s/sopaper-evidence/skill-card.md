## Description:

Evidence-first research workflow for evidence discovery, source verification, and citation grounding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheepxux](https://clawhub.ai/user/sheepxux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research teams use this skill to find and verify sources, map claims to evidence, identify evidence gaps, and prepare source-grounded research briefs, related work, experiment plans, and paper outlines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send research topics and queries to external search services and fetch public web pages.

Mitigation: Avoid confidential topics, private project details, and unreviewed URL lists unless external disclosure is acceptable.

Risk: Fetched source notes and automatic evidence-upgrade logic may overstate source reliability if accepted without review.

Mitigation: Require human review before using verified evidence labels, comparative claims, or quantitative results in downstream research writing.

Risk: External fetching may follow redirects or retrieve unexpectedly large responses.

Mitigation: Use curated public URLs, keep fetch timeouts and response-size controls in place, and review redirect behavior before broad deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sheepxux/skills/sopaper-evidence)
- [SoPaper-Evidence Repository](https://github.com/sheepxux/SoPaper-Evidence)
- [Source Priority](references/source-priority.md)
- [Input Schemas](references/input-schemas.md)
- [Evidence Schema](references/evidence-schema.md)
- [Prior Work Search Playbook](references/prior-work-search-playbook.md)
- [Claim Audit Rules](references/claim-audit-rules.md)
- [Evidence Gap Triage](references/evidence-gap-triage.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, CSV, and shell command guidance depending on the workflow step]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs emphasize evidence briefs, source lists, claim-to-evidence maps, gap reports, fairness reviews, and draft-safe writing notes.]

## Skill Version(s):

1.1.1 (source: server release evidence and artifact SKILL.md version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
