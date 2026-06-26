## Description: <br>
Master routing skill for all X/Twitter operations -- reading, researching, posting, and engaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremyknows](https://clawhub.ai/user/jeremyknows) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to route X/Twitter tasks to the right workflow for reading tweets, researching discourse, drafting posts, handling mentions, or using credentialed X API tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentialed X API routes can enable broad state-changing actions such as posting, follower operations, batch operations, or analytics access. <br>
Mitigation: Connect X OAuth credentials only after review, keep state-changing actions behind explicit approval, and review optional sub-skill permissions before installation. <br>
Risk: Posting or replying from an account can publish unintended, misleading, or off-brand content. <br>
Mitigation: Use draft-and-approve mode and require human approval of the exact account and text before publishing. <br>
Risk: Using the public fxtwitter proxy may expose sensitive monitoring targets or private investigative context to an external service. <br>
Mitigation: Avoid the public proxy for sensitive monitoring unless the data-sharing tradeoff is acceptable. <br>


## Reference(s): <br>
- [X Master on ClawHub](https://clawhub.ai/jeremyknows/x-master) <br>
- [fxtwitter Pattern](references/fxtwitter-pattern.md) <br>
- [Algorithm Intelligence](references/algo-intel.md) <br>
- [FxTwitter](https://github.com/FixTweet/FxTwitter) <br>
- [fxtwitter Public API](https://api.fxtwitter.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline commands, routing decisions, drafts, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes posting and credentialed X API actions through approval-oriented workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
