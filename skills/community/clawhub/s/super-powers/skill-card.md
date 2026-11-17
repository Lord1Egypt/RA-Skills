## Description:

Installs and runs the published `superpowers-ai` npm package so an agent can help a user log in, start or stop the SuperPowers desktop streamer, and troubleshoot common setup issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohanarun](https://clawhub.ai/user/rohanarun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install and operate the SuperPowers desktop streamer from the published npm package without source-code access. The skill also provides common install, login, streaming, and macOS permission troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs an unpinned npm package with the user's normal local permissions.

Mitigation: Use it only when the `superpowers-ai` package and publisher are trusted, prefer a least-privileged environment without sensitive environment variables, and check the resolved package version before granting permissions.

Risk: The desktop streamer may require Screen Recording or Accessibility permissions on macOS.

Mitigation: Grant permissions only after validating the package and use the documented stop or logout commands when finished.

## Reference(s):

- [Super Powers AI ClawHub page](https://clawhub.ai/rohanarun/skills/super-powers)
- [rohanarun publisher profile](https://clawhub.ai/user/rohanarun)
- [superpowers-ai npm package](https://www.npmjs.com/package/superpowers-ai)
- [Install And Run](references/install.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands for local installation, streamer start and stop, account status, logout, and troubleshooting.]

## Skill Version(s):

1.0.4 (source: release evidence, released 2026-04-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
