## Description:

Swiss phone directory lookup via search.ch API for finding contact details for Swiss companies or people, reverse-looking up phone numbers, and finding business categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xenofex7](https://clawhub.ai/user/xenofex7)

### License/Terms of Use:


## Use Case:

External users, developers, and support staff use this skill to look up Swiss business and person contact details, addresses, phone numbers, and reverse phone matches through search.ch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup terms, locations, phone numbers, and the search.ch API key are sent to search.ch.

Mitigation: Use the skill only with data acceptable to share with search.ch, and provide the API key through per-session environment variables, a gateway secret, or a secrets manager.

Risk: Returned names, addresses, emails, websites, and phone links are untrusted display data.

Mitigation: Review or sanitize returned data before displaying it in Markdown-capable clients or using it in downstream workflows.

## Reference(s):

- [Configuration](configuration.md)
- [search.ch API documentation](https://search.ch/tel/api/help.en.html)
- [search.ch API key request](https://search.ch/tel/api/getkey.en.html)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown search results with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SEARCHCH_API_KEY; results may include personal contact data and clickable tel: links.]

## Skill Version(s):

1.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
