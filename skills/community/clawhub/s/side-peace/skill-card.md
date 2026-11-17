## Description:

Minimal secure secret handoff with no external dependencies: a human opens a browser form, submits a secret, and the agent receives it through a temporary file without printing the secret to stdout or logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitbrujo](https://clawhub.ai/user/bitbrujo)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to hand a credential or other secret from a human browser session to an agent process through a local temporary file, avoiding exposure of the secret in command output or chat logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The credential entry server can be exposed too broadly for a secret handoff workflow.

Mitigation: Review before installing or using with real credentials, and prefer a version that binds to localhost by default or uses a one-time secret URL or other authentication.

Risk: The submission endpoint lacks protective controls for request size and form label handling.

Mitigation: Limit request size and escape the displayed label before using the skill in environments where untrusted users can reach the form.

Risk: Credential handling can remain risky after receipt if tokens are passed through command-line arguments or unpinned commands.

Mitigation: Avoid passing secrets through unpinned npx commands or command-line arguments, and delete the temporary secret file immediately after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bitbrujo/skills/side-peace)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [Plain text status messages, shell command examples, and a local secret file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The submitted secret is written to a temporary file and is not printed to stdout.]

## Skill Version(s):

1.1.1 (source: release evidence; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
