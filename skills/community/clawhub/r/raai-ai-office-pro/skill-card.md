## Description: <br>
Operational chief-of-staff for Russian CEOs: OKR, weekly review, decision log, briefing, delegation and strategic priorities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raaipro](https://clawhub.ai/user/raaipro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
CEOs, owners, and operating leaders use this skill to structure business cadence through daily briefings, OKRs, weekly reviews, decision logs, delegation checkpoints, quarterly planning, and investor updates. It is aimed at Russian-language small and midsize businesses that already have teams, metrics, and recurring management cycles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle sensitive company metrics, decisions, team details, and operating cadence. <br>
Mitigation: Review the configuration before connecting real company data, use scoped credentials, and keep optional integrations disabled until access boundaries are approved. <br>
Risk: Calendar, diary, Telegram, CRM, or Sheets actions may change operational records without clear approval gates. <br>
Mitigation: Require explicit user confirmation before any write action and start with read-only or disabled integrations during evaluation. <br>
Risk: Broad production triggers can route ordinary messages into management workflows. <br>
Mitigation: Avoid broad one-word triggers in production and use stricter intent routing or confirmation prompts for workflow activation. <br>
Risk: Installation can affect an existing ai-office-pro skill directory. <br>
Mitigation: Back up any existing ai-office-pro directory before installation or upgrade. <br>


## Reference(s): <br>
- [ClawHub listing for Ai Office Pro](https://clawhub.ai/raaipro/raai-ai-office-pro) <br>
- [Quick Start](examples/quick-start.md) <br>
- [Onboarding Guide](docs/onboarding.md) <br>
- [Anti-Fail Guide](docs/anti-fail.md) <br>
- [Dogfooding Evidence](proof/dogfooding-RAAI.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Structured Russian-language Markdown or plain text for briefings, OKRs, weekly reviews, decision logs, delegation plans, quarterly plans, and investor updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on user-provided business metrics and optional integrations such as Sheets, Calendar, Telegram, CRM, or diary tools.] <br>

## Skill Version(s): <br>
3.5.4 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
