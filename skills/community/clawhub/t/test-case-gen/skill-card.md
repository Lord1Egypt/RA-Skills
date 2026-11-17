## Description:

Generate structured test cases from requirements, user stories, PRDs, or API documentation, with support for common test design techniques and markdown, CSV, or JSON-style outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanghengyi1986-afk](https://clawhub.ai/user/zhanghengyi1986-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, product teams, and external users use this skill to turn requirements, user stories, PRDs, or API documentation into structured test cases, coverage summaries, and export-ready test data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated test cases or exported test data may be incomplete, incorrect, or unsuitable for direct import into downstream test-management tools.

Mitigation: Review generated cases, expected results, priorities, and import fields before using them for release decisions or importing them into TestLink, ZenTao, or similar tools.

Risk: The skill may write user-requested export files in the OpenClaw workspace output directory.

Mitigation: Confirm the requested export format and destination before using generated CSV, JSON, or XML artifacts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhanghengyi1986-afk/skills/test-case-gen)
- [Publisher Profile](https://clawhub.ai/user/zhanghengyi1986-afk)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown tables with optional CSV, JSON, or XML export structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include priority labels, test types, coverage summaries, and import-oriented field mappings for tools such as TestLink or ZenTao.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
