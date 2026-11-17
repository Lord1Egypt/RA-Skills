## Description:

Post tweets, threads, replies, and quote-tweets to X (Twitter) via API v2 with OAuth 1.0a.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3rdbrain](https://clawhub.ai/user/3rdbrain)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to publish and manage X (Twitter) content for an authenticated account, including tweets, threads, replies, quote-tweets, likes, deletions, and recent timeline checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth credentials allow actions on a live X account, including posting, replying, quote-tweeting, liking, deleting tweets, and reading recent account tweets.

Mitigation: Install only when those account permissions are acceptable, and require explicit user approval before public engagement or deletion actions.

Risk: The delete action can remove live account content without a documented confirmation guard.

Mitigation: Use an external confirmation workflow before running delete commands.

Risk: Documented scheduling commands are not supported by the implementation evidence.

Mitigation: Do not rely on scheduling commands unless the implementation is updated and revalidated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/3rdbrain/skills/x-leads-api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with bash command examples; runtime command output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, and X_ACCESS_SECRET environment variables.]

## Skill Version(s):

1.0.0 (source: server release evidence, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
