## Description:

x-mirror helps agents configure, switch, inspect, and restore package-manager download mirrors across tools such as pip, npm, brew, apt, Go, Cargo, RubyGems, and Docker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunrenyi](https://clawhub.ai/user/lunrenyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage package-manager mirrors, including listing available mirrors, changing registries, checking current settings, restoring official defaults, and improving download speed in China-region or slow-network environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install guide includes a high-impact remote installer path that can execute mutable code directly in the user's shell.

Mitigation: Prefer Homebrew or manual download-and-review installation, avoid direct curl-to-shell on machines with credentials or production access, and install only after explicit user consent.

Risk: Mirror-changing commands can alter package-manager source configuration and affect where future dependencies are downloaded from.

Mitigation: Confirm the intended package manager and mirror before execution, and use the documented unset command to restore official sources when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lunrenyi/skills/x-mirror)
- [x-mirror repository](https://github.com/x-cmd/x-mirror)
- [x-cmd installation guide](data/install.md)
- [x-cmd release artifacts](https://github.com/x-cmd/release)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose mirror-management commands that change package-manager source configuration.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
