## Description:

Generate comprehensive SEO analysis reports from Google Search Console data with PDF export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgx-00](https://clawhub.ai/user/lgx-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO analysts, and site operators use this skill to fetch Google Search Console data, analyze search performance across one or more sites, and generate chart-rich PDF reports with recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Google service-account credentials for Search Console access.

Mitigation: Use only a Google-generated service-account key with restricted Search Console permissions and review credential handling before running.

Risk: The artifact writes local report data, charts, screenshots, scripts, and PDF outputs.

Mitigation: Run it in a private per-run working directory and choose an output directory that does not expose sensitive search analytics data.

Risk: Dependencies are installed and executed locally.

Mitigation: Install dependencies from reviewed, pinned versions in an isolated virtual environment.

Risk: OAuth token requests depend on the service-account token URI.

Mitigation: Prefer code that pins the OAuth token endpoint to Google's official URL.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lgx-00/skills/search-console-report)
- [Google OAuth Token Endpoint](https://oauth2.googleapis.com/token)
- [Google Search Console API Scope](https://www.googleapis.com/auth/webmasters.readonly)
- [Google Search Console API Library](https://console.cloud.google.com/apis/library/searchconsole.googleapis.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; generated artifacts include PDF, JSON, and PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Google service-account JSON key with restricted Search Console access and writes local report artifacts.]

## Skill Version(s):

1.1.1 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
