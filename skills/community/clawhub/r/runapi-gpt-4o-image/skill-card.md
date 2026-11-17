## Description:

Generate and edit images with GPT-4o Image through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to generate or edit image artifacts with GPT-4o Image through RunAPI. It guides one-off CLI execution and SDK-based application integration while requiring contract discovery and result verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned third-party RunAPI CLI installed from a Homebrew tap.

Mitigation: Trust the RunAPI tap before installation, avoid elevated privileges, and inspect the installed command help before execution.

Risk: The skill can send local media inputs to RunAPI.

Mitigation: Use a scoped RunAPI API key where possible and provide only local media files intended for upload.

Risk: Asynchronous image-generation tasks can create billable work before final deliverables are available.

Mitigation: Submit once, preserve task evidence, wait on the same task, and do not resubmit after terminal failure without user authorization.

## Reference(s):

- [RunAPI GPT-4o Image model page](https://runapi.ai/models/gpt-4o-image)
- [RunAPI GPT-4o Image model documentation](https://runapi.ai/models/gpt-4o-image.md)
- [RunAPI OpenAI provider documentation](https://runapi.ai/providers/openai.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI GPT-4o Image SDK](https://github.com/runapi-ai/gpt-4o-image-sdk)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create request, task, result, and downloaded image files during execution.]

## Skill Version(s):

0.2.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
