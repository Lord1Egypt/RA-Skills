## Description:

Generate textual descriptions of one or more images by delegating selected image files to a vision-capable OpenRouter model through opencode run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when a task needs image contents described but the current session model cannot read images. It supports image captions, article notes, infographic inputs, video shot lists, face-presence checks, and narrative ordering recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected image files may be processed by the configured OpenRouter vision model through opencode run.

Mitigation: Confirm that external processing is acceptable before use, and avoid sensitive images unless that processing is approved.

Risk: AI-generated image descriptions may be inaccurate or incomplete.

Mitigation: Spot-check generated descriptions against the source images before using them in articles, prompts, or downstream media workflows.

## Reference(s):

- [ClawHub read-image skill page](https://clawhub.ai/j3ffyang/skills/read-image)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown descriptions with optional labeled lists and command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include AI-generated image descriptions, face-presence notes, and narrative ordering recommendations that should be spot-checked by the user.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
