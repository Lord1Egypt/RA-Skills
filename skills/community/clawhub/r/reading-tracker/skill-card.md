## Description:

Reading Tracker helps users record reading progress, capture quotes and reflections, schedule reviews, and generate reading reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ttff117](https://clawhub.ai/user/ttff117)

### License/Terms of Use:

MIT-0

## Use Case:

Readers and personal-productivity users use this skill to maintain book notes, track reading progress, preserve quotes and reflections, and build weekly and monthly review habits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted book titles can cause note files to be written outside the intended reading notes folder.

Mitigation: Review title handling before installation or use only trusted, ordinary book titles until filename and path handling is fixed.

Risk: The skill stores reading notes, quotes, reflections, progress, and reminder data locally and may resurface that data in reviews.

Mitigation: Avoid recording sensitive personal information unless local workspace storage and review behavior are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ttff117/skills/reading-tracker)
- [Book Note Templates](references/note_template.md)
- [Review Prompt Library](references/review_prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, JSON reading indexes and review schedules, text reports, and CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local reading files under the user's reading workspace.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
