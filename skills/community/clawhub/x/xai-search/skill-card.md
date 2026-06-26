## Description: <br>
Search X/Twitter and the web in real-time using xAI's Grok API with agentic search tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aydencook03](https://clawhub.ai/user/aydencook03) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run real-time web, X/Twitter, or combined searches through xAI's Grok API and return the resulting answer with available citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to xAI/Grok and may include sensitive content if entered by the user. <br>
Mitigation: Do not submit secrets, regulated data, or confidential internal information in search queries. <br>
Risk: The helper requires an xAI API key in the execution environment. <br>
Mitigation: Provide XAI_API_KEY only in trusted environments and avoid exposing it in command history, logs, or shared configuration. <br>
Risk: The helper depends on the external xai-sdk package. <br>
Mitigation: Use an isolated Python environment and pin the xai-sdk version when deploying the skill. <br>


## Reference(s): <br>
- [xAI API documentation](https://docs.x.ai/docs/) <br>
- [ClawHub xAI Search release page](https://clawhub.ai/aydencook03/xai-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and streamed plain-text search responses with optional source URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XAI_API_KEY and sends user search queries to xAI/Grok.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
