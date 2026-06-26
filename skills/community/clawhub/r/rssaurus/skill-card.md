## Description: <br>
Uses the RSSaurus command-line client to authenticate with rssaurus.com, list feeds and items, output or open item URLs, and perform RSS triage actions such as marking items read or saved. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justinburdett](https://clawhub.ai/user/justinburdett) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate RSSaurus from the terminal for feed review, URL extraction, scripting, authentication troubleshooting, and item state changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RSSaurus CLI configuration may contain API tokens. <br>
Mitigation: Do not print CLI config files; re-authenticate or share only non-sensitive error details when authentication fails. <br>
Risk: Bulk read, unread, save, and unsave commands can change RSSaurus account state. <br>
Mitigation: Run bulk actions only after confirming the intended account and item scope with commands such as rssaurus auth whoami and filtered item listings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justinburdett/rssaurus) <br>
- [RSSaurus service](https://rssaurus.com) <br>
- [RSSaurus CLI repository](https://github.com/RSSaurus/rssaurus-cli) <br>
- [RSSaurus Homebrew tap](https://github.com/RSSaurus/tap) <br>
- [RSSaurus token creation](https://rssaurus.com/api_tokens/new) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-producing RSSaurus CLI commands when IDs are needed for scripting; avoid printing config files that may contain API tokens.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
