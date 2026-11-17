## Description:

Generates comprehensive test cases from MySQL/Redis data. Invoke when user wants to create test cases for an API endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hcyyy0120](https://clawhub.ai/user/hcyyy0120)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to analyze API endpoint code, read MySQL table schemas/data and Redis values, and generate comprehensive JSON test cases for later review or JUnit test generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access application configuration, MySQL databases, Redis caches, and generated output files that may contain sensitive data.

Mitigation: Use non-production, read-only credentials; prefer schema-only or sanitized test data; restrict table names and Redis key patterns tightly.

Risk: Generated JSON outputs may include secrets or personal data from database/cache reads before they are shared with an LLM or another test-execution skill.

Mitigation: Review generated outputs for secrets or personal data before sharing them or invoking downstream test-generation workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON test case structures and optional shell commands; generated artifacts may be JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read database/cache data and save test_cases_{timestamp}.json or data export JSON when requested.]

## Skill Version(s):

2.0.1 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
