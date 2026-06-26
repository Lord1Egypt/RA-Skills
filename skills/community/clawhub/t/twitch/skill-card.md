## Description: <br>
Manage Twitch channel data, scores, and rankings from CLI. Use when rolling highlights, scoring streams, ranking metrics, tracking stats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a local Twitch-themed CLI for recording stream-related actions, viewing recent activity and statistics, searching entries, and exporting local history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Twitch history and exports are stored in plaintext under ~/.local/share/twitch. <br>
Mitigation: Do not enter passwords, OAuth tokens, private stream notes, or other secrets; periodically review or remove the local data directory if retained history is not desired. <br>


## Reference(s): <br>
- [Twitch skill page](https://clawhub.ai/ckchzh/twitch) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, CSV] <br>
**Output Format:** [Plain text CLI output with optional JSON, CSV, or TXT exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local logs and exports under ~/.local/share/twitch.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
