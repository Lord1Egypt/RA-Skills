## Description:

Helps verify the cryptographic integrity of skill updates by checking whether each version is signed by the same key as the original install, detecting key changes, signature gaps, and unsigned updates that may indicate a compromised or transferred skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to audit skill update histories for signature continuity, key changes, unsigned versions, and chain-of-custody gaps. Its report helps decide whether an update path needs publisher follow-up, content review, or version pinning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat a clean or continuous signature report as proof that update content is safe.

Mitigation: Treat the report as advisory evidence and still review signed update content for unsafe behavior.

Risk: Missing version history, signing records, or historical key fingerprints can make chain-of-custody findings incomplete.

Mitigation: Provide available version-signing metadata and treat absent metadata as an audit gap rather than evidence of continuity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/update-signature-verifier)
- [Publisher profile](https://clawhub.ai/user/andyxinweiminicloud)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown signature continuity report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes version-by-version signing key comparison, key change events, unsigned version detection, chain-of-custody status, and recommended actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
