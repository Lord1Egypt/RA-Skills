## Description: <br>
Shuttle AI Chatbot queries a configured local AI `/chat_direct` service for single or batch product questions and returns the service response as JSON or text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sean810720](https://clawhub.ai/user/sean810720) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send product-specification or comparison prompts to a configured Shuttle AI service, either one query at a time or from a batch file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and batch-file contents may be sent to a configurable network endpoint, including the default HTTP service URL. <br>
Mitigation: Verify the endpoint operator and transport security before use, prefer localhost or HTTPS endpoints, and avoid sending secrets, credentials, private documents, or sensitive batch files. <br>
Risk: The configured AI service controls the response content and may return incorrect or unexpected product guidance. <br>
Mitigation: Review responses before using them for customer-facing, procurement, or operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sean810720/shuttle-ai-chatbot) <br>
- [Publisher profile](https://clawhub.ai/user/sean810720) <br>
- [README](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON or plain text emitted by a CLI command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses include the original query, service response, elapsed time, timestamp, service URL, and generated session ID when JSON output is selected.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence and package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
