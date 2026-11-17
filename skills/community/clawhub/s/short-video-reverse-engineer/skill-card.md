## Description:

Analyzes short videos by extracting keyframes and speech transcripts, reviewing visual and compliance details, and producing structured HTML reports with reusable prompts and 10-second adaptation plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pdxingqq](https://clawhub.ai/user/pdxingqq)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, developers, and automation users can use this skill to break down short-form video files into frames, transcripts, visual analysis, compliance notes, reusable generation prompts, and practical production guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts perform file cleanup and archival actions in configured video, temporary, and output directories.

Mitigation: Run in an isolated, non-admin Python environment, confirm all configured paths before execution, and test on copies of media files first.

Risk: Hardcoded external Windows and WorkBuddy paths can cause the batch workflow to fail or execute an unexpected interpreter or template.

Mitigation: Replace hardcoded paths with package-relative paths and review script configuration before batch generation.

Risk: Untrusted configuration JSON can affect generated report content and referenced local files.

Mitigation: Use trusted configuration files only and review generated HTML reports and referenced image paths before sharing.

Risk: Reverse-engineering short videos can preserve copyrighted, branded, personal, or sensitive content in prompts, reports, transcripts, and reference images.

Mitigation: Apply the skill's compliance checks and human review to remove or generalize protected logos, real institution names, personal identifiers, and sensitive topics before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pdxingqq/skills/short-video-reverse-engineer)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [HTML report files with JSON transcript/configuration data, JPEG reference images, reusable prompts, and inline shell command templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes timestamped dialogue, visual breakdowns, compliance review, 10-second adaptation guidance, and local reference image paths.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
