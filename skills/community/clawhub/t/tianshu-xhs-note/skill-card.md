## Description: <br>
Formats existing draft material into a Xiaohongshu note structure with title ideas, paragraphing, hashtag suggestions, word-count guidance, and a pre-publication checklist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and publishing assistants use this skill to turn existing Xiaohongshu draft text or notes into a structured Markdown draft with title options, readable paragraphs, hashtag candidates, and a posting checklist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A selected input file may contain private or sensitive draft text that appears in the generated Markdown output. <br>
Mitigation: Use --text for short drafts when practical, or pass --file only for the draft that should be formatted. <br>
Risk: Rule-based hashtag and compliance checklist suggestions may be incomplete or unsuitable for regulated topics. <br>
Mitigation: Review generated tags and checklist items before publishing, especially for medical, financial, or advertising claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangshengli0421/tianshu-xhs-note) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated locally from provided text or a selected UTF-8 draft file; hashtag suggestions are rule-based candidates that should be reviewed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
