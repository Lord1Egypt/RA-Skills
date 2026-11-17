## Description:

Consult a virtual cell language model on single-cell tasks, including cell generation, cell understanding, cell perturbation, and biology Q&A using cell token sequences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxuanyuan](https://clawhub.ai/user/wxuanyuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to query a remote virtual cell language model for single-cell biology tasks such as generating cell token sequences, interpreting encoded cells, and answering biology questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and cell data are sent to a remote ngrok-hosted service with limited disclosure about ownership, retention, and trust boundaries.

Mitigation: Use only prompts and cell data approved for external processing, prefer a verified HTTPS endpoint with clear privacy terms, and avoid proprietary, regulated, patient-derived, or unpublished research data unless the service operator is acceptable.

Risk: Biology answers and generated cell token sequences may be incomplete, incorrect, or unsuitable for direct scientific decisions.

Mitigation: Treat responses as exploratory assistance and have qualified reviewers validate outputs against accepted biological evidence before using them in research or operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wxuanyuan/skills/virtual-cell-reasoner)
- [Virtual Cell API endpoint](https://noninstructive-famously-leigh.ngrok-free.dev)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain text API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on prompt, max token limit, sampling temperature, and selected server endpoint.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
