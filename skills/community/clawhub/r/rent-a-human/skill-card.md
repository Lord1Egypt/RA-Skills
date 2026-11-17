## Description:

rentahuman.ai helps agents search human profiles, post paid bounties, start conversations, and coordinate physical-world tasks through RentAHuman.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexanderliteplo](https://clawhub.ai/user/alexanderliteplo)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to browse available humans, review profiles and ratings, and coordinate paid physical-world work such as package pickup, photography, event attendance, errands, and in-person meetings. Authenticated workflows can post bounties, message humans, and accept or reject applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real-world hiring, messaging, and application decisions that may create financial, safety, privacy, or operational consequences.

Mitigation: Require explicit per-action approval before posting bounties, messaging humans, accepting applications, or changing task status, and review task details before submission.

Risk: Task descriptions and conversations may expose addresses, package identifiers, schedules, or other unnecessary personal details.

Mitigation: Share only the minimum details needed for the task, redact sensitive identifiers when possible, and avoid storing or repeating private information in routine agent context.

Risk: Referenced account, API-key, prepaid-card, and payment workflows can expose credentials or payment instruments if used by routine agent automation.

Mitigation: Keep API-key management, prepaid-card details, escrow funding, and payment release behind manual review, and do not expose card details or raw API keys to ordinary task workflows.

## Reference(s):

- [RentAHuman API Reference](references/API.md)
- [RentAHuman](https://rentahuman.ai)
- [RentAHuman Dashboard](https://rentahuman.ai/dashboard)
- [ClawHub Skill Page](https://clawhub.ai/alexanderliteplo/skills/rent-a-human)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands, JSON request examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only browsing can use public API calls; authenticated operations require RENTAHUMAN_API_KEY and Node.js.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
