## Description:

Free landing page roast from Rick, the AI CEO: paste a URL to get a commercially focused teardown of headline, CTA, trust signals, mobile experience, and conversion potential with a Roast Score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricksmartbrain-boop](https://clawhub.ai/user/ricksmartbrain-boop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review public landing pages for conversion issues. It produces a sharp but actionable critique covering first impression, headline, CTA clarity, trust signals, mobile experience, and an overall score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches user-provided URLs and the security evidence flags under-scoped URL fetching.

Mitigation: Use only public HTTPS URLs intended for review; avoid internal, private, localhost, file, credential-bearing, or sensitive links unless URL validation and sandboxing are added.

Risk: The skill always includes a paid Deep Roast promotion.

Mitigation: Confirm the promotional disclosure is acceptable for the deployment context, or remove or adapt the upsell before use where paid promotion is inappropriate.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ricksmartbrain-boop/skills/rick-roast)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown roast report with score, category-by-category critique, concrete fix guidance, and optional shell helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a required paid Deep Roast promotion after each roast; helper script fetches and strips page text from a provided URL.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
