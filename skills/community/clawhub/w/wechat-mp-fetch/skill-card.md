## Description:

Wechat Mp Fetch extracts titles, body text, and final URLs from accessible WeChat Official Account articles on mp.weixin.qq.com using Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[write31bug](https://clawhub.ai/user/write31bug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content workflows use this skill to fetch text and metadata from accessible WeChat Official Account articles for archival, note-taking, research, and writing reference. Users should only archive or repurpose fetched content where they have permission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weak URL checks can allow a supplied link to make the local browser visit unintended sites or private network addresses.

Mitigation: Use only trusted WeChat article URLs, avoid running the skill in environments with sensitive network access, and add strict host and redirect validation before broader deployment.

Risk: Fetched article content may be subject to access, copyright, or reuse restrictions.

Mitigation: Archive or repurpose fetched content only where the user has permission and keep downstream use aligned with the article source terms.

Risk: The skill depends on Playwright and command-line package installation.

Mitigation: Install pinned dependencies from a trusted registry and review dependency updates before use in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/write31bug/skills/wechat-mp-fetch)
- [Project homepage](https://github.com/write31bug/wechat-mp-fetch)
- [npm package](https://www.npmjs.com/package/wechat-mp-fetch)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON or Markdown article extraction output from a command-line workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied mp.weixin.qq.com article URL; supports timeout, debug, and output format options.]

## Skill Version(s):

1.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
