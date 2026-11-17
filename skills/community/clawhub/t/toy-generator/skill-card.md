## Description:

Generates toy design drafts, multi-view sheets, and 3D toy model tasks through OneKey Agent Gateway APIs served by Craftsman Agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to call Craftsman Agent toy-generation APIs that turn prompts or reference images into toy design drafts, 3D generation tasks, progress polling, preview links, and downloadable model files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, generated assets, task metadata, and share links may be sent to OneKey or Craftsman services.

Mitigation: Avoid sensitive or proprietary inputs unless there is a clear data-handling agreement, and keep returned share URLs private.

Risk: The skill documents unpinned npm command execution for the OneKey CLI.

Mitigation: Prefer the REST examples or run a pinned, reviewed OneKey CLI version in a restricted environment.

Risk: The skill requires the DEEPNLP_ONEKEY_ROUTER_ACCESS credential.

Mitigation: Store the key in a protected environment variable, do not paste it into logs or prompts, and rotate it if exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai-hub-admin/skills/toy-generator)
- [Publisher Profile](https://clawhub.ai/user/ai-hub-admin)
- [OneKey Agent Gateway Endpoint](https://agent.deepnlp.org/agent_router)
- [Craftsman 3D Generator](https://craftsman-agent.aiagenta2z.com/app/3d-generator)
- [Craftsman Agent Website](https://craftsman-agent.aiagenta2z.com)
- [OneKey API Key Workspace](https://deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [Markdown guidance with REST and CLI command examples plus JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The APIs may return share URLs, generated image URLs, task IDs, preview URLs, and 3D model files such as GLB.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
