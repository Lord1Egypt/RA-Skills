## Description: <br>
Adaptive spaced repetition engine using the FSRS-6 algorithm that manages markdown flashcard reviews and schedules study sessions from recall ratings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tylerbittner](https://clawhub.ai/user/tylerbittner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain markdown-based flashcards, list due reviews, record review ratings, and keep study intervals updated with FSRS scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and edit the markdown flashcard file selected by the user. <br>
Mitigation: Use a dedicated cards file or folder, keep backups or version control for important notes, and confirm write actions when recording reviews. <br>


## Reference(s): <br>
- [FSRS Algorithm Reference](references/fsrs-algorithm.md) <br>
- [open-spaced-repetition/py-fsrs](https://github.com/open-spaced-repetition/py-fsrs) <br>
- [Formation](https://formation.dev) <br>
- [ClawHub Skill Page](https://clawhub.ai/tylerbittner/spaced-repetition-teaching) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and updated markdown flashcard content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update the user-specified markdown flashcard file when recording reviews or adding cards.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
