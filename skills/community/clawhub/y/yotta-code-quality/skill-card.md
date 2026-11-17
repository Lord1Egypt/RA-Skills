## Description:

Reviews code, pull requests, tests, and architecture for maintainability, release safety, and first-paint user experience, then reports evidence-based findings and remedies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT

## Use Case:

Developers use the skill to review code, pull requests, tests, and architecture before merging or shipping. It produces scoped findings and a per-review deduction index; it reports only unless the user requests fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Upgrading can overwrite an existing skill folder and remove development or cache items.

Mitigation: Back up the folder before upgrading and install to one chosen target.

Risk: Optional repository rules or hooks may be mistaken for a complete security boundary.

Mitigation: Enable them deliberately and retain host protections; the example hook is not a complete security boundary.

## Reference(s):

- [Review workflow and scoring](artifact/references/common.md)
- [Pull request review guide](artifact/references/pr-review-guide.md)
- [Production code decay risks](artifact/references/decay-risks.md)
- [Test quality risks](artifact/references/test-decay-risks.md)
- [Release safety and first-paint UX checks](artifact/references/editorial-extensions.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review report with findings and a 0–100 per-review deduction index]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings use Symptom → Source → Consequence → Remedy; the score is a per-run deduction index, not an objective codebase grade.]

## Skill Version(s):

0.4.5 (source: frontmatter, package.json, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
