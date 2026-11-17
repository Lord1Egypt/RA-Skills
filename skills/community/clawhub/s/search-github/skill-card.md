## Description:

Search GitHub for repositories, code, issues, or projects matching the user's query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other GitHub users use this skill to have an agent open GitHub search results for repositories, code, issues, or projects matching a user-provided query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may focus or reuse an existing Brave browser and GitHub login state.

Mitigation: Review the opened page before interacting further, and stop if the workflow asks to enter credentials, create accounts, submit forms, or change GitHub data.

## Reference(s):

- [GitHub Search](https://github.com/search)
- [ClawHub Skill Page](https://clawhub.ai/ruchir17-cmd/skills/search-github)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Text instructions and browser navigation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reuse an existing Brave browser session and relevant GitHub tab when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
