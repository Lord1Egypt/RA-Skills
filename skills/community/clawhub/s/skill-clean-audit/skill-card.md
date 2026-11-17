## Description:

Guides agents in auditing user-selected Python code for comprehension cost and change risk, producing a file-and-line-evidenced report and checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elisabeth15501](https://clawhub.ai/user/elisabeth15501)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess readability and maintainability of their Python scripts or skill code. The agent reports evidence-backed red, amber, and green findings without modifying the reviewed source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit report or checklist files may clutter the workspace or overwrite an existing checklist.

Mitigation: Review planned output paths before running and inspect or remove generated artifacts as needed.

Risk: Subjective audit ratings or metric hints may be mistaken for definitive code quality judgments.

Mitigation: Check file-and-line evidence and confirm findings before making code changes; use metric hints only to guide review.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/elisabeth15501/skills/skill-clean-audit)
- [Audit FAQ (English)](references/faq.en.md)
- [Example audit (English)](references/clean_code_audit_sample.en.md)
- [Code-smell crosswalk](references/smells_crosswalk.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML, Guidance]

**Output Format:** [Markdown audit report and reusable HTML checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite file and line; grades use red, amber, and green. Reviewed source remains unchanged.]

## Skill Version(s):

1.4.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
