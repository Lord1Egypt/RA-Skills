## Description:

Helps agents apply a legacy, reversible workaround for web_fetch fake-IP failures on older npm-global OpenClaw installs while directing newer OpenClaw versions to the built-in openclaw.json ssrfPolicy fix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xing-xing-coder](https://clawhub.ai/user/xing-xing-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess and run a patch, status, inspect, and revert flow for older npm-global OpenClaw installs where web_fetch is blocked in fake-IP proxy environments. OpenClaw v2026.4.10 and later should use the documented configuration approach instead.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workaround modifies a global OpenClaw runtime and allows the RFC2544 fake-IP range for web_fetch on older installs.

Mitigation: Prefer openclaw.json ssrfPolicy configuration on OpenClaw v2026.4.10 or later; on older npm-global installs, run status and inspect before apply and use the documented revert command when no longer needed.

Risk: The workaround is intended only for older npm-global OpenClaw installs affected by fake-IP web_fetch blocking.

Mitigation: Do not use it for source-built OpenClaw, certificate problems, proxy rule mistakes, port mistakes, or missing proxy environment variables.

## Reference(s):

- [web_fetch Fake-IP Workaround Reference](references/README.md)
- [ClawHub Skill Page](https://clawhub.ai/xing-xing-coder/skills/web-fetch-fakeip)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash, JSON, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-facing operational guidance for a local workaround; file changes occur only if the user runs the bundled patch script.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
