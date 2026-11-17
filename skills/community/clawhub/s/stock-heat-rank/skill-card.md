## Description:

Stock Heat Rank collects A-share popularity rankings from Wencai, Xueqiu, and Eastmoney and returns a composite market heat ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n1e](https://clawhub.ai/user/n1e)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-analysis agents use this skill to identify currently popular A-share stocks by comparing rankings across Wencai, Xueqiu, and Eastmoney. It is useful for market attention monitoring, hot-stock discovery, and limit-up heat analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A large obfuscated JavaScript signer and mutable npm dependencies execute locally with the user's permissions.

Mitigation: Review before installing, run only in a restricted environment, avoid elevated privileges, and prefer a release with readable signer source, pinned dependencies, a committed lockfile, and documented sandboxing.

Risk: The skill depends on live third-party market websites and API responses that can fail or change.

Mitigation: Treat results as current best-effort market-attention signals and review collection failures or parser errors before relying on the ranking.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/n1e/skills/stock-heat-rank)
- [Publisher Profile](https://clawhub.ai/user/n1e)
- [Wencai](https://www.iwencai.com/)
- [Xueqiu Hot Stock Page](https://xueqiu.com/hot/stock)
- [Eastmoney Stock Rank Endpoint](https://emappdata.eastmoney.com/stockrank/getAllCurrentList)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Console table or JSON array with stock code, name, platform ranks, composite score, and appearance count]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports a top-N option and table or JSON output format.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
