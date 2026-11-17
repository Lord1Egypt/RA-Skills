## Description:

WeWe RSS Reader helps an agent retrieve full text from WeChat public-account article links through a locally deployed WeWe RSS REST API and use that text for reading comprehension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to read, summarize, or answer questions about WeChat public-account articles. The skill is intended for local WeWe RSS deployments that expose article, feed, subscription, refresh, health, and login endpoints on localhost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external local WeWe RSS service and deployment commands that may run Docker or Python code from a forked repository.

Mitigation: Review and pin the external repository before deployment, and run the service only in an environment where you can maintain and monitor it.

Risk: The documented AUTH_CODE is a shared example value and could allow unwanted access if reused.

Mitigation: Replace the documented AUTH_CODE with a unique secret before exposing or relying on the local service.

Risk: WeChat Reading login QR codes and confirmation URLs can authorize account access if shared in a group chat.

Mitigation: Send login artifacts only through a trusted private channel and avoid posting QR codes or confirmation URLs to shared group chats.

Risk: The service exposes local ports for the REST API and WeWe RSS UI.

Mitigation: Keep ports bound to localhost unless there is a reviewed network-access requirement.

## Reference(s):

- [Deployment guide](artifact/references/deployment.md)
- [WeWe RSS fork](https://github.com/AxelHu/wewe-rss)
- [ClawHub skill page](https://clawhub.ai/axelhu/skills/wewe-rss-reader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST API paths, curl examples, and plain-text article content returned from the local service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Article text may be truncated to the first 15000 characters by the local REST API. The skill expects a local service on port 4001 and a WeWe RSS UI on port 4000.]

## Skill Version(s):

1.2.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
