## Description: <br>
Real Estate Spider helps agents collect Chinese real estate listing data from Anjuke, Soufun, Beike, and Lianjia, including property details and export workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h8296699](https://clawhub.ai/user/h8296699) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill to configure and run authorized real estate data collection workflows, then export property records for analysis. It is intended for targets where the user has permission to collect data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents anti-bot, CAPTCHA-bypass, proxy-rotation, real-cookie, and saved-session workflows against third-party real estate sites. <br>
Mitigation: Install and run it only for targets where collection is clearly permitted; prefer official APIs or licensed datasets. <br>
Risk: Generated session files, screenshots, PDFs, and exports may contain cookies, account state, or protected site content. <br>
Mitigation: Treat generated files as sensitive, store them securely, avoid committing them, and delete them when no longer needed. <br>
Risk: Using bypass or proxy workflows on third-party services may create terms-of-service, legal, or account-access risk. <br>
Mitigation: Avoid those workflows unless explicit authorization and applicable site terms allow them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/h8296699/real-estate-spider) <br>
- [README](artifact/README.md) <br>
- [CAPTCHA strategies](artifact/docs/captcha_strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell and Python examples; generated crawl outputs may be JSON, CSV, Excel, screenshots, or text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and agent-browser; outputs may contain site content, cookies, or saved browser state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
