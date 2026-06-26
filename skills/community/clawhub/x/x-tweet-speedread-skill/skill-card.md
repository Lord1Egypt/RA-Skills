## Description: <br>
X Tweet Speedread (Premium) provides an instant English brief for an X post using a charge-first SkillPay flow at 0.001 USDT per call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangkefeng-ai](https://clawhub.ai/user/huangkefeng-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to turn an X status URL into a short English speedread with key bullets, a core takeaway, risks, and suggested actions. Each run should be treated as billable through the publisher's SkillPay model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is billable and uses a caller-supplied user ID, creating an unclear charge authorization boundary. <br>
Mitigation: Require explicit user confirmation before invoking the script with a user ID and treat each run as a billable action. <br>
Risk: The skill processes X URLs and may expose private, sensitive, or unwanted content to third-party fetch and billing services. <br>
Mitigation: Use only non-sensitive X URLs and install the skill only when the publisher and SkillPay billing model are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangkefeng-ai/x-tweet-speedread-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful output includes a charged status, fetch attempts, input URL, and a summary with bullets, core takeaway, risks, and actions; low balance can return PAYMENT_URL and PAYMENT_INFO.] <br>

## Skill Version(s): <br>
1.2.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
