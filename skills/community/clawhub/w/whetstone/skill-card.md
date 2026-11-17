## Description:

Scales engineering care to the risk of a software change, keeping small edits light and adding evidence, compatibility and recovery checks as risk grows. Use when writing, fixing, debugging, reviewing, refactoring or shipping code, configuration, schemas and migrations, infrastructure, user interfaces, or LLM and agent features in a software project, including casual add, fix or build requests. Not for prose, slides, explanations, summaries or standalone snippets outside a project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardodpalmeida](https://clawhub.ai/user/ricardodpalmeida)

### License/Terms of Use:

MIT-0

## Use Case:

Coding agents and software developers use Whetstone to scale engineering checks to change risk, preserve contracts, verify behavior, and document recovery when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's tool scope is undeclared, and its optional change scanner invokes Git.

Mitigation: Review the actions and Git commands before use, and run the scanner only from a repository you intend to inspect.

## Reference(s):

- [Verification](references/testing.md)
- [Security](references/security.md)
- [Dependencies and build permissions](references/supply-chain.md)
- [AI boundaries](references/ai-features.md)
- [Whetstone on ClawHub](https://clawhub.ai/ricardodpalmeida/skills/whetstone)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, Shell commands, Markdown]

**Output Format:** [Task-specific engineering guidance, code or configuration changes, and Markdown reports as applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks and reporting are scaled to the risk of the change.]

## Skill Version(s):

0.3.7 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
