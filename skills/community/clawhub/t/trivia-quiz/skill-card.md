## Description:

Play knowledge quizzes with facts, categories, and daily challenges for learning topics, drilling flashcards, reviewing answers, and tracking progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as a local study assistant to generate trivia quizzes, plan study sessions, create flashcards, save notes, review material, and track learning progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store notes and command history as plaintext on the user's local machine.

Mitigation: Avoid entering sensitive personal, proprietary, or credential-like information, and delete ~/.local/share/trivia-quiz or the configured TRIVIA_QUIZ_DIR to remove stored history.

## Reference(s):

- [Trivia Quiz on ClawHub](https://clawhub.ai/bytesagain-lab/skills/trivia-quiz)
- [bytesagain-lab ClawHub profile](https://clawhub.ai/user/bytesagain-lab)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and terminal-oriented text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local plaintext notes and command history under ~/.local/share/trivia-quiz or TRIVIA_QUIZ_DIR.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
