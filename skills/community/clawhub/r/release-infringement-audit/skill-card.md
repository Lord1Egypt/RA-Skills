## Description:

Screens projects before public release for license conflicts, copied code, unlicensed assets, trademark concerns, and exposed secrets, then produces a prioritized audit report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[y16689540962-cloud](https://clawhub.ai/user/y16689540962-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release managers use this skill to triage potential copyright, licensing, trademark, asset, and secret-exposure issues before publishing a project to npm, ClawHub, or GitHub. Its findings are an initial screen, not legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auditing a repository can expose local configuration and files containing secrets to the audit process.

Mitigation: Run the audit only against repositories you intend to inspect and review the report before sharing it.

Risk: Enabling online license lookup sends dependency names and versions to the npm registry.

Mitigation: Keep the default offline mode unless you accept that disclosure; enable --online only when needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/y16689540962-cloud/skills/release-infringement-audit)
- [Verdict basis](references/verdict-basis.md)
- [SPDX License List](https://spdx.org/licenses/)
- [FSF GPL FAQ](https://www.gnu.org/licenses/gpl-faq.en.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Structured Markdown or JSON audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are graded BLOCK, WARN, or INFO with evidence and recommended actions; automated screening is not legal advice.]

## Skill Version(s):

1.0.5 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
