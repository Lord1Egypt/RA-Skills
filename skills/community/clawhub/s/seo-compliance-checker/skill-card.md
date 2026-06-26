## Description: <br>
Checks Chinese marketing and SEO content for advertising-law risk, banned words, keyword-density issues, and platform-specific optimization opportunities using API-backed scans and bundled shell scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content marketers, ecommerce operators, SEO writers, and agents producing Chinese-language copy use this skill to scan existing drafts or generate platform-aware content for Baidu, Xiaohongshu, Douyin, Taobao, and JD. It helps identify banned-word and advertising-claim risks, suggests safer wording, and reports SEO issues before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User content may be sent to an external API without clear privacy or consent safeguards. <br>
Mitigation: Avoid confidential customer data, unreleased campaigns, regulated business material, and sensitive internal copy unless the publisher provides acceptable privacy and retention terms. <br>
Risk: The suggestions script has an unsafe keyword URL-encoding bug according to the security evidence. <br>
Mitigation: Treat suggestions.sh cautiously until keyword encoding is fixed; avoid untrusted or shell-special keyword inputs and prefer safer manual review or a patched script. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lm203688/seo-compliance-checker) <br>
- [Web app](https://1341839497-jv04655vcs.ap-shanghai.tencentscf.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, generated Chinese content, inline shell commands, and script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled scripts can send text, titles, keywords, and related content to an external API and may enforce a free-tier usage limit.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
