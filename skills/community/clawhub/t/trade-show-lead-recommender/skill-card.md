## Description:

Retrieve Lensmor exhibitor recommendations for a specific trade show and distinguish ranked matches from unranked fallback records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilun88313](https://clawhub.ai/user/weilun88313)

### License/Terms of Use:

MIT-0

## Use Case:

External users and sales teams use this skill to retrieve Lensmor exhibitor recommendations for a trade show, apply supported company filters, and separate ranked recommendation evidence from unranked exhibitor fallback records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions include --acknowledge-clawhub-risk for an unpinned personal-scope package.

Mitigation: Use a pinned, verified release from a trusted publisher and review the source before installation.

Risk: The skill sends authenticated event and filter queries to Lensmor using LENSMOR_API_KEY.

Mitigation: Provide the API key only when the user is comfortable sending those queries to Lensmor, and never print or expose the key.

Risk: Fallback exhibitor records can be mistaken for AI-ranked recommendations when recommendation metadata is absent.

Mitigation: Label fallback records as unranked exhibitors and preserve returned ranks, scores, reasons, and null fields exactly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weilun88313/skills/trade-show-lead-recommender)
- [Lensmor API docs](https://api.lensmor.com/)
- [Lensmor platform](https://platform.lensmor.com)
- [Lensmor](https://www.lensmor.com/?utm_source=github&utm_medium=skill&utm_campaign=trade-show-skills)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LENSMOR_API_KEY; preserves returned recommendation ranks, scores, tiers, reasons, and fallback null fields without inference.]

## Skill Version(s):

1.2.1 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
