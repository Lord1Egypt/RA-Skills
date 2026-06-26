## Description: <br>
Plan and run X (Twitter) operations in three modes: (1) monitor-only intelligence, (2) draft-and-approve posting, and (3) limited automation with strict guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inceptivco](https://clawhub.ai/user/inceptivco) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to monitor X activity, draft posts or replies for approval, define posting guardrails, schedule content, and review account performance before enabling any limited automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Posting automation could affect an X account if credentials are added and limited automation is enabled. <br>
Mitigation: Start in monitor-only or draft-and-approve mode, require explicit approval before publishing, and enable limited automation only for pre-approved playbooks. <br>
Risk: Account misuse or over-posting could occur without clear operational limits. <br>
Mitigation: Use a dedicated low-privilege X app or account where possible, store API keys locally, set daily and hourly caps, configure quiet hours and banned topics, and verify the kill switch before enabling automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/inceptivco/x-agent) <br>
- [Publisher profile](https://clawhub.ai/user/inceptivco) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with briefs, draft packages, guardrail settings, and automation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed to keep automation disabled until explicitly enabled with guardrails such as approval, hard caps, quiet hours, banned topics, and a kill switch.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
