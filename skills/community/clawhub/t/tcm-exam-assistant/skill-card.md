## Description:

中医执业医师考试备考助手，生成每日复习计划、评估答案并管理错题集。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tom859174-sketch](https://clawhub.ai/user/tom859174-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

External learners preparing for the Chinese traditional medicine practitioner examination use this skill to turn study feedback into daily review plans, evaluate practice-answer results, track progress, and maintain a wrong-question set.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local study history, wrong answers, preferences, and document-cache metadata, and can export a wrong-question file.

Mitigation: Use a private local workspace, avoid sensitive personal notes in shared or cloud-synced folders, and review exported files before sharing them.

Risk: Export and initialization may fail because the implementation references an undefined output directory variable.

Mitigation: Confirm the publisher fixes or configures the output directory before relying on wrong-question export.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tom859174-sketch/skills/tcm-exam-assistant)
- [Publisher profile](https://clawhub.ai/user/tom859174-sketch)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-like Chinese study plans, answer-evaluation reports, command-line guidance, and exported text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local memory JSON files and an exported wrong-question text file when requested.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
