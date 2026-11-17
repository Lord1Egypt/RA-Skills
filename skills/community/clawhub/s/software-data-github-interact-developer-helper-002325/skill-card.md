## Description:

Helps AI-agent users and maintainers plan and execute GitHub-style developer workflows, including bug fixes, setup hardening, reliability work, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI-agent users, skill authors, maintainers, and teams use this skill to turn GitHub-style software and data workflow requests into concrete plans, artifacts, checklists, code changes, shell commands, configuration guidance, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad GitHub/developer workflow triggers may cause the skill to activate for requests that need repository changes, API calls, issue or pull request activity, or command execution.

Mitigation: Review the agent's proposed actions before allowing repository changes, API calls, issue or pull request activity, or command execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-002325)
- [Requirement plan](artifact/references/requirement-plan.md)
- [ClawHub Github skill demand signal](https://clawhub.ai/skills/github)
- [Hacker News sandbox workflow signal](https://news.ycombinator.com/item?id=48632192)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reusable checklists, local scripts, verification commands, implementation notes, assumptions, limits, and follow-up risks.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
