## Description:

Valu Ai helps agents generate DCF-based stock valuation analysis for Chinese A-share and selected Hong Kong-listed companies, including single-stock reports and batch comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoxiang603](https://clawhub.ai/user/gaoxiang603)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, analysts, and finance-focused agent users use this skill to create AI-assisted valuation reports for A-share and selected Hong Kong stocks. It gathers market and financial data, applies DCF and relative valuation framing, and produces single-company or 2-5 stock comparison reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends generated valuation prompts and report context to DeepSeek and uses external market-data services.

Mitigation: Run only in trusted environments, configure API credentials through environment variables, and avoid including confidential portfolio, account, or personal financial data in prompts.

Risk: The skill stores local reports, logs, quota, billing, and user-state files with weak controls.

Mitigation: Do not rely on the local quota or billing files for production payment enforcement; add strong authentication, access control, and auditable billing before commercial deployment.

Risk: Generated valuation reports may be incomplete, inaccurate, or mistaken for financial advice.

Mitigation: Require human review by a qualified user, preserve the investment-risk disclaimer, and verify market and financial assumptions before using a report for decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gaoxiang603/skills/valu-ai)
- [DeepSeek API Keys](https://platform.deepseek.com/api-keys)
- [DeepSeek Chat Completions Endpoint](https://api.deepseek.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown valuation reports and comparison summaries, with local report files when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include disclaimers and should be treated as AI-assisted drafts rather than licensed financial advice.]

## Skill Version(s):

2.1.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
