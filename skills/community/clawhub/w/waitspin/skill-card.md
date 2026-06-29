## Description: <br>
Use this skill for WaitSpin, the sponsored wait-state ads CLI and API. Trigger when a user wants to create or manage WaitSpin campaigns, buy prepaid impression blocks, inspect the public market, onboard with email OTP keys, install or check earning surfaces for VS Code, Cursor, Devin Desktop, Claude Code, Antigravity CLI, GitHub Copilot CLI, MiMo Code, OpenCode, Grok Code CLI, or Qoder CLI, inspect wallet/ledger/payout status, or reason about WaitSpin public API, trust boundary, privacy, and shipped vs not-shipped capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nttylock](https://clawhub.ai/user/nttylock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, advertisers, and publishers use this skill to operate WaitSpin campaigns, install supported earning surfaces, inspect wallet and payout readiness, and understand the public API and trust boundary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys or OTP codes could be exposed if copied into logs, screenshots, shell history, source files, issues, or chat output. <br>
Mitigation: Validate OTP codes as exactly 6 digits, keep API keys secret, and pass secrets through a host-agent secret store or tool-scoped environment variables. <br>
Risk: User-supplied emails, codes, URLs, campaign IDs, or ad text could be misused if interpolated into raw shell strings. <br>
Mitigation: Validate inputs and pass real values through structured argv/tool arguments or scoped environment variables instead of raw shell interpolation. <br>
Risk: Installer workflows can modify local editor or CLI configuration. <br>
Mitigation: Run dry-run/status checks where available, resolve conflicts target by target, and avoid overwriting unmanaged config unless the CLI provides an explicit option. <br>
Risk: Wallet or payout results could be overstated if test-mode or readiness previews are treated as live payout proof. <br>
Mitigation: Treat dry-run and confirm-test-transfer output as non-live unless the user provides fresh operator proof. <br>


## Reference(s): <br>
- [WaitSpin Public Site](https://waitspin.com) <br>
- [WaitSpin API Docs](https://waitspin.com/docs) <br>
- [WaitSpin Agent Contract](https://waitspin.com/.well-known/agents.md) <br>
- [WaitSpin Trust Boundary](https://waitspin.com/waitspin/trust) <br>
- [WaitSpin API Base](https://api.waitspin.com) <br>
- [WaitSpin OpenAPI Document](https://waitspin.com/openapi/waitspin-api.openapi.json) <br>
- [WaitSpin ClawHub Skill Page](https://clawhub.ai/nttylock/skills/waitspin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON-oriented command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that require human-supplied OTP codes and tool-scoped secret handling.] <br>

## Skill Version(s): <br>
0.1.17 (source: server release evidence and artifact Source Of Truth) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
