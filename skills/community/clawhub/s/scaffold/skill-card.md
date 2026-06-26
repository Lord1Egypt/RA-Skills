## Description: <br>
Your agent. Configured to you. Remembers everything. Includes setup wizard, 30-day roadmap, 25 ready-to-use prompts, and pre-built memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scaffoldworkspace](https://clawhub.ai/user/scaffoldworkspace) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenClaw users use Scaffold to bootstrap a personalized agent workspace with memory, identity, lifecycle hooks, onboarding prompts, and setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures a highly autonomous, file-backed agent workspace with broad ongoing authority over files, memory, commits, and possible external pushes. <br>
Mitigation: Install only in an isolated workspace or machine and review the permission model before use. <br>
Risk: Automatic local commits and any outbound push workflow can expose unintended file changes or repository contents. <br>
Mitigation: Revise automatic git commit behavior as needed and require explicit approval before every git push or external publication. <br>
Risk: Persistent memory files can accumulate credentials, sensitive personal data, or stale operating assumptions. <br>
Mitigation: Keep credentials and sensitive personal data out of memory files, use environment variables for secrets, and periodically audit memory content. <br>
Risk: Heartbeat or cron-style monitoring can create recurring autonomous activity before the user has configured clear boundaries. <br>
Mitigation: Disable heartbeat and cron monitoring until intentionally configured and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scaffoldworkspace/scaffold) <br>
- [Scaffold README](artifact/README.md) <br>
- [Scaffold setup wizard](artifact/setup-wizard.sh) <br>
- [Scaffold Full upgrade](https://getscaffold.gumroad.com/l/ixtnp) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files with inline shell commands and a bash setup script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates file-backed workspace guidance for agent identity, memory, lifecycle hooks, onboarding, prompts, and task tracking.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
