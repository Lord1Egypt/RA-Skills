## Description:

Redline Annotate lets an agent add a browser annotation overlay to AI-generated HTML pages, collect element-level comments, and feed those comments back for targeted edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[times77](https://clawhub.ai/user/times77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to review generated HTML pages visually, attach comments to specific page elements, and have the agent apply those comments to the source HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent global prompt hook.

Mitigation: Review ~/.claude/settings.json before and after installation, and uninstall or disable the hook when annotation work is complete.

Risk: The local feedback server is unauthenticated and can write inbox files under the user's home directory or /tmp.

Mitigation: Run the workflow in a disposable workspace, keep the server bound to localhost, stop it after use, and inspect .redline-inbox.json before allowing edits.

Risk: Submitted annotations can cause the agent to modify source HTML files.

Mitigation: Review the pending feedback payload and resulting file changes before accepting them.

## Reference(s):

- [Redline Annotate on ClawHub](https://clawhub.ai/times77/skills/redline-annotate)
- [Times77 publisher profile](https://clawhub.ai/user/times77)
- [@medv/finder selector helper](https://unpkg.com/@medv/finder@3.1.0/finder.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON feedback payloads, and HTML/CSS/JavaScript file edits.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates annotated HTML copies and a feedback inbox; the apply flow edits the original HTML and should remove the inbox after processing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
