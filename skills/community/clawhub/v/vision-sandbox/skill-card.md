## Description:

Agentic Vision via Gemini's native Code Execution sandbox. Use for spatial grounding, visual math, and UI auditing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johanesalxd](https://clawhub.ai/user/johanesalxd)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use Vision Sandbox to send images and prompts to Gemini for spatial grounding, visual calculation, UI auditing, and visual reasoning that can inform coding or review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chosen images and prompts are sent to Gemini/Google for processing.

Mitigation: Do not use sensitive screenshots, secrets, regulated data, or private customer material unless policy permits that external processing.

Risk: Generated inline image outputs can be written as sandbox_output_*.png in the current directory, where names may collide.

Mitigation: Run the skill from a working directory where these output filenames are acceptable, or move existing sandbox_output_*.png files before execution.

## Reference(s):

- [Vision Sandbox on ClawHub](https://clawhub.ai/johanesalxd/skills/vision-sandbox)
- [Vision Sandbox source repository](https://github.com/johanesalxd/vision-sandbox)
- [uv Python package manager](https://github.com/astral-sh/uv)

## Skill Output:

**Output Type(s):** [text, markdown, code, files]

**Output Format:** [Markdown-like CLI output with model text, Python code blocks, sandbox output blocks, and optional generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write sandbox_output_<candidate>_<part>.png files when Gemini returns inline image data.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
