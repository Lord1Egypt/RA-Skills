## Description:

Guidance for choosing varg video, image, voice, and music models and writing prompts, reference instructions, and quality checks for generated shots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and production teams use this skill to choose a suitable model, prepare image, video, and audio prompts with references, estimate generation costs, and review clips for visual and audio defects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags advice that may rephrase prompts around content moderation.

Mitigation: Review moderation-related suggestions against the model provider's rules and do not use them to evade safety controls.

Risk: The workflow can upload local footage or recordings to hosted services.

Mitigation: Check the upload destination and avoid sensitive footage or recordings unless disclosure is approved.

Risk: The scan was partial because some referenced paths were unresolved.

Mitigation: Review unresolved referenced resources before installing or relying on the skill.

Risk: The README's installer command does not pin a release, as noted in the security summary.

Mitigation: Verify the source and intended release before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vargai/skills/varg-video-prompting)
- [varg.ai](https://varg.ai)
- [Prompt templates](references/prompt-templates.md)
- [Model notes and quirks](references/models.md)
- [MCP tools guide](references/mcp-tools.md)
- [Examples](references/examples.md)
- [Look references](references/look-references.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, API calls]

**Output Format:** [Markdown with prompt text, checklists, and optional command or API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model recommendations, generation prompts, reference guidance, and visual or audio QA checklists.]

## Skill Version(s):

1.0.12 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
