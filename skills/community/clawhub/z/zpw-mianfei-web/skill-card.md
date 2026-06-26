## Description: <br>
Uses a local free search engine to search the web with specified keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blue-sky-8](https://clawhub.ai/user/blue-sky-8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks to search the web, including requests using terms such as "search", "查一下", or "找找". The skill extracts search keywords and fetches JSON results from a local search service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to a fixed private-network HTTP address. <br>
Mitigation: Install only when the operator controls or fully trusts the service at 192.168.199.100:8080, and avoid sensitive queries. <br>
Risk: The skill places user-provided query text into a shell command. <br>
Mitigation: Review generated commands before execution and prefer a version that safely URL-encodes the query. <br>
Risk: The local search endpoint uses HTTP rather than a protected channel. <br>
Mitigation: Prefer HTTPS or another trusted local channel before using the skill in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blue-sky-8/zpw-mianfei-web) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with a curl command and JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search terms are sent to a fixed private-network HTTP endpoint.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
