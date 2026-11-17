## Description:

Search Google programmatically using the Serper.dev API and return structured organic results with titles, URLs, snippets, displayed links, and domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to query Serper.dev for web search, news, image, shopping, and places results. It is especially suited to lead generation, competitor research, content research, and local business discovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to a third-party Serper.dev API and may reveal sensitive intent or business context.

Mitigation: Do not use the skill with secrets, confidential business plans, regulated personal data, or private internal prompts.

Risk: Lead-generation results can include business contact information whose collection or use may be regulated or limited by policy.

Mitigation: Confirm that collecting and using contact information complies with applicable laws, platform terms, and organizational policies.

Risk: The skill requires a Serper API key for third-party API access.

Mitigation: Provide SERPER_API_KEY only in a controlled environment and rotate or revoke the key if it is exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maverick-software/skills/serper-dev)
- [Serper Web Search Endpoint](https://google.serper.dev/search)
- [Serper News Endpoint](https://google.serper.dev/news)
- [Serper Images Endpoint](https://google.serper.dev/images)
- [Serper Places Endpoint](https://google.serper.dev/places)
- [Serper Shopping Endpoint](https://google.serper.dev/shopping)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Python snippets, environment-variable configuration, tables, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SERPER_API_KEY and produces guidance for third-party Serper.dev API calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
