## Description: <br>
Generate an overall team summary covering the last 24 hours across all SageOx-enabled teams. Reads distilled daily entries via `ox distill history` and produces a structured, Slack-ready overview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galexy](https://clawhub.ai/user/galexy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product managers, and team leads use this skill to convert new SageOx distilled daily entries across configured teams into a Slack-ready 24-hour activity summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected SageOx distilled team entries are sent through the Claude CLI using the user's existing Claude credentials. <br>
Mitigation: Use the skill only in environments where sending the selected team summaries through the configured Claude CLI account is approved. <br>
Risk: The skill installs and checks a pinned ox binary under the user's home directory. <br>
Mitigation: Keep the checksum-verified pinned install flow, review the pinned ox version during upgrades, and avoid substituting package-manager installs for this skill. <br>
Risk: The skill depends on local OpenClaw memory files for install and summary state. <br>
Mitigation: Treat local state as user-writable, keep the artifact's validation checks for paths and entry ids, and review local state paths in stricter environments. <br>


## Reference(s): <br>
- [SageOx](https://sageox.ai) <br>
- [sageox-distill skill](https://clawhub.ai/skills/sageox-distill) <br>
- [ox distill history PR](https://github.com/sageox/ox/pull/507) <br>
- [Installing ox](references/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Slack mrkdwn summary, with concise shell-command or configuration guidance when prerequisites fail.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes new SageOx distilled daily entries from the last 24-hour window and uses local state to avoid repeat summaries.] <br>

## Skill Version(s): <br>
0.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
