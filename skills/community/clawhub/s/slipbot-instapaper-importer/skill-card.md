## Description: <br>
Import reading notes from Instapaper exports into the slipbox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrswab](https://clawhub.ai/user/jrswab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to parse pasted Instapaper highlight exports, skip quoted article highlights, preview the user's own notes, and create slipbox entries after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Instapaper exports may include private URLs or sensitive personal notes. <br>
Mitigation: Review the precheck before confirming import and only import notes that are appropriate to store in the slipbox. <br>
Risk: The importer creates one slipbox entry for each parsed plain-text note. <br>
Mitigation: Confirm the article title and note count before allowing slipbot to create entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jrswab/slipbot-instapaper-importer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and plain-text slipbot commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs parsed note previews, confirmation prompts, per-note slipbot import commands, and a final import count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
