## Description:

在用户需要使用腾讯云官网公共能力时，该技能 helps an agent search Tencent Cloud documentation through TCCLI portal SearchDocuments and present only returned results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support engineers, and external users use this skill to search Tencent Cloud product documentation, operation guides, API documentation, best practices, and troubleshooting material from an agent workflow. It is for portal information retrieval only and does not manage Tencent Cloud resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading TCCLI and the Tencent Cloud SDK can change the local Python environment.

Mitigation: Use a virtual environment and pinned package versions when possible, and verify the portal module before running searches.

Risk: Cloud credentials may be exposed if an agent requests, prints, or stores SecretId/SecretKey carelessly.

Mitigation: Prefer OAuth login, never ask users to reveal secrets, avoid commands that print credentials, and log out or remove local TCCLI credentials when finished.

Risk: The headless login FIFO workflow can leave temporary files or logs on shared machines.

Mitigation: Avoid the headless FIFO example on shared hosts; if used, keep the process local, restrict access to temporary files, and clean the FIFO and logs immediately after authentication.

Risk: Search results or parameter assumptions can be stale or incomplete.

Mitigation: Check `tccli portal SearchDocuments help` when parameters are uncertain and present only data returned by the portal API.

## Reference(s):

- [配置 TCCLI（凭证）](references/auth.md)
- [安装 TCCLI](references/install.md)
- [portal SearchDocuments 接口参考](references/search-documents.md)
- [Tencent Cloud TCCLI installation documentation](https://cloud.tencent.com/document/product/440/34011)
- [Tencent Cloud API key console](https://console.cloud.tencent.com/cam/capi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output should include returned totals, titles, product names, snippets, URLs, and RequestId on failure; pagination should ask before continuing.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
