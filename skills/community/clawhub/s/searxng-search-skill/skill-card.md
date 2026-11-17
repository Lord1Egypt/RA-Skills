## Description:

Perform privacy-focused metasearch through local or remote SearXNG instances with retries, timeouts, category filters, time filters, engine-specific queries, autocomplete, health checks, and result export helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elmaslouhymouaad](https://clawhub.ai/user/elmaslouhymouaad)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to query configured SearXNG instances, collect web, image, video, news, science, file, and social-media search results, and return either raw dictionaries or structured result objects for downstream research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unaudited package or relying on unresolved package ownership can introduce supply-chain exposure.

Mitigation: Review the release before installing and prefer installation from the audited local source until publisher identity and package ownership are verified.

Risk: Search queries sent to public or untrusted SearXNG instances may expose sensitive research intent or user data.

Mitigation: Use a self-hosted or explicitly trusted SearXNG instance and avoid public fallback instances for sensitive searches.

Risk: Disabling TLS certificate verification can weaken transport security outside local testing.

Mitigation: Keep SSL verification enabled except for strictly local development or test instances.

Risk: CSV exports may carry spreadsheet formula-execution risk when opened in spreadsheet software.

Mitigation: Avoid opening exported CSV files in spreadsheet software with formula execution enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elmaslouhymouaad/skills/searxng-search-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; runtime helpers return JSON-like dictionaries, structured Python objects, text responses, and optional JSON or CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search behavior depends on the configured SearXNG instance, enabled engines, timeout, retry, safe-search, category, language, and output-format settings.]

## Skill Version(s):

0.1.1 (source: server release evidence; artifact package files report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
