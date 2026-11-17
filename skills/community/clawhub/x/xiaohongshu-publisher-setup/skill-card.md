## Description:

Deploys a two-agent Xiaohongshu publishing team for XHS formatting, browser-assisted publishing, and post data review, triggered with /xiaohongshu-publisher-setup after content-creation is installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[little-ke](https://clawhub.ai/user/little-ke)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to install a Xiaohongshu-focused OpenClaw team that prepares platform-style content packages, registers publishing agents, and supports browser-assisted posting. The workflow is intended for accounts that can provide their own Xiaohongshu login session and review content before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a reusable Xiaohongshu browser session at ~/.openclaw/workspace-xiaohongshu-publisher/.session/state.json.

Mitigation: Treat the session file like a credential: keep it local, restrict access, do not sync or share it, and re-login if exposure is suspected.

Risk: The installer deploys local workspace files and registers OpenClaw agents.

Mitigation: Review the setup script before running it and install only in the intended OpenClaw workspace.

Risk: Browser automation depends on Playwright and Xiaohongshu page behavior, which may change or fail during publishing.

Mitigation: Use pinned Playwright dependencies where possible and keep the documented human confirmation step before final publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/little-ke/skills/xiaohongshu-publisher-setup)
- [Publisher profile](https://clawhub.ai/user/little-ke)
- [Xiaohongshu](https://www.xiaohongshu.com)
- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands, JSON examples, and deployed Node.js scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw, the content-creation team, node, npm, Playwright with Chromium, and a Xiaohongshu account login session.]

## Skill Version(s):

1.0.0 (source: evidence.release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
