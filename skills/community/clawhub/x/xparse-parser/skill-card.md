## Description: <br>
Parse documents into clean markdown or structured JSON via the xparse-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[intsig-textin](https://clawhub.ai/user/intsig-textin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert local documents or document URLs into agent-readable Markdown or structured JSON before summarization, extraction, or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local documents and document passwords may be sent to the TextIn/xParse service during parsing. <br>
Mitigation: Use the skill only for documents you are allowed to process with that external provider, and avoid confidential or regulated files unless the provider relationship is approved. <br>
Risk: Installer commands fetch and execute remote scripts. <br>
Mitigation: Review and verify the installer source before running it. <br>
Risk: API credentials, document passwords, and parsed output files may contain sensitive information. <br>
Mitigation: Protect XPARSE_APP_ID, XPARSE_SECRET_CODE, document passwords, and generated output files. <br>


## Reference(s): <br>
- [API Reference](references/api-reference.md) <br>
- [CLI Guidance](references/cli-guidance.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [TextIn Key Setup](references/textin-key-setup.md) <br>
- [TextIn Parse API v1](https://docs.textin.com/xparse/v1/) <br>
- [TextIn Documentation](https://docs.textin.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/intsig-textin/xparse-parser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from xparse-cli] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write parsed Markdown or JSON files when the agent uses xparse-cli with an output path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
