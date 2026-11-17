## Description:

Comprehensive guide for writing shell scripts with Google zx, including JavaScript and TypeScript zx scripts, shell command execution, ProcessPromise and ProcessOutput APIs, stream piping, configuration, and CLI usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write, debug, review, and refactor zx-based shell scripts in JavaScript or TypeScript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated zx examples may execute shell commands or scripts with local file, network, or environment access.

Mitigation: Review generated commands as real shell code before running them.

Risk: Remote or Markdown-based zx scripts can execute code from content the user may not control.

Mitigation: Avoid running remote or Markdown scripts from untrusted sources.

Risk: Environment files and inherited process environments can expose secrets to commands or external services.

Mitigation: Keep secrets out of environment files passed to zx commands and limit command environments to needed variables.

Risk: Unpinned zx or npm dependencies can change behavior across installs.

Mitigation: Pin package versions when possible.

## Reference(s):

- [Zx API Reference](references/api.md)
- [Zx CLI Reference](references/cli.md)
- [Zx Configuration Reference](references/configuration.md)
- [ProcessPromise and ProcessOutput Reference](references/process.md)
- [ClawHub skill page](https://clawhub.ai/openlark/skills/zx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with JavaScript, TypeScript, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory content only; generated commands and scripts should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
