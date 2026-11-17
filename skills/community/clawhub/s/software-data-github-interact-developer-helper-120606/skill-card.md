## Description:

Helps AI-agent users, skill authors, maintainers, and teams create GitHub-style workflows for bug fixing, setup hardening, reliability improvement, and related ClawHub skill work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI-agent users, skill authors, and maintainers use this skill to turn requests around GitHub-style ClawHub workflows into concrete implementation support, checklists, analyses, code changes, or verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation could activate the skill for general developer prompts where a more specific skill would fit.

Mitigation: Review trigger wording and invocation policy before deployment; prefer explicit invocation for sensitive or unrelated work.

Risk: Guidance-only outputs can still introduce incorrect workflow, code, or configuration advice if applied without project-specific review.

Mitigation: Review proposed changes, run relevant tests or scans, and confirm assumptions before applying recommendations to production systems.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-120606)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub Github Skill Demand Signal](https://clawhub.ai/skills/github)
- [Ask HN: Active GitHub accounts delivering malware](https://news.ycombinator.com/item?id=48548530)
- [Ask HN: AI dev in the cloud](https://news.ycombinator.com/item?id=48543969)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with code blocks, checklists, workflow steps, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation steps, and follow-up risks when relevant.]

## Skill Version(s):

0.20260729.110214 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
