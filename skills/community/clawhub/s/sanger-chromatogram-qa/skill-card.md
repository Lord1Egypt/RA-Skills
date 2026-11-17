## Description:

Guides agents through Sanger chromatogram QA workflows with explicit assumptions, bounded execution, and reviewable outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and lab informatics users can use this skill to structure Sanger sequencing review tasks such as mutation verification, clone confirmation, genotyping QC, and SNP validation. The packaged implementation should be treated as a draft aid rather than a validated chromatogram QA system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may rely on prototype scientific output for mutation confirmation or other Sanger QA decisions.

Mitigation: Require validation with known chromatograms and make clear that results need expert review before they inform scientific or operational decisions.

Risk: The packaged code does not provide validated AB1 parsing or substantive mixed-peak detection.

Mitigation: Add real AB1 parsing, mixed-peak detection, and input validation before using the skill as a chromatogram QA tool.

Risk: The NumPy dependency is unpinned.

Mitigation: Install dependencies in an isolated environment and use a pinned or locked dependency set before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and structured QA findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should separate assumptions, workflow, results, risks, unresolved items, and validation needs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
