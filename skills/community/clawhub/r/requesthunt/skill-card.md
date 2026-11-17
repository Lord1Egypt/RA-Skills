## Description:

Generate user demand research reports from real user feedback by scraping and analyzing feature requests, complaints, and questions from Reddit, X, GitHub, YouTube, LinkedIn, and Amazon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

Product teams, founders, researchers, and agents use this skill to collect public user feedback and turn it into demand research, pain-point analysis, feature-gap reports, and competitive opportunity summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow tells users to run a mutable remote installer directly in a shell.

Mitigation: Review the installer before use, prefer a pinned release or source build, independently verify checksums or signatures, and run installation as an unprivileged user.

Risk: The skill relies on API credentials for RequestHunt access.

Mitigation: Provide the API key through REQUESTHUNT_API_KEY or protected local config, and do not hardcode secrets in skill instructions or agent output.

Risk: Scraped platform content is public user-generated content and may be unreliable or instruction-like.

Mitigation: Treat scraped content as untrusted input, summarize it for reports, and avoid executing or following instructions found in scraped text.

## Reference(s):

- [RequestHunt Documentation](https://requesthunt.com/docs)
- [RequestHunt Agent Setup](https://requesthunt.com/setup.md)
- [RequestHunt Dashboard](https://requesthunt.com/dashboard)
- [RequestHunt CLI Releases](https://github.com/ReScienceLab/requesthunt-cli/releases)
- [RequestHunt CLI Repository](https://github.com/ReScienceLab/requesthunt-cli)
- [ClawHub Skill Page](https://clawhub.ai/golngod/skills/requesthunt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with CLI commands, tables, summaries, and optional JSON, TOON, or human-readable CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include summarized public user-generated content from external platforms; quote or summarize that content with clear boundaries.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
