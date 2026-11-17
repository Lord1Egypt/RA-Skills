## Description:

Guides AI-assisted software development with project kickoff practices, PLAN/ACT separation, multi-agent collaboration, recovery procedures, and security review checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[russellfei](https://clawhub.ai/user/russellfei)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to structure AI-assisted coding work, including planning, execution handoff, multi-agent coordination, failure recovery, and acceptance review. It is most useful when starting a new project, setting up agent rules, debugging with agents, or reviewing AI-generated code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Emergency procedures include destructive rollback commands that can discard local work.

Mitigation: Check git status first, create a backup branch or stash, and confirm exactly what will be lost before using git reset --hard or git checkout .

Risk: The artifact suggests a post-commit hook that can persistently auto-push future commits.

Mitigation: Install that hook only when automatic pushes are intentional, the remote is verified, and the operator knows how to remove the hook.

Risk: Verification examples use npx commands that may resolve moving tool versions.

Mitigation: Prefer pinned local project tools or locked package versions when running automated checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/russellfei/skills/vibe-3k)
- [Quickstart and Project Setup](references/01-quickstart.md)
- [Single-Agent Workflow](references/02-single-agent.md)
- [Multi-Agent Collaboration](references/03-multi-agent.md)
- [Emergency Recovery](references/04-emergency.md)
- [Security and QA](references/05-security-qa.md)
- [Tool Selection](references/06-tools.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with prompt templates, checklists, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Chinese-language guidance and time-sensitive tool notes current to 2026-02.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
