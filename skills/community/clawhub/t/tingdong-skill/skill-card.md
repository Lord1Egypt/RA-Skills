## Description:

Converts user-provided articles, links, or plain text into personalized podcast audio with content analysis, selectable podcast styles, and audio output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentforge-cyber](https://clawhub.ai/user/agentforge-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn URLs or pasted text into short-form podcast audio for listening, summarization, or deeper review. It is suited to user-initiated conversion of public articles, WeChat posts, Zhihu content, general web pages, or user-provided text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text, links, and generated audio metadata are sent to a remote service over unencrypted HTTP.

Mitigation: Use only non-sensitive content unless the service is moved behind HTTPS and reviewed for privacy, retention, and access controls.

Risk: The skill can fetch third-party web content, including sites with anti-scraping controls, paywalls, access restrictions, robots rules, or copyright constraints.

Mitigation: Limit use to user-authorized content and verify that fetching and conversion comply with the source site's terms and applicable rights.

Risk: The security verdict is suspicious due to weak privacy and scraping safeguards.

Mitigation: Review the implementation and remote service behavior before installation, and avoid submitting confidential, internal, paywalled, or sensitive copyrighted material.

## Reference(s):

- [TingDong backend API documentation](artifact/references/api_docs.md)
- [Content source handling strategy](artifact/references/content_sources.md)
- [ClawHub skill release page](https://clawhub.ai/agentforge-cyber/skills/tingdong-skill)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with JSON API responses and audio file or audio URL results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio is returned with title, duration, source attribution when available, and task status metadata.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
