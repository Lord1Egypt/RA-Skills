## Description:

Parse anime storyboard scripts and generate four types of prompts: character prompts, scene prompts, Sora video generation prompts, and standard storyboard prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to convert anime or film storyboard scripts into bilingual prompts for character, scene, Sora video, and standard storyboard generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompt wording can influence downstream image or video generation results and may carry incorrect storyboard, style, or formatting assumptions.

Mitigation: Review generated prompts before using them in media generation tools, especially for project style consistency, negative prompts, and aspect ratio choices.

## Reference(s):

- [Storyboard Terminology Reference](references/terminology.md)
- [Prompt Template Library](references/templates.md)
- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/storyboard-prompt-generator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with bilingual prompt text, template-driven sections, negative prompt suggestions, and aspect ratio guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single storyboard requests and batch generation for multiple storyboard panels.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
