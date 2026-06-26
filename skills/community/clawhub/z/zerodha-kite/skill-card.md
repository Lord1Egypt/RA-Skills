## Description: <br>
Route natural-language trading and account queries to the correct `zerodha` CLI command with exact flags, validation constraints, and synonym mapping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jatinbansal1998](https://clawhub.ai/user/jatinbansal1998) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading workflow users use this skill to translate plain-English Zerodha Kite account, market data, portfolio, authentication, and order-management requests into validated CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated commands can place, modify, cancel, or exit brokerage orders. <br>
Mitigation: Review every generated order command before execution, especially side, symbol, quantity, price, product, and order type. <br>
Risk: Authentication and profile commands can expose API keys, API secrets, request tokens, or refresh tokens. <br>
Mitigation: Treat credentials and tokens as sensitive, avoid logging or sharing them, and verify the target profile before running credential commands. <br>
Risk: Bootstrap commands pipe installer scripts from an unpinned GitHub branch directly to shell or PowerShell. <br>
Mitigation: Install only from a trusted Zerodha CLI source, and prefer reviewing or pinning the installer before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jatinbansal1998/zerodha-kite) <br>
- [Linux/macOS installer script referenced by the skill](https://raw.githubusercontent.com/jatinbansal1998/zerodha-kite-cli/main/scripts/install.sh) <br>
- [Windows installer script referenced by the skill](https://raw.githubusercontent.com/jatinbansal1998/zerodha-kite-cli/main/scripts/install.ps1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Structured text with command, why, and missing fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs the next runnable command or the required missing inputs; may include installer commands for bootstrap flows.] <br>

## Skill Version(s): <br>
v1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
