## Description:

Optimize OpenClaw workflows and reduce LLM API costs by running a local companion that reduces repeated context, unnecessary steps, and token waste without workflow changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[immrlucky](https://clawhub.ai/user/immrlucky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Spectyra to route OpenClaw model requests through a local companion that exposes spectyra/* model profiles and a local savings dashboard for workflow and token optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install and run third-party npm code for a local companion.

Mitigation: Use a pinned, reviewed package version and confirm the package source before installing or updating it.

Risk: The companion becomes the default model path for OpenClaw agent traffic.

Mitigation: Review what prompts, responses, and provider credentials the companion can access before enabling it as the default provider.

Risk: The companion starts a local HTTP dashboard and API endpoint on 127.0.0.1.

Mitigation: Run the companion only when needed, keep it bound to localhost, and confirm how to stop or uninstall it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/immrlucky/skills/spectyra)
- [Publisher Profile](https://clawhub.ai/user/immrlucky)
- [Spectyra Homepage](https://spectyra.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs and starts a local companion, then configures OpenClaw model defaults and provider settings.]

## Skill Version(s):

1.0.25 (source: ClawHub release metadata, skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
