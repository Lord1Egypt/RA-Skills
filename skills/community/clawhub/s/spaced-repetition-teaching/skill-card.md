## Description:

Adaptive spaced repetition engine using the FSRS-6 algorithm to manage markdown flashcard reviews, due-card queues, review ratings, and retention-oriented study sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tylerbittner](https://clawhub.ai/user/tylerbittner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, learners, and agents use this skill to maintain a markdown flashcard deck, list cards due for review, record review ratings, and schedule future reviews with FSRS-based intervals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The review workflow writes scheduling updates directly to the selected markdown flashcard file.

Mitigation: Confirm the card file path before running reviews or adding cards, and keep a backup for important decks.

## Reference(s):

- [FSRS Algorithm Reference](artifact/references/fsrs-algorithm.md)
- [open-spaced-repetition/py-fsrs](https://github.com/open-spaced-repetition/py-fsrs)
- [Formation](https://formation.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown and terminal-oriented text with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update the user-selected markdown flashcard file when recording a review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
