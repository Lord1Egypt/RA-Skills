## Description:

Video pusher helps agents manage publishing account groups, preserve login sessions, and prepare posts for Douyin, Xiaohongshu, WeChat Channels, Threads, and Instagram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samcheng0717](https://clawhub.ai/user/samcheng0717)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to route social publishing requests, manage platform login profiles, and prepare multi-platform video, image, or text posts for manual final submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores logged-in browser profiles for social accounts on disk.

Mitigation: Use a dedicated automation profile, keep profile data out of shared repositories and archives, and avoid installing unless local session storage is acceptable.

Risk: Profile cleanup and remove operations can delete stored sessions and the evidence notes weak path containment safeguards.

Mitigation: Review account group names and target platforms before delete or remove actions, and keep recoverable login methods available.

Risk: The security verdict is suspicious due to session storage and unsafe profile-management behavior.

Mitigation: Review the skill before deployment, restrict use to trusted workspaces, and follow the security guidance in the release evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samcheng0717/skills/video-pusher)
- [Publisher profile](https://clawhub.ai/user/samcheng0717)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and Chromium browser automation; publishing scripts keep the final publish or share action under user control.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
