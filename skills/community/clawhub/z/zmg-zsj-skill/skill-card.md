## Description:

Provides Z-Sight APP capabilities for finding live streams, variety shows, short videos, trending topics, opening app pages, publishing content, reading messages, and managing user content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[295522894](https://clawhub.ai/user/295522894)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search and browse Z-Sight APP media, navigate to app pages, publish authorized posts or short videos, review messages, and manage user-owned content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer authorization may be exposed if the runtime MCP endpoint uses plaintext HTTP.

Mitigation: Install only after the endpoint is corrected to HTTPS on the documented domain and the publisher is trusted.

Risk: Publishing and deletion tools can create or remove user-visible content.

Mitigation: Confirm exact post, video, or article details with the user before calling publishing or deletion actions.

Risk: Authorized calls depend on a bearer token issued through the Z-Sight APP flow.

Mitigation: Use the documented authorization flow and stop further API calls when authorization expires until the user reauthorizes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/295522894/skills/zmg-zsj-skill)
- [Publisher profile](https://clawhub.ai/user/295522894)
- [Live response examples](artifact/references/live.json)
- [Search response examples](artifact/references/search.json)
- [Short video response examples](artifact/references/short_video.json)
- [Variety response examples](artifact/references/variety.json)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown or text responses with JSON-backed tool results and app deep links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some actions require bearer-token authorization; publishing and deletion operations can modify user content.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
