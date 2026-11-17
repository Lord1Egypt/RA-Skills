## Description:

Packages QA requirements, scenarios, boundaries, and risks into a structured, source-labeled AI context package for downstream test-case generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA practitioners and developers use this skill to consolidate upstream testing analysis into a four-layer context package before prompting an AI to generate test cases. It flags missing inputs and distinguishes supplied facts, inferences, and assumptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unverified assumptions or missing upstream inputs could distort later test cases.

Mitigation: Label each item as supplied, inferred, or assumed; disclose missing inputs and confirm assumptions before downstream use.

Risk: An optional command to install the broader skill set runs third-party code.

Mitigation: Treat installation as optional and verify the package source and version before running it.

Risk: Uploaded requirements or fetched URLs may expose unrelated information.

Mitigation: Provide only files or URLs relevant to the QA context package.

## Reference(s):

- [Context package template](artifact/assets/context-package.md)
- [Context window adaptation](artifact/references/window-adaptation.md)
- [ClawHub release page](https://clawhub.ai/kokxi/skills/qa-ai-context-engineering)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Structured four-layer AI context package with source labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports missing upstream inputs and fallback guidance; does not generate test cases.]

## Skill Version(s):

1.8.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
