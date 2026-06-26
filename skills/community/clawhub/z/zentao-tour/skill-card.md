## Description: <br>
以轻松聊天的方式带用户上手禅道（ZenTao）与 zentao-cli，让用户顺着自己的角色（产品经理/项目经理/测试/开发/高管）在真实禅道环境里边聊边动手，熟悉产品、需求、计划、任务、Bug、测试用例等模块的增删改查与状态流转。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catouse](https://clawhub.ai/user/catouse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ZenTao users, product managers, project managers, testers, developers, and executives use this skill to learn ZenTao and zentao-cli through a conversational role-based tour in a real ZenTao environment. The agent helps users inspect and, with approval, create, update, transition, or delete products, stories, plans, tasks, bugs, test cases, and related records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tour can issue zentao-cli commands that create, update, transition, or delete real ZenTao records. <br>
Mitigation: Use a sandbox or low-risk project for practice and approve write or delete actions only when the resulting data change is acceptable. <br>
Risk: ZenTao credentials or tokens used by zentao-cli may grant access to project data. <br>
Mitigation: Prefer tokens over passwords and protect the local zentao-cli configuration file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/catouse/zentao-tour) <br>
- [ZenTao official website](https://www.zentao.net/) <br>
- [ZenTao user manual](https://www.zentao.net/book/zentaopms/38.html) <br>
- [ZenTao version comparison](https://www.zentao.net/compare-features.html) <br>
- [zentao-cli repository](https://github.com/easysoft/zentao-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Conversational Markdown with inline zentao-cli shell commands and occasional JSON or Markdown table outputs from the CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may ask role-selection questions and should request approval before write, delete, or workflow-transition actions against ZenTao data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
