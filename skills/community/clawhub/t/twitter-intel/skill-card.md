## Description: <br>
Twitter keyword search, monitoring, and trend analysis via GraphQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Twitter/X by keyword, monitor configured topics over time, and produce structured trend reports from collected tweets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to Twitter/X browser session cookies. <br>
Mitigation: Use a low-risk account where possible, keep the cookie file out of shared folders and source control, and restrict file permissions. <br>
Risk: The skill depends on unpinned external rnet_twitter.py code. <br>
Mitigation: Review the external code before use and pin or vendor a trusted revision for repeatable operation. <br>
Risk: Scheduled monitoring may store collected tweet data locally. <br>
Mitigation: Review what monitor state and daily output files contain before enabling scheduled collection. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/PHY041/twitter-intel) <br>
- [Publisher Profile](https://clawhub.ai/user/PHY041) <br>
- [Skill Homepage](https://canlah.ai) <br>
- [rnet Twitter Client](https://github.com/PHY041/rnet-twitter-client) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline Python, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide cookie setup, monitoring configuration, search filtering, and trend-report generation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
