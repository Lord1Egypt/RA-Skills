## Description:

Fetches readable web page body content with Scrapling and html2text, including WeChat article cleanup, Markdown output, batch fetches, selector overrides, and support for many hard-to-fetch modern pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jllyzzd2023](https://clawhub.ai/user/jllyzzd2023)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to retrieve article bodies, news, blog posts, announcements, and WeChat pages as Markdown for downstream summarization, archiving, translation, or analysis. It is useful when ordinary fetch tools return unstable, noisy, or incomplete content from modern pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches arbitrary user-supplied URLs, which can expose internal, tokenized, or sensitive links if used without restrictions.

Mitigation: Use it only with public URLs, avoid internal or credential-bearing links, and run it in a network-restricted environment.

Risk: Dependencies are installed ad hoc when missing, which can introduce supply-chain drift.

Mitigation: Pin dependencies or use a reviewed lock file before broad deployment.

Risk: Fetched page content can be noisy, incomplete, or adversarial because it comes from external websites.

Mitigation: Review fetched output before relying on it for summaries, decisions, or downstream automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jllyzzd2023/skills/scrapling-web-fetch)
- [Release notes 1.0.1](artifact/references/release-1.0.1.md)
- [Usage](artifact/references/usage.md)
- [Selector strategy](artifact/references/selectors.md)
- [Site selector overrides example](artifact/references/site-overrides.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown by default, or JSON when requested with --json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output can be truncated by max_chars, includes selector/title/quality diagnostics on stderr in text mode, and supports batch URL fetches.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
