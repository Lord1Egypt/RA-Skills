## Description:

Create and launch an Instantly.ai cold email campaign with D0/D3/D8 sequences and bulk-import leads via the Instantly API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and sales teams use this skill to configure and run code-driven Instantly.ai outreach campaigns without using the dashboard. It is suited for B2B outreach workflows that need reusable campaign templates, scheduled sequences, and bulk lead import.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can create or reuse campaigns, add sequences, and upload lead data to Instantly.ai using the provided API key.

Mitigation: Use an Instantly API key with only the intended access, and review the campaign name, sequence copy, schedule, timezone, and leads file before running.

Risk: Lead imports send contact data to an external email campaign service.

Mitigation: Confirm the lead file contains only approved recipients and fields for the campaign before import.

Risk: The artifact notes that the Instantly API v2 sequence endpoint can occasionally return 404, requiring manual sequence setup.

Mitigation: Check the console output after execution and manually verify campaign sequences in the Instantly dashboard when the API sequence call fails.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zero2ai-hub/skills/skill-instantly-campaign-launcher)
- [Publisher Profile](https://clawhub.ai/user/zero2ai-hub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, JSON, and JavaScript examples; Node.js console output when run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script creates or reuses an Instantly campaign, attempts to add email sequences, imports leads, and reports total, imported, skipped, and failed counts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
