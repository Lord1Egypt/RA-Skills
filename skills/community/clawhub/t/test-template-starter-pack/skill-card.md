## Description:

Provides a Python starter template, tests, and guide for adapting Telegram vertical-agent workflows with intent classification, lead scoring, CRM persistence, routing, follow-up, analytics, and tier gating.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oturans](https://clawhub.ai/user/oturans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and builders use this skill to scaffold and test narrow Telegram vertical-agent prototypes such as intake, CRM, appointment, tax, or support workflows before replacing mock data stores with real integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact presents the template as production-ready, while the security evidence says it should be treated as a prototype/test template rather than a production Telegram agent.

Mitigation: Review and adapt the template before real deployment; add production secret handling, webhook verification, access controls, logging limits, and data-retention rules.

Risk: The Python test runner can write and delete fixed SQLite database files outside the skill directory through FUTURE_WORKSPACE.

Mitigation: Run tests only in an isolated workspace and set FUTURE_WORKSPACE to a disposable directory before executing the runner.

Risk: Example verticals include CRM, payment, tax, legal, healthcare, and customer-data scenarios that can carry sensitive operational or personal data.

Mitigation: Use mock data until the workflow has been reviewed, then connect real CRM, payment, tax, legal, healthcare, or customer data only after appropriate controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oturans/skills/test-template-starter-pack)
- [Vertical builder guide](artifact/GUIDE.md)
- [Real estate example brief](artifact/examples/realestate-brief.md)
- [SelfBot example brief](artifact/examples/selfbot-brief.md)
- [Claw Mart upgrade path](https://shopclawmart.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces starter template instructions and local test commands; the Python runner writes SQLite test databases under FUTURE_WORKSPACE.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
