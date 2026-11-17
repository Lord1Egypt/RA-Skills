## Description:

Fetches the title and body text for a single Zhihu Zhuanlan article URL and returns structured article metadata and content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woai36d](https://clawhub.ai/user/woai36d)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch and save the title, plain-text body, word count, source URL, fetch method, and metadata for individual Zhihu Zhuanlan articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weak URL validation can send saved Zhihu session cookies to a non-Zhihu URL.

Mitigation: Require the URL to match exactly https://zhuanlan.zhihu.com/p/<id> before any request that attaches cookies.

Risk: Real Zhihu cookies stored in config/cookie.json should be treated like account credentials.

Mitigation: Keep real cookies out of shared folders and source control, run the skill in an isolated environment, and rotate cookies if they may have been exposed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/woai36d/skills/zhihu-article-fetcher)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration instructions]

**Output Format:** [JSON text or a JSON file containing metadata, title, URL, extracted content, word count, and fetch method]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use configured Zhihu cookies, a browser profile, or simulated browser headers depending on availability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
