## Description:

Adaptive tech quiz skill for OpenClaw that asks one multiple-choice coding or CS question at a time, explains answers, adapts difficulty, and tracks topics and progress across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericshi123](https://clawhub.ai/user/ericshi123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and learners use QuizMe to practice coding and computer science topics through adaptive multiple-choice quiz sessions. The skill is intended for technical study across Python, JavaScript, SQL, system design, algorithms, networking, Git, Docker, APIs, and general CS concepts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates local files under ~/quizme/ that record quiz topics, generated questions, and progress.

Mitigation: Install and run it only if local persistence of quiz history is acceptable, and review or remove ~/quizme/ files when that history should not be retained.

Risk: The bundled generator script can use the OpenAI API and OPENAI_API_KEY if run directly.

Mitigation: Avoid running the script unless API use is intentional and the dependency, network behavior, and API-key handling have been reviewed.

## Reference(s):

- [Per-Topic Coverage Guide](references/topics.md)
- [QuizMe ClawHub Release Page](https://clawhub.ai/ericshi123/skills/quizme)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown quiz prompts and explanations with JSON question-bank files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local topic, progress, and question-bank state under ~/quizme/.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
