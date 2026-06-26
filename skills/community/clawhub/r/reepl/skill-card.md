## Description: <br>
Manage LinkedIn and Twitter/X content with Reepl, including drafts, publishing, scheduling, contacts, collections, AI images, carousels, and voice-profile maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhibavishi](https://clawhub.ai/user/abhibavishi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and creators use this skill to draft, schedule, publish, and organize LinkedIn and Twitter/X content through their Reepl account. It also helps maintain writing style guidance, contacts, saved content, AI-generated images, and carousel drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, schedule, comment on, delete, and update content or profile state in connected social accounts. <br>
Mitigation: Require explicit user confirmation of exact content, account, target IDs or titles, visibility, and timing before any publish, schedule, comment, delete, contact-list, or voice-profile update. <br>
Risk: The skill requires trusting Reepl with connected LinkedIn and Twitter/X workflows and stored account context. <br>
Mitigation: Install only when the user trusts Reepl for those workflows, and review connected accounts and permissions before using the MCP key. <br>
Risk: Voice-profile updates can persistently change how future content is generated. <br>
Mitigation: Show proposed voice-profile changes before saving them, and do not update locked or user-controlled voice-profile fields unless the user explicitly asks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abhibavishi/reepl) <br>
- [Reepl](https://reepl.io) <br>
- [Reepl Help Center](https://help.reepl.io) <br>
- [MCP Setup Guide](https://mcp.reepl.io) <br>
- [Reepl Chrome Extension](https://chromewebstore.google.com/detail/reepl/geomampobbapgnflneaofdplfomdkejn) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown guidance with JSON-style tool arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Reepl MCP key via REEPL_MCP_KEY; AI image generation may require a linked Gemini API key in Reepl.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
