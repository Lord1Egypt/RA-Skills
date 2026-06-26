## Description: <br>
Tetrac Perp Trader gives agents a multi-exchange perpetuals trading CLI for market data, account checks, order placement, position management, TWAP and DCA ladders, scanner signals, trailing stops, and trading loops through TTC Box. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tetrac-official](https://clawhub.ai/user/tetrac-official) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to let an OpenClaw agent inspect perpetuals markets, check account and position state, and prepare or execute exchange actions with explicit pre-order and retry safeguards. It is intended for users who understand the risk of giving an agent access to live crypto trading credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can interact with real-money crypto trading accounts and requires sensitive TTC Box and exchange credentials. <br>
Mitigation: Install only for intended live trading use, provide least-privilege exchange API keys with withdrawals disabled, keep credentials in environment files rather than config, and require dry-runs plus explicit confirmations before write actions. <br>
Risk: The security evidence says the package needs review because claimed bundled executables may be missing or need verification. <br>
Mitigation: Before running, verify the actual release package contents, launcher, platform binary availability, and file hashes or source package against the expected release. <br>
Risk: The security evidence flags unsafe credential-handling patterns in the API documentation. <br>
Mitigation: Avoid URL-based credential flows, use only trusted TTC Box endpoints over secure transport, rotate exposed credentials, and do not grant broader trading permissions than the task requires. <br>
Risk: Automated loops such as TWAP, market-maker, or trailing-stop watchers can amplify losses or duplicate actions if they continue after ambiguous failures. <br>
Mitigation: Constrain loops by symbol, size, duration, and stop conditions; stop on in-flight write failures; verify balance, positions, and open orders before any retry or resume. <br>


## Reference(s): <br>
- [ClawHub Tetrac Perp Trader skill page](https://clawhub.ai/tetrac-official/tetrac-perp-trader) <br>
- [Project homepage](https://github.com/tetrac-official/tetrac-perp-trader) <br>
- [README](README.md) <br>
- [TTC Box REST API reference](references/api-reference.md) <br>
- [Supported exchanges](references/exchanges.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying CLI can return table, JSON, CSV, or quiet output depending on command flags and TTC_OUTPUT.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
