## Description:

Helps agents retrieve and organize the latest Vue version changelog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aliangtech](https://clawhub.ai/user/aliangtech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when they want an agent to fetch the latest Vue changelog from Vue's published GitHub changelog and save the newest section for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a Node.js script that contacts GitHub and writes a local changelog file.

Mitigation: Review the script before execution and run it only where outbound GitHub access and local file writes are acceptable.

Risk: The workflow depends on live network access to Vue's GitHub changelog.

Mitigation: Use a reviewed offline changelog source or defer execution in environments that require no-network operation.

## Reference(s):

- [Vue Core Changelog](https://raw.githubusercontent.com/vuejs/core/refs/heads/main/CHANGELOG.md)
- [ClawHub Skill Page](https://clawhub.ai/aliangtech/skills/vue-latest-changelog)
- [Publisher Profile](https://clawhub.ai/user/aliangtech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with a Node.js command and a generated Markdown changelog file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script writes the latest changelog section to assets/latest_changelog.md.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
