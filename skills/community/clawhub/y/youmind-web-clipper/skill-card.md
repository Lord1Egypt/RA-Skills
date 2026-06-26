## Description: <br>
Save URLs to a YouMind board from an agent, terminal, or CI/CD workflow using the YouMind CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DophinL](https://clawhub.ai/user/DophinL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to save webpages, articles, videos, and documents into a YouMind board from chat, terminal, or automation workflows after configuring the YouMind CLI and YOUMIND_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad command permissions and may install and run the YouMind CLI. <br>
Mitigation: Review the allowed commands before installation, approve any global npm install yourself, and restrict command permissions where your agent platform supports it. <br>
Risk: The skill uses YOUMIND_API_KEY for authentication. <br>
Mitigation: Store the API key in configuration or environment variables, keep it out of chat, and rotate it if exposure is suspected. <br>
Risk: Submitted URLs are saved to YouMind and may contain confidential or tokenized information. <br>
Mitigation: Only submit links you are comfortable storing in YouMind, and avoid confidential or credential-bearing URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DophinL/youmind-web-clipper) <br>
- [YouMind CLI package](https://www.npmjs.com/package/@youmind-ai/cli) <br>
- [Setup guide](references/setup.md) <br>
- [Error handling guide](references/error-handling.md) <br>
- [YouMind skills gallery](https://youmind.com/skills?utm_source=youmind-web-clipper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and CLI call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the youmind CLI, npm for installation, and YOUMIND_API_KEY for authenticated saves.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
