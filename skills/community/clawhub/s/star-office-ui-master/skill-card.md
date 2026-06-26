## Description: <br>
Helps an agent deploy and operate a pixel-art office dashboard with multi-agent status visualization, mobile viewing, public access guidance, and optional AI-powered room design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pinke](https://clawhub.ai/user/pinke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent set up a web dashboard that shows an AI assistant's work state, invites other agents through join keys, and exposes the office view locally or through a public tunnel. It also gives configuration guidance for status updates, sidebar access, Gemini image generation, and optional desktop-pet mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local dashboard exposed through a public URL can make status data and dashboard controls reachable by unintended users. <br>
Mitigation: Use public access only when needed, set strong FLASK_SECRET_KEY and ASSET_DRAWER_PASS values first, and restrict who receives the public URL. <br>
Risk: Default or reused join keys can allow unwanted agents to join or push status updates. <br>
Mitigation: Rotate or replace default join keys before deployment and set appropriate expiration and concurrency limits. <br>
Risk: Memo display and agent status details may reveal private local notes or working context. <br>
Mitigation: Avoid putting sensitive information in status details and disable or protect memo display when local notes may contain private data. <br>
Risk: Gemini image generation requires sensitive credentials that may be stored or reachable through the dashboard. <br>
Mitigation: Only enter a Gemini API key after reviewing where it is stored, who can access the dashboard, and whether the deployment is protected. <br>


## Reference(s): <br>
- [Star Office UI README](artifact/README.en.md) <br>
- [Star Office UI Skill](artifact/SKILL.md) <br>
- [Star Office UI Overview](artifact/docs/STAR_OFFICE_UI_OVERVIEW.md) <br>
- [State API](artifact/desktop-pet/STATE_API.md) <br>
- [March 2026 Changelog](artifact/docs/CHANGELOG_2026-03.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands, code snippets, configuration values, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commercial use may require replacing bundled art assets with original assets; optional Gemini image generation requires user-supplied credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
