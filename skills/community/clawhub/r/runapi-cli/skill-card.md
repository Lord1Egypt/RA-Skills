## Description:

Guides agents in discovering RunAPI services and pricing, running one-off tasks with the CLI, and making wallet-funded x402 Task calls through the REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find RunAPI models and prices, run supported one-off CLI tasks, or pay for and poll eligible REST tasks with an agent wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote installer may execute unreviewed code.

Mitigation: Prefer the package-manager install; inspect or verify the remote installer before using the curl-to-shell option.

Risk: Task inputs and uploaded files are sent to RunAPI.

Mitigation: Use the skill only with data that may be shared with RunAPI.

Risk: Wallet-funded tasks may incur charges.

Mitigation: Check live pricing and confirm each paid task before spending.

Risk: API keys, payment signatures, and listener secrets could be exposed.

Mitigation: Keep secrets out of logs and project files; use environment or secure wallet authentication.

## Reference(s):

- [RunAPI model and CLI service documentation](https://runapi.ai/models.md)
- [RunAPI model catalog](https://runapi.ai/models)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI responses are JSON; task results and generated file links come from RunAPI.]

## Skill Version(s):

0.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
