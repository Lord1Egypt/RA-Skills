## Description: <br>
Real-time social intelligence across TikTok, YouTube Shorts, and Instagram Reels, powered by the Virlo API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arod90](https://clawhub.ai/user/arod90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research short-form video markets, discover trends and creators, analyze campaign opportunities, and set up recurring monitoring across TikTok, YouTube Shorts, and Instagram Reels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requests to Virlo using a configured API key. <br>
Mitigation: Install only when the user intends to use Virlo and is comfortable storing a Virlo API key in the skill configuration. <br>
Risk: Some workflows can spend prepaid Virlo credits or enable optional paid add-ons. <br>
Mitigation: Ask the agent to confirm before paid requests or optional add-ons, and review cost information before proceeding. <br>
Risk: Recurring monitoring jobs can continue consuming prepaid balance over time. <br>
Mitigation: Review active tracking and monitoring jobs periodically, and pause or delete jobs that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/arod90/short-form-market-research-brain) <br>
- [Virlo API Documentation](https://dev.virlo.ai/docs) <br>
- [Virlo Full API Reference for Agents](https://dev.virlo.ai/llms-full.txt) <br>
- [Virlo Pricing](https://dev.virlo.ai/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with API request examples and research summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Virlo API key and may initiate paid or recurring Virlo API requests.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
