## Description:

Use Serpshot Google Search API to perform web searches and image searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[downdawn](https://clawhub.ai/user/downdawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current Google web and image search results through the Serpshot API when live information is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are transmitted to Serpshot as a third-party search provider.

Mitigation: Do not submit secrets, private internal URLs, confidential research topics, or personal data unless sharing them with Serpshot under the configured API key is acceptable.

Risk: Use requires a Serpshot API key and may consume paid or limited API credits.

Mitigation: Store SERPSHOT_API_KEY in the environment, avoid logging the key, monitor available credits, and handle 402 and 429 API responses before repeated use.

## Reference(s):

- [Serpshot Homepage](https://serpshot.com)
- [Serpshot API Documentation](https://serpshot.com/docs)
- [ClawHub Skill Page](https://clawhub.ai/downdawn/skills/serpshot)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SERPSHOT_API_KEY. Search queries are sent to Serpshot, and each query may consume API credits.]

## Skill Version(s):

1.1.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
