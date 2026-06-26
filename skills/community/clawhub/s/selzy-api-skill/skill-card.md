## Description: <br>
Creates and sends Selzy email marketing campaigns, manages contacts, segments and templates, schedules campaigns and A/B tests, and analyzes opens, clicks and bounces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[selzy-openclaw](https://clawhub.ai/user/selzy-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and marketers use this skill to manage Selzy email marketing workflows from an agent, including contact lists, templates, campaign creation, scheduling and performance reporting. It is especially relevant when campaign sends require explicit recipient-list verification, sender checks and rate-limit discipline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent real email-campaign authority, including actions that can create or schedule sends. <br>
Mitigation: Review before installing, use a least-privileged Selzy API key if available, and require separate explicit confirmation before any createCampaign call. <br>
Risk: Campaigns can target the wrong audience if list_id and recipient counts are not verified. <br>
Mitigation: Call getLists or getList before campaign creation, verify the exact list_id and recipient count, and stop when the count is zero or unexpected. <br>
Risk: Some safety steps conflict about timing for campaign creation and scheduling. <br>
Mitigation: Follow the stricter 1-campaign-per-hour rule everywhere and ignore stale 60-second timing guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/selzy-openclaw/selzy-api-skill) <br>
- [Selzy API base endpoint](https://api.selzy.com/en/api) <br>
- [Selzy API limits](https://selzy.com/en/support/api/common/selzy-api-limits/) <br>
- [README.md](artifact/README.md) <br>
- [TEST_CHECKLIST.md](artifact/TEST_CHECKLIST.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SELZY_API_KEY and returns human-readable campaign, contact and analytics guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact metadata lists 2.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
