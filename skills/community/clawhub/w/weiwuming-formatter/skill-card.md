## Description: <br>
Converts uploaded .doc/.docx files or pasted text into WeChat article Markdown using the Weiwuming editor syntax while preserving source content and reporting formatting or review issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roloyty](https://clawhub.ai/user/roloyty) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and publishing agents use this skill to convert Word documents or pasted article text into WeChat-ready Markdown using the Weiwuming editor syntax. It preserves source content while adding required editorial sections, keyword blocks, image handling reports, and proofreading reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document-related images may be uploaded to a public third-party image host. <br>
Mitigation: Use only material intended for publication, avoid private or licensed images unless public rehosting is explicitly approved, and review uploaded image URLs before publishing. <br>
Risk: Web searches for keyword blocks and extended reading can introduce inaccurate or unsuitable metadata. <br>
Mitigation: Manually review generated keyword blocks, book recommendations, sources, and proofreading reminders before publishing. <br>
Risk: Local downloaded images may remain in an images/ folder after formatting. <br>
Mitigation: Delete the local images/ folder when the publishing workflow is complete. <br>


## Reference(s): <br>
- [Weiwuming Formatter ClawHub page](https://clawhub.ai/roloyty/weiwuming-formatter) <br>
- [WeChat Article Editor Syntax Rules](artifact/references/syntax_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with Weiwuming editor syntax, image-processing report, and proofreading reminders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local images/ folder and reference publicly hosted image URLs when image upload succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
