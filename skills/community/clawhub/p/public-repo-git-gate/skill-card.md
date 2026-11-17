## Description:

Runs public-repository gates for Git commits, pushes, and pull requests by checking staged and untracked scope, secrets and personal data, internal material, branch and remote state, PR base/head, CI, and merge prerequisites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wardlu](https://clawhub.ai/user/wardlu)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill before public commits, pushes, pull requests, and repository-content reviews to apply a read-only Git safety checklist and run the bundled public repository check script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can miss committed sensitive content.

Mitigation: Treat the skill as an advisory checklist and require final PR or release checks that scan committed `HEAD` content directly.

Risk: `--check-remote` can print credential-bearing Git remote URLs into logs.

Mitigation: Avoid `--check-remote` on repositories with credential-bearing remotes until remote URL output is redacted.

Risk: `--changed-since` does not prove committed branch contents are safe.

Mitigation: Do not rely on `--changed-since` as the sole safety gate; pair it with checks that inspect the final committed branch state.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wardlu/skills/public-repo-git-gate)
- [Publisher Profile](https://clawhub.ai/user/wardlu)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with shell commands and plain-text script results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; the user must explicitly authorize commits, pushes, PR creation, or remote branch updates.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
