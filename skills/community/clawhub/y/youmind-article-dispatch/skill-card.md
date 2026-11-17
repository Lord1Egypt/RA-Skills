## Description:

Dispatches one content topic across multiple publishing platforms by creating a shared brief, adapting it per platform, and aggregating draft or publishing results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindy-youmind](https://clawhub.ai/user/mindy-youmind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and publishing teams use this skill to turn one topic into platform-adapted content for Dev.to, Hashnode, WordPress, Tumblr, Ghost, Beehiiv, Kit, X/Twitter, WeChat, and Qiita. It is most useful when a user wants cross-posting, all-platform publishing, or a coordinated publishing summary without manually invoking each platform skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a shared YouMind API key and can coordinate drafts or posts across connected publishing accounts.

Mitigation: Use the least-privileged YouMind key available, rotate it regularly, keep it out of project files, and prefer draft mode unless the user explicitly requests publishing.

Risk: The skill keeps author profile, dispatch roster, draft, and learning-history data under ~/.youmind/.

Mitigation: Review local profile and learning files before use with sensitive content, remove data that should not persist, and confirm retention expectations with the user.

Risk: The skill requests broad node and npm command authority.

Mitigation: Review or narrow allowed tool permissions before deployment and inspect generated shell commands before execution.

Risk: The skill may analyze historical articles or engagement data to learn an author profile.

Mitigation: Run profile bootstrapping and learning only with user consent, and summarize what data was analyzed before saving profile updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindy-youmind/skills/youmind-article-dispatch)
- [YouMind API Key Settings](https://youmind.com/settings/api-keys?utm_source=youmind-article-dispatch)
- [YouMind Connector Settings](https://youmind.com/settings/connector?utm_source=youmind-article-dispatch)
- [Content Brief Format](references/content-brief-format.md)
- [Platform Registry](references/platform-registry.md)
- [Author Profile Specification](references/author-profile-spec.md)
- [Content Adaptation Matrix](references/content-adaptation-matrix.md)
- [Dispatch Protocol](references/dispatch-protocol.md)
- [Profile Learning](references/profile-learning.md)
- [Dispatch Integration Protocol](shared/DISPATCH_CONTRACT.md)
- [YouMind Home Directory](shared/YOUMIND_HOME.md)
- [Publishing Guidelines](shared/PUBLISHING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with YAML content briefs, platform-specific article drafts or posts, result tables, configuration files, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local YouMind configuration, dispatch roster, author profile, article draft, and learning history files under ~/.youmind/.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
