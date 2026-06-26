## Description: <br>
Search and analyze global news using SonarBay News Intelligence via its CLI or REST API for news search, trending entities, mention counts, and news-related data analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pavanxs](https://clawhub.ai/user/pavanxs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to search recent global news, inspect trending entities, compute mention counts over time, and compare coverage across sources through SonarBay CLI commands or REST API endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional CLI setup runs a remote installer script, and news queries sent through the CLI or REST API are visible to the SonarBay service. <br>
Mitigation: Install only when the SonarBay provider is trusted; prefer reviewing the installer script first or using the REST API directly for lower setup risk. <br>


## Reference(s): <br>
- [Sonarbay News ClawHub listing](https://clawhub.ai/pavanxs/sonarbay-news) <br>
- [SonarBay service home](https://sonarbay.com) <br>
- [SonarBay CLI installer for Mac/Linux](https://sonarbay.com/install.sh) <br>
- [SonarBay CLI installer for Windows PowerShell](https://sonarbay.com/install.ps1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, API Calls, Guidance] <br>
**Output Format:** [Markdown with CLI examples, REST API endpoints, and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [News queries may be sent to the SonarBay service; CLI and REST responses can return JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
