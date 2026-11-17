## Description:

This skill helps an agent call UAPI's Clipzy GET /api/raw/{id} endpoint to retrieve plaintext from a Clipzy item when the required ID and decryption key are available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when they need an agent to prepare or perform the Clipzy raw-text retrieval step through UAPI. It is focused on confirming required parameters, calling the single endpoint, and interpreting documented response codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a Clipzy decryption key to the third-party UAPI service for server-side decryption.

Mitigation: Use it only when that data flow is intended, and avoid using it for secrets unless the user accepts sending the key to uapis.cn.

Risk: Broad automatic triggers such as raw can cause the skill to be selected ambiguously.

Mitigation: Invoke it explicitly with the UAPI Clipzy raw-text endpoint or full Clipzy context before providing retrieval credentials.

Risk: Successful calls may return plaintext clipboard contents.

Mitigation: Treat returned plaintext as sensitive user data and avoid exposing it beyond the active task.

## Reference(s):

- [Server-resolved ClawHub skill page](https://clawhub.ai/shuakami/skills/uapi-get-clipzy-raw)
- [Clipzy raw-text operation reference](references/operations/get-clipzy-raw.md)
- [Quick start](references/quick-start.md)
- [Clipzy online clipboard resource reference](references/resources/Clipzy-在线剪贴板.md)
- [UAPI service](https://uapis.cn)

## Skill Output:

**Output Type(s):** [guidance, API calls, shell commands, configuration]

**Output Format:** [Markdown with endpoint details and optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include plaintext returned by the third-party Clipzy raw-text endpoint when the user provides valid retrieval credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
