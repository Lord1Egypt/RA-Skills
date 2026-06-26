## Description: <br>
Provides BaZi and Qi Men Dun Jia chart generation and interpretation through the Xiaoqi Intelligent Calculation API using a required API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colorwlof](https://clawhub.ai/user/colorwlof) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect agents to Xiaoqi Intelligent Calculation for BaZi fortune-cycle queries and Qi Men Dun Jia chart preparation or interpretation. It is intended as a decision-reference aid rather than deterministic advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends birth details, sex, and question text to xiaoqizhisuan.cn for processing. <br>
Mitigation: Provide only the data needed for the request, avoid unnecessary sensitive free-form details, and review the provider privacy policy before use. <br>
Risk: API calls may incur pay-per-call charges through the configured provider account. <br>
Mitigation: Keep user confirmation enabled, monitor account balance and usage, and rely on the configured per-session spend cap. <br>
Risk: Traditional chart interpretations can be mistaken for deterministic personal, financial, or life guidance. <br>
Mitigation: Treat outputs as decision-reference material and review interpretation results before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/colorwlof/skill-qimen-api) <br>
- [Xiaoqi Intelligent Calculation homepage](https://www.xiaoqizhisuan.cn) <br>
- [Xiaoqi API help](https://www.xiaoqizhisuan.cn/help.html) <br>
- [Xiaoqi privacy policy](https://www.xiaoqizhisuan.cn/privacy.html) <br>
- [Xiaoqi terms of service](https://www.xiaoqizhisuan.cn/terms.html) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, text, configuration, guidance] <br>
**Output Format:** [MCP tool responses with JSON fields, text prompts, interpretation text, and chart URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XIAOQIZHISUAN_API_KEY and user confirmation for pay-per-call usage; per-session spend cap is ¥2.] <br>

## Skill Version(s): <br>
1.0.20 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
