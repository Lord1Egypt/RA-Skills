## Description:

Designs production English prompts for Seedance 2.0 and helps generate WeryAI text-to-video, image-to-video, and multi-image video jobs with explicit pre-submit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative operators use this skill to convert short Seedance 2.0 video briefs into structured prompts, map reference images into WeryAI JSON fields, and submit paid video generation jobs only after confirming the full prompt and parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can read local image paths and upload those files to WeryAI when image inputs are not public HTTPS URLs.

Mitigation: Default to public HTTPS image URLs; allow local paths only after reviewing the script behavior and receiving explicit consent for the specific files.

Risk: Live submit and wait commands can consume paid WeryAI credits.

Mitigation: Require explicit approval of the full prompt and all generation parameters before every paid submit or wait action.

Risk: The WERYAI_API_KEY is required for live model, submit, status, wait, and upload operations.

Mitigation: Use a limited or short-lived key, keep it out of committed files, and run the skill from an isolated environment when higher assurance is needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zoucdr/skills/seedance-2-prompt-engineering-to-video)
- [Seedance 2.0 prompt engineering playbook](resources/seedance2-prompt-engineering-playbook.md)
- [Modes, strengths, and WeryAI field mapping](resources/modes-and-weryai-mapping.md)
- [Seedance 2.0 prompt recipes](resources/recipes-weryai.md)
- [Camera language and visual styles vocabulary](resources/camera-and-styles.md)
- [WeryAI video CLI and JSON](resources/WERYAI_VIDEO_API.md)
- [WeryAI video generation API host](https://api.weryai.com)
- [WeryAI model registry and upload host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON parameters and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce WeryAI task identifiers and Markdown video links after explicit user approval; requires Node.js 18+ and WERYAI_API_KEY for live API calls.]

## Skill Version(s):

1.1.2 (source: ClawHub release metadata; artifact frontmatter states 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
