## Description: <br>
Real-time X/Twitter search powered by Grok-4. Find tweets, trends, and discussions with citations. Grok-4.20 also returns image results alongside tweet citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvanhorn](https://clawhub.ai/user/mvanhorn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to search X/Twitter in real time for tweets, trends, account-specific posts, and cited discussions through xAI's Grok search capability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tweet-search prompts are sent to xAI using the configured XAI_API_KEY. <br>
Mitigation: Use the skill only for explicit X/Twitter search requests and avoid submitting sensitive or confidential prompts. <br>
Risk: The API key may be available through the environment or local skill configuration. <br>
Mitigation: Keep XAI_API_KEY in scoped local configuration or environment variables and rotate it if exposure is suspected. <br>
Risk: Returned tweets, citations, and trends may be incomplete or misleading for decision-making. <br>
Mitigation: Review cited X/Twitter links and corroborate important claims before acting on the results. <br>


## Reference(s): <br>
- [Search X on ClawHub](https://clawhub.ai/mvanhorn/search-x) <br>
- [xAI Documentation](https://docs.x.ai) <br>
- [xAI Console](https://console.x.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text search results with tweet citations; optional full JSON or links-only output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XAI_API_KEY. Supports day-range filters, included or excluded handles, compact output, links-only output, JSON output, and model override.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
