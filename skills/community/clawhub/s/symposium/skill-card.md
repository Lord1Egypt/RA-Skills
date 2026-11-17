## Description:

Orchestrate a philosophical dialogue between Plato's Symposium characters, each powered by a different AI model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyz2102](https://clawhub.ai/user/dyz2102)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, and developers use this skill to run multi-perspective philosophical dialogues about AI, consciousness, meaning, and related questions. It coordinates model-backed philosopher personas and returns a readable dialogue for reflection or discussion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generated dialogue context are sent to OpenRouter using the user's API key.

Mitigation: Avoid secrets, private documents, and sensitive personal data in symposium prompts or dialogue context.

Risk: The optional web app path includes repository checkout and dependency installation.

Mitigation: Review or pin the repository and dependencies before running install commands, and do not use elevated privileges.

Risk: Generated philosophical dialogue may contain inaccurate, misleading, or overconfident claims.

Mitigation: Review outputs before relying on them for instruction, publication, or decision-making.

## Reference(s):

- [The Symposium on ClawHub](https://clawhub.ai/dyz2102/skills/symposium)
- [dyz2102 ClawHub publisher profile](https://clawhub.ai/user/dyz2102)
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown dialogue text with inline shell command examples and an optional saved .md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OpenRouter API calls under the user's API key; dialogue length depends on selected speakers and model responses.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
