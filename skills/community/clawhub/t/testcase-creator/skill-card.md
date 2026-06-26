## Description: <br>
本技能从需求文档生成全面的测试用例文档。当用户需要从需求文档、产品规格说明或描述系统功能的文档创建测试用例时使用此技能。默认生成Markdown格式的测试用例文档；当用户明确要求生成"思维导图格式"或"xmind格式"时，会额外生成XMind思维导图文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duyinghua](https://clawhub.ai/user/duyinghua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and QA engineers use this skill to turn requirements documents or product specifications into structured test-case documentation, with optional XMind output when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process private requirements documents or document URLs. <br>
Mitigation: Only provide documents and URLs the agent is authorized to access, and avoid exposing confidential product or business information unnecessarily. <br>
Risk: Generated Markdown or XMind files may persist sensitive requirements-derived content. <br>
Mitigation: Choose an appropriate output folder and clean up old timestamped versions when source requirements contain confidential information. <br>


## Reference(s): <br>
- [Test case template](artifact/references/testcase_template.md) <br>
- [Requirements analysis guide](artifact/references/analysis_guide.md) <br>
- [Test case quality standard](artifact/references/quality_standard.md) <br>
- [Module merge guide](artifact/references/module_merge_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown test-case documents by default; XMind files may also be produced when explicitly requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated test-case filenames include timestamp suffixes to preserve historical versions.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
