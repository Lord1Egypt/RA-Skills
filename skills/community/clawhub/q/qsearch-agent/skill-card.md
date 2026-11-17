## Description:

QSearch Agent is a general-purpose search assistant that responds to /sp, /search, /\u627e, and /\u641c prompts to find results for movies, novels, stocks, news, images, tutorials, and other topics while filtering advertising, phishing, and illegal content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kany2000](https://clawhub.ai/user/kany2000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to request concise web search results across Chinese and English topics through short slash commands. It is intended for broad information lookup, including media, tutorials, news, images, and stock-related queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be sent to external search or model providers.

Mitigation: Do not submit secrets, private personal data, or confidential business information as search queries.

Risk: The trigger language is broad and may activate for general search requests beyond explicit slash commands.

Mitigation: Review activation wording before deployment if the release should only respond to /sp, /search, /\u627e, or /\u641c commands.

Risk: Returned search results can still be incomplete, outdated, or misleading despite filtering.

Mitigation: Verify important results against trusted sources before acting on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown search-result summaries with titles, descriptions, and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically returns 5-10 filtered search results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
