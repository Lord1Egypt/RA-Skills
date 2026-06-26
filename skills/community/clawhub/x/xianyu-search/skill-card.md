## Description: <br>
Generates second-hand shopping search links and structured buying guidance for Xianyu, Zhuanzhuan, and Paipai based on budget, condition, seller-credit, battery-health, and location preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lg2021888](https://clawhub.ai/user/lg2021888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to turn natural-language second-hand shopping requests into platform search URLs, comparison tables, and practical pre-purchase checks. It is most useful when a user wants help narrowing product searches by budget, condition, battery health, location, and seller trust signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags the skill as suspicious because some shopping guidance can frame enterprise or MDM-managed devices as bypassable purchase options. <br>
Mitigation: Treat MDM-managed, locked, already-bypassed, or otherwise restricted devices as high-risk and advise users to avoid relying on this skill as proof that a listing is legitimate, safe, or transferable. <br>
Risk: Generated recommendations may be based on user-provided or example listing data rather than verified live marketplace details. <br>
Mitigation: Require users to open the platform listing, verify seller reputation and device status, use protected payment flows, and perform independent inspection before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lg2021888/xianyu-search) <br>
- [Publisher profile](https://clawhub.ai/user/lg2021888) <br>
- [Goofish search](https://www.goofish.com/search) <br>
- [Goofish safety center](https://www.goofish.com/safety) <br>
- [Yanhuobao inspection service](https://www.yanhuobao.com) <br>
- [12315 consumer complaint portal](https://www.12315.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with search links, comparison tables, checklist items, and optional JavaScript usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory and link-oriented; users must inspect live listings and make purchase decisions themselves.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
