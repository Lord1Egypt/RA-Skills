## Description:

Guides agents through creating, reviewing, styling, and exporting video captions with the local Yaps app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaps](https://clawhub.ai/user/yaps)

### License/Terms of Use:

MIT

## Use Case:

Video creators and editors use this skill to add and refine timed captions in Yaps, then export a captioned video while keeping the source video intact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The adapter can invoke Yaps commands beyond captions and uses local app and account state.

Mitigation: Review the skill before installation, use only intended caption commands, and run it only when you trust Yaps and local app automation.

Risk: Caption jobs can save Yaps projects and write media outputs, including after an export fails.

Mitigation: Use a new output filename, preserve source media and existing files, and inspect saved projects before retrying.

## Reference(s):

- [Yaps local runtime guide](references/runtime.md)
- [Yaps download](https://yaps.ai/download)
- [Yaps Auto Captions on ClawHub](https://clawhub.ai/yaps/skills/yaps-auto-captions)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with command examples and a link to the exported video]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates an editable Yaps project and an exported captioned MP4 when the local app and account are available.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
