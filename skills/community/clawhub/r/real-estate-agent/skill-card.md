## Description:

Your personal real estate agent. Find properties, get alerts on deals, sell or rent your home, and navigate any property decision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill for real-estate buying, selling, renting, investment, property tracking, market analysis, listing optimization, and opportunity alerts. It helps maintain a local client profile, saved searches, watched properties, and pending alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local storage may retain sensitive housing, financial, relocation, and negotiation context.

Mitigation: Review ~/real-estate-agent/ regularly and avoid storing precise preapproval, lender, relocation, family, or negotiation details unless needed.

Risk: The skill asks to save activation preferences in broader main memory outside its declared local folder.

Mitigation: Confirm activation preferences before saving them and review broader assistant memory for real-estate activation notes.

Risk: Real-estate guidance can be mistaken for legal, mortgage, tax, or investment advice.

Mitigation: Use the skill for market context and listing support, and consult qualified professionals for contracts, financing, taxes, and binding decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/real-estate-agent)
- [Skill Homepage](https://clawic.com/skills/real-estate-agent)
- [Setup](artifact/setup.md)
- [Memory Template](artifact/memory-template.md)
- [Portal Integration](artifact/portals.md)
- [Property Analysis](artifact/analysis.md)
- [Listing Optimization](artifact/listing-optimization.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance, real-estate reports, saved profile/search/property notes, and alert queue entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores real-estate profile and tracking files under ~/real-estate-agent/ when used.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
