## Description:

Audits what changed between an installed skill and a pending update, flagging new tool requests and risk changes before approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ordo-tech](https://clawhub.ai/user/ordo-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill before applying ClawHub skill updates to compare the installed skill with the pending version and receive a concise update-risk verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the installed SKILL.md for the audited skill and fetches the comparison copy from ClawHub.

Mitigation: Use it only for intended skill-update audits and review the returned report before approving any update.

Risk: Generated reports may include a Gumroad promotional link that is not security evidence.

Mitigation: Treat promotional links as optional advertising and base update decisions on the audit findings and trusted release evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ordo-tech/skills/skill-diff-auditor)
- [ClawHub publisher profile](https://clawhub.ai/user/ordo-tech)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with a verdict, new-tool summary, and risk profile]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free version focuses on new tools requested, overall risk direction, and a plain-English verdict.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
