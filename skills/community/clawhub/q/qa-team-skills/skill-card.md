## Description:

A Chinese-language QA assistant for requirements reviews, test-case design, agent testing, defect analysis, reports, team workflows, and exploratory testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT

## Use Case:

QA engineers and test managers use this skill to review requirements, design and assess tests, analyze defects, prepare reports, and reuse local testing history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local testing history may retain sensitive input or customer data.

Mitigation: Do not provide real credentials, personal data, payment identifiers, or sensitive screenshots; review and confirm memory writes and cleanup.

Risk: Generated test cases, security-test payloads, and reports may be unsafe or inaccurate if used without review.

Mitigation: Review payloads before running them, check critical cases and report figures against test systems, and keep final QA decisions with a human reviewer.

## Reference(s):

- [ClawHub release](https://clawhub.ai/kokxi/skills/qa-team-skills)
- [QA skill user manual](docs/user-manual.md)
- [QA workflow reference](references/qa-team.md)
- [Local memory guide](memory/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Structured Markdown responses and reports, with optional local JSON testing records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language QA output; local test history may be retained with user confirmation]

## Skill Version(s):

1.8.0 (source: ClawHub release, skill frontmatter, VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
