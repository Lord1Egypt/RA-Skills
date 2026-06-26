## Description: <br>
Social Intel Hub gathers social media search results across supported platforms, analyzes engagement and topic trends, and can generate word clouds, exports, comparison reports, and LLM-ready insight prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kk-kingkong](https://clawhub.ai/user/kk-kingkong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators can use this skill to collect public social media data, compare topics or competitors, review trend signals, and prepare exports or prompts for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to configured mcporter/TikHub services. <br>
Mitigation: Avoid confidential keywords and only run searches that are appropriate to send to those services. <br>
Risk: Collected posts, comments, usernames, URLs, and exports may contain personal content. <br>
Mitigation: Review generated files before sharing them and handle exported CSV, Excel, and PNG outputs according to applicable privacy requirements. <br>
Risk: Cached search results may remain locally under /tmp/social_intel_cache for up to 24 hours. <br>
Mitigation: Use --no-cache for sensitive searches and clear /tmp/social_intel_cache when cached social content should not persist. <br>


## Reference(s): <br>
- [Social Intel Hub on ClawHub](https://clawhub.ai/kk-kingkong/social-intel) <br>
- [Publisher profile: kk-kingkong](https://clawhub.ai/user/kk-kingkong) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Console text, Markdown-style reports, CSV, Excel, PNG word clouds, and LLM-ready prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cache retrieved social content for 24 hours under /tmp/social_intel_cache and can write exports under /tmp/social_intel or a user-provided output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
