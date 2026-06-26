## Description: <br>
Enables AI agents to use Prismer Cloud for web and document context, agent messaging, task and memory management, file sharing, and self-improving evolution workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ooxxxxoo](https://clawhub.ai/user/ooxxxxoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect AI agents to Prismer Cloud services for compressed web context, OCR-backed document parsing, inter-agent messaging, shared tasks, persistent memory, and evolution strategy learning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install and run external Prismer Cloud packages and integrations. <br>
Mitigation: Install only when Prismer Cloud and the requested packages are trusted, and review generated shell commands before execution. <br>
Risk: API keys, uploaded documents, logs, and shared files may expose sensitive data to a cloud service. <br>
Mitigation: Use dedicated or revocable API keys and avoid uploading sensitive content unless retention, access, and sharing behavior are understood. <br>
Risk: Incoming agent messages, synced skills, and shared evolution outcomes can introduce untrusted instructions or unsafe changes. <br>
Mitigation: Treat remote messages and installed skills as untrusted content, require confirmation before installing skills or changing shared learning records, and scan skill content before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ooxxxxoo/self-envolve-engine) <br>
- [Prismer Cloud Documentation](https://prismer.cloud/docs) <br>
- [Prismer Cloud](https://prismer.cloud) <br>
- [Prismer Cloud Dashboard](https://prismer.cloud/dashboard) <br>
- [Prismer Go SDK](https://github.com/Prismer-AI/Prismer/sdk/golang) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions] <br>
**Output Format:** [Markdown with bash and SDK code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI setup, API key handling, webhook and realtime delivery options, SDK snippets, and operational command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
