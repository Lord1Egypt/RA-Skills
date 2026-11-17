## Description:

Use the RSSaurus command-line client (Go binary `rssaurus`) to interact with https://rssaurus.com from the terminal: authenticate (`rssaurus auth login/whoami`), list feeds/items, print item URLs for piping, open URLs, and perform triage actions (mark read/unread, bulk mark-read, save/unsave).

This skill is ready for commercial/non-commercial use.

## Publisher:

[justinburdett](https://clawhub.ai/user/justinburdett)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to operate an authenticated RSSaurus account from the terminal for feed review, item listing, URL extraction, and RSS triage actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through RSSaurus account actions that change item state, including bulk mark-read operations.

Mitigation: Review proposed mark-read, read, unread, save, and unsave commands before execution, especially commands that target all items or an entire feed.

Risk: RSSaurus CLI configuration may contain API tokens or other sensitive authentication details.

Mitigation: Do not print or share CLI config contents; re-authenticate or share only non-sensitive error details when troubleshooting.

## Reference(s):

- [RSSaurus skill page](https://clawhub.ai/justinburdett/skills/rssaurus)
- [RSSaurus CLI repository](https://github.com/RSSaurus/rssaurus-cli)
- [RSSaurus Homebrew tap](https://github.com/RSSaurus/tap)
- [RSSaurus API token creation](https://rssaurus.com/api_tokens/new)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON CLI output when item IDs are required for scripted RSSaurus actions.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
