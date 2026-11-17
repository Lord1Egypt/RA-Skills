## Description:

TokenSaver is a Korean-language context database client for storing prompts and searching memory so agents can retrieve compact context instead of sending long prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorongss](https://clawhub.ai/user/dorongss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to save Korean-language context to TokenSaver and retrieve compact memory snippets by search level for prompt optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved content and search queries can be sent to a third-party remote service.

Mitigation: Avoid secrets or regulated data unless the TokenSaver service has been assessed, and invoke save or search only when remote memory update or retrieval is intended.

Risk: The security evidence flags broad activation phrases and limited privacy or installation disclosure.

Mitigation: Review before installing, prefer a pinned and verified package version, and constrain use to explicit save/search requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dorongss/skills/token-saver-kr)
- [TokenSaver website](https://tokensaver.ai)
- [TokenSaver API service](https://api.tokensaver.ai)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration]

**Output Format:** [JSON responses, CLI text, and Markdown guidance with Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TokenSaver API key and sends save/search content to the TokenSaver service.]

## Skill Version(s):

1.0.0 (source: server release metadata and openclaw.skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
