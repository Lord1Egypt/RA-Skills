## Description: <br>
Generates realistic test data for software testing, including Chinese-locale fixtures and JSON, CSV, and SQL output patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanghengyi1986-afk](https://clawhub.ai/user/zhanghengyi1986-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to create synthetic fixtures, API payloads, and seed data for testing databases, services, and Chinese-locale workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production personal or financial data copied into test environments can expose sensitive information. <br>
Mitigation: Prefer fully synthetic data and only use production-derived data when legal and security requirements explicitly allow it. <br>
Risk: Masking examples are illustrative and may not provide irreversible anonymization. <br>
Mitigation: Validate any masking workflow against internal privacy and security requirements before relying on it. <br>
Risk: Generated SQL may not be appropriate for every schema or database environment. <br>
Mitigation: Review generated SQL before running it against any database. <br>


## Reference(s): <br>
- [Faker documentation](https://faker.readthedocs.io/en/master/) <br>
- [ClawHub skill page](https://clawhub.ai/zhanghengyi1986-afk/qa-test-data-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and optional JSON, CSV, or SQL files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports seeded local generation for reproducible fixtures when users provide a seed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
