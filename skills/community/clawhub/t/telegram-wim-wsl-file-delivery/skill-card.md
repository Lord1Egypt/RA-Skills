## Description: <br>
Guides agents through delivering local reports and artifacts through OpenClaw chat channels from local, self-hosted, or WSL setups where host-read policy and path handling matter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pe4atnik](https://clawhub.ai/user/pe4atnik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to send generated HTML, PDF, archive, table, and text artifacts from a local filesystem into Telegram or another OpenClaw chat channel. It is most useful when absolute paths, host-read policy, MIME checks, or wrapper send failures make local file delivery unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local shell commands and file operations could affect sensitive files if run in the wrong directory. <br>
Mitigation: Review commands before execution, avoid directories containing secrets unless necessary, and prefer a sandbox or limited workspace for first use. <br>
Risk: Sending a local file to a chat channel can expose file contents outside the machine. <br>
Mitigation: Confirm the exact file path, destination channel or target, and user intent before sending, then report the resulting message id or send result. <br>
Risk: Local HTML delivery may fail or use the wrong source path when host-read policy rejects arbitrary workspace or temp locations. <br>
Mitigation: Use absolute paths, verify MIME/type, copy HTML reports to the trusted OpenClaw temp root such as /tmp/openclaw when applicable, and send that verified copy. <br>
Risk: Telegram or channel handling may compress media or reject large artifacts. <br>
Mitigation: Use --force-document for artifacts where compression is undesirable, and split or archive large files when channel limits are reached. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pe4atnik/skills/telegram-wim-wsl-file-delivery) <br>
- [Debug notes](references/debug-notes.md) <br>
- [Positioning](references/positioning.md) <br>
- [Comparison notes](references/comparison-notes.md) <br>
- [HTML report send example](examples/send-html-report.sh) <br>
- [Archive send example](examples/send-archive.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw plus local shell tools including file, cp, chmod, mkdir, node, and ls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
