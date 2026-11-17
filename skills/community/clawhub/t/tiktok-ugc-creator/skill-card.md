## Description:

Hire TikTok users to create authentic user-generated content (UGC), testimonials, and brand storytelling videos that build trust and drive engagement through genuine customer voices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realroc](https://clawhub.ai/user/realroc)

### License/Terms of Use:


## Use Case:

External marketing teams and agents use this skill to find TikTok UGC creators, create paid campaign tasks, review submissions, and manage content-rights choices for authentic product testimonials and brand storytelling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through paid creator workflows, including campaign creation, content approval, and creator ratings.

Mitigation: Require explicit user approval before creating paid tasks, approving submissions, rating creators, or making commitments on campaign terms.

Risk: The skill uses PingHuman API bearer tokens in example requests.

Mitigation: Store API tokens in a secret manager or environment variable and constrain the agent's API permissions before use.

Risk: The artifact recommends installation from a mutable remote skill URL.

Mitigation: Prefer a pinned or locally reviewed copy of the skill before enabling it for an agent.

Risk: Product-shipping workflows may involve collecting creator shipping addresses.

Mitigation: Collect shipping addresses only with consent and documented secure handling, retention, and deletion practices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realroc/skills/tiktok-ugc-creator)
- [Publisher profile](https://clawhub.ai/user/realroc)
- [PingHuman homepage](https://www.pinghuman.ai)
- [PingHuman API base](https://www.pinghuman.ai/api/v1)
- [PingHuman skill file](https://www.pinghuman.ai/skills/tiktok-ugc-creator/skill.md)
- [PingHuman registration guide](https://www.pinghuman.ai/skill.md#getting-started-agent-registration)
- [UGC Creator Dashboard](https://www.pinghuman.ai/dashboard/tiktok-ugc)
- [UGC Best Practices Guide](https://www.pinghuman.ai/docs/ugc-guide)
- [Content Rights Guide](https://www.pinghuman.ai/docs/content-licensing)
- [TikTok UGC Trends](https://www.tiktok.com/business/en/blog/ugc-trends)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example API requests for creator search, task creation, submission review, approval, and rating.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
