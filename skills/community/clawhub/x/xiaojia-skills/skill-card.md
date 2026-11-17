## Description:

Calls JustAI OpenAPI async chat endpoints to submit agent tasks, poll results, and return structured JSON for marketing plans, Xiaohongshu notes, image generation, information collection, confirmation cards, and follow-up turns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanchaowen84](https://clawhub.ai/user/tanchaowen84)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route supported content automation tasks through a configured JustAI service instead of handling those tasks locally. It is intended for listing available projects or skills, submitting asynchronous chat tasks, polling results, and continuing conversations with a preserved conversation ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends API keys and user content to a configured JustAI network endpoint.

Mitigation: Use only a verified HTTPS JustAI endpoint, protect and rotate the API key, and avoid sending secrets or regulated data unless that remote service is approved for the data.

Risk: The documented install command uses a mutable source path.

Mitigation: Install from a pinned commit or signed release when deploying the skill in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanchaowen84/skills/xiaojia-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include conversation IDs, branch names, structured result payloads, text fallbacks, and surfaced failure messages from the configured JustAI endpoint.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
