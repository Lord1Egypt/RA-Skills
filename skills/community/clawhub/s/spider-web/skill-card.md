## Description:

Spider Web Trigger Network indexes installed skills, matches natural-language requests against trigger words, and recommends the most relevant skill through command-line tools or a local dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to index installed skills, test trigger-word coverage, and route ambiguous user requests to candidate skills. It is most useful in local skill collections where routing recommendations should remain reviewable before another skill is loaded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan installed skills and create a trigger database that reveals local skill names and routing metadata.

Mitigation: Treat the trigger database as sensitive local data and avoid sharing exports unless the installed skill inventory can be disclosed.

Risk: The dashboard exposes routing data and match operations through a local web server.

Mitigation: Keep the dashboard bound to localhost, avoid running it on a network-facing host, and stop the server when review is complete.

Risk: Routing recommendations could cause an agent to load or invoke another skill without enough user context.

Mitigation: Require user confirmation before loading matched skills, especially when the match confidence is low or multiple skills have close scores.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/spider-web)
- [Publisher profile](https://clawhub.ai/user/bettermen)
- [Repository link from metadata](https://github.com/bettermen/spider-web)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON match results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can read and regenerate a local trigger database and can expose a localhost dashboard when the server script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
