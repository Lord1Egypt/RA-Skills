## Description:

TS Prompt Optimizer turns vague user requests into clearer, more specific task prompts using configurable model routing and personalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen435636097](https://clawhub.ai/user/chen435636097)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI assistant users use this skill to rewrite underspecified prompts into clearer instructions for coding, writing, analysis, and creative tasks. It can route optimization through configured model providers and apply local preferences or prompt history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can persist API keys in local config or shell profile files.

Mitigation: Use dedicated low-privilege keys, avoid entering live credentials unless local persistence is acceptable, and rotate any keys already processed by the skill.

Risk: Diagnostics and prompt history can expose credentials or sensitive prompts.

Mitigation: Avoid show or get diagnostics with live credentials, and disable, clear, or review memory and history files before submitting sensitive prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chen435636097/skills/ts-prompt-optimizer)
- [ClawHub project homepage from metadata](https://github.com/openclaw/clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text prompts with optional inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local configuration and memory files when setup or learning features are enabled.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
