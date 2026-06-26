## Description: <br>
代码审查助手会分析代码结构和风格，提供审查意见、性能优化建议、安全漏洞检测，并生成详细的代码审查报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to request automated review of individual files or project directories, with findings on code quality, performance, and potential security issues. It is intended to produce a review report that can guide follow-up fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package is documentation-only and references node scripts/review.mjs without including that tool. <br>
Mitigation: Before running the command, confirm scripts/review.mjs comes from a trusted intended source in the target project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/smart-code-reviewer) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node; reviewed package does not include the referenced review script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
