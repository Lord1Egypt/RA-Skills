## Description:

Automates local-business lead collection, personalized pitch drafting, and WhatsApp outreach through WAHA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[izletenadam-creator](https://clawhub.ai/user/izletenadam-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and marketing operators or developers use this skill to collect local business lead details, draft personalized outreach, and send WhatsApp messages through WAHA with batching and ignore-list controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports WhatsApp outreach to scraped business contacts.

Mitigation: Use only legally obtained contacts, document consent or another valid outreach basis, provide opt-out handling, and define retention or deletion rules for phone numbers and ignore lists.

Risk: The batch sender can expose WAHA keys when real credentials are passed on the command line.

Mitigation: Avoid passing real WAHA keys as command-line arguments; prefer a protected secret source or local environment handling and run a dry run before live sending.

Risk: Untrusted lead filenames or unrestricted WAHA endpoints can cause unintended execution or message delivery behavior.

Mitigation: Use trusted lead files only, restrict WAHA to trusted local or HTTPS endpoints, and review generated messages and recipient lists before sending.

## Reference(s):

- [Pitch Templates by Sector](references/pitch-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/izletenadam-creator/skills/whatsapp-lead-hunter)
- [Publisher Profile](https://clawhub.ai/user/izletenadam-creator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate personalized outreach copy, lead JSON structure, WAHA API calls, ignore-list configuration, and batch-send commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
