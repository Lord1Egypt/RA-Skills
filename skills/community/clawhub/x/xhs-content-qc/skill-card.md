## Description: <br>
对小红书达人笔记进行品牌词、必带话题、@官号、调性、链接有效性、广告法敏感词和竞品提及的自动化质检，并输出结构化报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wandervine](https://clawhub.ai/user/wandervine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketing and content review teams use this skill to check Xiaohongshu KOL/KOC notes for required brand wording, topics, official account mentions, positive tone, link availability, sensitive advertising claims, and competitor mentions. It also supports explicit maintenance requests for the skill's wordlist and reference files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make HTTP GET requests to public Xiaohongshu or short-link URLs supplied for checking. <br>
Mitigation: Use it only with public links intended for review; avoid internal or private URLs. <br>
Risk: Wordlist replacement or append requests persist and change future quality-check results. <br>
Mitigation: Review requested wordlist changes before allowing edits, and keep each .txt list to one item per line. <br>
Risk: Fetched link content can be incomplete because sites may require login, block requests, or return shell pages. <br>
Mitigation: Treat fetched fields as partial evidence and ask the user to provide title, body, hashtags, account mentions, and links when required fields are missing. <br>


## Reference(s): <br>
- [Brand Name and Official Accounts](references/brand-name-and-official-accounts.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wandervine/xhs-content-qc) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured Markdown quality report; helper scripts may return JSON when fetching linked note content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports PASS, WARNING, FAIL, SKIP, or BLOCKED by review dimension; wordlist files may be updated only on explicit user request.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
