## Description: <br>
自动处理多平台中文编码问题的发布基础设施，集成防卡顿策略，支持Discord、GitHub等平台，遵循'防止勤务干扰'原则。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrpulorx2025-source](https://clawhub.ai/user/mrpulorx2025-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate UTF-8 text, compute byte lengths, create UTF-8 JSON payloads, and publish encoded content to Discord or GitHub workflows. It is especially aimed at Chinese-language publishing flows where terminal display encoding can be misleading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded live-looking Discord and GitHub credentials may be used if integration tests or publishing commands run as provided. <br>
Mitigation: Remove and revoke embedded credentials before installation or testing; require users to provide fresh credentials through environment variables or a secure secret manager. <br>
Risk: Publishing workflows can send file content to Discord or GitHub with limited user confirmation. <br>
Mitigation: Require explicit opt-in confirmation for each external publish target and show the destination plus content scope before sending. <br>
Risk: Publishing failure paths can persist content to local backup Markdown files. <br>
Mitigation: Make local backup creation configurable, document the storage location, and avoid writing sensitive content unless the user confirms. <br>
Risk: Credential previews and API responses may expose sensitive operational details in logs. <br>
Mitigation: Redact tokens, webhook URLs, and response bodies before logging or reporting failures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrpulorx2025-source/utf8-encoder) <br>
- [Publisher profile](https://clawhub.ai/user/mrpulorx2025-source) <br>
- [Server-resolved provenance](unavailable: No server-resolved GitHub import provenance is stored for this version.) <br>
- [Artifact package repository metadata](https://github.com/mrpulorx2025-source/utf8-encoder-skill) <br>
- [Artifact package issues metadata](https://github.com/mrpulorx2025-source/utf8-encoder-skill/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, CLI commands, and generated text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send content to Discord or GitHub and may write local backup Markdown files when publishing paths are used.] <br>

## Skill Version(s): <br>
2.0.0 (source: target metadata, evidence.release.version, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
