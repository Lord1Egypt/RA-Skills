## Description:

Retrieve search results from web search engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lwq057](https://clawhub.ai/user/lwq057)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run lightweight web searches across supported search engines and receive serialized search result text for follow-up analysis or citation discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to selected external search engines.

Mitigation: Do not submit secrets, credentials, private customer data, or highly confidential prompts as search terms.

Risk: Search results may be localized toward Chinese-language content.

Mitigation: Review returned results for locale relevance and corroborate important findings with additional sources when needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON-serialized array of search result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches may be run against one or more selected engines; result ordering corresponds to the requested engine order.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
