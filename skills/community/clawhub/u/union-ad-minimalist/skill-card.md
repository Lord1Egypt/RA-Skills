## Description: <br>
Union Ad Minimalist helps an agent turn documents, notes, or prompts into UnionSkill-branded minimalist black-and-white advertising presentations through content analysis, outline confirmation, slide image generation, and PPTX assembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, designers, consultants, and developers use this skill to create branded UnionSkill promotional decks for design showcases, architecture proposals, business roadshows, exhibitions, customer proposals, and open-source release materials. The workflow requires outline confirmation before generating full-slide images and assembling the final presentation package. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or proprietary input material may be reflected in generated slides or packaged outputs. <br>
Mitigation: Review source material before use and avoid providing sensitive content unless it is intended for the final presentation. <br>
Risk: The presentation assembly step depends on a separate ppt-generator assembler component. <br>
Mitigation: Verify the assembler dependency and its behavior before using the Python packaging step. <br>
Risk: Generated slide images can contain incorrect, unreadable, or off-brand text. <br>
Mitigation: Use the required outline-confirmation step and final QA checks for slide count, blank pages, and Chinese title readability before delivery. <br>


## Reference(s): <br>
- [Union Ad Minimalist on ClawHub](https://clawhub.ai/timo2026/union-ad-minimalist) <br>
- [Minimalist Black-and-White Style Guide](artifact/references/style_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance and terminal text with generated presentation files such as PPTX, PNG slide images, ZIP archives, text notes, and optional HTML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation of the proposed outline before slide image generation; outputs are UnionSkill-branded with watermarking and metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
