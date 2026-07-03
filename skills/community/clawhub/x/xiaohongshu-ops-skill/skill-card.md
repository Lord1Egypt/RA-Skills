## Description: <br>
Xiaohongshu Ops Skill helps an agent plan, analyze, draft, publish-prep, reply, and review Xiaohongshu account operations through OpenClaw browser workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongjie-oss](https://clawhub.ai/user/dongjie-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media operators, creators, and agent developers use this skill to run Xiaohongshu workflows for account positioning, feed and account analysis, topic ideation, content drafting, publish preparation, comment replies, and post-run knowledge capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a real Xiaohongshu account and perform posting or replying workflows. <br>
Mitigation: Use preview or draft mode for posts and replies, and require explicit confirmation before any live posting or reply is sent. <br>
Risk: The skill requires sensitive credentials and may expose gateway tokens in shared terminals or logs. <br>
Mitigation: Review the installer before running it and avoid displaying, pasting, or logging tokens in shared environments. <br>
Risk: The skill may persist or mutate account operational notes. <br>
Mitigation: Require explicit confirmation before knowledge-base writes and review retained notes for sensitive account or campaign information. <br>


## Reference(s): <br>
- [Xiaohongshu Ops Skill on ClawHub](https://clawhub.ai/dongjie-oss/xiaohongshu-ops-skill) <br>
- [OpenClaw browser tool documentation](https://docs.openclaw.ai/tools/browser) <br>
- [XHS runtime rules](references/xhs-runtime-rules.md) <br>
- [XHS account analysis](references/xhs-account-analysis.md) <br>
- [XHS home feed analysis](references/xhs-home-feed-analysis.md) <br>
- [XHS topic ideation](references/xhs-topic-ideation.md) <br>
- [XHS viral copy flow](references/xhs-viral-copy-flow.md) <br>
- [XHS publish flows](references/xhs-publish-flows.md) <br>
- [XHS comment operations](references/xhs-comment-ops.md) <br>
- [XHS knowledge base](references/xhs-knowledge-base.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured checklists, content drafts, analysis summaries, inline code, shell commands, and local knowledge-base notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May operate a real Xiaohongshu account through OpenClaw browser automation and may persist operational notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
