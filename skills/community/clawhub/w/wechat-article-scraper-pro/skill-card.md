## Description: <br>
Provides a paid local Flask workflow advertised for batching WeChat Official Account article collection, storing article records, and exporting generated results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baolige2023](https://clawhub.ai/user/baolige2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators and operations teams can use this skill to run a local web interface for creating WeChat article collection tasks, reviewing generated article records, and exporting results after payment verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags the release as suspicious and reports an exposed payment API key. <br>
Mitigation: Review carefully before installing or paying; remove and rotate the exposed key and load payment credentials from a protected runtime secret. <br>
Risk: The artifact contains mock WeChat article parsing and article content generation while advertising real scraping capabilities. <br>
Mitigation: Treat the skill as a paid demo until real scraping behavior is implemented, tested, and clearly documented. <br>
Risk: Payment behavior and pricing are inconsistent across the documentation and code paths. <br>
Mitigation: Confirm the intended price and billing flow before enabling payment collection. <br>
Risk: The app stores task records, article content, and downloads in local files. <br>
Mitigation: Document storage location, retention, and deletion behavior before using the skill with sensitive or regulated content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baolige2023/wechat-article-scraper-pro) <br>
- [SkillPay billing endpoint](https://skillpay.me/api/v1/billing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with Python Flask code, JSON responses, and local Markdown or spreadsheet exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Flask service on port 5002 and writes exported article data under a local data/downloads directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
