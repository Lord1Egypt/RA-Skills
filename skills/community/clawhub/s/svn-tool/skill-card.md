## Description:

Subversion (SVN) code version-control helper that uses the svn CLI for checkout, update, commit, status, log, branching, diff, cleanup, and conflict-resolution workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjbook](https://clawhub.ai/user/bjbook)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need agent guidance for common SVN working-copy and repository tasks, including checkout, update, commit, status review, history inspection, branch operations, diffs, cleanup, and conflict resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SVN commands proposed by the skill can delete local work, remove cached credentials, or perform recursive reverts and cleanup operations.

Mitigation: Require explicit user approval before commits, deletes, recursive reverts, cleanup operations, or authentication-cache changes.

Risk: The artifact includes a certificate trust bypass example using --trust-server-cert.

Mitigation: Use --trust-server-cert only after the server certificate has been verified through a trusted channel.

Risk: The security verdict is suspicious because the skill under-warns about destructive SVN operations and unsafe certificate handling.

Mitigation: Review before installing or using the skill in an agent that can run commands automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bjbook/skills/svn-tool)
- [SVN Tool examples](artifact/examples/README.md)
- [SVN Tool configuration notes](artifact/config/README.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are command-oriented guidance for SVN workflows and should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
