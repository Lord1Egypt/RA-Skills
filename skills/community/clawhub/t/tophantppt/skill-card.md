## Description: <br>
tophantppt helps an agent generate image-based PowerPoint presentations from specified slide content or raw source material, using required background reference images to guide visual style and layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizhedm](https://clawhub.ai/user/lizhedm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn specified slide plans or raw source material into polished, image-based PowerPoint decks. It is especially useful when the deck must follow a consistent visual language driven by provided background reference images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches external reference images during presentation generation. <br>
Mitigation: Use it only in environments where fetching the listed reference images is acceptable, and review the fetched assets before final delivery. <br>
Risk: The workflow creates local slide images, design markdown, and PPTX output files that could overwrite existing work. <br>
Mitigation: Run the skill in a dedicated output folder and choose explicit filenames for generated files. <br>
Risk: Generated slide images may contain unreadable text, layout issues, or content errors because the final deck is image-based. <br>
Mitigation: Review each generated slide image for clarity and accuracy before merging the deck or sharing the PPTX. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lizhedm/tophantppt) <br>
- [Publisher profile](https://clawhub.ai/user/lizhedm) <br>
- [Skill homepage](https://clawic.com/skills/tophantppt) <br>
- [Cover background reference image](https://github.com/lizhedm/tophantppt/blob/main/assets/cover_bg.png) <br>
- [Default background reference image](https://github.com/lizhedm/tophantppt/blob/main/assets/moren.png) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown design plans, image-generation prompts, generated slide images, and a PPTX file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Automatic mode is constrained to no more than 40 slides; generated slide images are expected to be 16:9 and at least 1920x1080.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
