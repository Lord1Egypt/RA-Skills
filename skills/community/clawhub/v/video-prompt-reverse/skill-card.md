## Description:

Video Prompt Reverse helps agents turn short videos or local clips into structured visual prompt language by guiding video download, key-frame extraction, Doubao browser analysis, and shot-language prompt assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobemsk](https://clawhub.ai/user/tobemsk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content workflow builders use this skill to reverse-engineer video framing, camera motion, lighting, costume, composition, and scene atmosphere into reusable AI image or storyboard prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can attach to and act on an unrelated browser tab.

Mitigation: Use a dedicated browser profile with no sensitive sessions and verify the exact Doubao tab before any CDP action.

Risk: Video frames may contain private, sensitive, or copyrighted content before upload to an external analysis service.

Mitigation: Review frames before upload and avoid sending private, sensitive, or copyrighted material.

Risk: Cookie-based downloads combined with disabled certificate checks can expose browsing sessions or weaken transport protections.

Mitigation: Avoid combining browser cookies with disabled certificate checks; use isolated sessions and safer download settings where possible.

Risk: Unpinned command-line and Python dependencies can change behavior across installations.

Mitigation: Install dependencies in an isolated environment and prefer pinned versions.

## Reference(s):

- [Full workflow](references/full_workflow.md)
- [Output patterns](references/output_patterns.md)
- [Troubleshooting](references/troubleshooting.md)
- [Doubao](https://doubao.com)
- [ClawHub skill page](https://clawhub.ai/tobemsk/skills/video-prompt-reverse)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, code snippets, and structured prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces frame-selection guidance, browser automation instructions, troubleshooting notes, and structured cinematic prompt text.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
