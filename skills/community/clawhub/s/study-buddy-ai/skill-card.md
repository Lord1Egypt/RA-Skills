## Description: <br>
Study Buddy helps users study by creating flashcards, quizzes, notes, study plans, Pomodoro sessions, spaced repetition reviews, topic explanations, practice questions, and progress summaries while keeping data local. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkpareek0315](https://clawhub.ai/user/mkpareek0315) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Students and self-directed learners use this skill to manage local study workflows: create and review flashcards, take quizzes, save notes, build study plans, track progress, and get topic explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Study notes, flashcards, quiz results, plans, and history are saved locally on the user's device. <br>
Mitigation: Avoid storing sensitive personal information in Study Buddy data and review or delete local files under ~/.openclaw/study-buddy/ when they are no longer needed. <br>
Risk: Broad phrases such as "explain" or "review" may activate the skill outside an intended study context. <br>
Mitigation: Apply the skill only when the surrounding conversation is clearly about studying, learning, reviewing material, or managing study data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mkpareek0315/study-buddy-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with code blocks and local JSON file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update study data under ~/.openclaw/study-buddy/.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
