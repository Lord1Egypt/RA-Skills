## Description: <br>
Site Feeds helps agents fetch recent content and updates from websites and platforms such as YouTube, GitHub, Instagram, Reddit, news sites, and blogs without a browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heqi201255](https://clawhub.ai/user/heqi201255) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to discover available website feeds, fetch current content through airsstool, and manage persistent feed subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RSSHub setup may deploy a local Docker service and change environment configuration. <br>
Mitigation: Ask for explicit approval before Docker deployment or .env edits, and review the RSSHub deployment steps before running them. <br>
Risk: airsstool initialization and subscriptions create persistent local data that can reveal feed interests or subscription names. <br>
Mitigation: Use a custom database path for sensitive feed sets and confirm where the SQLite database will be stored before initialization. <br>
Risk: Subscription deletion commands can remove a group or path from persistent subscriptions. <br>
Mitigation: Confirm the exact user, subscription name, and path before running unsubscribe or remove-subscription commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/heqi201255/site-feeds) <br>
- [airsstool repository](https://github.com/heqi201255/airsstool) <br>
- [RSSHub deployment documentation](https://docs.rsshub.app/deploy/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and feed output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The guided CLI can return Markdown by default, with RSS, Atom, JSON, RSS3, brief text, limits, offsets, and persistent SQLite-backed subscriptions when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
