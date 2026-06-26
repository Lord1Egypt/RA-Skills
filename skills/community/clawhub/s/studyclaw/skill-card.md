## Description: <br>
Interactive study assistant that creates flashcards, quizzes, and spaced repetition reviews from notes, PDFs, photos, text, URLs, or topic prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keepfit44](https://clawhub.ai/user/keepfit44) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn study material into flashcard decks, quiz sessions, practice exams, and spaced repetition reviews through an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local deck file operations may create, import, export, or delete files using deck names that are only partially constrained. <br>
Mitigation: Review the skill before installing, use ordinary deck names, avoid untrusted imported deck JSON, and confirm delete/export operations before relying on them. <br>
Risk: Study material and generated decks are stored locally, which may be inappropriate for sensitive notes if local retention is not acceptable. <br>
Mitigation: Use the skill only with study material you are comfortable storing locally, and avoid sensitive content unless local storage is approved. <br>


## Reference(s): <br>
- [Study Buddy on ClawHub](https://clawhub.ai/keepfit44/studyclaw) <br>
- [Publisher profile](https://clawhub.ai/user/keepfit44) <br>
- [Study Buddy Guidelines](references/guidelines.md) <br>
- [Study Buddy Data Format](references/data_format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown chat guidance with inline shell commands and local JSON deck files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; stores study decks locally under ~/.openclaw/study-buddy/decks/.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
