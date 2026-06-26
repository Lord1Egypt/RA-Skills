## Description: <br>
Enables an OpenClaw agent to handle web research and browser-backed web interaction through search, page reading, logged-in Chrome sessions, dynamic page inspection, and real browser UI operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ysyyrps777](https://clawhub.ai/user/ysyyrps777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill when an agent needs to find, read, verify, or act on web content, including dynamic sites, logged-in pages, JavaScript-rendered pages, and browser UI flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a user's real logged-in Chrome session and may access account-specific or sensitive pages. <br>
Mitigation: Use a separate Chrome profile with only the accounts needed for the task, keep actions scoped to the user's request, and avoid existing user tabs unless necessary. <br>
Risk: Browser automation can perform write actions such as uploads, posts, purchases, submissions, deletes, or account changes. <br>
Mitigation: Require explicit user confirmation before any write action and prefer read-only inspection until the user approves the action. <br>
Risk: Screenshots and downloaded page assets can capture sensitive information from logged-in sessions. <br>
Mitigation: Save screenshots or files only when required for the task, place them in task-appropriate temporary locations, and ask before capturing sensitive pages. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ysyyrps777/web-access-openclaw) <br>
- [CDP Proxy API reference](references/cdp-api.md) <br>
- [README](README.md) <br>
- [Attribution](ATTRIBUTION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, shell commands, JSON API responses, screenshots, and local files as needed for browser-backed tasks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and close browser tabs, run local Node.js scripts, call a local CDP HTTP API, upload local files through browser controls, and save screenshots when explicitly needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
