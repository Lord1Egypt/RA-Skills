## Description: <br>
Generates concise Chinese reflections, aphorisms, quote-card lines, article endings, daily thoughts, and short 感悟 from a user's second-brain notes, GBrain, llm-wiki anchors, and long-term questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Knowledge workers, writers, and developers use this skill to turn local second-brain context into personally grounded Chinese reflections, aphorisms, quote-card copy, article endings, or daily thoughts. It is best suited to drafting compact prose from recalled notes, anchors, and long-term questions rather than creating generic motivational text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read personal notes, wiki pages, or GBrain search results when the user asks it to ground writing in second-brain context. <br>
Mitigation: Use it only when that context is intended, keep recall focused on relevant anchors, and review generated text before sharing. <br>
Risk: Broad activation wording could make the skill relevant to many personal-knowledge writing requests. <br>
Mitigation: Confirm the desired output shape or context when ambiguous, and disclose lower confidence when recall is thin or unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/second-brain-maxim) <br>
- [Second Brain Aphorism skill instructions](artifact/SKILL.md) <br>
- [Second Brain Aphorism style guide](artifact/references/style-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with Chinese prose labels such as 感悟, 箴言, numbered variants, and concise recall receipts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local GBrain or llm-wiki recall when available; does not write back to the user's second brain unless explicitly requested.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
