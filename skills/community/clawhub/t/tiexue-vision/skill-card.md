## Description: <br>
Recognizes text, objects, and scenes in images from Feishu chats, Feishu documents, or local files, with optional Chinese translation and result writeback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldt5200-sys](https://clawhub.ai/user/ldt5200-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to extract text, object, and scene information from images in Feishu or local workflows, then return the recognition result to the source document or a local text file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted image text may be sent to Google Translate. <br>
Mitigation: Use only where translation egress is allowed by policy, or disable and gate translation before production use. <br>
Risk: Recognition results can be written back to shared Feishu chats or documents. <br>
Mitigation: Scope Feishu edit permissions tightly and require explicit approval for writeback in sensitive workspaces. <br>
Risk: Sensitive images may be processed by OCR and object detection. <br>
Mitigation: Review installation in workspaces containing sensitive images and limit access to trusted users and locations. <br>


## Reference(s): <br>
- [Tiexue Vision on ClawHub](https://clawhub.ai/ldt5200-sys/tiexue-vision) <br>
- [Publisher profile: ldt5200-sys](https://clawhub.ai/user/ldt5200-sys) <br>
- [Server-resolved provenance](unavailable) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text results with local file paths or Feishu writeback content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a same-name .txt result file for local images or update Feishu messages and documents when credentials and source context are provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
