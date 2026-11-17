## Description:

Align a user's narration, measured subtitles, audio, preview, and frame-based timeline while preserving the selected composition and source facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors and content creators use this skill to align approved narration, subtitle timing, audio, visuals, and scenes in a selected project. It preserves the project's native timeline schema and approved facts while checking measured durations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Timing changes can leave scenes or captions out of sync with the measured audio and preview.

Mitigation: Use measured media durations and review the resulting video after timing changes.

Risk: Applying the sample checker to a project-native timeline can misread its structure.

Mitigation: Preserve the project's existing schema and use the checker only for its documented sample format.

Risk: An unintended file change can overwrite work outside the selected task.

Mitigation: Select the intended timeline file and keep a backup before editing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xxjrq/skills/selfmedia-script-storyboard)

## Skill Output:

**Output Type(s):** [Guidance, Files, Configuration instructions, Shell commands]

**Output Format:** [Project-native timeline edits and concise validation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves the selected project's timeline schema and identifiers.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
