## Description:

Generate educational comic-style Xiaohongshu posts using AI-generated comic images, including topic research, storyboard creation, image generation, and automated publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horizonzzzz](https://clawhub.ai/user/horizonzzzz)

### License/Terms of Use:


## Use Case:

Creators and agents use this skill to turn a topic into an educational Xiaohongshu comic post with research notes, a Chinese dialogue storyboard, generated comic images, post copy, and publication steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can publish live Xiaohongshu posts using sensitive account cookies.

Mitigation: Protect Xiaohongshu cookies like passwords and require approval of the exact title, body, images, and target account before publishing.

Risk: The skill depends on mutable external skill installs and API-backed services.

Mitigation: Use pinned, trusted versions of external skills and review installed dependencies before execution.

Risk: Automated publishing can duplicate or misorder image posts.

Mitigation: Check recent runs, confirm all image paths are unique and ordered, and stop for user confirmation when similar work was just completed.

## Reference(s):

- [Workflow](references/workflow.md)
- [Comic Image Prompt Rules](references/comic_generation.md)
- [Xiaohongshu Posting](references/xhs_posting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured post copy, storyboard details, image-generation commands, and publishing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a title, body text, 5-6 comic image assets, and Xiaohongshu publishing payload guidance.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
