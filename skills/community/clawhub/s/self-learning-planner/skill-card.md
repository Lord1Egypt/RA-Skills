## Description:

Self Learning Planner helps users design personalized, evidence-informed learning paths, study schedules, resource lists, reflection prompts, and optional progress artifacts for new topics or skill-development goals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thedataq](https://clawhub.ai/user/thedataq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and learning-focused agents use this skill to turn a target topic, current level, time budget, and desired outcome into a structured self-learning plan. It is suited for study-roadmap design, prerequisite assessment, resource selection, weekly planning, progress tracking, and troubleshooting common self-learning obstacles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to append newly found web-search results into its bundled resource database.

Mitigation: Require explicit user or administrator approval before modifying installed skill files, and require source validation plus provenance notes for any resource-database update.

Risk: Learning plans may rely on resource recommendations that become outdated or are not appropriate for a user's level or goal.

Mitigation: Ask the user to confirm learning goals, constraints, and resource preferences, then verify current resource availability before presenting a final plan.

## Reference(s):

- [Learning Science Core Principles](references/learning-science.md)
- [Five-Step Self-Learning Framework](references/self-learning-framework.md)
- [Topic Mapping Guide](references/topic-mapping-guide.md)
- [Self-Learning Obstacles and Troubleshooting](references/obstacles-troubleshooting.md)
- [Learning Resource Database](resources/resource-database.md)
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [Exercism Python Track](https://exercism.org/tracks/python)
- [LeetCode](https://leetcode.com/)
- [Refactoring UI](https://www.refactoringui.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown by default, with optional HTML checklist code and calendar-reminder guidance when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include phased learning paths, weekly templates, daily checklists, method tags, resource recommendations, milestone criteria, reflection prompts, and progress-tracking plans.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
