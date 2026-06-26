## Description: <br>
Provides Twitter/X search, account monitoring, trend tracking, posting, and engagement workflows through AISA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to research Twitter/X content, monitor accounts or trends, and perform posting or engagement workflows through AISA when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured AISA API key may be exposed in normal command output. <br>
Mitigation: Review outputs before sharing them, avoid status, authorization, or posting flows with production keys until secrets are redacted, and rotate any key that may have appeared in logs or transcripts. <br>
Risk: The skill can post, reply, like, follow, and unfollow on Twitter/X after OAuth authorization. <br>
Mitigation: Grant OAuth only for accounts where those actions are acceptable, review requested actions before execution, and revoke access when it is no longer needed. <br>
Risk: Twitter/X read and write workflows depend on the AISA relay handling API keys, OAuth authorization, and account actions. <br>
Mitigation: Install and run the skill only if the user trusts the AISA relay and is comfortable granting the requested Twitter/X authority. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aisadocs/twitter-autopilot-zh) <br>
- [AISA](https://aisa.one) <br>
- [AISA API Reference](https://docs.aisa.one/reference/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; posting and engagement actions require OAuth authorization through the AISA relay.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
