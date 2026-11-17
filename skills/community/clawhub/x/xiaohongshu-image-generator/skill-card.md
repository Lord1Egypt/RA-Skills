## Description:

Generates Xiaohongshu-style vertical image cards from user prompts using HTML/CSS templates and browser screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parker-y](https://clawhub.ai/user/parker-y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to create Xiaohongshu note covers, marketing visuals, and generic vertical social cards from prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unescaped prompt or content text may be rendered in a local browser workflow and run injected HTML or script.

Mitigation: Review before installing, use only trusted prompts and content, write outputs into a dedicated empty directory, stop the localhost server after screenshotting, and prefer an implementation that HTML-escapes displayed fields and applies a restrictive content security policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parker-y/skills/xiaohongshu-image-generator)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Guidance]

**Output Format:** [HTML/CSS files with text guidance, shell commands, and screenshot file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 800x1000 vertical card assets through a local browser screenshot workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
