## Description:

Guides agents through using the Craftsman/OneKey toy generation APIs to create toy design drafts, multi-view reference sheets, and generated 3D toy models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative agents use this skill to draft stuffed-toy concepts, submit 3D generation tasks from prompts or images, poll task progress, and retrieve generated model and preview URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image references, session or task IDs, and generated outputs may be sent to external services.

Mitigation: Use a revocable API key and avoid submitting confidential prompts or images.

Risk: The optional npx CLI workflow executes a third-party package.

Mitigation: Prefer the REST API examples, or pin and verify the onekey CLI package before use.

Risk: Returned share_url links may expose generated task results.

Mitigation: Treat share_url links as private and avoid sharing them publicly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/stuffed-toy-generator)
- [Craftsman 3D Generator](https://craftsman-agent.aiagenta2z.com/app/3d-generator)
- [Craftsman website](https://craftsman-agent.aiagenta2z.com)
- [OneKey API key workspace](https://deepnlp.org/workspace/keys)
- [OneKey Agent Gateway endpoint](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with REST JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API request parameters, response fields, and polling workflow notes.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
