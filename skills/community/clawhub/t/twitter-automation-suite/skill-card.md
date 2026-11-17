## Description:

Twitter/X automation guidance for posting tweets, monitoring keywords, configuring automated replies, generating content with AI, and reviewing account analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjstate](https://clawhub.ai/user/cjstate)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators, developers, and account-growth teams use this skill to prepare Twitter/X posting workflows, keyword monitoring, automatic reply rules, and basic account analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use direct Twitter/X login credentials and post publicly from an account.

Mitigation: Use a dedicated low-privilege account when possible, avoid exposing unrelated secrets in the same environment, and review posts before sending.

Risk: The browser automation launches with sandboxing disabled.

Mitigation: Run browser automation only in an isolated environment and do not disable sandboxing on shared or sensitive systems.

Risk: The install process depends on mutable npm packages without a lockfile.

Mitigation: Pin dependencies with a lockfile and review dependency changes before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment variable names, cron-style schedules, and Node.js command examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
