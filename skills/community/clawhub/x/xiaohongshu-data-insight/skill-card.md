## Description: <br>
小红书数据洞察大师 supports keyword search and note detail lookup for Xiaohongshu public-content analysis, helping agents find popular posts, compare competitors, and monitor content trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[um-why](https://clawhub.ai/user/um-why) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brand marketers, market analysts, MCN teams, and agent operators use this skill to retrieve Xiaohongshu keyword results and note details for topic discovery, competitor analysis, trend monitoring, and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, note URLs, and returned public-content data are sent to a third-party Guaikei API service. <br>
Mitigation: Use a dedicated revocable API token and avoid queries that should not leave the local environment. <br>
Risk: Task results are saved to local log files after execution. <br>
Mitigation: Periodically delete generated logs when local retention is not desired. <br>
Risk: The third-party API may be rate-limited, unavailable, or changed outside the skill owner's control. <br>
Mitigation: Keep request volume within documented limits and treat failed or empty results as operational signals rather than complete market evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/um-why/xiaohongshu-data-insight) <br>
- [Publisher profile](https://clawhub.ai/user/um-why) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Analysis] <br>
**Output Format:** [JSON or Markdown emitted by Node.js command-line tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output includes Xiaohongshu note metadata and interaction counts; detail output includes note information, interaction data, and comment analysis when returned by the API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, OpenClaw metadata, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
