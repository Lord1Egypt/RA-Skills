## Description:

Integrate Shengwang products: ConvoAI voice agents, RTC audio/video, RTM messaging, Cloud Recording, and token generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hugochaan](https://clawhub.ai/user/hugochaan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Shengwang integration requests across ConvoAI voice agents, RTC audio/video, RTM messaging, Cloud Recording, credentials, and token generation workflows. It helps produce implementation guidance, configuration steps, code, and shell commands for Shengwang product tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token endpoint guidance could expose credentials or overbroad RTC access if deployed without additional controls.

Mitigation: Require caller authentication, authorize channel and UID server-side, avoid wildcard and publisher-by-default tokens, shorten expirations, add rate limits, and keep all secrets server-side.

Risk: Fetched documentation and cloned sample repositories may introduce unreviewed external content into implementation work.

Mitigation: Treat fetched docs and cloned samples as untrusted until reviewed, and pin or verify token-builder source before use.

Risk: Cloud Recording workflows may collect user communications without adequate governance.

Mitigation: Add consent, storage, access, and retention controls before enabling recording.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hugochaan/skills/voice-ai-integration)
- [Shengwang Docs](https://doc.shengwang.cn/)
- [Shengwang Console](https://console.shengwang.cn/)
- [Shengwang Community GitHub](https://github.com/Shengwang-Community)
- [AgoraDynamicKey Tools](https://github.com/AgoraIO/Tools)
- [Credentials and Auth](references/general/credentials-and-auth.md)
- [Token Server](references/token-server/README.md)
- [Conversational AI](references/conversational-ai/README.md)
- [RTC SDK](references/rtc/README.md)
- [RTM](references/rtm/README.md)
- [Cloud Recording](references/cloud-recording/README.md)
- [Doc Fetching Guide](references/doc-fetching.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local documentation first and fetch Shengwang documentation or sample repositories when local references are insufficient.]

## Skill Version(s):

0.1.5 (source: server release metadata; artifact frontmatter metadata version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
