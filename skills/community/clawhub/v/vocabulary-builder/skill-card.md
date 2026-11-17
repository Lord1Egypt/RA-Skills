## Description:

Builds and reviews vocabulary from books, podcasts, and daily encounters using reading sessions, word collection, three-step learning, spaced repetition, quiz scheduling, and progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winlinvip](https://clawhub.ai/user/winlinvip)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal learning agents use this skill to capture unfamiliar words, generate pronunciation-first word cards, practice vocabulary, track review progress, and optionally schedule recurring quizzes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vocabulary data, source and page details, context sentences, quiz history, and quiz state are stored locally by default.

Mitigation: Review memory/vocabulary.md before sharing the workspace and avoid adding sensitive source material or personal context.

Risk: Scheduled quizzes can create recurring reminders when the user enables them.

Mitigation: Set up reminders only after confirming the frequency, delivery channel, target, and sleep-hour constraints with the user.

## Reference(s):

- [Why I Stopped Using Flashcards and Started Using AI](https://youtu.be/wjWrVpZZXSg)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with vocabulary cards, tracker entries, quiz state, and optional cron setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores vocabulary progress in memory/vocabulary.md and references optional pronunciation audio in docs/tts-fr/.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
