## Description: <br>
学习DNA档案 helps an OpenClaw tutoring agent create, update, inspect, pause, and delete a consent-based student learning profile for personalized academic support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qizhitang](https://clawhub.ai/user/qizhitang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, guardians, and tutoring agents use this skill to maintain a controlled learning profile that supports personalized follow-up across sessions. It is intended for learning-memory workflows where profile creation, updates, sharing, and deletion remain gated by explicit user consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive student learning, behavior, interest, and emotion-related observations across sessions. <br>
Mitigation: Require explicit profile opt-in, separate consent for emotion tracking, minimal necessary collection, and easy view, edit, delete, and pause controls before use. <br>
Risk: Profile updates from ordinary conversation could occur without a clear consent boundary. <br>
Mitigation: Add an active consent check and confirmation step before automatic profile updates, reminders, or cross-skill sharing. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/qizhitang/xiaozhi-learning-dna) <br>
- [DNA profile schema](schemas/dna-profile.schema.json) <br>
- [DNA schema README](schemas/README.md) <br>
- [DNA template](references/dna-template.md) <br>
- [Growth milestones reference](references/growth-milestones.md) <br>
- [Cross-subject connections reference](references/cross-subject-connections.md) <br>
- [Published DNA profile schema URL](https://xiaozhi-skills.openclaw.dev/schemas/dna-profile.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Configuration] <br>
**Output Format:** [Markdown guidance and structured JSON profile records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Profile data should follow the bundled JSON Schema and consent controls.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
