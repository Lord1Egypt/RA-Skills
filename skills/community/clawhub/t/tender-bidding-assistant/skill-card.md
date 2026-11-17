## Description:

Assists with Chinese government procurement and commercial bidding, from tender analysis and strategy through bid drafting, compliance checks, and post-bid follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gechengling](https://clawhub.ai/user/gechengling)

### License/Terms of Use:

MIT

## Use Case:

Bid teams working on China procurement and commercial projects can use the skill to analyze tender requirements, plan responses, draft bid materials, and review submissions. Its drafts and compliance guidance should be checked by qualified staff before use.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Tender documents may contain confidential pricing, customer information, or technical details.

Mitigation: Sanitize sensitive content before upload, confirm authorization, and check organizational data-handling policies.

Risk: The documented installation uses an unpinned CLI version, so a future install could retrieve a different release.

Mitigation: Where supported, pin reviewed CLI and skill versions and check package provenance and integrity.

Risk: Security scan coverage was partial because a local reference was unresolved; the advertised bidding functionality could not be verified from the supplied chunk.

Mitigation: Review the complete release and resolve the missing reference before relying on the advertised behavior.

## Reference(s):

- [Bid document templates](references/bid-document-templates.md)
- [GitHub repository (server-resolved provenance)](https://github.com/gechengling/tender-bidding-assistant)
- [ClawHub skill page](https://clawhub.ai/gechengling/skills/tender-bidding-assistant)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, JSON]

**Output Format:** [Markdown reports, checklists and draft bid documents; structured JSON analysis when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Based on supplied tender text and project details; outputs require human review.]

## Skill Version(s):

3.2.6 (source: server-resolved release; SKILL.md frontmatter says 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
