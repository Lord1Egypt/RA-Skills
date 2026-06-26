## Description: <br>
Detects sensitive information in text or fetched webpage content by sending the content to the UCAP sensitive-information checking service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1227323804](https://clawhub.ai/user/1227323804) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content reviewers, and compliance teams use this skill to check text or webpage content for sensitive information before publishing, sharing, or processing it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text or webpage content submitted for checking is sent to UCAP. <br>
Mitigation: Use the skill only for content approved for UCAP processing, and avoid secrets, private documents, source code, or regulated data unless UCAP is approved for that data. <br>
Risk: Fetching arbitrary webpages can expose URL-fetching and SSRF-style risk. <br>
Mitigation: Keep the default static HTTPS fetching mode, rely on the built-in URL safety checks, and avoid broad domain allowlists. <br>
Risk: Dynamic browser mode can execute page JavaScript and add browser-rendering risk. <br>
Mitigation: Leave dynamic mode disabled unless it is intentionally required, and enable it only with a tight ALLOWED_DOMAINS allowlist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1227323804/ucap-sensitive-check) <br>
- [Skill documentation](artifact/skill.md) <br>
- [UCAP safeguard service](https://safeguard.ucap.com.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, guidance] <br>
**Output Format:** [JSON result object with status code, message, UCAP detection data, and source metadata when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source_url and source_type for webpage inputs; errors are returned as structured codes and messages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
