## Description: <br>
Captures architecture decisions, code quality issues, build and deployment failures, dependency problems, performance regressions, tech debt, and test gaps as structured learning logs for continuous engineering improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to capture build failures, architecture findings, test gaps, dependency issues, performance regressions, and feature requests in project learning logs. Teams can promote recurring or broadly useful learnings into ADRs, coding standards, CI/CD runbooks, or workspace instruction files after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Learning logs or promoted instructions could capture secrets, sensitive operational details, or misleading guidance. <br>
Mitigation: Redact secrets and sensitive details before logging or committing .learnings files, and review diffs before adding guidance to AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, ADRs, or Copilot instructions. <br>
Risk: Optional hooks can add reminders broadly if installed with a global empty matcher. <br>
Mitigation: Keep hooks project-scoped by default, use the activator-only setup unless broader behavior is intentional, and avoid global empty matchers unless reminders are wanted on every prompt. <br>
Risk: Optional command-output checks may encounter sensitive terminal output. <br>
Mitigation: Enable PostToolUse error detection only in trusted environments and do not log or forward raw command output verbatim. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jose-compu/self-improving-engineering) <br>
- [OpenClaw integration guide](references/openclaw-integration.md) <br>
- [Hook setup guide](references/hooks-setup.md) <br>
- [Entry examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown learning entries and setup guidance with shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or append local .learnings markdown files and may provide optional hook configuration guidance.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
