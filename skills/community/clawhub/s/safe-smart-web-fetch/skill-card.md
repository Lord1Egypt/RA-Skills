## Description:

Safe Smart Web Fetch retrieves web pages by using third-party cleaners for ordinary public pages while keeping URLs that appear sensitive, private, local, or non-HTTP on direct fetch only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zqh2333](https://clawhub.ai/user/zqh2333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch webpage content as Markdown-like text or JSON while reducing the chance that sensitive or private URLs are sent to third-party cleaning services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence says the safety checks are not strong enough for sensitive URLs or private-network fetching.

Mitigation: Review before installing in environments with access to private networks, cloud metadata, internal tools, or sensitive links.

Risk: Ordinary-looking public URLs may be sent to Jina Reader, markdown.new, or defuddle.md for cleaning.

Mitigation: Use the skill only with URLs that are acceptable to fetch from the agent host and acceptable to send to those cleaning services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zqh2333/skills/safe-smart-web-fetch)
- [Publisher profile](https://clawhub.ai/user/zqh2333)
- [Jina Reader endpoint](https://r.jina.ai/)
- [markdown.new](https://markdown.new)
- [defuddle.md](https://defuddle.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Plain text or JSON containing fetched content, source metadata, third-party usage status, blocked reason, and error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use third-party cleaning services for URLs classified as ordinary public pages; sensitive, private, local, or non-HTTP URLs are fetched directly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
