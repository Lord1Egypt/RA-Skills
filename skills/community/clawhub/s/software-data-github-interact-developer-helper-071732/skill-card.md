## Description:

Helps AI-agent users, skill authors, maintainers, and teams plan and execute GitHub-style workflows for bug fixes, setup hardening, reliability improvements, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, skill authors, and AI-agent users use this skill to structure GitHub-style work such as bug fixing, reliability hardening, CLI or API workflow planning, issue and PR support, and reusable checklist creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation can activate the skill for general developer-help requests.

Mitigation: Prefer explicit invocation or disable implicit invocation unless a broad GitHub/developer-workflow helper should be available automatically.

Risk: The skill may propose repository, issue, PR, CLI, or API actions that affect source code or project state.

Mitigation: Review proposed actions and verification steps before allowing an agent to execute them.

Risk: Outputs may rely on generalized workflow guidance and demand evidence rather than the user's full local context.

Mitigation: Check stated assumptions, constraints, success criteria, and remaining risks before applying the result.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-071732)
- [GitHub Demand Signal](https://github.com/bhaskarsureshkondeypati/skills-integrate-mcp-with-copilot/issues/1)
- [ClawHub GitHub Skill Demand Signal](https://clawhub.ai/skills/github)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with optional code blocks, checklists, implementation steps, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, remaining risks, and next-step notes tailored to the user's request.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
