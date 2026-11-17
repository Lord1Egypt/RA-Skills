## Description:

Fetches category-specific news from TianAPI across channels such as finance, sports, entertainment, technology, and domestic or international news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve and present recent TianAPI category news by channel ID, with optional result count, keyword, and page controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The TianAPI API key may be exposed through command-line arguments, logs, shell history, or an uncontrolled local .env file.

Mitigation: Use a protected environment variable for the API key, avoid passing it on the command line, keep any .env file permissioned and ignored by version control, and rotate keys that may have appeared in examples or logs.

## Reference(s):

- [TianAPI Category News API](https://www.tianapi.com/apiview/51)
- [TianAPI All News API Endpoint](https://apis.tianapi.com/allnews/index)
- [ClawHub Skill Page](https://clawhub.ai/workxin/skills/tianapi-allnews-news)
- [ClawHub Publisher Profile](https://clawhub.ai/user/workxin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON from a Python CLI, typically summarized by the agent in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TianAPI API key and a category channel ID; result count is capped at 50 by the script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
