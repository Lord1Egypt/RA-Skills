## Description:

Generates simple SVG frame animations and video or GIF rendering guidance for themes or short stories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juliantsaiii](https://clawhub.ai/user/juliantsaiii)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to ask an agent for SVG frame-generation code, animation timing guidance, and shell commands that render short MP4 or GIF animations with local tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes local command execution and generated file handling under /tmp.

Mitigation: Review commands before execution, avoid untrusted output paths, and run in a constrained local environment.

Risk: The advertised generation scope may exceed the included template-based animation behavior.

Mitigation: Treat the skill as a helper for simple SVG animation templates and verify generated outputs before relying on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/juliantsaiii/skills/svg-animator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local files under /tmp and generated MP4 or GIF outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
