## Description:

Helps AI-agent users, skill authors, maintainers, and teams turn GitHub-style workflow needs into practical bug-fixing, setup-hardening, reliability, checklist, analysis, and implementation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI-agent users, skill authors, maintainers, and teams use this skill to structure GitHub-style work such as bug fixing, setup hardening, reliability improvements, workflow creation, and adjacent skill planning. It produces practical outputs that clarify constraints, define success criteria, and include verification steps when code or data is involved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger keywords and implicit invocation can activate the skill on unrelated coding requests.

Mitigation: Confirm the skill is relevant before relying on its workflow and prefer narrower trigger wording in future versions.

Risk: Workflow guidance or generated code changes may be incorrect for a specific repository or environment.

Mitigation: Review proposed changes and run the verification commands before deployment or reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-110309)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub Github skill demand](https://clawhub.ai/skills/github)
- [Hacker News demand signal](https://news.ycombinator.com/item?id=48661232)
- [V2EX coding-agent demand signal](https://www.v2ex.com/t/1222867)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or text with checklists, implementation steps, code changes, and verification commands as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, limits, remaining risks, and next-step notes.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
