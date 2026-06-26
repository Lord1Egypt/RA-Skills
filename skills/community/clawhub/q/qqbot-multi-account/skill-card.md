## Description: <br>
Helps OpenClaw operators configure and troubleshoot QQBot multi-account, multi-agent routing, duplicate sessions, proactive sends, and local plugin export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Naluko](https://clawhub.ai/user/Naluko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw operators and developers use this skill to manage multiple QQBot accounts, verify account-to-agent bindings, diagnose duplicate sessions, send QQ messages or files through a selected account, and package a local QQBot plugin for handoff or backup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic output may expose QQ user IDs, appIds, service details, or secret file paths. <br>
Mitigation: Treat inspection output as private and redact these details before sharing logs or reports. <br>
Risk: File-send examples can disclose unintended local files or send content to the wrong recipient. <br>
Mitigation: Confirm each <qqfile> path and recipient before executing a send workflow. <br>
Risk: Using an unpinned QQBot plugin version can reduce reproducibility across environments. <br>
Mitigation: Pin the QQBot plugin version when reproducible behavior matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Naluko/qqbot-multi-account) <br>
- [Multi-account routing](references/multi-account-routing.md) <br>
- [Proactive send and file delivery](references/proactive-send.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local inspection or export commands; inspection output can contain private QQBot deployment details.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
