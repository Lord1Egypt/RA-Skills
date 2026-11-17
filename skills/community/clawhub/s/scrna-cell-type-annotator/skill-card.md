## Description:

Auto-annotate cell clusters from single-cell RNA data using marker genes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to annotate post-clustering single-cell RNA cell clusters from marker genes, including common post-clustering, cross-study comparison, novel cell type discovery, and atlas construction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release declares an unpinned pandas dependency, which can reduce reproducibility and introduce supply-chain drift across installations.

Mitigation: Install in an isolated virtual environment and remove pandas if unused or pin it to a reviewed version before operational use.

Risk: The skill runs a local Python script and may read input files or write outputs in the workspace during annotation workflows.

Mitigation: Validate input and output paths before execution and run the script in a sandboxed workspace with only the required files available.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell commands and plain-text annotation results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should identify inputs, assumptions, workflow, predictions, confidence levels, alternatives, risks, and unresolved checks when relevant.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
