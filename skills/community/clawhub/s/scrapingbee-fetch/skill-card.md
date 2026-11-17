## Description:

Advanced JavaScript web page renderer using the ScrapingBee API that extracts main content and returns clean Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flobo3](https://clawhub.ai/user/flobo3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to fetch JavaScript-heavy web pages through ScrapingBee and return extracted page title and body text as Markdown for LLM reading or data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs, rendering parameters, the ScrapingBee API key, and returned page content are sent through ScrapingBee.

Mitigation: Use only for approved public or non-sensitive URLs; avoid private intranet pages, authenticated pages, or URLs containing tokens unless that transfer is approved.

Risk: The security evidence notes unpinned Python dependencies.

Mitigation: Pin dependencies or run the skill in a controlled environment before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flobo3/skills/scrapingbee-fetch)
- [ScrapingBee](https://www.scrapingbee.com/)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCRAPINGBEE_API_KEY; output contains the extracted title and relevant body text from the requested URL.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
