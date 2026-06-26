## Description: <br>
Build and review vocabulary from books, podcasts, and daily encounters with reading-session support, word collection, pronunciation guidance, spaced repetition, quizzes, and progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[winlinvip](https://clawhub.ai/user/winlinvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and reading assistants use this skill to capture unfamiliar words, generate clear pronunciation and meaning notes, practice words through a three-step flow, and schedule spaced-review quizzes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vocabulary entries and quiz history may include sensitive reading excerpts or personal information saved in the workspace tracker. <br>
Mitigation: Avoid storing sensitive excerpts or personal details in memory/vocabulary.md, and review tracker contents before sharing the workspace. <br>
Risk: Scheduled quizzes can create unwanted recurring prompts if configured for an unsuitable channel or frequency. <br>
Mitigation: Enable scheduled quizzes only for welcome delivery channels and frequencies, and keep sleep-hour and pending-quiz checks in the cron message. <br>


## Reference(s): <br>
- [Why I Stopped Using Flashcards and Started Using AI](https://youtu.be/wjWrVpZZXSg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown word cards, vocabulary tracker entries, quiz prompts, pronunciation guidance, and cron setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes vocabulary data to memory/vocabulary.md and references user-provided audio clips under docs/tts-fr/.] <br>

## Skill Version(s): <br>
1.1.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
