## Description: <br>
Xiaohongshu Radar lets an agent run Xiaohongshu keyword searches and note-detail lookups for content planning, competitive analysis, KOL screening, and trend research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[um-why](https://clawhub.ai/user/um-why) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, marketers, and content analysts use this command-line skill to collect public Xiaohongshu search results and note details for campaign research, content ideation, and structured reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, note URLs, and the GUAIKEI_API_TOKEN are sent to the GuaiKei API service. <br>
Mitigation: Use only when that data sharing is acceptable, store the token as a protected credential, and rotate it if exposure is suspected. <br>
Risk: Search and detail results are written to local log files that may contain sensitive queries or returned content. <br>
Mitigation: Protect or delete the logs directory when outputs contain sensitive research, customer, or campaign information. <br>
Risk: Some documentation claims are broader than the implemented search and detail commands, and one limitation line names Douyin instead of Xiaohongshu. <br>
Mitigation: Evaluate the skill as a Xiaohongshu keyword-search and note-detail tool, and verify claims outside those implemented commands before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/um-why/xiaohongshu-radar) <br>
- [Publisher profile](https://clawhub.ai/user/um-why) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [JSON or Markdown command-line output, with JSON log files written locally] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; search output supports json or markdown, while detail output is JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
