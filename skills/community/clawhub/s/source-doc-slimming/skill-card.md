## Description:

Slim down an oversized "always-read" source document — a single source of truth, a registry, a config, a published skill/README, or a rule document — without deleting any content. Use when a file that must be read under time pressure has grown so large that its load-bearing parts get skimmed past, when a review or incident concludes that something important was missed because of file volume, when a document accretes a new section after every incident, or when someone sets a size target for a file and you need to check whether that target is arithmetically reachable. Moves long narrative, chronology and incident history into a companion file, leaves an operating spine plus pointers inline, adds a shape guard so the file cannot silently re-inflate, and proves the move was lossless by replaying the original text line-by-line against the companion. Do not use for ordinary editing or for trimming prose that is genuinely dead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining large always-read source documents use this skill to move narrative and history into a companion file while keeping operative rules easy to find. It guides them through adding a shape guard and checking that moved content is preserved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changed or incomplete content could pass the content verification check; the scan evidence is partial.

Mitigation: Before installing, consider whether you can tolerate this risk. Review the moved content and the verification results, and assess referenced material because the partial scan does not establish that all of it was checked.

## Reference(s):

- [source-doc-slimming on ClawHub](https://clawhub.ai/haiyangchenbj/skills/source-doc-slimming)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [An abridged source document with a companion reference, plus verification and supporting scripts where needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Moved text is intended to remain verbatim; a line-by-line check is used to verify preservation.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
