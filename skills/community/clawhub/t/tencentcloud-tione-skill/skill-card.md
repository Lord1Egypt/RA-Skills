## Description: <br>
Tencent Cloud TI-ONE query toolkit for inspecting training jobs, online services, notebooks, resource groups, model repositories, datasets, logs, and events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alger-z](https://clawhub.ai/user/alger-z) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to query Tencent Cloud TI-ONE resources, inspect logs and events, and generate console links while reviewing training and inference workloads. <br>

### Deployment Geography for Use: <br>
Tencent Cloud TI-ONE regions listed by the skill: Beijing, Shanghai, Guangzhou, Shanghai ADC, Zhongwei, and Nanjing. <br>

## Known Risks and Mitigations: <br>
Risk: Tencent Cloud API credentials can expose TI-ONE data visible to the provided key. <br>
Mitigation: Use a dedicated read-only, least-privileged Tencent Cloud key for this skill. <br>
Risk: TI-ONE log and metadata queries may return sensitive operational details in the agent conversation. <br>
Mitigation: Keep log queries narrowly scoped and review returned data before sharing it outside the intended audience. <br>
Risk: The skill depends on external command-line tools. <br>
Mitigation: Install tccli and jq from trusted sources before use. <br>


## Reference(s): <br>
- [TI-ONE tool parameter reference](references/cmd-reference.md) <br>
- [TI-ONE console reference](references/tione-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/alger-z/tencentcloud-tione-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, formatted JSON query results, and Tencent Cloud console URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only TI-ONE Describe queries through bundled scripts; requires Tencent Cloud credentials, tccli, jq, and an optional default region.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
