## Description:

Publish and manage articles on Tilda website builder via browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vspandexe](https://clawhub.ai/user/vspandexe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to create, edit, and publish Tilda articles through Playwright browser automation when a write API is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Tilda account credentials and reusable browser session data in the workspace.

Mitigation: Use a dedicated low-privilege Tilda account where possible, protect or delete .env and tilda-session.json, and ensure those files are not committed or shared.

Risk: The skill can make live changes to a Tilda site, including creating, editing, and publishing pages.

Mitigation: Require explicit confirmation of the target project, page, and publish or edit action before running it on a live site.

Risk: Browser automation can fail or act on the wrong UI element when Tilda changes its interface.

Mitigation: Review generated actions before execution, inspect debug screenshots and selector-recovery files when self-healing occurs, and stop for manual review if selector recovery fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vspandexe/skills/tilda-publisher)
- [Publisher profile](https://clawhub.ai/user/vspandexe)
- [Tilda login](https://tilda.cc/login/)
- [Tilda projects](https://tilda.cc/projects/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return live published URLs and may create local credential, session, debug, screenshot, or selector-recovery files during execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
