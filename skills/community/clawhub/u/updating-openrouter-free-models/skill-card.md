## Description:

Use when needing to fetch, test, and update OpenRouter free model lists in Claude Code or OpenClaw configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youshu3008](https://clawhub.ai/user/youshu3008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to refresh OpenRouter free model allowlists, test model availability, and synchronize Claude Code and OpenClaw configuration with validated fallbacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The model tester can use ANTHROPIC_AUTH_TOKEN before OPENROUTER_API_KEY, which may expose the wrong token to OpenRouter.

Mitigation: Use a dedicated OpenRouter-scoped API key and avoid relying on ANTHROPIC_AUTH_TOKEN for this workflow.

Risk: The update scripts can make persistent changes to Claude Code and OpenClaw model configuration.

Mitigation: Back up ~/.claude/settings.json and ~/.openclaw/openclaw.json, then inspect /tmp/verified_models.txt before applying updates.

Risk: The complete test and restart helper can affect a live OpenClaw setup.

Mitigation: Avoid complete_test.sh on production or live setups and confirm any OpenClaw restart manually.

## Reference(s):

- [OpenRouter API docs](https://openrouter.ai/docs)
- [OpenRouter models API](https://openrouter.ai/api/v1/models)
- [ClawHub skill page](https://clawhub.ai/youshu3008/skills/updating-openrouter-free-models)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, and generated JSON configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary model-list files under /tmp and update local Claude Code or OpenClaw configuration when the user runs the scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
