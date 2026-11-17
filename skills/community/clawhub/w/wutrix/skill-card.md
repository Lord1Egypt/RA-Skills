## Description:

Wutrix connects an OpenClaw agent to a wutrix film-preproduction workspace so it can capture ideas and query projects, scenes, characters, and story-world material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwneox](https://clawhub.ai/user/kwneox)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to connect an agent to a configured wutrix server for screenplay development workflows, including saving inspiration and retrieving project, scene, character, and vault search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may cause the agent to send matched user text to the configured wutrix server.

Mitigation: Install only in contexts where wutrix capture and search are expected, and avoid enabling it for unrelated private conversations.

Risk: The skill depends on a configured server URL and API key for all save and query operations.

Mitigation: Use a trusted HTTPS wutrix URL and a narrowly scoped, revocable API key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kwneox/skills/wutrix)
- [wutrix project homepage](https://github.com/kwneox/inspirestudio)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [JSON from helper scripts and concise Chinese text or Markdown summaries from the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires INSPIRESTUDIO_URL and INSPIRESTUDIO_API_KEY; helper scripts make HTTP requests to the configured wutrix server with 10 second timeouts.]

## Skill Version(s):

1.5.2 (source: server release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
