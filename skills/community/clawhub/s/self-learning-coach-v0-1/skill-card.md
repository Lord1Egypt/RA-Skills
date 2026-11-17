## Description:

Business self-learning coach for AI agents that helps employees turn business topics, documents, Feishu materials, web materials, or local sources into learning paths, HTML lessons, teach-back dialogue, active recall, critiques, source notes, and next-step study plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzj997](https://clawhub.ai/user/zzj997)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business learners use this skill to transform an internal process, role, workflow, concept, or selected source material into a structured self-study experience. Agents can plan a short learning path, create HTML lesson pages, track sources and progress, and support teach-back review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read user-provided or authorized business materials and include source-derived content in generated learning artifacts.

Mitigation: Use it only with materials the user is comfortable granting read access to, and review generated HTML or delivered files before forwarding them.

Risk: Generated lessons and local progress/source indexes can reflect internal learning context or sensitive source titles.

Mitigation: Avoid exposing private URLs, local paths, account traces, or permission-sensitive metadata in shared lessons and source records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzj997/skills/self-learning-coach-v0-1)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance and self-contained HTML lesson files, with optional Markdown source and progress records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local HTML lessons and lesson tracking files when file tools are available; generated lessons are intended for review before sharing.]

## Skill Version(s):

0.1.12 (source: server release metadata and skill title)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
