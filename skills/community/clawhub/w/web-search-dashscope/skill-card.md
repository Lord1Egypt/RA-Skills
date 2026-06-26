## Description: <br>
Uses the Serper API to provide real-time internet search results based on Google Search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tom859174-sketch](https://clawhub.ai/user/tom859174-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run real-time web searches for news, weather, finance, documentation, and other current information from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an embedded Serper API key. <br>
Mitigation: Remove the embedded key, rotate the exposed credential, and require users to supply their own secret through a safer configuration mechanism such as an environment variable. <br>
Risk: Search queries are sent to Serper and Google-backed infrastructure. <br>
Mitigation: Avoid sensitive queries and disclose third-party query handling before use. <br>
Risk: The release was flagged suspicious by the authoritative security scan. <br>
Mitigation: Review and scan the skill before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tom859174-sketch/web-search-dashscope) <br>
- [Serper website](https://serper.dev/) <br>
- [Serper API key documentation](https://serper.dev/api-key) <br>
- [Serper search API endpoint](https://google.serper.dev/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API Calls] <br>
**Output Format:** [JSON-RPC response containing formatted text search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 10 search results and may include answer-box or weather information when supplied by the API.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
