## Description:

Story Video Skill helps agents turn story text into screenplay shot JSON, MiniMax-generated images and videos, and an FFmpeg-merged final video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhongm](https://clawhub.ai/user/yhongm)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers can use this skill to plan story structure, generate shot breakdowns, create MiniMax image and video assets, and merge generated clips into a finished story video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API keys and story content to MiniMax or to endpoints configured through override variables.

Mitigation: Use a low-privilege MiniMax API key with spending limits, leave endpoint override variables unset unless the destination is trusted, and avoid submitting confidential story material.

Risk: The merge workflow may attempt system-level FFmpeg installation.

Mitigation: Install FFmpeg manually or run the skill in a container, and do not run the merge script with passwordless sudo.

Risk: Text-to-image and image-to-video generation can consume paid MiniMax tokens.

Mitigation: Confirm account balance and expected shot count before running full video generation.

## Reference(s):

- [Story Video Skill page](https://clawhub.ai/yhongm/skills/story-video-skill)
- [MiniMax API overview](references/minimax-api/api-overview.txt)
- [MiniMax models introduction](references/minimax-api/models-intro.txt)
- [MiniMax quickstart preparation](references/minimax-api/quickstart-preparation.txt)
- [Image generation text-to-image reference](references/minimax-api/image-generation-t2i.txt)
- [Image generation image-to-image reference](references/minimax-api/image-generation-i2i.txt)
- [Screenwriting story structure reference](references/screenwriting/story-structure.txt)
- [Screenwriting shot breakdown reference](references/screenwriting/shot-breakdown.txt)
- [Visual storytelling principles reference](references/director-knowledge/visual-storytelling-principles.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces screenplay shot JSON, generated image and video files, storyboard text, and a merged MP4 when the external services and local tools are configured.]

## Skill Version(s):

1.5.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
