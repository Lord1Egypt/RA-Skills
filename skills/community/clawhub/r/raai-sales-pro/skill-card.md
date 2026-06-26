## Description: <br>
Full sales system: scripts, objection handling, follow-up, BANT and MEDDIC qualification, pipeline management and commercial offers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raaipro](https://clawhub.ai/user/raaipro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales leaders, business owners, and sales teams use this skill to generate and adapt sales scripts, objection handling, follow-up sequences, lead qualification, pipeline reports, win/loss analysis, commercial proposals, and unit economics guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer, lead, and pipeline data may be processed or synced through memory, Supabase, messaging, CRM, or timer integrations without clear retention and deletion controls. <br>
Mitigation: Enable integrations only after confirming what data is stored, who can access it, customer opt-out handling, retention periods, and deletion procedures. <br>
Risk: The skill may require sensitive credentials for optional LLM, Telegram, WhatsApp, CRM, or related integrations. <br>
Mitigation: Configure only the integrations needed for the deployment, store credentials outside shared skill files, restrict scopes, and rotate tokens if exposed. <br>
Risk: Generated sales scripts, ROI claims, commercial offers, and pipeline analysis can be misleading if source data is incomplete or inaccurate. <br>
Mitigation: Have a sales owner review customer-facing outputs and validate assumptions, metrics, and claims before use. <br>
Risk: Pipeline forecasts and win/loss conclusions depend on current and truthful business data. <br>
Mitigation: Keep config and pipeline inputs current, record real loss reasons, and review forecasts before making business decisions. <br>


## Reference(s): <br>
- [Sales Pro marketplace page](https://clawhub.ai/raaipro/raai-sales-pro) <br>
- [Publisher profile](https://clawhub.ai/user/raaipro) <br>
- [README](artifact/README.md) <br>
- [Onboarding guide](artifact/docs/onboarding.md) <br>
- [Anti-fail guide](artifact/docs/anti-fail.md) <br>
- [ROI guide](artifact/docs/roi.md) <br>
- [Quick start examples](artifact/examples/quick-start.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured plain text with optional shell commands and YAML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces sales process artifacts and analytical guidance from user-supplied sales context; core use does not require external API calls.] <br>

## Skill Version(s): <br>
3.5.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
