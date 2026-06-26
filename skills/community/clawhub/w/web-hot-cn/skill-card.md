## Description: <br>
Fetches live Chinese hot search, music chart, entertainment ranking, App Store ranking, and People's Daily newspaper data through Node.js scripts and returns unified JSON results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gfhe](https://clawhub.ai/user/gfhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer questions about current Chinese trends, rankings, entertainment data, app charts, music charts, and People's Daily newspaper pages by running the relevant crawler script and summarizing its JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts third-party public websites at use time, so results may fail, change, or be incomplete when upstream pages or network access change. <br>
Mitigation: Show users when a source fails or returns empty data, and avoid treating live scraped rankings as guaranteed complete or authoritative. <br>
Risk: Broad recommendation questions may be answered from scraped rankings rather than from a curated editorial response. <br>
Mitigation: Frame rankings as current public signals and add context or caveats before presenting them as recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gfhe/web-hot-cn) <br>
- [Script parameter reference](references/api-endpoints.md) <br>
- [Data format reference](references/data-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON from Node.js scripts, with optional Markdown summaries or rendered newspaper images in the agent response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and network access to third-party public web sources; no API key or server is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
