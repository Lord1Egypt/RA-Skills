## Description: <br>
Monitors Twitter/X feeds with AI signal detection, semantic tweet search, signal detector management, and bookmark folder organization for Purefeed accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poloniki](https://clawhub.ai/user/poloniki) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with Purefeed accounts use this skill to find relevant tweets, monitor topics through AI signal detectors, and organize curated tweet results into folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Purefeed API key that can read and modify signals, folders, and curated tweet data. <br>
Mitigation: Install only when that account access is acceptable, and revoke or rotate the API key when access is no longer needed. <br>
Risk: The skill can update account objects and delete signals, including irreversible signal deletion. <br>
Mitigation: Require the agent to show the exact target and obtain explicit user confirmation before update or delete requests. <br>
Risk: API error hints may suggest follow-up actions that do not match the user's intent. <br>
Mitigation: Treat error hints as suggestions and validate them against the user's stated goal before following them. <br>


## Reference(s): <br>
- [Purefeed ClawHub Release](https://clawhub.ai/poloniki/purefeed) <br>
- [Purefeed API](https://purefeed.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline links, curl commands, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tweet outputs should include linked screen names, linked tweet references, view counts, and engagement-oriented sorting when applicable.] <br>

## Skill Version(s): <br>
0.13.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
