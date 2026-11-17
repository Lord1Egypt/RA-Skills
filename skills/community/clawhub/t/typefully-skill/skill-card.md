## Description:

Create, schedule, list, edit, and delete drafts on Typefully, including single tweets, threads, and multi-platform posts for X, LinkedIn, Threads, Bluesky, and Mastodon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chapati23](https://clawhub.ai/user/chapati23)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and social media operators use this skill to let an agent manage Typefully drafts, threads, schedules, and multi-platform social posts from shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, schedule, publish, edit, and delete social content through Typefully.

Mitigation: Install only with a Typefully account and API key that the operator is comfortable using for those actions, and review publish or delete commands before execution.

Risk: Scheduling values can cause immediate publishing when set to 'now' and evidence reports a scheduling input flaw.

Mitigation: Avoid schedule values copied from untrusted text, use explicit reviewed timestamps or next-free-slot, and prefer a fixed version that fully validates and JSON-encodes schedule values.

Risk: Deleting drafts is destructive.

Mitigation: Require operator confirmation before running delete-draft and verify the draft ID with get-draft or list-drafts first.

## Reference(s):

- [Typefully](https://typefully.com)
- [Typefully API v2 endpoint](https://api.typefully.com/v2)
- [Unix password store](https://www.passwordstore.org/)
- [ClawHub skill page](https://clawhub.ai/chapati23/skills/typefully-skill)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown guidance with bash commands; command output is Typefully API JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TYPEFULLY_API_KEY and optionally TYPEFULLY_SOCIAL_SET_ID; commands can create, schedule, publish, edit, list, and delete social drafts.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
