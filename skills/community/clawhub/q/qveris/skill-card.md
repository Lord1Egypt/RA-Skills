## Description: <br>
Search and execute dynamic tools via QVeris API. Use when needing to find and call external APIs/tools dynamically (weather, search, data retrieval, stock trading analysis, etc.). Requires QVERIS_API_KEY environment variable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hqman](https://clawhub.ai/user/hqman) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Claude Code users use this skill to discover QVeris-hosted API tools by capability and execute selected tools for weather, market data, search, currency, geolocation, translation, and similar data-retrieval tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act as a broad remote tool gateway and may auto-invoke QVeris tool discovery or execution without clear confirmation boundaries. <br>
Mitigation: Review the selected tool ID, search ID, and parameters before execution, especially for financial, account-related, or other high-impact tasks. <br>
Risk: Queries and execution parameters may be sent to QVeris or downstream tools, which can expose sensitive personal or business data. <br>
Mitigation: Use a dedicated QVeris API key and avoid sending secrets, credentials, confidential records, or sensitive personal data through tool searches or parameters. <br>


## Reference(s): <br>
- [QVeris](https://qveris.ai) <br>
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) <br>
- [Qveris on ClawHub](https://clawhub.ai/hqman/qveris) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text, JSON, Configuration] <br>
**Output Format:** [Formatted terminal text or JSON returned from QVeris tool search and execution commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QVERIS_API_KEY and uv; remote responses are capped by the script's max response size option.] <br>

## Skill Version(s): <br>
0.1.0 (source: pyproject.toml and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
