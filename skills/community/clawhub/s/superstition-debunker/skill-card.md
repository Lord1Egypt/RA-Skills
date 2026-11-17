## Description:

Identifies folklore-style rhetoric in forwarded claims and suggests questions to help verify them, without determining whether the claims are true.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users and educators can triage chain messages and viral claims for common folklore patterns, then ask focused questions before sharing or investigating further.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional logging retains the first 120 characters of pasted claims, which may include personal or sensitive details.

Mitigation: Avoid --log for sensitive claims; review and remove local logs when no longer needed.

Risk: Pattern scores may be mistaken for factual verdicts on a claim.

Mitigation: Present scores as structural signals only and verify consequential claims with primary sources or qualified professionals.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/voronindenis5/skills/superstition-debunker)
- [Folklore Fingerprint Catalog](references/pattern-catalog.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text claim analysis with scores, matched patterns, and verification questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional local analysis log and aggregate pattern statistics]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
