## Description:

A safe AI agent evolution engine that analyzes runtime history to identify improvements and applies protocol-constrained evolution with comprehensive safety checks and audit logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[confidentkai](https://clawhub.ai/user/confidentkai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Safe Evolver to record local agent interactions, analyze runtime history for efficiency and error patterns, and review improvement suggestions before applying behavior changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local interaction history and log files may contain sensitive prompts, tool inputs, command output, or file paths if users provide them to recordInteraction.

Mitigation: Configure log and history paths deliberately, protect or clear generated files, and avoid recording secrets, tokens, private file contents, or sensitive command output.

Risk: Improvement suggestions may be incomplete or unsuitable for a specific agent workflow.

Mitigation: Review suggested changes before applying them and scan modified skills before deployment.

## Reference(s):

- [Safe Evolver ClawHub Skill Page](https://clawhub.ai/confidentkai/skills/safe-evolver)
- [confidentkai ClawHub Publisher Profile](https://clawhub.ai/user/confidentkai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JavaScript usage examples, with runtime reports and suggestions returned as JavaScript objects serialized to local JSON/log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local interaction history and evolution logs at configured paths.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter and package.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
