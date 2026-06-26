## Description: <br>
Unified Apify-based retrieval for TikTok, Instagram, X/Twitter, and YouTube profile, post, and comment data with cross-platform normalization for analysis workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Galaxy-Earth](https://clawhub.ai/user/Galaxy-Earth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect profile, post, and comment data from supported social platforms through Apify and normalize the results for cross-platform analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Apify token is handled in URL query strings. <br>
Mitigation: Use a dedicated or limited Apify token, avoid sharing logs or command output that may contain request URLs, and ask the publisher to move authentication out of query strings. <br>
Risk: Collected social-media data is processed through Apify and may not be appropriate for confidential or regulated investigations. <br>
Mitigation: Use the skill only after organizational approval for Apify processing and review applicable privacy, data-use, and platform requirements. <br>
Risk: Apify actor runs can incur usage costs. <br>
Mitigation: Monitor spending, set practical count limits, and prefer bulk retrieval where the skill documentation identifies it as more cost-effective. <br>


## Reference(s): <br>
- [Apify Actor Quick Reference](references/apify_actors_reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/Galaxy-Earth/social-media-data-hub) <br>
- [Galaxy-Earth publisher profile](https://clawhub.ai/user/Galaxy-Earth) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts return normalized JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and APIFY_TOKEN; output schemas cover normalized posts, profiles, and comments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
