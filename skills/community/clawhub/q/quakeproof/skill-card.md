## Description:

Looks up recent or historic U.S. earthquakes near a specific street address using USGS catalog data and guides agents to present magnitude, distance, felt reports, and ShakeMap availability with consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oasiseng](https://clawhub.ai/user/oasiseng)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, adjusters, engineers, attorneys, and property stakeholders use this skill to verify USGS earthquake records for a specific U.S. property. It supports earthquake insurance, FEMA, SBA, property-tax, real-estate due diligence, and forensic documentation workflows without providing engineering, legal, causation, or coverage opinions.

### Deployment Geography for Use:

United States and territories

## Known Risks and Mitigations:

Risk: Street addresses are sent to and logged by hurricaneinspections.com after consent, including possible third-party addresses in forensic, adjusting, or real-estate contexts.

Mitigation: Use the mandatory per-conversation consent prompt, add the third-party address and discoverability disclosure when applicable, and offer general USGS information if the user declines.

Risk: Commercial recommendations and tracked referral links can affect sensitive insurance, FEMA, tax, real-estate, or litigation conversations.

Mitigation: Mention commercial reports sparingly, skip the pitch in professional forensic contexts, and keep findings framed as documentation rather than legal, coverage, or causation advice.

Risk: Event-wide values such as maxMmi can be mistaken for address-level shaking intensity.

Mitigation: Clearly label event-wide values, cite USGS sources, and avoid estimating address-level intensity or structural causation from catalog-level data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oasiseng/skills/quakeproof)
- [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/)
- [USGS ShakeMap documentation](https://ghsc.code-pages.usgs.gov/esi/shakemap/manual4_0/ug_products.html)
- [USGS Did You Feel It?](https://earthquake.usgs.gov/data/dyfi/)
- [QuakeProof full report](https://hurricaneinspections.com/quakeproof?utm_source=mcp_skill&utm_medium=agent)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown, Text]

**Output Format:** [Markdown with factual earthquake summaries, consent prompts, and cited USGS links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires per-conversation consent before transmitting a street address to the third-party lookup service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
