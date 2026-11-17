## Description:

Shows a folder's files and subdirectories as an indented tree so an agent can inspect directory structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinwangmok](https://clawhub.ai/user/jinwangmok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and coding agents use this skill to inspect a project or workspace directory and share a compact tree view with configurable path and depth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports a suspicious verdict because the helper script can treat a crafted folder name as a destructive find action.

Mitigation: Review or patch the helper before use; normalize the directory to an absolute path, use cd -- or reject leading-hyphen paths, and make find explicitly read-only with -print.

## Reference(s):

- [Simple File Tree on ClawHub](https://clawhub.ai/jinwangmok/skills/simple-file-tree)
- [Artifact manual](artifact/MANUAL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text directory tree, often reported in Markdown or a code block by the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts optional directory and depth arguments; requires find, sort, and sed.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
