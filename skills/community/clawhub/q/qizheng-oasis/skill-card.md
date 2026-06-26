## Description: <br>
Qizheng Oasis runs OASIS-style market promotion and public-opinion crisis simulations with role-based agents, propagation models, and report/dashboard outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horizoncove](https://clawhub.ai/user/horizoncove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, e-commerce, and public-relations teams can use this skill to simulate promotional spread, inventory pressure, opinion propagation, and crisis-response timelines. Treat results as scenario analysis, not financial optimization or investment guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read a SiliconFlow API key from a workspace credential file or SILICONFLOW_API_KEY and make external LLM calls. <br>
Mitigation: Remove or isolate the key unless external SiliconFlow calls are intended, and avoid sending confidential scenarios or business data through the skill. <br>
Risk: The dashboard includes iframe inspection and postMessage behavior. <br>
Mitigation: Do not embed the dashboard in other sites until the iframe inspection code is removed or constrained with explicit origin checks and user-controlled activation. <br>
Risk: Finance-oriented metadata may cause users to treat the simulator as finance or investment optimization. <br>
Mitigation: Describe and use the skill as marketing, buyer-persona, and public-opinion scenario simulation only. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/horizoncove/qizheng-oasis) <br>
- [Publisher profile](https://clawhub.ai/user/horizoncove) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, Python scripts, JSON simulation outputs, and an HTML dashboard.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Simulation outputs can include generated role profiles, promotion forecasts, crisis timelines, report data, and dashboard-ready JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
