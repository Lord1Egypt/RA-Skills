## Description:

Smart Web Fetch helps agents retrieve cleaner Markdown from webpages by trying Jina Reader, markdown.new, and defuddle.md before falling back to raw page content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leochens](https://clawhub.ai/user/leochens)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to fetch public webpage content as cleaned Markdown or JSON when they need lower-noise page text for reading, summarization, or follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill forwards target URLs to third-party cleaning services.

Mitigation: Use it only for public webpages and avoid private intranet URLs, signed links, tokenized URLs, and sensitive documents unless explicit consent and destination validation are added.

Risk: The security evidence reports weakened HTTPS verification when fetching arbitrary URLs.

Mitigation: Review the code before installation and require normal HTTPS certificate verification before using it in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leochens/skills/smart-web-fetch)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration]

**Output Format:** [Markdown text or JSON emitted by command-line scripts, with optional configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source service, resolved URL, fetched content, success status, and error details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
