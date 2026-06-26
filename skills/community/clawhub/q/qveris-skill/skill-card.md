## Description: <br>
Search and execute dynamic tools via QVeris API for external APIs and tools such as weather, search, data retrieval, stock analysis, and market indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yifeiwang1981](https://clawhub.ai/user/yifeiwang1981) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to discover QVeris-hosted external tools by capability and execute selected tools with JSON parameters. It is useful when an agent needs dynamic access to weather, market, search, currency, geolocation, translation, or other API-backed data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a QVeris API key and can send user-provided queries and execution parameters to external QVeris-hosted tools. <br>
Mitigation: Configure the key only in trusted environments, review the selected tool and parameters before execution, and avoid sending secrets, personal data, regulated information, or private business data unless downstream handling has been verified. <br>
Risk: Server security evidence flags a broad auto-invoked gateway that can search and execute external APIs without clear per-call consent or data-flow warnings. <br>
Mitigation: Use explicit user confirmation for tool execution, inspect destinations and expected costs, and keep execution scoped to the minimum parameters needed for the task. <br>


## Reference(s): <br>
- [QVeris](https://qveris.ai) <br>
- [QVeris API endpoint](https://qveris.ai/api/v1) <br>
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) <br>
- [ClawHub skill page](https://clawhub.ai/yifeiwang1981/qveris-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QVERIS_API_KEY and can limit execution responses with a max response size option.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
