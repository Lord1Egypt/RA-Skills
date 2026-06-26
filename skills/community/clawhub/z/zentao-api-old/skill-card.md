## Description: <br>
Integrate with ZenTao Legacy API 1.0 to manage projects, tasks, bugs, products, and workflows with session persistence and role-specific operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellotombruce](https://clawhub.ai/user/hellotombruce) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, project managers, testers, and product teams use this skill to automate ZenTao Legacy API workflows such as creating requirements, managing tasks, tracking bugs, recording work, and querying project data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plaintext ZenTao credentials and reusable local sessions can expose the connected account. <br>
Mitigation: Use a least-privilege ZenTao account, keep TOOLS.md out of source control, avoid printing credentials, and remove or protect .zentao/sessions/ when the skill is no longer needed. <br>
Risk: The skill can change or delete project data through delete, close, unlink, and bulk-create operations. <br>
Mitigation: Require explicit user confirmation before destructive or high-volume operations and verify the target project, task, bug, or product identifiers before execution. <br>


## Reference(s): <br>
- [ZenTao API Client README](README.md) <br>
- [ZenTao Skill Guide](SKILL.md) <br>
- [ZenTao API Documentation Index](docs/index.md) <br>
- [ZenTao Official Site](https://www.zentao.net/) <br>
- [ZenTao API Help](https://www.zentao.net/book/zentaopmshelp/562.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/hellotombruce/zentao-api-old) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with Python and shell snippets, plus ZenTao API call results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, edit, delete, close, unlink, or bulk-create ZenTao project data when connected to a configured ZenTao account.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
