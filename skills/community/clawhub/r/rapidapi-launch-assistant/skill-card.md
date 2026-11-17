## Description:

End-to-end launch and monetization skill for API products on RapidAPI and Clawhub. Use when a user wants to publish APIs, fix gateway/auth/test failures, configure plans, optimize listing conversion, run outreach, or package and sell an API-launch workflow skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leduc121](https://clawhub.ai/user/leduc121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, solo builders, indie hackers, and API founders use this skill to validate API readiness, configure marketplace auth and pricing, write conversion-focused listing copy, troubleshoot launch issues, and plan first-customer outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated launch plans or marketplace guidance could lead to unintended pricing, auth, listing, or outreach changes if applied without review.

Mitigation: Review launch plans and explicitly approve pricing, auth, listing, and outreach actions before publishing or contacting users.

Risk: The helper script reads an input JSON path and writes markdown to the requested output path.

Mitigation: Run the script only with intended local input and output paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leduc121/skills/rapidapi-launch-assistant)
- [ClawHub Packaging and Sales](references/clawhub-packaging.md)
- [Launch Channels and First-Customer Motion](references/launch-channels.md)
- [RapidAPI Listing Copy Template](references/listing-copy-template.md)
- [Pricing Playbooks by API Niche](references/pricing-playbooks.md)
- [Troubleshooting Matrix](references/troubleshooting-matrix.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional launch-plan markdown files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a launch-plan markdown file from JSON input when the helper script is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
