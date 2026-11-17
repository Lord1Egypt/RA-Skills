## Description:

Weekday AI briefing - fetches top AI stories from Hacker News and dev.to, then generates a 3-item curated briefing post in Sol's voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrree](https://clawhub.ai/user/amrree)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to automate a weekday AI-news briefing workflow that curates stories, drafts a short post, and publishes it to a GitHub-backed Jekyll site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish generated Jekyll posts and push changes to GitHub automatically on a weekday schedule.

Mitigation: Confirm the launchd schedule, review the referenced pipeline script, and add a dry-run or human approval step before commit or push.

Risk: The skill uses local MiniMax and GitHub credentials and specific local repository paths.

Mitigation: Use narrowly scoped credentials, verify the configured paths before deployment, and install only where automatic publication to the target site is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/amrree/skills/sol-quick-hits)
- [sol-skills-bundle Source Repository](https://github.com/TheSolAI/sol-skills-bundle)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown briefing post plus agent guidance for local file creation and publishing commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates dated Jekyll posts and may trigger commits and pushes when configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
