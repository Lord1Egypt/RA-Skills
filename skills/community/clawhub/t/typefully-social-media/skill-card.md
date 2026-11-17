## Description:

Create, schedule, and manage social media posts via Typefully for Twitter/X, LinkedIn, Threads, Bluesky, and Mastodon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankdilo](https://clawhub.ai/user/frankdilo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to draft, schedule, publish, and manage Typefully social media content across connected accounts and platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Typefully API key that can affect real connected social media accounts.

Mitigation: Install it only in trusted agent environments, prefer interactive setup or carefully managed secret environment variables, and avoid exposing the API key in command history or shared project files.

Risk: Publishing or deleting social content can have immediate public or irreversible effects.

Mitigation: Review commands before execution, create drafts for review when intent is not explicit, and require clear confirmation before publishing or deleting content.

Risk: Changing the API base can redirect authenticated requests away from the normal Typefully API.

Mitigation: Avoid setting TYPEFULLY_API_BASE unless it is required for a trusted test environment.

## Reference(s):

- [Typefully API Documentation](https://typefully.com/docs/api)
- [Typefully](https://typefully.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, schedule, publish, update, delete, or inspect Typefully drafts and media through authenticated API-backed commands.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
