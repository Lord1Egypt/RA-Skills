## Description:

Searches the web through configurable SearXNG instances and returns aggregated results across supported engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoncatbot](https://clawhub.ai/user/simoncatbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run current web, news, image, video, file, and science searches through a configured public or self-hosted SearXNG instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to the configured SearXNG instance, including the default public instance.

Mitigation: Use a trusted or self-hosted SearXNG instance for sensitive workflows and avoid submitting confidential queries to public instances.

Risk: Self-hosting guidance uses Docker images, Python packages, downloaded configuration, and persistent services.

Mitigation: Review and pin images, packages, and downloaded configs before deployment, and explicitly stop or remove Docker/systemd services when they are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/simoncatbot/skills/web-search-searxng)
- [SearXNG Self-Hosting Guide](artifact/SETUP.md)
- [SearXNG Public Instances](https://searx.space/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON search results, plus Markdown setup guidance and YAML configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result count, category, engine, time range, language, safesearch, timeout, and SearXNG base URL are configurable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
