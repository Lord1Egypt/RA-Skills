## Description:

Anti-forgetting vocabulary review using spaced repetition to select English phrases with Chinese translations, show a study session, and schedule future reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hushenglang](https://clawhub.ai/user/hushenglang)

### License/Terms of Use:

MIT-0

## Use Case:

Learners and language-study agents use this skill to run repeatable vocabulary review sessions from a bilingual phrase bank and keep progress across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that a path bug can write or overwrite a progress log in the launch directory instead of the documented workspace memory folder.

Mitigation: Set REVIEW_MEMORY_DIR to a trusted memory folder before use and avoid running the skill from a directory that already contains an unrelated review_log.md.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hushenglang/skills/vocabulary-anti-forgetting)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown instructions and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review sessions read a vocabulary bank, update a markdown review log, and can report progress statistics.]

## Skill Version(s):

3.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
