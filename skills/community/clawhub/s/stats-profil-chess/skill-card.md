## Description: <br>
Shows a Chess.com player's rapid, blitz, bullet, and puzzle statistics using the public Chess.com API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HugoRamon](https://clawhub.ai/user/HugoRamon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up public Chess.com statistics for a named player and present ratings, records, and puzzle information in a clear summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Chess.com username supplied by the user is sent to Chess.com's public API. <br>
Mitigation: Use only public Chess.com usernames and do not provide passwords, tokens, or private account information. <br>
Risk: The skill cannot modify Chess.com accounts or play chess moves for the user. <br>
Mitigation: Treat the output as read-only public statistics and use separate tools for gameplay or account management. <br>
Risk: Network errors, missing players, private profiles, or Chess.com API changes can prevent a successful lookup. <br>
Mitigation: Validate the username, handle 404 and network errors clearly, and retry later if the public API is unavailable. <br>


## Reference(s): <br>
- [Chess.com public player stats API endpoint](https://api.chess.com/pub/player/{username}/stats) <br>
- [ClawHub skill page](https://clawhub.ai/HugoRamon/stats-profil-chess) <br>
- [Publisher profile](https://clawhub.ai/user/HugoRamon) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown summary with optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a public Chess.com username; does not request credentials, tokens, or private account data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
