## Description:

Generate high-quality images on-demand via the Runware.ai API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geeklord](https://clawhub.ai/user/geeklord)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to ask an agent to generate images from text prompts through the Runware API and save the generated image files locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send user prompts to Runware automatically.

Mitigation: Review prompts before execution, avoid sensitive prompt content, and use the skill only where sending prompts to Runware is acceptable.

Risk: The Runware API key may incur usage charges if misused.

Mitigation: Use a dedicated Runware API key with limited billing exposure and manage it through environment variables or a secret manager.

Risk: The skill writes generated image files to local storage.

Mitigation: Run it only where local file writes are acceptable, confine output to a dedicated image directory, and avoid overwriting existing files without review.

Risk: Dependencies are not pinned to exact versions.

Mitigation: Review and pin dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geeklord/skills/runware-image)
- [Publisher profile](https://clawhub.ai/user/geeklord)
- [Runware documentation](https://runware.ai/docs/getting-started/introduction)
- [Runware task API endpoint](https://api.runware.ai/v1/tasks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated image files saved by the skill script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a RUNWARE_API_KEY environment variable and writes generated image files to a configured local output directory.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
