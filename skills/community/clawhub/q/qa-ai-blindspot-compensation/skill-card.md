## Description:

Reviews AI-generated test cases against six common blind-spot categories and proposes traceable additional test scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and developers use this Chinese-language checklist after reviewing AI-generated test cases to identify missing timing, concurrency, resource, state, data-consistency, and third-party integration scenarios. The skill suggests risk-ranked supplemental cases linked to requirements and original tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewing unintended local files may expose unrelated or sensitive information.

Mitigation: Limit file reads to the requirements and test cases selected for review.

Risk: The optional command to install a companion skill would add code from a separately sourced package.

Mitigation: Do not run the optional installation command unless its package and source have been independently trusted.

Risk: A checklist-based coverage report can overstate completeness when requirements or test inputs are missing.

Mitigation: State the coverage basis, mark missing modules as uncovered with reasons, and avoid claims of full or 100% coverage.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-ai-blindspot-compensation)
- [Six blind-spot categories and checklists](artifact/references/blindspot-details.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown blind-spot report with coverage and supplemental test-case tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supplemental cases include blind-spot category, risk level, and links to requirement and original test IDs; coverage is scoped to supplied materials.]

## Skill Version(s):

1.8.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
