## Description: <br>
Assists with Xiaohongshu account operations, including account positioning, topic research, content drafting, publishing preparation, comment handling, and post-performance review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and social media teams use this skill to plan, draft, review, and prepare Xiaohongshu posts and replies while maintaining account-specific style and operational notes. It supports content workflows and live-account assistance, so users should review and confirm any publish or comment action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can assist with actions on a live Xiaohongshu account, including publishing preparation and comment replies. <br>
Mitigation: Require explicit user confirmation before any publish or comment send, and keep the workflow stopped at the publish button or reply draft until confirmed. <br>
Risk: Bulk or rapid replies can create account enforcement or spam-like behavior risk. <br>
Mitigation: Use one reply per turn by default, avoid bulk replies, preserve deliberate pacing, and stop immediately on frequency or send-failure warnings. <br>
Risk: Knowledge-base and style-learning files may persist account context, drafts, user preferences, or operational history. <br>
Mitigation: Review and redact persisted notes before reuse or sharing, and avoid storing sensitive personal, credential, or private account information. <br>
Risk: The artifact contains image-prompt guidance that suggests bypassing sensitive-person or copyright refusals. <br>
Mitigation: Remove or override that instruction and follow applicable safety, intellectual-property, and personality-rights policies for generated images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lovensky1992-wk/xhs-ops) <br>
- [README](artifact/README.md) <br>
- [XHS runtime rules](artifact/references/xhs-runtime-rules.md) <br>
- [XHS publish flows](artifact/references/xhs-publish-flows.md) <br>
- [XHS comment ops](artifact/references/xhs-comment-ops.md) <br>
- [Content analysis framework](artifact/references/content-analysis.md) <br>
- [Anti-AI checklist](artifact/references/anti-ai-checklist.md) <br>
- [Evaluation spec](artifact/evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured checklists, draft social posts, reply copy, image-prompt blocks, and occasional shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce knowledge-base updates and operational checkpoints for account workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
