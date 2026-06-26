## Description: <br>
End-to-end Xiaohongshu operations including positioning, topic research, content production, publish execution, and post-incident recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjscjj](https://clawhub.ai/user/mjscjj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, brand operators, and agency teams use this skill to plan Xiaohongshu account positioning, produce post drafts, prepare publishing flows, and manage comment replies with human confirmation for sensitive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live Xiaohongshu account automation for publishing and comment replies. <br>
Mitigation: Use it only with accounts that are appropriate for agent operation and require human confirmation before any publish or reply action. <br>
Risk: The optional OpenClaw setup script prints the gateway token in plaintext. <br>
Mitigation: Edit out the token-printing line before running the setup script, treat any displayed token as a secret, and rotate the token if it may have been exposed. <br>
Risk: Running social-account automation on a shared machine can expose account state or session access. <br>
Mitigation: Avoid shared machines and review the skill before installing or executing account automation flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mjscjj/xiaohongshu-ops-lobster) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mjscjj) <br>
- [XHS runtime rules](artifact/references/xhs-runtime-rules.md) <br>
- [XHS publish flows](artifact/references/xhs-publish-flows.md) <br>
- [XHS comment ops](artifact/references/xhs-comment-ops.md) <br>
- [XHS viral copy flow](artifact/references/xhs-viral-copy-flow.md) <br>
- [XHS evaluation patterns](artifact/references/xhs-eval-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with structured checklists, draft copy, prompts, and occasional shell command blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose browser automation steps and publishing or reply actions that should be confirmed by a human before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/PUBLISH.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
