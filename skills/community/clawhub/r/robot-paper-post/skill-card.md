## Description: <br>
Deeply analyzes robotics and embodied AI papers and generates illustrated technical posts using a zero-extra-installation workflow that extracts figures and captions from arXiv HTML and project pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessy-huang](https://clawhub.ai/user/jessy-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, researchers, and developers use this skill to turn robotics or embodied AI paper titles, arXiv IDs, project pages, or paper links into structured technical posts with evidence-based summaries, resource links, and inserted figures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional local image downloading may fetch external paper images into the working directory. <br>
Mitigation: Prefer direct arXiv figure URLs when possible; when local files are needed, inspect the download script first and write output to a scoped folder. <br>
Risk: Generated article text may misstate paper claims, experimental numbers, or image-to-section alignment. <br>
Mitigation: Review the final post against the original paper, project page, and selected figures before publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jessy-huang/robot-paper-post) <br>
- [README](README.md) <br>
- [Paper structure guide](references/paper-structure.md) <br>
- [Technology terms glossary](references/tech-terms-glossary.md) <br>
- [Research teams index](references/research-teams.md) <br>
- [Classic papers index](references/classic-papers.md) <br>
- [Image insertion workflow](references/image-insertion-workflow.md) <br>
- [Post template](assets/post-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown technical post with figure links, captions, resource lists, and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference remote arXiv figure URLs or local image paths when the user asks for offline delivery.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
