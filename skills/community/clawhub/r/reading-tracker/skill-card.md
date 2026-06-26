## Description: <br>
Reading Tracker helps readers manage book progress, capture quotes and reflections, schedule spaced-repetition reviews, and generate reading reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ttff117](https://clawhub.ai/user/ttff117) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers and personal knowledge-management users use this skill to track books, record quotes and reflections, receive review prompts, and summarize monthly or yearly reading activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Book titles containing slashes, '..', absolute paths, or other path-like characters can cause files to be written outside the intended reading folder. <br>
Mitigation: Use plain book titles without path separators or traversal patterns, and review generated file paths before relying on CLI writes. <br>
Risk: Local reading notes, library indexes, and review schedules are stored on disk. <br>
Mitigation: Avoid storing sensitive reading notes unless the local workspace is protected and reviewed before sharing. <br>
Risk: The weekly reminder can create scheduled reading-review activity. <br>
Mitigation: Enable the weekly reminder only when scheduled review prompts are desired. <br>


## Reference(s): <br>
- [Book Note Templates](artifact/references/note_template.md) <br>
- [Review Prompt Library](artifact/references/review_prompts.md) <br>
- [Reading Tracker ClawHub Page](https://clawhub.ai/ttff117/reading-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown notes, text prompts, CLI output, and local JSON or Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When the included CLI is used, reading notes, book indexes, and review schedules are stored on local disk.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
