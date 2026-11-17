## Description:

Reads WeChat Official Account article links and extracts the article title, account name, and body text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnwarden](https://clawhub.ai/user/cnwarden)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to fetch readable text from trusted mp.weixin.qq.com articles for summarization, review, or translation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can fetch arbitrary URLs and follow redirects, which could expose local or private network services if misused.

Mitigation: Use only trusted WeChat article URLs, and prefer a version that enforces an HTTPS mp.weixin.qq.com allowlist and validates redirect destinations.

Risk: Some WeChat articles may require verification or may not parse successfully.

Mitigation: Treat verification and parsing failures as expected errors, and do not attempt to bypass access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cnwarden/skills/weixin-reader-plus)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text with title, account name, article body, or an error message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return an error when an article requires verification or parsing fails.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
