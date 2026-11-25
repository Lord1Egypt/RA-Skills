## Description:

Resolve a company website, name, Google Maps listing or lead dataset to its LinkedIn, X, YouTube, Instagram and Facebook profiles, with evidence; Instagram and Facebook come from the company's site by default and are not platform-verified.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geminigeorge22](https://clawhub.ai/user/geminigeorge22)

### License/Terms of Use:

MIT

## Use Case:

External users and agents can identify and enrich company records with social profile links from a company name, website, Google Maps listing or existing lead dataset. It is limited to organizations and includes evidence to help assess profile matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended Apify MCP connection exposes unrelated Apify tools.

Mitigation: Review which Actors the connection enables and limit the connection to the company-profile lookup and the tools it needs; check what the Apify account token can access.

Risk: The example API request is an incomplete template and does not match the stated lookup purpose.

Mitigation: Confirm the intended Actor endpoint and input schema before running an API request; keep account tokens out of public files.

## Reference(s):

- [Apify company social profile finder](https://apify.com/publicrecords/company-social-profile-finder)
- [ClawHub skill page](https://clawhub.ai/geminigeorge22/skills/publicrecords-company-social-profiles)

## Skill Output:

**Output Type(s):** [Structured data, Guidance]

**Output Format:** [Company profile results with social URLs and supporting evidence; exact dataset fields depend on the Actor output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instagram and Facebook links use the company's own site by default and are not platform-verified.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
