## Description:

Capture authorized original thinking and notable entity facts from an explicitly scoped conversation into a designated knowledge destination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjjhenriksen](https://clawhub.ai/user/jjjhenriksen)

### License/Terms of Use:

MIT-0

## Use Case:

External users can capture original ideas and notable entity facts from authorized conversations into an approved knowledge destination, with scope and audience controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent capture could expose private or sensitive details if the approved scope, destination, audience, or retention is unclear.

Mitigation: Require explicit authorization for each of those boundaries before writing; skip capture when any is ambiguous and exclude secrets and sensitive details.

Risk: Guidance to act “without checking” may not fit a user's preferences.

Mitigation: Assess whether that guidance fits the user's preferences before relying on it; the security review rates the release benign but notes that benign does not mean risk-free.

## Reference(s):

- [ClawHub release](https://clawhub.ai/jjjhenriksen/skills/signal-detector)
- [Scoped capture examples](artifact/references/capture-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Knowledge-base notes]

**Output Format:** [Short notes using exact permitted excerpts with source context and date; optional one-line capture receipt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Capture only within explicit scope; omit secrets and sensitive details.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
