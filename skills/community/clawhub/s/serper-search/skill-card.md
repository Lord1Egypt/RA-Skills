## Description: <br>
Fetches real Google Search or News results with links, snippets, knowledge graph data, and related questions via the Serper.dev API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Samoppakiks](https://clawhub.ai/user/Samoppakiks) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve current Google web or news search results through Serper.dev when they need source links, snippets, knowledge graph facts, or related questions rather than generated answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Serper.dev, so sensitive prompts, secrets, credentials, private customer data, or sensitive investigations may be disclosed to an external service. <br>
Mitigation: Use only queries that are acceptable to share with Serper.dev under the user's policy, and avoid sending secrets, credentials, private customer data, or sensitive investigations. <br>
Risk: The skill requires a Serper.dev API key and will not register its search tool when no key is configured. <br>
Mitigation: Provide the API key through the documented environment variable or plugin configuration, and manage the key according to local credential handling and rotation practices. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Samoppakiks/serper-search) <br>
- [Serper.dev](https://serper.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON string returned as text content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Serper.dev API key; supports web or news search and a configurable result count from 1 to 100.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
