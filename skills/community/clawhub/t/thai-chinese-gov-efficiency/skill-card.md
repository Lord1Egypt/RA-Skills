## Description: <br>
Academic research agent for comparative analysis of governance structures in Thai and Chinese public business schools and their impact on educational efficiency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1829162846lw](https://clawhub.ai/user/1829162846lw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and academic teams use this skill to build theoretical frameworks, design mixed-methods comparative studies, coordinate literature review and data collection, and manage longitudinal research workflows for Thai and Chinese public business schools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to run local Python or R commands and fetch web content during data collection. <br>
Mitigation: Review proposed commands, paths, data sources, and outputs before execution; run only in an isolated workspace with appropriate permissions. <br>
Risk: The skill describes spawning subagents for literature review and data analysis. <br>
Mitigation: Approve subagent delegation, tool access, and scope before use, especially when delegated work may execute commands. <br>
Risk: The quality protocol requests recurring updates to another skill without version pinning. <br>
Mitigation: Do not allow recurring skill updates unless intentionally approving a pinned, reviewed version. <br>


## Reference(s): <br>
- [Chinese Ministry of Education public notice](https://public.moe.gov.cn/jytb_ghfz/ghfw/202312/t20231201_1093012.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell, tool, JSON, and Mermaid snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local Python or R commands and subagent delegation for user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
