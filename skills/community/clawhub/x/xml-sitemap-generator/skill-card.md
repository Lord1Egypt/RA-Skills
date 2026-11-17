## Description:

Generates XML sitemaps by crawling same-domain website pages or scanning local HTML, Markdown, and PHP files, with optional robots.txt output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to create sitemap.xml and robots.txt outputs for websites or local static content before SEO publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTPS certificate and hostname verification are disabled during crawl mode, so sitemap results from HTTPS sites could be manipulated on an untrusted network.

Mitigation: Use the skill only on trusted networks or in local-file mode until normal certificate validation is restored or an explicit warned insecure mode is added.

Risk: The skill can crawl websites and write sitemap.xml and robots.txt outputs.

Mitigation: Use it only for sites you are authorized to crawl and choose output paths deliberately before writing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/xml-sitemap-generator)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Markdown instructions with shell command examples; generated outputs can be XML, JSON, text, sitemap.xml, and robots.txt.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can crawl up to a configurable page limit and can write sitemap.xml and robots.txt to deliberate output paths.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and script __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
