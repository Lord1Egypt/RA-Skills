## Description:

Upload local files to Qiniu Cloud and return a publicly accessible URL (or signed private URL).

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenggongdu](https://clawhub.ai/user/chenggongdu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to upload selected local files to Qiniu Cloud and pass the resulting public or signed URL into downstream workflows such as transcription or cloud processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user or agent may upload the wrong local file or expose sensitive content through a public URL.

Mitigation: Confirm the exact file path before execution and use private mode or signed URLs for sensitive content.

Risk: Qiniu access credentials could be exposed if placed in source control, prompts, or logs.

Mitigation: Store credentials only in environment variables or a secrets manager, and avoid echoing them in command output.

Risk: A returned URL may not be anonymously reachable if the configured Qiniu domain uses authorization or anti-leeching controls.

Mitigation: Verify the returned URL is externally accessible before passing it to downstream services, or use signed private URLs when access control is required.

## Reference(s):

- [Qiniu Cloud](https://www.qiniu.com/)
- [Qiniu environment variables](references/env-example.md)
- [ClawHub skill page](https://clawhub.ai/chenggongdu/skills/qiniu-upload)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands; the upload script emits JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the object key, URL, size, privacy mode, MIME type, and source path after upload.]

## Skill Version(s):

0.1.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
