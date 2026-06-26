## Description: <br>
Automates update tracking for OpenClaw and other GitHub-released tools by monitoring a watchlist, reviewing release notes with a security lens, checking for regressions, and preparing approval-ready recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziggy2socks](https://clawhub.ai/user/ziggy2socks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Update Scout to monitor GitHub-released tools, compare installed and latest versions, review release notes and post-release issues, and decide whether to upgrade, wait, or skip. It also helps maintain a local watchlist and skip list for periodic checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured version-check commands can run locally and may be unsafe if a watchlist entry is untrusted. <br>
Mitigation: Keep watchlist entries limited to trusted commands, review ~/.config/scout/watchlist.json before scheduled checks, and inspect proposed upgrade or restart commands before approval. <br>
Risk: Update recommendations can be incomplete when release notes or post-release issue data are incomplete. <br>
Mitigation: Review the recommendation card and verify release stability before approving installation. <br>


## Reference(s): <br>
- [Scout Watchlist Reference](references/watchlist.md) <br>
- [Update Scout on ClawHub](https://clawhub.ai/ziggy2socks/update-scout) <br>
- [ziggy2socks ClawHub Publisher Profile](https://clawhub.ai/user/ziggy2socks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown recommendation cards, JSON reports, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local watchlist and skip-list JSON files, call GitHub APIs, and run configured local version-detection commands.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
