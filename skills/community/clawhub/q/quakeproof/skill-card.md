## Description: <br>
Looks up recent USGS earthquake catalog data for a specific U.S. street address, including magnitude, distance from the address, felt reports, ShakeMap availability, and authoritative USGS links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oasiseng](https://clawhub.ai/user/oasiseng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Property owners, insurance adjusters, inspectors, and real-estate professionals use this skill to verify earthquake activity tied to a specific U.S. property address for claims, disaster aid, tax reassessment, or due diligence. The skill supports factual lookup and attribution, not causation, coverage, or structural-safety opinions. <br>

### Deployment Geography for Use: <br>
United States and U.S. territories <br>

## Known Risks and Mitigations: <br>
Risk: The lookup sends a specific property address and optional date to a third-party service that logs the request. <br>
Mitigation: Ask for explicit consent before each lookup, disclose the destination and logging behavior, and avoid sending an address if the user declines. <br>
Risk: Responses may include paid report or promotional links, which can affect user expectations. <br>
Mitigation: Distinguish free USGS catalog results from paid address-level reports and present commercial links plainly and sparingly. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/oasiseng/skills/quakeproof) <br>
- [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/) <br>
- [USGS ShakeMap documentation](https://ghsc.code-pages.usgs.gov/esi/shakemap/manual4_0/ug_products.html) <br>
- [USGS Did You Feel It?](https://earthquake.usgs.gov/data/dyfi/) <br>
- [Hurricane Inspections privacy policy](https://hurricaneinspections.com/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, API Calls] <br>
**Output Format:** [Markdown or plain text with structured earthquake lookup summaries, USGS attribution, and relevant links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user consent before sending a U.S. street address and optional date to the third-party lookup service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
