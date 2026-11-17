## Description:

Scaffold the standard ai/ directory structure in any repo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to create or normalize an ai/ workspace for plans, notes, development updates, todos, and product documentation inside a repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the tool on a repository with an existing ai/ folder reorganizes that folder by moving current contents under ai/_sort/ai_old/.

Mitigation: Use --dry-run first on existing repositories, and avoid --yes unless you are comfortable with the planned move.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/skills/wip-repo-init)
- [AI DevOps Toolbox](https://github.com/wipcomputer/wip-ai-devops-toolbox)
- [Skill definition](SKILL.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Generated repository files and Markdown templates, with CLI guidance for command-line use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+; supports dry-run preview and confirmation controls for existing ai/ folders.]

## Skill Version(s):

1.9.72 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
