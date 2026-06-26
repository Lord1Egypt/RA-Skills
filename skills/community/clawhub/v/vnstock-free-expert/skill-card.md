## Description: <br>
Runs an end-to-end vnstock workflow for free-tier-safe Vietnam stock valuation, ranking, and API operations with strict rate-limit control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndtchan](https://clawhub.ai/user/ndtchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts and developers use this skill to run a free-tier-safe vnstock workflow for Vietnam stock screening, valuation, ranking, and analyst-style reporting while tracking coverage and missing data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local Python scripts, contact financial data providers, and write result files. <br>
Mitigation: Review commands before execution, run in a controlled workspace, and inspect generated files before reuse. <br>
Risk: The universal invocation helper accepts module, class, method, and argument values that can broaden what code is executed. <br>
Mitigation: Prefer the fixed valuation pipeline scripts and use only trusted vnstock class and method values. <br>
Risk: The skill may read an optional VNSTOCK_API_KEY from the environment or a skill-local .env file. <br>
Mitigation: Store credentials only in local environment configuration, avoid sharing output directories that may reveal run context, and rotate keys if exposure is suspected. <br>
Risk: Financial provider limits, blocking, stale data, or missing fields can affect analysis quality. <br>
Mitigation: Keep free-tier pacing, do not bypass provider blocking with rotating proxies, and report coverage, missing fields, and confidence with any ranking or valuation. <br>
Risk: Brokerage-related connectors or DNSE material could be mistaken for authorization to support real-money trading. <br>
Mitigation: Treat brokerage and trade-execution behavior as out of scope unless explicit controls and authorization are in place. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ndtchan/vnstock-free-expert) <br>
- [VNStock Capability Reference](references/capabilities.md) <br>
- [Free-Tier Playbook](references/free_tier_playbook.md) <br>
- [VNStock Method Matrix](references/method_matrix.md) <br>
- [Vnstock Overview](references/vnstock/01-overview.md) <br>
- [Vnstock Installation and API Key Configuration](references/vnstock/02-installation.md) <br>
- [Vnstock Insiders Program](https://vnstocks.com/insiders-program) <br>
- [Vnstock Login](https://vnstocks.com/login) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON/CSV output files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local outputs/ files and load optional VNSTOCK_API_KEY.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
