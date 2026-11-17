## Description:

Retrieve existing PyAI Recap summaries or submit timed agent/customer transcripts for summarization with the PyAI CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atomsai](https://clawhub.ai/user/atomsai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using PyAI Recap can retrieve an existing call summary or request a summary and action items from a supplied, timed agent/customer transcript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitting a transcript sends it to the selected PyAI project and may incur usage charges.

Mitigation: Confirm the intended project and that you are authorized to share the transcript; review expected usage before submitting.

Risk: The external PyAI CLI was not audited in this artifact review.

Mitigation: Review the CLI and provider security posture before use, and install the CLI only from a trusted source.

## Reference(s):

- [PyAI Recap](https://pyai.com/mcp)
- [PyAI CLI documentation](https://pyai.com/cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries and action items, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves speaker attribution and uncertainty; does not automatically carry out follow-up actions.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
