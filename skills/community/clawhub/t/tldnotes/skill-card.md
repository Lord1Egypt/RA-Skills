## Description:

📝 用 tldraw 画板制作学神风格板书——外框围栏、分区清晰、笔记感。适合高校/竞赛风格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

Students, educators, and agents assisting them use this skill to create structured tldraw whiteboard notes with framed sections, restrained colors, annotations, formulas, and optional illustrations. It also guides agents through creating, editing, validating, and recovering local tldraw Desktop canvases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose a local tldraw Desktop auth token and open document metadata to agent context.

Mitigation: Treat ~/.config/tldraw/server.json and its token as sensitive, and avoid logging, sharing, or persisting the token outside the local session.

Risk: The /exec and document script workflows can change saved canvases.

Mitigation: Confirm the target document and current shapes before broad edits, use the skill's validation steps after changes, and stop when the open document does not match expectations.

Risk: The security verdict is suspicious because authenticated local canvas access is available to agents.

Mitigation: Install only when comfortable granting agents authenticated access to the running tldraw Desktop server.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/tldnotes)
- [tldraw Offline download page](https://offline.tldraw.com/)
- [tldraw Offline latest releases](https://github.com/tldraw/tldraw-offline/releases/latest)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or modify local tldraw canvas documents through the authenticated local tldraw Desktop server.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
