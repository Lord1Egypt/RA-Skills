## Description: <br>
Provides practical AI-assisted coding workflow guidance for project setup, PLAN/ACT separation, multi-agent collaboration, recovery, and security review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[russellfei](https://clawhub.ai/user/russellfei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to structure AI-assisted software work, including planning, implementation handoff, multi-agent coordination, troubleshooting, and review of AI-generated code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recovery and automation snippets can discard, auto-commit, or auto-push project changes. <br>
Mitigation: Require explicit approval before git reset, checkout rollback, hook creation, auto-commit timers, or git push; create a backup branch or stash first. <br>
Risk: Project handoff, log, status, and memory files can expose secrets or private user data. <br>
Mitigation: Avoid writing secrets or private user data into DESIGN, HANDOFF, LOG, status, or memory/task files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/russellfei/vibe-3k) <br>
- [Quickstart: Core Concepts and Project Setup](references/01-quickstart.md) <br>
- [Single-Agent Development](references/02-single-agent.md) <br>
- [Multi-Agent Collaboration](references/03-multi-agent.md) <br>
- [Emergency and Recovery Procedures](references/04-emergency.md) <br>
- [Security and QA](references/05-security-qa.md) <br>
- [Tool Recommendations](references/06-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code blocks and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes workflow checklists, project-rule templates, recovery procedures, and security review guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
