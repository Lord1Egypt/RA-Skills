## Description:

Scores and diagnoses Chinese Ruankao advanced-qualification essays across five qualification tracks, with tailored improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nieen](https://clawhub.ai/user/nieen)

### License/Terms of Use:

MIT-0

## Use Case:

Ruankao advanced-qualification candidates use this skill to score a submitted essay against the relevant qualification rubric, identify weaknesses, and prioritize revisions. It can also review a single scoring dimension or compare a revised draft with an earlier version.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for general Chinese essay-scoring requests outside Ruankao exams.

Mitigation: Confirm the essay is for a Ruankao advanced qualification before applying its rubric.

Risk: An agent might modify a local draft while providing scoring feedback.

Mitigation: Allow file edits only when the user explicitly requests changes to the draft.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nieen/skills/ruankao-essay-scoring)
- [General and system architect scoring rubric](artifact/references/scoring-rubric.md)
- [Project manager scoring rubric](artifact/references/scoring-rubric-pm.md)
- [Systems analyst scoring rubric](artifact/references/scoring-rubric-sa.md)
- [Network planner scoring rubric](artifact/references/scoring-rubric-ne.md)
- [Systems planning and management scoring rubric](artifact/references/scoring-rubric-sp.md)
- [Scoring report template](artifact/references/report-template.md)
- [Common scoring errors and troubleshooting](artifact/references/common-errors.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Chinese-language Markdown scoring report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dimension scores, an essay checklist, an overall diagnosis, and prioritized revision advice.]

## Skill Version(s):

1.5.2 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
