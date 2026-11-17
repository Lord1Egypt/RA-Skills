## Description:

RTK (Rust Token Kit) is a CLI proxy that reduces LLM token consumption by compressing output from common development commands such as git, file search, tests, linters, Docker, and Kubernetes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[radicalgeek](https://clawhub.ai/user/radicalgeek)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to choose token-efficient RTK wrappers for verbose shell commands during code navigation, testing, linting, build, container, and log workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags that RTK guidance includes displaying environment variables with filters such as AWS, which could expose secrets.

Mitigation: Avoid using environment-variable filters on secret-bearing prefixes such as AWS, TOKEN, GCP, or AZURE unless values are redacted before display.

Risk: RTK tee logs and command-history analytics can retain command output on the local machine.

Mitigation: Review local RTK log and history retention settings, avoid capturing sensitive command output, and inspect full tee logs only when troubleshooting requires it.

## Reference(s):

- [RTK Full Docs](references/rtk-full-docs.md)
- [RTK GitHub Repository](https://github.com/rtk-ai/rtk)
- [RTK Documentation](https://www.rtk-ai.app)
- [RTK Troubleshooting](https://github.com/rtk-ai/rtk/blob/master/docs/TROUBLESHOOTING.md)
- [ClawHub Skill Page](https://clawhub.ai/radicalgeek/skills/rtk)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance focuses on compressed command output, optional configuration, and paths to raw tee logs when full output is needed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
