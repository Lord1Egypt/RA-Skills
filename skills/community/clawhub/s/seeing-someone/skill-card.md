## Description: <br>
Early-stage rapport: phase updates, question relay, and summaries while things are still forming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesamething](https://clawhub.ai/user/thesamething) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use Seeing Someone to check AILove matching status, relay pending deep questions, submit the user's verbatim answers, and summarize early-stage rapport updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AILOVE_API_KEY grants access to the AILove agent API and could let another party impersonate the user's agent if exposed. <br>
Mitigation: Store the key in OpenClaw secrets or an environment variable when possible, restrict any credentials file to owner-only permissions, and send the key only to https://heerweiyi.cc/api/v1/agent/*. <br>
Risk: Scheduled relationship updates can appear in channels where the user did not intend to share them. <br>
Mitigation: Create cron jobs only for appropriate user, group, or channel targets and verify delivery after setup. <br>
Risk: The skill can submit answers to pending questions, which could misrepresent the user if answers are fabricated or edited. <br>
Mitigation: Relay questions to the user and submit only the user's verbatim answer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thesamething/seeing-someone) <br>
- [AILove homepage](https://heerweiyi.cc) <br>
- [AILove Agent API base](https://heerweiyi.cc/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scheduled check-in instructions and concise relationship-status summaries.] <br>

## Skill Version(s): <br>
1.4.2 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
