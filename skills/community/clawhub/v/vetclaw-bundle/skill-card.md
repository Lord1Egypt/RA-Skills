## Description: <br>
VetClaw Bundle provides 52 AI automation skills for pet hospitals and veterinary clinics, covering scheduling, medical record workflows, customer follow-up, operations, and business reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Veterinary clinic owners, doctors, assistants, and operations staff use this skill bundle to automate front-desk intake, appointment reminders, record workflows, client communications, inventory, finance, marketing, and reporting. Clinical diagnosis and treatment decisions remain with licensed veterinary staff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundle stores and exposes sensitive clinic, client, and pet records. <br>
Mitigation: Put the system behind authentication, restrict access to records and reports by role, and define retention and deletion practices before deployment. <br>
Risk: Some workflows can mutate records or create appointments. <br>
Mitigation: Require human confirmation before writes to records, appointments, financial entries, or customer communications. <br>
Risk: External AI, SMS, and WeChat integrations may send customer or staff data outside the clinic environment. <br>
Mitigation: Do not configure DeepSeek, SMS, or WeChat keys until affected customers and staff have been told what data may be sent and appropriate consent or opt-out controls are in place. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daimingvip-a11y/vetclaw-bundle) <br>
- [VetClaw Wiki](https://github.com/DMNO1/vetclaw-bundle/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown, JSON-like records, configuration snippets, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce clinic workflow content, customer-facing messages, structured records, schedules, reminders, reports, and setup guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
