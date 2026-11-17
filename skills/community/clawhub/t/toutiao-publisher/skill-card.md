## Description:

Publish articles to Toutiao (Today's Headlines). Handles persistent authentication (login once) and session management. Opens browser for interactive publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guanyang](https://clawhub.ai/user/guanyang)

### License/Terms of Use:


## Use Case:

Developers and content operators use this skill to manage Toutiao login state and publish Markdown or text articles, optionally with a local cover image, through an interactive or automated browser workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content to a live Toutiao account using stored login sessions.

Mitigation: Review article content before execution, prefer visible non-headless runs, and use --dry-run until the intended publication flow is confirmed.

Risk: Browser session data is persisted locally under data/browser_state.

Mitigation: Keep the browser state private, avoid sharing generated state files, and clear saved sessions when publishing is complete.

Risk: Setup installs Python dependencies and Chrome for browser automation.

Mitigation: Run the skill in an isolated environment and review dependency installation before first use.

Risk: The skill can upload specified local files as article content or cover images.

Mitigation: Verify file paths and file contents before running automated publishing commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guanyang/skills/toutiao-publisher)
- [Toutiao publisher portal](https://mp.toutiao.com/)
- [Toutiao article publish page](https://mp.toutiao.com/profile_v4/graphic/publish)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Files, Guidance]

**Output Format:** [Terminal status output and browser-mediated publishing workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent browser session files and debug screenshots; successful runs can publish externally to a live Toutiao account.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
