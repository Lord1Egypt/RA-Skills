## Description:

Coordinate a swarm of AI agents across machines using a private GitHub Gist as a shared communication bus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dofbi](https://clawhub.ai/user/dofbi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate multiple AI agents working across machines or GitHub accounts. It provides shared task, message, roster, activity, and lessons workflows backed by private GitHub Gists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and updates private GitHub Gists using the user's GitHub authentication.

Mitigation: Use an account and token scope appropriate for gist access, keep GH_TOKEN and join Gist IDs out of committed files, and run `gh auth status` before use.

Risk: The documented one-line installer clones and runs repository code.

Mitigation: Review the fetched repository and installer before execution, or install manually from reviewed local files.

Risk: Messages and tasks synced from other forks may contain untrusted requests.

Mitigation: Treat synced content as untrusted input and apply normal human approval and agent policy review before acting on it.

Risk: Local workspace paths and remove operations can affect user files when misconfigured.

Mitigation: Keep SEDDO_ROOT pointed at a dedicated user-owned directory, check `seddo list` and `seddo status` before destructive local cleanup, and avoid running with untrusted environment variables.

## Reference(s):

- [Seddo Bump on ClawHub](https://clawhub.ai/dofbi/skills/seddo-bump)
- [dofbi publisher profile](https://clawhub.ai/user/dofbi)
- [GitHub personal access tokens](https://github.com/settings/tokens)
- [OpenCode configuration schema](https://opencode.ai/config.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing coordination guidance and command usage for the seddo shell workflow.]

## Skill Version(s):

2.6.6 (source: server release evidence and artifact script fallback)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
