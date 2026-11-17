## Description:

Yula Web Search helps an agent run no-API-key web searches through public search services, fetch selected result pages with curl and Python, and summarize current information for the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjzhb](https://clawhub.ai/user/wjzhb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs current web information, news, prices, product availability, or content extracted from specific public URLs, including Chinese-language searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and fetched pages may be sent to public search engines and arbitrary websites from the user's network.

Mitigation: Use the skill in a restricted environment, avoid sensitive or private queries, and review searches before execution.

Risk: Automatic page fetching can reach unsafe destinations, including redirects to internal services or private network addresses.

Mitigation: Require confirmation before fetching pages and block localhost, private IP ranges, redirects to internal services, and unsafe query interpolation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjzhb/skills/yula-web-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown answer with source references and optional shell/Python command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are based on selected public search results and extracted page text, with artifact guidance to fetch the top 2-3 relevant URLs and limit extracted text.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
