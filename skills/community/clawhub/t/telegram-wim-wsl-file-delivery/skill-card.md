## Description: <br>
Deliver local reports and artifacts through OpenClaw chat channels when generated HTML, PDF, archives, tables, or other local files must be sent from local, self-hosted, or WSL OpenClaw setups where path handling and host-read policy matter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pe4atnik](https://clawhub.ai/user/pe4atnik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and engineers use this skill to deliver generated local reports and artifacts from local, self-hosted, or WSL OpenClaw environments into Telegram or another OpenClaw channel while handling path validation, host-read policy, and CLI fallbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected files leave the local machine when sent to Telegram or another OpenClaw channel. <br>
Mitigation: Confirm the exact file path, destination target, and file contents before each send. <br>
Risk: Temporary HTML copies under /tmp/openclaw can leave sensitive report content on disk after delivery. <br>
Mitigation: Remove temporary copies after delivery when they are no longer needed. <br>
Risk: Incorrect, relative, or guessed paths can fail host-read checks or point to the wrong file. <br>
Mitigation: Use absolute paths and verify file existence, size, and type before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pe4atnik/skills/telegram-wim-wsl-file-delivery) <br>
- [Debug notes](references/debug-notes.md) <br>
- [Positioning](references/positioning.md) <br>
- [Comparison notes](references/comparison-notes.md) <br>
- [Skill audit - 2026-06-23](references/skill-audit-2026-06-23.md) <br>
- [HTML report send example](examples/send-html-report.sh) <br>
- [Archive send example](examples/send-archive.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes confirmation guidance, absolute-path validation, trusted temporary HTML copy flow, OpenClaw CLI fallback, and delivery verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
