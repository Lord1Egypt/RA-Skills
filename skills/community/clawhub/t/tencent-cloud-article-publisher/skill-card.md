## Description:

Publishes Markdown or plain text articles to Tencent Cloud Developer Community using a user-provided Tencent Cloud session cookie.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanminjie](https://clawhub.ai/user/seanminjie)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content teams use this skill to publish article drafts to Tencent Cloud Developer Community through an authenticated API call. It collects a title, article body, and session cookie, then returns publish status and the article link when successful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a live Tencent Cloud browser session cookie.

Mitigation: Use a secure prompt or secret store for the cookie, avoid command-line arguments for secrets, and revoke or refresh any cookie that may have been exposed.

Risk: The skill can publish articles publicly under the user's Tencent Cloud account.

Mitigation: Require manual review and explicit confirmation of the title, body, destination account, and publish action before each API call.

Risk: A stale or invalid cookie can cause publishing failure.

Mitigation: Ask the user to refresh the Tencent Cloud session cookie when authentication fails or the cookie expires.

## Reference(s):

- [Tencent Cloud Developer Community](https://cloud.tencent.com/developer)
- [Tencent Cloud Article Publish API Endpoint](https://cloud.tencent.com/developer/api/article/addArticle)
- [ClawHub Skill Listing](https://clawhub.ai/seanminjie/skills/tencent-cloud-article-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text guidance with command examples and JSON-like publish status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success or failure status, article ID, and article URL when publishing succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
