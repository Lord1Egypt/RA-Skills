## Description: <br>
End-to-end Xiaohongshu operations including account positioning, topic research, content production, publishing workflows, comment replies, viral-copy drafting, and post-incident recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saybanet](https://clawhub.ai/user/saybanet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use this skill to run supervised Xiaohongshu account workflows: positioning an account, researching topics, drafting posts, preparing publish flows, checking comments, drafting replies, and recovering from failed automation steps. It is intended for human-reviewed social-media operations rather than unattended posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live Xiaohongshu account actions, including preparing posts and replies. <br>
Mitigation: Keep a human approval step before publishing or sending replies, and stop when the platform shows rate-limit, frequency, or send-failure warnings. <br>
Risk: The install guide prints a local gateway token that could grant access if shared. <br>
Mitigation: Redact token output, avoid sharing setup logs or screenshots, and rotate or reissue the token if it is exposed. <br>
Risk: Viral-copy workflows can create copyright, impersonation, or platform-policy risk if they reuse source text or images too closely. <br>
Mitigation: Use structure-level and style-only adaptation, avoid reusing original images or wording, and manually review every draft before publication. <br>
Risk: Persistent browser access to a logged-in social account can affect account integrity and reputation. <br>
Mitigation: Use a dedicated account or profile where appropriate, monitor account state, and revoke credentials or browser sessions when the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/saybanet/sayba-xiaohongshu-ops) <br>
- [XHS runtime rules](references/xhs-runtime-rules.md) <br>
- [XHS publish flows](references/xhs-publish-flows.md) <br>
- [XHS comment operations](references/xhs-comment-ops.md) <br>
- [XHS viral-copy workflow](references/xhs-viral-copy-flow.md) <br>
- [XHS evaluate patterns](references/xhs-eval-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with structured checklists, draft copy, inline code blocks, shell commands, and browser-operation steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may prepare live account actions, but posting and comment replies should remain human-reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
