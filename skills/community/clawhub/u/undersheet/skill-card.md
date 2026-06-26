## Description: <br>
Persistent thread memory for OpenClaw agents across Moltbook, Hacker News, Reddit, Discord, and Twitter that tracks engaged threads, surfaces new replies, and maintains feed cursors across heartbeat sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ubgb](https://clawhub.ai/user/ubgb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use Undersheet to persist per-platform thread and feed state so recurring OpenClaw heartbeats can detect new replies, avoid rereading posts, and optionally post responses through configured platform adapters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores social-platform account credentials and can post publicly through configured services. <br>
Mitigation: Install it only for accounts where this access is intended, prefer read-only credentials when available, omit write tokens unless posting is required, and restrict credential file permissions. <br>
Risk: Automated posting or Moltbook challenge solving can act on external accounts without clear write-mode controls. <br>
Mitigation: Enable posting behavior only after explicit account-level approval and review heartbeat workflows before scheduled use. <br>


## Reference(s): <br>
- [ClawHub Undersheet Release Page](https://clawhub.ai/ubgb/undersheet) <br>
- [Undersheet Project Homepage](https://github.com/ubgb/undersheet) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [CLI text summaries with JSON state and credential configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes per-platform state under the user's Undersheet configuration directory and can call configured social-platform APIs.] <br>

## Skill Version(s): <br>
1.2.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
