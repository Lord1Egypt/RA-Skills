## Description: <br>
AI Agent usage tracking and billing verification tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeterWang](https://clawhub.ai/user/jeterWang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI Agent users use this skill to track feature usage, generate usage reports, check account balance, create recharge links, and verify paid feature billing through SkillPay.me. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawScan reports that the skill ships real payment authority in code and can trigger charges without enough safeguards. <br>
Mitigation: Use only after removing and rotating embedded credentials, requiring installer-provided credentials, and adding clear user confirmation, limits, and auditability for every charge. <br>
Risk: The skill depends on SkillPay.me for billing actions. <br>
Mitigation: Install only when the publisher and SkillPay.me are trusted, and test billing behavior before using it with real funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeterWang/usage-tracker-clawhub) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jeterWang) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration] <br>
**Output Format:** [Plain text responses with Markdown-style command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands can call SkillPay.me billing, balance, and payment-link endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
