## Description:

Search and extract data from Yandex.Archive: metric books, newspapers, and directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flobo3](https://clawhub.ai/user/flobo3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and genealogy/history workflows can use this skill to search Yandex.Archive indexes and retrieve document titles, snippets, viewer links, and image links for archive, periodical, and directory results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses stealth scraping tooling to bypass bot protection, which can violate service terms or authorization boundaries.

Mitigation: Use only with authorization for the target service, respect applicable terms and robots or rate-limit expectations, and set conservative page limits and delays.

Risk: Dependencies and browser downloads are not pinned or hash-verified in the artifact.

Mitigation: Install and run the skill in a dedicated virtual environment or container, then pin and verify dependencies before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flobo3/skills/yandex-archive-scraper)
- [Yandex Archive search](https://yandex.ru/archive/search)

## Skill Output:

**Output Type(s):** [text, JSON, links, shell commands, guidance]

**Output Format:** [Console text and JSON-like search result objects with titles, snippets, viewer URLs, thumbnail URLs, and original image URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a query string, an optional index selector, and an optional maximum page count.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
