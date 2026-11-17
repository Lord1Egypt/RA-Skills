## Description:

Smart Leaner is a personal learning assistant that explains concepts with diagrams and examples, tracks mastery, schedules reviews, archives notes, and adapts teaching style from user feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hexavi8](https://clawhub.ai/user/hexavi8)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to learn technical or non-technical topics through calibrated explanations, structured notes, quizzes, and spaced-review prompts. It is suited for ongoing study workflows where the user wants progress and preferences remembered across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps a persistent local learning profile, preferences, notes, quiz records, and review plans under smart-learner/.

Mitigation: Install only when local retention is acceptable, periodically review or delete the stored files, and avoid using the skill with sensitive documents unless derived notes and preferences may be saved.

Risk: Broad learning-related triggers can activate the skill in many educational or document-analysis conversations.

Mitigation: Prefer explicit invocation and confirm when the skill should save generated notes, preference changes, or mastery updates.

Risk: The skill may use web search for current materials, which can introduce conflicting or low-quality source material into explanations.

Mitigation: Review cited sources and treat explanations as study guidance, especially when web results conflict with existing knowledge.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hexavi8/skills/smart-learner)
- [Publisher profile](https://clawhub.ai/user/hexavi8)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown explanations, Mermaid diagrams, quiz debriefs, and learning-note file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learning memory, preference, note, quiz, and review-plan files under smart-learner/ when confirmed by the user.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
