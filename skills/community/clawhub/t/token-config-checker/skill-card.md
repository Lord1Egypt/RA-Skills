## Description:

Validates Codex/OpenAI-style token and auth JSON files with offline checks, optional online access-token probing, redacted reporting, and valid/no_quota/invalid bucketing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe12801](https://clawhub.ai/user/joe12801)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to inspect token/auth JSON files they own, triage validity and quota state, and produce redacted reports or separated config sets for debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive token and auth configuration files.

Mitigation: Run it only on token files you own, keep raw configs private, and share only redacted reports.

Risk: Online probing can send access tokens to remote endpoints, including user-selected probe URLs.

Mitigation: Use offline checks by default and pass a custom --probe-url only when the endpoint operator is fully trusted.

Risk: Save-directory options can create additional copies of live credential files.

Mitigation: Avoid bucket-copy options unless the destination directories are protected and scheduled for cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joe12801/skills/token-config-checker)
- [Default OpenAI models probe endpoint](https://api.openai.com/v1/models)
- [Codex usage probe endpoint](https://chatgpt.com/backend-api/wham/usage)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, text reports, JSON lines, index.json, and bucketed configuration file copies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports redact token values; save-directory options can duplicate credential files.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
