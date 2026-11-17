## Description:

Collects bounded, traceable web observations for YouTube captions and comments, Google AI citations, Xiaohongshu notes, and identified product offers through supplied connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swiftadviser](https://clawhub.ai/user/swiftadviser)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to gather source-linked web observations and access diagnostics before retrieval, customer-feedback analysis, citation comparisons, or price monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proxy or MCP secrets could be exposed during live collection.

Mitigation: Run in an isolated environment, supply secrets through approved private channels, and keep credentials out of commands and shared outputs.

Risk: Bounded observations may be mistaken for complete access, representative sampling, verified regional effects, or checkout prices.

Mitigation: Review coverage and gaps, set Google language and country explicitly, and verify consequential claims separately.

Risk: Pinned dependencies or changing source surfaces may affect live collection.

Mitigation: Review dependencies before live runs and confirm current source behavior rather than treating fixture output as live proof.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/swiftadviser/skills/proxylane-web-evidence)
- [Source modes and boundaries](artifact/references/source-modes.md)
- [Output contract](artifact/references/output-contract.md)
- [Running the collectors](artifact/references/running.md)
- [Known gaps](artifact/references/KNOWN_GAPS.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance and JSON observations with redacted evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bounded collection with source identity, observation time, coverage, diagnostics, and evidence hashes]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
