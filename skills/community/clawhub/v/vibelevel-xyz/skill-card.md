## Description:

Check any GitHub developer's vibe score across 7 dimensions. Compare coders, flex leaderboards, and discover who's really shipping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[therealstein](https://clawhub.ai/user/therealstein)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve and interpret public GitHub vibe data from vibelevel.xyz, compare developer profiles, and present the seven-dimension score breakdown in concise Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends GitHub usernames to vibelevel.xyz and includes that service's profile links in responses.

Mitigation: Use it only for public GitHub usernames and make the external lookup clear to the user before or during the response.

Risk: Profile-claim and vibe-score language could be read as stronger identity or quality evidence than the external service supports.

Mitigation: Present scores and claimed-profile status as vibelevel.xyz results, not as independent verification of a developer's identity or ability.

## Reference(s):

- [Vibelevel homepage](https://vibelevel.xyz)
- [ClawHub skill page](https://clawhub.ai/therealstein/skills/vibelevel-xyz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with optional shell command execution and parsed JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq on Darwin or Linux; fetches public GitHub profile vibe data from vibelevel.xyz.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
