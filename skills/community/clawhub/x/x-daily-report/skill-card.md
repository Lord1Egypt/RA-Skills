## Description: <br>
Generates a structured daily Markdown report from monitored X/Twitter activity by AI organizations and industry influencers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongxiaodan20001201-alt](https://clawhub.ai/user/kongxiaodan20001201-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor selected AI-related X/Twitter accounts and generate a daily intelligence brief with highlighted updates, activity summaries, and follow-up recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may reuse an existing Chrome X/Twitter login session. <br>
Mitigation: Run it only from a reviewed browser profile, preferably a dedicated profile or throwaway X account. <br>
Risk: Scheduled reporting and Feishu/Bitable destinations may send data outside the local workspace. <br>
Mitigation: Verify every destination and disable scheduled jobs until the configuration has been reviewed. <br>
Risk: The optional official API path includes mock tweet generation behavior. <br>
Mitigation: Confirm the API mode returns real live data before relying on reports generated through that path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kongxiaodan20001201-alt/x-daily-report) <br>
- [Monitored account list](references/account-list.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown report with command snippets and optional local report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read live X/Twitter content through a browser session or optional API path and may save dated Markdown reports locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
