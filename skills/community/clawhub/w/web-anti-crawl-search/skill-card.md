## Description:

Searches current web content across multiple search engines with headless browser scripts and returns result titles, links, snippets, and source labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlutwuwei](https://clawhub.ai/user/dlutwuwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run live searches for recent news, market information, and other time-sensitive queries. It can compare results across supported search engines and fall back when an engine is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Headless browser automation loads remote pages while Chromium sandboxing is disabled.

Mitigation: Run the skill only in an isolated environment and prefer removing Chromium no-sandbox flags before deployment.

Risk: Stealth browser automation may bypass anti-crawl controls and can raise policy or terms-of-use concerns.

Mitigation: Review target engine terms and remove the stealth plugin unless its use is explicitly approved.

Risk: Search terms may be sent to third-party search engines and remote pages.

Mitigation: Avoid sensitive, confidential, or regulated search terms.

Risk: Dependencies and documented engine support may need release review before installation.

Mitigation: Regenerate dependencies from an approved registry with pinned versions and align the documented engine list with the scripts.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON search-result lists with titles, links, snippets, and source labels.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and a headless Chromium runtime; result quality depends on search engine availability and page markup.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
