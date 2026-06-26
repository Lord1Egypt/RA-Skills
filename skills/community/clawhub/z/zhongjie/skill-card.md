## Description: <br>
Zhongjie is a Chinese-language home-buying advisor skill that helps buyers clarify needs, research neighborhoods and policies, compare properties, and maintain a localhost browser workspace for buyer profiles, research notes, recommendations, and maps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MorvanZhou](https://clawhub.ai/user/MorvanZhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External home buyers and real-estate advisors use this skill to turn buyer conversations into structured requirements, research notes, policy checks, property comparisons, and recommendation reports. It is especially detailed for Chinese-language buying workflows and Shenzhen school-enrollment considerations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The localhost dashboard stores buyer notes on disk and exposes them while active. <br>
Mitigation: Keep the service bound to localhost, stop it after use, and avoid storing highly sensitive financial or family details until authentication and CORS controls are fixed. <br>
Risk: Map keys and customer-owned API secrets may be exposed or shared accidentally. <br>
Mitigation: Keep secrets in the local .env file, do not paste customer-owned API secrets into chat, and restrict or rotate the AMap key. <br>
Risk: Fetched WeChat or markdown content may be untrusted. <br>
Mitigation: Review and sanitize fetched content before relying on it, especially until markdown sanitization and TLS verification are corrected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MorvanZhou/zhongjie) <br>
- [Data file templates and standards](references/data_templates.md) <br>
- [Home-buying need dimensions and methodology](references/dimensions.md) <br>
- [Property map display options](references/map_display.md) <br>
- [School enrollment and policy reference](references/school_enrollment_policies.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Chinese-language conversational guidance, Markdown notes and reports, JSON property records, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update .skills-data/zhongjie/data files and use localhost dashboard or map configuration when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
