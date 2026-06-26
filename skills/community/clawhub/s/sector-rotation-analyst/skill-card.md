## Description: <br>
Identify sector rotation opportunities across all 11 GICS sectors using relative strength, momentum, and macro regime context from the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch Finskills sector and market data, compare sector relative strength, map likely economic-cycle phase, and produce overweight, neutral, and underweight sector research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Finskills API key and sends market-data queries to the Finskills API. <br>
Mitigation: Install only if you trust Finskills for the intended market-data use case, and protect FINSKILLS_API_KEY as a sensitive credential. <br>
Risk: Sector recommendations may be mistaken for financial advice or may not fit the user's portfolio, time horizon, or risk constraints. <br>
Mitigation: Treat outputs as investment research assistance, verify recommendations independently, and avoid sending proprietary or sensitive investment context unless acceptable for the use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/finskills/sector-rotation-analyst) <br>
- [Skill homepage](https://github.com/finskills/sector-rotation-analyst) <br>
- [Finskills API](https://finskills.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown sector rotation report with tables, rankings, rationale, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY; Pro plan data may be needed for sector and market summary endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
