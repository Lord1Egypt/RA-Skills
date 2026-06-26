## Description: <br>
Star Office helps an agent deploy and operate a pixel-art office dashboard with multi-agent status visualization, mobile viewing, public access, and optional AI room redesign. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18153](https://clawhub.ai/user/18153) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent set up a local or publicly shared AI office dashboard, push assistant status updates, invite other agents, and configure optional room-design features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard may be exposed publicly while using weak default secrets or the default sidebar password. <br>
Mitigation: Set strong FLASK_SECRET_KEY and ASSET_DRAWER_PASS values, replace the default 1234 password, and restrict public access with Cloudflare Access, basic authentication, or IP allowlists. <br>
Risk: Shared status text and yesterday memo files may reveal private work details. <br>
Mitigation: Review and limit status messages and memo content before sharing the dashboard outside a trusted audience. <br>
Risk: Gemini API credentials are entered into and used by the server-side application. <br>
Mitigation: Configure a Gemini API key only when that storage and usage model is acceptable, protect runtime configuration files, and rotate the key if exposure is suspected. <br>
Risk: Desktop wrappers and asset upload or editing surfaces are experimental/admin-oriented areas. <br>
Mitigation: Treat those features as trusted-admin workflows and avoid enabling them for untrusted users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18153/star-office) <br>
- [Publisher profile](https://clawhub.ai/user/18153) <br>
- [SKILL.md](SKILL.md) <br>
- [README.en.md](README.en.md) <br>
- [Guest onboarding skill](frontend/join-office-skill.md) <br>
- [Desktop pet state API](desktop-pet/STATE_API.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash and Python snippets plus configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local setup commands, environment variables, dashboard URLs, and status-push configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
