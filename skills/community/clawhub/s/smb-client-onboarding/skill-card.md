## Description: <br>
Local client onboarding tracker that stores client records, tracks onboarding steps, and optionally generates reminder text via MiniMax. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzargona](https://clawhub.ai/user/jzargona) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agencies, consultants, and freelancers use this skill to keep local records for client onboarding, monitor incomplete steps, configure reminders, and draft reminder text for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Client names, contact emails, contract values, and onboarding status are stored locally and may be sensitive. <br>
Mitigation: Use only on machines where local JSON storage is acceptable and protect ~/.openclaw/smb-client-onboarding/ according to client-data handling requirements. <br>
Risk: Optional reminder generation can send client identifiers, including contact email, to MiniMax. <br>
Mitigation: Leave MINIMAX_API_KEY unset unless that data sharing is approved, and review generated reminder text before using it. <br>
Risk: Several integrations are planned but not implemented in v1.0. <br>
Mitigation: Treat Gmail, WhatsApp, CRM, Stripe, project-board, Slack, Calendly, and Telegram actions as unsupported in this version and rely on manual follow-up. <br>


## Reference(s): <br>
- [SMB Client Onboarding Reference Docs](references/README.md) <br>
- [Marketplace Marketing Copy](references/marketing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON files, Guidance] <br>
**Output Format:** [Plain text status and reminder output plus local JSON configuration and onboarding records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores data under ~/.openclaw/smb-client-onboarding/; optional reminder generation calls MiniMax when MINIMAX_API_KEY is set.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release, SKILL.md frontmatter, script __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
