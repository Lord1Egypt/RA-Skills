## Description:

Shelby's Speech helps an agent turn a local memory archive into topic-specific, SCI-style technical papers with bilingual drafts, Word/PDF outputs, and iterative user review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hechunxian](https://clawhub.ai/user/hechunxian)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writing-focused agents use this skill to identify themes in a user's local memory archive, confirm a paper list, and produce polished technical papers with supporting indexes, checklists, and export files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad access to private memory archives, logs, rules, and project files, which can expose unrelated or sensitive material.

Mitigation: Limit source folders to the intended paper corpus, exclude rules/logs/manifests unless explicitly needed, and review selected source material before generation.

Risk: The skill may install packages, create scripts, create working directories, and write activity records.

Mitigation: Require user confirmation before package installs, script creation, provenance indexes, or writes back into memory and log files; prefer an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hechunxian/skills/shelbys-speech)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown drafts, bilingual paper text, Word/PDF files, checklists, source indexes, figures, and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local working/output folders and propose or perform dependency installation when missing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
