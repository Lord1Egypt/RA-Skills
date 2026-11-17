## Description:

Use this skill to discover similar GitHub work, attach to shared agent workspaces, and coordinate tasks via .shared files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nativ3ai](https://clawhub.ai/user/nativ3ai)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to find related work, attach agents to shared repositories, and coordinate task ownership through .shared workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned global npm installation can expose users to supply-chain changes in published packages.

Mitigation: Install only from trusted publishers, prefer pinned package versions, and use an isolated environment for evaluation or deployment.

Risk: Optional GitHub integration may use credentials with broader access than the workspace task requires.

Mitigation: Use short-lived, least-privilege GitHub tokens scoped only to the repositories and actions needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nativ3ai/skills/shared-workspace)
- [agent-shared-workspace npm package](https://www.npmjs.com/package/agent-shared-workspace)
- [h1dr4 source repository](https://github.com/pokke1/h1dr4)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference optional GitHub tokens, npm packages, repository paths, branches, and .shared task files.]

## Skill Version(s):

0.1.2 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
