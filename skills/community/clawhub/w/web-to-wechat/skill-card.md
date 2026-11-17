## Description:

Scrapes web article content, helps an agent clean and reformat it for WeChat Official Accounts, generates or compresses cover imagery, and prepares publication to the WeChat draft box.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lutongsuo](https://clawhub.ai/user/lutongsuo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a supplied web URL into a WeChat Official Account draft with cleaned article Markdown, WeChat-compatible HTML, source attribution, and compressed cover media. It is intended for workflows that need reviewable publication drafts rather than only extraction guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create WeChat Official Account drafts and may affect an account-connected publishing workflow.

Mitigation: Require explicit final user approval before creating any WeChat draft and review the generated article, source attribution, cover image, and target account before publishing.

Risk: The skill fetches arbitrary user-provided URLs.

Mitigation: Run it in an isolated environment and avoid scraping internal, private, sensitive, or untrusted URLs.

Risk: The skill depends on companion WeChat skills and Python packages that may be installed automatically.

Mitigation: Pin and preinstall dependencies, audit the companion skills before use, and review package installation behavior before running scripts.

Risk: WeChat AppSecret values could be exposed if placed into generated commands or logs.

Mitigation: Use environment variables or secure prompts for credentials and do not paste AppSecret values into command strings, transcripts, or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lutongsuo/skills/web-to-wechat)
- [Publisher profile](https://clawhub.ai/user/lutongsuo)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON scrape output, WeChat-compatible HTML, shell commands, and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create article files, cover image files, compressed JPEGs, and WeChat draft-box publishing commands that require user credentials and final approval.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
