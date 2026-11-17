## Description:

Use this skill for SlideClaw and Marp deck tasks, including creating slide decks, rendering Marp files, and saving reusable templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akamichikota](https://clawhub.ai/user/akamichikota)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and teams use this skill to create Marp slide decks with SlideClaw, select or create templates, render HTML and PDF outputs, and optionally save durable presentation preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use npx -y slideclaw@latest, which can run the current npm package instead of a pinned or locally reviewed version.

Mitigation: Prefer a locally installed or pinned SlideClaw CLI, and review the npm package before allowing the fallback.

Risk: Rendering can copy generated files to the operating system Downloads folder outside the workspace.

Mitigation: Use --no-copy-to-downloads or set SLIDECLAW_NO_DOWNLOADS=1 when out-of-workspace copies are not desired.

Risk: The workflow can update profile/user.md with durable presentation preferences.

Mitigation: Review and approve profile changes explicitly before saving them.

## Reference(s):

- [SlideClaw GitHub homepage](https://github.com/akamichikota/SlideClaw)
- [SlideClaw ClawHub skill page](https://clawhub.ai/akamichikota/skills/slideclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, Marp slide source, shell commands, and rendered slide artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update SlideClaw workspace files and render HTML or PDF outputs; PDF rendering depends on local CLI and browser dependencies.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
