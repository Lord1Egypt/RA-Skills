## Description: <br>
Xby Smart Search helps developers route technical search requests across web, GitHub, StackOverflow, NPM, documentation, API reference, and Chinese developer platforms, returning search URLs and API-backed results for the agent to present. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to find technical documentation, API references, packages, code examples, and community answers across multiple search providers from one agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to the XBY MCP service and may also be sent to destination search sites. <br>
Mitigation: Avoid searching for secrets, credentials, private repository names, customer data, or sensitive incident details. <br>
Risk: The skill stores the XBY API key in a local .env file when configured through the provided helper. <br>
Mitigation: Use a scoped API key where possible and remove XBY_APIKEY from the local .env file when the skill no longer needs access. <br>


## Reference(s): <br>
- [XiaoBenYang API key portal](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown summaries with search URLs and JSON-derived results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY API key; returned search URLs may require follow-up web fetching.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
