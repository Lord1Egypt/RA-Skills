## Description: <br>
Reads draft Markdown from ~/.openclaw/workspace/tibetanDraft/, identifies a Tibetan Buddhist product theme, and generates a Simplified Chinese article with Tibetan-style PNG images in ~/.openclaw/workspace/tibetanProc/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3ffyang](https://clawhub.ai/user/j3ffyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to turn Tibetan Buddhist product drafts into Simplified Chinese articles with factual research notes and matching Tibetan-style images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Markdown drafts from ~/.openclaw/workspace/tibetanDraft/, so unrelated or sensitive local drafts could be processed if placed there. <br>
Mitigation: Keep unrelated or sensitive Markdown out of the draft folder and review the selected input before running the skill. <br>
Risk: Generated articles, images, source logs, and fallback content may contain inaccuracies or claims that need review before publication. <br>
Mitigation: Review the generated article, images, logs, and research sources, and fact-check marked or uncertain claims before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j3ffyang/tibetan-buddhist-product-article-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Images, JSON, Text] <br>
**Output Format:** [Timestamped Markdown article files, PNG image files, JSON run metadata, and optional text logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written under ~/.openclaw/workspace/tibetanProc/ using timestamp-based filenames.] <br>

## Skill Version(s): <br>
1.1.0 (source: artifact/SKILL.md frontmatter; server release metadata: 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
