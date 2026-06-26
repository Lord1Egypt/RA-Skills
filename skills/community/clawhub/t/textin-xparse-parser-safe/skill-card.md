## Description: <br>
Parse documents into clean markdown or structured JSON via the xparse-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaorui921](https://clawhub.ai/user/zhaorui921) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert local documents or document URLs into agent-friendly Markdown or structured JSON for reading, summarization, extraction, and downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document contents may be processed by xparse/TextIn services outside the local machine. <br>
Mitigation: Use the skill only when external document processing is acceptable, and avoid sending confidential documents unless that processing path has been approved. <br>
Risk: The CLI installer is vendor-hosted remote code. <br>
Mitigation: Ask for explicit user approval before installation and offer to inspect the installer script before execution. <br>
Risk: APP_ID, SECRET_CODE, and document passwords are sensitive secrets. <br>
Mitigation: Prefer `xparse-cli auth` for credential setup, avoid exposing secrets in shared logs, and request missing passwords from the user instead of guessing or bypassing protected documents. <br>


## Reference(s): <br>
- [API Reference](references/api-reference.md) <br>
- [CLI Guidance](references/cli-guidance.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [TextIn Key Setup](references/textin-key-setup.md) <br>
- [TextIn Parse API v1](https://docs.textin.com/xparse/v1/) <br>
- [TextIn Documentation](https://docs.textin.com/) <br>
- [TextIn Console](https://www.textin.com/console/dashboard/setting) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; parsed document output may be Markdown text or structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save parsed Markdown or JSON to stdout, a file, or a directory depending on xparse-cli options.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
