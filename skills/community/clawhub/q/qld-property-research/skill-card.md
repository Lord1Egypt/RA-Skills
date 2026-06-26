## Description: <br>
Detailed Queensland property due-diligence for a single street address using official sources, covering flood-map checks, nearest train-station access, main-road proximity, NBN infrastructure, cited findings, and a composite suitability score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mhear22](https://clawhub.ai/user/mhear22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to research a single Queensland property address with official-source evidence for NBN technology, flood exposure, main-road proximity, train access, and a caveated suitability score. <br>

### Deployment Geography for Use: <br>
Queensland, Australia <br>

## Known Risks and Mitigations: <br>
Risk: Property addresses, parcel details, and route coordinates may be sent to public government, NBN, and openrouteservice endpoints during advertised checks. <br>
Mitigation: Use the skill only when those external lookups are acceptable for the address being researched, and avoid sensitive addresses unless sharing them with those services is permitted. <br>
Risk: The optional walking-route check depends on an openrouteservice API key and third-party OSM-based routing rather than official government walking-route data. <br>
Mitigation: Use a dedicated ORS_API_KEY, keep it in the runtime environment, and present openrouteservice route results as third-party walking analysis only. <br>
Risk: Some Queensland councils or data sources may not provide current property-specific evidence for every scored section. <br>
Mitigation: Emit a partial report, mark unsupported sections as unsupported with current official data, and omit the composite score when required evidence is unavailable. <br>


## Reference(s): <br>
- [QLD Property Research methodology](references/methodology.md) <br>
- [QLD Property Research official sources](references/official-sources.md) <br>
- [openrouteservice routing](references/openrouteservice.md) <br>
- [ClawHub release page](https://clawhub.ai/mhear22/qld-property-research) <br>
- [Find addresses | Queensland Government](https://www.qld.gov.au/environment/land/title/addressing/finding) <br>
- [Using the Queensland Globe | Business Queensland](https://www.business.qld.gov.au/running-business/support-services/mapping-data-imagery/queensland-globe/using) <br>
- [Plan your journey | Translink](https://translink.com.au/plan-your-journey) <br>
- [Check address | nbn](https://www.nbnco.com.au/check-address) <br>
- [FloodWise Property Report | Brisbane City Council](https://www.brisbane.qld.gov.au/building-and-planning/supporting-documents-and-online-tools/floodwise-property-report) <br>
- [openrouteservice API](https://api.openrouteservice.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown report with cited findings, section scores, and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include partial-report markers when official data or openrouteservice configuration is unavailable.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
