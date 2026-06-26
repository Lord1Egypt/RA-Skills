## Description: <br>
Get stock prices, quotes, and compare stocks using Tencent Finance API with no API key required, including US stocks, China A-shares, Hong Kong stocks, and crypto symbols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunerw-dev](https://clawhub.ai/user/sunerw-dev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to check market prices, detailed quotes, comparisons, and symbol searches through Tencent Finance-backed CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock symbols queried with this skill are sent to Tencent Finance. <br>
Mitigation: Avoid submitting confidential watchlists or sensitive symbols unless that network disclosure is acceptable. <br>
Risk: The optional global symlink can expose an executable as a system-wide command. <br>
Mitigation: Create the symlink only after verifying the actual tfin executable or source obtained outside this documentation-only artifact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunerw-dev/tecent-finance-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stock symbols and CLI command examples for Tencent Finance queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
