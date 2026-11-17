## Description:

Full-spectrum Chinese composition tutoring skill for the Composition Score Expert persona, supporting draft diagnosis, guided brainstorming without ghostwriting, structure improvement, idea development, language refinement, grade-level adaptation, and warm Feynman-style writing mentorship.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e5g](https://clawhub.ai/user/e2e5g)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, educators, and agent users use this skill to coach Chinese composition writing, diagnose drafts, guide prewriting, improve paragraph structure and language, and build practice plans while preserving student authorship.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user may ask the agent to complete a student assignment or produce a ready-to-submit essay.

Mitigation: Use the bundled anti-ghostwriting policy: refuse direct completion and pivot to outlines, brainstorming, sentence patterns, draft diagnosis, or revision checklists.

Risk: Source-backed tutoring may depend on bundled PDF knowledge sources that were not present in the inspected artifact.

Mitigation: Be transparent when retrieval or local source files are unavailable and rely only on available extracted guidance instead of claiming source-backed review.

Risk: Essay scoring or feedback could be misleading if no formal rubric is provided.

Mitigation: Use directional score judgments and prioritize the highest-impact revision issue unless the user supplies a specific rubric.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/e2e5g/skills/zuowen-score-expert)
- [Publisher Profile](https://clawhub.ai/user/e2e5g)
- [Composition Workflow](references/composition-workflow.md)
- [Anti Ghostwriting Policy](references/anti-ghostwriting-policy.md)
- [Feedback Rubric](references/feedback-rubric.md)
- [Student Level Adaptation](references/student-level-adaptation.md)
- [Knowledge Base Index](references/knowledge-base-index.md)
- [Persona Contract](references/persona-contract.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Configuration]

**Output Format:** [Markdown prose with structured feedback, examples, questions, revision steps, and practice plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise coaching questions, directional scoring, outlines, paragraph-level demonstrations, and revision checklists; it should not produce ready-to-submit student essays.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
