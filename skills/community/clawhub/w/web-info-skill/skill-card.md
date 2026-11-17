## Description:

Extract and display useful information from web pages including title, meta description, headers, and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sangjie123](https://clawhub.ai/user/sangjie123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to inspect web pages reachable from the agent environment and summarize titles, descriptions, headers, links, images, and word counts from static HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound HTTP(S) requests to arbitrary URLs from the agent host.

Mitigation: Use egress restrictions, avoid untrusted URLs, and require private or internal destination blocking before broad deployment.

Risk: The artifact claims public-only fetching and robots.txt protections that security evidence says are not implemented.

Mitigation: Document the actual fetch behavior and add redirect, robots.txt, and destination validation before relying on those protections.

Risk: The shell script emits JSON from page text without a real JSON serializer.

Mitigation: Validate or serialize extracted values with a JSON-aware tool before downstream automation consumes the output.

## Reference(s):

- [Web info skill on ClawHub](https://clawhub.ai/sangjie123/skills/web-info-skill)
- [OpenClaw homepage](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Plain text summaries or JSON objects emitted by a shell command.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; fetches static HTML and does not execute JavaScript.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter, script VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
