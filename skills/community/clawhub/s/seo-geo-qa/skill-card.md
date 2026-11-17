## Description:

Check blog posts and articles before publishing by finding broken links, weak sources, missing SEO elements, and citation problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justinbao19](https://clawhub.ai/user/justinbao19)

### License/Terms of Use:

MIT-0

## Use Case:

Content, SEO, and editorial teams use this skill to audit draft or published articles for link health, source quality, SEO metadata, SERP coverage, and publish-readiness. Agents can run the bundled checks and return markdown and JSON reports with PASS, FAIL, or REVISE outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact extracted or supplied URLs and share SEO keywords or full URLs with external services such as DuckDuckGo and r.jina.ai.

Mitigation: Run it only on content and URLs approved for external network access, or disable Jina with --no-jina and use a network-restricted sandbox or URL allowlist for sensitive reviews.

Risk: Confidential drafts, preview links, signed URLs, intranet URLs, localhost/private-network addresses, or cloud metadata paths could be exposed during automated checks.

Mitigation: Avoid using those inputs unless private-address blocking, URL allowlisting, and network egress controls are in place.

## Reference(s):

- [Configuration](references/configuration.md)
- [Example QA Report](references/example-report.md)
- [Source Tiers](references/source-tiers.md)
- [Verdict Rules](references/verdict-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/justinbao19/skills/seo-geo-qa)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON reports with shell command examples and editorial guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Timestamped reports are written to a qa-reports directory by default; JSON output is available for automation.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
