## Description: <br>
Researches a topic in a managed browser and writes a complete, human-sounding blog post as a Markdown file under ~/blogs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dishant0406](https://clawhub.ai/user/dishant0406) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to have an agent research a specified topic from public web sources and draft a casual, structured blog post. It is suited for one-off article drafting where a human will review the facts, tone, and final Markdown before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill researches topics through public web sources in a managed browser. <br>
Mitigation: Use it only for topics that are acceptable to research externally, and avoid confidential or sensitive prompts. <br>
Risk: The skill persists finished drafts locally under ~/blogs. <br>
Mitigation: Review the generated file path and remove or relocate drafts that should not remain on disk. <br>
Risk: The finished blog post may include factual claims or subjective takes gathered from public sources. <br>
Mitigation: Review the draft, sources, and claims before publishing or reusing the content. <br>


## Reference(s): <br>
- [Skill Source](SKILL.md) <br>
- [Research](references/research.md) <br>
- [Structure](references/structure.md) <br>
- [Writing Style](references/writing-style.md) <br>
- [Human Voice](references/human-voice.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dishant0406/re-blog-writer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Text] <br>
**Output Format:** [Markdown blog draft saved as a .md file, plus a short text completion report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets 1200-1500 words and saves the draft under ~/blogs without an H1 title.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
