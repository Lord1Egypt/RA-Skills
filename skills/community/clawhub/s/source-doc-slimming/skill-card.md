## Description:

Slim down an oversized "always-read" source document — a single source of truth, a registry, a config, a published skill/README, or a rule document — without deleting any content. Use when a file that must be read under time pressure has grown so large that its load-bearing parts get skimmed past, when a review or incident concludes that something important was missed because of file volume, when a document accretes a new section after every incident, or when someone sets a size target for a file and you need to check whether that target is arithmetically reachable. Moves long narrative, chronology and incident history into a companion file, leaves an operating spine plus pointers inline, adds a shape guard so the file cannot silently re-inflate, and proves the move was lossless by replaying the original text line-by-line against the companion. Do not use for ordinary editing or for trimming prose that is genuinely dead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to restructure oversized, frequently read source documents while preserving their content, keeping operating guidance easy to find, and adding checks against future drift.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the instructions to modify files conflict with the declared read-only permission; the scan was partial and its evidence is incomplete.

Mitigation: Before installing, review which files the workflow would change and confirm you intend to grant the required write access.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/haiyangchenbj/skills/source-doc-slimming)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [Markdown, source files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a companion document, validation helpers, and updates to an existing project gate.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
