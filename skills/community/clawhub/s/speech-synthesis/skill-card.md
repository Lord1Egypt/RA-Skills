## Description:

一个集成了Microsoft Edge高质量语音合成能力的MCP服务器，支持多语言语音生成、音频合并和云端存储。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to route text-to-speech requests through XiaoBenYang's remote speech synthesis service. It supports multi-segment speech generation and optional MP3 merging for multilingual audio workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a local .env file.

Mitigation: Avoid committing .env, restrict local file access, and rotate the key if exposure is suspected.

Risk: The security review notes mismatched service identity and an overridable authenticated endpoint.

Mitigation: Install only when the XiaoBenYang service is trusted, and review or constrain the endpoint before use.

## Reference(s):

- [XiaoBenYang](https://xiaobenyang.com)
- [ClawHub Skill Page](https://clawhub.ai/alinklab/skills/speech-synthesis)

## Skill Output:

**Output Type(s):** [Text, API Calls, Files]

**Output Format:** [JSON-backed results summarized as text, with generated audio file details when returned by the service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY API key and sends requests to a remote speech-generation API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
