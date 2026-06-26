## Description: <br>
调用本地安装的 vRain 工具，将 Markdown 或纯文本中文古籍转换为古籍刻本风格的直排 PDF 电子书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanleiguang](https://clawhub.ai/user/shanleiguang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and digital humanities users use this skill to prepare Chinese classic texts as vertically typeset PDF ebooks with traditional book-page styling. It provides local command guidance for installing vRain, configuring book and canvas assets, testing layout, and generating final PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on a separately installed local vRain repository and Perl modules. <br>
Mitigation: Install only from trusted sources and prefer non-sudo dependency installation when possible. <br>
Risk: Large batch runs can overwrite existing generated PDFs or produce many local files. <br>
Mitigation: Use the documented test mode before large runs, confirm output paths, and back up existing generated PDFs before rerunning commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shanleiguang/vrain) <br>
- [vRain GitHub repository](https://github.com/shanleiguang/vRain) <br>
- [vYinn GitHub repository](https://github.com/shanleiguang/vYinn) <br>
- [vQi GitHub repository](https://github.com/shanleiguang/vQi) <br>
- [vModou GitHub repository](https://github.com/shanleiguang/vModou) <br>
- [vBorder GitHub repository](https://github.com/shanleiguang/vBorder) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and configuration code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workflow guidance for creating PDF files with vRain; it does not include the vRain code.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
