## Description:

Autonomous multi-agent code generation. Planner creates manifest, specialized roles execute tasks. Generates complete projects with tests, Docker, CI, and decision logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arunnadarasa](https://clawhub.ai/user/arunnadarasa)

### License/Terms of Use:


## Use Case:

Developers use this skill to turn a plain-English software request into a complete generated project with coordinated planning, implementation, tests, Docker/CI assets, decision logs, and run summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated output can write files outside the intended project folder.

Mitigation: Install and run only in a throwaway or tightly isolated workspace with no valuable files nearby until the path traversal issue is fixed.

Risk: Prompts, generated decisions, and agent reasoning may be retained in DECISIONS.md and .learnings/.

Mitigation: Do not include secrets or sensitive data in prompts; review generated logs before committing or sharing.

Risk: Generated code, including blockchain or authentication integrations, may be incorrect or unsafe for deployment.

Mitigation: Review, test, and scan generated code before deploying or connecting real credentials, wallets, or production data.

## Reference(s):

- [Hackathon Swarm Coding on ClawHub](https://clawhub.ai/arunnadarasa/skills/swarm-coding-skill)
- [OpenRouter API Keys](https://openrouter.ai/keys)
- [Privy Agentic Wallets Skill](https://clawhub.ai/tedim52/privy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Project files with Markdown decision logs, summaries, configuration files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated projects under swarm-projects/{timestamp}/ and records decision and learning logs for review.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
