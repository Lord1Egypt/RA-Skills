## Description: <br>
SeedDrop monitors Bilibili, Tieba, Zhihu, and Xiaohongshu discussions, scores relevant posts, and helps an agent draft human-reviewed community replies that use SocialVault-managed credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2019-02-18](https://clawhub.ai/user/2019-02-18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams, small businesses, and indie developers use this skill to find relevant social discussions, evaluate whether a reply is appropriate, and prepare helpful reply drafts for manual approval before posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses live social-platform sessions and cookies for monitoring and replies. <br>
Mitigation: Use SocialVault-managed credentials, prefer dedicated accounts, and avoid sharing cookies outside the intended credential flow. <br>
Risk: Browser/API automation can interact with public social platforms and may conflict with platform expectations or account limits. <br>
Mitigation: Keep manual approval enabled, respect platform rate limits, and avoid browser fallback or posting actions unless the target and content are explicitly approved. <br>
Risk: Generated replies may be perceived as undisclosed or overly promotional engagement. <br>
Mitigation: Review every draft for honest disclosure, useful content, and compliance with the skill's limits on brand mentions, links, and marketing claims. <br>


## Reference(s): <br>
- [SeedDrop ClawHub Page](https://clawhub.ai/2019-02-18/seed-drop) <br>
- [Safety Rules](references/safety-rules.md) <br>
- [Scoring Criteria](references/scoring-criteria.md) <br>
- [Platform Terms Notes](references/platform-tos-notes.md) <br>
- [Quickstart Guide](guides/quickstart.md) <br>
- [Brand Profile Setup](guides/brand-profile-setup.md) <br>
- [Adapter Development Guide](guides/adapter-development.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, reply drafts, shell commands, and JSONL monitoring or scoring records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SocialVault-managed credentials and manual approval for replies.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; bundled package/frontmatter report 3.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
