## Description: <br>
武侠小说创作主编 coordinates wuxia novel ideation, outlining, drafting, review, revision, continuation from existing drafts, and final TXT formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongzichixiangjiao](https://clawhub.ai/user/kongzichixiangjiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creative writers use this skill to generate or continue Chinese wuxia novels with an autonomous editorial workflow. It plans the story, coordinates drafting and review roles, checks continuity and style, and produces a formatted text manuscript. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and resume manuscript files in a target output directory. <br>
Mitigation: Run it in a dedicated project or output folder and avoid pointing it at broad private directories. <br>
Risk: The skill makes creative decisions autonomously and may not ask clarifying questions before generating or continuing a novel. <br>
Mitigation: Review generated outlines, drafts, and final TXT output before publication or distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kongzichixiangjiao/wuxia-novel-master) <br>
- [README](artifact/README.md) <br>
- [Main skill definition](artifact/SKILL.md) <br>
- [Writer sub-skill](artifact/references/05-写手/SKILL.md) <br>
- [Checker sub-skill](artifact/references/06-检查/SKILL.md) <br>
- [Typesetter sub-skill](artifact/references/07-排版/SKILL.md) <br>
- [Evaluation cases](artifact/evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown planning and review artifacts plus a final TXT novel manuscript] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save and resume work from files in a target output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
