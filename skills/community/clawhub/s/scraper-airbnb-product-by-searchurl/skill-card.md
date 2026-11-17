## Description:

Prepare Dataify builder requests for the airbnb.com scraper family rooted at airbnb_product_by-searchurl, guiding tool selection, parameter collection, and curl command generation with DATAIFY_API_TOKEN.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare Dataify scraper builder requests for Airbnb search URL and location tools. It helps collect required parameters, normalize selectable values, and produce a ready-to-run curl request for Dataify.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated curl commands can expose a live DATAIFY_API_TOKEN in logs, transcripts, or shared output.

Mitigation: Review output before sharing, avoid pasting token-bearing commands into public channels, and rotate any token that has already appeared in logs or transcripts.

Risk: User-supplied parameter values are embedded into generated shell commands and may create unsafe requests if they are untrusted.

Mitigation: Use trusted values files, inspect generated commands before execution, and avoid running commands that contain unexpected parameter values.

Risk: The artifact recommends persistent shell-profile token setup, which can leave credentials stored longer than necessary.

Mitigation: Prefer session-scoped or managed secret storage for DATAIFY_API_TOKEN when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/scraper-airbnb-product-by-searchurl)
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill)
- [Dataify builder endpoint](https://scraperapi.dataify.com/builder)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash or PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated curl output may include a live DATAIFY_API_TOKEN and user-provided scraper parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
