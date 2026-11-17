## Description:

SDD - Scenario-Driven Detection helps agents infer, verify, and report logic defects in websites, UI/API projects, and application workflows, including suggested or automatic fixes when source code is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kimky1122](https://clawhub.ai/user/kimky1122)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use SDD to explore application flows, infer expected behavior, verify logic-level defects, and produce fixes or fix recommendations. It is intended for URL-based crawling, source-code UI/API logic checks, and scenario testing requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live application crawling and UI/API exercise may affect production data or authenticated user state.

Mitigation: Run against staging or test data first, require an explicit target and read-only mode, and approve mutation testing before execution.

Risk: Automatic fixes and commits may introduce incorrect code changes.

Mitigation: Require manual review before applying fixes or commits, and run the existing test suite before accepting changes.

Risk: Reports may include sensitive application structure, DOM details, or behavior observations.

Mitigation: Review generated reports before external sharing and avoid providing production credentials unless the scope is approved.

## Reference(s):

- [Inference rules](references/inference-rules.md)
- [ClawHub skill release page](https://clawhub.ai/kimky1122/skills/sdd)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports, code patches, shell commands, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scenario maps, pass/fail summaries, defect details, fix history, and manual review tags.]

## Skill Version(s):

1.0.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
