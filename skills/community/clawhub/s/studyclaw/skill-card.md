## Description:

Study Buddy creates flashcards, quizzes, practice exams, and spaced repetition reviews from notes, PDFs, photos, text, URLs, topics, or recent conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keepfit44](https://clawhub.ai/user/keepfit44)

### License/Terms of Use:

MIT-0

## Use Case:

Students, educators, and other external users use Study Buddy to turn study material into flashcards, run quiz or practice exam sessions, and track due reviews with local spaced repetition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flashcards and review history are stored locally on the user's machine.

Mitigation: Use on trusted machines and avoid highly sensitive notes on shared systems.

Risk: Imported deck files can add or overwrite local study content.

Mitigation: Review deck files before importing them and confirm the source is trusted.

Risk: Generated cards, quizzes, and practice exams can contain inaccurate or incomplete study guidance.

Mitigation: Review generated study material against the original source before relying on it for exams or decisions.

## Reference(s):

- [Study Buddy Guidelines](references/guidelines.md)
- [Study Buddy Data Format](references/data_format.md)
- [Study Buddy ClawHub Release](https://clawhub.ai/keepfit44/skills/studyclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown chat responses with shell command invocations and JSON deck records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores deck files and review history locally under ~/.openclaw/study-buddy/decks/.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
