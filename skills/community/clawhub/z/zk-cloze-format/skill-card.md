## Description: <br>
中考短文填空识别与格式化技能，用于在用户上传题目图片和可选答案图片后识别内容、还原格式，并按需输出Word文档或推送到飞书多维表格。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abendeng](https://clawhub.ai/user/abendeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers, tutors, and education-content operators use this skill to OCR Chinese middle-school cloze-test images, preserve the original exam layout, align answers by blank number, and export the result as a Word document or Feishu table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR may misread exam text, blank numbers, candidate words, or answers. <br>
Mitigation: Review the recognized text and aligned answers against the uploaded images before relying on or distributing the result. <br>
Risk: Feishu export can store or share recognized exam content outside the chat. <br>
Mitigation: Confirm the intended Feishu destination and permissions before pushing a document or table link. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abendeng/zk-cloze-format) <br>
- [中考短文填空格式规范参考](artifact/references/format-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown text, DOCX document, or Feishu table/link depending on the user's requested channel.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves paragraph breaks, numbered blanks, underscores, punctuation, candidate words, and answer alignment when the uploaded images provide them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
