## Description:

Normalizes URLs, PDFs, Word, Excel, CSV, images, and text into clean JSON for reliable agent input parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etytabs](https://clawhub.ai/user/etytabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to convert web pages, documents, spreadsheets, images, and text into a deterministic JSON envelope before passing content to an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote HTTP mode may send URLs, uploaded files, and parsed outputs to api.reversal.dev.

Mitigation: Use local stdio mode for sensitive documents, and review the remote service's privacy, retention, and security practices before sending confidential data.

Risk: Production installs from floating sources can change behavior unexpectedly.

Mitigation: Pin repository commits and package versions in production or credentialed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/etytabs/skills/reversal-engine)
- [Reversal repository](https://github.com/Etytabs/REVERSAL)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Structured JSON from tool calls, plus Markdown guidance with code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports URL, PDF, Word, Excel, CSV, image, and text inputs; batch normalization supports up to 10 sources.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
