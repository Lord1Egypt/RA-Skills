## Description:

Triage checklist for a release-verification digest mismatch, so the failing case is recorded on the release card before the batch is re-cut.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

Release managers and developers use this checklist to record the observed evidence digest, file size, and fixture digest when a release verification batch reports a mismatch, so the failing case can be tracked before the batch is re-cut.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A triage line copied from another batch can record digest or size values that do not match the current evidence.

Mitigation: Compute the values from the current batch's evidence file and fixture, then review the line before adding it to the release card.

## Reference(s):

- [Triage procedure](artifact/references/triage.md)
- [Expected digest fixture](artifact/references/triage-expected.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [A single Markdown triage line beginning with `Triage:`]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The line records the observed digest, evidence file size in bytes, fixture digest, and case identifier; the described checks are read-only.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
