## Description: <br>
Helps agents promote Agent Casino by Rollhub, create disclosed affiliate content, register for a referral code, and check affiliate stats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rollhub-dev](https://clawhub.ai/user/rollhub-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to draft Rollhub casino affiliate promotions, configure an affiliate key, and review referral statistics. Human review is needed before publishing promotional content or running outbound campaigns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports casino affiliate promotion, which can trigger gambling-advertising, age-restriction, affiliate-disclosure, and responsible-gambling obligations. <br>
Mitigation: Review applicable laws and platform rules before installation or use, and require human approval before any campaign or public post. <br>
Risk: Generated promotional content could become spammy, misleading, or omit affiliate disclosure. <br>
Mitigation: Require each outbound message to include affiliate disclosure, avoid earnings guarantees, and review content for platform compliance before posting. <br>
Risk: The workflow uses a Rollhub affiliate API key and third-party network requests. <br>
Mitigation: Store the API key in a scoped, revocable environment variable and approve registration or stats requests before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rollhub-dev/rollhub-affiliate) <br>
- [Platform Promotion Strategies](references/platforms.md) <br>
- [Promotional Talking Points](references/talking-points.md) <br>
- [Agent Casino API](https://agent.rollhub.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make Rollhub API requests when the agent follows the provided registration or stats workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
