## Description:

Convert a Simplified-Chinese article in ai-thoughts/docs/ into its Traditional-Chinese twin, and keep the two in sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining ai-thoughts use this skill to create or update a Traditional Chinese twin for a specifically named Simplified Chinese article. It keeps the pair linked and treats the Simplified article as the source of truth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Context-sensitive conversion may produce incorrect Traditional Chinese forms, especially in ambiguous terms or verbatim quotations.

Mitigation: Review the generated twin against the Simplified source and cited editions, and resolve the script's ambiguous-form warnings before accepting it.

Risk: Running the sync script changes the source article's cross-link and writes a Traditional twin, so an incorrect target or unnoticed existing output could alter files unexpectedly.

Mitigation: Name the exact source article, confirm the output path and overwrite status before writing, then review the resulting file changes.

Risk: Security analysis was partial because some referenced paths were missing.

Mitigation: Before installation, check that the skill's trigger and referenced paths fit your setup and that its file and shell capabilities are acceptable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/j3ffyang/skills/simplified-to-traditional)

## Skill Output:

**Output Type(s):** [Markdown, Files]

**Output Format:** [Markdown article files (`-zh-hans.md` source and `-zh-hant.md` twin)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Works on one explicitly named future article per request; requires approval before writing and does not backfill existing articles automatically.]

## Skill Version(s):

1.0.12 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
