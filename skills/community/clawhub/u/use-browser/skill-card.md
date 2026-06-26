## Description: <br>
Automates browser interactions for social media workflows across Instagram, LinkedIn, and X, including posting, messaging, lead scraping, monitoring, and approved-site data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mathiasthu](https://clawhub.ai/user/mathiasthu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to operate pre-authenticated browser sessions for social media management tasks such as publishing posts, sending messages, extracting leads, and monitoring notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through logged-in social media accounts with broad authority to post, message, engage, and scrape leads. <br>
Mitigation: Use a dedicated VM or browser profile and require manual review for posts, DMs, comments, reposts, connection requests, and scraping batches before execution. <br>
Risk: Persistent sessions and cookie management can expose or prolong access to authenticated accounts. <br>
Mitigation: Avoid cookie export or import unless necessary, store any cookie files in a restricted location, delete exports after use, and close or log out sessions when finished. <br>
Risk: Automated social media engagement or scraping can trigger platform restrictions or create compliance concerns. <br>
Mitigation: Limit batch size, add human-paced delays, stop at CAPTCHA or account restriction prompts, and confirm the activity complies with the relevant platform rules. <br>


## Reference(s): <br>
- [browser-use project homepage](https://github.com/browser-use/browser-use) <br>
- [browser-use skill CLI README](https://github.com/browser-use/browser-use/blob/main/browser_use/skill_cli/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and browser session outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the browser-use binary and user-authenticated browser sessions; commands may return page state, screenshots, extracted text, or cookie data depending on the requested action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
