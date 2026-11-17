## Description:

Use the wallapop CLI to search listings, fetch item details, view user profiles, and list categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pjtf93](https://clawhub.ai/user/pjtf93)

### License/Terms of Use:


## Use Case:

Developers, analysts, and marketplace operators use this skill to get concise wallapop-cli commands for searching Wallapop listings, retrieving item and user details, listing categories, and requesting JSON output for scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may install an untrusted wallapop-cli package or expose an access token unnecessarily.

Mitigation: Install only a trusted wallapop-cli package and set WALLAPOP_ACCESS_TOKEN only when authenticated item or user lookups require it.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference WALLAPOP_LAT, WALLAPOP_LNG, and optional WALLAPOP_ACCESS_TOKEN environment variables for CLI configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
