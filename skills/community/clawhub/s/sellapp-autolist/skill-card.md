## Description: <br>
Auto-creates digital products on SellApp using the v2 API, maintaining a catalog of digital products and listing missing items publicly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and storefront operators use this skill to create or sync a small catalog of digital products on a SellApp account through an agent-run Python script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create public SellApp storefront products using the user's API key without a clear confirmation or draft-first step. <br>
Mitigation: Use a test SellApp account or restricted API key first, verify catalog entries and prices, and add a dry-run or explicit confirmation before creating public listings. <br>


## Reference(s): <br>
- [SellApp API documentation](https://sell.app/docs/api) <br>
- [ClawHub skill page](https://clawhub.ai/ssidharhubble/sellapp-autolist) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and agent-run Python/API actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates public SellApp product listings when executed with a valid SELLAPP_API_KEY.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
