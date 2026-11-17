## Description:

小龙虾 is a coding assistant for code generation, code review, debugging, optimization, explanation, refactoring, testing, API design, SQL, and architecture guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengpengliu1212-art](https://clawhub.ai/user/pengpengliu1212-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get coding assistance across implementation, review, debugging, optimization, testing, API design, SQL, and architecture tasks. It can run as a command-line assistant backed by a configured Volcengine DeepSeek endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation content is sent to the configured Volcengine endpoint and stored in local history.

Mitigation: Use a disposable or tightly scoped API key, avoid submitting secrets or proprietary code, and clear history when needed.

Risk: The save and export commands can write generated code to user-selected paths and may overwrite user-writable files.

Mitigation: Avoid arbitrary save paths until path validation and overwrite protection are fixed; review target paths before using save or export commands.

Risk: Generated coding advice or code may be incorrect, insecure, or unsuitable for the target project.

Mitigation: Review, test, and scan generated changes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pengpengliu1212-art/skills/xiaolongxia)
- [Publisher profile](https://clawhub.ai/user/pengpengliu1212-art)
- [Configured Volcengine coding endpoint](https://ark.cn-beijing.volces.com/api/coding/v3)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with code blocks, command output, and optional generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a configured Volcengine DeepSeek endpoint and can save or export generated code files.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
