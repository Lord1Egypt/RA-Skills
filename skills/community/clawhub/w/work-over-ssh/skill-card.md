## Description:

Use when editing a remote Git project over SSH.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhhfcgjk](https://clawhub.ai/user/abhhfcgjk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect, edit, test, and diagnose a remote Git repository over SSH while the agent remains local. It is intended for workflows where the user supplies a concrete SSH target, an absolute project path, and an explicit Python environment selector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the user's existing SSH access to operate on a remote project.

Mitigation: Provide only non-secret connection details and use pre-configured key-based or other non-interactive authentication; do not share passwords, private keys, tokens, or .env contents.

Risk: Remote commands or patches could change project files or affect existing work.

Mitigation: Confirm the SSH target, project root, environment selector, and Git status before mutation; apply edits through reviewed patches and require explicit approval for package installs, deployments, service restarts, database changes, or destructive Git/filesystem actions.

Risk: An incorrect Python environment could produce misleading test or diagnostic results.

Mitigation: Require an explicit virtualenv, Conda name, Conda prefix, or none value and pass that selector on each environment-dependent command.

## Reference(s):

- [Using Work Over SSH](references/usage.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell commands and patch workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local ssh and python3 binaries plus pre-configured non-interactive SSH authentication.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
