## Description: <br>
Sends HTML emails through the Resend API using a configured sender plus recipient, subject, and HTML body inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chjm-ai](https://clawhub.ai/user/chjm-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send generated reports, summaries, HTML content, or lightweight notifications through a configured Resend account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email can disclose private or sensitive information if the recipient, subject, or body is wrong. <br>
Mitigation: Review recipients, subject, and body before sending, and send secrets or sensitive records only when authorized. <br>
Risk: The skill requires a Resend API key capable of sending email from the configured sender. <br>
Mitigation: Use a dedicated low-privilege Resend API key where possible, keep it in the environment or local .env file, and avoid committing credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chjm-ai/save-to-email) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance, Text] <br>
**Output Format:** [Markdown guidance with shell commands and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RESEND_API_KEY, RESEND_FROM, curl, and python3; sends HTML content through Resend.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
