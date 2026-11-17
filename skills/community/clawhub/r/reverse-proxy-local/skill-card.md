## Description:

Connect OpenClaw to the internet via Tailscale Funnel for externally reachable OpenAI-compatible chat completions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsheasha](https://clawhub.ai/user/tsheasha)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to expose a local OpenClaw gateway through Tailscale Funnel, generate bearer-token credentials, check status, disconnect public access, and package connection details for trusted recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally makes a local OpenClaw API reachable through Tailscale Funnel.

Mitigation: Use it only when public reachability is intended, verify the exposed endpoint, and run the disconnect script when access is no longer needed.

Risk: The generated ecto-credentials.json file contains a reusable bearer credential that grants remote API access.

Mitigation: Share credentials only with trusted recipients, rotate the token after sharing, and keep packages or ZIP files out of chats, cloud folders, logs, and repositories.

Risk: Setup may use sudo, install Homebrew or Tailscale, change service state, and restart OpenClaw gateway processes.

Mitigation: Review the scripts before execution and run them only on a machine where those administrative changes are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tsheasha/skills/reverse-proxy-local)
- [Tailscale](https://tailscale.com)
- [Tailscale Funnel administration](https://login.tailscale.com/admin/machines)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown with inline bash commands and JSON credential examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a public API URL, bearer token location, status output, disconnect guidance, and optional packaged credentials for trusted recipients.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
