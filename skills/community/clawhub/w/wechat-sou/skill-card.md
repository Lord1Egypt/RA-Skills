## Description:

Search public WeChat articles and videos by keyword and return structured results; image search, full-text extraction, and account login are not supported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT

## Use Case:

External users and analysts use this skill to search public WeChat articles and videos for topic discovery, trend monitoring, and competitor analysis. Results are intended for individual or team internal analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benign security verdict has medium confidence because analysis covered 60% of components and ten files were partly inspected.

Mitigation: Review the bundled files before installation and reassess if fuller security analysis becomes available.

Risk: Search keywords are sent to the third-party API, and results are written to the skill logs directory.

Mitigation: Use non-sensitive queries and restrict access to local result logs; keep use to public WeChat data for internal analysis.

## Reference(s):

- [Search options and examples](artifact/references/options.md)
- [GuaiKei API support](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON search results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GuaiKei API token. Search terms are sent to the API provider, and results are saved in the skill logs directory; use only public WeChat data for internal analysis.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata, SKILL.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
