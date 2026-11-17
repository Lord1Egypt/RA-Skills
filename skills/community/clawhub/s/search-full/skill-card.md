## Description:

Searches the web with SearXNG, fetches the full page with Crawl4AI, and answers from the extracted page content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettajiayi](https://clawhub.ai/user/bettajiayi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when search snippets are insufficient and they need to search the web, open the best result, and answer from full extracted Markdown page content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive queries may be sent through remote or shared search and crawl services.

Mitigation: Avoid sending sensitive queries unless the configured SearXNG and Crawl4AI services are trusted for logging and privacy.

Risk: A target page may fail to open or may not provide usable extracted content.

Mitigation: Report page-open failures clearly and answer only from accessible extracted content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettajiayi/skills/search-full)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown page content and concise natural-language answers, with a fixed shell command when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on the local ocsearch command and configured SearXNG/Crawl4AI services; reports page-open failures rather than inventing content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
