## Description:

Performs Google web searches through the Serper API when provided a valid Serper API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oakcoderx](https://clawhub.ai/user/oakcoderx)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to issue web search queries through Serper and receive structured Google search results for user-requested research tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Serper and Google, so sensitive or confidential query terms could leave the user's environment.

Mitigation: Confirm the query is appropriate for an external search provider before use, and avoid searching for secrets, personal data, or confidential business terms.

Risk: A Serper API key is required, and inline key examples can lead to accidental credential exposure in shell history or shared logs.

Mitigation: Use the SERPER_API_KEY environment-variable form and avoid pasting real keys directly into commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/oakcoderx/skills/serper-web-search)
- [Publisher Profile](https://clawhub.ai/user/oakcoderx)
- [Serper API Endpoint](https://google.serper.dev/search)
- [Serper](https://serper.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON search-result structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and SERPER_API_KEY; search responses include organic results, the original query, and API credit usage.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
