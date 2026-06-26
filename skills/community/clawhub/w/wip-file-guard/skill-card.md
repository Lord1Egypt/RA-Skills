## Description: <br>
Hook that blocks destructive edits to protected identity files for Claude Code CLI and OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install or configure a local guard that prevents agents from overwriting or destructively trimming protected identity, memory, and instruction files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The persistent local hook can block legitimate edits to protected identity, memory, or instruction files. <br>
Mitigation: Review protected filenames and path patterns before installation, and document how to disable or adjust the hook when legitimate maintenance is needed. <br>
Risk: Installing the wrong package or version could apply unexpected guard behavior. <br>
Mitigation: Verify the npm package name, publisher, and version before installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/parkertoddbrooks/wip-file-guard) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/parkertoddbrooks) <br>
- [npm Package](https://www.npmjs.com/package/@wipcomputer/wip-file-guard) <br>
- [GitHub Repository](https://github.com/wipcomputer/wip-file-guard) <br>
- [Manual Install and Customization Reference](REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local hook setup guidance and guard behavior descriptions; runtime guard decisions are emitted as allow or deny responses.] <br>

## Skill Version(s): <br>
1.9.72 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
