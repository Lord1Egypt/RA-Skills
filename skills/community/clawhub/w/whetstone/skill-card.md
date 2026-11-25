## Description:

Scales engineering care to the risk of a software change, keeping small edits light and adding evidence, compatibility and recovery checks as risk grows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardodpalmeida](https://clawhub.ai/user/ricardodpalmeida)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use Whetstone to size implementation, review, testing, and recovery work to the risks of changes in a software project. It guides work on code, configuration, infrastructure, interfaces, and AI features while keeping out-of-project prose and standalone snippets out of scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has environment and shell capabilities without a declared tool scope.

Mitigation: Review proposed commands and changes, and check host runtime permissions before execution.

## Reference(s):

- [Whetstone ClawHub release](https://clawhub.ai/ricardodpalmeida/skills/whetstone)
- [Overview, installation, and release notes](https://github.com/Ricardodpalmeida/whetstone/blob/main/README.md)
- [Understanding the ask](references/understanding-the-ask.md)
- [Testing and verification](references/testing.md)
- [Security](references/security.md)
- [Delivery and release](references/delivery-and-release.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Code, Configuration, Shell commands]

**Output Format:** [Markdown guidance and project changes such as code, configuration, tests, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scope and verification depth vary with the risk of the requested change]

## Skill Version(s):

0.3.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
