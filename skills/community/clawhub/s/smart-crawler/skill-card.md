## Description: <br>
Smart Crawler helps agents perform web crawling and data extraction with static, batch, and dynamic browser-based crawling support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to fetch webpages, extract structured data with selectors, run batch crawls, and handle dynamic pages through browser automation. It is intended for authorized crawling workflows with conservative operating boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The crawler may be used against sites where crawling or automated access is not authorized. <br>
Mitigation: Use it only on sites where crawling is permitted, and enforce explicit scope, rate limits, and access-policy checks before running jobs. <br>
Risk: Proxy and anti-detection behavior can bypass site controls or violate acceptable-use limits. <br>
Mitigation: Disable proxy and anti-detection modes unless they are explicitly authorized for the target environment. <br>
Risk: Dynamic browser automation and third-party dependencies increase execution and supply-chain risk. <br>
Mitigation: Review scripted browser actions before execution and install dependencies in an isolated environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/smart-crawler) <br>
- [Project Homepage](https://github.com/openclaw/smart-crawler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce crawler configuration, extraction rules, usage guidance, and runnable code snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
