## Description:

Skill Finder Cn helps agents search ClawHub for relevant skills, inspect results, recommend install commands, and verify whether an installation succeeded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent users, and ClawHub users can use this skill to find Chinese-language recommendations for ClawHub skills, compare search results, and receive install and post-install verification commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommended third-party skill installs can change what an agent is able to do.

Mitigation: Review the recommended skill, inspect its details, and scan or validate it before running any clawhub install command.

Risk: Search results and install status can become stale as the ClawHub catalog and local installed skills change.

Mitigation: Run fresh clawhub search, inspect, list, and post-install file checks before relying on a recommendation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/skill-finder-cn)
- [Publisher profile](https://clawhub.ai/user/guohongbin-git)
- [ClawHub skill API endpoint pattern](https://clawhub.ai/api/v1/skills/<skill-name>)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and Chinese-language recommendation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and install guidance depends on the local clawhub CLI and the current ClawHub catalog.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact package metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
