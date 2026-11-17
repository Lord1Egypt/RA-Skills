## Description:

Generate realistic structured test data for software testing with Chinese locale support, Faker-based generators, and JSON, CSV, SQL, and API-ready output patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanghengyi1986-afk](https://clawhub.ai/user/zhanghengyi1986-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to generate synthetic users, orders, products, database seed data, API fixtures, and Chinese-locale test records for software testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real personal data copied into test environments may remain identifiable if only simple masking snippets are used.

Mitigation: Prefer synthetic Faker data; require formal anonymization, access controls, and compliance review before using any real personal data.

Risk: SQL output can be unsafe when untrusted table names are accepted.

Mitigation: Use reviewed fixed table names or validate SQL identifiers before generating SQL output.

Risk: Dependency behavior can change if Faker is installed without version review.

Mitigation: Pin Faker to a reviewed version before using the generated data workflow.

## Reference(s):

- [Faker documentation](https://faker.readthedocs.io/en/master/)
- [ClawHub skill page](https://clawhub.ai/zhanghengyi1986-afk/skills/qa-test-data-gen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python and shell snippets; generated data files may be JSON, CSV, or SQL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional record counts, data type selection, output paths, SQL table names, and random seeds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
