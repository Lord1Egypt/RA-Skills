## Description:

Skill Auditor guides security audits of newly added, installed, imported, updated, or written agent skills, covering integrity, prompt injection, data exfiltration, persistence, cross-skill writes, remote downloads, credentials, and related risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ambarion](https://clawhub.ai/user/ambarion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to inspect an agent skill bundle and produce security findings plus a final verdict before installation, update, or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad file-reading scope can expose local files beyond the submitted skill bundle.

Mitigation: Run the skill only against a sandboxed, read-only copy of the target bundle and disable out-of-root reads unless explicitly approved.

Risk: Remote fetching during audit can pull untrusted content into the review process.

Mitigation: Disable remote fetching by default and approve any static remote fetch per target before use.

Risk: Broad triggers and strict final-output rules can interfere with unrelated skill workflows or structured responses.

Mitigation: Narrow activation triggers to explicit skill-audit requests and keep final-output formatting scoped to audit reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ambarion/skills/skill-integrity-auditor)
- [ClawHub publisher profile](https://clawhub.ai/user/ambarion)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown audit report with structured findings and a final Chinese verdict line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output language follows the triggering message for the report; the final verdict line is always Chinese.]

## Skill Version(s):

0.1.12 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
