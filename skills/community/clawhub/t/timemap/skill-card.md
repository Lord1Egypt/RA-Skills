## Description: <br>
Timemap helps agents search historical entertainment, nightlife, and culture venues in Tel Aviv and Haifa using public data from timemap.co.il. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexpolonsky](https://clawhub.ai/user/alexpolonsky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to explore historical venue records, answer questions about addresses or neighborhoods, and retrieve venue details, timelines, statistics, memories, or nearby results from Timemap data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python script that makes network requests to timemap.co.il and stores a temporary cache of public venue data. <br>
Mitigation: Review the script before deployment, allow outbound access only where appropriate, and clear the temporary cache if local retention is not desired. <br>
Risk: The underlying community-curated venue data may be incomplete or inaccurate. <br>
Mitigation: Treat responses as historical reference material and verify important conclusions against authoritative sources before relying on them. <br>


## Reference(s): <br>
- [ClawHub Timemap skill page](https://clawhub.ai/alexpolonsky/timemap) <br>
- [Timemap public website](https://timemap.co.il) <br>
- [Timemap public venue API](https://timemap.co.il/api/venue) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; command output may be terminal text or JSON when --json is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; queries timemap.co.il and may use a temporary local cache of public venue data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
