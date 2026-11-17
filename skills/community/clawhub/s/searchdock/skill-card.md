## Description:

Helps agents inspect Google Search Console search performance, sitemaps, and indexed URLs through SearchDock's read-only tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xplormityai](https://clawhub.ai/user/xplormityai)

### License/Terms of Use:

MIT-0

## Use Case:

Site owners and SEO teams use this skill to review Search Console traffic, query and page performance, sitemap status, and indexing evidence for a verified property.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search Console reports may reveal private search queries and page performance data.

Mitigation: Treat reports as private and keep tokens, OAuth client files, sign-in URLs, and private reports out of responses and public artifacts.

Risk: Using an untrusted CLI package or an unintended Search Console property could expose sensitive site data.

Mitigation: Confirm trust in the SearchDock CLI package and use only the verified property the user intends to inspect; ask when multiple properties exist.

## Reference(s):

- [SearchDock on ClawHub](https://clawhub.ai/xplormityai/skills/searchdock)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should include the returned date range and indicate when row limits were reached; indexing actions and live tests require Search Console outside this skill.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
