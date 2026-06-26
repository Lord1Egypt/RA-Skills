## Description: <br>
Semantic Shield helps agents and developers check AI skills, plugins, and MCP tools for safety by querying trust scores, risk levels, threat details, and install recommendations from a third-party advisory API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simplysemantics](https://clawhub.ai/user/simplysemantics) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, AI agent builders, and security teams use this skill to check whether a skill, plugin, or MCP tool has a vetted safety profile before installation or use. It can also submit public skill identifiers or URLs for expert review when no existing verdict is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party advisory service and API quota, so results may be unavailable or incomplete when credentials, quota, or service availability fail. <br>
Mitigation: Use a revocable Semantic Shield API key, monitor lookup and inquiry quota, and handle authentication, quota, not-found, and temporary service errors before making install decisions. <br>
Risk: Validation requests can transmit skill identifiers, provider names, and optional public URLs to the Semantic Shield service. <br>
Mitigation: Submit only public skill identifiers or public listing URLs, and do not send secrets, private repositories, internal URLs, source code, environment variables, or personal data. <br>
Risk: A third-party safety score can be useful context but should not be the only control for high-impact or sensitive tool installation. <br>
Mitigation: Combine Semantic Shield results with local review, organizational policy, and independent security checks before installing or enabling high-impact tools. <br>


## Reference(s): <br>
- [Semantic Shield product page](https://www.simplysemantics.com/semantic-shield.html) <br>
- [ClawHub listing](https://clawhub.ai/simplysemantics/semantic-shield) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown trust reports with API request guidance and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SEMANTIC_SHIELD_API_KEY and returns safety scores, risk levels, threat summaries, and recommendations based on submitted skill identifiers, providers, or public URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
