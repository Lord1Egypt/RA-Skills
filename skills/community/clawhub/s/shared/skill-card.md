## Description:

Provides a reusable Python cache utility for stock-trading skills, including A-share trading-time detection, cache loading and saving, cache expiration, and fallback behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georgetao730](https://clawhub.ai/user/georgetao730)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building Chinese A-share stock-trading agents or skills use this utility to decide when to fetch live data versus reuse local cached stock data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cache helper can create, overwrite, read, and clear cache.json in the caller-selected cache directory.

Mitigation: Configure a dedicated cache directory and review integrations so the helper cannot affect unrelated local files.

Risk: The A-share trading-time logic includes a 15:30 post-market window that may not match every data freshness requirement.

Mitigation: Confirm the post-market freshness policy before relying on cached data outside the regular trading window.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Python code snippets and concise integration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external Python dependencies; cache behavior depends on a caller-selected local cache directory and cache age setting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
