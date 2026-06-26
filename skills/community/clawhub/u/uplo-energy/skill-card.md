## Description: <br>
AI-powered energy sector knowledge management. Search power generation records, grid management data, regulatory filings, and safety protocols with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Energy operations, compliance, engineering, environmental, and regulatory affairs teams use this skill to search organizational power generation, grid management, regulatory, safety, environmental, and asset documentation. It supports workflows such as NERC compliance evidence gathering, outage investigation, rate case research, safety review, and environmental inspection preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches, exports, and logs can expose operational energy data, including restricted CEII, grid, safety, outage, or compliance information. <br>
Mitigation: Install only for a trusted UPLO instance, use least-privilege API tokens, respect classification tiers, and avoid exposing restricted data to untrusted agents or conversations. <br>
Risk: The skill connects through an npm MCP package and a configured UPLO instance. <br>
Mitigation: Verify the npm MCP package source and the configured UPLO endpoint before deployment. <br>
Risk: Context export and compliance-session logging may create retention or audit obligations. <br>
Mitigation: Confirm organizational retention and logging rules before using export or compliance logging workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-energy) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include organization-specific search results, context exports, ownership guidance, knowledge-gap reports, outdated-document flags, and conversation logs when connected to a trusted UPLO instance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
