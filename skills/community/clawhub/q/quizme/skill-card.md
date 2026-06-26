## Description: <br>
Adaptive tech quiz skill for OpenClaw that asks one multiple-choice coding or computer science question at a time, adapts difficulty from the user's answers, and tracks topics and progress across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericshi123](https://clawhub.ai/user/ericshi123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, students, and technical learners use this skill to practice coding and computer science topics through adaptive multiple-choice quiz sessions with explanations and persistent progress tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores quiz topics, progress, and generated question banks locally under ~/quizme. <br>
Mitigation: Install only if local storage of quiz topics and progress is acceptable, and review or remove ~/quizme data when it is no longer needed. <br>
Risk: Broad trigger phrases such as "teach me X" or "start a quiz" may activate the skill unexpectedly. <br>
Mitigation: Prefer explicit activation such as /quizme or "quiz me on Python". <br>
Risk: The bundled helper script can call OpenAI with OPENAI_API_KEY if it is run manually, even though normal skill operation generates questions inline. <br>
Mitigation: Do not run scripts/generate_bank.py unless external question generation with an OpenAI API key is intended. <br>


## Reference(s): <br>
- [QuizMe topic coverage guide](references/topics.md) <br>
- [QuizMe on ClawHub](https://clawhub.ai/ericshi123/quizme) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration] <br>
**Output Format:** [Markdown quiz prompts with optional code blocks and local JSON question-bank/progress files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One question per message; stores topics, progress, and generated question banks under ~/quizme.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
