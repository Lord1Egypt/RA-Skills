## Description: <br>
Star Office UI helps agents deploy and operate a pixel office dashboard for multi-agent status visualization, mobile viewing, invitations, and public access. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[DponXiaodong](https://clawhub.ai/user/DponXiaodong) <br>

### License/Terms of Use: <br>
MIT code; non-commercial art assets <br>


## Use Case: <br>
Developers and agent operators use this skill to set up a collaborative pixel office dashboard, update agent status, invite additional agents, and view short daily status summaries. It is best suited for demonstration and learning scenarios because the bundled art assets are described as non-commercial. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages public exposure of a local dashboard while handling local notes and agent controls without enough access control or security guidance. <br>
Mitigation: Install only in a trusted local or access-protected environment, and add authentication before exposing the dashboard publicly. <br>
Risk: Default join keys and unrestricted state-changing endpoints can allow unwanted agent joins or status changes if the service is reachable by untrusted users. <br>
Mitigation: Replace and rotate default join keys, restrict state-changing endpoints, and approve only expected agents. <br>
Risk: The yesterday memo feature reads local memory files and may expose sensitive information despite basic sanitization. <br>
Mitigation: Disable the memo feature or sanitize memory content before enabling it in any shared or public deployment. <br>
Risk: Bundled art assets are described as non-commercial and include fan-created content tied to third-party IP. <br>
Mitigation: Use the bundled assets only for learning or demonstration, and replace them with original or properly licensed art before commercial use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/DponXiaodong/star-office-ui) <br>
- [Star Office UI README](artifact/README.md) <br>
- [Star Office UI overview](artifact/docs/STAR_OFFICE_UI_OVERVIEW.md) <br>
- [Release feature notes](artifact/docs/FEATURES_NEW_2026-03-01.md) <br>
- [LimeZu Animated Mini Characters 2 asset page](https://limezu.itch.io/animated-mini-characters-2-platform-free) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with shell commands, API payload examples, and file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and operation instructions for a local Flask-backed dashboard, join-key based agent invitations, status updates, and optional public tunnel access.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
