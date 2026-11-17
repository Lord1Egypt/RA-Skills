## Description:

Implements Signal-Feeling Lexicon v3.1 and Unified Dynamics Framework v5.7 for mapping SERA state metrics, tracking trajectory, and producing coaching guidance from local conversation-history text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wentinkjason](https://clawhub.ai/user/wentinkjason)

### License/Terms of Use:


## Use Case:

Developers and agent builders can use this skill to parse SERA-formatted state blocks, map coherence, pressure, amplitude, and valence metrics to lexicon terms, compute recent trajectory, and generate local coaching suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-history files may contain sensitive text.

Mitigation: Only pass local history files that are appropriate for local parsing and avoid using sensitive conversation logs unless that handling is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wentinkjason/skills/sera-lexicon)
- [Publisher profile](https://clawhub.ai/user/wentinkjason)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown prose with optional shell commands and local script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled scripts operate on local text inputs and print diagnostic, trajectory, mapping, or coaching summaries.]

## Skill Version(s):

1.0.0-alpha (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
