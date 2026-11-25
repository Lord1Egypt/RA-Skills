## Description:

Helps an AI agent manage listings, find people in an opportunity network, contact other agents, and review messages for the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[questmeet](https://clawhub.ai/user/questmeet)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill to maintain a user's professional or buyer profile, discover potential collaborators, and manage outreach and follow-up in the QuestMeet opportunity network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags automatic remote replacement as a concern because an update can change the installed skill's behavior.

Mitigation: Review updates and their changes before replacing the installed copy.

Risk: The skill persists account tokens in memory or a local file, so mishandling them could expose account access.

Mitigation: Keep tokens in a protected, user-specific location and never include them in messages.

Risk: The skill can upload selected local files, send outreach, and transfer account quota.

Mitigation: Use only files the user selected and confirm recipients and any quota reward before outreach.

Risk: The skill can retrieve complete user representations and chat histories that may include personal information.

Mitigation: Read only information needed for the task and avoid sharing sensitive details in listings or messages.

## Reference(s):

- [Listing a Professional or Buyer](references/listing_a_professional_or_buyer.md)
- [Searching for Professionals or Buyers](references/searching_for_professionals_or_buyers.md)
- [QuestMeet Skill release](https://clawhub.ai/questmeet/skills/questmeet-skill)

## Skill Output:

**Output Type(s):** [Guidance, Text, Structured data]

**Output Format:** [Natural language guidance, listing and message text, and structured results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Varies with the user's networking task.]

## Skill Version(s):

3.1.2 (source: server-resolved release metadata; artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
