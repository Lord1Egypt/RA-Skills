## Description: <br>
Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AISA relay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to research X/Twitter accounts, tweets, trends, lists, communities, and Spaces, then perform OAuth-approved posting and engagement actions through the AISA relay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live public X/Twitter account actions, including posting, liking, following, and unfollowing. <br>
Mitigation: Require explicit user confirmation before write actions and do not report success unless the relay returns a successful response. <br>
Risk: The OAuth client may print the raw AISA API key in command output. <br>
Mitigation: Avoid running the OAuth client in logged environments until that output is fixed, and restrict access to terminals or logs that may contain the key. <br>
Risk: Relay-backed workflows send API keys, post text, engagement targets, and uploaded media to the AISA service. <br>
Mitigation: Install and run the skill only when the operator trusts the AISA relay with those inputs. <br>


## Reference(s): <br>
- [X/Twitter OAuth posting workflow](references/post_twitter.md) <br>
- [X/Twitter engagement workflow](references/engage_twitter.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/x-intelligence-automation-aisa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and OAuth authorization for write actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
