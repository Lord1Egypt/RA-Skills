## Description:

Code Sandbox executes Node.js, Python, Go, and Rust code snippets with configurable timeouts, temporary working directories, execution history, and cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to run small code snippets or demos across supported runtimes and inspect execution results, errors, timing, and recent execution history. It should only be used with trusted code or inside a separate disposable container or VM with restricted secrets, filesystem, and network access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes submitted code directly on the host with insufficient containment.

Mitigation: Use only code you already trust or run the skill inside a separate disposable container or VM with no secrets and restricted filesystem and network access.

Risk: The release should not be exposed to strangers or agent-generated code before stronger containment and resource controls are implemented.

Mitigation: Add real containment, resource limits, and cleanup controls before broader or untrusted-code use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-code-sandbox)
- [Publisher profile](https://clawhub.ai/user/yuyonghao-123)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact testing report](artifact/TESTING.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JavaScript API results and Markdown usage guidance with inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Execution results include success status, stdout, error text, exit code, execution time, and memory usage fields.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
