## Description: <br>
Guide an existing OpenClaw operator through the SprintX handoff proof packet with the minimum safe steps: verify prerequisites, connect with sx auth, select the project, send the first event and artifact, then confirm read-back with sx status and sx brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terry3838](https://clawhub.ai/user/terry3838) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw operators use this skill to connect an existing SprintX account and project, send the first verifiable event and artifact, and confirm read-back with the SprintX CLI. It is for narrow handoff setup, not project creation, task management, or review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires the SprintX CLI and a browser-approved SprintX authentication flow, so users could install or authenticate the wrong CLI package if they do not verify the package source. <br>
Mitigation: Before installing, confirm that @sprint-x/cli is the intended SprintX CLI package and prefer the default browser-approved sx auth path. <br>
Risk: Access tokens or sensitive local data could be exposed if users paste credentials into chat or attach the wrong file or URI as an artifact. <br>
Mitigation: Do not paste tokens into chat, keep token override behavior advanced-only, and review the file or URI passed to sx artifact add before submission. <br>


## Reference(s): <br>
- [Source Of Truth](references/source-of-truth.md) <br>
- [SprintX OpenClaw Handoff Quickstart](https://www.sprintx.co.kr/docs/getting-started/openclaw-handoff-quickstart) <br>
- [SprintX CLI Quickstart](https://www.sprintx.co.kr/docs/getting-started/cli-quickstart) <br>
- [SprintX CLI Quickstart (Korean)](https://www.sprintx.co.kr/docs/getting-started/cli-quickstart.ko) <br>
- [ClawHub Skill Page](https://clawhub.ai/terry3838/sprintx-openclaw-handoff) <br>
- [ClawHub Skill Format](https://raw.githubusercontent.com/openclaw/clawhub/main/docs/skill-format.md) <br>
- [ClawHub CLI Docs](https://raw.githubusercontent.com/openclaw/clawhub/main/docs/cli.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and checklist-style pass/fail guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of the sx CLI; does not execute SprintX tasks itself.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter, package.json, CHANGELOG, released 2026-04-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
