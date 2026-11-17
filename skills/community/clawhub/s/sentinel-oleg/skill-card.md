## Description:

Runtime security layer for OpenClaw agents that scans external input and agent output for prompt injection, data exfiltration, credential leaks, social engineering, secret leakage, and suspicious command requests before content is processed or sent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oleglegegg](https://clawhub.ai/user/oleglegegg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add shell-based checks around untrusted external content and outgoing agent responses. It is intended for prompt-injection screening, secret-leak detection, canary-token checks, and audit-log review in OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detected sensitive content may be stored in plaintext logs.

Mitigation: Disable raw snippet logging, redirect logs to a protected location, or redact snippets before scanning secrets.

Risk: Sanitized output may be treated as fully trusted even though coverage is incomplete.

Mitigation: Use the clean output only as a helper signal and keep downstream review, allowlists, and least-privilege controls in place.

Risk: The advertised runtime interception and sanitization coverage is stronger than the artifact behavior supports.

Mitigation: Review and test the scripts in the target workflow before relying on them as a runtime security boundary.

Risk: A different pattern file than expected could be loaded.

Mitigation: Verify the configured pattern path and test representative malicious and benign inputs after installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oleglegegg/skills/sentinel-oleg)
- [Publisher profile](https://clawhub.ai/user/oleglegegg)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON scan results, with shell command examples and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write plaintext threat logs under the configured Sentinel log path.]

## Skill Version(s):

1.0.5 (source: server release evidence; artifact frontmatter reports 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
