## Description:

Manages the full lifecycle of invoice validation rules, rule groups, and validation scenarios through a unified CLI that performs API calls, parses parameters, loads configuration, and reports errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[12266601032](https://clawhub.ai/user/12266601032)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations staff use this skill to create, query, update, enable, disable, and delete invoice validation rules, rule groups, and validation scenarios. It is intended for teams maintaining validation-admin environments where invoice rule behavior must be configured through documented API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens may be exposed or reused if stored in local configuration or broad environment contexts.

Mitigation: Use least-privilege, short-lived tokens, prefer environment injection for controlled runs, and avoid committing config.json.

Risk: Rule, rule group, and scene delete or enable/disable operations can alter validation behavior in administrative environments.

Mitigation: Require explicit operator confirmation and change review before destructive or state-changing actions.

Risk: Weak transport settings can expose credentials or administrative requests.

Mitigation: Use the skill only with intended validation-admin endpoints over HTTPS.

Risk: Generic npx invocation can run an unexpected package when the local CLI is not pinned or reviewed.

Mitigation: Invoke a pinned or reviewed local CLI path, such as npx with an explicit local prefix.

## Reference(s):

- [Skill page](https://clawhub.ai/12266601032/skills/validation-rule-management)
- [Publisher profile](https://clawhub.ai/user/12266601032)
- [Data model reference](references/data-model.md)
- [Usage examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke a local Node.js CLI that prints API responses as formatted JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
