## Description:

Adaptive web scraping framework with anti-bot bypass and spider crawling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zendenho7](https://clawhub.ai/user/zendenho7)

### License/Terms of Use:

BSD-3-Clause

## Use Case:

Developers and agents use Scrapling to fetch, parse, and crawl permitted public websites for research, content extraction, brand data gathering, and structured data collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes API reverse-engineering and anti-bot or Cloudflare bypass guidance.

Mitigation: Use the skill only on public sites or systems where scraping is permitted, and avoid the reverse-engineering and stealth bypass sections unless they have been specifically reviewed and authorized.

Risk: The run script accepts URLs, selectors, and spider files that can drive external requests or execute a local spider script.

Mitigation: Do not pass untrusted URLs, selectors, or spider files to run.sh; review inputs and run in an isolated environment.

Risk: The run script may install dependencies dynamically and the security guidance recommends pinned dependencies.

Mitigation: Prefer a reviewed environment with pinned Scrapling dependencies before running the script.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zendenho7/skills/scrapling)
- [Scrapling Documentation](https://scrapling.readthedocs.io)
- [Scrapling Repository](https://github.com/D4Vinci/Scrapling)
- [free-solscan-api Repository](https://github.com/paoloanzn/free-solscan-api)
- [API Reverse Engineering Methodology Post](https://x.com/paoloanzn/status/2026361234032046319)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scraped page snippets, structured dictionaries, URLs, or local install and run commands depending on the selected workflow.]

## Skill Version(s):

1.0.8 (source: frontmatter, server release metadata, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
