## Description:

[QwenCloud] Manage account auth and query usage/billing. Use for: login, logout, check usage, view billing, free tier quota, coding plan status, pay-as-you-go costs. Skip for: model browsing, non-account tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to authenticate with QwenCloud and retrieve usage, free tier quota, coding plan status, and pay-as-you-go billing information through the QwenCloud CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install an unpinned global third-party CLI that handles QwenCloud sessions, credentials, usage, and billing data.

Mitigation: Install only a reviewed pinned CLI version from a trusted source in a constrained environment, and verify credential storage before logging in.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Markdown]

**Output Format:** [Markdown guidance with inline shell commands; CLI results are parsed from JSON or shown as plaintext when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers explicit JSON CLI output for agent parsing and human-readable summaries.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
