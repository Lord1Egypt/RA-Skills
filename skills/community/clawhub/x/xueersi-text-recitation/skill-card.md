## Description:

Xueersi Text Recitation Coach helps K-9 students memorize Chinese textbook passages and classical poems through fill-in-the-blank drills, paragraph prompts, dictation quizzes, and mnemonics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouzhi-tal](https://clawhub.ai/user/zhouzhi-tal)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, parents, and educators use this skill to run guided recitation practice for Chinese K-9 textbook passages and classical poems, including blanks, hints, mnemonics, and dictation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic trigger phrases may activate recitation-coach behavior when the user intended a different task.

Mitigation: Confirm the user wants recitation practice when the request is ambiguous, especially for broad prompts such as asking for a hint or a test.

Risk: Practice content can be less useful if the requested passage title maps to a different textbook version than the learner expects.

Mitigation: Ask for the passage text or textbook edition when the title alone is ambiguous, then base drills and feedback on that supplied text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouzhi-tal/skills/xueersi-text-recitation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style tutoring prompts, fill-in-the-blank exercises, mnemonic summaries, dictation quizzes, and feedback.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code or external tools; outputs depend on user-supplied titles or passage text.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
