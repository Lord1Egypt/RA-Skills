## Description: <br>
根据提供的网站页面自动生成测试用例，支持 UI 测试、功能测试、流程测试、异常测试、权限测试和兼容性测试，并输出 Markdown 表格或 CSV。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linzetai](https://clawhub.ai/user/linzetai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and product teams use this skill to inspect web pages, identify interactive elements and flows, and generate structured UI, functional, process, exception, permission, and compatibility test cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect live web pages and propose real clicks, form fills, submissions, or external document exports. <br>
Mitigation: Use staging sites or test accounts where possible, and explicitly approve real clicks, form fills, submissions, and exports before they occur. <br>
Risk: Generated Markdown or CSV files could overwrite or create confusing local test-case artifacts. <br>
Mitigation: Choose non-destructive filenames and review generated test cases before saving or sharing them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown tables and CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce named test-case files such as <feature>-test-cases.md and <feature>-test-cases.csv.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
