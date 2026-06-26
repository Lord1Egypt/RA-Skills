## Description: <br>
Read Bear notes tagged "待整理", extract topic keywords, search for relevant GIFs via gifgrep, insert them into the note, and remove the tag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to batch-process Bear research notes marked with the "待整理" tag by adding topic-relevant GIF markdown and removing the workflow tag when processing is complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill batch-edits Bear notes tagged "待整理" by adding GIF links and removing the workflow tag. <br>
Mitigation: Reserve the tag for notes intended for automated finalization and review or back up important notes before running the workflow. <br>
Risk: The workflow uses a local Bear token file and may send derived note topics to GIF or web search providers. <br>
Mitigation: Protect the grizzly token file and avoid using the skill on sensitive notes when derived topics should not leave the local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/research-assistant-bear) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with shell command guidance and inserted GIF markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Bear notes accessible through grizzly and reports processed notes and GIF insertion counts.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
