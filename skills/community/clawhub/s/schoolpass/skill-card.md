## Description:

This skill should be used when the user asks about their child's school arrival/dismissal through a SchoolPass parent account. Triggers on phrases like "check SchoolPass", "when is my kid dismissed", "what's my dismissal default", "list my students in SchoolPass", "who are my pickup drivers", "any pickup changes today", "school dismissal locations", or any request to read a SchoolPass parent account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Parents use this skill with their SchoolPass parent account to review student arrival and dismissal plans, pickup changes, authorized drivers, dismissal locations, and school information. It can also prepare or submit an arrival or dismissal change after the parent reviews and approves the confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the skill suspicious because reported write tools can change a child’s arrival or dismissal arrangements despite a read-oriented description; the analysis was partial.

Mitigation: Review the write capabilities and decide whether to allow real changes. Show the confirmation preview and obtain explicit approval before submitting a change.

## Reference(s):

- [ClawHub release](https://clawhub.ai/chrischall/skills/schoolpass)
- [Source repository](https://github.com/chrischall/schoolpass-mcp)
- [npm package](https://www.npmjs.com/package/schoolpass-mcp)

## Skill Output:

**Output Type(s):** [Structured data, Text, Guidance]

**Output Format:** [Structured SchoolPass account data and concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confirmation previews and receipts for parent-approved arrival or dismissal changes.]

## Skill Version(s):

1.1.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
