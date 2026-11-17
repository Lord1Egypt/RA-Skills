## Description:

Agent Marketplace helps agents and developers discover, search, rate, version, and install skills from local or remote registries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to expose a marketplace-style API for skill catalog browsing, search, ratings, version selection, dependency checks, and installation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can save unverified remote or registry-provided skill code locally.

Mitigation: Use only trusted HTTPS registries, require signed or otherwise verified skills, and review packages before installation.

Risk: Marketplace cache files may retain user identifiers, ratings, reviews, installation history, or activity data.

Mitigation: Use cache directories with appropriate permissions and define a retention policy before using real user or registry data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-agent-marketplace)
- [Publisher profile](https://clawhub.ai/user/yuyonghao-123)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with JavaScript and shell command examples, plus Node.js module outputs from marketplace APIs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces filesystem cache and registry state when its marketplace APIs are used.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
