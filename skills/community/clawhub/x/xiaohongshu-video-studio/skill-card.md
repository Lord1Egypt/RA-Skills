## Description:

Analyzes Xiaohongshu video links and creates transcripts, summaries, video breakdowns, scripts, and generation prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators can use the skill to turn Xiaohongshu video links into transcripts, summaries, structural analyses, shot scripts, rewritten or original scripts, and generation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions ask users to paste a Cue API key into chat, which could expose credentials.

Mitigation: Configure the key locally in an environment variable or restricted config file; do not send it in chat, and rotate it if already shared.

Risk: Video links are sent to Cue for processing; server retention behavior is unverified, and processing can spend credits.

Mitigation: Submit only links you are permitted to share, check expected credit use, and confirm retention terms with Cue before sending sensitive material.

Risk: Low balances trigger promotional referral or purchase prompts in the workflow.

Mitigation: Treat referral and top-up suggestions as optional and verify current pricing before acting.

## Reference(s):

- [Cue Omni Reader remote endpoint](https://mcp.cuecue.cn/api/omni-reader/mcp/)
- [Cue Omni Reader online experience](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown reports and scripts, with optional structured JSON prompts and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include time-based tables, transcript excerpts, scores, and clearly labeled inferred production details.]

## Skill Version(s):

1.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
