## Description: <br>
Provides Qunar travel information queries for flights, hotels, attraction tickets, and train tickets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellllll0world](https://clawhub.ai/user/hellllll0world) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and travel-support agents use this skill to collect travel query parameters, call Qunar travel APIs, and summarize results for flights, hotels, attractions, and train tickets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured Qunar API key can be sent to a runtime-supplied URL. <br>
Mitigation: Use only verified official Qunar HTTPS endpoints, prefer a version with a Qunar-domain allowlist, and attach the API key only to approved Qunar hosts. <br>
Risk: The release has a suspicious security verdict. <br>
Mitigation: Review the skill before installation and deploy it only in environments where the operator and API endpoint choices are trusted. <br>


## Reference(s): <br>
- [Qunar API Reference](references/api_reference.md) <br>
- [Qunar Open Platform Documentation](http://open.qunar.com/developer/doc) <br>
- [ClawHub Skill Page](https://clawhub.ai/hellllll0world/qunar-travel-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports list, detail, and conversational result summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
