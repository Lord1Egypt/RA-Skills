## Description:

Academic writing revision advisor for the Results section of psychology and STEMM research papers. Checks claim-hedging alignment, causal language appropriateness, statistical reporting completeness, and interpretation boundaries. Triggers when the user asks to review, revise, or check a Results section draft, or mentions hedging, claim strength, overclaiming, or causal language in academic writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seulkilu](https://clawhub.ai/user/seulkilu)

### License/Terms of Use:

MIT-0

## Use Case:

External academic authors, editors, and research teams use this skill to audit Results-section drafts for claim strength, hedging, causal language, interpretation leakage, and subjective wording. It provides sentence-level findings, 1-5 dimension scores, example-based comparisons, and concrete revision suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the audit for validation of the underlying statistical analysis.

Mitigation: Present outputs as reporting and language guidance, and route statistical validity, p-hacking, assumptions, and test appropriateness to qualified statistical review.

Risk: Causal-language judgments can be overly conservative when the research design is not provided.

Mitigation: Ask for the study design before relying on causal-language flags, especially for experimental, correlational, cross-sectional, or longitudinal work.

Risk: Outputs may include Chinese rubric language unless the calling workflow constrains the presentation language.

Mitigation: Specify the desired output language when invoking the skill in English-only or localized review workflows.

## Reference(s):

- [Scoring Rubric](references/rubric.md)
- [Diagnostic Checklist](references/checklist.md)
- [Curated Psychology Examples](references/examples/examples_memberF.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit with six standardized sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes 1-5 dimension scores, flagged draft evidence, example-based comparisons, revision suggestions, and priority levels.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
