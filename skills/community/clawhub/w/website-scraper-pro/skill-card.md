## Description:

Scrapes a single web page into clean markdown or deterministic JSON with optional JavaScript-aware rendering and query-focused narrowing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youpele52](https://clawhub.ai/user/youpele52)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and external users use this skill to retrieve content from a specific public HTTP or HTTPS page as markdown or JSON for downstream reading, extraction, or automation. It is suited to single-page retrieval rather than broad search or site-wide crawling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary user-provided URLs from the execution environment.

Mitigation: Run it in a sandbox with restricted outbound network access and avoid internal, private, localhost, or cloud metadata URLs.

Risk: The skill relies on runtime setup for Crawl4AI and browser support.

Mitigation: Use a reviewed, prebuilt environment or pin dependencies before running it on sensitive systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youpele52/skills/website-scraper-pro)
- [Crawl4AI project homepage](https://github.com/unclecode/crawl4ai)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown or JSON returned from a command-line scrape of one URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON output can include title, URL, markdown, links, metadata, JavaScript mode, query, and markdown source.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
