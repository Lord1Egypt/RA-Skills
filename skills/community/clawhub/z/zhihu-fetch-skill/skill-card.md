## Description:

Fetches Zhihu collection lists, articles, answers, questions, user posts, and history into local JSON and Markdown, with Playwright fallback, cookie persistence, image localization, resumable batch runs, and optional Obsidian export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handsomestwei](https://clawhub.ai/user/handsomestwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to collect Zhihu content, resume interrupted crawls, save article bodies and images as Markdown, and optionally organize mirrored content and notes inside an Obsidian vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Zhihu session cookies and can reuse them while fetching pages and images.

Mitigation: Use a dedicated workspace, restrict access to zhihu_cookies.json, and delete or rotate cookies when the run is complete.

Risk: Untrusted batch JSON or fetched article content may drive authenticated requests or introduce unsafe Markdown content.

Mitigation: Run only trusted batch lists, review fetched content before importing it into a knowledge base, and avoid sensitive logged-in sessions for untrusted inputs.

Risk: Obsidian export commands write into the selected vault and may update or delete source mirror files during import workflows.

Mitigation: Back up the vault, test with a small batch first, and verify the target vault path before running export commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handsomestwei/skills/zhihu-fetch-skill)
- [Publisher profile](https://clawhub.ai/user/handsomestwei)
- [Python](https://www.python.org/)
- [Playwright](https://playwright.dev/)
- [AgentSkills](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts include JSON lists, Markdown articles, local image files, progress files, run summaries, and Obsidian notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local workspace state for cookies, browser data, progress checkpoints, crawl limits, URL indexes, and run summaries.]

## Skill Version(s):

2.2.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
