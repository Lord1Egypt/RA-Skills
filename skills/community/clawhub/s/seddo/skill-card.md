## Description:

Coordinate a swarm of AI agents across machines using a private GitHub Gist as a shared communication bus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dofbi](https://clawhub.ai/user/dofbi)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent operators use Seddo to coordinate multiple AI agents across machines and accounts through shared Gist-backed messages, task lists, lessons, rosters, and activity logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell scripts have unsafe local path handling that can affect files outside the intended Seddo workspace.

Mitigation: Review before installing, use a dedicated Seddo workspace, and patch name validation and path containment before use in sensitive environments.

Risk: Joined Gists can expose shared task, message, or lesson content to participants and accounts that can access the Gist.

Mitigation: Only join Gists from trusted people and avoid putting secrets, credentials, regulated data, or confidential customer data in Seddo files.

Risk: Seddo requires GitHub Gist access through the GitHub CLI, which can broaden the impact of a compromised credential.

Mitigation: Use a GitHub credential limited to Gist access where possible, verify `gh auth status`, and rotate or revoke credentials after use.

Risk: Concurrent edits to the same Gist file are last-write-wins and may drop one update.

Mitigation: Run `seddo sync` before writing, avoid simultaneous edits to the same file, use `LOCK:` markers for contention, and keep usage on demand for small agent groups.

## Reference(s):

- [Seddo ClawHub listing](https://clawhub.ai/dofbi/skills/seddo)
- [README](README.md)
- [Architecture](ARCHITECTURE.md)
- [OpenCode installation guide](OPENCODE.md)
- [Gist protocol template](templates/PROTOCOL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Gist-backed markdown state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GitHub CLI commands and local Seddo configuration under a user-selected workspace.]

## Skill Version(s):

2.6.5 (source: server release metadata and scripts/seddo.sh)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
