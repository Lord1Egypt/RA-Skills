## Description:

Saves article URLs to Readwise Reader and uses an LLM to apply content-based tags, with specialized handling for WeChat Official Account articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zz123-awef](https://clawhub.ai/user/zz123-awef)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save one or more article links into Readwise Reader and receive consistent content-based tags for later retrieval. It is especially intended for article links that Readwise may not parse reliably on its own, such as WeChat Official Account articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch and send saved URLs, article metadata, and article text to Readwise and the configured LLM provider.

Mitigation: Use it only for links intended for saving, avoid private or sensitive URLs, and confirm that the chosen LLM provider is acceptable for the article content.

Risk: The security guidance flags unsafe command and URL handling.

Mitigation: Require explicit save intent, validate URLs before execution, avoid localhost or intranet targets, and pass arguments safely when invoking bundled scripts.

Risk: Automatic processing can act on pasted links without confirmation.

Mitigation: Configure the agent to ask before processing sensitive contexts or disable automatic URL handling where accidental saves would be unacceptable.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zz123-awef/skills/readwise-article-saver)
- [Publisher profile](https://clawhub.ai/user/zz123-awef)
- [OpenClaw documentation](https://docs.openclaw.ai/)
- [Readwise Reader](https://readwise.io/read)
- [Readwise Save API endpoint](https://readwise.io/api/v3/save/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON script results and concise Markdown or plain-text status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires READWISE_TOKEN and OPENROUTER_API_KEY. Article text previews may include up to about 8000 characters for tagging.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
